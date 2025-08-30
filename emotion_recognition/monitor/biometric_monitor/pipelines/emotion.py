"""Emotion aggregation pipeline that combines data from all sensors."""

import time
from typing import Any, Dict, Optional
from .base import BasePipeline, PipelineResult
from ..osc.osc_client import get_osc_client


class EmotionPipeline(BasePipeline):
    """Pipeline that aggregates VAD data from all sensors using SmoothedVADState."""
    
    def __init__(self, update_interval: float = 0.1):
        super().__init__("emotion_aggregation")
        
        # Get the global OSC client with SmoothedVADState
        self.osc_client = get_osc_client()
        self.update_interval = update_interval
        self.last_update_time = 0.0
        
        # Keep track of last sent values to avoid duplicate messages
        self.last_sent_vad = None
        self.last_sent_vaq = None
    
    def validate_input(self, data: Any) -> bool:
        """Validate input data - accepts any data since this pipeline is internally driven."""
        return True
    
    def process_data(self, data: Any) -> PipelineResult:
        """Process aggregated VAD data from all sensors."""
        timestamp = time.time()
        
        try:
            # Get combined VAD values from SmoothedVADState
            valence, arousal, dominance = self.osc_client.vad_state.get_vad()
            sensor_status = self.osc_client.vad_state.get_status()
            
            # Calculate VAQ
            vaq = self.osc_client._calculate_vaq(valence, arousal)
            
            # Check if values have changed significantly (avoid spam)
            current_vad = (valence, arousal, dominance)
            
            # Always send first message, then check for changes
            if self.last_sent_vad is None:
                vad_changed = True
            else:
                vad_changed = (abs(valence - self.last_sent_vad[0]) > 0.001 or
                              abs(arousal - self.last_sent_vad[1]) > 0.001 or
                              abs(dominance - self.last_sent_vad[2]) > 0.001)
            
            if vad_changed:
                self.last_sent_vad = current_vad
                self.last_sent_vaq = vaq
                
                return PipelineResult(
                    timestamp=timestamp,
                    data_type="emotion_aggregation",
                    predictions={
                        "vad": {
                            "valence": float(valence),
                            "arousal": float(arousal),
                            "dominance": float(dominance)
                        },
                        "vaq": int(vaq),
                        "sensor_status": sensor_status,
                        "active_sensors": [sensor for sensor, active in sensor_status.items() if active]
                    },
                    raw_data={
                        "combined_vad": current_vad,
                        "individual_sensors": {
                            "eeg": self.osc_client.vad_state.vad_eeg,
                            "facial": self.osc_client.vad_state.vad_facial,
                            "gsr": self.osc_client.vad_state.vad_gsr
                        }
                    },
                    metadata={
                        "weights": {
                            "eeg": self.osc_client.vad_state.weight_eeg,
                            "facial": self.osc_client.vad_state.weight_facial,
                            "gsr": self.osc_client.vad_state.weight_gsr
                        },
                        "tau_values": {
                            "eeg": self.osc_client.vad_state.tau_eeg,
                            "facial": self.osc_client.vad_state.tau_facial,
                            "gsr": self.osc_client.vad_state.tau_gsr
                        }
                    },
                    success=True
                )
            else:
                # No significant change, return unsuccessful result to avoid callbacks
                return PipelineResult(
                    timestamp=timestamp,
                    data_type="emotion_aggregation",
                    predictions={},
                    raw_data={},
                    metadata={"no_change": True},
                    success=False,
                    error_message="No significant VAD change"
                )
                
        except Exception as e:
            return PipelineResult(
                timestamp=timestamp,
                data_type="emotion_aggregation",
                predictions={},
                raw_data={},
                metadata={},
                success=False,
                error_message=str(e)
            )
    
    def _get_run_loop(self):
        """Override to use timer-based loop instead of queue-based."""
        return self._timer_based_loop
    
    def _timer_based_loop(self) -> None:
        """Timer-based processing loop that generates results at regular intervals."""
        print(f"Starting emotion aggregation loop with {self.update_interval}s interval")
        message_count = 0
        
        while not self._stop_event.is_set():
            try:
                # Wait if paused
                if self._pause_event.is_set():
                    time.sleep(0.1)
                    continue
                
                current_time = time.time()
                
                # Check if it's time to update
                if current_time - self.last_update_time >= self.update_interval:
                    self.last_update_time = current_time
                    
                    # Process aggregated data
                    result = self.process_data(None)  # No input data needed
                    
                    # Update statistics
                    self.process_count += 1
                    if not result.success:
                        self.error_count += 1
                    
                    # Send to output queue (non-blocking)
                    try:
                        self.output_queue.put(result, block=False)
                    except:
                        # Queue full, remove old result and try again
                        try:
                            self.output_queue.get_nowait()
                            self.output_queue.put(result, block=False)
                        except:
                            pass
                    
                    # Call result callbacks only for successful results
                    if result.success:
                        message_count += 1
                        if message_count <= 3 or message_count % 50 == 0:  # Debug first few and every 50th
                            print(f"EmotionPipeline: Sending message #{message_count}, VAD=({result.predictions['vad']['valence']:.3f}, {result.predictions['vad']['arousal']:.3f}, {result.predictions['vad']['dominance']:.3f})")
                        
                        for callback in self.result_callbacks:
                            try:
                                callback(result)
                            except Exception as e:
                                print(f"Error in emotion aggregation callback: {e}")
                        
                        # Send OSC data
                        try:
                            self._send_osc_data(result)
                        except Exception as e:
                            print(f"Error sending emotion aggregation OSC data: {e}")
                    elif message_count <= 10:  # Debug first few unsuccessful results
                        print(f"EmotionPipeline: Skipping message (no change), error: {result.error_message}")
                
                else:
                    # Sleep for a short time to avoid busy waiting
                    time.sleep(0.05)  # 20Hz check rate
                
            except Exception as e:
                self.error_count += 1
                print(f"Error in emotion aggregation loop: {e}")
                time.sleep(0.1)
        
        print("Emotion aggregation loop ended")
    
    def _send_osc_data(self, result: PipelineResult) -> None:
        """Send aggregated emotion data via OSC."""
        if not result.success:
            return
        
        predictions = result.predictions
        vad = predictions.get("vad", {})
        vaq = predictions.get("vaq")
        
        # The OSC sending is already handled by the OSC client itself
        # when individual sensors update, but we could add additional 
        # OSC messages here if needed for the aggregated data
        pass
    
    def get_latest_emotion_state(self) -> Dict[str, Any]:
        """Get the current emotion state."""
        valence, arousal, dominance = self.osc_client.vad_state.get_vad()
        sensor_status = self.osc_client.vad_state.get_status()
        vaq = self.osc_client._calculate_vaq(valence, arousal)
        
        return {
            "vad": {
                "valence": float(valence),
                "arousal": float(arousal), 
                "dominance": float(dominance)
            },
            "vaq": int(vaq),
            "sensor_status": sensor_status,
            "active_sensors": [sensor for sensor, active in sensor_status.items() if active],
            "timestamp": time.time()
        }
    
    def start(self) -> bool:
        """Start the emotion aggregation pipeline."""
        print(f"Starting emotion aggregation pipeline...")
        print(f" - Update interval: {self.update_interval}s")
        print(f" - OSC client: {self.osc_client}")
        
        # Always allow starting since we don't depend on models
        return super().start()