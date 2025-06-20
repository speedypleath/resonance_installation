import argparse

try:
    from pythonosc import dispatcher
    from pythonosc import osc_server
    from pythonosc import udp_client
except ImportError:
    print("pythonosc not found. Installing...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pythonosc"])
    from pythonosc import dispatcher
    from pythonosc import osc_server
    from pythonosc import udp_client


# Global variables to store current state
current_data = {
    'delta': [0.0, 0.0, 0.0, 0.0],
    'theta': [0.0, 0.0, 0.0, 0.0],
    'alpha': [0.0, 0.0, 0.0, 0.0],
    'beta': [0.0, 0.0, 0.0, 0.0],
    'gamma': [0.0, 0.0, 0.0, 0.0],
    'horseshoe': [0, 0, 0, 0],
    'blink': False,
    'jaw_clench': False,
    'blink_counter': 0,
    'clench_counter': 0,
    'bands_received': {'delta': False, 'theta': False, 'alpha': False, 'beta': False, 'gamma': False}
}

# OSC client for sending data
osc_client = None


def send_osc_message(address: str, *args):
    """Send OSC message if client is configured"""
    global osc_client
    if osc_client is not None:
        try:
            osc_client.send_message(address, args)
        except Exception as e:
            print(f"Error sending OSC message: {e}")


def calculate_vad(delta: float, theta: float, alpha: float, beta: float, gamma: float) -> tuple:
    arousal = beta + gamma - alpha
    valence = alpha - theta
    dominance = beta - theta
    
    return arousal, valence, dominance


def check_and_calculate_vad():
    """Check if all bands are received and calculate VAD if so"""
    if all(current_data['bands_received'].values()):
        # Calculate averages for all bands
        delta_avg = calculate_average_band('delta')
        theta_avg = calculate_average_band('theta')
        alpha_avg = calculate_average_band('alpha')
        beta_avg = calculate_average_band('beta')
        gamma_avg = calculate_average_band('gamma')
        
        # Calculate VAD
        arousal, valence, dominance = calculate_vad(delta_avg, theta_avg, alpha_avg, beta_avg, gamma_avg)
        
        # Print VAD results
        artifact_status = ""
        if current_data['blink_counter'] > 0:
            artifact_status += f" blink_ignore({current_data['blink_counter']})"
        if current_data['clench_counter'] > 0:
            artifact_status += f" clench_ignore({current_data['clench_counter']})"
        
        print(f"VAD - Arousal: {arousal:.4f}, Valence: {valence:.4f}, Dominance: {dominance:.4f}{artifact_status}")
        
        # Send only VAD data via OSC
        send_osc_message("/eeg", arousal, valence, dominance)
        
        # Reset the received flags
        for band in current_data['bands_received']:
            current_data['bands_received'][band] = False


def calculate_average_band(band_name: str) -> float:
    """Calculate weighted average for a brain wave band, ignoring electrodes 1 and 4 during artifacts"""
    if band_name not in current_data:
        return 0.0
    
    values = current_data[band_name]
    horseshoe = current_data['horseshoe']
    
    # Check if we should ignore electrodes 1 and 4 due to recent artifacts
    ignore_outer = (current_data['blink_counter'] > 0 or current_data['clench_counter'] > 0)
    
    if ignore_outer and len(values) >= 3:
        # Use only electrodes 2 and 3 (indices 1 and 2)
        electrode_values = [values[1], values[2]]
        electrode_quality = [horseshoe[1], horseshoe[2]]
    else:
        # Use all electrodes
        electrode_values = values
        electrode_quality = horseshoe
    
    # Calculate weighted average based on signal quality
    # Quality weights: 1=Good (weight 1.0), 2=Medium (weight 0.5), 4=Bad (weight 0.1)
    total_weighted_sum = 0.0
    total_weight = 0.0
    
    for i, (value, quality) in enumerate(zip(electrode_values, electrode_quality)):
        if quality == 1:  # Good
            weight = 1.0
        elif quality == 2:  # Medium
            weight = 0.5
        elif quality == 4:  # Bad
            weight = 0.1
        else:
            weight = 0.0  # Unknown quality
        
        total_weighted_sum += value * weight
        total_weight += weight
    
    if total_weight > 0:
        return total_weighted_sum / total_weight
    else:
        return 0.0


def update_artifact_counters():
    """Update artifact counters - decrement them each sample"""
    if current_data['blink_counter'] > 0:
        current_data['blink_counter'] -= 1
    if current_data['clench_counter'] > 0:
        current_data['clench_counter'] -= 1


def print_message(address: str, *args):
    """Simple function to print received OSC messages"""
    if address.startswith("/muse/elements"):
        # Update artifact counters for each message
        update_artifact_counters()
        
        # Parse different types of messages
        if "/delta" in address:
            if len(args) == 4:
                current_data['delta'] = list(args)
                current_data['bands_received']['delta'] = True
                avg = calculate_average_band('delta')
                artifact_status = ""
                if current_data['blink_counter'] > 0:
                    artifact_status += f" blink_ignore({current_data['blink_counter']})"
                if current_data['clench_counter'] > 0:
                    artifact_status += f" clench_ignore({current_data['clench_counter']})"
                print(f"Delta: {avg:.4f}{artifact_status}")
                check_and_calculate_vad()
        
        elif "/theta" in address:
            if len(args) == 4:
                current_data['theta'] = list(args)
                current_data['bands_received']['theta'] = True
                avg = calculate_average_band('theta')
                artifact_status = ""
                if current_data['blink_counter'] > 0:
                    artifact_status += f" blink_ignore({current_data['blink_counter']})"
                if current_data['clench_counter'] > 0:
                    artifact_status += f" clench_ignore({current_data['clench_counter']})"
                print(f"Theta: {avg:.4f}{artifact_status}")
                check_and_calculate_vad()
        
        elif "/alpha" in address:
            if len(args) == 4:
                current_data['alpha'] = list(args)
                current_data['bands_received']['alpha'] = True
                avg = calculate_average_band('alpha')
                artifact_status = ""
                if current_data['blink_counter'] > 0:
                    artifact_status += f" blink_ignore({current_data['blink_counter']})"
                if current_data['clench_counter'] > 0:
                    artifact_status += f" clench_ignore({current_data['clench_counter']})"
                print(f"Alpha: {avg:.4f}{artifact_status}")
                check_and_calculate_vad()
        
        elif "/beta" in address:
            if len(args) == 4:
                current_data['beta'] = list(args)
                current_data['bands_received']['beta'] = True
                avg = calculate_average_band('beta')
                artifact_status = ""
                if current_data['blink_counter'] > 0:
                    artifact_status += f" blink_ignore({current_data['blink_counter']})"
                if current_data['clench_counter'] > 0:
                    artifact_status += f" clench_ignore({current_data['clench_counter']})"
                print(f"Beta: {avg:.4f}{artifact_status}")
                check_and_calculate_vad()
        
        elif "/gamma" in address:
            if len(args) == 4:
                current_data['gamma'] = list(args)
                current_data['bands_received']['gamma'] = True
                avg = calculate_average_band('gamma')
                artifact_status = ""
                if current_data['blink_counter'] > 0:
                    artifact_status += f" blink_ignore({current_data['blink_counter']})"
                if current_data['clench_counter'] > 0:
                    artifact_status += f" clench_ignore({current_data['clench_counter']})"
                print(f"Gamma: {avg:.4f}{artifact_status}")
                check_and_calculate_vad()
        
        elif "/horseshoe" in address:
            if len(args) == 4:
                current_data['horseshoe'] = list(args)
                print(f"Horseshoe: {args} (1=Good, 2=Medium, 4=Bad)")
        
        elif "/blink" in address:
            print(f"Blink: {args}")
            if len(args) == 1 and args[0] == 1:
                current_data['blink'] = True
                current_data['blink_counter'] = 5  # Ignore for 5 samples
                print("BLINK DETECTED - Ignoring electrodes 1&4 for 5 samples")
            else:
                current_data['blink'] = False
        
        elif "/jaw_clench" in address:
            print(f"Jaw Clench: {args}")
            if len(args) == 1 and args[0] == 1:
                current_data['jaw_clench'] = True
                current_data['clench_counter'] = 5  # Ignore for 5 samples
                print("JAW CLENCH DETECTED - Ignoring electrodes 1&4 for 5 samples")
            else:
                current_data['jaw_clench'] = False


def main():
    """Main function to run the OSC receiver"""
    parser = argparse.ArgumentParser(description="Simple OSC Data Receiver")
    parser.add_argument("--host", default="192.168.0.141", help="Host to bind to")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind to")
    parser.add_argument("--send-host", default="192.168.0.141", help="Host to send OSC messages to")
    parser.add_argument("--send-port", type=int, default=5001, help="Port to send OSC messages to")
    
    args = parser.parse_args()
    
    # Setup OSC client for sending messages
    global osc_client
    try:
        osc_client = udp_client.SimpleUDPClient(args.send_host, args.send_port)
        print(f"OSC client configured to send to {args.send_host}:{args.send_port}")
    except Exception as e:
        print(f"Warning: Could not setup OSC client: {e}")
        print("OSC messages will not be sent")
    
    # Create dispatcher and map all messages to print function
    disp = dispatcher.Dispatcher()
    disp.set_default_handler(print_message)
    
    # Create and start server
    server = osc_server.ThreadingOSCUDPServer((args.host, args.port), disp)
    
    print(f"OSC receiver listening on {args.host}:{args.port}")
    print("Tracking: delta, theta, alpha, beta, gamma")
    print("Ignoring electrodes 1&4 during blinks and jaw clenches")
    print("Sending OSC messages with 'eeg' prefix")
    print("Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping OSC receiver...")
        server.shutdown()
        print("OSC receiver stopped")


if __name__ == "__main__":
    main()
