from tracer.store.log_reader import LogReader
from tracer.store.log_writer import LogWriter
from tracer.config import LogDomain
def print_logs(domain: str, start_time: str = None, end_time: str = None):
    """Prints logs for the specified domain and time range."""
    log_domain = next((d for d in LogDomain if d.value == domain), None)
    if log_domain is None:
        print(f"Unknown domain: {domain}")
        return

    reader = LogReader(log_domain)
    reader.print_logs(start_time, end_time)