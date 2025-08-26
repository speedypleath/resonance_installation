"""GSR stress detection pipeline."""

import numpy as np
import time
from typing import Any, Dict, List, Optional, Tuple
from collections import deque
from datetime import datetime, timezone
from pylsl import StreamInlet, resolve_byprop
import tensorflow 
from .base import BiometricPipeline, PipelineResult
from ..models.gsr import GSRStressModel
from ..osc.osc_client import OSCClient


class GSRPipeline(BiometricPipeline):
    """Pipeline for real-time GSR stress detection and data processing."""
    
    def __init__(self, model: GSRStressModel, osc_client: Optional[OSCClient] = None,
                 window_size: float = 20.0, window_step: float = 10.0,
                 stream_name: str = "GSR", stream_type: str = "GSR"):
        
        super().__init__("gsr_stress_detection", model, osc_client)
        
        # Use model's configured parameters
        self.sampling_rate = model.sampling_rate  # 4Hz from training
        self.window_size = window_size            # 20s analysis windows
        self.window_step = window_step            # 10s step between analyses
        self.stream_name = stream_name
        self.stream_type = stream_type
        
        # Calculate buffer sizes
        self._update_buffer_sizes()
        
        # Data storage
        self.data_buffer = deque(maxlen=self.window_samples * 3)  # Keep 60s of data
        self.timestamps_buffer = deque(maxlen=self.window_samples * 3)
        self.analysis_windows = []
        self.stress_predictions = []
        
        # LSL stream
        self.inlet = None
        self.stream_info = None
        
        # Statistics
        self.window_count = 0
        self.prediction_count = 0
        self.last_analysis_time = None
        self.samples_received = 0
        
        # Quality monitoring
        self.signal_quality_history = deque(maxlen=10)
        self.min_quality_threshold = 0.2
    
    def _update_buffer_sizes(self) -> None:
        """Update buffer sizes based on sampling rate."""
        self.window_samples = int(self.window_size * self.sampling_rate)  # 80 samples at 4Hz
        self.window_step_samples = int(self.window_step * self.sampling_rate)  # 40 samples at 4Hz
    
    def find_gsr_stream(self, timeout: float = 10.0) -> bool:
        """Find and connect to GSR LSL stream."""
        print("Looking for GSR stream...")
        
        try:
            # Look for GSR streams first by type
            streams = resolve_byprop('type', 'GSR', timeout=timeout)
            
            if not streams:
                # Try broader search for EDA streams
                streams = resolve_byprop('type', 'EDA', timeout=timeout)

            if not streams:
                print("No GSR/EDA streams found")
                return False

            self.stream_info = streams[0]
            print(f"Found GSR stream: {self.stream_info.name()}")
            print(f"Type: {self.stream_info.type()}")
            print(f"Sampling rate: {self.stream_info.nominal_srate()} Hz")
            print(f"Channels: {self.stream_info.channel_count()}")
            
            # Create inlet
            self.inlet = StreamInlet(self.stream_info, max_buflen=360, max_chunklen=12)
            
            # Validate sampling rate
            stream_rate = self.stream_info.nominal_srate()
            if stream_rate > 0 and abs(stream_rate - self.sampling_rate) > 0.5:
                print(f"Warning: Stream rate ({stream_rate}Hz) differs significantly from training rate ({self.sampling_rate}Hz)")
                print("This may affect model performance")
            
            self._update_buffer_sizes()
            
            return True
            
        except Exception as e:
            print(f"Error connecting to GSR stream: {e}")
            return False
    
    def start(self) -> bool:
        """Start GSR data collection."""
        if not self.inlet and not self.find_gsr_stream():
            print("Cannot start GSR pipeline: no LSL stream available")
            print("Make sure your GSR device is connected and streaming via LSL")
            return False
        
        return super().start()
    
    def _get_run_loop(self):
        """Override to use LSL data collection loop instead of queue-based loop."""
        return self._lsl_data_collection_loop
    
    def validate_input(self, data: Any) -> bool:
        """Validate GSR data input."""
        return isinstance(data, (list, np.ndarray, tuple)) and len(data) > 0
    
    def process_data(self, samples_chunk: Tuple[List, List]) -> PipelineResult:
        """Process GSR samples chunk."""
        timestamp = time.time()
        samples, timestamps = samples_chunk
        
        try:
            # Convert to numpy arrays and handle multi-channel data
            if isinstance(samples, list) and len(samples) > 0:
                if isinstance(samples[0], (list, np.ndarray)):
                    # Multi-channel data - take first channel for GSR
                    sample_values = [s[0] if len(s) > 0 else 0.0 for s in samples]
                else:
                    # Single channel data
                    sample_values = samples
            else:
                sample_values = samples
            
            # Add samples to buffer
            for sample, ts in zip(sample_values, timestamps):
                self.data_buffer.append(float(sample))
                self.timestamps_buffer.append(ts)
            
            self.samples_received += len(sample_values)
            
            # Check if we can create a new analysis window
            windows_created = []
            predictions_made = []
            
            if len(self.data_buffer) >= self.window_samples:
                if (self.last_analysis_time is None or 
                    timestamp - self.last_analysis_time >= self.window_step):
                    
                    window, prediction = self._create_analysis_window()
                    if window and prediction:
                        windows_created.append(window)
                        predictions_made.append(prediction)
                        self.last_analysis_time = timestamp
            
            return PipelineResult(
                timestamp=timestamp,
                data_type="gsr_stress",
                predictions={
                    "analysis_windows": windows_created,
                    "stress_predictions": predictions_made,
                    "buffer_status": {
                        "size": len(self.data_buffer),
                        "capacity": self.window_samples * 3,
                        "duration_s": len(self.data_buffer) / self.sampling_rate
                    }
                },
                raw_data={
                    "samples": sample_values,
                    "timestamps": timestamps,
                    "n_samples": len(sample_values)
                },
                metadata={
                    "sampling_rate": self.sampling_rate,
                    "window_count": self.window_count,
                    "prediction_count": self.prediction_count,
                    "stream_name": self.stream_info.name() if self.stream_info else None
                },
                success=True
            )
            
        except Exception as e:
            return PipelineResult(
                timestamp=timestamp,
                data_type="gsr_stress",
                predictions={},
                raw_data={"samples": samples, "timestamps": timestamps},
                metadata={},
                success=False,
                error_message=str(e)
            )
    
    def _create_analysis_window(self) -> Tuple[Optional[Dict], Optional[Dict]]:
        """Create analysis window and make stress prediction."""
        try:
            # Extract window data (20 seconds at 4Hz = 80 samples)
            window_data = np.array(list(self.data_buffer)[-self.window_samples:])
            window_timestamps = np.array(list(self.timestamps_buffer)[-self.window_samples:])
            
            # Check for valid data
            if len(window_data) < self.window_samples // 2:  # Need at least 10 seconds
                return None, None
            
            # Create analysis window record
            window = {
                'data': window_data,
                'timestamps': window_timestamps,
                'window_id': self.window_count,
                'start_time': window_timestamps[0],
                'end_time': window_timestamps[-1],
                'duration': window_timestamps[-1] - window_timestamps[0],
                'created_at': str(datetime.now(timezone.utc))
            }
            
            # Make stress prediction using the trained model
            prediction_result = self.model.predict(window_data)
            print(prediction_result)
            
            # Create prediction record
            prediction = {
                'window_id': self.window_count,
                'prediction_id': self.prediction_count,
                'created_at': str(datetime.now(timezone.utc)),
                'model_info': self.model.get_model_info(),
                'stress_level': prediction_result.get("stress_level"),
                'confidence': prediction_result.get("confidence", 0.0),
                **self._make_json_serializable(prediction_result),
                'raw_data': self._make_json_serializable(window)
            }
            
            # Store records
            self.analysis_windows.append(window)
            self.stress_predictions.append(prediction)
            
            # Update counters
            self.window_count += 1
            self.prediction_count += 1
            
            # Update signal quality history
            if 'signal_quality' in prediction_result:
                overall_quality = prediction_result['signal_quality'].get('overall', 0)
                self.signal_quality_history.append(overall_quality)
            
            # Keep memory usage reasonable
            if len(self.analysis_windows) > 50:
                self.analysis_windows.pop(0)
                self.stress_predictions.pop(0)
            
            return window, prediction
            
        except Exception as e:
            print(f"Error creating analysis window and prediction: {e}")
            return None, None
    
    def _send_osc_data(self, result: PipelineResult) -> None:
        """Send GSR stress data via OSC."""
        if not result.success:
            return
        
        predictions = result.predictions
        
        # Send stress predictions
        for prediction in predictions.get("stress_predictions", []):
            # Send stress level as binary value
            stress_binary = 1.0 if prediction['stress_level'] == "Stress" else 0.0
            self.osc_client.send_message("/stress/level", stress_binary)
            self.osc_client.send_message("/stress/confidence", prediction['confidence'])
            self.osc_client.send_message("/stress/arousal", prediction['arousal_score'])
            
            # Send feature data
            features = prediction.get('features', {})
            if features:
                self.osc_client.send_message("/gsr/mean", features.get('mean_gsr', 0.0))
                self.osc_client.send_message("/gsr/peaks", features.get('num_peaks', 0))
                self.osc_client.send_message("/gsr/max_amp", features.get('max_amplitude', 0.0))
        
        # Send window data
        for window in predictions.get("analysis_windows", []):
            # Send average GSR value for the window
            avg_gsr = float(np.mean(window['data']))
            self.osc_client.send_message("/gsr/avg", avg_gsr)
    
    def _make_json_serializable(self, obj):
        """Convert numpy arrays and other non-JSON types to JSON serializable types."""
        if isinstance(obj, dict):
            return {k: self._make_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_json_serializable(item) for item in obj]
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        else:
            return obj
    
    def _lsl_data_collection_loop(self) -> None:
        """Main LSL data collection and processing loop."""
        if not self.inlet:
            print("ERROR: No LSL inlet available for GSR data collection")
            return
        
        print("Starting GSR data collection from LSL stream...")
        print(f"Stream: {self.stream_info.name()} ({self.stream_info.channel_count()} channels @ {self.stream_info.nominal_srate()}Hz)")
        print(f"Analysis: {self.window_size}s windows every {self.window_step}s")
        
        consecutive_failures = 0
        max_failures = 50  # 5 seconds at 10 attempts per second
        
        while not self._stop_event.is_set():
            try:
                # Wait if paused
                if self._pause_event.is_set():
                    time.sleep(0.1)
                    continue
                
                # Pull data from LSL stream
                samples, timestamps = self.inlet.pull_chunk(timeout=0.1, max_samples=32)
                
                if samples and timestamps:
                    consecutive_failures = 0
                    
                    # Process the data chunk
                    result = self.process_data((samples, timestamps))
                    
                    # Update statistics
                    self.process_count += 1
                    if not result.success:
                        self.error_count += 1
                    
                    # Send to output queue (non-blocking)
                    try:
                        self.output_queue.put(result, block=False)
                    except Exception:
                        # Queue full, remove old results
                        try:
                            self.output_queue.get_nowait()
                            self.output_queue.put(result, block=False)
                        except Exception:
                            pass
                    
                    # Call result callbacks
                    for callback in self.result_callbacks:
                        try:
                            callback(result)
                        except Exception as e:
                            print(f"Error in GSR callback: {e}")
                    
                    # Send OSC data if successful
                    if result.success and self.osc_client:
                        try:
                            self._send_osc_data(result)
                        except Exception as e:
                            print(f"Error sending GSR OSC data: {e}")
                    
                    stats = self.get_stats()

                    # Log new predictions (less frequently)
                    for prediction in result.predictions.get("stress_predictions", []):
                        stress = prediction['stress_level']
                        confidence = prediction['confidence']
                        quality = prediction.get('signal_quality', {}).get('overall', 0)
                        print(f"GSR Analysis {prediction['window_id']}: {stress} "
                              f"(confidence: {confidence:.2%}, quality: {quality:.3f})")
                
                    stats.update({
                        "stress_predictions": result.predictions.get("stress_predictions", [])
                    })
                else:
                    # No data received
                    consecutive_failures += 1
                    if consecutive_failures > max_failures:
                        print(f"WARNING: No GSR data received for {max_failures * 0.1:.1f} seconds")
                        consecutive_failures = 0  # Reset to avoid spam
                    
                    time.sleep(0.1)  # Wait before trying again
                
            except Exception as e:
                self.error_count += 1
                print(f"Error in GSR data collection: {e}")
                time.sleep(0.1)
        
        print("GSR data collection loop ended")
    
    def get_latest_window(self) -> Optional[Dict]:
        """Get the most recent analysis window."""
        return self.analysis_windows[-1] if self.analysis_windows else None
    
    def get_latest_prediction(self) -> Optional[Dict]:
        """Get the most recent stress prediction."""
        return self.stress_predictions[-1] if self.stress_predictions else None
    
    def get_buffer_data(self) -> Dict[str, Any]:
        """Get current buffer data for visualization."""
        if len(self.data_buffer) == 0:
            return {}
        
        data = np.array(list(self.data_buffer))
        timestamps = np.array(list(self.timestamps_buffer))
        
        return {
            "data": data,
            "timestamps": timestamps,
            "time_axis": timestamps - timestamps[0] if len(timestamps) > 0 else np.array([]),
            "n_samples": len(data),
            "duration": timestamps[-1] - timestamps[0] if len(timestamps) > 1 else 0.0,
            "sampling_rate": self.sampling_rate
        }
    
    def get_recent_predictions(self, n: int = 10) -> List[Dict]:
        """Get the most recent n stress predictions."""
        return self.stress_predictions[-n:] if self.stress_predictions else []
    
    def get_gsr_stats(self) -> Dict[str, Any]:
        """Get GSR-specific statistics."""
        stats = self.get_stats()
        
        # Calculate signal quality metrics
        avg_quality = 0.0
        if self.signal_quality_history:
            avg_quality = np.mean(list(self.signal_quality_history))
        
        # Calculate stress detection rate
        stress_count = 0
        if self.stress_predictions:
            stress_count = sum(1 for p in self.stress_predictions if p['stress_level'] == 'Stress')
        
        stats.update({
            "window_count": self.window_count,
            "prediction_count": self.prediction_count,
            "samples_received": self.samples_received,
            "buffer_utilization": len(self.data_buffer) / (self.window_samples * 3),
            "avg_signal_quality": avg_quality,
            "stress_detection_rate": stress_count / max(1, len(self.stress_predictions)),
            "stream_info": {
                "name": self.stream_info.name() if self.stream_info else None,
                "type": self.stream_info.type() if self.stream_info else None,
                "sampling_rate": self.stream_info.nominal_srate() if self.stream_info else self.sampling_rate,
                "n_channels": self.stream_info.channel_count() if self.stream_info else 1
            },
            "model_info": self.model.get_model_info() if hasattr(self.model, 'get_model_info') else {}
        })
        return stats


class GSRDataProcessor:
    """Utility class for GSR data processing and analysis."""
    
    @staticmethod
    def compute_signal_statistics(data: np.ndarray) -> Dict[str, float]:
        """Compute basic signal statistics."""
        return {
            'mean': float(np.mean(data)),
            'std': float(np.std(data)),
            'min': float(np.min(data)),
            'max': float(np.max(data)),
            'range': float(np.ptp(data)),
            'rms': float(np.sqrt(np.mean(data**2)))
        }
    
    @staticmethod
    def detect_artifacts(data: np.ndarray, threshold_std: float = 3.0) -> Dict[str, Any]:
        """Detect artifacts in GSR data."""
        artifacts = {
            'outliers': [],
            'sudden_jumps': [],
            'flat_segments': [],
            'artifact_percentage': 0.0
        }
        
        # Find outliers
        mean_val = np.mean(data)
        std_val = np.std(data)
        outlier_indices = np.where(np.abs(data - mean_val) > threshold_std * std_val)[0]
        artifacts['outliers'] = outlier_indices.tolist()
        
        # Find sudden jumps (large derivatives)
        if len(data) > 1:
            diff = np.diff(data)
            jump_threshold = threshold_std * np.std(diff)
            jump_indices = np.where(np.abs(diff) > jump_threshold)[0]
            artifacts['sudden_jumps'] = jump_indices.tolist()
        
        # Find flat segments (constant values)
        if len(data) > 5:
            for i in range(len(data) - 5):
                segment = data[i:i+5]
                if np.std(segment) < 1e-6:  # Essentially constant
                    artifacts['flat_segments'].append(i)
        
        # Calculate overall artifact percentage
        total_artifacts = len(set(artifacts['outliers'] + artifacts['sudden_jumps'] + artifacts['flat_segments']))
        artifacts['artifact_percentage'] = total_artifacts / len(data) * 100
        
        return artifacts
    
    @staticmethod
    def apply_smoothing(data: np.ndarray, window_size: int = 5) -> np.ndarray:
        """Apply smoothing filter to GSR data."""
        from scipy import signal
        
        if window_size >= len(data):
            return data
        
        # Use Savitzky-Golay filter for smoothing while preserving peaks
        return signal.savgol_filter(data, window_size, polyorder=2)
    
    @staticmethod
    def estimate_sampling_rate(timestamps: np.ndarray) -> float:
        """Estimate actual sampling rate from timestamps."""
        if len(timestamps) < 2:
            return 0.0
        
        # Calculate intervals and take median to handle jitter
        intervals = np.diff(timestamps)
        median_interval = np.median(intervals)
        
        return 1.0 / median_interval if median_interval > 0 else 0.0