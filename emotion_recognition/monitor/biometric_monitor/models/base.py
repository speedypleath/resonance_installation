"""Base classes for biometric models."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple, Union
import numpy as np
import torch
from pathlib import Path


class BiometricModel(ABC):
    """Abstract base class for all biometric models."""
    
    def __init__(self, model_path: Optional[str] = None, device: str = "cpu"):
        self.model_path = model_path
        self.device = device
        self.model = None
        self.is_loaded = False
        
        if model_path and Path(model_path).exists():
            self.load_model()
    
    @abstractmethod
    def load_model(self) -> bool:
        """Load the model from file."""
        pass
    
    @abstractmethod
    def predict(self, data: Union[np.ndarray, torch.Tensor]) -> Dict[str, Any]:
        """Make predictions on input data."""
        pass
    
    @abstractmethod
    def preprocess(self, data: Any) -> Union[np.ndarray, torch.Tensor]:
        """Preprocess input data for model."""
        pass
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        return {
            "model_path": self.model_path,
            "device": self.device,
            "is_loaded": self.is_loaded,
            "model_type": self.__class__.__name__
        }


class FaceModel(BiometricModel):
    """Base class for emotion recognition models."""
    
    def __init__(self, model_path: Optional[str] = None, device: str = "cpu"):
        super().__init__(model_path, device)
        self.emotion_labels = {
            0: 'Neutral', 1: 'Happiness', 2: 'Sadness', 3: 'Surprise',
            4: 'Fear', 5: 'Disgust', 6: 'Anger'
        }

        # since we don't have labels such as bored or calm I lowered the overall arousal
        self.vad_mapping = {
            0: (0.5, 0.2, 0.5),   # Neutral
            1: (0.9, 0.8, 0.8),   # Happiness
            2: (0.15, 0.1, 0.15), # Sadness
            3: (0.65, 0.8, 0.45), # Surprise
            4: (0.1, 0.8, 0.05), # Fear
            5: (0.2, 0.4, 0.25),  # Disgust
            6: (0.15, 0.8, 0.85), # Anger
        }
    
    def compute_vad(self, emotion_probs: np.ndarray) -> Tuple[float, float, float]:
        """Compute weighted VAD values from emotion probabilities."""
        valence, arousal, dominance = 0.0, 0.0, 0.0
        
        for label, prob in enumerate(emotion_probs):
            if label in self.vad_mapping:
                v, a, d = self.vad_mapping[label]
                valence += v * prob
                arousal += a * prob
                dominance += d * prob
        
        return valence, arousal, dominance


class EEGModel(BiometricModel):
    """Base class for EEG analysis models."""
    
    def __init__(self, model_path: Optional[str] = None, device: str = "cpu"):
        super().__init__(model_path, device)
        self.sampling_rate = 256
        self.n_channels = 4
        self.channel_names = ['TP9', 'AF7', 'AF8', 'TP10']
    
    def get_sampling_info(self) -> Dict[str, Any]:
        """Get sampling information."""
        return {
            "sampling_rate": self.sampling_rate,
            "n_channels": self.n_channels,
            "channel_names": self.channel_names
        }

class ModelRegistry:
    """Registry for managing multiple models."""
    
    def __init__(self):
        self.models: Dict[str, BiometricModel] = {}
        self.active_models: Dict[str, str] = {}
    
    def register_model(self, name: str, model: BiometricModel) -> None:
        """Register a model with a given name."""
        self.models[name] = model
        print(f"Registered model: {name}")
    
    def get_model(self, name: str) -> Optional[BiometricModel]:
        """Get a model by name."""
        return self.models.get(name)
    
    def set_active_model(self, model_type: str, model_name: str) -> bool:
        """Set the active model for a given type."""
        if model_name in self.models:
            self.active_models[model_type] = model_name
            return True
        return False
    
    def get_active_model(self, model_type: str) -> Optional[BiometricModel]:
        """Get the active model for a given type."""
        if model_type in self.active_models:
            return self.models.get(self.active_models[model_type])
        return None
    
    def list_models(self) -> Dict[str, Dict[str, Any]]:
        """List all registered models with their info."""
        return {name: model.get_model_info() for name, model in self.models.items()}
    
    def unload_model(self, name: str) -> bool:
        """Unload a model to free memory."""
        if name in self.models:
            model = self.models[name]
            if hasattr(model, 'model') and model.model is not None:
                del model.model
                model.model = None
                model.is_loaded = False
            return True
        return False