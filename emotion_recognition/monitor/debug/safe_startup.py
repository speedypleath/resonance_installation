#!/usr/bin/env python3
"""
Safe startup script to avoid segmentation faults.
Starts components individually with error isolation.
"""

import sys
import os
import signal
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def signal_handler(signum, frame):
    print(f"\nReceived signal {signum}, exiting safely...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def start_emotion_only():
    """Start only emotion recognition to isolate segfault."""
    print("Starting EMOTION RECOGNITION only...")
    
    try:
        from biometric_monitor.config import MonitorConfig
        from biometric_monitor.models.face import ResNetEmotionModel
        from biometric_monitor.pipelines.face import EmotionPipeline
        from biometric_monitor.osc.osc_client import OSCClient, OSCConfig
        
        print("Imports successful")
        
        # Create emotion model
        emotion_model = ResNetEmotionModel(
            backbone_path="models/FER_static_ResNet50_AffectNet.pt",
            lstm_path="models/FER_dinamic_LSTM_Aff-Wild2.pt",
            sadness_boost=1.5
        )
        
        if not emotion_model.is_loaded:
            print("Error: Emotion model failed to load")
            return False
        
        print("Emotion model loaded successfully")
        
        # Create OSC client
        osc_config = OSCConfig(host="127.0.0.1", port=8000, enabled=True)
        osc_client = OSCClient(osc_config)
        
        # Create pipeline
        pipeline = EmotionPipeline(
            model=emotion_model,
            osc_client=osc_client,
            camera_id=0,
            target_fps=10,
            confidence_threshold=0.3
        )
        
        print("Pipeline created, starting...")
        
        # Start pipeline
        if pipeline.start():
            print("Pipeline started successfully!")
            print("Running emotion recognition... Press Ctrl+C to stop")
            
            try:
                while pipeline.is_running:
                    time.sleep(1)
                    
                    # Print stats every 10 seconds
                    if int(time.time()) % 10 == 0:
                        stats = pipeline.get_stats()
                        print(f"Status: Processed={stats['process_count']}, "
                              f"Errors={stats['error_count']}, "
                              f"Running={stats['is_running']}")
                        
            except KeyboardInterrupt:
                print("\nStopping pipeline...")
                pipeline.stop()
                
            return True
        else:
            print("Failed to start pipeline")
            return False
            
    except Exception as e:
        print(f"Error in emotion-only startup: {e}")
        import traceback
        traceback.print_exc()
        return False

def start_eeg_only():
    """Start only EEG processing to isolate segfault."""
    print("Starting EEG PROCESSING only...")
    
    try:
        from biometric_monitor.pipelines.eeg import EEGPipeline, DummyEEGModel
        from biometric_monitor.osc.osc_client import OSCClient, OSCConfig
        
        print("Imports successful")
        
        # Create OSC client
        osc_config = OSCConfig(host="127.0.0.1", port=8001, enabled=True)
        osc_client = OSCClient(osc_config)
        
        # Explicitly create dummy model
        dummy_model = DummyEEGModel()
        print(f"Created dummy model: {dummy_model.__class__.__name__}")
        
        # Create EEG pipeline with explicit dummy model
        pipeline = EEGPipeline(
            model=dummy_model,  # Explicitly pass dummy model
            osc_client=osc_client,
            fragment_duration=10.0,
            segment_duration=2.0
        )
        
        print("EEG pipeline created, starting...")
        
        # Start pipeline
        if pipeline.start():
            print("EEG pipeline started successfully!")
            print("Processing EEG data... Press Ctrl+C to stop")
            
            try:
                while pipeline.is_running:
                    time.sleep(1)
                    
                    # Print stats every 15 seconds
                    if int(time.time()) % 15 == 0:
                        stats = pipeline.get_eeg_stats()
                        print(f"EEG Status: Fragments={stats['fragment_count']}, "
                              f"Segments={stats['segment_count']}, "
                              f"Samples={stats['samples_received']}")
                        
            except KeyboardInterrupt:
                print("\nStopping EEG pipeline...")
                pipeline.stop()
                
            return True
        else:
            print("Failed to start EEG pipeline")
            return False
            
    except Exception as e:
        print(f"Error in EEG-only startup: {e}")
        import traceback
        traceback.print_exc()
        return False

def start_minimal_web():
    """Start minimal web interface only."""
    print("Starting MINIMAL WEB INTERFACE...")
    
    try:
        from flask import Flask, jsonify, render_template_string
        from flask_socketio import SocketIO
        
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'test_secret'
        socketio = SocketIO(app, cors_allowed_origins="*")
        
        @app.route('/')
        def index():
            return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head><title>Minimal Test</title></head>
            <body>
                <h1>Biometric Monitor - Minimal Test</h1>
                <p>If you see this, web server is working</p>
                <p>Time: {{ time }}</p>
            </body>
            </html>
            ''', time=time.strftime('%H:%M:%S'))
        
        @app.route('/api/test')
        def api_test():
            return jsonify({'status': 'ok', 'time': time.time()})
        
        print("Starting web server on http://127.0.0.1:5001")
        socketio.run(app, host='127.0.0.1', port=5001, debug=False)
        
    except Exception as e:
        print(f"Error in web interface: {e}")
        return False

def main():
    """Main function with startup options."""
    if len(sys.argv) < 2:
        print("Safe Startup Script - Isolate Segmentation Fault")
        print("Usage:")
        print("  python examples/safe_startup.py emotion  - Emotion recognition only")
        print("  python examples/safe_startup.py eeg      - EEG processing only")
        print("  python examples/safe_startup.py web      - Web interface only")
        print("  python examples/safe_startup.py debug    - Run diagnostics first")
        return
    
    mode = sys.argv[1].lower()
    
    if mode == "debug":
        print("Running diagnostics first...")
        os.system("python examples/debug.py")
        return
    elif mode == "emotion":
        success = start_emotion_only()
    elif mode == "eeg":
        success = start_eeg_only()
    elif mode == "web":
        success = start_minimal_web()
    else:
        print(f"Unknown mode: {mode}")
        return
    
    if success:
        print("Component started successfully")
    else:
        print("Component failed to start")

if __name__ == "__main__":
    main()