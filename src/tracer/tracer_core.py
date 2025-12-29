import threading
from tracer.store import LogReader, LogWriter
from tracer.config import LogDomain
from tracer.core import BaseTracer
from tracer.core import FileTracer
from typing import Dict, Tuple


class TracerCore:
    # Use tuple of (domain, path) as key for filesystem tracers
    active_tracers: Dict[Tuple[str, str], BaseTracer] = {}
    tracer_threads: Dict[Tuple[str, str], threading.Thread] = {}

    @staticmethod
    def start_tracing(domain: str, dir_to_watch: str = None):
        """Starts tracing for the specified domain."""
        if domain == LogDomain.FS.value:
            if not dir_to_watch:
                raise ValueError("Error: --dir is required to start filesystem tracing")

            tracer_key = (domain, dir_to_watch)
            if tracer_key in TracerCore.active_tracers:
                raise ValueError(
                    f"Tracing already active for {domain} in directory {dir_to_watch}"
                )

            tracer = FileTracer(LogDomain.FS, dir_to_watch)

            # Create and start thread for tracing
            thread = threading.Thread(
                target=tracer.start,
                daemon=True,  # Thread will exit when main program exits
                name=f"tracer-{domain}-{dir_to_watch}",
            )
            thread.start()

            TracerCore.active_tracers[tracer_key] = tracer
            TracerCore.tracer_threads[tracer_key] = thread
            return (
                f"Successfully started filesystem tracing for directory: {dir_to_watch}"
            )

        elif domain == LogDomain.NET.value:
            # Replace with actual NetTracer implementation
            tracer = BaseTracer(LogDomain.NET)
            tracer_key = (domain, None)

            if tracer_key in TracerCore.active_tracers:
                raise ValueError(f"Tracing already active for {domain}")

            # Create and start thread for tracing
            thread = threading.Thread(
                target=tracer.start,
                daemon=True,  # Thread will exit when main program exits
                name=f"tracer-{domain}",
            )
            thread.start()

            TracerCore.active_tracers[tracer_key] = tracer
            TracerCore.tracer_threads[tracer_key] = thread
            return "Successfully started network tracing"
        else:
            raise ValueError(
                f"Unknown domain: {domain}. Should be {LogDomain.FS.value} or {LogDomain.NET.value}"
            )

    @staticmethod
    def stop_tracing(domain: str, dir_to_watch: str = None):
        """Stops tracing for the specified domain."""
        tracer_key = (domain, dir_to_watch)

        if domain == LogDomain.FS.value:
            if not dir_to_watch:
                raise ValueError("Error: --dir is required to start filesystem tracing")

        if tracer_key not in TracerCore.active_tracers:
            if domain == LogDomain.FS.value and dir_to_watch:
                raise ValueError(
                    f"No active tracing found for {domain} in directory {dir_to_watch}"
                )
            else:
                raise ValueError(f"No active tracing found for {domain}")

        # Stop the tracer
        tracer = TracerCore.active_tracers[tracer_key]
        if hasattr(tracer, "stop") and callable(getattr(tracer, "stop")):
            tracer.stop()

        # Wait for thread to finish (with timeout to avoid blocking)
        thread = TracerCore.tracer_threads.get(tracer_key)
        if thread and thread.is_alive():
            thread.join(timeout=5.0)  # Wait up to 5 seconds
            if thread.is_alive():
                print(f"Warning: Tracer thread for {domain} did not stop gracefully")

        # Remove from active tracers and threads
        del TracerCore.active_tracers[tracer_key]
        if tracer_key in TracerCore.tracer_threads:
            del TracerCore.tracer_threads[tracer_key]

        if domain == LogDomain.FS.value and dir_to_watch:
            return f"Stopped tracing for {domain} in directory {dir_to_watch}"
        else:
            return f"Stopped tracing for {domain}"

    @staticmethod
    def list_tracers():
        """Returns information about currently active tracers."""
        if not TracerCore.active_tracers:
            return {}

        active_info = {}
        for (domain, directory), tracer in TracerCore.active_tracers.items():
            key = f"{domain}_{directory}" if directory else domain
            thread = TracerCore.tracer_threads.get((domain, directory))
            thread_status = "running" if thread and thread.is_alive() else "stopped"

            active_info[key] = {
                "domain": domain,
                "directory": directory,
                "tracer_type": type(tracer).__name__,
                "thread_status": thread_status,
                "thread_name": thread.name if thread else None,
            }

        return active_info

    @staticmethod
    def print_logs(domain: str, start_time: str = None, end_time: str = None):
        """Prints logs for the specified domain and time range."""
        log_domain = next((d for d in LogDomain if d.value == domain), None)
        if log_domain is None:
            raise ValueError(f"Unknown domain: {domain}")

        reader = LogReader(log_domain)
        reader.print_logs(start_time, end_time)

    @staticmethod
    def clear_logs(domain: str):
        """Clears all logs for the specified domain."""
        log_domain = next((d for d in LogDomain if d.value == domain), None)
        if log_domain is None:
            raise ValueError(f"Unknown domain: {domain}")

        writer = LogWriter(log_domain)
        writer.clear()
        return f"Successfully cleared logs for domain: {domain}"
