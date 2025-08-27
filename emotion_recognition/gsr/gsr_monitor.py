import sys
import time
import argparse
from grove.adc import ADC
from rich.live import Live
from rich.table import Table
from rich.console import Console
from rich import box
from collections import deque
import numpy as np
import joblib
import pickle
from scipy.signal import butter, filtfilt
import scipy.signal as sp_signal
from scipy.signal import savgol_filter
from sklearn.preprocessing import RobustScaler
from pythonosc.udp_client import SimpleUDPClient

SAMPLE_RATE = 4  # Hz
WINDOW_DURATION_8S = 8  # seconds
WINDOW_DURATION_20S = 20  # seconds
OVERLAP_8S = 5  # seconds
OVERLAP_20S = 10  # seconds
DISPLAY_RATE = 4  # Hz

OSC_IP = "127.0.0.1"
OSC_PORT = 9000
OSC_ADDRESS_8S = "/gsr/prediction/8s"
OSC_ADDRESS_20S = "/gsr/prediction/20s"

osc_client = SimpleUDPClient(OSC_IP, OSC_PORT)

class GroveGSRSensor:
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def GSR(self):
        return self.adc.read(self.channel)

class GSRStressPredictor:
    def __init__(self, model_name="wesad_gsr_stress_cnn_random_forest"):
        # Load trained model
        self.model = joblib.load(f"{model_name}.joblib")
        
        # Load preprocessing
        with open(f"{model_name}_preprocessing.pkl", "rb") as f:
            self.preprocessing = pickle.load(f)
        
        # Load model info
        with open(f"{model_name}_info.pkl", "rb") as f:
            self.info = pickle.load(f)
        
        self.sampling_rate = 4  # 4Hz for WESAD
        
        print(f"Loaded {self.info['classifier']} model")
        print(f"Accuracy: {self.info['accuracy']:.1%}")
    
    def predict_stress(self, gsr_signal):
        """
        Predict stress from GSR signal using EXACT training methodology
        
        Args:
            gsr_signal: numpy array of GSR values (80 samples = 20 seconds at 4Hz)
            
        Returns:
            prediction: 0 (no stress) or 1 (stress)
            confidence: prediction confidence [0-1]
        """
        features_scaled = self._extract_cnn_features(gsr_signal).reshape(1, -1)
        
        # Make prediction
        prediction = self.model.predict(features_scaled)[0]
        
        # Get confidence if available
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba(features_scaled)[0]
            confidence = max(probabilities)
        else:
            confidence = 1.0  # kNN doesn't have probabilities
        
        return prediction, confidence
    
    def _extract_statistical_features(self, signal):
        """Extract EXACT statistical features used in training"""
        
        # Step 1: Preprocess exactly as training
        min_max_scaler = self.preprocessing['min_max_scaler']
        processed = min_max_scaler.transform(signal.reshape(-1, 1)).flatten()
        
        # Step 2: Extract phasic component (simplified but working version)
        phasic, tonic = self._extract_phasic_simple(processed)
        
        # Step 3: Detect peaks (simplified but working version)
        peaks_info = self._detect_peaks_simple(phasic)
        
        # Step 4: Extract EXACT same 10 features as training
        mean_gsr = np.mean(processed)
        num_peaks = peaks_info['num_peaks']
        max_peak_amplitude = peaks_info['max_amplitude']
        
        # Scale features to be more kNN-friendly (same as training)
        signal_range = np.ptp(processed) if np.ptp(processed) > 0 else 1
        signal_duration = len(processed) / self.sampling_rate
        
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
        
        return np.array(features)
    
    def _extract_cnn_features(self, signal):
        """Extract CNN features using trained feature extractor"""
        
        if self.preprocessing['feature_extractor'] is None:
            raise ValueError("CNN feature extractor not found")
        
        # Step 1: Scale input signal for CNN (using CNN input scaler)
        cnn_input_scaler = self.preprocessing['cnn_input_scaler']
        signal_scaled_flat = cnn_input_scaler.transform(signal.reshape(-1, 1))
        signal_scaled = signal_scaled_flat.reshape(1, len(signal), 1)  # Reshape for CNN
        
        # Step 2: Extract features from trained CNN
        feature_extractor = self.preprocessing['feature_extractor']
        cnn_features = feature_extractor.predict(signal_scaled, verbose=0)
        cnn_features_flat = cnn_features.reshape(1, -1)
        
        # Step 3: Scale CNN features for classifier (using feature scaler)
        feature_scaler = self.preprocessing['feature_scaler'] 
        cnn_features_scaled = feature_scaler.transform(cnn_features_flat)
        
        return cnn_features_scaled.flatten()
    
    def _extract_phasic_simple(self, signal):
        """Simplified phasic extraction (fallback)"""
        try:
            # Try simple high-pass filter
            nyquist = self.sampling_rate / 2
            if nyquist > 0.05:
                cutoff = 0.05 / nyquist
                b, a = butter(4, cutoff, btype='high')
                phasic = filtfilt(b, a, signal)
                tonic = signal - phasic
            else:
                phasic = np.diff(signal, prepend=signal[0])
                tonic = signal - phasic
        except:
            # Ultimate fallback
            phasic = signal - np.mean(signal)
            tonic = np.full_like(signal, np.mean(signal))
        
        return phasic, tonic
    
    def _detect_peaks_simple(self, phasic_signal):
        """Simplified peak detection"""
        
        onset_threshold = 0.01
        amplitude_threshold = 0.005
        
        # Find peaks as local maxima above threshold
        peaks_amplitudes = []
        peak_indices = []
        
        threshold = np.mean(phasic_signal) + 0.5 * np.std(phasic_signal)
        
        for i in range(1, len(phasic_signal) - 1):
            if (phasic_signal[i] > phasic_signal[i-1] and 
                phasic_signal[i] > phasic_signal[i+1] and 
                phasic_signal[i] > threshold and
                phasic_signal[i] > amplitude_threshold):
                
                peaks_amplitudes.append(phasic_signal[i])
                peak_indices.append(i)
        
        return {{
            'peak_indices': peak_indices,
            'peak_amplitudes': peaks_amplitudes,
            'num_peaks': len(peaks_amplitudes),
            'max_amplitude': max(peaks_amplitudes) if peaks_amplitudes else 0
        }}

console = Console()
model_name_8s = 'model/wesad_gsr_stress_cnn_random_forest_8s_4hz'
model_name_20s = 'model/wesad_gsr_stress_cnn_random_forest_20s_4hz'

# Initialize components
predictor_8s = GSRStressPredictor(model_name_8s)
predictor_20s = GSRStressPredictor(model_name_20s)
scaler = RobustScaler()

def adc_to_conductance_microSiemens(R):
    if R >= 512:
        return 0
    return ((512 - R) * 100) / (1024 + 2 * R)

def preprocess(data):
    detrended = sp_signal.detrend(data, type='linear')
    
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
        nyquist = SAMPLE_RATE / 2
        cutoff = min(1.0, nyquist * 0.8)
        sos = sp_signal.butter(2, cutoff / nyquist, btype='low', output='sos')
        filtered = sp_signal.sosfilt(sos, smoothed)
    else:
        filtered = smoothed
    
    # Robust normalization
    filtered_reshaped = filtered.reshape(-1, 1)
    normalized = scaler.fit_transform(filtered_reshaped).flatten()
    
    return normalized

def send_osc_prediction(address, label, probability):
    osc_client.send_message(address, [int(label), float(probability)])

def predict_8s(data_8s):
    """Predict stress using the 8s model only if the buffer is exactly 32 values."""
    if data_8s and len(data_8s) == 32:
        segment_8s = preprocess(list(data_8s))
        if segment_8s.shape[0] != 32:
            raise ValueError(f"8s model: Expected 32 values after preprocessing, got {segment_8s.shape[0]}")
        prediction_8s, confidence_8s = predictor_8s.predict_stress(segment_8s)
        print(f"\n=== 8s Model Prediction ===")
        print(f"8s Model: {'Stress' if prediction_8s == 1 else 'No Stress'} (Confidence: {confidence_8s:.1%})")
        print("=" * 40)
        send_osc_prediction(OSC_ADDRESS_8S, prediction_8s, confidence_8s)
    elif data_8s:
        print(f"[WARN] 8s model called with {len(data_8s)} values (expected 32). Skipping.")

def predict_20s(data_20s):
    """Predict stress using the 20s model only if the buffer is exactly 80 values."""
    if data_20s and len(data_20s) == 80:
        segment_20s = preprocess(list(data_20s))
        if segment_20s.shape[0] != 80:
            raise ValueError(f"20s model: Expected 80 values after preprocessing, got {segment_20s.shape[0]}")
        prediction_20s, confidence_20s = predictor_20s.predict_stress(segment_20s)
        print(f"\n=== 20s Model Prediction ===")
        print(f"20s Model: {'Stress' if prediction_20s == 1 else 'No Stress'} (Confidence: {confidence_20s:.1%})")
        print("=" * 40)
        send_osc_prediction(OSC_ADDRESS_20S, prediction_20s, confidence_20s)
    elif data_20s:
        print(f"[WARN] 20s model called with {len(data_20s)} values (expected 80). Skipping.")

def make_table(readings):
    table = Table(title="GSR Sensor Readings", box=box.SIMPLE_HEAD)
    table.add_column("Time", justify="right")
    table.add_column("ADC Value", justify="right")
    table.add_column("Conductance (µS)", justify="right")
    for t, adc, cond in readings[-20:]:
        table.add_row(t, str(adc), f"{cond:.2f}")
    return table

def calibrate_sensor(sensor):
    console.print("[bold cyan]🧪 Calibration Step[/bold cyan]")
    console.print(
        "- Turn the trimpot on the GSR module slowly\n"
        "- Watch the ADC value live\n"
        "- Adjust until it's close to [bold yellow]512[/bold yellow]\n"
        "- Press Ctrl+C to exit calibration and continue"
    )
    try:
        with Live(refresh_per_second=8) as live:
            while True:
                raw = sensor.GSR
                live.update(f"ADC Reading: [bold magenta]{raw}[/bold magenta]   (aim for ~512)")
                time.sleep(0.3)
    except KeyboardInterrupt:
        pass
        
        
def main(channel=0, sample_rate=SAMPLE_RATE, window_duration_8s=WINDOW_DURATION_8S, overlap_8s=OVERLAP_8S, window_duration_20s=WINDOW_DURATION_20S, overlap_20s=OVERLAP_20S, calibrate=True, use_dual_models=True):
    sensor = GroveGSRSensor(channel)
    
    if calibrate:
        calibrate_sensor(sensor)
    else:
        console.print("[bold yellow]⚠️  Skipping calibration - ensure sensor is properly calibrated[/bold yellow]")

    interval = 1 / sample_rate
    window_samples_8s = int(window_duration_8s * sample_rate)
    step_samples_8s = int((window_duration_8s - overlap_8s) * sample_rate)
    window_samples_20s = int(window_duration_20s * sample_rate)
    step_samples_20s = int((window_duration_20s - overlap_20s) * sample_rate)

    buffer_8s = deque(maxlen=window_samples_8s)  # hold last 8 seconds
    buffer_20s = deque(maxlen=window_samples_20s)  # hold last 20 seconds
    samples_since_last_save_8s = 0
    samples_since_last_save_20s = 0
    readings = []

    print(f"Starting continuous logging on channel {channel} at {sample_rate}Hz")
    print(f"8s Window duration: {window_duration_8s}s, overlap: {overlap_8s}s, step: {step_samples_8s} samples")
    print(f"20s Window duration: {window_duration_20s}s, overlap: {overlap_20s}s, step: {step_samples_20s} samples")
    if use_dual_models:
        print("Mode: Dual model prediction (8s + 20s)")
    else:
        print("Mode: Single model prediction (8s only)")
    console.print("[bold green]📈 Starting GSR Monitor[/bold green] (Press Ctrl+C to stop)")
    try:
        with Live(make_table(readings), refresh_per_second=4) as live:
            while True:
                raw_value = sensor.GSR
                conductance = adc_to_conductance_microSiemens(raw_value)
                timestamp = time.strftime("%H:%M:%S")
                readings.append((timestamp, raw_value, conductance))
                live.update(make_table(readings))
                buffer_8s.append(conductance)
                buffer_20s.append(conductance)
                samples_since_last_save_8s += 1
                samples_since_last_save_20s += 1
                
                # 8s model: run only when buffer is exactly full and step count is reached
                if len(buffer_8s) == window_samples_8s and samples_since_last_save_8s >= step_samples_8s:
                    predict_8s(buffer_8s)
                    samples_since_last_save_8s = 0
                
                # 20s model: run only when buffer is exactly full and step count is reached
                if use_dual_models and len(buffer_20s) == window_samples_20s and samples_since_last_save_20s >= step_samples_20s:
                    predict_20s(buffer_20s)
                    samples_since_last_save_20s = 0
                
                time.sleep(interval)
    except KeyboardInterrupt:
        console.print("\n[red]Stopped by user[/red]")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GSR Stress Monitor with Real-time Prediction')
    parser.add_argument('adc_channel', type=int, help='ADC channel number (0-7)')
    parser.add_argument('--calibrate', action='store_true', 
                       help='Skip the calibration step (use with caution)')
    parser.add_argument('--single-model', action='store_true',
                       help='Use only 8s model (faster, less comprehensive)')
    parser.add_argument('--sample-rate', type=int, default=SAMPLE_RATE,
                       help=f'Sampling rate in Hz (default: {SAMPLE_RATE})')
    parser.add_argument('--window-duration-8s', type=int, default=WINDOW_DURATION_8S,
                       help=f'8s Window duration in seconds (default: {WINDOW_DURATION_8S})')
    parser.add_argument('--overlap-8s', type=int, default=OVERLAP_8S,
                       help=f'8s Overlap duration in seconds (default: {OVERLAP_8S})')
    parser.add_argument('--window-duration-20s', type=int, default=WINDOW_DURATION_20S,
                       help=f'20s Window duration in seconds (default: {WINDOW_DURATION_20S})')
    parser.add_argument('--overlap-20s', type=int, default=OVERLAP_20S,
                       help=f'20s Overlap duration in seconds (default: {OVERLAP_20S})')
    
    args = parser.parse_args()
    
    # Validate ADC channel
    if not 0 <= args.adc_channel <= 7:
        print("Error: ADC channel must be between 0 and 7")
        sys.exit(1)
    
    # Validate sampling rate
    if args.sample_rate <= 0:
        print("Error: Sample rate must be positive")
        sys.exit(1)
    
    # Validate window duration
    if args.window_duration_8s <= 0 or args.window_duration_20s <= 0:
        print("Error: Window duration must be positive")
        sys.exit(1)
    
    # Validate overlap
    if args.overlap_8s < 0 or args.overlap_8s >= args.window_duration_8s or args.overlap_20s < 0 or args.overlap_20s >= args.window_duration_20s:
        print("Error: Overlap must be >= 0 and < window duration")
        sys.exit(1)
    
    main(
        channel=args.adc_channel,
        sample_rate=args.sample_rate,
        window_duration_8s=args.window_duration_8s,
        overlap_8s=args.overlap_8s,
        window_duration_20s=args.window_duration_20s,
        overlap_20s=args.overlap_20s,
        calibrate=args.calibrate,
        use_dual_models=not args.single_model
    )