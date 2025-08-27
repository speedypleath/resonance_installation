"""Main entry point for the biometric monitoring system."""

import argparse
import sys
import time
import signal
import os
import threading
import requests
from typing import Optional

from .config import ConfigManager, MonitorConfig
from .models.base import ModelRegistry
from .models.face import ResNetEmotionModel
from .models.gsr import GSRStressModel
from .pipelines.base import PipelineManager
from .pipelines.face import FacePipeline
from .pipelines.eeg import DummyEEGModel, EEGPipeline
from .pipelines.gsr import GSRPipeline
from .web.app import BiometricWebApp

# https://bugs.python.org/issue30385 fucking god i hate my life
os.environ["no_proxy"] = "*"

class BiometricMonitorSystem:
    """Main system orchestrator for biometric monitoring."""
    
    def __init__(self, config: MonitorConfig):
        self.config = config
        
        # Core components
        self.model_registry = ModelRegistry()
        self.pipeline_manager = PipelineManager()
        self.web_app: Optional[BiometricWebApp] = None
        
        # System state
        self.is_running = False
        self.shutdown_requested = False
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print(f"\nReceived signal {signum}, shutting down gracefully...")
        self.shutdown_requested = True
        self.shutdown()
    
    def initialize(self) -> bool:
        """Initialize all system components."""
        print("Initializing Biometric Monitor System...")
        
        # Initialize models
        if not self._initialize_models():
            return False
        
        # Initialize web application
        self._initialize_web_app()
        
        # Initialize pipelines
        if not self._initialize_pipelines():
            return False
        
        print("System initialization complete!")
        return True
    
    def _initialize_models(self) -> bool:
        """Initialize and register models."""
        try:
            # Load emotion recognition model
            face_model = ResNetEmotionModel(
                backbone_path=self.config.facial.backbone_model_path,
                lstm_path=self.config.facial.lstm_model_path,
                sadness_boost=self.config.facial.sadness_boost
            )

            if face_model.is_loaded:
                self.model_registry.register_model("emotion_resnet_lstm", face_model)
                self.model_registry.set_active_model("facial", "emotion_resnet_lstm")
                print("Facial emotion recognition model loaded successfully")
            else:
                print("Warning: Facial emotion recognition model failed to load")
                return False

            gsr_model = GSRStressModel(
                model_path=self.config.gsr.model_path,
                window_size=self.config.gsr.window_size,
                overlap=self.config.gsr.overlap
            )

            if gsr_model.is_loaded:
                self.model_registry.register_model("gsr_stress", gsr_model)
                self.model_registry.set_active_model("gsr", "gsr_stress")
                print("GSR stress model loaded successfully")
            else:
                print("Warning: GSR stress model failed to load")
                return False

            return True
            
        except Exception as e:
            print(f"Error initializing models: {e}")
            return False
    
    def _initialize_pipelines(self) -> bool:
        """Initialize processing pipelines."""
        try:
            # Initialize facial emotion recognition pipeline
            face_model = self.model_registry.get_active_model("facial")
            if face_model:
                face_pipeline = FacePipeline(
                    model=face_model,
                    camera_id=self.config.facial.camera_id,
                    target_fps=self.config.facial.target_fps,
                    confidence_threshold=self.config.facial.confidence_threshold
                )
                self.pipeline_manager.register_pipeline(face_pipeline)
                print("Emotion recognition pipeline initialized")
                    # Explicitly create dummy model

            # Initialize EEG pipeline
            dummy_model = DummyEEGModel()
            eeg_pipeline = EEGPipeline(
                model=dummy_model,  # No EEG model for now
                fragment_duration=self.config.eeg.fragment_duration,
                window_step=self.config.eeg.window_step,
                segment_duration=self.config.eeg.segment_duration,
                segment_overlap=self.config.eeg.segment_overlap
            )
            self.pipeline_manager.register_pipeline(eeg_pipeline)
            print("EEG processing pipeline initialized")

            # Initialize GSR pipeline
            gsr_model = self.model_registry.get_active_model("gsr")
            if gsr_model:
                gsr_pipeline = GSRPipeline(
                    model=gsr_model,
                    window_size=self.config.gsr.window_size,
                )
                self.pipeline_manager.register_pipeline(gsr_pipeline)
                print("GSR processing pipeline initialized")

            return True
            
        except Exception as e:
            print(f"Error initializing pipelines: {e}")
            return False
    
    def _initialize_web_app(self) -> None:
        """Initialize web application."""
        self.web_app = BiometricWebApp(
            config=self.config.web,
            pipeline_manager=self.pipeline_manager,
        )
        print("Web application initialized")
    
    def start(self, auto_start_pipelines: bool = False) -> bool:
        """Start the monitoring system."""
        if not self.initialize():
            return False
        
        self.is_running = True
        
        # Don't start pipelines here - wait for web server in run_web_interface
        # or start immediately in console mode
        
        print("Biometric Monitor System ready!")
        return True
    
    def _wait_for_web_server(self, timeout: int = 30) -> bool:
        """Wait for web server to be ready."""
        host = self.config.web.host
        port = self.config.web.port
        url = f"http://{host}:{port}/api/status"
        
        print(f"Waiting for web server to be ready at {host}:{port}...")
        
        for attempt in range(timeout):
            try:
                response = requests.get(url, timeout=1)
                if response.status_code == 200:
                    print(f"✅ Web server is ready! (took {attempt + 1}s)")
                    return True
            except (requests.exceptions.RequestException, requests.exceptions.ConnectionError):
                pass
            
            time.sleep(1)
            if attempt % 5 == 4:  # Print every 5 seconds
                print(f"Still waiting for web server... ({attempt + 1}s elapsed)")
        
        print(f"❌ Web server failed to start within {timeout} seconds")
        return False

    def run_web_interface(self, auto_start_pipelines: bool = False) -> None:
        """Run the web interface (blocking)."""
        if not self.web_app:
            print("Web application not initialized")
            return
        
        # Use a simpler approach: start web server with a delay for pipelines
        def delayed_pipeline_start():
            """Start pipelines after a delay to ensure web server is ready."""
            if auto_start_pipelines:
                print("Waiting for web server to initialize...")
                time.sleep(3)  # Give web server time to start
                
                # Try to verify server is ready
                max_retries = 10
                for i in range(max_retries):
                    try:
                        response = requests.get(f"http://{self.config.web.host}:{self.config.web.port}/api/status", timeout=1)
                        if response.status_code == 200:
                            print("✅ Web server is ready - starting pipelines...")
                            break
                    except:
                        if i < max_retries - 1:
                            time.sleep(1)
                            continue
                    
                    if i == max_retries - 1:
                        print("⚠️  Starting pipelines anyway (web server check failed)")
                
                results = self.pipeline_manager.start_all()
                for pipeline, success in results.items():
                    status = "✅ started" if success else "❌ failed to start"
                    print(f"  {pipeline}: {status}")
        
        # Start pipeline initialization in background
        if auto_start_pipelines:
            pipeline_thread = threading.Thread(target=delayed_pipeline_start, daemon=True)
            pipeline_thread.start()
        
        try:
            print(f"Starting web server on http://{self.config.web.host}:{self.config.web.port}")
            # Run web server in main thread to avoid signal issues
            self.web_app.run()
        except KeyboardInterrupt:
            print("\nShutting down web interface...")
        finally:
            self.shutdown()
    
    def run_console_mode(self, auto_start_pipelines: bool = False) -> None:
        """Run in console-only mode without web interface."""
        print("Running in console mode. Press Ctrl+C to stop.")
        
        # Start pipelines immediately in console mode
        if auto_start_pipelines:
            print("Starting pipelines...")
            results = self.pipeline_manager.start_all()
            for pipeline, success in results.items():
                status = "✅ started" if success else "❌ failed to start"
                print(f"  {pipeline}: {status}")
        
        try:
            while not self.shutdown_requested:
                time.sleep(1)
                
                # Print periodic status updates
                if int(time.time()) % 30 == 0:  # Every 30 seconds
                    self._print_status_summary()
                    
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            self.shutdown()
    
    def _print_status_summary(self) -> None:
        """Print status summary to console."""
        stats = self.pipeline_manager.get_summary_stats()
        print("\n--- Status Update ---")
        print(f"Running pipelines: {stats['running_pipelines']}/{stats['total_pipelines']}")
        print(f"Total processes: {stats['total_processes']}")
        print(f"Error rate: {stats['error_rate']:.2%}")
        
        # Print individual pipeline stats
        for name, pipeline_stats in self.pipeline_manager.get_all_stats().items():
            status = "RUNNING" if pipeline_stats['is_running'] else "STOPPED"
            if pipeline_stats.get('is_paused'):
                status = "PAUSED"
            print(f"  {name}: {status} (processed: {pipeline_stats['process_count']})")
    
    def shutdown(self) -> None:
        """Shutdown the monitoring system."""
        if not self.is_running:
            return
        
        print("Shutting down Biometric Monitor System...")
        
        # Stop all pipelines first
        print("Stopping pipelines...")
        self.pipeline_manager.stop_all()
        
        # Give threads time to clean up
        time.sleep(1)
        
        # Web app cleanup is handled automatically by Flask-SocketIO on process exit
        
        # Clean up any remaining camera resources
        print("Cleaning up camera resources...")
        import cv2
        cv2.destroyAllWindows()
        
        self.is_running = False
        print("System shutdown complete.")


def create_argument_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Biometric Monitoring System with Emotion Recognition and EEG Analysis"
    )
    
    # Pipeline selection
    parser.add_argument("--face", action="store_true", 
                       help="Enable face emotion recognition pipeline")
    parser.add_argument("--eeg", action="store_true", 
                       help="Enable EEG monitoring pipeline")
    parser.add_argument("--gsr", action="store_true",
                       help="Enable GSR monitoring pipeline")
    parser.add_argument("--auto-start", action="store_true",
                       help="Automatically start enabled pipelines")
    
    # Web interface
    parser.add_argument("--web", action="store_true", default=True,
                       help="Enable web interface (default: True)")
    parser.add_argument("--web-port", type=int, default=5001,
                       help="Web server port (default: 5001)")
    parser.add_argument("--web-host", default="127.0.0.1",
                       help="Web server host (default: 127.0.0.1)")
    
    # OSC configuration
    parser.add_argument("--osc-host", default="127.0.0.1",
                       help="OSC host (default: 127.0.0.1)")
    parser.add_argument("--osc-port", type=int, default=8000,
                       help="OSC port (default: 8000)")
    parser.add_argument("--no-osc", action="store_true",
                       help="Disable OSC communication")
    
    # Emotion recognition options
    parser.add_argument("--camera-id", type=int, default=0,
                       help="Camera device ID (default: 0)")
    parser.add_argument("--target-fps", type=int, default=15,
                       help="Target processing FPS (default: 15)")
    parser.add_argument("--sadness-boost", type=float, default=2.0,
                       help="Sadness detection boost factor (default: 2.0)")
    parser.add_argument("--confidence-threshold", type=float, default=0.1,
                       help="Emotion confidence threshold (default: 0.1)")
    
    # Model paths
    parser.add_argument("--emotion-backbone", 
                       default="models/FER_static_ResNet50_AffectNet.pt",
                       help="Path to emotion backbone model")
    parser.add_argument("--emotion-lstm", 
                       default="models/FER_dinamic_LSTM_Aff-Wild2.pt",
                       help="Path to emotion LSTM model")
    
    # Configuration file
    parser.add_argument("--config", type=str,
                       help="Path to configuration JSON file")
    
    # Debug options
    parser.add_argument("--debug", action="store_true",
                       help="Enable debug mode")
    parser.add_argument("--console-only", action="store_true",
                       help="Run in console mode without web interface")
    
    return parser


def main():
    """Main entry point."""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    print("=" * 60)
    print("🧠 Biometric Monitor System")
    print("=" * 60)
    
    # Load configuration
    config_manager = ConfigManager(args.config)
    config = config_manager.load_config()
    
    # Override config with command line arguments
    if args.web_host:
        config.web.host = args.web_host
    if args.web_port:
        config.web.port = args.web_port
    if args.debug:
        config.web.debug = True
    
    if args.osc_host:
        config.osc.host = args.osc_host
    if args.osc_port:
        config.osc.port = args.osc_port
    if args.no_osc:
        config.osc.enabled = False
    
    if args.camera_id is not None:
        config.facial.camera_id = args.camera_id
    if args.target_fps:
        config.facial.target_fps = args.target_fps
    if args.sadness_boost:
        config.facial.sadness_boost = args.sadness_boost
    if args.confidence_threshold:
        config.facial.confidence_threshold = args.confidence_threshold

    if args.emotion_backbone:
        config.facial.backbone_model_path = args.emotion_backbone
    if args.emotion_lstm:
        config.facial.lstm_model_path = args.emotion_lstm

    # Validate model files
    if not config_manager.validate_model_files(config):
        print("Error: Required model files are missing!")
        print("Please ensure the following files exist:")
        print(f"  - {config.facial.backbone_model_path}")
        print(f"  - {config.facial.lstm_model_path}")
        print(f"  - {config.gsr.model_path}")
        return 1
    
    # Create and initialize system
    system = BiometricMonitorSystem(config)
    
    if not system.start():
        print("Failed to start system")
        return 1
    
    try:
        if args.console_only:
            system.run_console_mode(auto_start_pipelines=args.auto_start)
        else:
            system.run_web_interface(auto_start_pipelines=args.auto_start)
    except Exception as e:
        print(f"Error running system: {e}")
        return 1
    finally:
        system.shutdown()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())