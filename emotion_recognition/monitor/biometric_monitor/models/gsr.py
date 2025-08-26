# GSR Model Fixes - Apply to your models/gsr.py file

import numpy as np
import pickle
import joblib
import os
from typing import Dict, Any, Tuple
from scipy.signal import detrend, savgol_filter, butter, sosfilt, filtfilt
from sklearn.preprocessing import RobustScaler
import warnings
from .base import BiometricModel
warnings.filterwarnings('ignore')

class GSRFeatureExtractor:
    """Extract features from GSR signal using exact training methodology."""
    
    def __init__(self, sampling_rate: float = 4.0, target_rate: float = 4.0):
        self.sampling_rate = sampling_rate
        self.target_rate = target_rate
        self.robust_scaler = RobustScaler()
        
    def preprocess_signal(self, signal: np.ndarray) -> np.ndarray:
        """Preprocess signal using exact training method with error handling."""
        if signal is None or len(signal) == 0:
            return np.array([])
        
        try:
            # Ensure signal is numeric and finite
            signal = np.array(signal, dtype=float)
            finite_mask = np.isfinite(signal)
            if not np.any(finite_mask):
                print("Warning: No finite values in signal")
                return np.zeros_like(signal)
            
            # Use only finite values
            if not np.all(finite_mask):
                signal = signal[finite_mask]
            
            if len(signal) < 3:
                print("Warning: Signal too short for preprocessing")
                return signal
            
            # Linear detrending
            detrended = detrend(signal, type='linear')
            
            # Savitzky-Golay filtering for smoothing while preserving peaks
            window_length = min(11, len(detrended) // 4)
            if window_length % 2 == 0:
                window_length += 1
            if window_length >= 3:
                smoothed = savgol_filter(detrended, window_length, polyorder=2)
            else:
                smoothed = detrended
            
            # Low-pass filtering for noise removal
            if len(smoothed) > 8:
                nyquist = self.target_rate / 2
                cutoff = min(1.0, nyquist * 0.8)
                if cutoff > 0:
                    sos = butter(2, cutoff / nyquist, btype='low', output='sos')
                    filtered = sosfilt(sos, smoothed)
                else:
                    filtered = smoothed
            else:
                filtered = smoothed
            
            # Robust normalization
            if len(filtered) > 0:
                filtered_reshaped = filtered.reshape(-1, 1)
                normalized = self.robust_scaler.fit_transform(filtered_reshaped).flatten()
            else:
                normalized = filtered
            
            return normalized
            
        except Exception as e:
            print(f"Error in signal preprocessing: {e}")
            return signal  # Return original signal as fallback
    
    def cvxeda_decomposition(self, signal: np.ndarray, alpha: float = 8e-4, gamma: float = 1e-2):
        """cvxEDA implementation for phasic/tonic separation with fallback."""
        if len(signal) < 5:
            return self._highpass_fallback(signal)
        
        try:
            import cvxpy as cp
        except ImportError:
            return self._highpass_fallback(signal)
        
        n = len(signal)
        
        try:
            # Variables for cvxEDA
            r = cp.Variable(n-1, nonneg=True)  # Phasic driver
            t = cp.Variable(n)                # Tonic component
            e = cp.Variable(n)                # Residual
            
            # Matrices
            D = np.eye(n, n-1) - np.eye(n, n-1, k=-1)  # Integration matrix
            M = np.eye(n-2, n, k=0) - 2*np.eye(n-2, n, k=-1) + np.eye(n-2, n, k=-2)  # Smoothness
            
            # Constraints
            constraints = [
                signal == t + D @ r + e,  # Signal decomposition
                r >= 0                     # Phasic driver non-negative
            ]
            
            # Objective
            objective = cp.Minimize(
                0.5 * cp.sum_squares(e) +     # Fit to data
                alpha * cp.sum(r) +           # Sparsity of phasic
                gamma * 0.5 * cp.sum_squares(M @ t)  # Smoothness of tonic
            )
            
            # Solve
            problem = cp.Problem(objective, constraints)
            problem.solve(solver=cp.ECOS, verbose=False)
            
            if problem.status == cp.OPTIMAL:
                phasic = D.dot(r.value) if r.value is not None else np.zeros(n)
                tonic = t.value if t.value is not None else signal
            else:
                return self._highpass_fallback(signal)
                
        except Exception:
            return self._highpass_fallback(signal)
        
        return phasic, tonic
    
    def _highpass_fallback(self, signal: np.ndarray):
        """Fallback high-pass filter when cvxEDA fails."""
        if len(signal) < 3:
            return signal * 0.1, signal * 0.9  # Simple fallback
        
        try:
            nyquist = self.target_rate / 2
            if nyquist > 0.05:
                cutoff = 0.05 / nyquist
                if cutoff < 1.0:
                    b, a = butter(4, cutoff, btype='high')
                    phasic = filtfilt(b, a, signal)
                    tonic = signal - phasic
                else:
                    phasic = np.diff(signal, prepend=signal[0])
                    tonic = signal - phasic
            else:
                phasic = np.diff(signal, prepend=signal[0])
                tonic = signal - phasic
        except:
            # Ultimate fallback
            phasic = signal * 0.1
            tonic = signal * 0.9
        
        return phasic, tonic
    
    def detect_peaks(self, phasic_signal: np.ndarray, onset_threshold: float = 0.01, 
                    offset_threshold: float = 0.0, amplitude_threshold: float = 0.005, 
                    duration_threshold: float = 1.0):
        """Peak detection with error handling."""
        if len(phasic_signal) == 0:
            return {'peak_indices': [], 'peak_amplitudes': [], 'num_peaks': 0, 'max_amplitude': 0}
        
        try:
            # Apply low-pass filter
            nyquist = self.target_rate / 2
            if nyquist > 1.0 and len(phasic_signal) > 8:
                cutoff = min(1.0, nyquist * 0.8)
                cutoff_norm = cutoff / nyquist
                if cutoff_norm < 1.0:
                    b, a = butter(4, cutoff_norm, btype='low')
                    filtered_phasic = filtfilt(b, a, phasic_signal)
                else:
                    filtered_phasic = phasic_signal
            else:
                filtered_phasic = phasic_signal
            
            # Find onset and offset points
            onsets = []
            offsets = []
            
            above_onset = filtered_phasic > onset_threshold
            onset_crossings = np.diff(above_onset.astype(int))
            onset_indices = np.where(onset_crossings == 1)[0] + 1
            
            for onset_idx in onset_indices:
                if onset_idx >= len(filtered_phasic):
                    continue
                    
                remaining_signal = filtered_phasic[onset_idx:]
                below_offset = remaining_signal <= offset_threshold
                
                if np.any(below_offset):
                    offset_relative = np.where(below_offset)[0][0]
                    offset_idx = onset_idx + offset_relative
                    
                    duration = (offset_idx - onset_idx) / self.target_rate
                    if duration >= duration_threshold:
                        onsets.append(onset_idx)
                        offsets.append(offset_idx)
            
            # Extract peak amplitudes
            peaks_amplitudes = []
            peak_indices = []
            
            for onset, offset in zip(onsets, offsets):
                if onset < len(filtered_phasic) and offset < len(filtered_phasic):
                    window_signal = filtered_phasic[onset:offset+1]
                    if len(window_signal) > 0:
                        max_idx = np.argmax(window_signal)
                        peak_idx = onset + max_idx
                        amplitude = filtered_phasic[peak_idx] - filtered_phasic[onset]
                        
                        if amplitude >= amplitude_threshold:
                            peaks_amplitudes.append(amplitude)
                            peak_indices.append(peak_idx)
            
            return {
                'peak_indices': peak_indices,
                'peak_amplitudes': peaks_amplitudes,
                'num_peaks': len(peaks_amplitudes),
                'max_amplitude': max(peaks_amplitudes) if peaks_amplitudes else 0
            }
            
        except Exception as e:
            print(f"Error in peak detection: {e}")
            return {'peak_indices': [], 'peak_amplitudes': [], 'num_peaks': 0, 'max_amplitude': 0}
    
    def extract_statistical_features(self, signal: np.ndarray) -> np.ndarray:
        """Extract features with comprehensive error handling."""
        if signal is None or len(signal) == 0:
            print("Warning: Empty signal provided to feature extractor")
            return np.zeros(10)
        
        try:
            # Clean and validate signal
            signal = np.array(signal, dtype=float)
            finite_mask = np.isfinite(signal)
            if not np.any(finite_mask):
                print("Warning: No finite values in GSR signal")
                return np.zeros(10)
            
            signal = signal[finite_mask]
            if len(signal) < 3:
                print("Warning: Insufficient signal length after cleaning")
                return np.zeros(10)
            
            # Preprocess
            processed = self.preprocess_signal(signal)
            if len(processed) == 0:
                return np.zeros(10)
            
            # Extract phasic component
            try:
                phasic, tonic = self.cvxeda_decomposition(processed)
            except Exception as e:
                print(f"Warning: Phasic decomposition failed: {e}")
                phasic = processed * 0.1  # Simple fallback
                tonic = processed * 0.9
            
            # Detect peaks
            try:
                peaks_info = self.detect_peaks(phasic)
            except Exception as e:
                print(f"Warning: Peak detection failed: {e}")
                peaks_info = {'num_peaks': 0, 'max_amplitude': 0.0, 'peak_amplitudes': []}
            
            # Calculate features with safe defaults
            mean_gsr = np.mean(processed) if len(processed) > 0 else 0.0
            num_peaks = peaks_info.get('num_peaks', 0)
            max_peak_amplitude = peaks_info.get('max_amplitude', 0.0)
            
            # Safe divisions
            signal_range = max(np.ptp(processed), 1e-8) if len(processed) > 0 else 1.0
            signal_duration = max(len(processed) / self.target_rate, 1e-8)
            
            features = [
                mean_gsr,                                                    # 1
                num_peaks,                                                   # 2
                max_peak_amplitude,                                          # 3
                num_peaks / signal_duration,                                 # 4
                max_peak_amplitude / signal_range,                           # 5
                np.std(processed) if len(processed) > 1 else 0.0,           # 6
                np.mean(phasic) if len(phasic) > 0 else 0.0,                # 7
                np.std(phasic) if len(phasic) > 1 else 0.0,                 # 8
                np.sum(np.array(peaks_info.get('peak_amplitudes', [])) > 0.01), # 9
                np.mean(peaks_info.get('peak_amplitudes', [])) if peaks_info.get('peak_amplitudes') else 0.0 # 10
            ]
            
            # Handle any NaN or inf values
            feature_vector = np.array(features, dtype=float)
            feature_vector = np.nan_to_num(feature_vector, nan=0.0, posinf=0.0, neginf=0.0)
            
            return feature_vector
            
        except Exception as e:
            print(f"Error in feature extraction: {e}")
            import traceback
            traceback.print_exc()
            return np.zeros(10)


class GSRStressModel(BiometricModel):
    """GSR-based stress detection model using trained sklearn models."""
    
    def __init__(self, model_path: str, device: str = "cpu", 
                 sampling_rate: float = 4.0, window_size: float = 20.0, overlap: float = 10.0):
        self.model_path = model_path
        self.sampling_rate = sampling_rate
        self.window_size = window_size
        self.overlap = overlap
        
        # Initialize base class
        super().__init__(model_path, device)
        
        # Stress level mapping (binary classification)
        self.stress_labels = {0: "No Stress", 1: "Stress"}
        self.arousal_mapping = {"No Stress": "Low", "Stress": "High"}
        
        # Feature extractor using training preprocessing
        self.feature_extractor = GSRFeatureExtractor(
            sampling_rate=sampling_rate, 
            target_rate=sampling_rate
        )
        
        # Model components
        self.classifier = None
        self.preprocessing_pipeline = None
        self.model_info = None
        self.load_model()
    
    def load_model(self) -> bool:
        """Load the trained sklearn model and preprocessing pipeline."""
        try:
            # Load main classifier
            if os.path.exists(self.model_path):
                self.classifier = joblib.load(self.model_path)
                print(f"Loaded sklearn classifier from {self.model_path}")
            else:
                print(f"Model file not found: {self.model_path}")
                return self._create_dummy_model()
            
            # Load preprocessing pipeline
            preprocessing_path = self.model_path.replace('.joblib', '_preprocessing.pkl')
            if os.path.exists(preprocessing_path):
                with open(preprocessing_path, 'rb') as f:
                    self.preprocessing_pipeline = pickle.load(f)
                print(f"Loaded preprocessing pipeline from {preprocessing_path}")
            else:
                print(f"Preprocessing file not found: {preprocessing_path}")
                return self._create_dummy_model()
            
            # Load model info
            info_path = self.model_path.replace('.joblib', '_info.pkl')
            if os.path.exists(info_path):
                with open(info_path, 'rb') as f:
                    self.model_info = pickle.load(f)
                print(f"Model info loaded - Accuracy: {self.model_info.get('accuracy', 'unknown'):.3f}")
            
            self.is_loaded = True
            return True
            
        except Exception as e:
            print(f"Error loading GSR stress model: {e}")
            return self._create_dummy_model()
    
    def _create_dummy_model(self) -> bool:
        """Create a dummy model for testing when trained model isn't available."""
        try:
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.preprocessing import StandardScaler
            
            print("Creating dummy GSR stress model for testing...")
            
            self.classifier = RandomForestClassifier(n_estimators=100, random_state=42)
            
            # Create and properly initialize dummy preprocessing pipeline
            feature_scaler = StandardScaler()
            
            # Train dummy model with random data that matches expected features
            dummy_features = np.random.randn(200, 10)  # 10 features as in training
            dummy_labels = np.random.randint(0, 2, 200)
            
            # Fit the scaler with dummy data
            feature_scaler.fit(dummy_features)
            scaled_features = feature_scaler.transform(dummy_features)
            self.classifier.fit(scaled_features, dummy_labels)
            
            # NOW properly initialize the preprocessing pipeline
            self.preprocessing_pipeline = {
                'min_max_scaler': None,
                'feature_scaler': feature_scaler,  # This is now properly fitted
                'cnn_input_scaler': None,
                'feature_extractor': None,
                'cnn_model': None
            }
            
            # Create dummy model info
            self.model_info = {
                'model_type': 'Statistical',
                'classifier': 'Random_Forest_dummy',
                'accuracy': 0.5,  # Random performance
                'segment_length_seconds': 20,
                'sampling_rate_hz': 4
            }
            
            self.is_loaded = True
            print("Dummy model created successfully")
            return True
            
        except Exception as e:
            print(f"Error creating dummy model: {e}")
            self.is_loaded = False
            return False
    
    def preprocess(self, data):
        """Preprocess GSR data for model input."""
        if not self.is_loaded:
            raise RuntimeError("Model not loaded")
        
        if self.preprocessing_pipeline is None:
            raise RuntimeError("Preprocessing pipeline not loaded")
        
        try:
            # Extract features using training method
            features = self.feature_extractor.extract_statistical_features(data)
            
            # Debug: Check feature dimensions
            print(f"Debug: Extracted features shape: {features.shape}")
            print(f"Debug: Features: {features}")
            
            # Ensure we have exactly 10 features
            if features.size != 10:
                print(f"Warning: Expected 10 features, got {features.size}. Using zeros.")
                features = np.zeros(10)
            
            features = features.reshape(1, -1)  # Single sample: (1, 10)
            
            # Apply preprocessing based on model type
            if self.model_info and self.model_info.get('model_type') == 'CNN':
                # CNN model preprocessing
                if (self.preprocessing_pipeline.get('cnn_model') is not None and 
                    self.preprocessing_pipeline.get('feature_extractor') is not None):
                    
                    # Use CNN feature extraction
                    gsr_reshaped = data.reshape(1, -1, 1)
                    gsr_scaled = self.preprocessing_pipeline['cnn_input_scaler'].transform(
                        data.reshape(-1, 1)
                    ).reshape(gsr_reshaped.shape)
                    
                    cnn_features = self.preprocessing_pipeline['feature_extractor'].predict(gsr_scaled)
                    cnn_features_flat = cnn_features.reshape(1, -1)
                    scaled_features = self.preprocessing_pipeline['feature_scaler'].transform(cnn_features_flat)
                else:
                    # Fallback to statistical features
                    if 'feature_scaler' in self.preprocessing_pipeline and self.preprocessing_pipeline['feature_scaler'] is not None:
                        scaled_features = self.preprocessing_pipeline['feature_scaler'].transform(features)
                    else:
                        print("Warning: No feature scaler available, using raw features")
                        scaled_features = features
            else:
                # Statistical model (most common case)
                if 'feature_scaler' in self.preprocessing_pipeline and self.preprocessing_pipeline['feature_scaler'] is not None:
                    print(f"Debug: Scaling features with shape {features.shape}")
                    scaled_features = self.preprocessing_pipeline['feature_scaler'].transform(features)
                else:
                    print("Warning: No feature scaler available, using raw features")
                    scaled_features = features
                    
        except Exception as e:
            print(f"Error in preprocessing: {e}")
            import traceback
            traceback.print_exc()
            raise RuntimeError(f"Error in stress prediction preprocessing: {e}")
        
        return scaled_features, features
    
    def predict(self, gsr_data: np.ndarray) -> Dict[str, Any]:
        """Predict stress level from GSR data with comprehensive error handling."""
        if not self.is_loaded:
            raise RuntimeError("Model not loaded")
        
        # Input validation
        if gsr_data is None or len(gsr_data) == 0:
            print("Warning: Empty GSR data provided")
            return self._create_default_prediction()
        
        if not isinstance(gsr_data, np.ndarray):
            gsr_data = np.array(gsr_data, dtype=float)
        
        # Remove invalid values
        valid_mask = np.isfinite(gsr_data) & (gsr_data >= 0)
        if not np.any(valid_mask):
            print("Warning: No valid GSR samples found")
            return self._create_default_prediction()
        
        # Keep only valid samples
        original_length = len(gsr_data)
        gsr_data = gsr_data[valid_mask]
        if len(gsr_data) < original_length * 0.5:
            print(f"Warning: Removed {original_length - len(gsr_data)} invalid samples")
        
        # Check minimum data requirements
        if len(gsr_data) < 10:
            print(f"Warning: Insufficient data length: {len(gsr_data)} samples")
            return self._create_default_prediction()
        
        try:
            scaled_features, features = self.preprocess(gsr_data)
            
            # Validate preprocessing output
            if scaled_features is None or np.any(~np.isfinite(scaled_features)):
                print("Warning: Feature preprocessing failed")
                return self._create_default_prediction()
            
            # Make prediction with error handling
            try:
                prediction_proba = self.classifier.predict_proba(scaled_features)[0]
                prediction_class = self.classifier.predict(scaled_features)[0]
            except Exception as e:
                print(f"Warning: Model prediction failed: {e}")
                return self._create_default_prediction()
            
            # Validate prediction outputs
            if not np.all(np.isfinite(prediction_proba)) or len(prediction_proba) != 2:
                print("Warning: Invalid prediction probabilities")
                return self._create_default_prediction()
            
            # Map to stress labels
            stress_level = self.stress_labels.get(prediction_class, "No Stress")
            confidence = float(prediction_proba[prediction_class])
            arousal_level = self.arousal_mapping.get(stress_level, "Low")
            arousal_score = float(prediction_proba[1]) if len(prediction_proba) > 1 else 0.0
            
            # Compute signal quality
            # signal_quality = self._assess_signal_quality(gsr_data)
            
            return {
                "stress_level": stress_level,
                "arousal_level": arousal_level,
                "arousal_score": arousal_score,
                "confidence": confidence,
                "probabilities": {
                    "No Stress": float(prediction_proba[0]),
                    "Stress": float(prediction_proba[1])
                },
                "arousal_probabilities": {
                    "Low": float(prediction_proba[0]),
                    "High": float(prediction_proba[1])
                },
                # "signal_quality": signal_quality,
                "features": self._extract_feature_dict(features),
                "raw_output": prediction_proba.tolist()
            }
            
        except Exception as e:
            print(f"Error in GSR stress prediction: {e}")
            import traceback
            traceback.print_exc()
            return self._create_default_prediction()
    
    def _create_default_prediction(self):
        """Create a safe default prediction when errors occur."""
        return {
            "stress_level": "No Stress",
            "arousal_level": "Low",
            "arousal_score": 0.0,
            "confidence": 0.0,
            "probabilities": {"No Stress": 1.0, "Stress": 0.0},
            "arousal_probabilities": {"Low": 1.0, "High": 0.0},
            "signal_quality": {"overall": 0.0, "error": True, "constant_signal": True},
            "features": {"mean_gsr": 0.0, "num_peaks": 0, "max_amplitude": 0.0, "peak_rate": 0.0, "signal_std": 0.0},
            "raw_output": [1.0, 0.0]
        }
    
    def _extract_feature_dict(self, features):
        """Safely extract feature dictionary from feature array."""
        try:
            if features is None or features.size == 0:
                return {"mean_gsr": 0.0, "num_peaks": 0, "max_amplitude": 0.0, "peak_rate": 0.0, "signal_std": 0.0}
            
            feature_array = features.flatten()
            return {
                "mean_gsr": float(feature_array[0]) if len(feature_array) > 0 else 0.0,
                "num_peaks": int(feature_array[1]) if len(feature_array) > 1 else 0,
                "max_amplitude": float(feature_array[2]) if len(feature_array) > 2 else 0.0,
                "peak_rate": float(feature_array[3]) if len(feature_array) > 3 else 0.0,
                "signal_std": float(feature_array[5]) if len(feature_array) > 5 else 0.0
            }
        except Exception as e:
            print(f"Error extracting feature dict: {e}")
            return {"mean_gsr": 0.0, "num_peaks": 0, "max_amplitude": 0.0, "peak_rate": 0.0, "signal_std": 0.0}

    # Keep all other existing methods unchanged (load_model, preprocess, _assess_signal_quality, etc.)