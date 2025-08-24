# Biometric Monitor

A real-time biometric monitoring system that combines facial emotion recognition and EEG analysis with OSC messaging and web-based monitoring.

## Project Structure

```
biometric-monitor/
├── pyproject.toml
├── README.md
├── biometric_monitor/
│   ├── __init__.py
│   ├── main.py                 # Main entry point
│   ├── config.py               # Configuration management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py             # Base model interface
│   │   ├── emotion_models.py   # Emotion recognition models
│   │   └── eeg_models.py       # EEG analysis models
│   ├── pipelines/
│   │   ├── __init__.py
│   │   ├── base.py             # Base pipeline interface
│   │   ├── emotion_pipeline.py # Emotion recognition pipeline
│   │   └── eeg_pipeline.py     # EEG processing pipeline
│   ├── communication/
│   │   ├── __init__.py
│   │   └── osc_client.py       # OSC messaging
│   ├── web/
│   │   ├── __init__.py
│   │   ├── app.py              # Flask application
│   │   ├── routes.py           # API routes
│   │   └── templates/
│   │       └── dashboard.html  # Web dashboard
│   └── utils/
│       ├── __init__.py
│       ├── image_processing.py
│       └── data_processing.py
├── models/                     # Pre-trained model files
│   ├── FER_static_ResNet50_AffectNet.pt
│   └── FER_dinamic_LSTM_Aff-Wild2.pt
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_pipelines.py
    └── test_communication.py
```

## Installation

```bash
# Create and activate virtual environment with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e .

# For development
uv pip install -e ".[dev]"
```

## Usage

### Start the monitoring system

```bash
biometric-monitor --emotion --eeg --web-port 5001 --osc-port 8000
```

### Command line options

- `--emotion`: Enable emotion recognition
- `--eeg`: Enable EEG monitoring
- `--web-port`: Flask web server port (default: 5001)
- `--osc-port`: OSC output port (default: 8000)
- `--osc-host`: OSC host (default: 127.0.0.1)
- `--camera-id`: Camera device ID (default: 0)
- `--sadness-boost`: Emotion bias factor for sadness (default: 2.0)

### Web Interface

Navigate to `http://localhost:5001` to access the real-time dashboard.

## Architecture

### Models

- **Emotion Recognition**: ResNet50 backbone with LSTM for temporal modeling
- **EEG Analysis**: Extensible framework for EEG signal processing

### Pipelines

- **Emotion Pipeline**: Real-time facial emotion recognition with VAD output
- **EEG Pipeline**: Real-time EEG data processing and segmentation

### Communication

- **OSC Client**: Sends VAD (Valence-Arousal-Dominance) data to external applications
- **WebSocket**: Real-time data streaming to web interface

### Web Interface

- Real-time visualization of biometric data
- Control panel for starting/stopping data streams
- Statistics and logging dashboard
