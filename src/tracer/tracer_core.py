from tracer.store import LogReader, LogWriter
from tracer.config import LogDomain
from tracer.core import BaseTracer
from tracer.core import FileTracer
from typing import Dict, Tuple

class TracerCore:
    def __init__(self):
        # Use tuple of (domain, path) as key for filesystem tracers
        self.active_tracers: Dict[Tuple[str, str], BaseTracer] = {}

    def start_tracing(self, domain: str, dir_to_watch: str = None):
        """Starts tracing for the specified domain."""
        if domain == LogDomain.FS.value:
            if not dir_to_watch:
                print("Error: --dir is required start filesystem tracing")
                return
            
            tracer_key = (domain, dir_to_watch)
            if tracer_key in self.active_tracers:
                print(f"Tracing already active for {domain} in directory {dir_to_watch}")
                return
                
            print("Starting filesystem tracing...")
            tracer = FileTracer(LogDomain.FS, dir_to_watch)
            tracer.start()
            self.active_tracers[tracer_key] = tracer

        elif domain == LogDomain.NET.value:
            print("Starting network tracing...")
            # Replace with actual NetTracer implementation
            tracer = BaseTracer(LogDomain.NET)
            tracer.start()
            tracer_key = (domain, None)
            self.active_tracers[tracer_key] = tracer
        else:
            print(f"Unknown domain: {domain}")
            print(f"should {LogDomain.FS.value}")

    def print_logs(self, domain: str, start_time: str = None, end_time: str = None):
        """Prints logs for the specified domain and time range."""
        log_domain = next((d for d in LogDomain if d.value == domain), None)
        if log_domain is None:
            print(f"Unknown domain: {domain}")
            return

        reader = LogReader(log_domain)
        reader.print_logs(start_time, end_time)

    def clear_logs(self, domain: str):
        """Clears all logs for the specified domain."""
        log_domain = next((d for d in LogDomain if d.value == domain), None)
        if log_domain is None:
            print(f"Unknown domain: {domain}")
            return
        
        writer = LogWriter(log_domain)
        writer.clear()
