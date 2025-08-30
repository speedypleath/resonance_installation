"""Biometric data processing pipelines."""

from .base import BasePipeline, BiometricPipeline, PipelineManager, PipelineResult
from .face import FacePipeline
from .eeg import EEGPipeline
from .gsr import GSRPipeline
from .emotion import EmotionPipeline

__all__ = [
    'BasePipeline',
    'BiometricPipeline', 
    'PipelineManager',
    'PipelineResult',
    'FacePipeline',
    'EEGPipeline', 
    'GSRPipeline',
    'EmotionPipeline'
]