import cv2
import mediapipe as mp
import math
import numpy as np
import time
import threading
from queue import Queue, Empty
import warnings
import gc
import argparse

try:
    from pythonosc import udp_client
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pythonosc"])
    from pythonosc import udp_client

warnings.simplefilter("ignore", UserWarning)

import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms

# Optimize PyTorch for ARM/CPU
torch.set_num_threads(2)  # Limit threads for Pi
torch.backends.cudnn.enabled = False


# Lightweight model architectures
class Bottleneck(nn.Module):
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


class Conv2dSame(torch.nn.Conv2d):
    def calc_same_pad(self, i: int, k: int, s: int, d: int) -> int:
        return max((math.ceil(i / s) - 1) * s + (k - 1) * d + 1 - i, 0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        ih, iw = x.size()[-2:]
        pad_h = self.calc_same_pad(i=ih, k=self.kernel_size[0], s=self.stride[0], d=self.dilation[0])
        pad_w = self.calc_same_pad(i=iw, k=self.kernel_size[1], s=self.stride[1], d=self.dilation[1])

        if pad_h > 0 or pad_w > 0:
            x = F.pad(x, [pad_w // 2, pad_w - pad_w // 2, pad_h // 2, pad_h - pad_h // 2])
        return F.conv2d(x, self.weight, self.bias, self.stride, self.padding, self.dilation, self.groups)


class ResNet(nn.Module):
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
        with torch.no_grad():  # Save memory
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


def ResNet50(num_classes, channels=3):
    return ResNet(Bottleneck, [3,4,6,3], num_classes, channels)


class LSTMPyTorch(nn.Module):
    def __init__(self):
        super(LSTMPyTorch, self).__init__()
        # Keep original dimensions to match pre-trained weights
        self.lstm1 = nn.LSTM(input_size=512, hidden_size=512, batch_first=True, bidirectional=False)
        self.lstm2 = nn.LSTM(input_size=512, hidden_size=256, batch_first=True, bidirectional=False)
        self.fc = nn.Linear(256, 7)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        with torch.no_grad():
            x, _ = self.lstm1(x)
            x, _ = self.lstm2(x)        
            x = self.fc(x[:, -1, :])
            x = self.softmax(x)
            return x


# Optimized preprocessing for Pi - keep model input size but optimize other aspects
def pth_processing_lite(fp, target_size=224):  # Keep original 224 for model compatibility
    """Preprocessing optimized for Raspberry Pi"""
    class PreprocessInput(torch.nn.Module):
        def __init__(self):
            super(PreprocessInput, self).__init__()

        def forward(self, x):
            x = x.to(torch.float32)
            x = torch.flip(x, dims=(0,))
            x[0, :, :] -= 91.4953
            x[1, :, :] -= 103.8827
            x[2, :, :] -= 131.0912
            return x

    def get_img_torch(img):
        # Optimized transform pipeline
        ttransform = transforms.Compose([
            transforms.PILToTensor(),
            PreprocessInput()
        ])
        img = img.resize((target_size, target_size), Image.Resampling.BILINEAR)  # Slightly better quality
        img = ttransform(img)
        img = torch.unsqueeze(img, 0)
        return img
    
    return get_img_torch(fp)


def norm_coordinates(normalized_x, normalized_y, image_width, image_height):
    x_px = min(math.floor(normalized_x * image_width), image_width - 1)
    y_px = min(math.floor(normalized_y * image_height), image_height - 1)
    return x_px, y_px


def get_box(fl, w, h):
    idx_to_coors = {}
    for idx, landmark in enumerate(fl.landmark):
        landmark_px = norm_coordinates(landmark.x, landmark.y, w, h)
        if landmark_px:
            idx_to_coors[idx] = landmark_px

    x_min = np.min(np.asarray(list(idx_to_coors.values()))[:,0])
    y_min = np.min(np.asarray(list(idx_to_coors.values()))[:,1])
    endX = np.max(np.asarray(list(idx_to_coors.values()))[:,0])
    endY = np.max(np.asarray(list(idx_to_coors.values()))[:,1])

    (startX, startY) = (max(0, x_min), max(0, y_min))
    (endX, endY) = (min(w - 1, endX), min(h - 1, endY))
    
    return startX, startY, endX, endY


class OptimizedEmotionRecognizer:
    def __init__(self, backbone_model_path='FER_static_ResNet50_AffectNet.pt', 
                 lstm_model_name='Aff-Wild2', target_fps=5, sadness_boost=1.0, 
                 process_every_n_frames=3, osc_host='127.0.0.1', osc_port=8000):
        self.target_fps = target_fps  # Reduced default FPS
        self.frame_interval = 1.0 / target_fps
        self.sadness_boost = sadness_boost
        self.process_every_n_frames = process_every_n_frames  # Process only every Nth frame
        self.frame_counter = 0
        
        # OSC client for sending VAD data
        self.osc_client = None
        try:
            self.osc_client = udp_client.SimpleUDPClient(osc_host, osc_port)
            print(f"OSC client configured to send to {osc_host}:{osc_port}")
        except Exception as e:
            print(f"Warning: Could not setup OSC client: {e}")
            print("VAD data will not be sent via OSC")
        
        print("Loading models... (this may take a moment on Pi)")
        
        # Load models with CPU optimization
        self.backbone_model = ResNet50(7, channels=3)
        self.backbone_model.load_state_dict(torch.load(backbone_model_path, map_location='cpu'))
        self.backbone_model.eval()
        
        # Try quantization for Pi (optional, may not work with all models)
        try:
            self.backbone_model = torch.quantization.quantize_dynamic(
                self.backbone_model, {nn.Linear}, dtype=torch.qint8
            )
            print("Backbone model quantization successful")
        except Exception as e:
            print(f"Quantization failed, using full precision: {e}")
        
        self.lstm_model = LSTMPyTorch()
        self.lstm_model.load_state_dict(torch.load(f'FER_dinamic_LSTM_{lstm_model_name}.pt', map_location='cpu'))
        self.lstm_model.eval()
        
        # Try to quantize LSTM too
        try:
            self.lstm_model = torch.quantization.quantize_dynamic(
                self.lstm_model, {nn.Linear, nn.LSTM}, dtype=torch.qint8
            )
            print("LSTM model quantization successful")
        except Exception as e:
            print(f"LSTM quantization failed: {e}")
            
        print("Models loaded successfully!")
        
        # Emotion dictionary
        self.DICT_EMO = {0: 'Neutral', 1: 'Happiness', 2: 'Sadness', 3: 'Surprise', 
                        4: 'Fear', 5: 'Disgust', 6: 'Anger'}
        
        # Lightweight MediaPipe face mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=False,
            min_detection_confidence=0.7,  # Higher threshold for better performance
            min_tracking_confidence=0.7
        )
        
        # Reduced LSTM buffer for Pi
        self.lstm_features = []
        self.lstm_buffer_size = 5  # Reduced from 10
        self.last_emotion = "Neutral"
        self.last_confidence = 0.0
        self.last_output = None
        
        # Threading for async processing
        self.frame_queue = Queue(maxsize=1)  # Small queue
        self.result_queue = Queue(maxsize=1)
        self.processing = False
    
    def apply_emotion_bias(self, output):
        """Apply bias to emotion predictions"""
        if self.sadness_boost == 1.0:
            return output
        
        biased_output = output.copy()
        biased_output[0][2] *= self.sadness_boost
        biased_output[0] = biased_output[0] / np.sum(biased_output[0])
        return biased_output
    
    def process_frame_async(self):
        """Background processing thread"""
        while self.processing:
            try:
                frame_data = self.frame_queue.get(timeout=0.1)
                if frame_data is None:
                    continue
                    
                frame, bbox = frame_data
                result = self.process_face_region(frame, bbox)
                
                if not self.result_queue.full():
                    self.result_queue.put(result)
                    
            except Empty:
                continue
            except Exception as e:
                print(f"Processing error: {e}")
                continue
    
    def process_face_region(self, frame, bbox):
        """Process face region for emotion recognition"""
        try:
            startX, startY, endX, endY = bbox
            cur_face = frame[startY:endY, startX:endX]
            
            if cur_face.size == 0:
                return None
                
            # Keep original preprocessing for model compatibility
            cur_face = pth_processing_lite(Image.fromarray(cur_face))
            
            with torch.no_grad():
                features = torch.nn.functional.relu(self.backbone_model.extract_features(cur_face)).detach().numpy()
                
                # Update LSTM buffer
                if len(self.lstm_features) == 0:
                    self.lstm_features = [features] * self.lstm_buffer_size
                else:
                    self.lstm_features = self.lstm_features[1:] + [features]
                
                # LSTM prediction
                lstm_f = torch.from_numpy(np.vstack(self.lstm_features))
                lstm_f = torch.unsqueeze(lstm_f, 0)
                output = self.lstm_model(lstm_f).detach().numpy()
                
                # Apply bias
                output = self.apply_emotion_bias(output)
                
                cl = np.argmax(output)
                confidence = output[0][cl]
                emotion = self.DICT_EMO[cl]
                
                return emotion, confidence, output, bbox
                
        except Exception as e:
            print(f"Face processing error: {e}")
            return None
    
    def send_vad_osc(self, *args):
        """Send VAD data via OSC"""
        if self.osc_client is not None:
            try:
                self.osc_client.send_message("/facial", args)
            except Exception as e:
                print(f"Error sending OSC message: {e}")

    def compute_weighted_vad(self, emotion_probs):
        valence, arousal, dominance = 0.0, 0.0, 0.0
        for label, prob in enumerate(emotion_probs):
            v, a, d = self.DICT_VAD.get(label, (0.0, 0.0, 0.0))
            valence += v * prob
            arousal += a * prob
            dominance += d * prob
        return valence, arousal, dominance

    def run_webcam(self, camera_id=0, show_display=False, webcam_width=320, webcam_height=240):
        """Run optimized webcam emotion recognition"""
        
        # Lower resolution for Pi
        cap = cv2.VideoCapture(camera_id)
        if not cap.isOpened():
            print("Error: Could not open webcam")
            return
            
        # Set lower resolution
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, webcam_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, webcam_height)
        cap.set(cv2.CAP_PROP_FPS, 15)  # Lower FPS for capture
        
        print(f"Camera resolution: {webcam_width}x{webcam_height}")
        print(f"Processing every {self.process_every_n_frames} frames")
        print(f"Output rate: {self.target_fps}Hz")
        if self.sadness_boost != 1.0:
            print(f"Sadness boost: {self.sadness_boost}x")
        print("Press Ctrl+C to quit")
        
        # Start processing thread
        self.processing = True
        processing_thread = threading.Thread(target=self.process_frame_async, daemon=True)
        processing_thread.start()
        
        last_output_time = time.time()
        frame_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    continue
                
                current_time = time.time()
                self.frame_counter += 1
                
                # Only process every Nth frame for face detection
                if self.frame_counter % self.process_every_n_frames == 0:
                    h, w = frame.shape[:2]
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = self.face_mesh.process(frame_rgb)
                    
                    if results.multi_face_landmarks:
                        for fl in results.multi_face_landmarks:
                            bbox = get_box(fl, w, h)
                            
                            # Add to processing queue (non-blocking)
                            if not self.frame_queue.full():
                                self.frame_queue.put((frame_rgb, bbox))
                
                # Get latest result and output at target FPS
                latest_result = None
                while not self.result_queue.empty():
                    latest_result = self.result_queue.get()
                
                if current_time - last_output_time >= self.frame_interval:
                    if latest_result is not None:
                        emotion, confidence, output, bbox = latest_result
                        timestamp = time.strftime("%H:%M:%S", time.localtime(current_time))
                        print(f"[{timestamp}] {emotion} ({confidence:.1%})")
                        # Compute and send VAD
                        vad = self.compute_weighted_vad(output[0])
                        print(f"Weighted Valence: {vad[0]:.3f}, Arousal: {vad[1]:.3f}, Dominance: {vad[2]:.3f}")
                        self.send_vad_osc(vad[0], vad[1], vad[2])
                        # Store for display
                        self.last_emotion = emotion
                        self.last_confidence = confidence
                        self.last_output = output
                    
                    last_output_time = current_time
                    frame_count += 1
                    
                    # Performance monitoring
                    if frame_count % 30 == 0:
                        print(f"--- Processed {frame_count} outputs ---")
                
                # Optional minimal display
                if show_display:
                    if hasattr(self, 'last_emotion'):
                        cv2.putText(frame, f"{self.last_emotion}", (10, 30), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.imshow('Emotion (Press q to quit)', frame)
                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                # Memory cleanup
                if frame_count % 100 == 0:
                    gc.collect()
                        
        except KeyboardInterrupt:
            print("\nStopping...")
        
        finally:
            self.processing = False
            cap.release()
            if show_display:
                cv2.destroyAllWindows()
            print("Emotion recognition stopped.")


def main():
    parser = argparse.ArgumentParser(description="Optimized Facial Emotion Recognition with OSC VAD output")
    parser.add_argument("--sadness-boost", type=float, default=2.0, help="Sadness detection boost factor")
    parser.add_argument("--osc-host", default="192.168.0.141", help="OSC host to send VAD data to")
    parser.add_argument("--osc-port", type=int, default=5001, help="OSC port to send VAD data to")
    parser.add_argument("--target-fps", type=int, default=5, help="Target output FPS")
    parser.add_argument("--show-display", action="store_true", help="Show video display")
    parser.add_argument("--process-every-n-frames", type=int, default=8, help="Process every Nth frame only")
    parser.add_argument("--webcam-width", type=int, default=240, help="Webcam width")
    parser.add_argument("--webcam-height", type=int, default=180, help="Webcam height")
    args = parser.parse_args()

    recognizer = OptimizedEmotionRecognizer(
        backbone_model_path='model/FER_static_ResNet50_AffectNet.pt',
        lstm_model_name='Aff-Wild2',
        target_fps=args.target_fps,
        sadness_boost=args.sadness_boost,
        process_every_n_frames=args.process_every_n_frames,
        osc_host=args.osc_host,
        osc_port=args.osc_port
    )
    recognizer.run_webcam(
        camera_id=0,
        show_display=args.show_display,
        webcam_width=args.webcam_width,
        webcam_height=args.webcam_height
    )


if __name__ == "__main__":
    main()
