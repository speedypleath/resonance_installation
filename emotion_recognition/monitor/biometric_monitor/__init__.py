# biometric_monitor/__init__.py
"""Biometric monitoring system for real-time emotion recognition and EEG analysis."""

__version__ = "0.1.0"
__author__ = "Biometric Monitor Team"

from .config import MonitorConfig, ConfigManager
from .models.base import ModelRegistry
from .pipelines.base import PipelineManager
from .osc.osc_client import OSCRouter
from .main import BiometricMonitorSystem

__all__ = [
    "MonitorConfig",
    "ConfigManager", 
    "ModelRegistry",
    "PipelineManager",
    "OSCRouter",
    "BiometricMonitorSystem"
]


# biometric_monitor/models/__init__.py
"""Biometric models package."""

from .models.base import BiometricModel, EmotionModel, EEGModel, ModelRegistry
from .models.face import ResNetEmotionModel

__all__ = [
    "BiometricModel",
    "EmotionModel", 
    "EEGModel",
    "ModelRegistry",
    "ResNetEmotionModel"
]


# biometric_monitor/pipelines/__init__.py
"""Data processing pipelines package."""

from .pipelines.base import BiometricPipeline, PipelineResult, PipelineManager
from .pipelines.face import EmotionPipeline
from .pipelines.eeg import EEGPipeline

__all__ = [
    "BiometricPipeline",
    "PipelineResult", 
    "PipelineManager",
    "EmotionPipeline",
    "EEGPipeline"
]


# biometric_monitor/communication/__init__.py
"""Communication modules package."""

from .osc.osc_client import OSCClient, OSCRouter

__all__ = [
    "OSCClient",
    "OSCRouter"
]


# biometric_monitor/web/__init__.py
"""Web interface package."""

from .web.app import BiometricWebApp

__all__ = [
    "BiometricWebApp"
]


# biometric_monitor/utils/__init__.py
"""Utility functions package."""

from .utils.image_processing import (
    normalize_coordinates,
    get_face_box,
    expand_bbox,
    crop_face_region,
    pad_to_square
)

__all__ = [
    "normalize_coordinates",
    "get_face_box", 
    "expand_bbox",
    "crop_face_region",
    "pad_to_square"
]