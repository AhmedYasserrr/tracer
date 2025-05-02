from tracer.store.log_reader import LogReader
from tracer.config import LogDomain
from tracer.core.base_tracer import BaseTracer
from tracer.core.fs_tracer import FileTracer

class TracerCore:
    def __init__(self):
        pass 

    def start_tracing(self, domain: str, dir_to_watch: str = None):
        """Starts tracing for the specified domain."""
        if domain == "fs":
            if not dir_to_watch:
                print("Error: --dir is required for the 'fs' domain.")
                return
            print("Starting filesystem tracing...")
            # Replace with actual FileTracer implementation
            tracer = FileTracer(LogDomain.FS, dir_to_watch)
            tracer.start()
        elif domain == "net":
            print("Starting network tracing...")
            # Replace with actual NetTracer implementation
            tracer = BaseTracer(LogDomain.NET)
            tracer.start()
        else:
            print(f"Unknown domain: {domain}")

    def print_logs(self, domain: str, start_time: str = None, end_time: str = None):
        """Prints logs for the specified domain and time range."""
        log_domain = next((d for d in LogDomain if d.value == domain), None)
        if log_domain is None:
            print(f"Unknown domain: {domain}")
            return

        reader = LogReader(log_domain)
        reader.print_logs(start_time, end_time)