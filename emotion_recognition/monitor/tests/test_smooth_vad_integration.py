#!/usr/bin/env python3
"""
Test script for OSC client integration with pipelines.
This demonstrates how the pipelines now send data to the centralized OSC client.

Usage: uv run tests/test_smooth_vad_integration.py
"""

import time
import sys
import os

# Add the parent directory to Python path to import biometric_monitor
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from biometric_monitor.osc.osc_client import get_osc_client

def test_integration():
    """Test the OSC client integration."""
    print("Testing OSC Client Integration")
    print("=" * 50)
    
    # Get the OSC client instance
    osc_client = get_osc_client(
        output_host="127.0.0.1",
        output_port=5002,
        tau_eeg=0.5,
        tau_facial=0.5,
        tau_gsr=3.0,
        weight_eeg=0.05,
        weight_facial=0.6,
        weight_gsr=0.35
    )
    
    print("Simulating pipeline data flow...")
    print()
    
    # Simulate facial emotion pipeline data
    print("1. Simulating Facial Pipeline:")
    osc_client.update_facial(0.7, 0.6, 0.8)  # Happy, medium arousal, confident
    time.sleep(1)
    
    # Simulate EEG pipeline data
    print("2. Simulating EEG Pipeline:")
    osc_client.update_eeg(0.5, 0.4, 0.5)  # Neutral, low arousal, neutral dominance
    time.sleep(1)
    
    # Simulate GSR stress detection pipeline data
    print("3. Simulating GSR Pipeline (No Stress):")
    osc_client.update_gsr(0.7, 0.3, 0.6)  # Positive valence, low arousal, good signal
    time.sleep(2)
    
    print("4. Simulating GSR Pipeline (Stress Detected):")
    osc_client.update_gsr(0.2, 0.8, 0.7)  # Negative valence, high arousal, good signal
    time.sleep(1)
    
    # Show combined state
    combined_vad = osc_client.vad_state.get_vad()
    status = osc_client.vad_state.get_status()
    
    print()
    print("Final Combined State:")
    print(f"  Valence: {combined_vad[0]:.3f}")
    print(f"  Arousal: {combined_vad[1]:.3f}")
    print(f"  Dominance: {combined_vad[2]:.3f}")
    print()
    print("Sensor Status:")
    print(f"  EEG Active: {status['eeg']}")
    print(f"  Facial Active: {status['facial']}")
    print(f"  GSR Active: {status['gsr']}")
    print()
    print("Integration test completed!")

if __name__ == "__main__":
    test_integration()