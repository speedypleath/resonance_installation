#!/usr/bin/env python3
"""
Muse 2 EEG Real-Time Web Streaming Application
Streams EEG data segments to a web interface using Flask and WebSockets
"""

import numpy as np
import time
import json
from collections import deque
from pylsl import StreamInlet, resolve_bypred
import threading
from datetime import datetime, timezone
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import base64
import io
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import logging

# Suppress Flask development server warnings
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class MuseEEGWebStreamer:
    def __init__(self, fragment_duration=10.0, window_step=5.0, segment_duration=2.0, segment_overlap=0.5):
        """
        Initialize the EEG web streamer
        
        Args:
            fragment_duration (float): Duration of each data fragment in seconds
            window_step (float): Step size for sliding window in seconds
            segment_duration (float): Duration of each segment in seconds
            segment_overlap (float): Overlap between segments (0-1)
        """
        self.fragment_duration = fragment_duration
        self.window_step = window_step
        self.segment_duration = segment_duration
        self.segment_overlap = segment_overlap
        
        self.sampling_rate = 256  # Muse 2 default sampling rate
        self.n_channels = 4  # Muse 2 has 4 EEG channels
        self.channel_names = ['TP9', 'AF7', 'AF8', 'TP10']
        
        # Calculate buffer sizes
        self.fragment_samples = int(self.fragment_duration * self.sampling_rate)
        self.window_step_samples = int(self.window_step * self.sampling_rate)
        self.segment_samples = int(self.segment_duration * self.sampling_rate)
        
        # Data storage
        self.data_buffer = deque(maxlen=self.fragment_samples * 2)
        self.timestamps = deque(maxlen=self.fragment_samples * 2)
        self.fragments = []
        self.current_segments = []
        
        # Stream variables
        self.inlet = None
        self.is_streaming = False
        self.stream_thread = None
        self.data_lock = threading.Lock()
        
        # Statistics
        self.fragment_count = 0
        self.segment_count = 0
        self.last_fragment_time = None
        self.start_time = None
        
        # Flask app and SocketIO
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'eeg_streamer_secret'
        self.socketio = SocketIO(self.app, cors_allowed_origins="*", async_mode='threading')
        
        self.setup_routes()
        
    def setup_routes(self):
        """Set up Flask routes and SocketIO events"""
        
        @self.app.route('/')
        def index():
            return render_template('eeg_dashboard.html')
        
        @self.app.route('/api/status')
        def get_status():
            with self.data_lock:
                return jsonify({
                    'is_streaming': self.is_streaming,
                    'fragment_count': self.fragment_count,
                    'segment_count': self.segment_count,
                    'buffer_size': len(self.data_buffer),
                    'sampling_rate': self.sampling_rate,
                    'channels': self.n_channels,
                    'channel_names': self.channel_names,
                    'fragment_duration': self.fragment_duration,
                    'segment_duration': self.segment_duration,
                    'uptime': time.time() - self.start_time if self.start_time else 0
                })
        
        @self.app.route('/api/latest_fragment')
        def get_latest_fragment():
            with self.data_lock:
                if self.fragments:
                    fragment = self.fragments[-1]
                    return jsonify({
                        'fragment_id': fragment['fragment_id'],
                        'duration': fragment['duration'],
                        'shape': fragment['data'].shape,
                        'timestamp': str(fragment['created_at'].isoformat())
                    })
                return jsonify({'error': 'No fragments available'})
        
        @self.socketio.on('connect')
        def handle_connect():
            print(f"Client connected: {threading.current_thread().ident}")
            emit('status', {'message': 'Connected to EEG streamer'})
        
        @self.socketio.on('disconnect')
        def handle_disconnect(**kwargs):
            print(f"Client disconnected: {threading.current_thread().ident}")
        
        @self.socketio.on('request_start_stream')
        def handle_start_stream():
            if self.find_muse_stream():
                if self.start_streaming():
                    emit('stream_status', {'status': 'started', 'message': 'EEG streaming started'})
                else:
                    emit('stream_status', {'status': 'error', 'message': 'Failed to start streaming'})
            else:
                emit('stream_status', {'status': 'error', 'message': 'Could not find Muse stream'})
        
        @self.socketio.on('request_stop_stream')
        def handle_stop_stream():
            self.stop_streaming()
            emit('stream_status', {'status': 'stopped', 'message': 'EEG streaming stopped'})
    
    def find_muse_stream(self, timeout=10):
        """Find and connect to Muse EEG stream"""
        print("Looking for Muse EEG stream...")
        
        try:
            # Look for EEG streams
            streams = resolve_bypred('type', 'EEG', timeout=timeout)
            
            if not streams:
                print("No EEG streams found! Trying any LSL streams...")
                all_streams = resolve_bypred(timeout=timeout)
                if all_streams:
                    print(f"Found {len(all_streams)} streams:")
                    for i, stream in enumerate(all_streams):
                        print(f"  {i+1}. {stream.name()} - Type: {stream.type()} - Channels: {stream.channel_count()}")
                    
                    muse_streams = [s for s in all_streams if 'muse' in s.name().lower() or s.channel_count() == 4]
                    if muse_streams:
                        streams = [muse_streams[0]]
                        print(f"Using Muse-like stream: {streams[0].name()}")
                    else:
                        return False
                else:
                    return False
            
            stream_info = streams[0]
            print(f"Found EEG stream: {stream_info.name()}")
            print(f"Sampling rate: {stream_info.nominal_srate()} Hz")
            print(f"Channels: {stream_info.channel_count()}")
            
            # Create inlet
            self.inlet = StreamInlet(stream_info, max_buflen=360, max_chunklen=12)
            self.sampling_rate = int(stream_info.nominal_srate())
            self.n_channels = stream_info.channel_count()
            
            # Update channel names and buffer sizes
            if self.n_channels != len(self.channel_names):
                self.channel_names = [f'Ch{i+1}' for i in range(self.n_channels)]
            
            self.fragment_samples = int(self.fragment_duration * self.sampling_rate)
            self.window_step_samples = int(self.window_step * self.sampling_rate)
            self.segment_samples = int(self.segment_duration * self.sampling_rate)
            
            return True
            
        except Exception as e:
            print(f"Error connecting to stream: {e}")
            return False
    
    def start_streaming(self):
        """Start streaming data from Muse headset"""
        if not self.inlet:
            return False
        
        if self.is_streaming:
            return True
        
        self.is_streaming = True
        self.start_time = time.time()
        self.stream_thread = threading.Thread(target=self._stream_data)
        self.stream_thread.daemon = True
        self.stream_thread.start()
        
        print("EEG streaming started!")
        return True
    
    def stop_streaming(self):
        """Stop streaming data"""
        self.is_streaming = False
        if self.stream_thread:
            self.stream_thread.join(timeout=2)
        print("EEG streaming stopped!")
    
    def _stream_data(self):
        """Continuously stream data and process fragments"""
        print("Starting data collection...")
        
        while self.is_streaming and self.inlet:
            try:
                samples, timestamps = self.inlet.pull_chunk(timeout=1.0, max_samples=32)
                
                if samples:
                    with self.data_lock:
                        for sample, timestamp in zip(samples, timestamps):
                            self.data_buffer.append(sample)
                            self.timestamps.append(timestamp)
                        
                        self._check_for_new_fragment()
                        
            except Exception as e:
                print(f"Error in data streaming: {e}")
                break
    
    def _check_for_new_fragment(self):
        """Check if we can create a new fragment and segments"""
        if len(self.data_buffer) >= self.fragment_samples:
            current_time = time.time()
            
            if (self.last_fragment_time is None or 
                current_time - self.last_fragment_time >= self.window_step):
                
                # Create fragment
                fragment_data = np.array(list(self.data_buffer)[-self.fragment_samples:])
                fragment_timestamps = np.array(list(self.timestamps)[-self.fragment_samples:])
                
                fragment = {
                    'data': fragment_data,
                    'timestamps': fragment_timestamps,
                    'fragment_id': self.fragment_count,
                    'start_time': fragment_timestamps[0],
                    'end_time': fragment_timestamps[-1],
                    'duration': fragment_timestamps[-1] - fragment_timestamps[0],
                    'created_at': datetime.now(timezone.utc)
                }
                
                # Store fragment
                self.fragments.append(fragment)
                self.fragment_count += 1
                self.last_fragment_time = current_time
                
                # Create segments from fragment
                segments = self._create_segments_from_fragment(fragment)
                self.current_segments = segments
                
                print(f"Fragment {self.fragment_count} created with {len(segments)} segments")
                
                # Emit to web clients
                self._emit_fragment_and_segments(fragment, segments)
                
                # Keep memory usage reasonable
                if len(self.fragments) > 50:
                    self.fragments.pop(0)
    
    def _create_segments_from_fragment(self, fragment):
        """Create segments from a fragment"""
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
                'data': data[start_idx:end_idx].tolist(),  # Convert to list for JSON
                'time': time_axis[start_idx:end_idx].tolist(),
                'timestamps': timestamps[start_idx:end_idx].tolist(),
                'start_time': float(time_axis[start_idx]),
                'end_time': float(time_axis[end_idx-1]),
                'duration': float(time_axis[end_idx-1] - time_axis[start_idx]),
                'created_at': datetime.now(timezone.utc).isoformat()
            }
            
            segments.append(segment)
            segment_id += 1
            self.segment_count += 1
        
        return segments
    
    def _emit_fragment_and_segments(self, fragment, segments):
        """Emit fragment and segments to web clients"""
        try:
            # Prepare fragment data for web
            fragment_data = {
                'fragment_id': fragment['fragment_id'],
                'duration': float(fragment['duration']),
                'data': fragment['data'].tolist(),
                'time': (fragment['timestamps'] - fragment['timestamps'][0]).tolist(),
                'channel_names': self.channel_names,
                'sampling_rate': self.sampling_rate,
                'created_at': fragment['created_at'].isoformat()
            }
            
            # Emit fragment
            self.socketio.emit('new_fragment', fragment_data)
            
            # Emit segments
            self.socketio.emit('new_segments', {
                'fragment_id': fragment['fragment_id'],
                'segments': segments,
                'channel_names': self.channel_names
            })
            
            # Emit statistics
            self.socketio.emit('statistics', {
                'fragment_count': self.fragment_count,
                'segment_count': self.segment_count,
                'buffer_size': len(self.data_buffer),
                'uptime': time.time() - self.start_time if self.start_time else 0
            })
            
        except Exception as e:
            print(f"Error emitting data: {e}")
    
    def generate_segment_plot(self, segment):
        """Generate a plot for a segment and return as base64 string"""
        try:
            fig, axes = plt.subplots(self.n_channels, 1, figsize=(10, 8))
            if self.n_channels == 1:
                axes = [axes]
            
            data = np.array(segment['data'])
            time_axis = np.array(segment['time'])
            
            for i, ax in enumerate(axes):
                if i < self.n_channels:
                    ax.plot(time_axis, data[:, i], linewidth=1)
                    ax.set_title(f'{self.channel_names[i]} - Segment {segment["segment_id"]+1}')
                    ax.set_ylabel('Amplitude (μV)')
                    ax.grid(True, alpha=0.3)
            
            axes[-1].set_xlabel('Time (s)')
            plt.tight_layout()
            
            # Save plot to base64 string
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            plot_data = base64.b64encode(buffer.getvalue()).decode()
            plt.close(fig)
            
            return plot_data
        
        except Exception as e:
            print(f"Error generating plot: {e}")
            return None
    
    def run_web_app(self, host='127.0.0.1', port=5001, debug=False):
        """Run the web application"""
        print(f"Starting EEG Web Streamer on http://{host}:{port}")
        print("Open your browser and navigate to the URL above")
        
        # Create templates directory and HTML file
        import os
        template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
        os.makedirs(template_dir, exist_ok=True)
        
        html_content = self.get_html_template()
        with open(os.path.join(template_dir, 'eeg_dashboard.html'), 'w') as f:
            f.write(html_content)
        
        self.socketio.run(self.app, host=host, port=port, debug=debug)
    
    def get_html_template(self):
        """Return the HTML template for the web interface"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Muse 2 EEG Real-Time Dashboard</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            min-height: 100vh;
        }
        .header { 
            background: rgba(255,255,255,0.1); 
            padding: 20px; 
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }
        .header h1 { 
            text-align: center; 
            font-size: 2.5rem; 
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        .controls { 
            text-align: center; 
            margin-top: 15px; 
        }
        .btn { 
            background: rgba(255,255,255,0.2); 
            border: 1px solid rgba(255,255,255,0.3); 
            color: white; 
            padding: 12px 24px; 
            margin: 5px; 
            border-radius: 25px; 
            cursor: pointer; 
            font-size: 1rem;
            backdrop-filter: blur(5px);
            transition: all 0.3s ease;
        }
        .btn:hover { 
            background: rgba(255,255,255,0.3); 
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        .btn:disabled { 
            opacity: 0.5; 
            cursor: not-allowed; 
        }
        .status { 
            text-align: center; 
            margin: 20px; 
            padding: 15px; 
            background: rgba(255,255,255,0.1); 
            border-radius: 10px;
            backdrop-filter: blur(5px);
        }
        .stats { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 15px; 
            margin: 20px; 
        }
        .stat-card { 
            background: rgba(255,255,255,0.1); 
            padding: 20px; 
            border-radius: 15px; 
            text-align: center;
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        .stat-card h3 { 
            font-size: 2rem; 
            margin-bottom: 5px; 
            color: #FFD700;
        }
        .plot-container { 
            margin: 20px; 
            padding: 20px; 
            background: rgba(255,255,255,0.1); 
            border-radius: 15px;
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        .plot-container h2 { 
            margin-bottom: 15px; 
            text-align: center;
            color: #FFD700;
        }
        .segments-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); 
            gap: 20px; 
            margin-top: 20px; 
        }
        .segment-plot { 
            background: rgba(255,255,255,0.05); 
            border-radius: 10px; 
            padding: 15px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .segment-plot h3 { 
            text-align: center; 
            margin-bottom: 10px;
            color: #FFD700;
        }
        #connectionStatus { 
            display: inline-block; 
            width: 12px; 
            height: 12px; 
            border-radius: 50%; 
            margin-right: 8px; 
        }
        .connected { background-color: #4CAF50; }
        .disconnected { background-color: #f44336; }
        .log-container {
            margin: 20px;
            padding: 15px;
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            font-family: monospace;
            max-height: 200px;
            overflow-y: auto;
        }
        .log-entry {
            margin: 5px 0;
            padding: 5px;
            border-left: 3px solid #FFD700;
            padding-left: 10px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 Muse 2 EEG Real-Time Dashboard</h1>
        <div class="status">
            <span id="connectionStatus" class="disconnected"></span>
            <span id="statusText">Connecting...</span>
        </div>
        <div class="controls">
            <button class="btn" id="startBtn" onclick="startStreaming()">Start Streaming</button>
            <button class="btn" id="stopBtn" onclick="stopStreaming()" disabled>Stop Streaming</button>
            <button class="btn" onclick="clearLogs()">Clear Logs</button>
        </div>
    </div>

    <div class="stats">
        <div class="stat-card">
            <h3 id="fragmentCount">0</h3>
            <p>Fragments</p>
        </div>
        <div class="stat-card">
            <h3 id="segmentCount">0</h3>
            <p>Segments</p>
        </div>
        <div class="stat-card">
            <h3 id="bufferSize">0</h3>
            <p>Buffer Size</p>
        </div>
        <div class="stat-card">
            <h3 id="uptime">0</h3>
            <p>Uptime (s)</p>
        </div>
    </div>

    <div class="plot-container">
        <h2>📈 Live Fragment (10s window)</h2>
        <div id="fragmentPlot"></div>
    </div>

    <div class="plot-container">
        <h2>🔬 Real-Time Segments (2s windows)</h2>
        <div class="segments-grid" id="segmentsContainer"></div>
    </div>

    <div class="plot-container">
        <h2>📋 Activity Log</h2>
        <div class="log-container" id="logContainer"></div>
    </div>

    <script>
        const socket = io();
        let fragmentPlotData = {};
        let segmentPlots = {};

        // Connection status
        socket.on('connect', function() {
            document.getElementById('connectionStatus').className = 'connected';
            document.getElementById('statusText').textContent = 'Connected to server';
            addLog('Connected to EEG streamer');
        });

        socket.on('disconnect', function() {
            document.getElementById('connectionStatus').className = 'disconnected';
            document.getElementById('statusText').textContent = 'Disconnected from server';
            addLog('Disconnected from server');
        });

        // Stream control
        function startStreaming() {
            socket.emit('request_start_stream');
            document.getElementById('startBtn').disabled = true;
            document.getElementById('stopBtn').disabled = false;
        }

        function stopStreaming() {
            socket.emit('request_stop_stream');
            document.getElementById('startBtn').disabled = false;
            document.getElementById('stopBtn').disabled = true;
        }

        // Logging
        function addLog(message) {
            const logContainer = document.getElementById('logContainer');
            const logEntry = document.createElement('div');
            logEntry.className = 'log-entry';
            logEntry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
            logContainer.appendChild(logEntry);
            logContainer.scrollTop = logContainer.scrollHeight;
        }

        function clearLogs() {
            document.getElementById('logContainer').innerHTML = '';
        }

        // Socket event handlers
        socket.on('stream_status', function(data) {
            addLog(`Stream ${data.status}: ${data.message}`);
            document.getElementById('statusText').textContent = data.message;
        });

        socket.on('statistics', function(data) {
            document.getElementById('fragmentCount').textContent = data.fragment_count;
            document.getElementById('segmentCount').textContent = data.segment_count;
            document.getElementById('bufferSize').textContent = data.buffer_size;
            document.getElementById('uptime').textContent = Math.round(data.uptime);
        });

        socket.on('new_fragment', function(data) {
            addLog(`New fragment ${data.fragment_id} (${data.duration.toFixed(2)}s)`);
            updateFragmentPlot(data);
        });

        socket.on('new_segments', function(data) {
            addLog(`${data.segments.length} new segments from fragment ${data.fragment_id}`);
            updateSegmentPlots(data);
        });

        function updateFragmentPlot(fragmentData) {
            const traces = [];
            
            for (let ch = 0; ch < fragmentData.channel_names.length; ch++) {
                const channelData = fragmentData.data.map(sample => sample[ch]);
                
                traces.push({
                    x: fragmentData.time,
                    y: channelData,
                    type: 'scatter',
                    mode: 'lines',
                    name: fragmentData.channel_names[ch],
                    line: { width: 2 }
                });
            }

            const layout = {
                title: `Fragment ${fragmentData.fragment_id} - ${fragmentData.duration.toFixed(2)}s`,
                xaxis: { title: 'Time (s)' },
                yaxis: { title: 'Amplitude (μV)' },
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(255,255,255,0.1)',
                font: { color: 'white' }
            };

            Plotly.newPlot('fragmentPlot', traces, layout);
        }

        function updateSegmentPlots(segmentData) {
            const container = document.getElementById('segmentsContainer');
            container.innerHTML = ''; // Clear existing plots

            segmentData.segments.forEach((segment, index) => {
                const segmentDiv = document.createElement('div');
                segmentDiv.className = 'segment-plot';
                segmentDiv.innerHTML = `<h3>Segment ${segment.segment_id + 1}</h3><div id="segment_${index}"></div>`;
                container.appendChild(segmentDiv);

                const traces = [];
                
                for (let ch = 0; ch < segmentData.channel_names.length; ch++) {
                    const channelData = segment.data.map(sample => sample[ch]);
                    
                    traces.push({
                        x: segment.time,
                        y: channelData,
                        type: 'scatter',
                        mode: 'lines',
                        name: segmentData.channel_names[ch],
                        line: { width: 1.5 }
                    });
                }

                const layout = {
                    title: `${segment.duration.toFixed(2)}s (${segment.start_time.toFixed(1)}s - ${segment.end_time.toFixed(1)}s)`,
                    xaxis: { title: 'Time (s)' },
                    yaxis: { title: 'μV' },
                    paper_bgcolor: 'rgba(0,0,0,0)',
                    plot_bgcolor: 'rgba(255,255,255,0.1)',
                    font: { color: 'white' },
                    margin: { t: 40, b: 40, l: 50, r: 20 },
                    height: 300
                };

                Plotly.newPlot(`segment_${index}`, traces, layout);
            });
        }

        // Initial setup
        addLog('EEG Dashboard loaded - Ready to start streaming');
    </script>
</body>
</html>'''

def main():
    """Main function to run the EEG web streamer"""
    print("🧠 Muse 2 EEG Real-Time Web Streamer")
    print("=" * 50)
    
    # Create streamer with custom parameters
    streamer = MuseEEGWebStreamer(
        fragment_duration=10.0,    # 10-second fragments
        window_step=5.0,          # 5-second sliding window
        segment_duration=2.0,      # 2-second segments
        segment_overlap=0.5        # 50% overlap between segments
    )
    
    print("Web streamer initialized with:")
    print(f"  - Fragment duration: {streamer.fragment_duration}s")
    print(f"  - Window step: {streamer.window_step}s") 
    print(f"  - Segment duration: {streamer.segment_duration}s")
    print(f"  - Segment overlap: {streamer.segment_overlap*100}%")
    print()
    
    try:
        # Run the web application
        streamer.run_web_app(host='127.0.0.1', port=5001, debug=False)
    except KeyboardInterrupt:
        print("\nShutting down...")
        streamer.stop_streaming()
    except Exception as e:
        print(f"Error running web app: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()