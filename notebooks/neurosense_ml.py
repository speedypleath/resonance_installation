import numpy as np
from sklearn.model_selection import LeaveOneGroupOut, RandomizedSearchCV
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.metrics import accuracy_score
from sktime.transformations.panel.rocket import MiniRocket
import warnings
warnings.filterwarnings('ignore')

class NeuroSenseMLModel:
    """
    Machine Learning model for NeuroSense emotion recognition using MiniRocket + SVM
    """
    
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.models = {}
        self.best_params = {}
        self.results = {}
        
    def create_russell_quadrant_labels(self, valence_scores, arousal_scores):
        """
        Convert valence and arousal scores to Russell's quadrant labels
        1: High valence, High arousal (Happy)
        2: Low valence, High arousal (Angry) 
        3: Low valence, Low arousal (Sad)
        4: High valence, Low arousal (Relaxed)
        """
        labels = np.zeros(len(valence_scores))
        
        valence_median = np.median(valence_scores)
        arousal_median = np.median(arousal_scores)
        
        for i, (v, a) in enumerate(zip(valence_scores, arousal_scores)):
            if v >= valence_median and a >= arousal_median:
                labels[i] = 1  # Happy
            elif v < valence_median and a >= arousal_median:
                labels[i] = 2  # Angry
            elif v < valence_median and a < arousal_median:
                labels[i] = 3  # Sad
            else:
                labels[i] = 4  # Relaxed
                
        return labels.astype(int)
    
    def create_binary_labels(self, quadrant_labels, target_quadrant):
        """
        Create binary labels for one-vs-all classification
        """
        return (quadrant_labels == target_quadrant).astype(int)
    
    def prepare_time_series_data(self, eeg_data):
        """
        Prepare EEG data for MiniRocket
        Input: (n_samples, n_channels, n_timepoints)
        Output: (n_samples, n_timepoints, n_channels) for sktime
        """
        return eeg_data.transpose(0, 2, 1)
    
    def create_ml_pipeline(self, n_features=10000, max_dilations_per_kernel=32):
        """
        Create ML pipeline with MiniRocket + SVM
        """
        pipeline = Pipeline([
            ('minirocket', MiniRocket(
                num_kernels=n_features,
                max_dilations_per_kernel=max_dilations_per_kernel,
                random_state=self.random_state
            )),
            ('scaler', StandardScaler()),
            ('classifier', SVC(
                kernel='rbf',
                probability=True,
                random_state=self.random_state
            ))
        ])
        
        return pipeline
    
    def define_hyperparameter_grid(self):
        """
        Define hyperparameter grid for optimization
        """
        param_grid = {
            'minirocket__num_kernels': [1000, 5000, 10000],
            'minirocket__max_dilations_per_kernel': [16, 32, 64],
            'scaler': [StandardScaler(), MinMaxScaler(), RobustScaler()],
            'classifier__C': [0.1, 1.0, 10.0, 100.0],
            'classifier__gamma': ['scale', 'auto', 0.001, 0.01, 0.1]
        }
        
        return param_grid
    
    def loso_validation(self, X, y, subject_ids, quadrant_name="unknown"):
        """
        Leave-One-Subject-Out cross-validation
        """
        loso = LeaveOneGroupOut()
        unique_subjects = np.unique(subject_ids)
        
        results = {
            'test_scores': [],
            'train_scores': [],
            'subject_predictions': {},
            'subject_probabilities': {},
            'best_params_per_fold': []
        }
        
        print(f"LOSO validation for {quadrant_name} ({len(unique_subjects)} subjects)...")
        
        for fold_idx, (train_idx, test_idx) in enumerate(loso.split(X, y, subject_ids)):
            test_subject = subject_ids[test_idx[0]]
            print(f"  Fold {fold_idx + 1}: Testing subject {test_subject}")
            
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            
            # Create pipeline and hyperparameter grid
            pipeline = self.create_ml_pipeline()
            param_grid = self.define_hyperparameter_grid()
            
            # Hyperparameter optimization
            search = RandomizedSearchCV(
                pipeline,
                param_grid,
                cv=3,
                scoring='accuracy',
                n_iter=20,  # Reduced for faster processing
                random_state=self.random_state,
                n_jobs=-1
            )
            
            # Fit and predict
            search.fit(X_train, y_train)
            y_pred = search.predict(X_test)
            y_proba = search.predict_proba(X_test)
            
            # Calculate scores
            test_score = accuracy_score(y_test, y_pred)
            train_score = search.score(X_train, y_train)
            
            results['test_scores'].append(test_score)
            results['train_scores'].append(train_score)
            results['subject_predictions'][test_subject] = {
                'true': y_test,
                'predicted': y_pred,
                'accuracy': test_score
            }
            results['subject_probabilities'][test_subject] = y_proba
            results['best_params_per_fold'].append(search.best_params_)
            
            print(f"    Subject {test_subject}: {test_score:.3f}")
        
        return results
    
    def train_quadrant_models(self, X, subject_ids, valence_scores, arousal_scores):
        """
        Train models for all four Russell's quadrants
        """
        # Convert to quadrant labels
        quadrant_labels = self.create_russell_quadrant_labels(valence_scores, arousal_scores)
        
        print("Quadrant distribution:")
        unique, counts = np.unique(quadrant_labels, return_counts=True)
        for q, c in zip(unique, counts):
            print(f"  Quadrant {q}: {c} samples")
        
        # Train binary classifiers for each quadrant
        quadrant_names = {1: "Happy", 2: "Angry", 3: "Sad", 4: "Relaxed"}
        
        for quadrant in [1, 2, 3, 4]:
            print(f"\nTraining Quadrant {quadrant} ({quadrant_names[quadrant]}) Model")
            
            # Create binary labels
            binary_labels = self.create_binary_labels(quadrant_labels, quadrant)
            
            # Check class balance
            pos_samples = np.sum(binary_labels)
            neg_samples = len(binary_labels) - pos_samples
            print(f"  Class balance: {pos_samples} positive, {neg_samples} negative")
            
            if pos_samples < 5 or neg_samples < 5:
                print(f"  Skipping quadrant {quadrant} - insufficient samples")
                continue
            
            # LOSO validation
            results = self.loso_validation(X, binary_labels, subject_ids, 
                                         f"Quadrant_{quadrant}")
            
            # Store results
            self.results[f'quadrant_{quadrant}'] = results
            
            mean_acc = np.mean(results['test_scores'])
            std_acc = np.std(results['test_scores'])
            print(f"  Mean Accuracy: {mean_acc:.3f} ± {std_acc:.3f}")
    
    def train_stimulus_baseline_classifier(self, stimulus_data, baseline_data, subject_ids):
        """
        Train binary classifier to distinguish stimulus from baseline
        """
        print("\nTraining Stimulus vs Baseline Classifier")
        
        # Combine data
        n_stimulus = len(stimulus_data)
        n_baseline = len(baseline_data)
        
        # Match sizes if different
        min_size = min(n_stimulus, n_baseline)
        stimulus_data = stimulus_data[:min_size]
        baseline_data = baseline_data[:min_size]
        subject_ids = subject_ids[:min_size]
        
        X = np.concatenate([stimulus_data, baseline_data], axis=0)
        y = np.concatenate([np.ones(min_size), np.zeros(min_size)])
        extended_subject_ids = np.concatenate([subject_ids, subject_ids])
        
        print(f"  Using {min_size} samples each for stimulus and baseline")
        
        # LOSO validation
        results = self.loso_validation(X, y, extended_subject_ids, "Stimulus_vs_Baseline")
        
        # Store results
        self.results['stimulus_baseline'] = results
        
        mean_acc = np.mean(results['test_scores'])
        std_acc = np.std(results['test_scores'])
        print(f"  Mean Accuracy: {mean_acc:.3f} ± {std_acc:.3f}")
        
        return results
    
    def evaluate_participant_reliability(self, subject_ids, valence_scores, arousal_scores):
        """
        Evaluate participant reliability based on STD of self-assessment scores
        """
        reliability_analysis = {}
        unique_subjects = np.unique(subject_ids)
        
        for subject in unique_subjects:
            subject_mask = subject_ids == subject
            
            if np.sum(subject_mask) < 2:
                continue
                
            # Calculate STD for each dimension
            valence_std = np.std(valence_scores[subject_mask])
            arousal_std = np.std(arousal_scores[subject_mask])
            
            # Get average probability scores if available
            avg_prob = 0.5
            if 'quadrant_1' in self.results and subject in self.results['quadrant_1']['subject_probabilities']:
                probs = []
                for q in [1, 2, 3, 4]:
                    if f'quadrant_{q}' in self.results and subject in self.results[f'quadrant_{q}']['subject_probabilities']:
                        prob_matrix = self.results[f'quadrant_{q}']['subject_probabilities'][subject]
                        avg_prob_q = np.mean(np.max(prob_matrix, axis=1))
                        probs.append(avg_prob_q)
                if probs:
                    avg_prob = np.mean(probs)
            
            # Calculate reliability thresholds
            all_valence_stds = [np.std(valence_scores[subject_ids == s]) 
                              for s in unique_subjects if np.sum(subject_ids == s) >= 2]
            all_arousal_stds = [np.std(arousal_scores[subject_ids == s]) 
                              for s in unique_subjects if np.sum(subject_ids == s) >= 2]
            
            valence_threshold = np.percentile(all_valence_stds, 25) if all_valence_stds else 0
            arousal_threshold = np.percentile(all_arousal_stds, 25) if all_arousal_stds else 0
            
            reliability_analysis[subject] = {
                'valence_std': valence_std,
                'arousal_std': arousal_std,
                'avg_probability': avg_prob,
                'reliable': valence_std > valence_threshold and arousal_std > arousal_threshold
            }
        
        return reliability_analysis
    
    def generate_classification_report(self):
        """
        Generate comprehensive classification report
        """
        report = {}
        
        for model_name, results in self.results.items():
            if not results['test_scores']:
                continue
                
            report[model_name] = {
                'mean_accuracy': np.mean(results['test_scores']),
                'std_accuracy': np.std(results['test_scores']),
                'accuracy_range': [np.min(results['test_scores']), np.max(results['test_scores'])],
                'n_subjects': len(results['subject_predictions'])
            }
        
        return report
    
    def print_results_summary(self):
        """
        Print comprehensive results summary
        """
        print("\n" + "="*60)
        print("NEUROSENSE EMOTION RECOGNITION RESULTS")
        print("="*60)
        
        for model_name, results in self.results.items():
            if not results['test_scores']:
                continue
                
            print(f"\n{model_name.upper().replace('_', ' ')}:")
            mean_acc = np.mean(results['test_scores'])
            std_acc = np.std(results['test_scores'])
            min_acc = np.min(results['test_scores'])
            max_acc = np.max(results['test_scores'])
            
            print(f"  Mean Accuracy: {mean_acc:.3f} ± {std_acc:.3f}")
            print(f"  Range: [{min_acc:.3f}, {max_acc:.3f}]")
            print(f"  Subjects: {len(results['subject_predictions'])}")


def run_neurosense_ml_analysis(dataset, segment_length=10.0):
    """
    Run complete NeuroSense ML analysis
    """
    from neurosense_preprocessor import NeuroSensePreprocessor
    
    print("="*60)
    print("NEUROSENSE ML ANALYSIS")
    print("="*60)
    
    # Initialize components
    preprocessor = NeuroSensePreprocessor()
    ml_model = NeuroSenseMLModel(random_state=42)
    
    print(f"\nPreprocessing with {segment_length}s segments...")
    
    # Preprocess data
    processed_data = preprocessor.preprocess_pipeline_optimized(
        dataset['eeg_data'],
        events=dataset['events'],
        event_id=dataset['event_id'],
        baseline_events=dataset['baseline_events'],
        segment_length=segment_length,
        subepoch_length=5.0
    )
    
    print("Processed data shapes:")
    print(f"  Stimulus: {processed_data['stimulus_data'].shape}")
    if processed_data['baseline_data'] is not None:
        print(f"  Baseline: {processed_data['baseline_data'].shape}")
    
    # Prepare data for ML
    X_stimulus = ml_model.prepare_time_series_data(processed_data['stimulus_data'])
    
    # Extend subject metadata to match processed samples
    n_processed = X_stimulus.shape[0]
    n_original = len(dataset['subject_ids'])
    
    if n_processed != n_original:
        # Calculate how many sub-epochs per trial
        sub_epochs_per_trial = n_processed // n_original
        print(f"Sub-epochs per trial: {sub_epochs_per_trial}")
        
        # Extend metadata
        extended_subject_ids = np.repeat(dataset['subject_ids'], sub_epochs_per_trial)
        extended_valence = np.repeat(dataset['valence_scores'], sub_epochs_per_trial)
        extended_arousal = np.repeat(dataset['arousal_scores'], sub_epochs_per_trial)
        
        # Trim to exact match
        extended_subject_ids = extended_subject_ids[:n_processed]
        extended_valence = extended_valence[:n_processed]
        extended_arousal = extended_arousal[:n_processed]
    else:
        extended_subject_ids = dataset['subject_ids']
        extended_valence = dataset['valence_scores']
        extended_arousal = dataset['arousal_scores']
    
    print(f"Final data shapes: X={X_stimulus.shape}, subjects={len(extended_subject_ids)}")
    
    # Train emotion recognition models
    print("\nTraining Russell's Quadrant Models...")
    ml_model.train_quadrant_models(
        X_stimulus,
        extended_subject_ids,
        extended_valence,
        extended_arousal
    )
    
    # Train stimulus vs baseline classifier
    if processed_data['baseline_data'] is not None:
        X_baseline = ml_model.prepare_time_series_data(processed_data['baseline_data'])
        min_samples = min(len(X_stimulus), len(X_baseline))
        
        ml_model.train_stimulus_baseline_classifier(
            X_stimulus[:min_samples],
            X_baseline[:min_samples],
            extended_subject_ids[:min_samples]
        )
    
    # Generate results
    print("\nGenerating Results...")
    report = ml_model.generate_classification_report()
    ml_model.print_results_summary()
    
    # Participant reliability analysis
    reliability = ml_model.evaluate_participant_reliability(
        extended_subject_ids, extended_valence, extended_arousal
    )
    
    reliable_count = sum(1 for r in reliability.values() if r['reliable'])
    print(f"\nParticipant Reliability: {reliable_count}/{len(reliability)} reliable")
    
    return {
        'ml_model': ml_model,
        'results': ml_model.results,
        'reliability': reliability,
        'report': report,
        'processed_data': processed_data
    }