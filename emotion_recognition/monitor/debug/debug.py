#!/usr/bin/env python3
"""
Segmentation fault debugging script.
Tests components individually to isolate the crash.
"""

import sys
import traceback
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test basic imports."""
    print("Testing imports...")
    
    try:
        import cv2
        print("✓ OpenCV imported")
    except Exception as e:
        print(f"✗ OpenCV failed: {e}")
        return False
    
    try:
        import mediapipe as mp
        print("✓ MediaPipe imported")
    except Exception as e:
        print(f"✗ MediaPipe failed: {e}")
        return False
    
    try:
        import torch
        print("✓ PyTorch imported")
    except Exception as e:
        print(f"✗ PyTorch failed: {e}")
        return False
    
    try:
        from pylsl import StreamInlet, resolve_bypred
        print("✓ LSL imported")
    except Exception as e:
        print(f"✗ LSL failed: {e}")
        return False
    
    return True

def test_camera_basic():
    """Test basic camera access."""
    print("\nTesting basic camera access...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"✓ Camera basic test OK: {frame.shape}")
            else:
                print("✗ Camera opened but no frame")
            cap.release()
            return True
        else:
            print("✗ Camera not accessible")
            return False
            
    except Exception as e:
        print(f"✗ Camera test failed: {e}")
        return False

def test_mediapipe():
    """Test MediaPipe face detection."""
    print("\nTesting MediaPipe...")
    
    try:
        import cv2
        import mediapipe as mp
        import numpy as np
        
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=False,
            min_detection_confidence=0.3,
            min_tracking_confidence=0.3
        )
        
        # Test with dummy image
        test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        results = face_mesh.process(test_image)
        
        print("✓ MediaPipe face detection OK")
        return True
        
    except Exception as e:
        print(f"✗ MediaPipe test failed: {e}")
        return False

def test_pytorch_models():
    """Test PyTorch model loading."""
    print("\nTesting PyTorch model loading...")
    
    try:
        backbone_path = "models/FER_static_ResNet50_AffectNet.pt"
        lstm_path = "models/FER_dinamic_LSTM_Aff-Wild2.pt"
        
        if not Path(backbone_path).exists():
            print(f"✗ Model file missing: {backbone_path}")
            return False
        
        if not Path(lstm_path).exists():
            print(f"✗ Model file missing: {lstm_path}")
            return False
        
        import torch
        
        # Test loading models without the custom classes first
        try:
            # Just try to load the raw state dict
            backbone_state = torch.load(backbone_path, map_location='cpu')
            print("✓ Backbone model file loads")
            
            lstm_state = torch.load(lstm_path, map_location='cpu')
            print("✓ LSTM model file loads")
            
            # Clear from memory
            del backbone_state, lstm_state
            
            return True
            
        except Exception as e:
            print(f"✗ Model loading failed: {e}")
            return False
            
    except Exception as e:
        print(f"✗ PyTorch model test failed: {e}")
        return False

def test_lsl():
    """Test LSL stream discovery."""
    print("\nTesting LSL...")
    
    try:
        from pylsl import resolve_bypred
        
        # Correct LSL call - need property and value arguments
        streams = resolve_bypred('type', 'EEG', timeout=2)
        print(f"✓ LSL EEG discovery OK: found {len(streams)} EEG streams")
        
        return True
        
    except Exception as e:
        print(f"✗ LSL test failed: {e}")
        return False

def test_threading():
    """Test basic threading."""
    print("\nTesting threading...")
    
    try:
        import threading
        import time
        
        test_result = []
        
        def worker():
            time.sleep(0.1)
            test_result.append("done")
        
        thread = threading.Thread(target=worker)
        thread.start()
        thread.join(timeout=1)
        
        if test_result:
            print("✓ Threading OK")
            return True
        else:
            print("✗ Threading failed")
            return False
            
    except Exception as e:
        print(f"✗ Threading test failed: {e}")
        return False

def test_emotion_model_creation():
    """Test creating emotion model (most likely segfault source)."""
    print("\nTesting emotion model creation...")
    
    try:
        from biometric_monitor.models.face import ResNetEmotionModel
        
        # Try to create model
        model = ResNetEmotionModel(
            backbone_path="models/FER_static_ResNet50_AffectNet.pt",
            lstm_path="models/FER_dinamic_LSTM_Aff-Wild2.pt",
            sadness_boost=1.0
        )
        
        if model.is_loaded:
            print("✓ Emotion model creation OK")
            return True
        else:
            print("✗ Emotion model creation failed - not loaded")
            return False
            
    except Exception as e:
        print(f"✗ Emotion model creation failed: {e}")
        traceback.print_exc()
        return False

def test_pipeline_creation():
    """Test creating pipelines."""
    print("\nTesting pipeline creation...")
    
    try:
        # Test dummy EEG pipeline first
        from biometric_monitor.pipelines.eeg import EEGPipeline
        
        eeg_pipeline = EEGPipeline()
        print("✓ EEG pipeline creation OK")
        
        # Test emotion pipeline (more likely to segfault)
        from biometric_monitor.models.face import ResNetEmotionModel
        from biometric_monitor.pipelines.face import EmotionPipeline
        
        emotion_model = ResNetEmotionModel(
            backbone_path="models/FER_static_ResNet50_AffectNet.pt",
            lstm_path="models/FER_dinamic_LSTM_Aff-Wild2.pt"
        )
        
        emotion_pipeline = EmotionPipeline(
            model=emotion_model,
            camera_id=0,
            target_fps=10
        )
        
        print("✓ Emotion pipeline creation OK")
        return True
        
    except Exception as e:
        print(f"✗ Pipeline creation failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run diagnostic tests in sequence."""
    print("=" * 60)
    print("SEGMENTATION FAULT DIAGNOSTIC")
    print("=" * 60)
    print("Running tests to isolate the crash...")
    
    tests = [
        ("Basic Imports", test_imports),
        ("Camera Basic", test_camera_basic),
        ("MediaPipe", test_mediapipe),
        ("PyTorch Models", test_pytorch_models),
        ("LSL", test_lsl),
        ("Threading", test_threading),
        ("Emotion Model", test_emotion_model_creation),
        ("Pipeline Creation", test_pipeline_creation),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        
        try:
            result = test_func()
            results.append((test_name, result))
            
            if not result:
                print(f"❌ FAILED at {test_name} - likely segfault source")
                break
                
        except Exception as e:
            print(f"💥 CRASHED at {test_name} - segfault source found!")
            print(f"Error: {e}")
            traceback.print_exc()
            results.append((test_name, False))
            break
    
    print(f"\n{'='*60}")
    print("DIAGNOSTIC RESULTS:")
    print("="*60)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} {test_name}")
    
    print("\nIf the crash occurred during a specific test, that component")
    print("is likely causing the segmentation fault.")


if __name__ == "__main__":
    main()