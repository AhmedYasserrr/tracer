import os
import json
from tracer.config import get_log_file, LogDomain
from tracer.utils.timestamp import is_in_range

class LogReader:
    def __init__(self, domain: LogDomain):
        # Initialize the LogReader with the log file path for the given domain
        self.file_path = get_log_file(domain)

    def reverse_iter(self, start_time=None, end_time=None):
        """
        Yields log entries in reverse order, optionally filtered by a timestamp range.

        Args:
            start_time: The start of the timestamp range (inclusive).
            end_time: The end of the timestamp range (inclusive).

        This method reads the log file from the end to the beginning, processing
        each line in reverse order. It decodes each line, parses it as JSON, and
        checks if the event's timestamp falls within the specified range.
        """
        with open(self.file_path, "rb") as f:
            # Move the file pointer to the end of the file
            f.seek(0, os.SEEK_END)
            buffer = b''  # Buffer to store the current line in reverse
            pointer = f.tell()  # Get the current position of the file pointer

            while pointer > 0:
                pointer -= 1  # Move the pointer one byte backward
                f.seek(pointer)  # Set the file pointer to the new position
                byte = f.read(1)  # Read a single byte

                if byte == b'\n':  # Check if the byte is a newline character
                    if buffer:  # If the buffer contains data, process it
                        try:
                            # Reverse the buffer, decode it, and parse it as JSON
                            line = buffer[::-1].decode()
                            event = json.loads(line)
                            # Yield the event if it falls within the timestamp range
                            if self._is_in_range(event, start_time, end_time):
                                yield event
                        except Exception:
                            # Ignore any errors during decoding or parsing
                            pass
                        buffer = b''  # Reset the buffer for the next line
                else:
                    # Append the byte to the buffer (building the line in reverse)
                    buffer += byte

            if buffer:  # Process the last line if the buffer is not empty
                try:
                    # Reverse the buffer, decode it, and parse it as JSON
                    line = buffer[::-1].decode()
                    event = json.loads(line)
                    # Yield the event if it falls within the timestamp range
                    if self._is_in_range(event, start_time, end_time):
                        yield event
                except Exception:
                    # Ignore any errors during decoding or parsing
                    pass

    def _is_in_range(self, event, start, end):
        ts = event.get("timestamp")  # Extract the timestamp from the event
        return ts is not None and is_in_range(ts, start, end)  # Check the range
