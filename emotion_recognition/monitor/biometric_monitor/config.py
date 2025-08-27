"""Configuration management for the biometric monitoring system."""

from typing import Dict, Any, Optional
from dataclasses import dataclass
import os


@dataclass
class FacialConfig:
    """Configuration for emotion recognition."""
    backbone_model_path: str = "models/FER_static_ResNet50_AffectNet.pt"
    lstm_model_path: str = "models/FER_dinamic_LSTM_Aff-Wild2.pt"
    target_fps: int = 15
    sadness_boost: float = 2.0
    camera_id: int = 0
    confidence_threshold: float = 0.0


@dataclass
class EEGConfig:
    """Configuration for EEG monitoring."""
    fragment_duration: float = 10.0
    window_step: float = 5.0
    segment_duration: float = 2.0
    segment_overlap: float = 0.5
    sampling_rate: int = 256
    n_channels: int = 4
    channel_names: list = None
    
    def __post_init__(self):
        if self.channel_names is None:
            self.channel_names = ['TP9', 'AF7', 'AF8', 'TP10']


@dataclass
class GSRConfig:
    """Configuration for GSR monitoring."""
    model_path: str = "models/wesad_gsr_stress_cnn_random_forest_20s_4hz.joblib"
    window_size: int = 20
    overlap: float = 5


@dataclass
class OSCConfig:
    """Configuration for OSC communication."""
    host: str = "127.0.0.1"
    port: int = 8000
    enabled: bool = True


@dataclass
class WebConfig:
    """Configuration for web interface."""
    host: str = "127.0.0.1"
    port: int = 5001
    debug: bool = True
    secret_key: str = "biometric_monitor_secret"


@dataclass
class MonitorConfig:
    """Main configuration class."""
    facial: FacialConfig
    eeg: EEGConfig
    gsr: GSRConfig
    osc: OSCConfig
    web: WebConfig
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'MonitorConfig':
        """Create configuration from dictionary."""
        return cls(
            facial=FacialConfig(**config_dict.get('facial', {})),
            eeg=EEGConfig(**config_dict.get('eeg', {})),
            gsr=GSRConfig(**config_dict.get('gsr', {})),
            osc=OSCConfig(**config_dict.get('osc', {})),
            web=WebConfig(**config_dict.get('web', {}))
        )
    
    @classmethod
    def default(cls) -> 'MonitorConfig':
        """Create default configuration."""
        return cls(
            facial=FacialConfig(),
            eeg=EEGConfig(),
            gsr=GSRConfig(),
            osc=OSCConfig(),
            web=WebConfig()
        )


class ConfigManager:
    """Manages configuration loading and validation."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self._config = None
    
    def load_config(self) -> MonitorConfig:
        """Load configuration from file or create default."""
        if self.config_path and os.path.exists(self.config_path):
            import json
            with open(self.config_path, 'r') as f:
                config_dict = json.load(f)
            self._config = MonitorConfig.from_dict(config_dict)
        else:
            self._config = MonitorConfig.default()
        
        return self._config
    
    def save_config(self, config: MonitorConfig) -> None:
        """Save configuration to file."""
        if self.config_path:
            import json
            config_dict = {
                'facial': config.facial.__dict__,
                'eeg': config.eeg.__dict__,
                'gsr': config.gsr.__dict__,
                'osc': config.osc.__dict__,
                'web': config.web.__dict__
            }
            with open(self.config_path, 'w') as f:
                json.dump(config_dict, f, indent=2)
    
    def validate_model_files(self, config: MonitorConfig) -> bool:
        """Validate that required model files exist."""
        required_files = [
            config.facial.backbone_model_path,
            config.facial.lstm_model_path,
            config.gsr.model_path
        ]
        
        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            print(f"Warning: Missing model files: {missing_files}")
            return False
        
        return True