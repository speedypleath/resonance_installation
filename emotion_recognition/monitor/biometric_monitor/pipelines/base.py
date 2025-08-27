"""Base pipeline classes for biometric data processing."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
import threading
import time
import queue
from dataclasses import dataclass

from ..osc.osc_client import OSCClient
from ..models.base import BiometricModel


@dataclass
class PipelineResult:
    """Standard result format for pipeline outputs."""
    timestamp: float
    data_type: str
    predictions: Dict[str, Any]
    raw_data: Any
    metadata: Dict[str, Any]
    success: bool
    error_message: Optional[str] = None


class BiometricPipeline(ABC):
    """Abstract base class for biometric data processing pipelines."""
    
    def __init__(self, name: str, model: BiometricModel, osc_client: Optional[OSCClient] = None):
        self.name = name
        self.model = model
        self.osc_client = osc_client
        
        # Pipeline state
        self.is_running = False
        self.is_paused = False
        self.process_count = 0
        self.error_count = 0
        self.start_time = None
        
        # Threading
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        
        # Data queues
        self.input_queue: queue.Queue = queue.Queue(maxsize=100)
        self.output_queue: queue.Queue = queue.Queue(maxsize=100)
        
        # Callbacks
        self.result_callbacks: List[Callable[[PipelineResult], None]] = []
        self.error_callbacks: List[Callable[[Exception], None]] = []
    
    @abstractmethod
    def process_data(self, data: Any) -> PipelineResult:
        """Process input data and return result."""
        pass
    
    @abstractmethod
    def validate_input(self, data: Any) -> bool:
        """Validate input data format."""
        pass
    
    def add_result_callback(self, callback: Callable[[PipelineResult], None]) -> None:
        """Add callback for processing results."""
        self.result_callbacks.append(callback)
    
    def add_error_callback(self, callback: Callable[[Exception], None]) -> None:
        """Add callback for handling errors."""
        self.error_callbacks.append(callback)
    
    def start(self) -> bool:
        """Start the pipeline processing thread."""
        if self.is_running:
            return True
        
        # Check if it's a dummy model (for visualization pipelines like EEG)
        is_dummy_model = (hasattr(self.model, '__class__') and 
                         'Dummy' in self.model.__class__.__name__)
        
        print(f"Starting pipeline '{self.name}'...")
        print(f" - Model: {self.model.__class__.__name__ if self.model else 'None'}")
        print(f" - Is dummy model: {is_dummy_model}")

        # Check model requirement - allow dummy models for visualization
        if self.model is None and not is_dummy_model:
            print(f"Cannot start pipeline '{self.name}': no model provided")
            return False
        
        # Check if it's a real model that needs to be loaded
        is_loaded = getattr(self.model, 'is_loaded', False)
        
        if not is_dummy_model and not is_loaded:
            print(f"Cannot start pipeline '{self.name}': model not loaded")
            return False
        
        if is_dummy_model:
            print(f"Pipeline '{self.name}' starting with dummy model for visualization")
        
        self._stop_event.clear()
        self._pause_event.clear()
        
        # Use the method returned by _get_run_loop() instead of hardcoded _run_loop
        run_method = self._get_run_loop()
        self._thread = threading.Thread(target=run_method, daemon=True)
        self._thread.start()
        
        self.is_running = True
        self.start_time = time.time()
        print(f"Pipeline '{self.name}' started with {run_method.__name__}")
        return True
    
    def _get_run_loop(self):
        """Get the appropriate run loop method (can be overridden by subclasses)."""
        return self._run_loop
    
    def stop(self) -> None:
        """Stop the pipeline processing."""
        if not self.is_running:
            return
        
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        
        self.is_running = False
        print(f"Pipeline '{self.name}' stopped")
    
    def pause(self) -> None:
        """Pause pipeline processing."""
        if self.is_running:
            self._pause_event.set()
            self.is_paused = True
            print(f"Pipeline '{self.name}' paused")
    
    def resume(self) -> None:
        """Resume pipeline processing."""
        if self.is_paused:
            self._pause_event.clear()
            self.is_paused = False
            print(f"Pipeline '{self.name}' resumed")
    
    def add_data(self, data: Any, timeout: float = 1.0) -> bool:
        """Add data to processing queue."""
        try:
            if not self.validate_input(data):
                return False
            
            self.input_queue.put(data, timeout=timeout)
            return True
        except queue.Full:
            print(f"Pipeline '{self.name}' input queue full, dropping data")
            return False
    
    def get_result(self, timeout: float = 1.0) -> Optional[PipelineResult]:
        """Get processed result from output queue."""
        try:
            return self.output_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def _run_loop(self) -> None:
        """Main processing loop."""
        while not self._stop_event.is_set():
            try:
                # Wait if paused
                if self._pause_event.is_set():
                    time.sleep(0.1)
                    continue
                
                # Get input data
                try:
                    data = self.input_queue.get(timeout=0.1)
                except queue.Empty:
                    continue
                
                # Process data
                result = self.process_data(data)
                
                # Update statistics
                self.process_count += 1
                if not result.success:
                    self.error_count += 1
                
                # Send to output queue
                try:
                    self.output_queue.put(result, timeout=0.1)
                except queue.Full:
                    print(f"Pipeline '{self.name}' output queue full, dropping result")
                
                # Call result callbacks
                for callback in self.result_callbacks:
                    try:
                        callback(result)
                    except Exception as e:
                        print(f"Error in result callback: {e}")
                
                # Send OSC data if configured
                if result.success and self.osc_client:
                    self._send_osc_data(result)
                
            except Exception as e:
                self.error_count += 1
                print(f"Error in pipeline '{self.name}': {e}")
                
                # Call error callbacks
                for callback in self.error_callbacks:
                    try:
                        callback(e)
                    except Exception as cb_error:
                        print(f"Error in error callback: {cb_error}")
    
    def _send_osc_data(self, result: PipelineResult) -> None:
        """Send result data via OSC (to be implemented by subclasses)."""
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """Get pipeline statistics."""
        uptime = time.time() - self.start_time if self.start_time else 0
        
        return {
            "name": self.name,
            "is_running": self.is_running,
            "is_paused": self.is_paused,
            "process_count": self.process_count,
            "error_count": self.error_count,
            "uptime": uptime,
            "input_queue_size": self.input_queue.qsize(),
            "output_queue_size": self.output_queue.qsize(),
            "model_info": self.model.get_model_info() if self.model else None,
            "osc_stats": self.osc_client.get_stats() if self.osc_client else None
        }
    
    def clear_queues(self) -> None:
        """Clear input and output queues."""
        while not self.input_queue.empty():
            try:
                self.input_queue.get_nowait()
            except queue.Empty:
                break
        
        while not self.output_queue.empty():
            try:
                self.output_queue.get_nowait()
            except queue.Empty:
                break
        
        print(f"Cleared queues for pipeline '{self.name}'")


class PipelineManager:
    """Manager for multiple biometric pipelines."""
    
    def __init__(self):
        self.pipelines: Dict[str, BiometricPipeline] = {}
        self.global_callbacks: List[Callable[[str, PipelineResult], None]] = []
    
    def register_pipeline(self, pipeline: BiometricPipeline) -> None:
        """Register a pipeline."""
        self.pipelines[pipeline.name] = pipeline
        
        # Add global callback to pipeline
        pipeline.add_result_callback(
            lambda result, name=pipeline.name: self._handle_global_result(name, result)
        )
        
        print(f"Registered pipeline: {pipeline.name}")
    
    def get_pipeline(self, name: str) -> Optional[BiometricPipeline]:
        """Get pipeline by name."""
        return self.pipelines.get(name)
    
    def start_pipeline(self, name: str) -> bool:
        """Start specific pipeline."""
        pipeline = self.pipelines.get(name)
        if pipeline and not pipeline.is_running:
            return pipeline.start()
        return False
    
    def stop_pipeline(self, name: str) -> None:
        """Stop specific pipeline."""
        pipeline = self.pipelines.get(name)
        if pipeline:
            pipeline.stop()
    
    def start_all(self) -> Dict[str, bool]:
        """Start all pipelines."""
        results = {}
        for name, pipeline in self.pipelines.items():
            results[name] = pipeline.start()
        return results
    
    def stop_all(self) -> None:
        """Stop all pipelines."""
        for pipeline in self.pipelines.values():
            pipeline.stop()
    
    def pause_all(self) -> None:
        """Pause all pipelines."""
        for pipeline in self.pipelines.values():
            pipeline.pause()
    
    def resume_all(self) -> None:
        """Resume all pipelines."""
        for pipeline in self.pipelines.values():
            pipeline.resume()
    
    def add_global_callback(self, callback: Callable[[str, PipelineResult], None]) -> None:
        """Add global callback for all pipeline results."""
        self.global_callbacks.append(callback)
    
    def _handle_global_result(self, pipeline_name: str, result: PipelineResult) -> None:
        """Handle result from any pipeline."""
        for callback in self.global_callbacks:
            try:
                callback(pipeline_name, result)
            except Exception as e:
                print(f"Error in global callback: {e}")
    
    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all pipelines."""
        return {name: pipeline.get_stats() for name, pipeline in self.pipelines.items()}
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics across all pipelines."""
        total_processes = sum(p.process_count for p in self.pipelines.values())
        total_errors = sum(p.error_count for p in self.pipelines.values())
        running_count = sum(1 for p in self.pipelines.values() if p.is_running)
        
        return {
            "total_pipelines": len(self.pipelines),
            "running_pipelines": running_count,
            "total_processes": total_processes,
            "total_errors": total_errors,
            "error_rate": total_errors / max(total_processes, 1)
        }