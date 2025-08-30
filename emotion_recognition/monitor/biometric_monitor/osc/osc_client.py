import time
import math
import argparse
import random
import threading
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

# Global variables
vad_state = None
osc_client = None

# Singleton instance for pipeline integration
_osc_client_instance = None

class SmoothedVADState:
    def __init__(self, 
                 tau_eeg=0.5, tau_facial=0.5, tau_gsr=2.0,
                 weight_eeg=0.3, weight_facial=0.5, weight_gsr=0.2):

        self.vad_eeg = {'valence': 0.0, 'arousal': 0.0, 'dominance': 0.0}
        self.vad_facial = {'valence': 0.0, 'arousal': 0.0, 'dominance': 0.0}
        self.vad_gsr = {'valence': 0.0, 'arousal': 0.0, 'dominance': 0.0}

        self.last_update = {'eeg': None, 'facial': None, 'gsr': None}

        # Time constants
        self.tau_eeg = tau_eeg
        self.tau_facial = tau_facial
        self.tau_gsr = tau_gsr

        # Weights
        self.weight_eeg = weight_eeg
        self.weight_facial = weight_facial
        self.weight_gsr = weight_gsr

        # Final combined state
        self.valence = 0.0
        self.arousal = 0.0
        self.dominance = 0.0

    def _calculate_alpha(self, tau, dt):
        """Exponential smoothing factor based on time constant and sample interval"""
        return 1 - math.exp(-dt / tau)

    def _update_vad(self, state_dict, new_vad, tau, last_time_key):
        now = time.time()
        last_time = self.last_update[last_time_key]
        if last_time is None:
            dt = tau  # First sample = assume tau
        else:
            dt = now - last_time

        alpha = self._calculate_alpha(tau, dt)

        state_dict['valence'] = max(0.0, min(1.0, alpha * new_vad[0] + (1 - alpha) * state_dict['valence']))
        state_dict['arousal'] = max(0.0, min(1.0, alpha * new_vad[1] + (1 - alpha) * state_dict['arousal']))
        state_dict['dominance'] = max(0.0, min(1.0, alpha * new_vad[2] + (1 - alpha) * state_dict['dominance']))

        self.last_update[last_time_key] = now
        self._recalculate_combination()

    def update_eeg(self, vad):       
        self._update_vad(self.vad_eeg, vad, self.tau_eeg, 'eeg')
    
    def update_facial(self, vad):    
        self._update_vad(self.vad_facial, vad, self.tau_facial, 'facial')
    
    def update_gsr(self, vad):       
        self._update_vad(self.vad_gsr, vad, self.tau_gsr, 'gsr')

    def _recalculate_combination(self):
        total_weight = self.weight_eeg + self.weight_facial + self.weight_gsr
        if total_weight == 0:
            return
        
        # Fixed: Include GSR in valence calculation and fix weight_eeg reference
        self.valence = max(0.0, min(1.0, (
            self.vad_eeg['valence'] * self.weight_eeg +
            self.vad_facial['valence'] * self.weight_facial +
            self.vad_gsr['valence'] * self.weight_gsr
        ) / total_weight))
        
        self.arousal = max(0.0, min(1.0, (
            self.vad_eeg['arousal'] * self.weight_eeg +
            self.vad_facial['arousal'] * self.weight_facial +
            self.vad_gsr['arousal'] * self.weight_gsr
        ) / total_weight))
        
        self.dominance = max(0.0, min(1.0, (
            self.vad_eeg['dominance'] * self.weight_eeg +
            self.vad_facial['dominance'] * self.weight_facial +
            self.vad_gsr['dominance'] * self.weight_gsr
        ) / total_weight))

    def get_vad(self):
        """Final combined VAD"""
        return self.valence, self.arousal, self.dominance
    
    def get_status(self):
        """Get status of each sensor"""
        return {
            'eeg': self.vad_eeg['valence'] > 0.5,
            'facial': self.vad_facial['valence'] > 0.5,
            'gsr': self.vad_gsr['valence'] > 0.5
        }

def print_message(address: str, *args):
    """Handle incoming OSC messages"""
    global vad_state
    
    if address == "/eeg":
        if len(args) >= 3:
            valence, arousal, dominance = args[0], args[1], args[2]
            vad_state.update_eeg((valence, arousal, dominance))
            print(f"EEG VAD: V={valence:.3f}, A={arousal:.3f}, D={dominance:.3f}")
            print_combined_state()
    
    elif address == "/facial":
        if len(args) >= 3:
            valence, arousal, dominance = args[0], args[1], args[2]
            vad_state.update_facial((valence, arousal, dominance))
            print(f"Facial VAD: V={valence:.3f}, A={arousal:.3f}, D={dominance:.3f}")
            print_combined_state()

    elif address == "/gsr/prediction/8s":
        if len(args) >= 3:
            valence, arousal, dominance = args[0], args[1], args[2]
            vad_state.update_gsr((valence, arousal, dominance))
            print(f"GSR Prediction 8s: V={valence:.3f}, A={arousal:.3f}, D={dominance:.3f}")
            print_combined_state()
    
    elif address == "/gsr/prediction/20s":
        if len(args) >= 3:
            valence, arousal, dominance = args[0], args[1], args[2]
            vad_state.update_gsr((valence, arousal, dominance))
            print(f"GSR Prediction 20s: V={valence:.3f}, A={arousal:.3f}, D={dominance:.3f}")
            print_combined_state()

def print_combined_state():
    """Print the combined emotional state and send via OSC"""
    valence, arousal, dominance = vad_state.get_vad()
    status = vad_state.get_status()
    
    print(f"Combined VAD: V={valence:.3f}, A={arousal:.3f}, D={dominance:.3f}")
    print(f"Status: EEG={status['eeg']}, Facial={status['facial']}, GSR={status['gsr']}")
    print("-" * 50)
    
    # Send combined VAD via OSC if client is available
    if osc_client:
        send_combined_vad(valence, arousal, dominance)

def send_combined_vad(valence, arousal, dominance):
    """Send the combined VAD values via OSC"""
    try:
        # Send individual values
        osc_client.send_message("/valence", valence)
        osc_client.send_message("/arousal", arousal)
        osc_client.send_message("/dominance", dominance)

        # # Send as a bundle
        # osc_client.send_message("/vad/combined", [valence, arousal, dominance])
        
        # # Send status information
        # status = vad_state.get_status()
        # osc_client.send_message("/vad/status/eeg", 1 if status['eeg'] else 0)
        # osc_client.send_message("/vad/status/facial", 1 if status['facial'] else 0)
        # osc_client.send_message("/vad/status/gsr", 1 if status['gsr'] else 0)
        
        print(f"→ OSC sent: V={valence:.3f}, A={arousal:.3f}, D={dominance:.3f}")
        
    except Exception as e:
        print(f"Error sending OSC: {e}")


class OSCClient:
    """OSC client for centralized VAD processing that can be used by pipelines."""
    
    def __init__(self, output_host="127.0.0.1", output_port=5002,
                 tau_eeg=0.5, tau_facial=0.5, tau_gsr=3.0,
                 weight_eeg=0.05, weight_facial=0.6, weight_gsr=0.35):
        
        self.vad_state = SmoothedVADState(
            tau_eeg=tau_eeg,
            tau_facial=tau_facial, 
            tau_gsr=tau_gsr,
            weight_eeg=weight_eeg,
            weight_facial=weight_facial,
            weight_gsr=weight_gsr
        )
        
        # Initialize OSC client
        self.osc_client = None
        try:
            self.osc_client = udp_client.SimpleUDPClient(output_host, output_port)
            print(f"OSCClient: OSC output configured: {output_host}:{output_port}")
        except Exception as e:
            print(f"OSCClient: Could not create OSC client: {e}")
    
    def update_eeg(self, valence, arousal, dominance):
        """Update EEG VAD values."""
        self.vad_state.update_eeg((valence, arousal, dominance))
        print(f"EEG VAD: V={valence:.3f}, A={arousal:.3f}, D={dominance:.3f}")
        self._send_combined_vad()
    
    def update_facial(self, valence, arousal, dominance):
        """Update facial VAD values."""
        self.vad_state.update_facial((valence, arousal, dominance))
        print(f"Facial VAD: V={valence:.3f}, A={arousal:.3f}, D={dominance:.3f}")
        self._send_combined_vad()
    
    def update_gsr(self, valence, arousal, dominance):
        """Update GSR VAD values."""
        self.vad_state.update_gsr((valence, arousal, dominance))
        print(f"GSR VAD: V={valence:.3f}, A={arousal:.3f}, D={dominance:.3f}")
        self._send_combined_vad()

    def send_facial_label(self, label):
        """Send facial emotion label via OSC."""
        print(f"Facial Emotion Label: {label}")
        if self.osc_client:
            try:
                self.osc_client.send_message("/emotion", label)
                print(f"→ OSC sent: Facial Label={label}")
            except Exception as e:
                print(f"Error sending OSC facial label: {e}")
    
    def _send_combined_vad(self):
        """Send the combined VAD values via OSC."""
        valence, arousal, dominance = self.vad_state.get_vad()
        status = self.vad_state.get_status()
        
        print(f"Combined VAD: V={valence:.3f}, A={arousal:.3f}, D={dominance:.3f}")
        print(f"Status: EEG={status['eeg']}, Facial={status['facial']}, GSR={status['gsr']}")
        print("-" * 50)
        
        if self.osc_client:
            try:
                # Send individual values
                self.osc_client.send_message("/valence", valence)
                self.osc_client.send_message("/arousal", arousal)
                self.osc_client.send_message("/dominance", dominance)
                print(f"→ OSC sent: V={valence:.3f}, A={arousal:.3f}, D={dominance:.3f}")
            except Exception as e:
                print(f"Error sending OSC: {e}")


def get_osc_client(**kwargs):
    """Get or create singleton OSCClient instance."""
    global _osc_client_instance
    if _osc_client_instance is None:
        # Use default parameters if none provided
        default_params = {
            "output_host": "127.0.0.1",
            "output_port": 5002,
            "tau_eeg": 0.5,
            "tau_facial": 0.5, 
            "tau_gsr": 3.0,
            "weight_eeg": 0.05,
            "weight_facial": 0.6,
            "weight_gsr": 0.35
        }
        default_params.update(kwargs)
        _osc_client_instance = OSCClient(**default_params)
    return _osc_client_instance

def reset_osc_client():
    """Reset the singleton instance (useful for testing)."""
    global _osc_client_instance
    _osc_client_instance = None

def generate_mock_vad():
    """Generate realistic mock VAD values with some variation"""
    base_valence = 0.5 + 0.3 * math.sin(time.time() * 0.1)  # Slow oscillation
    base_arousal = 0.4 + 0.2 * math.sin(time.time() * 0.15)  # Different frequency
    base_dominance = 0.6 + 0.1 * math.sin(time.time() * 0.05)  # Even slower
    
    # Add some random noise
    valence = max(0, min(1, base_valence + random.gauss(0, 0.1)))
    arousal = max(0, min(1, base_arousal + random.gauss(0, 0.1)))
    dominance = max(0, min(1, base_dominance + random.gauss(0, 0.05)))
    
    return valence, arousal, dominance

def mock_sensor_thread(sensor_type, interval, stop_event):
    """Thread function to simulate sensor data"""
    while not stop_event.is_set():
        vad = generate_mock_vad()
        
        if sensor_type == "eeg":
            print_message("/eeg", *vad)
        elif sensor_type == "facial":
            print_message("/facial", *vad)
        elif sensor_type == "gsr_8s":
            print_message("/gsr/prediction/8s", *vad)
        elif sensor_type == "gsr_20s":
            print_message("/gsr/prediction/20s", *vad)
        
        stop_event.wait(interval)

def run_test_mode():
    """Run the application in test mode with mock data"""
    print("Running in TEST MODE - generating mock VAD data")
    print("=" * 50)
    
    stop_event = threading.Event()
    
    # Create threads for different sensors with different update rates
    threads = [
        threading.Thread(target=mock_sensor_thread, args=("eeg", 0.2, stop_event)),      # 5 Hz
        threading.Thread(target=mock_sensor_thread, args=("facial", 0.1, stop_event)),   # 10 Hz
        threading.Thread(target=mock_sensor_thread, args=("gsr_8s", 8.0, stop_event)),   # Every 8 seconds
        threading.Thread(target=mock_sensor_thread, args=("gsr_20s", 20.0, stop_event)), # Every 20 seconds
    ]
    
    # Start all threads
    for thread in threads:
        thread.daemon = True
        thread.start()
    
    try:
        print("Mock sensors running. Press Ctrl+C to stop")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping test mode...")
        stop_event.set()
        
        # Wait for threads to finish
        for thread in threads:
            thread.join(timeout=1)
        
        print("Test mode stopped.")

def main():
    """Main function to run the OSC receiver"""
    global vad_state, osc_client
    
    parser = argparse.ArgumentParser(description="Smooth VAD State Receiver")
    parser.add_argument("--host", default="192.168.0.141", help="Host to bind to for incoming messages")
    parser.add_argument("--port", type=int, default=5001, help="Port to bind to for incoming messages")
    parser.add_argument("--output-host", default="127.0.0.1", help="Host to send combined VAD to")
    parser.add_argument("--output-port", type=int, default=5002, help="Port to send combined VAD to")
    parser.add_argument("--test", action="store_true", help="Run in test mode with mock data")
    parser.add_argument("--no-osc-output", action="store_true", help="Disable OSC output (print only)")
    
    args = parser.parse_args()
    
    # Initialize VAD state
    vad_state = SmoothedVADState(
        tau_eeg=0.5,    # ~0.5 seconds smoothing for EEG
        tau_facial=0.5, # ~0.5 seconds smoothing for Facial
        tau_gsr=3.0,    # ~3 seconds smoothing for GSR
        weight_eeg=0.05,
        weight_facial=0.6,
        weight_gsr=0.35
    )
    
    # Initialize OSC client for output
    osc_client = None
    if not args.no_osc_output:
        try:
            osc_client = udp_client.SimpleUDPClient(args.output_host, args.output_port)
            print(f"OSC output configured: {args.output_host}:{args.output_port}")
        except Exception as e:
            print(f"Warning: Could not create OSC client: {e}")
            print("Continuing without OSC output...")
    else:
        print("OSC output disabled")

    if args.test:
        run_test_mode()
        return
    
    # Create dispatcher and map messages
    disp = dispatcher.Dispatcher()
    disp.map("/eeg", print_message)
    disp.map("/facial", print_message)
    disp.map("/gsr", print_message)
    
    # Create and start server
    server = osc_server.ThreadingOSCUDPServer((args.host, args.port), disp)
    
    print(f"Smooth VAD receiver listening on {args.host}:{args.port}")
    print("Expected OSC messages:")
    print("  /eeg [valence, arousal, dominance]")
    print("  /facial [valence, arousal, dominance]")
    print("  /gsr/prediction/8s [valence, arousal, dominance]")
    print("  /gsr/prediction/20s [valence, arousal, dominance]")
    if osc_client:
        print(f"Sending combined VAD to: {args.output_host}:{args.output_port}")
        print("Output OSC messages:")
        print("  /vad/combined [valence, arousal, dominance]")
        print("  /vad/combined/valence [value]")
        print("  /vad/combined/arousal [value]") 
        print("  /vad/combined/dominance [value]")
        print("  /vad/status/eeg [0 or 1]")
        print("  /vad/status/facial [0 or 1]")
        print("  /vad/status/gsr [0 or 1]")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping VAD receiver...")
        server.shutdown()
        print("VAD receiver stopped.")


if __name__ == "__main__":
    main()