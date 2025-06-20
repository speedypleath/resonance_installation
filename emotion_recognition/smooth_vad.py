import time
import math
import argparse
from pythonosc import dispatcher
from pythonosc import osc_server
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

        state_dict['valence'] = alpha * new_vad[0] + (1 - alpha) * state_dict['valence']
        state_dict['arousal'] = alpha * new_vad[1] + (1 - alpha) * state_dict['arousal']
        state_dict['dominance'] = alpha * new_vad[2] + (1 - alpha) * state_dict['dominance']

        self.last_update[last_time_key] = now
        self._recalculate_combination()

    def update_eeg(self, vad):       self._update_vad(self.vad_eeg, vad, self.tau_eeg, 'eeg')
    def update_facial(self, vad):    self._update_vad(self.vad_facial, vad, self.tau_facial, 'facial')
    def update_gsr(self, vad):       self._update_vad(self.vad_gsr, vad, self.tau_gsr, 'gsr')

    def _recalculate_combination(self):
        total_weight = self.weight_eeg + self.weight_facial + self.weight_gsr
        if total_weight == 0:
            return
        self.valence = (
            self.vad_eeg['valence'] * self.weight_eeg +
            self.vad_facial['valence'] * self.weight_facial
        ) / (self.weight_eeg + self.weight_facial)
        self.arousal = (
            self.vad_eeg['arousal'] * self.c +
            self.vad_facial['arousal'] * self.weight_facial +
            self.vad_gsr['arousal'] * self.weight_gsr
        ) / total_weight
        self.dominance = (
            self.vad_eeg['dominance'] * self.weight_eeg +
            self.vad_facial['dominance'] * self.weight_facial +
            self.vad_gsr['dominance'] * self.weight_gsr
        ) / total_weight

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
    
    elif address == "/gsr/prediction/20s":
        if len(args) >= 3:
            valence, arousal, dominance = args[0], args[1], args[2]
            vad_state.update_gsr((valence, arousal, dominance))
            print(f"GSR Prediction 20s: V={valence:.3f}, A={arousal:.3f}, D={dominance:.3f}")

def print_combined_state():
    """Print the combined emotional state"""
    valence, arousal, dominance = vad_state.get_vad()
    status = vad_state.get_status()
    
    print(f"Combined VAD: V={valence:.3f}, A={arousal:.3f}, D={dominance:.3f}")
    print(f"Status: EEG={status['eeg']}, Facial={status['facial']}, GSR={status['gsr']}")
    print("-" * 50)


def main():
    """Main function to run the OSC receiver"""
    global vad_state
    
    parser = argparse.ArgumentParser(description="Smooth VAD State Receiver")
    parser.add_argument("--host", default="192.168.0.141", help="Host to bind to")
    parser.add_argument("--port", type=int, default=5001, help="Port to bind to")
    
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