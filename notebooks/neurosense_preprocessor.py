import numpy as np
import mne
from sklearn.neighbors import LocalOutlierFactor
from meegkit.detrend import reduce_ringing
import warnings
warnings.filterwarnings('ignore')

class NeuroSensePreprocessor:
    """
    EEG preprocessing pipeline for NeuroSense dataset following the paper methodology
    """
    
    def __init__(self, sampling_rate=256, filter_low=1, filter_high=45):
        self.sampling_rate = sampling_rate
        self.filter_low = filter_low
        self.filter_high = filter_high
        self.channel_names = ['AF7', 'AF8', 'TP9', 'TP10']
        
    def create_epochs_structure(self, raw_data, events, event_id, tmin=-0.5, tmax=5.0):
        """
        Create EEG epochs structure using MNE framework
        """
        info = mne.create_info(
            ch_names=self.channel_names,
            sfreq=self.sampling_rate,
            ch_types='eeg'
        )
        
        raw = mne.io.RawArray(raw_data.T, info)
        
        epochs = mne.Epochs(
            raw, events, event_id,
            tmin=tmin, tmax=tmax,
            baseline=None,
            preload=True,
            verbose=False
        )
        
        return epochs
    
    def apply_fir_filter(self, epochs):
        """
        Apply FIR filter with hamming window (1-45 Hz)
        """
        epochs_filtered = epochs.copy().filter(
            l_freq=self.filter_low,
            h_freq=self.filter_high,
            fir_window='hamming',
            verbose=False
        )
        
        return epochs_filtered
    
    def remove_artifacts(self, epochs, contamination=0.1, batch_size=10):
        """
        Optimized artifact removal using K-NN outlier detection and meegkit's reduce_ringing
        """
        data = epochs.get_data()
        n_epochs, n_channels, n_times = data.shape
        
        print(f"Processing {n_epochs} epochs with {n_times} samples each...")
        
        for epoch_idx in range(n_epochs):
            if (epoch_idx + 1) % batch_size == 0:
                print(f"  Processed {epoch_idx + 1}/{n_epochs} epochs")
                
            for ch_idx in range(n_channels):
                epoch_data = data[epoch_idx, ch_idx, :]
                
                # Downsample for outlier detection to reduce computation
                downsample_factor = max(1, n_times // 5000)  # Max 5000 points for LOF
                if downsample_factor > 1:
                    downsampled_data = epoch_data[::downsample_factor]
                    downsampled_indices = np.arange(0, n_times, downsample_factor)
                else:
                    downsampled_data = epoch_data
                    downsampled_indices = np.arange(n_times)
                
                # K-NN outlier detection on downsampled data
                epoch_reshaped = downsampled_data.reshape(-1, 1)
                
                lof = LocalOutlierFactor(
                    n_neighbors=min(20, len(downsampled_data)//2),
                    contamination=contamination,
                    novelty=False,
                    n_jobs=1  # Single job per channel to avoid nested parallelism
                )
                
                outlier_labels = lof.fit_predict(epoch_reshaped)
                outlier_downsampled_indices = downsampled_indices[outlier_labels == -1]
                
                # Map back to full resolution with expansion around outliers
                if len(outlier_downsampled_indices) > 0:
                    outlier_indices = []
                    expand_samples = downsample_factor * 2  # Expand around detected outliers
                    
                    for idx in outlier_downsampled_indices:
                        start_idx = max(0, idx - expand_samples)
                        end_idx = min(n_times, idx + expand_samples)
                        outlier_indices.extend(range(start_idx, end_idx))
                    
                    outlier_indices = np.unique(outlier_indices)
                    
                    # Apply reduce_ringing if artifacts detected
                    if len(outlier_indices) > 0:
                        X_reshaped = epoch_data.reshape(-1, 1)
                        cleaned_data = reduce_ringing(X_reshaped, samples=outlier_indices)
                        data[epoch_idx, ch_idx, :] = cleaned_data.flatten()
        
        epochs._data = data
        return epochs

    def preprocess_pipeline_optimized(self, raw_data, events, event_id, baseline_events=None, segment_length=10.0, subepoch_length=5.0,
                                    max_samples_per_batch=1000000):
        """
        Optimized preprocessing pipeline for large datasets
        """
        total_samples = raw_data.shape[0]
        
        if total_samples <= max_samples_per_batch:
            # Process normally if dataset is small enough
            return self.preprocess_pipeline(raw_data, events, event_id, baseline_events, segment_length=segment_length, subepoch_length=subepoch_length)

        print(f"Large dataset detected ({total_samples} samples). Using batch processing...")
        
        # Calculate batch parameters
        n_batches = int(np.ceil(total_samples / max_samples_per_batch))
        batch_size = total_samples // n_batches
        
        all_stimulus_data = []
        all_stimulus_labels = []
        all_baseline_data = []
        
        for batch_idx in range(n_batches):
            start_idx = batch_idx * batch_size
            end_idx = min((batch_idx + 1) * batch_size, total_samples)
            
            print(f"\nProcessing batch {batch_idx + 1}/{n_batches} "
                  f"(samples {start_idx}:{end_idx})")
            
            # Extract batch data
            batch_data = raw_data[start_idx:end_idx]
            
            # Filter events for this batch
            batch_events = events[(events[:, 0] >= start_idx) & (events[:, 0] < end_idx)]
            batch_events = batch_events.copy()
            batch_events[:, 0] -= start_idx  # Adjust event times to batch
            
            batch_baseline_events = None
            if baseline_events is not None:
                batch_baseline_events = baseline_events[
                    (baseline_events[:, 0] >= start_idx) & (baseline_events[:, 0] < end_idx)
                ]
                if len(batch_baseline_events) > 0:
                    batch_baseline_events = batch_baseline_events.copy()
                    batch_baseline_events[:, 0] -= start_idx
                else:
                    batch_baseline_events = None
            
            # Process batch
            if len(batch_events) > 0:
                result = self.preprocess_pipeline(
                    batch_data, batch_events, event_id, batch_baseline_events
                )
                
                all_stimulus_data.append(result['stimulus_data'])
                all_stimulus_labels.append(result['stimulus_labels'])
                
                if result['baseline_data'] is not None:
                    all_baseline_data.append(result['baseline_data'])
        
        # Combine results
        combined_stimulus = np.concatenate(all_stimulus_data, axis=0) if all_stimulus_data else None
        combined_labels = np.concatenate(all_stimulus_labels, axis=0) if all_stimulus_labels else None
        combined_baseline = np.concatenate(all_baseline_data, axis=0) if all_baseline_data else None
        
        print("\nBatch processing complete!")
        
        return {
            'stimulus_data': combined_stimulus,
            'stimulus_labels': combined_labels,
            'baseline_data': combined_baseline,
            'epochs': None  # Not available in batch mode
        }
    
    def create_subepochs(self, epochs, subepoch_length=5.0):
        """
        Divide processed EEG data into 5-second sub-epochs
        """
        data = epochs.get_data()
        sfreq = epochs.info['sfreq']
        
        samples_per_subepoch = int(subepoch_length * sfreq)
        
        subepochs_data = []
        subepochs_labels = []
        
        for epoch_idx, epoch_data in enumerate(data):
            if epoch_data.shape[1] < samples_per_subepoch:
                continue
                
            n_subepochs = epoch_data.shape[1] // samples_per_subepoch
            
            for sub_idx in range(n_subepochs):
                start_sample = sub_idx * samples_per_subepoch
                end_sample = start_sample + samples_per_subepoch
                
                subepoch = epoch_data[:, start_sample:end_sample]
                subepochs_data.append(subepoch)
                subepochs_labels.append(epochs.events[epoch_idx, 2])
        
        return np.array(subepochs_data), np.array(subepochs_labels)

    def preprocess_pipeline(self, raw_data, events, event_id, baseline_events=None, segment_length=10.0, subepoch_length=5.0):
        """
        Complete preprocessing pipeline following paper methodology
        """
        epochs = self.create_epochs_structure(raw_data, events, event_id, tmin=0.0, tmax=segment_length)
        epochs_filtered = self.apply_fir_filter(epochs)
        epochs_clean = self.remove_artifacts(epochs_filtered)
        subepochs_data, subepochs_labels = self.create_subepochs(epochs_clean, subepoch_length=subepoch_length)

        baseline_data = None
        if baseline_events is not None:
            baseline_epochs = self.create_epochs_structure(
                raw_data, baseline_events, {'baseline': 1}, tmin=0.0, tmax=3.0
            )
            baseline_filtered = self.apply_fir_filter(baseline_epochs)
            baseline_clean = self.remove_artifacts(baseline_filtered)
            baseline_data, _ = self.create_subepochs(baseline_clean, subepoch_length=subepoch_length)

        return {
            'stimulus_data': subepochs_data,
            'stimulus_labels': subepochs_labels,
            'baseline_data': baseline_data,
            'epochs': epochs_clean
        }

    def plot_preprocessing_comparison(self, raw_data, events, event_id, channel_idx=0, epoch_idx=0):
        """
        Plot before and after preprocessing comparison
        """
        import matplotlib.pyplot as plt
        
        # Process data
        epochs_original = self.create_epochs_structure(raw_data, events, event_id)
        epochs_filtered = self.apply_fir_filter(epochs_original)
        epochs_clean = self.remove_artifacts(epochs_filtered)
        
        # Get data for plotting
        original_data = epochs_original.get_data()[epoch_idx, channel_idx, :]
        filtered_data = epochs_filtered.get_data()[epoch_idx, channel_idx, :]
        clean_data = epochs_clean.get_data()[epoch_idx, channel_idx, :]
        
        # Time vector
        time = np.arange(len(original_data)) / self.sampling_rate
        
        # Create plots
        fig, axes = plt.subplots(3, 1, figsize=(12, 8))
        
        # Original data
        axes[0].plot(time, original_data, 'b-', linewidth=0.8)
        axes[0].set_title(f'Original EEG Data - Channel {self.channel_names[channel_idx]}')
        axes[0].set_ylabel('Amplitude (µV)')
        axes[0].grid(True, alpha=0.3)
        
        # Filtered data
        axes[1].plot(time, filtered_data, 'g-', linewidth=0.8)
        axes[1].set_title('After FIR Filter (1-45 Hz, Hamming window)')
        axes[1].set_ylabel('Amplitude (µV)')
        axes[1].grid(True, alpha=0.3)
        
        # Clean data
        axes[2].plot(time, clean_data, 'r-', linewidth=0.8)
        axes[2].set_title('After Artifact Removal (K-NN + reduce_ringing)')
        axes[2].set_xlabel('Time (s)')
        axes[2].set_ylabel('Amplitude (µV)')
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

    def load_dataset_from_csv(self, csv_path):
        """
        Load NeuroSense dataset using CSV metadata file
        
        Parameters:
        csv_path: str
            Path to CSV file with columns: subject_id, trial_id, valence, arousal, file_path
            
        Returns:
        dict: Dataset containing all subjects' data
        """
        import pandas as pd
        import mne
        
        # Load metadata
        df = pd.read_csv(csv_path)
        
        # Initialize storage
        all_eeg_data = []
        all_events = []
        all_baseline_events = []
        all_subject_ids = []
        all_valence = []
        all_arousal = []
        
        current_sample = 0
        
        print(f"Loading dataset from {len(df)} EDF files...")
        
        for idx, row in df.iterrows():
            subject_id = row['subject_id']
            trial_id = row['trial_id']
            valence = row['valence']
            arousal = row['arousal']
            file_path = row['file_path']
            
            try:
                # Load EDF file using MNE
                raw = mne.io.read_raw_edf(file_path, preload=True, verbose=False)
                
                # Get data in microvolts
                eeg_data = raw.get_data().T  # Transpose to (samples, channels)
                eeg_data *= 1e6  # Convert to microvolts
                
                # Ensure we have 4 channels (Muse 2 electrodes)
                if eeg_data.shape[1] != 4:
                    print(f"Warning: Expected 4 channels, got {eeg_data.shape[1]} for {file_path}")
                    if eeg_data.shape[1] > 4:
                        eeg_data = eeg_data[:, :4]
                    else:
                        continue
                
                all_eeg_data.append(eeg_data)
                
                # Create events based on known structure:
                # - 3 seconds baseline at start
                # - 60 seconds stimulus after baseline (3 to 63 seconds)
                baseline_start = current_sample  # Baseline starts at beginning
                stimulus_start = current_sample + 3 * self.sampling_rate  # Stimulus at 3 seconds
                
                all_baseline_events.append([baseline_start, 0, 1])
                all_events.append([stimulus_start, 0, 1])
                
                # Store metadata
                all_subject_ids.append(subject_id)
                all_valence.append(valence)
                all_arousal.append(arousal)
                
                current_sample += eeg_data.shape[0]
                
                if (idx + 1) % 10 == 0:
                    print(f"Loaded {idx + 1}/{len(df)} files...")
                
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
                continue
        
        # Combine all data
        combined_eeg = np.concatenate(all_eeg_data, axis=0)
        events_array = np.array(all_events)
        baseline_events_array = np.array(all_baseline_events)
        
        print("Dataset loaded successfully:")
        print(f"  - Total samples: {combined_eeg.shape[0]}")
        print(f"  - Channels: {combined_eeg.shape[1]}")
        print(f"  - Trials: {len(all_events)}")
        print(f"  - Subjects: {len(np.unique(all_subject_ids))}")
        print("  - File structure: 3s baseline + 60s stimulus (63s total)")
        
        return {
            'eeg_data': combined_eeg,
            'events': events_array,
            'baseline_events': baseline_events_array,
            'subject_ids': np.array(all_subject_ids),
            'valence_scores': np.array(all_valence),
            'arousal_scores': np.array(all_arousal),
            'event_id': {'stimulus': 1}
        }
        
if __name__ == "__main__":
    processor = NeuroSensePreprocessor()
    dataset = processor.load_dataset_from_csv("./output.csv")
    from neurosense_ml import run_neurosense_ml_analysis

    results = run_neurosense_ml_analysis(dataset)
    print("Analysis results:", results)
    