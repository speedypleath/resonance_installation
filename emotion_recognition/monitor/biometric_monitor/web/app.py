"""Flask web application for biometric monitoring dashboard."""

import json
import time
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from typing import Dict, Any, Optional

from ..config import WebConfig
from ..pipelines.base import PipelineManager, PipelineResult
from ..osc.osc_client import OSCRouter


class BiometricWebApp:
    """Flask web application for real-time biometric monitoring."""
    
    def __init__(self, config: WebConfig, pipeline_manager: PipelineManager, 
                 osc_router: OSCRouter):
        self.config = config
        self.pipeline_manager = pipeline_manager
        self.osc_router = osc_router
        
        # Initialize Flask app
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = config.secret_key
        self.socketio = SocketIO(self.app, cors_allowed_origins=['http://127.0.0.1:5001'], async_mode='threading')
        
        # Statistics
        self.connected_clients = 0
        self.messages_sent = 0
        self.start_time = time.time()
        
        self._setup_routes()
        self._setup_socketio_events()
        self._setup_pipeline_callbacks()
    
    def _setup_routes(self):
        """Set up Flask HTTP routes."""
        
        @self.app.route('/')
        def index():
            return render_template('dashboard.html')
        
        @self.app.route('/api/status')
        def get_status():
            return jsonify({
                'server_time': time.time(),
                'uptime': time.time() - self.start_time,
                'connected_clients': self.connected_clients,
                'messages_sent': self.messages_sent,
                'pipelines': self.pipeline_manager.get_summary_stats(),
                'osc': self.osc_router.get_router_stats()
            })
        
        @self.app.route('/api/pipelines')
        def get_pipelines():
            return jsonify(self.pipeline_manager.get_all_stats())
        
        @self.app.route('/api/pipelines/<pipeline_name>/start', methods=['POST'])
        def start_pipeline(pipeline_name):
            success = self.pipeline_manager.start_pipeline(pipeline_name)
            return jsonify({'success': success, 'pipeline': pipeline_name})
        
        @self.app.route('/api/pipelines/<pipeline_name>/stop', methods=['POST'])
        def stop_pipeline(pipeline_name):
            self.pipeline_manager.stop_pipeline(pipeline_name)
            return jsonify({'success': True, 'pipeline': pipeline_name})
        
        @self.app.route('/api/pipelines/<pipeline_name>/pause', methods=['POST'])
        def pause_pipeline(pipeline_name):
            pipeline = self.pipeline_manager.get_pipeline(pipeline_name)
            if pipeline:
                pipeline.pause()
                return jsonify({'success': True, 'pipeline': pipeline_name})
            return jsonify({'success': False, 'error': 'Pipeline not found'})
        
        @self.app.route('/api/pipelines/<pipeline_name>/resume', methods=['POST'])
        def resume_pipeline(pipeline_name):
            pipeline = self.pipeline_manager.get_pipeline(pipeline_name)
            if pipeline:
                pipeline.resume()
                return jsonify({'success': True, 'pipeline': pipeline_name})
            return jsonify({'success': False, 'error': 'Pipeline not found'})
        
        @self.app.route('/api/osc/test', methods=['POST'])
        def test_osc():
            data = request.get_json()
            client_name = data.get('client', 'default')
            
            if client_name in self.osc_router.clients:
                success = self.osc_router.clients[client_name].test_connection()
                return jsonify({'success': success, 'client': client_name})
            
            return jsonify({'success': False, 'error': 'Client not found'})
        
        @self.app.route('/video_feed')
        def video_feed():
            """Video streaming route for camera feed."""
            try:
                face_pipeline = self.pipeline_manager.get_pipeline('facial_emotion')
                if face_pipeline and face_pipeline.is_running and hasattr(face_pipeline, 'cap') and face_pipeline.cap:
                    return self._generate_video_stream(face_pipeline)
                else:
                    # Return error response
                    from flask import Response
                    return Response("Camera not available - start emotion recognition pipeline", 
                                  mimetype='text/plain', status=503)
            except Exception as e:
                print(f"Error in video feed route: {e}")
                from flask import Response
                return Response(f"Video feed error: {str(e)}", mimetype='text/plain', status=500)
    
    def _generate_video_stream(self, face_pipeline):
        """Generate video stream with emotion overlays."""
        from flask import Response
        import cv2
        
        def generate():
            frame_count = 0
            last_result = None
            
            try:
                while face_pipeline.is_running and face_pipeline.cap and face_pipeline.cap.isOpened():
                    try:
                        # Get latest frame directly from camera
                        frame = face_pipeline.capture_frame()
                        if frame is None:
                            continue
                        
                        # Try to get the most recent result from the pipeline
                        try:
                            while not face_pipeline.output_queue.empty():
                                last_result = face_pipeline.output_queue.get_nowait()
                        except:
                            pass
                        
                        # Draw emotion overlay using the last successful result
                        if last_result and last_result.raw_data.get("bbox"):
                            bbox = last_result.raw_data["bbox"]
                            startX, startY, endX, endY = bbox
                            
                            emotion = last_result.predictions.get("emotion", "Unknown")
                            confidence = last_result.predictions.get("confidence", 0)
                            
                            # Color based on success and confidence
                            if last_result.success and confidence > 0.5:
                                color = (0, 255, 0)  # Green for good detection
                            elif last_result.success:
                                color = (0, 255, 255)  # Yellow for low confidence
                            else:
                                color = (0, 0, 255)  # Red for failed detection
                            
                            # Draw bounding box
                            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
                            
                            # Draw emotion label with background
                            label = f"{emotion} ({confidence:.1%})"
                            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
                            
                            # Background rectangle for text
                            cv2.rectangle(frame, 
                                        (startX, startY - label_size[1] - 10),
                                        (startX + label_size[0] + 5, startY), 
                                        color, -1)
                            
                            # Text
                            cv2.putText(frame, label, (startX + 2, startY - 5), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                            
                            # Draw VAD values at bottom
                            if last_result.success and "vad" in last_result.predictions:
                                vad = last_result.predictions["vad"]
                                vad_text = f"V:{vad.get('valence', 0):.2f} A:{vad.get('arousal', 0):.2f} D:{vad.get('dominance', 0):.2f}"
                                cv2.putText(frame, vad_text, (10, frame.shape[0] - 50), 
                                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                        
                        # Draw status information
                        status_y = 25
                        cv2.putText(frame, f"Frame: {frame_count}", (10, status_y), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                        
                        if last_result:
                            if last_result.success:
                                status_text = f"Detecting: {last_result.predictions.get('emotion', 'Unknown')}"
                                cv2.putText(frame, status_text, (10, status_y + 25), 
                                          cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                            else:
                                error_msg = last_result.error_message or "Processing error"
                                if len(error_msg) > 30:
                                    error_msg = error_msg[:27] + "..."
                                cv2.putText(frame, f"Issue: {error_msg}", (10, status_y + 25), 
                                          cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                        
                        # Encode frame as JPEG
                        encode_param = [cv2.IMWRITE_JPEG_QUALITY, 80]
                        ret, buffer = cv2.imencode('.jpg', frame, encode_param)
                        
                        if ret:
                            frame_bytes = buffer.tobytes()
                            yield (b'--frame\r\n'
                                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                            frame_count += 1
                        
                    except Exception as e:
                        print(f"Error generating frame {frame_count}: {e}")
                        continue
                        
            except Exception as e:
                print(f"Error in video stream generator: {e}")
                # Send error frame
                import numpy as np
                error_frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(error_frame, "Video Stream Error", (50, 240), 
                          cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                ret, buffer = cv2.imencode('.jpg', error_frame)
                if ret:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        
        return Response(generate(), 
                       mimetype='multipart/x-mixed-replace; boundary=frame',
                       headers={'Cache-Control': 'no-cache, no-store, must-revalidate',
                               'Pragma': 'no-cache',
                               'Expires': '0'})
    
    def _setup_socketio_events(self):
        """Set up SocketIO event handlers."""
        
        @self.socketio.on('connect')
        def handle_connect(auth):
            self.connected_clients += 1
            print(f"WebSocket client connected (ID: {request.sid}). Total clients: {self.connected_clients}")
            emit('connection_status', {
                'status': 'connected',
                'client_id': request.sid,
                'server_time': time.time(),
                'message': 'Connected to Biometric Monitor'
            })
            
            # Send initial status immediately
            try:
                stats = {
                    'pipelines': self.pipeline_manager.get_all_stats(),
                    'osc': self.osc_router.get_router_stats(),
                    'server': {
                        'uptime': time.time() - self.start_time,
                        'connected_clients': self.connected_clients,
                        'messages_sent': self.messages_sent
                    }
                }
                emit('stats_update', stats)
            except Exception as e:
                print(f"Error sending initial stats: {e}")
        
        @self.socketio.on('disconnect')
        def handle_disconnect(auth):
            self.connected_clients = max(0, self.connected_clients - 1)
            print(f"WebSocket client disconnected (ID: {request.sid}). Total clients: {self.connected_clients}")
        
        @self.socketio.on('connect_error')
        def handle_connect_error(data):
            print(f"WebSocket connection error: {data}")
        
        @self.socketio.on_error_default
        def default_error_handler(e):
            print(f"WebSocket error: {e}")
            import traceback
            traceback.print_exc()
        
        @self.socketio.on('request_pipeline_control')
        def handle_pipeline_control(data):
            action = data.get('action')
            pipeline_name = data.get('pipeline')
            
            success = False
            message = ""
            
            # Prevent race conditions by checking current pipeline state
            pipeline = self.pipeline_manager.get_pipeline(pipeline_name)
            if not pipeline:
                emit('pipeline_control_response', {
                    'success': False,
                    'action': action,
                    'pipeline': pipeline_name,
                    'message': f"Pipeline {pipeline_name} not found"
                })
                return
            
            if action == 'start':
                # Check if already running to avoid multiple start attempts
                if pipeline.is_running:
                    success = True
                    message = f"Pipeline {pipeline_name} already running"
                else:
                    success = self.pipeline_manager.start_pipeline(pipeline_name)
                    message = f"Pipeline {pipeline_name} {'started' if success else 'failed to start'}"
            elif action == 'stop':
                if not pipeline.is_running:
                    success = True
                    message = f"Pipeline {pipeline_name} already stopped"
                else:
                    self.pipeline_manager.stop_pipeline(pipeline_name)
                    success = True
                    message = f"Pipeline {pipeline_name} stopped"
            elif action == 'pause':
                if pipeline.is_paused:
                    success = True
                    message = f"Pipeline {pipeline_name} already paused"
                elif pipeline.is_running:
                    pipeline.pause()
                    success = True
                    message = f"Pipeline {pipeline_name} paused"
                else:
                    success = False
                    message = f"Pipeline {pipeline_name} not running, cannot pause"
            elif action == 'resume':
                if not pipeline.is_paused:
                    success = True  
                    message = f"Pipeline {pipeline_name} already running"
                else:
                    pipeline.resume()
                    success = True
                    message = f"Pipeline {pipeline_name} resumed"
            else:
                success = False
                message = f"Unknown action: {action}"
            
            emit('pipeline_control_response', {
                'success': success,
                'action': action,
                'pipeline': pipeline_name,
                'message': message
            })
        
        @self.socketio.on('request_stats')
        def handle_stats_request():
            stats = {
                'pipelines': self.pipeline_manager.get_all_stats(),
                'osc': self.osc_router.get_router_stats(),
                'server': {
                    'uptime': time.time() - self.start_time,
                    'connected_clients': self.connected_clients,
                    'messages_sent': self.messages_sent
                }
            }
            emit('stats_update', stats)
    
    def _setup_pipeline_callbacks(self):
        """Set up callbacks for pipeline results."""
        
        def handle_emotion_result(pipeline_name: str, result: PipelineResult):
            """Handle emotion recognition results."""
            if result.data_type == "facial":
                try:
                    # Always send data, even if not successful
                    data = {
                        'timestamp': result.timestamp,
                        'success': result.success,
                        'error': result.error_message if not result.success else None
                    }
                    
                    if result.success and result.predictions:
                        data.update({
                            'emotion': result.predictions.get('emotion'),
                            'confidence': result.predictions.get('confidence'),
                            'vad': result.predictions.get('vad', {}),
                            'probabilities': result.predictions.get('probabilities', {}),
                        })
                    else:
                        # Send last known values even on failure
                        data.update({
                            'emotion': result.predictions.get('emotion', 'Unknown'),
                            'confidence': result.predictions.get('confidence', 0.0),
                            'vad': result.predictions.get('vad', {'valence': 0, 'arousal': 0, 'dominance': 0}),
                            'probabilities': {},
                        })
                    
                    data['metadata'] = result.metadata
                    
                    # Emit to all connected clients
                    self.socketio.emit('emotion_update', data)
                    self.messages_sent += 1
                    
                    # Debug logging
                    if self.messages_sent % 50 == 1:  # Every ~3 seconds
                        print(f"Sent emotion update #{self.messages_sent}: {data.get('facial')} ({data.get('confidence', 0):.1%})")
                
                except Exception as e:
                    print(f"Error in emotion callback: {e}")
                    import traceback
                    traceback.print_exc()
        
        def handle_eeg_result(pipeline_name: str, result: PipelineResult):
            """Handle EEG processing results."""
            if result.success and result.data_type == "eeg":
                try:
                    data = {
                        'timestamp': result.timestamp,
                        'fragments': [],
                        'segments': [],
                        'buffer_status': result.predictions.get('buffer_status'),
                        'metadata': result.metadata
                    }
                    
                    # Process fragments and segments for JSON serialization
                    for fragment in result.predictions.get('fragments', []):
                        if 'data' in fragment and hasattr(fragment['data'], 'tolist'):
                            fragment_copy = fragment.copy()
                            fragment_copy['data'] = fragment['data'].tolist()
                            fragment_copy['timestamps'] = fragment['timestamps'].tolist() if hasattr(fragment.get('timestamps', []), 'tolist') else fragment.get('timestamps', [])
                            data['fragments'].append(fragment_copy)
                    
                    for segment in result.predictions.get('segments', []):
                        if 'data' in segment and hasattr(segment['data'], 'tolist'):
                            segment_copy = segment.copy()
                            segment_copy['data'] = segment['data'].tolist()
                            if 'time' in segment_copy and hasattr(segment_copy['time'], 'tolist'):
                                segment_copy['time'] = segment_copy['time'].tolist()
                            if 'timestamps' in segment_copy and hasattr(segment_copy['timestamps'], 'tolist'):
                                segment_copy['timestamps'] = segment_copy['timestamps'].tolist()
                            data['segments'].append(segment_copy)
                    
                    self.socketio.emit('eeg_update', data)
                    self.messages_sent += 1
                    
                except Exception as e:
                    print(f"Error in EEG callback: {e}")
        
        # Register callbacks with debug output
        print("Setting up pipeline callbacks...")
        self.pipeline_manager.add_global_callback(handle_emotion_result)
        self.pipeline_manager.add_global_callback(handle_eeg_result)
        print("Pipeline callbacks registered")
    
    def run(self) -> None:
        """Run the Flask web application."""
        print(f"Starting web server on http://{self.config.host}:{self.config.port}")
        print("Open your browser and navigate to the URL above")
        
        self.socketio.run(
            self.app,
            host=self.config.host,
            port=self.config.port,
            debug=self.config.debug
        )
    
    def broadcast_message(self, event: str, data: Dict[str, Any]) -> None:
        """Broadcast message to all connected clients."""
        self.socketio.emit(event, data)
        self.messages_sent += 1
    
    def get_app_stats(self) -> Dict[str, Any]:
        """Get web application statistics."""
        return {
            'uptime': time.time() - self.start_time,
            'connected_clients': self.connected_clients,
            'messages_sent': self.messages_sent,
            'config': {
                'host': self.config.host,
                'port': self.config.port,
                'debug': self.config.debug
            }
        }