from tracer.config import LogDomain
from tracer.core.base_tracer import BaseTracer
from tracer.core.fs_tracer import FileTracer
from tracer.store.log_writer import LogWriter

def start_tracing(domain: str, dir_to_watch: str = None):
    """Starts tracing for the specified domain."""
    if domain == "fs":
        if not dir_to_watch:
            print("Error: --dir is required for the 'fs' domain.")
            return
        print("Starting filesystem tracing...")
        # Replace with actual FileTracer implementation
        tracer = FileTracer(LogWriter(LogDomain.FS), dir_to_watch)
        tracer.start()
    elif domain == "net":
        print("Starting network tracing...")
        # Replace with actual NetTracer implementation
        tracer = BaseTracer(LogWriter(LogDomain.NET))
        tracer.start()
    else:
        print(f"Unknown domain: {domain}")
