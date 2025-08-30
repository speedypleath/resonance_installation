"""Emotion recognition pipeline."""

import cv2
import mediapipe as mp
import numpy as np
import time
import threading
from typing import Any, Optional
from PIL import Image

from .base import BiometricPipeline, PipelineResult
from ..models.base import FaceModel
from ..osc.osc_client import get_osc_client
from ..utils.image_processing import get_face_box


class FacePipeline(BiometricPipeline):
    """Pipeline for real-time emotion recognition from webcam."""
    
    def __init__(self, model: FaceModel,
                 camera_id: int = 0, target_fps: int = 15, confidence_threshold: float = 0.2,
                 prediction_fps: float = 2.0):        
        
        super().__init__("facial_emotion", model)
        
        # Initialize OSC client for centralized OSC output
        self.osc_client = get_osc_client()
        self.camera_id = camera_id
        self.target_fps = target_fps
        self.frame_interval = 1.0 / target_fps
        self.confidence_threshold = confidence_threshold
        
        # Prediction rate limiting (2Hz by default)
        self.prediction_fps = prediction_fps
        self.prediction_interval = 1.0 / prediction_fps
        self.last_prediction_time = 0.0
        self.last_prediction_result = None
        
        # MediaPipe face detection with lower thresholds
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=False,
            min_detection_confidence=0.3,  # Lowered from 0.5
            min_tracking_confidence=0.3    # Lowered from 0.5
        )
        
        # Camera setup with thread safety
        self.cap = None
        self.camera_lock = threading.Lock()  # Protect camera access
        self.last_process_time = 0.0
        self.frame_count = 0
        self.last_emotion = "Neutral"
        self.last_confidence = 0.0
        self.no_face_count = 0  # Track consecutive frames with no face
        self.last_face_time = 0.0  # Last time a face was detected
    
    def start(self) -> bool:
        """Start the emotion recognition pipeline."""
        # Initialize camera here, not in __init__
        print(f"Attempting to open camera {self.camera_id}...")
        self.cap = cv2.VideoCapture(self.camera_id)
        
        if not self.cap.isOpened():
            print(f"Error: Could not open camera {self.camera_id}")
            # Try a few different camera IDs
            for alt_id in [1, 2, -1]:
                print(f"Trying camera {alt_id}...")
                self.cap = cv2.VideoCapture(alt_id)
                if self.cap.isOpened():
                    print(f"Success: Using camera {alt_id}")
                    self.camera_id = alt_id
                    break
            else:
                print("Failed to open any camera")
                return False
        
        # Test frame capture
        ret, test_frame = self.cap.read()
        if not ret:
            print("Camera opened but cannot read frames")
            self.cap.release()
            return False
        
        print(f"Camera {self.camera_id} working - Frame shape: {test_frame.shape}")
        
        # Set camera properties for better performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        return super().start()
    
    def _get_run_loop(self):
        """Override to use camera capture loop instead of queue-based loop."""
        return self._camera_capture_loop
    
    def _camera_capture_loop(self) -> None:
        """Main camera capture and processing loop."""
        print(f"Starting emotion recognition loop at {self.target_fps}Hz...")
        
        frame_skip_count = 0
        max_consecutive_failures = 30  # Allow 2 seconds of failures at 15fps
        
        while not self._stop_event.is_set():
            try:
                # Wait if paused
                if self._pause_event.is_set():
                    time.sleep(0.1)
                    continue
                
                current_time = time.time()
                
                # Capture frame from camera
                frame = self.capture_frame()
                if frame is None:
                    frame_skip_count += 1
                    if frame_skip_count > max_consecutive_failures:
                        print(f"ERROR: Failed to capture {frame_skip_count} consecutive frames. Camera may be disconnected.")
                        # Try to reconnect camera
                        if not self._reconnect_camera():
                            print("Camera reconnection failed. Pipeline stopping.")
                            break
                        frame_skip_count = 0
                    time.sleep(0.01)
                    continue
                
                frame_skip_count = 0  # Reset failure counter on successful frame
                
                # Process at target FPS
                if current_time - self.last_process_time >= self.frame_interval:
                    try:
                        result = self.process_data(frame)
                        
                        if not result:
                            continue

                        # Update statistics
                        self.process_count += 1
                        if not result.success:
                            self.error_count += 1
                        
                        # Send to output queue for web interface (non-blocking)
                        try:
                            self.output_queue.put(result, block=False)
                        except Exception as e:
                            # Queue full, clear old results
                            try:
                                self.output_queue.get_nowait()
                                self.output_queue.put(result, block=False)
                            except Exception as e:
                                print(f"Error managing output queue: {e}")
                                pass  # Skip if still can't add
                        
                        # Call result callbacks (for web interface updates)
                        for callback in self.result_callbacks:
                            try:
                                callback(result)
                            except Exception as e:
                                print(f"Error in result callback: {e}")
                        
                        # Send OSC data if successful
                        if result.success:
                            try:
                                self._send_osc_data(result)
                            except Exception as e:
                                print(f"Error sending OSC data: {e}")
                        
                        # Enhanced console logging
                        if result.success:
                            if self.process_count % 30 == 0:  # Every 2 seconds
                                self._print_emotion_result(result)
                        else:
                            self._log_processing_issue(result)
                        
                        self.last_process_time = current_time
                        self.frame_count += 1
                        
                    except Exception as e:
                        print(f"Error processing frame: {e}")
                        self.error_count += 1
                        continue
                
                # Small sleep to prevent CPU spinning
                time.sleep(0.001)
                
            except Exception as e:
                print(f"Critical error in emotion pipeline: {e}")
                import traceback
                traceback.print_exc()
                time.sleep(0.1)
        
        print("Emotion recognition loop ended")
    
    def _reconnect_camera(self) -> bool:
        """Attempt to reconnect to the camera with thread safety."""
        print("Attempting camera reconnection...")
        
        with self.camera_lock:
            # Safely release existing camera
            if self.cap:
                try:
                    self.cap.release()
                except Exception as e:
                    print(f"Warning: Error releasing camera: {e}")
                self.cap = None
            
            # Try original camera ID first
            try:
                self.cap = cv2.VideoCapture(self.camera_id)
                if self.cap.isOpened():
                    ret, test_frame = self.cap.read()
                    if ret:
                        print(f"Camera {self.camera_id} reconnected successfully")
                        return True
                    else:
                        self.cap.release()
                        self.cap = None
            except Exception as e:
                print(f"Error testing camera {self.camera_id}: {e}")
                if self.cap:
                    self.cap.release()
                    self.cap = None
            
            # Try alternative camera IDs
            for alt_id in [0, 1, 2, -1]:
                if alt_id == self.camera_id:
                    continue
                    
                print(f"Trying camera {alt_id}...")
                try:
                    self.cap = cv2.VideoCapture(alt_id)
                    if self.cap.isOpened():
                        ret, test_frame = self.cap.read()
                        if ret:
                            print(f"Switched to camera {alt_id}")
                            self.camera_id = alt_id
                            return True
                        else:
                            self.cap.release()
                            self.cap = None
                    else:
                        if self.cap:
                            self.cap.release()
                            self.cap = None
                except Exception as e:
                    print(f"Error testing camera {alt_id}: {e}")
                    if self.cap:
                        try:
                            self.cap.release()
                        except Exception as e:
                            print(f"Error releasing camera: {e}")
                        self.cap = None
            
            print("Camera reconnection failed")
            return False
    
    def _log_processing_issue(self, result: PipelineResult) -> None:
        """Log processing issues with appropriate frequency."""
        if not result.success:
            error_msg = result.error_message
            metadata = result.metadata
            
            if "no_face_detected" in metadata:
                # Log no face detection every 5 seconds or every 50 frames
                if (self.no_face_count % 75 == 1 or  # Every 5 seconds at 15fps
                    time.time() - self.last_face_time > 10):  # Or every 10 seconds
                    
                    time_since = time.time() - self.last_face_time if self.last_face_time > 0 else 0
                    timestamp_str = time.strftime("%H:%M:%S", time.localtime(result.timestamp))
                    
                    print(f"[{timestamp_str}] No face detected (count: {self.no_face_count}, "
                          f"last seen: {time_since:.1f}s ago)")
            
            elif "face_too_small" in metadata:
                # Log small face detections occasionally
                if self.process_count % 45 == 0:  # Every 3 seconds
                    timestamp_str = time.strftime("%H:%M:%S", time.localtime(result.timestamp))
                    face_size = metadata.get("face_size", "unknown")
                    print(f"[{timestamp_str}] Face detected but too small: {face_size}")
            
            elif "low_confidence" in metadata:
                # Log low confidence occasionally
                if self.process_count % 60 == 0:  # Every 4 seconds
                    timestamp_str = time.strftime("%H:%M:%S", time.localtime(result.timestamp))
                    threshold = metadata.get("threshold", self.confidence_threshold)
                    print(f"[{timestamp_str}] Face detected but confidence below {threshold:.1%}")
            
            else:
                # Log other errors immediately
                timestamp_str = time.strftime("%H:%M:%S", time.localtime(result.timestamp))
                print(f"[{timestamp_str}] Processing error: {error_msg}")
    
    def _print_emotion_result(self, result: PipelineResult) -> None:
        """Print emotion recognition result to console with enhanced info."""
        timestamp_str = time.strftime("%H:%M:%S", time.localtime(result.timestamp))
        emotion = result.predictions["emotion"]
        confidence = result.predictions["confidence"]
        
        # Calculate actual FPS
        actual_fps = self._calculate_fps()
        
        print(f"[{timestamp_str}] {emotion} ({confidence:.2%}) | FPS: {actual_fps:.1f} | Processed: {self.process_count}")
        
        if "vad" in result.predictions:
            vad = result.predictions["vad"]
            print(f"             VAD: V={vad['valence']:.2f}, A={vad['arousal']:.2f}, D={vad['dominance']:.2f}")
        
        # Show face detection health
        face_health = "Good" if self.no_face_count < 10 else "Poor"
        print(f"             Face detection: {face_health} (no-face count: {self.no_face_count})")
        
        if "probabilities" in result.predictions and self.process_count % 150 == 0:  # Every 10 seconds
            print("             All probabilities:")
            for emotion_name, prob in result.predictions["probabilities"].items():
                marker = " ←" if emotion_name == emotion else ""
                print(f"               {emotion_name:>9}: {prob:.3f} ({prob*100:.1f}%){marker}")
        
        print()  # Empty line for readability
    
    def stop(self) -> None:
        """Stop the pipeline and release camera."""
        print(f"Stopping {self.name} pipeline...")
        
        # Stop the parent pipeline first
        super().stop()
        
        # Clean up camera resources with thread safety
        with self.camera_lock:
            if self.cap:
                try:
                    print("Releasing camera...")
                    self.cap.release()
                    self.cap = None
                    
                    # Clean up OpenCV windows
                    cv2.destroyAllWindows()
                    
                    # Give time for resources to be released
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"Warning: Error releasing camera: {e}")
                    self.cap = None
        
        print(f"{self.name} pipeline stopped")
    
    def validate_input(self, data: Any) -> bool:
        """Validate input frame data."""
        return isinstance(data, np.ndarray) and len(data.shape) == 3
    
    def process_data(self, frame: np.ndarray) -> PipelineResult:
        """Process a single frame for emotion recognition."""
        timestamp = time.time()
        
        try:
            h, w = frame.shape[:2]
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detect faces
            results = self.face_mesh.process(frame_rgb)
            
            if results.multi_face_landmarks:
                self.no_face_count = 0  # Reset no-face counter
                self.last_face_time = timestamp
                
                for face_landmarks in results.multi_face_landmarks:
                    # Get face bounding box
                    bbox = get_face_box(face_landmarks, w, h)
                    startX, startY, endX, endY = bbox
                    
                    # Validate face region size
                    face_width = endX - startX
                    face_height = endY - startY
                    
                    if face_width < 30 or face_height < 30:
                        # Face too small
                        return PipelineResult(
                            timestamp=timestamp,
                            data_type="facial",
                            predictions={
                                "emotion": self.last_emotion,
                                "confidence": self.last_confidence,
                                "vad": {"valence": 0.0, "arousal": 0.0, "dominance": 0.0}
                            },
                            raw_data={"frame": frame, "bbox": bbox},
                            metadata={"face_too_small": True, "face_size": (face_width, face_height)},
                            success=False,
                            error_message=f"Face too small: {face_width}x{face_height}px"
                        )
                    
                    # Extract face region
                    face_region = frame_rgb[startY:endY, startX:endX]
                    
                    if face_region.size == 0:
                        continue
                    
                    # Check if it's time to make a new prediction (2Hz rate limiting)
                    should_predict = (timestamp - self.last_prediction_time) >= self.prediction_interval
                    
                    if should_predict:
                        # Convert to PIL and predict emotion
                        face_image = Image.fromarray(face_region)
                        prediction = self.model.predict(face_image)
                        self.last_prediction_time = timestamp
                        self.last_prediction_result = prediction
                    else:
                        # Use cached prediction
                        prediction = self.last_prediction_result if self.last_prediction_result else {
                            "emotion": self.last_emotion,
                            "confidence": self.last_confidence,
                            "vad": {"valence": 0.0, "arousal": 0.0, "dominance": 0.0},
                            "probabilities": {}
                        }
                    
                    # Only send results when we made a new prediction
                    if should_predict:
                        # Check confidence threshold
                        if prediction["confidence"] >= self.confidence_threshold:
                            self.last_emotion = prediction["emotion"]
                            self.last_confidence = prediction["confidence"]
                            
                            return PipelineResult(
                                timestamp=timestamp,
                                data_type="facial",
                                predictions=prediction,
                                raw_data={"frame": frame, "bbox": bbox},
                                metadata={
                                    "frame_size": (w, h),
                                    "face_region_size": face_region.shape,
                                    "processing_fps": self._calculate_fps(),
                                    "face_detected": True,
                                    "prediction_fps": self.prediction_fps
                                },
                                success=True
                            )
                        else:
                            # Low confidence on new prediction
                            return PipelineResult(
                                timestamp=timestamp,
                                data_type="facial",
                                predictions=prediction,
                                raw_data={"frame": frame, "bbox": bbox},
                                metadata={
                                    "low_confidence": True,
                                    "threshold": self.confidence_threshold,
                                    "prediction_fps": self.prediction_fps
                                },
                                success=False,
                                error_message=f"Confidence {prediction['confidence']:.2%} below threshold {self.confidence_threshold:.2%}"
                            )
                    
                    # No new prediction made, return last known prediction but don't trigger callbacks/OSC
                    return PipelineResult(
                        timestamp=timestamp,
                        data_type="facial",
                        predictions={
                            "emotion": self.last_emotion,
                            "confidence": self.last_confidence,
                            "vad": self.last_prediction_result.get("vad", {"valence": 0.0, "arousal": 0.0, "dominance": 0.0}) if self.last_prediction_result else {"valence": 0.0, "arousal": 0.0, "dominance": 0.0},
                            "probabilities": self.last_prediction_result.get("probabilities", {}) if self.last_prediction_result else {}
                        },
                        raw_data={"frame": frame, "bbox": bbox},
                        metadata={
                            "face_detected": True,
                            "prediction_skipped": True,
                            "prediction_fps": self.prediction_fps
                        },
                        success=True,  # Show as successful to avoid error display
                        error_message=None
                    )
            
            # No face detected
            self.no_face_count += 1
            time_since_face = timestamp - self.last_face_time if self.last_face_time > 0 else 0
            
            return PipelineResult(
                timestamp=timestamp,
                data_type="facial",
                predictions={
                    "emotion": self.last_emotion,
                    "confidence": self.last_confidence,
                    "vad": {"valence": 0.0, "arousal": 0.0, "dominance": 0.0}
                },
                raw_data={"frame": frame, "bbox": None},
                metadata={
                    "no_face_detected": True,
                    "no_face_count": self.no_face_count,
                    "time_since_face": time_since_face,
                    "frame_size": (w, h)
                },
                success=False,
                error_message="No face detected"
            )
            
        except Exception as e:
            return PipelineResult(
                timestamp=timestamp,
                data_type="facial",
                predictions={},
                raw_data={"frame": frame},
                metadata={},
                success=False,
                error_message=str(e)
            )
    
    def _calculate_fps(self) -> float:
        """Calculate actual processing FPS."""
        current_time = time.time()
        if self.last_process_time > 0:
            fps = 1.0 / (current_time - self.last_process_time)
        else:
            fps = 0.0
        self.last_process_time = current_time
        return fps
    
    def _send_osc_data(self, result: PipelineResult) -> None:
        """Send emotion data via OSC client."""
        if result.success and "vad" in result.predictions:
            vad = result.predictions["vad"]
            # Send to OSC client instead of direct OSC
            self.osc_client.update_facial(
                vad["valence"], vad["arousal"], vad["dominance"]
            )
    
    def _run_loop(self) -> None:
        """Main processing loop with automatic camera capture."""
        print(f"Starting emotion recognition loop at {self.target_fps}Hz...")
        
        while not self._stop_event.is_set():
            try:
                # Wait if paused
                if self._pause_event.is_set():
                    time.sleep(0.1)
                    continue
                
                current_time = time.time()
                
                # Capture frame from camera
                frame = self.capture_frame()
                if frame is None:
                    time.sleep(0.01)  # Brief pause if no frame
                    continue
                
                # Process at target FPS
                if current_time - self.last_process_time >= self.frame_interval:
                    # Process frame directly
                    result = self.process_data(frame)
                    
                    # Update statistics
                    self.process_count += 1
                    if not result.success:
                        self.error_count += 1
                    
                    # Send to output queue for web interface
                    try:
                        self.output_queue.put(result, timeout=0.01)
                    except Exception as e:
                        print(f"Error putting result in output queue: {e}")
                        pass  # Queue full, skip
                    
                    # Call result callbacks (for web interface updates)
                    for callback in self.result_callbacks:
                        try:
                            callback(result)
                        except Exception as e:
                            print(f"Error in result callback: {e}")
                    
                    # Send OSC data if successful
                    if result.success and self.osc_client:
                        self._send_osc_data(result)

                    # Send OSC label every 5 seconds
                    if self.process_count % (self.target_fps * 5) == 0:
                        if "emotion" in result.predictions:
                            self.osc_client.send_facial_label(result.predictions["emotion"])
                    
                    # Print to console
                    if result.success:
                        self._print_emotion_result(result)
                    
                    self.last_process_time = current_time
                    self.frame_count += 1
                
            except Exception as e:
                self.error_count += 1
                print(f"Error in emotion pipeline: {e}")
                time.sleep(0.1)
    
    def capture_frame(self) -> Optional[np.ndarray]:
        """Capture a single frame from camera with thread safety."""
        with self.camera_lock:
            if not self.cap or not self.cap.isOpened():
                return None
            
            try:
                ret, frame = self.cap.read()
                return frame if ret else None
            except Exception as e:
                print(f"Error capturing frame: {e}")
                return None
    
    def run_webcam_loop(self, show_display: bool = True) -> None:
        """Run continuous webcam emotion recognition."""
        if not self.start():
            return
        
        print(f"Starting emotion recognition at {self.target_fps}Hz...")
        print("Press 'q' to quit")
        
        try:
            while self.is_running:
                current_time = time.time()
                
                # Capture frame
                frame = self.capture_frame()
                if frame is None:
                    print("Warning: Could not capture frame")
                    continue
                
                # Process at target FPS
                if current_time - self.last_process_time >= self.frame_interval:
                    # Process frame directly instead of using queue
                    result = self.process_data(frame)
                    
                    if result.success:
                        self._print_emotion_result(result)
                        
                        # Send data to OSC client
                        if "vad" in result.predictions:
                            vad = result.predictions["vad"]
                            self.osc_client.update_facial(
                                vad["valence"], vad["arousal"], vad["dominance"]
                            )
                    else:
                        print(f"Processing failed: {result.error_message}")
                    
                    self.frame_count += 1
                    self.last_process_time = current_time
                
                # Display frame
                if show_display:
                    self._display_frame(frame, result if 'result' in locals() else None)
                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                        
        except KeyboardInterrupt:
            print("\nStopping emotion recognition...")
        finally:
            self.stop()
    
    def _display_frame(self, frame: np.ndarray, result: Optional[PipelineResult] = None) -> None:
        """Display frame with emotion overlay."""
        display_frame = frame.copy()
        
        if result and result.success and result.raw_data.get("bbox"):
            bbox = result.raw_data["bbox"]
            startX, startY, endX, endY = bbox
            
            emotion = result.predictions["emotion"]
            print(f"Detected emotion: {emotion}")
            print(f"Confidence: {result.predictions['confidence']:.1%}")
            print(result.predictions)
            confidence = result.predictions["confidence"]
            
            # Draw bounding box and label
            cv2.rectangle(display_frame, (startX, startY), (endX, endY), (255, 0, 255), 2)
            label = f"{emotion} {confidence:.1%}"
            cv2.putText(display_frame, label, (startX, startY-10), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
        
        cv2.imshow('Emotion Recognition', display_frame)
    
    def _print_emotion_result(self, result: PipelineResult) -> None:
        """Print emotion recognition result to console."""
        timestamp_str = time.strftime("%H:%M:%S", time.localtime(result.timestamp))
        emotion = result.predictions["emotion"]
        confidence = result.predictions["confidence"]
        
        print(f"[{timestamp_str}] Primary: {emotion} ({confidence:.2%})")
        
        if "vad" in result.predictions:
            vad = result.predictions["vad"]
            print(f"Weighted Valence: {vad['valence']:.3f}, "
                  f"Arousal: {vad['arousal']:.3f}, "
                  f"Dominance: {vad['dominance']:.3f}")
        
        if "probabilities" in result.predictions:
            print("  All probabilities:")
            for emotion_name, prob in result.predictions["probabilities"].items():
                print(f"    {emotion_name:>9}: {prob:.3f} ({prob*100:.1f}%)")
        
        print()  # Empty line for readability