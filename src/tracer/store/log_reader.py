import os
import json
from tracer import get_log_file, LogDomain
from tracer.utils import is_in_range
from rich.console import Console
from rich.table import Table

class LogReader:
    def __init__(self, domain: LogDomain):
        # Initialize the LogReader with the log file path for the given domain
        self.file_path = get_log_file(domain)

    def read_logs_iter(self, start_time=None, end_time=None):
        """
        Yields log entries in chronological order (oldest to newest), optionally filtered by a timestamp range.

        Args:
            start_time: The start of the timestamp range (inclusive).
            end_time: The end of the timestamp range (inclusive).

        This method first reads backwards to find the oldest log in range, then reads
        from the beginning of the file to yield logs in chronological order.
        """
        # First phase: scan backwards to check if any logs are in range
        found_in_range = False
        
        # Open the file and scan backwards to check if any logs match our criteria
        with open(self.file_path, "rb") as f:
            f.seek(0, os.SEEK_END)
            buffer = b''
            pointer = f.tell()
            
            while pointer > 0:
                pointer -= 1
                f.seek(pointer)
                byte = f.read(1)
                
                if byte == b'\n':
                    if buffer:
                        line = buffer[::-1].decode()
                        try:
                            event = json.loads(line)
                            if self._is_in_range(event, start_time, end_time):
                                found_in_range = True
                                break
                        except json.JSONDecodeError:
                            pass
                        buffer = b''
                else:
                    buffer += byte
                    
            # Check first line if we haven't found anything yet
            if buffer and not found_in_range:
                line = buffer[::-1].decode()
                try:
                    event = json.loads(line)
                    if self._is_in_range(event, start_time, end_time):
                        found_in_range = True
                except json.JSONDecodeError:
                    pass
        
        # If no logs match our criteria, stop here
        if not found_in_range:
            return
            
        # Second phase: read forward and yield logs in chronological order
        with open(self.file_path, "r") as f:
            for line in f:
                try:
                    event = json.loads(line.strip())
                    if self._is_in_range(event, start_time, end_time):
                        yield event
                except json.JSONDecodeError:
                    continue

    def _is_in_range(self, event, start, end):
        ts = event.get("timestamp")  # Extract the timestamp from the event
        return ts is not None and is_in_range(ts, start, end)  # Check the range
    
    def print_logs(self, start_time=None, end_time=None):
        """
        Prints log entries in chronological order using the rich library for formatting.

        Args:
            start_time: The start of the timestamp range (inclusive).
            end_time: The end of the timestamp range (inclusive).
        """
        console = Console()
        table = Table(title="Log Entries")

        # Define table columns
        table.add_column("Timestamp", style="cyan", no_wrap=True)
        table.add_column("Event", style="magenta")

        # Iterate over logs and add rows to the table
        for event in self.read_logs_iter(start_time, end_time):
            timestamp = event.get("timestamp", "N/A")
            event_copy = dict(event)  # Make a copy
            event_copy.pop("timestamp", None)  # Remove the timestamp
            event_data = json.dumps(event_copy, indent=2)  
            table.add_row(str(timestamp), event_data)

        # Print the table to the console
        console.print(table)