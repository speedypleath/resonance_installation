"""OSC client for sending biometric data to external applications."""

from typing import Any, Dict, List, Optional, Tuple
import time
import threading
from pythonosc import udp_client
from ..config import OSCConfig


class OSCClient:
    """OSC client for sending biometric data."""
    
    def __init__(self, config: OSCConfig):
        self.config = config
        self.client: Optional[udp_client.SimpleUDPClient] = None
        self.is_connected = False
        self.message_count = 0
        self.last_send_time = 0.0
        self._lock = threading.Lock()
        
        if config.enabled:
            self.connect()
    
    def connect(self) -> bool:
        """Connect to OSC server."""
        try:
            self.client = udp_client.SimpleUDPClient(self.config.host, self.config.port)
            self.is_connected = True
            print(f"OSC client connected to {self.config.host}:{self.config.port}")
            return True
        except Exception as e:
            print(f"Failed to connect OSC client: {e}")
            self.is_connected = False
            return False
    
    def disconnect(self) -> None:
        """Disconnect from OSC server."""
        self.client = None
        self.is_connected = False
        print("OSC client disconnected")
    
    def send_message(self, address: str, *args) -> bool:
        """Send OSC message."""
        if not self.is_connected or not self.client:
            return False
        
        try:
            with self._lock:
                self.client.send_message(address, args)
                self.message_count += 1
                self.last_send_time = time.time()
            return True
        except Exception as e:
            print(f"Error sending OSC message to {address}: {e}")
            return False
    
    def send_emotion_data(self, emotion: str, confidence: float, 
                         valence: float, arousal: float, dominance: float) -> bool:
        """Send emotion recognition data via OSC."""
        timestamp = time.time()
        return self.send_message("/emotion", timestamp, emotion, confidence, 
                               valence, arousal, dominance)
    
    def send_vad_data(self, valence: float, arousal: float, dominance: float) -> bool:
        """Send VAD (Valence-Arousal-Dominance) data via OSC."""
        return self.send_message("/facial", valence, arousal, dominance)
    
    def send_eeg_data(self, channel_data: List[float], fragment_id: int = 0) -> bool:
        """Send EEG data via OSC."""
        timestamp = time.time()
        return self.send_message("/eeg", timestamp, fragment_id, *channel_data)
    
    def send_eeg_segment(self, segment_id: int, channel_data: List[List[float]]) -> bool:
        """Send EEG segment data via OSC."""
        timestamp = time.time()
        flattened_data = [val for channel in channel_data for val in channel]
        return self.send_message("/eeg/segment", timestamp, segment_id, *flattened_data)
    
    def send_custom_data(self, address: str, data: Dict[str, Any]) -> bool:
        """Send custom data structure via OSC."""
        timestamp = time.time()
        
        # Flatten dictionary into OSC-compatible format
        args = [timestamp]
        for key, value in data.items():
            if isinstance(value, (list, tuple)):
                args.extend(value)
            else:
                args.append(value)
        
        return self.send_message(address, *args)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get OSC client statistics."""
        return {
            "is_connected": self.is_connected,
            "host": self.config.host,
            "port": self.config.port,
            "message_count": self.message_count,
            "last_send_time": self.last_send_time,
            "enabled": self.config.enabled
        }
    
    def test_connection(self) -> bool:
        """Test OSC connection by sending a ping message."""
        return self.send_message("/ping", time.time(), "biometric_monitor")


class OSCRouter:
    """Router for managing multiple OSC destinations."""
    
    def __init__(self):
        self.clients: Dict[str, OSCClient] = {}
        self.routes: Dict[str, List[str]] = {}  # message_type -> [client_names]
    
    def add_client(self, name: str, config: OSCConfig) -> bool:
        """Add OSC client with given name."""
        try:
            client = OSCClient(config)
            if client.is_connected:
                self.clients[name] = client
                print(f"Added OSC client '{name}' -> {config.host}:{config.port}")
                return True
            return False
        except Exception as e:
            print(f"Failed to add OSC client '{name}': {e}")
            return False
    
    def remove_client(self, name: str) -> bool:
        """Remove OSC client."""
        if name in self.clients:
            self.clients[name].disconnect()
            del self.clients[name]
            
            # Remove from routes
            for message_type in self.routes:
                if name in self.routes[message_type]:
                    self.routes[message_type].remove(name)
            
            print(f"Removed OSC client '{name}'")
            return True
        return False
    
    def add_route(self, message_type: str, client_name: str) -> bool:
        """Add routing rule for message type to client."""
        if client_name not in self.clients:
            return False
        
        if message_type not in self.routes:
            self.routes[message_type] = []
        
        if client_name not in self.routes[message_type]:
            self.routes[message_type].append(client_name)
            print(f"Added route: {message_type} -> {client_name}")
            return True
        
        return False
    
    def broadcast_emotion(self, emotion: str, confidence: float, 
                         valence: float, arousal: float, dominance: float) -> int:
        """Broadcast emotion data to all configured clients."""
        sent_count = 0
        
        for client_name in self.routes.get("facial", []):
            if client_name in self.clients:
                if self.clients[client_name].send_emotion_data(
                    emotion, confidence, valence, arousal, dominance):
                    sent_count += 1
        
        return sent_count
    
    def broadcast_vad(self, valence: float, arousal: float, dominance: float) -> int:
        """Broadcast VAD data to all configured clients."""
        sent_count = 0
        
        for client_name in self.routes.get("vad", []):
            if client_name in self.clients:
                if self.clients[client_name].send_vad_data(valence, arousal, dominance):
                    sent_count += 1
        
        return sent_count
    
    def broadcast_eeg(self, channel_data: List[float], fragment_id: int = 0) -> int:
        """Broadcast EEG data to all configured clients."""
        sent_count = 0
        
        for client_name in self.routes.get("eeg", []):
            if client_name in self.clients:
                if self.clients[client_name].send_eeg_data(channel_data, fragment_id):
                    sent_count += 1
        
        return sent_count
    
    def get_router_stats(self) -> Dict[str, Any]:
        """Get router statistics."""
        client_stats = {}
        for name, client in self.clients.items():
            client_stats[name] = client.get_stats()
        
        return {
            "clients": client_stats,
            "routes": self.routes,
            "total_clients": len(self.clients),
            "active_clients": sum(1 for client in self.clients.values() if client.is_connected)
        }