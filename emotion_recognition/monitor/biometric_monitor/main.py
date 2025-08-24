"""Main entry point for the biometric monitoring system."""

import argparse
import sys
import time
import signal
import os
from pathlib import Path
from typing import Optional

from .config import ConfigManager, MonitorConfig
from .models.base import ModelRegistry
from .models.face import ResNetEmotionModel
from .pipelines.base import PipelineManager
from .pipelines.face import EmotionPipeline
from .pipelines.eeg import DummyEEGModel, EEGPipeline
from .osc.osc_client import OSCRouter, OSCClient
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
        self.osc_router = OSCRouter()
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
        
        # Initialize OSC clients
        self._initialize_osc()
        
        # Initialize pipelines
        if not self._initialize_pipelines():
            return False
        
        # Initialize web application
        self._initialize_web_app()
        
        print("System initialization complete!")
        return True
    
    def _initialize_models(self) -> bool:
        """Initialize and register models."""
        try:
            # Load emotion recognition model
            emotion_model = ResNetEmotionModel(
                backbone_path=self.config.emotion.backbone_model_path,
                lstm_path=self.config.emotion.lstm_model_path,
                sadness_boost=self.config.emotion.sadness_boost
            )
            
            if emotion_model.is_loaded:
                self.model_registry.register_model("emotion_resnet_lstm", emotion_model)
                self.model_registry.set_active_model("emotion", "emotion_resnet_lstm")
                print("Emotion recognition model loaded successfully")
            else:
                print("Warning: Emotion recognition model failed to load")
                return False
            
            return True
            
        except Exception as e:
            print(f"Error initializing models: {e}")
            return False
    
    def _initialize_osc(self) -> None:
        """Initialize OSC communication."""
        if self.config.osc.enabled:
            try:
                # Add default OSC client
                self.osc_router.add_client("default", self.config.osc)
                
                # Set up routing
                self.osc_router.add_route("emotion", "default")
                self.osc_router.add_route("vad", "default")
                self.osc_router.add_route("eeg", "default")
                
                print(f"OSC communication initialized: {self.config.osc.host}:{self.config.osc.port}")
                
            except Exception as e:
                print(f"Warning: OSC initialization failed: {e}")
        else:
            print("OSC communication disabled")
    
    def _initialize_pipelines(self) -> bool:
        """Initialize processing pipelines."""
        try:
            # Get OSC client for pipelines
            osc_client = self.osc_router.clients.get("default")
            
            # Initialize emotion recognition pipeline
            emotion_model = self.model_registry.get_active_model("emotion")
            if emotion_model:
                emotion_pipeline = EmotionPipeline(
                    model=emotion_model,
                    osc_client=osc_client,
                    camera_id=self.config.emotion.camera_id,
                    target_fps=self.config.emotion.target_fps,
                    confidence_threshold=self.config.emotion.confidence_threshold
                )
                self.pipeline_manager.register_pipeline(emotion_pipeline)
                print("Emotion recognition pipeline initialized")
                    # Explicitly create dummy model
            dummy_model = DummyEEGModel()

            # Initialize EEG pipeline
            eeg_pipeline = EEGPipeline(
                model=dummy_model,  # No EEG model for now
                osc_client=osc_client,
                fragment_duration=self.config.eeg.fragment_duration,
                window_step=self.config.eeg.window_step,
                segment_duration=self.config.eeg.segment_duration,
                segment_overlap=self.config.eeg.segment_overlap
            )
            self.pipeline_manager.register_pipeline(eeg_pipeline)
            print("EEG processing pipeline initialized")
            
            return True
            
        except Exception as e:
            print(f"Error initializing pipelines: {e}")
            return False
    
    def _initialize_web_app(self) -> None:
        """Initialize web application."""
        self.web_app = BiometricWebApp(
            config=self.config.web,
            pipeline_manager=self.pipeline_manager,
            osc_router=self.osc_router
        )
        print("Web application initialized")
    
    def start(self, auto_start_pipelines: bool = False) -> bool:
        """Start the monitoring system."""
        if not self.initialize():
            return False
        
        self.is_running = True
        
        if auto_start_pipelines:
            print("Auto-starting pipelines...")
            results = self.pipeline_manager.start_all()
            for pipeline, success in results.items():
                status = "started" if success else "failed to start"
                print(f"  {pipeline}: {status}")
        
        print("Biometric Monitor System ready!")
        return True
    
    def run_web_interface(self) -> None:
        """Run the web interface (blocking)."""
        if not self.web_app:
            print("Web application not initialized")
            return
        
        try:
            self.web_app.run()
        except KeyboardInterrupt:
            print("\nShutting down web interface...")
        finally:
            self.shutdown()
    
    def run_console_mode(self) -> None:
        """Run in console-only mode without web interface."""
        print("Running in console mode. Press Ctrl+C to stop.")
        
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
        print(f"\n--- Status Update ---")
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
        
        # Stop all pipelines
        self.pipeline_manager.stop_all()
        
        # Disconnect OSC clients
        for client in self.osc_router.clients.values():
            client.disconnect()
        
        self.is_running = False
        print("System shutdown complete.")


def create_argument_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Biometric Monitoring System with Emotion Recognition and EEG Analysis"
    )
    
    # Pipeline selection
    parser.add_argument("--emotion", action="store_true", 
                       help="Enable emotion recognition pipeline")
    parser.add_argument("--eeg", action="store_true", 
                       help="Enable EEG monitoring pipeline")
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
        config.emotion.camera_id = args.camera_id
    if args.target_fps:
        config.emotion.target_fps = args.target_fps
    if args.sadness_boost:
        config.emotion.sadness_boost = args.sadness_boost
    if args.confidence_threshold:
        config.emotion.confidence_threshold = args.confidence_threshold
    
    if args.emotion_backbone:
        config.emotion.backbone_model_path = args.emotion_backbone
    if args.emotion_lstm:
        config.emotion.lstm_model_path = args.emotion_lstm
    
    # Validate model files
    if not config_manager.validate_model_files(config):
        print("Error: Required model files are missing!")
        print("Please ensure the following files exist:")
        print(f"  - {config.emotion.backbone_model_path}")
        print(f"  - {config.emotion.lstm_model_path}")
        return 1
    
    # Create and initialize system
    system = BiometricMonitorSystem(config)
    
    if not system.start(auto_start_pipelines=args.auto_start):
        print("Failed to start system")
        return 1
    
    try:
        if args.console_only:
            system.run_console_mode()
        else:
            system.run_web_interface()
    except Exception as e:
        print(f"Error running system: {e}")
        return 1
    finally:
        system.shutdown()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())