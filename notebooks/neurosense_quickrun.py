"""
Quick Test Script for NeuroSense Pipeline
Test the entire flow with a small subset of data
"""

import numpy as np
import time
from neurosense_preprocessor import NeuroSensePreprocessor
from neurosense_ml import run_neurosense_ml_analysis

def create_minimal_test_dataset(n_subjects=3, n_trials=2):
    """
    Create minimal synthetic dataset for testing
    """
    print(f"Creating test dataset: {n_subjects} subjects, {n_trials} trials each")
    
    sampling_rate = 256
    trial_duration = 63  # 63 seconds per trial
    n_samples_per_trial = sampling_rate * trial_duration
    n_channels = 4
    
    all_eeg_data = []
    all_events = []
    all_baseline_events = []
    all_subject_ids = []
    all_valence = []
    all_arousal = []
    
    current_sample = 0
    
    for subject_id in range(1, n_subjects + 1):
        for trial in range(n_trials):
            # Generate synthetic EEG
            time_vec = np.linspace(0, trial_duration, n_samples_per_trial)
            eeg_trial = np.zeros((n_samples_per_trial, n_channels))
            
            for ch in range(n_channels):
                # Base noise + alpha rhythm
                noise = np.random.randn(n_samples_per_trial) * 10
                alpha = 3 * np.sin(2 * np.pi * 10 * time_vec)
                eeg_trial[:, ch] = noise + alpha
            
            all_eeg_data.append(eeg_trial)
            
            # Events: baseline at start, stimulus at 3s
            baseline_start = current_sample
            stimulus_start = current_sample + 3 * sampling_rate
            
            all_baseline_events.append([baseline_start, 0, 1])
            all_events.append([stimulus_start, 0, 1])
            
            # Emotion scores (alternate between quadrants)
            if trial == 0:
                valence, arousal = 7.0, 7.0  # Happy
            else:
                valence, arousal = 3.0, 3.0  # Sad
            
            all_valence.append(valence)
            all_arousal.append(arousal)
            all_subject_ids.append(subject_id)
            
            current_sample += n_samples_per_trial
    
    # Combine data
    combined_eeg = np.concatenate(all_eeg_data, axis=0)
    
    return {
        'eeg_data': combined_eeg,
        'events': np.array(all_events),
        'baseline_events': np.array(all_baseline_events),
        'subject_ids': np.array(all_subject_ids),
        'valence_scores': np.array(all_valence),
        'arousal_scores': np.array(all_arousal),
        'event_id': {'stimulus': 1}
    }

def test_preprocessing_only(dataset, segment_length=5.0):
    """
    Test only the preprocessing pipeline
    """
    print("\n" + "="*50)
    print("TESTING PREPROCESSING PIPELINE")
    print("="*50)
    
    preprocessor = NeuroSensePreprocessor()
    
    print(f"Input data shape: {dataset['eeg_data'].shape}")
    print(f"Number of events: {len(dataset['events'])}")
    
    start_time = time.time()
    
    # Create epochs with specific segment length
    epochs = preprocessor.create_epochs_structure(
        dataset['eeg_data'],
        dataset['events'],
        dataset['event_id'],
        tmin=0.0, tmax=segment_length
    )
    
    # Apply filtering
    epochs_filtered = preprocessor.apply_fir_filter(epochs)
    
    # Remove artifacts
    epochs_clean = preprocessor.remove_artifacts(epochs_filtered)
    
    # Create sub-epochs
    stimulus_data, stimulus_labels = preprocessor.create_subepochs(epochs_clean)
    
    # Process baseline
    baseline_data = None
    if dataset['baseline_events'] is not None:
        baseline_epochs = preprocessor.create_epochs_structure(
            dataset['eeg_data'],
            dataset['baseline_events'],
            {'baseline': 1},
            tmin=0.0, tmax=3.0
        )
        baseline_filtered = preprocessor.apply_fir_filter(baseline_epochs)
        baseline_clean = preprocessor.remove_artifacts(baseline_filtered)
        baseline_data, _ = preprocessor.create_subepochs(baseline_clean)
    
    result = {
        'stimulus_data': stimulus_data,
        'stimulus_labels': stimulus_labels,
        'baseline_data': baseline_data,
        'epochs': epochs_clean
    }
    
    processing_time = time.time() - start_time
    
    print("\nPreprocessing Results:")
    print(f"  Stimulus data: {result['stimulus_data'].shape}")
    print(f"  Baseline data: {result['baseline_data'].shape if result['baseline_data'] is not None else None}")
    print(f"  Processing time: {processing_time:.2f} seconds")
    
    # Quick visualization
    if result['stimulus_data'].shape[0] > 0:
        preprocessor.plot_preprocessing_comparison(
            dataset['eeg_data'],
            dataset['events'],
            dataset['event_id'],
            channel_idx=0,
            epoch_idx=0
        )
    
    return result

def test_full_pipeline(dataset, segment_length=5.0):
    """
    Test the complete ML pipeline
    """
    print("\n" + "="*50)
    print("TESTING COMPLETE ML PIPELINE")
    print("="*50)
    
    start_time = time.time()
    
    # Run complete analysis
    results = run_neurosense_ml_analysis(dataset, segment_length=segment_length)
    
    total_time = time.time() - start_time
    
    print(f"\nTotal processing time: {total_time:.2f} seconds")
    print("\nPipeline test completed successfully!")
    
    return results

def quick_test_run(test_mode="preprocessing"):
    """
    Run quick test of the entire pipeline
    
    Parameters:
    test_mode: str
        'preprocessing' - Test only preprocessing (fastest)
        'full' - Test complete ML pipeline
    """
    
    print("NeuroSense Pipeline Quick Test")
    print(f"Mode: {test_mode}")
    print("="*50)
    
    # Create minimal test dataset
    dataset = create_minimal_test_dataset(n_subjects=3, n_trials=2)
    
    print("Test dataset created:")
    print(f"  Total samples: {dataset['eeg_data'].shape[0]:,}")
    print(f"  Channels: {dataset['eeg_data'].shape[1]}")
    print(f"  Subjects: {len(np.unique(dataset['subject_ids']))}")
    print(f"  Trials: {len(dataset['events'])}")
    
    if test_mode == "preprocessing":
        # Test preprocessing only (much faster)
        result = test_preprocessing_only(dataset, segment_length=5.0)
        
        print("\nPreprocessing test completed!")
        print("Next steps:")
        print("1. If preprocessing works, try test_mode='full'")
        print("2. If successful, run on your real dataset")
        
        return result
        
    elif test_mode == "full":
        # Test complete pipeline
        results = test_full_pipeline(dataset, segment_length=5.0)
        
        print("\nFull pipeline test completed!")
        print("Pipeline is ready for your real dataset.")
        
        return results
    
    else:
        print(f"Unknown test_mode: {test_mode}")
        print("Use 'preprocessing' or 'full'")

if __name__ == "__main__":
    # Quick preprocessing test (30 seconds)
    # print("Running preprocessing test...")
    # preprocessing_result = quick_test_run(test_mode="preprocessing")
    
    # If preprocessing works, uncomment to test full pipeline
    print("\nRunning full pipeline test...")
    full_result = quick_test_run(test_mode="full")