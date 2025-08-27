"""Emotion recognition models."""

import math
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms
from typing import Dict, Any

from .base import FaceModel


class Conv2dSame(torch.nn.Conv2d):
    """Conv2d with same padding."""
    
    def calc_same_pad(self, i: int, k: int, s: int, d: int) -> int:
        return max((math.ceil(i / s) - 1) * s + (k - 1) * d + 1 - i, 0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        ih, iw = x.size()[-2:]
        pad_h = self.calc_same_pad(i=ih, k=self.kernel_size[0], s=self.stride[0], d=self.dilation[0])
        pad_w = self.calc_same_pad(i=iw, k=self.kernel_size[1], s=self.stride[1], d=self.dilation[1])

        if pad_h > 0 or pad_w > 0:
            x = F.pad(x, [pad_w // 2, pad_w - pad_w // 2, pad_h // 2, pad_h - pad_h // 2])
        return F.conv2d(x, self.weight, self.bias, self.stride, self.padding, self.dilation, self.groups)


class Bottleneck(nn.Module):
    """ResNet Bottleneck block."""
    expansion = 4
    
    def __init__(self, in_channels, out_channels, i_downsample=None, stride=1):
        super(Bottleneck, self).__init__()
        
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, padding=0, bias=False)
        self.batch_norm1 = nn.BatchNorm2d(out_channels, eps=0.001, momentum=0.99)
        
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, padding='same', bias=False)
        self.batch_norm2 = nn.BatchNorm2d(out_channels, eps=0.001, momentum=0.99)
        
        self.conv3 = nn.Conv2d(out_channels, out_channels*self.expansion, kernel_size=1, stride=1, padding=0, bias=False)
        self.batch_norm3 = nn.BatchNorm2d(out_channels*self.expansion, eps=0.001, momentum=0.99)
        
        self.i_downsample = i_downsample
        self.stride = stride
        self.relu = nn.ReLU()
        
    def forward(self, x):
        identity = x.clone()
        x = self.relu(self.batch_norm1(self.conv1(x)))
        x = self.relu(self.batch_norm2(self.conv2(x)))
        x = self.conv3(x)
        x = self.batch_norm3(x)
        
        if self.i_downsample is not None:
            identity = self.i_downsample(identity)
        x += identity
        x = self.relu(x)
        return x


class ResNet(nn.Module):
    """ResNet architecture for emotion recognition."""
    
    def __init__(self, ResBlock, layer_list, num_classes, num_channels=3):
        super(ResNet, self).__init__()
        self.in_channels = 64

        self.conv_layer_s2_same = Conv2dSame(num_channels, 64, 7, stride=2, groups=1, bias=False)
        self.batch_norm1 = nn.BatchNorm2d(64, eps=0.001, momentum=0.99)
        self.relu = nn.ReLU()
        self.max_pool = nn.MaxPool2d(kernel_size=3, stride=2)
        
        self.layer1 = self._make_layer(ResBlock, layer_list[0], planes=64, stride=1)
        self.layer2 = self._make_layer(ResBlock, layer_list[1], planes=128, stride=2)
        self.layer3 = self._make_layer(ResBlock, layer_list[2], planes=256, stride=2)
        self.layer4 = self._make_layer(ResBlock, layer_list[3], planes=512, stride=2)
        
        self.avgpool = nn.AdaptiveAvgPool2d((1,1))
        self.fc1 = nn.Linear(512*ResBlock.expansion, 512)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(512, num_classes)

    def extract_features(self, x):
        """Extract features before final classification layer."""
        x = self.relu(self.batch_norm1(self.conv_layer_s2_same(x)))
        x = self.max_pool(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.avgpool(x)
        x = x.reshape(x.shape[0], -1)
        x = self.fc1(x)
        return x
        
    def forward(self, x):
        x = self.extract_features(x)
        x = self.relu1(x)
        x = self.fc2(x)
        return x
        
    def _make_layer(self, ResBlock, blocks, planes, stride=1):
        ii_downsample = None
        layers = []
        
        if stride != 1 or self.in_channels != planes*ResBlock.expansion:
            ii_downsample = nn.Sequential(
                nn.Conv2d(self.in_channels, planes*ResBlock.expansion, kernel_size=1, stride=stride, bias=False, padding=0),
                nn.BatchNorm2d(planes*ResBlock.expansion, eps=0.001, momentum=0.99)
            )
            
        layers.append(ResBlock(self.in_channels, planes, i_downsample=ii_downsample, stride=stride))
        self.in_channels = planes*ResBlock.expansion
        
        for i in range(blocks-1):
            layers.append(ResBlock(self.in_channels, planes))
            
        return nn.Sequential(*layers)


def ResNet50(num_classes: int, channels: int = 3) -> ResNet:
    """Create ResNet50 model."""
    return ResNet(Bottleneck, [3,4,6,3], num_classes, channels)


class LSTMEmotionModel(nn.Module):
    """LSTM model for temporal emotion recognition."""
    
    def __init__(self, input_size: int = 512, hidden_size1: int = 512, hidden_size2: int = 256, num_classes: int = 7):
        super(LSTMEmotionModel, self).__init__()
        self.lstm1 = nn.LSTM(input_size=input_size, hidden_size=hidden_size1, batch_first=True, bidirectional=False)
        self.lstm2 = nn.LSTM(input_size=hidden_size1, hidden_size=hidden_size2, batch_first=True, bidirectional=False)
        self.fc = nn.Linear(hidden_size2, num_classes)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x, _ = self.lstm1(x)
        x, _ = self.lstm2(x)        
        x = self.fc(x[:, -1, :])
        x = self.softmax(x)
        return x


class ResNetEmotionModel(FaceModel):
    """ResNet-based face recognition model."""
    
    def __init__(self, backbone_path: str, lstm_path: str, device: str = "cpu", sadness_boost: float = 1.0):
        super().__init__(device=device)
        self.backbone_path = backbone_path
        self.lstm_path = lstm_path
        self.sadness_boost = sadness_boost
        
        self.backbone_model = None
        self.lstm_model = None
        self.feature_buffer = []
        self.buffer_size = 10
        
        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.PILToTensor(),
            self._PreprocessInput()
        ])
        
        self.load_model()
    
    class _PreprocessInput(torch.nn.Module):
        """Image preprocessing for ResNet model."""
        
        def __init__(self):
            super().__init__()

        def forward(self, x):
            x = x.to(torch.float32)
            x = torch.flip(x, dims=(0,))
            x[0, :, :] -= 91.4953
            x[1, :, :] -= 103.8827
            x[2, :, :] -= 131.0912
            return x
    
    def load_model(self) -> bool:
        """Load both backbone and LSTM models."""
        try:
            # Load backbone model
            self.backbone_model = ResNet50(7, channels=3)
            self.backbone_model.load_state_dict(torch.load(self.backbone_path, map_location=self.device))
            self.backbone_model.eval()
            
            # Load LSTM model
            self.lstm_model = LSTMEmotionModel()
            self.lstm_model.load_state_dict(torch.load(self.lstm_path, map_location=self.device))
            self.lstm_model.eval()
            
            self.is_loaded = True
            print(f"Successfully loaded emotion models from {self.backbone_path} and {self.lstm_path}")
            return True
            
        except Exception as e:
            print(f"Error loading emotion models: {e}")
            self.is_loaded = False
            return False
    
    def preprocess(self, image: Image.Image) -> torch.Tensor:
        """Preprocess PIL image for model input."""
        image = image.resize((224, 224), Image.Resampling.NEAREST)
        tensor = self.transform(image)
        tensor = torch.unsqueeze(tensor, 0)
        return tensor
    
    def predict(self, image: Image.Image) -> Dict[str, Any]:
        """Predict emotion from PIL image."""
        if not self.is_loaded:
            raise RuntimeError("Models not loaded")
        
        try:
            # Preprocess image
            input_tensor = self.preprocess(image)
            
            # Extract features from backbone
            with torch.no_grad():
                features = torch.nn.functional.relu(
                    self.backbone_model.extract_features(input_tensor)
                ).detach().numpy()
            
            # Update feature buffer for temporal modeling
            if len(self.feature_buffer) == 0:
                self.feature_buffer = [features] * self.buffer_size
            else:
                self.feature_buffer = self.feature_buffer[1:] + [features]
            
            # LSTM prediction
            lstm_input = torch.from_numpy(np.vstack(self.feature_buffer))
            lstm_input = torch.unsqueeze(lstm_input, 0)
            
            with torch.no_grad():
                output = self.lstm_model(lstm_input).detach().numpy()
            
            # Apply sadness boost if configured
            if self.sadness_boost != 1.0:
                output = self._apply_emotion_bias(output)
            
            # Get predictions
            predictions = output[0]
            emotion_idx = np.argmax(predictions)
            emotion_label = self.emotion_labels[emotion_idx]
            confidence = predictions[emotion_idx]
            
            # Compute VAD values
            valence, arousal, dominance = self.compute_vad(predictions)
            
            return {
                "emotion": emotion_label,
                "confidence": float(confidence),
                "probabilities": {label: float(prob) for label, prob in 
                               zip(self.emotion_labels.values(), predictions)},
                "vad": {
                    "valence": float(valence),
                    "arousal": float(arousal),
                    "dominance": float(dominance)
                },
                "raw_output": predictions.tolist()
            }
            
        except Exception as e:
            raise RuntimeError(f"Error in emotion prediction: {e}")
    
    def _apply_emotion_bias(self, output: np.ndarray) -> np.ndarray:
        """Apply bias to emotion predictions."""
        biased_output = output.copy()
        biased_output[0][2] *= self.sadness_boost  # Boost sadness (index 2)
        
        # Renormalize probabilities
        biased_output[0] = biased_output[0] / np.sum(biased_output[0])
        
        return biased_output
    
    def reset_buffer(self) -> None:
        """Reset the feature buffer."""
        self.feature_buffer = []
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information."""
        info = super().get_model_info()
        info.update({
            "backbone_path": self.backbone_path,
            "lstm_path": self.lstm_path,
            "sadness_boost": self.sadness_boost,
            "buffer_size": self.buffer_size,
            "current_buffer_length": len(self.feature_buffer)
        })
        return info