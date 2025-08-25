"""GSR stress detection models using trained sklearn classifiers."""

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
        """Preprocess signal using exact training method."""
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
            sos = butter(2, cutoff / nyquist, btype='low', output='sos')
            filtered = sosfilt(sos, smoothed)
        else:
            filtered = smoothed
        
        # Robust normalization (same as training)
        filtered_reshaped = filtered.reshape(-1, 1)
        normalized = self.robust_scaler.fit_transform(filtered_reshaped).flatten()
        
        return normalized
    
    def cvxeda_decomposition(self, signal: np.ndarray, alpha: float = 8e-4, gamma: float = 1e-2):
        """cvxEDA implementation for phasic/tonic separation."""
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
        nyquist = self.target_rate / 2
        if nyquist > 0.05:
            cutoff = 0.05 / nyquist
            b, a = butter(4, cutoff, btype='high')
            phasic = filtfilt(b, a, signal)
            tonic = signal - phasic
        else:
            phasic = np.diff(signal, prepend=signal[0])
            tonic = signal - phasic
        
        return phasic, tonic
    
    def detect_peaks(self, phasic_signal: np.ndarray, onset_threshold: float = 0.01, 
                    offset_threshold: float = 0.0, amplitude_threshold: float = 0.005, 
                    duration_threshold: float = 1.0):
        """Paper's exact peak detection method."""
        # Apply low-pass filter
        nyquist = self.target_rate / 2
        if nyquist > 1.0:
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
    
    def extract_statistical_features(self, signal: np.ndarray) -> np.ndarray:
        """Extract paper's exact 10 statistical features."""
        # Preprocess
        processed = self.preprocess_signal(signal)
        
        # Extract phasic component using cvxEDA
        phasic, tonic = self.cvxeda_decomposition(processed)
        
        # Detect peaks
        peaks_info = self.detect_peaks(phasic)
        
        # Paper's exact features
        mean_gsr = np.mean(processed)
        num_peaks = peaks_info['num_peaks']
        max_peak_amplitude = peaks_info['max_amplitude']
        
        # Scale features
        signal_range = np.ptp(processed) if np.ptp(processed) > 0 else 1
        signal_duration = len(processed) / self.target_rate
        
        features = [
            mean_gsr,                                                    # 1
            num_peaks,                                                   # 2
            max_peak_amplitude,                                          # 3
            num_peaks / signal_duration,                                 # 4
            max_peak_amplitude / signal_range,                           # 5
            np.std(processed),                                           # 6
            np.mean(phasic) if len(phasic) > 0 else 0,                  # 7
            np.std(phasic) if len(phasic) > 0 else 0,                   # 8
            np.sum(np.array(peaks_info['peak_amplitudes']) > 0.01),     # 9
            np.mean(peaks_info['peak_amplitudes']) if peaks_info['peak_amplitudes'] else 0,  # 10
        ]
        
        # Handle any NaN or inf values
        feature_vector = np.array(features)
        feature_vector = np.nan_to_num(feature_vector, nan=0.0, posinf=0.0, neginf=0.0)
        
        return feature_vector


class GSRStressModel(BiometricModel):
    """GSR-based stress detection model using trained sklearn models."""
    
    def __init__(self, model_path: str, device: str = "cpu", 
                 sampling_rate: float = 4.0, window_size: float = 20.0, overlap: float = 10.0):
        super().__init__(device=device)
        
        self.model_path = model_path
        self.sampling_rate = sampling_rate
        self.window_size = window_size
        
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
        self.overlap = overlap

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
            
            # Create dummy preprocessing pipeline
            feature_scaler = StandardScaler()
            self.preprocessing_pipeline = {
                'min_max_scaler': None,
                'feature_scaler': feature_scaler,
                'cnn_input_scaler': None,
                'feature_extractor': None,
                'cnn_model': None
            }
            
            # Train dummy model with random data
            dummy_features = np.random.randn(200, 10)  # 10 features as in training
            dummy_labels = np.random.randint(0, 2, 200)
            
            feature_scaler.fit(dummy_features)
            scaled_features = feature_scaler.transform(dummy_features)
            self.classifier.fit(scaled_features, dummy_labels)
            
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
        if not self.is_loaded:
            raise RuntimeError("Model not loaded")
        
        try:
            # Extract features using training method
            features = self.feature_extractor.extract_statistical_features(data)
            features = features.reshape(1, -1)  # Single sample
            
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
                    scaled_features = self.preprocessing_pipeline['cnn_feature_scaler'].transform(cnn_features_flat)
                else:
                    # Fallback to statistical features
                    scaled_features = self.preprocessing_pipeline['feature_scaler'].transform(features)
            else:
                # Statistical model (most common case)
                scaled_features = self.preprocessing_pipeline['feature_scaler'].transform(features)
        except Exception as e:
            raise RuntimeError(f"Error in stress prediction: {e}")
        
        return scaled_features, features

    def predict(self, gsr_data: np.ndarray) -> Dict[str, Any]:
        """Predict stress level from GSR data."""
        if not self.is_loaded:
            raise RuntimeError("Model not loaded")
        
        try:
            scaled_features, features = self.preprocess(gsr_data)
            # Make prediction
            prediction_proba = self.classifier.predict_proba(scaled_features)[0]
            prediction_class = self.classifier.predict(scaled_features)[0]
            
            # Map to stress labels
            stress_level = self.stress_labels[prediction_class]
            confidence = prediction_proba[prediction_class]
            
            # Map to arousal for compatibility
            arousal_level = self.arousal_mapping[stress_level]
            arousal_score = prediction_proba[1]  # Probability of stress = high arousal
            
            # Compute signal quality
            signal_quality = self._assess_signal_quality(gsr_data)
            
            return {
                "stress_level": stress_level,
                "arousal_level": arousal_level,  # For compatibility
                "arousal_score": float(arousal_score),
                "confidence": float(confidence),
                "probabilities": {
                    label: float(prob) for label, prob in 
                    zip(self.stress_labels.values(), prediction_proba)
                },
                "arousal_probabilities": {
                    "Low": float(prediction_proba[0]),
                    "High": float(prediction_proba[1])
                },
                "signal_quality": signal_quality,
                "features": {
                    "mean_gsr": float(features[0][0]),
                    "num_peaks": int(features[0][1]),
                    "max_amplitude": float(features[0][2]),
                    "peak_rate": float(features[0][3]),
                    "signal_std": float(features[0][5])
                },
                "raw_output": prediction_proba.tolist()
            }
            
        except Exception as e:
            raise RuntimeError(f"Error in stress prediction: {e}")
    
    def _assess_signal_quality(self, gsr_data: np.ndarray) -> Dict[str, float]:
        """Assess the quality of the GSR signal."""
        quality_metrics = {}
        
        # Check for constant signal (sensor disconnected)
        if np.std(gsr_data) < 1e-6 or np.all(gsr_data == 0):
            quality_metrics["overall"] = 0.0
            quality_metrics["constant_signal"] = True
            quality_metrics["snr"] = 0.0
            quality_metrics["stability"] = 0.0
            quality_metrics["artifact_ratio"] = 1.0
            return quality_metrics
        
        # Signal-to-noise ratio estimate
        signal_power = np.var(gsr_data)
        noise_estimate = np.var(np.diff(gsr_data))
        snr = signal_power / (noise_estimate + 1e-8)
        quality_metrics["snr"] = float(snr)
        
        # Signal stability
        processed = self.feature_extractor.preprocess_signal(gsr_data.copy())
        stability = 1.0 / (1.0 + np.std(processed))
        quality_metrics["stability"] = float(stability)
        
        # Artifact detection
        diff = np.diff(gsr_data)
        artifact_threshold = 3 * np.std(diff)
        artifact_count = np.sum(np.abs(diff) > artifact_threshold)
        artifact_ratio = artifact_count / len(diff)
        quality_metrics["artifact_ratio"] = float(artifact_ratio)
        
        # Overall quality score
        overall_quality = (snr / (snr + 1.0)) * stability * (1.0 - artifact_ratio)
        quality_metrics["overall"] = float(overall_quality)
        quality_metrics["constant_signal"] = False
        
        return quality_metrics
    
    def reset_buffer(self) -> None:
        """Reset any internal buffers (not needed for sklearn models)."""
        pass
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information."""
        info = super().get_model_info()
        info.update({
            "model_path": self.model_path,
            "sampling_rate": self.sampling_rate,
            "window_size": self.window_size,
            "model_type": "sklearn_classifier",
            "feature_extractor": type(self.feature_extractor).__name__
        })
        
        if self.model_info:
            info.update({
                "training_accuracy": self.model_info.get("accuracy", "unknown"),
                "classifier_type": self.model_info.get("classifier", "unknown"),
                "paper_target_met": self.model_info.get("exceeded_target", False),
                "training_method": "WESAD dataset with cvxEDA features"
            })
        
        return info
    
    def compute_vad(self, predictions: np.ndarray) -> Tuple[float, float, float]:
        """Compute VAD values from stress predictions."""
        stress_prob = predictions[1] if len(predictions) > 1 else 0.5
        
        # Arousal: higher with stress
        arousal = 0.3 + 0.7 * stress_prob
        
        # Valence: neutral to slightly negative with stress
        valence = 0.6 - 0.3 * stress_prob
        
        # Dominance: higher with stress (activation/urgency)
        dominance = 0.4 + 0.5 * stress_prob
        
        return valence, arousal, dominance