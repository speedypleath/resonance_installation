"""EEG data processing pipeline."""

import numpy as np
import time
from typing import Any, Dict, List, Optional, Tuple
from collections import deque
from datetime import datetime, timezone
from pylsl import StreamInlet, resolve_byprop

from .base import BiometricPipeline, PipelineResult
from ..models.base import EEGModel
from ..osc.osc_client import OSCClient


class DummyEEGModel:
    """Dummy EEG model for data visualization without processing."""
    
    def __init__(self):
        self.is_loaded = True
        self.model_path = None
        self.device = "cpu"
    
    def get_model_info(self):
        return {
            "model_type": "DummyEEGModel",
            "is_loaded": True,
            "purpose": "Data visualization only"
        }


class EEGPipeline(BiometricPipeline):
    """Pipeline for real-time EEG data processing and segmentation."""
    
    def __init__(self, model: Optional[EEGModel] = None, osc_client: Optional[OSCClient] = None,
                 fragment_duration: float = 10.0, window_step: float = 5.0,
                 segment_duration: float = 2.0, segment_overlap: float = 0.5):
        
        # Create dummy model if none provided - BEFORE calling super().__init__
        if model is None:
            model = DummyEEGModel()
            print("EEG Pipeline: Created dummy model for visualization")
        
        super().__init__("eeg_processing", model, osc_client)
        
        self.fragment_duration = fragment_duration
        self.window_step = window_step
        self.segment_duration = segment_duration
        self.segment_overlap = segment_overlap
        
        # Stream parameters (will be updated when stream is found)
        self.sampling_rate = 256
        self.n_channels = 4
        self.channel_names = ['TP9', 'AF7', 'AF8', 'TP10']
        
        # Calculate buffer sizes
        self._update_buffer_sizes()
        
        # Data storage
        self.data_buffer = deque(maxlen=self.fragment_samples * 2)
        self.timestamps_buffer = deque(maxlen=self.fragment_samples * 2)
        self.fragments = []
        self.current_segments = []
        
        # LSL stream
        self.inlet = None
        self.stream_info = None
        
        # Statistics
        self.fragment_count = 0
        self.segment_count = 0
        self.last_fragment_time = None
        self.samples_received = 0
    
    def _update_buffer_sizes(self) -> None:
        """Update buffer sizes based on sampling rate."""
        self.fragment_samples = int(self.fragment_duration * self.sampling_rate)
        self.window_step_samples = int(self.window_step * self.sampling_rate)
        self.segment_samples = int(self.segment_duration * self.sampling_rate)
    
    def find_eeg_stream(self, timeout: float = 10.0) -> bool:
        """Find and connect to EEG LSL stream."""
        print("Looking for EEG stream...")
        
        try:
            # Look for EEG streams
            streams = resolve_byprop('type', 'EEG', timeout=timeout)
            
            if not streams:
                return False

            self.stream_info = streams[0]
            print(f"Found EEG stream: {self.stream_info.name()}")
            print(f"Sampling rate: {self.stream_info.nominal_srate()} Hz")
            print(f"Channels: {self.stream_info.channel_count()}")
            
            # Create inlet
            self.inlet = StreamInlet(self.stream_info, max_buflen=360, max_chunklen=12)
            self.sampling_rate = int(self.stream_info.nominal_srate())
            self.n_channels = self.stream_info.channel_count()
            
            # Update channel names and buffer sizes
            if self.n_channels != len(self.channel_names):
                self.channel_names = [f'Ch{i+1}' for i in range(self.n_channels)]
            
            self._update_buffer_sizes()
            
            return True
            
        except Exception as e:
            print(f"Error connecting to EEG stream: {e}")
            return False
    
    def start(self) -> bool:
        """Start EEG data collection."""
        if not self.inlet and not self.find_eeg_stream():
            print("Cannot start EEG pipeline: no LSL stream available")
            print("Make sure your EEG device is connected and streaming via LSL")
            return False
        
        return super().start()
    
    def _get_run_loop(self):
        """Override to use LSL data collection loop instead of queue-based loop."""
        return self._lsl_data_collection_loop
    
    def _simulation_loop(self) -> None:
        """Simulate EEG data when no LSL streams are available."""
        print("Starting EEG simulation loop...")
        print("Generating synthetic EEG data for visualization")
        
        import numpy as np
        
        chunk_size = 32
        sample_count = 0
        
        while not self._stop_event.is_set():
            try:
                if self._pause_event.is_set():
                    time.sleep(0.1)
                    continue
                
                # Generate realistic EEG data
                samples = []
                timestamps = []
                current_time = time.time()
                
                for i in range(chunk_size):
                    # Create synthetic EEG signals with realistic characteristics
                    sample = []
                    t = (sample_count + i) / self.sampling_rate
                    
                    for ch in range(self.n_channels):
                        # Base noise
                        signal = np.random.normal(0, 5)
                        
                        # Add typical EEG frequency components
                        signal += 10 * np.sin(2 * np.pi * 10 * t + ch * np.pi/2)  # Alpha (10Hz)
                        signal += 5 * np.sin(2 * np.pi * 20 * t + ch * np.pi/3)   # Beta (20Hz)
                        signal += 3 * np.sin(2 * np.pi * 4 * t + ch * np.pi/4)    # Theta (4Hz)
                        
                        # Add some random artifacts occasionally
                        if np.random.random() < 0.01:  # 1% chance
                            signal += np.random.normal(0, 20)  # Artifact
                        
                        sample.append(signal)
                    
                    samples.append(sample)
                    timestamps.append(current_time + i * (1/self.sampling_rate))
                
                # Process the simulated data
                result = self.process_data((samples, timestamps))
                
                # Handle result same as real data
                self.process_count += 1
                if not result.success:
                    self.error_count += 1
                
                # Send to output queue
                try:
                    self.output_queue.put(result, block=False)
                except:
                    try:
                        self.output_queue.get_nowait()
                        self.output_queue.put(result, block=False)
                    except:
                        pass
                
                # Call callbacks
                for callback in self.result_callbacks:
                    try:
                        callback(result)
                    except Exception as e:
                        print(f"Error in EEG callback: {e}")
                
                # Send OSC data
                if result.success and self.osc_client:
                    try:
                        self._send_osc_data(result)
                    except Exception as e:
                        print(f"Error sending EEG OSC data: {e}")
                
                # Log new fragments (less frequently than real data)
                for fragment in result.predictions.get("fragments", []):
                    print(f"Simulated EEG Fragment {fragment['fragment_id']}: "
                          f"{fragment['duration']:.2f}s, {len(fragment['data'])} samples")
                
                sample_count += len(samples)
                
                # Sleep to maintain realistic timing
                time.sleep(chunk_size / self.sampling_rate)
                
            except Exception as e:
                self.error_count += 1
                print(f"Error in EEG simulation: {e}")
                time.sleep(0.1)
        
        print("EEG simulation loop ended")
    
    def validate_input(self, data: Any) -> bool:
        """Validate EEG data input."""
        return isinstance(data, (list, np.ndarray)) and len(data) > 0
    
    def process_data(self, samples_chunk: Tuple[List, List]) -> PipelineResult:
        """Process EEG samples chunk."""
        timestamp = time.time()
        samples, timestamps = samples_chunk
        
        try:
            # Add samples to buffer
            for sample, ts in zip(samples, timestamps):
                self.data_buffer.append(sample)
                self.timestamps_buffer.append(ts)
            
            self.samples_received += len(samples)
            
            # Check if we can create a new fragment
            fragments_created = []
            segments_created = []
            
            if len(self.data_buffer) >= self.fragment_samples:
                if (self.last_fragment_time is None or 
                    timestamp - self.last_fragment_time >= self.window_step):
                    
                    fragment, segments = self._create_fragment_and_segments()
                    if fragment:
                        fragments_created.append(fragment)
                        segments_created.extend(segments)
                        self.last_fragment_time = timestamp
            
            return PipelineResult(
                timestamp=timestamp,
                data_type="eeg",
                predictions={
                    "fragments": fragments_created,
                    "segments": segments_created,
                    "buffer_status": {
                        "size": len(self.data_buffer),
                        "capacity": self.fragment_samples * 2
                    }
                },
                raw_data={
                    "samples": samples,
                    "timestamps": timestamps,
                    "n_samples": len(samples)
                },
                metadata={
                    "sampling_rate": self.sampling_rate,
                    "n_channels": self.n_channels,
                    "fragment_count": self.fragment_count,
                    "segment_count": self.segment_count
                },
                success=True
            )
            
        except Exception as e:
            return PipelineResult(
                timestamp=timestamp,
                data_type="eeg",
                predictions={},
                raw_data={"samples": samples, "timestamps": timestamps},
                metadata={},
                success=False,
                error_message=str(e)
            )
    
    def _create_fragment_and_segments(self) -> Tuple[Optional[Dict], List[Dict]]:
        """Create fragment and segments from current buffer."""
        try:
            # Extract fragment data
            fragment_data = np.array(list(self.data_buffer)[-self.fragment_samples:])
            fragment_timestamps = np.array(list(self.timestamps_buffer)[-self.fragment_samples:])
            
            fragment = {
                'data': fragment_data,
                'timestamps': fragment_timestamps,
                'fragment_id': self.fragment_count,
                'start_time': fragment_timestamps[0],
                'end_time': fragment_timestamps[-1],
                'duration': fragment_timestamps[-1] - fragment_timestamps[0],
                'created_at': str(datetime.now(timezone.utc))
            }
            
            # Store fragment
            self.fragments.append(fragment)
            self.fragment_count += 1
            
            # Create segments
            segments = self._create_segments_from_fragment(fragment)
            self.current_segments = segments
            
            # Keep memory usage reasonable
            if len(self.fragments) > 50:
                self.fragments.pop(0)
            
            return fragment, segments
            
        except Exception as e:
            print(f"Error creating fragment and segments: {e}")
            return None, []
    
    def _create_segments_from_fragment(self, fragment: Dict) -> List[Dict]:
        """Create segments from a fragment."""
        data = fragment['data']
        timestamps = fragment['timestamps']
        time_axis = timestamps - timestamps[0]
        
        overlap_samples = int(self.segment_samples * self.segment_overlap)
        step_samples = self.segment_samples - overlap_samples
        
        segments = []
        segment_id = 0
        
        for start_idx in range(0, len(data) - self.segment_samples + 1, step_samples):
            end_idx = start_idx + self.segment_samples
            
            segment = {
                'segment_id': segment_id,
                'fragment_id': fragment['fragment_id'],
                'data': data[start_idx:end_idx],
                'time': time_axis[start_idx:end_idx],
                'timestamps': timestamps[start_idx:end_idx],
                'start_time': float(time_axis[start_idx]),
                'end_time': float(time_axis[end_idx-1]),
                'duration': float(time_axis[end_idx-1] - time_axis[start_idx]),
                'created_at': str(datetime.now(timezone.utc))
            }
            
            segments.append(segment)
            segment_id += 1
            self.segment_count += 1
        
        return segments
    
    def _send_osc_data(self, result: PipelineResult) -> None:
        """Send EEG data via OSC."""
        if not result.success:
            return
        
        predictions = result.predictions
        
        # Send fragment data
        for fragment in predictions.get("fragments", []):
            # Send average channel values for the fragment
            avg_channels = np.mean(fragment['data'], axis=0).tolist()
            self.osc_client.send_eeg_data(avg_channels, fragment['fragment_id'])
        
        # Send segment data
        for segment in predictions.get("segments", []):
            # Send segment as flattened channel data
            segment_data = segment['data'].tolist()
            self.osc_client.send_eeg_segment(segment['segment_id'], segment_data)
    
    def _lsl_data_collection_loop(self) -> None:
        """Main LSL data collection and processing loop."""
        if not self.inlet:
            print("ERROR: No LSL inlet available for EEG data collection")
            return
        
        print(f"Starting EEG data collection from LSL stream...")
        print(f"Stream: {self.stream_info.name()} ({self.n_channels} channels @ {self.sampling_rate}Hz)")
        
        consecutive_failures = 0
        max_failures = 50  # 5 seconds at 10 attempts per second
        
        while not self._stop_event.is_set():
            try:
                # Wait if paused
                if self._pause_event.is_set():
                    time.sleep(0.1)
                    continue
                
                # Pull data from LSL stream
                samples, timestamps = self.inlet.pull_chunk(timeout=0.1, max_samples=32)
                
                if samples and timestamps:
                    consecutive_failures = 0
                    
                    # Process the data chunk
                    result = self.process_data((samples, timestamps))
                    
                    # Update statistics
                    self.process_count += 1
                    if not result.success:
                        self.error_count += 1
                    
                    # Send to output queue (non-blocking)
                    try:
                        self.output_queue.put(result, block=False)
                    except:
                        # Queue full, remove old results
                        try:
                            self.output_queue.get_nowait()
                            self.output_queue.put(result, block=False)
                        except:
                            pass
                    
                    # Call result callbacks
                    for callback in self.result_callbacks:
                        try:
                            callback(result)
                        except Exception as e:
                            print(f"Error in EEG callback: {e}")
                    
                    # Send OSC data if successful
                    if result.success and self.osc_client:
                        try:
                            self._send_osc_data(result)
                        except Exception as e:
                            print(f"Error sending EEG OSC data: {e}")
                    
                    # Log new fragments and segments (less frequently)
                    for fragment in result.predictions.get("fragments", []):
                        print(f"EEG Fragment {fragment['fragment_id']}: "
                              f"{fragment['duration']:.2f}s, {len(fragment['data'])} samples")
                
                else:
                    # No data received
                    consecutive_failures += 1
                    if consecutive_failures > max_failures:
                        print(f"WARNING: No EEG data received for {max_failures * 0.1:.1f} seconds")
                        consecutive_failures = 0  # Reset to avoid spam
                    
                    time.sleep(0.1)  # Wait before trying again
                
            except Exception as e:
                self.error_count += 1
                print(f"Error in EEG data collection: {e}")
                time.sleep(0.1)
        
        print("EEG data collection loop ended")
    
    def collect_lsl_data(self) -> None:
        """Continuously collect data from LSL stream."""
        if not self.inlet:
            return
        
        print("Starting EEG data collection from LSL stream...")
        
        while self.is_running:
            try:
                samples, timestamps = self.inlet.pull_chunk(timeout=1.0, max_samples=32)
                
                if samples:
                    # Add to processing queue
                    self.add_data((samples, timestamps))
                    
            except Exception as e:
                print(f"Error collecting LSL data: {e}")
                time.sleep(0.1)
    
    def get_latest_fragment(self) -> Optional[Dict]:
        """Get the most recent fragment."""
        return self.fragments[-1] if self.fragments else None
    
    def get_latest_segments(self) -> List[Dict]:
        """Get the most recent segments."""
        return self.current_segments.copy()
    
    def get_buffer_data(self) -> Dict[str, Any]:
        """Get current buffer data for visualization."""
        if len(self.data_buffer) == 0:
            return {}
        
        data = np.array(list(self.data_buffer))
        timestamps = np.array(list(self.timestamps_buffer))
        
        return {
            "data": data,
            "timestamps": timestamps,
            "time_axis": timestamps - timestamps[0] if len(timestamps) > 0 else np.array([]),
            "n_samples": len(data),
            "duration": timestamps[-1] - timestamps[0] if len(timestamps) > 1 else 0.0
        }
    
    def get_eeg_stats(self) -> Dict[str, Any]:
        """Get EEG-specific statistics."""
        stats = self.get_stats()
        stats.update({
            "fragment_count": self.fragment_count,
            "segment_count": self.segment_count,
            "samples_received": self.samples_received,
            "buffer_utilization": len(self.data_buffer) / (self.fragment_samples * 2),
            "stream_info": {
                "name": self.stream_info.name() if self.stream_info else None,
                "sampling_rate": self.sampling_rate,
                "n_channels": self.n_channels,
                "channel_names": self.channel_names
            }
        })
        return stats


class EEGDataProcessor:
    """Utility class for EEG data processing and analysis."""
    
    @staticmethod
    def compute_band_power(data: np.ndarray, sampling_rate: int, 
                          freq_bands: Dict[str, Tuple[float, float]]) -> Dict[str, np.ndarray]:
        """Compute power in frequency bands for each channel."""
        from scipy import signal
        
        # Default EEG frequency bands
        if not freq_bands:
            freq_bands = {
                'delta': (0.5, 4),
                'theta': (4, 8),
                'alpha': (8, 13),
                'beta': (13, 30),
                'gamma': (30, 100)
            }
        
        band_powers = {}
        
        for band_name, (low_freq, high_freq) in freq_bands.items():
            # Design bandpass filter
            sos = signal.butter(4, [low_freq, high_freq], btype='band', 
                              fs=sampling_rate, output='sos')
            
            # Apply filter to each channel
            filtered_data = signal.sosfilt(sos, data, axis=0)
            
            # Compute power (RMS)
            power = np.sqrt(np.mean(filtered_data**2, axis=0))
            band_powers[band_name] = power
        
        return band_powers
    
    @staticmethod
    def compute_coherence(data: np.ndarray, sampling_rate: int) -> np.ndarray:
        """Compute coherence between channels."""
        from scipy import signal
        
        n_channels = data.shape[1]
        coherence_matrix = np.zeros((n_channels, n_channels))
        
        for i in range(n_channels):
            for j in range(i, n_channels):
                if i == j:
                    coherence_matrix[i, j] = 1.0
                else:
                    # Compute coherence
                    f, Cxy = signal.coherence(data[:, i], data[:, j], 
                                            fs=sampling_rate, nperseg=min(256, len(data)//4))
                    # Average coherence across frequencies
                    avg_coherence = np.mean(Cxy)
                    coherence_matrix[i, j] = avg_coherence
                    coherence_matrix[j, i] = avg_coherence
        
        return coherence_matrix
    
    @staticmethod
    def detect_artifacts(data: np.ndarray, threshold_std: float = 3.0) -> Dict[str, Any]:
        """Detect artifacts in EEG data."""
        artifacts = {
            'muscle_artifacts': [],
            'eye_artifacts': [],
            'channel_artifacts': {},
            'global_artifacts': []
        }
        
        # Simple artifact detection based on amplitude thresholds
        for ch in range(data.shape[1]):
            channel_data = data[:, ch]
            std_val = np.std(channel_data)
            mean_val = np.mean(channel_data)
            
            # Find samples exceeding threshold
            outliers = np.where(np.abs(channel_data - mean_val) > threshold_std * std_val)[0]
            
            if len(outliers) > 0:
                artifacts['channel_artifacts'][f'Ch{ch+1}'] = {
                    'outlier_indices': outliers.tolist(),
                    'outlier_count': len(outliers),
                    'percentage': len(outliers) / len(channel_data) * 100
                }
        
        return artifacts


