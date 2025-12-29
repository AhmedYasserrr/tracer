from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
import os
import time
from tracer.core import BaseTracer
from tracer.store import LogWriter
from tracer import LogDomain


class WatchdogEventHandler(FileSystemEventHandler):
    def __init__(self, writer: LogWriter, log_file: str):
        self.writer = writer
        self.log_file = os.path.abspath(log_file)

    def dispatch(self, event: FileSystemEvent):
        full_path = os.path.abspath(event.src_path)
        if full_path == self.log_file:
            return  # Skip events on the log file

        event_details = {
            "event": event.event_type,
            "name": os.path.basename(full_path),
            "is_directory": event.is_directory,
            "full_path": full_path,
        }

        print(event_details)
        self.writer.append(event_details)


class FileTracer(BaseTracer):
    def __init__(self, domain: LogDomain, dir_to_watch: str):
        """
        Initialize the FileTracer.

        Args:
            writer (LogWriter): The log writer instance for appending events.
            dir_to_watch (str): The directory to monitor.
        """
        super().__init__(domain)
        self.dir_to_watch = dir_to_watch
        self.log_file = self.writer.file_path
        self.event_handler = WatchdogEventHandler(self.writer, self.log_file)
        self.observer = Observer()

    def start(self):
        """
        Start monitoring the directory and its subdirectories.
        """
        if not self.dir_to_watch:
            raise ValueError("No directory specified to watch.")

        self.observer.schedule(self.event_handler, self.dir_to_watch, recursive=True)
        self.observer.start()
        print(f"Started monitoring: {self.dir_to_watch} (and subdirectories)")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Stopping monitoring...")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.stop()

    def stop(self):
        """
        Clean up resources and stop the observer.
        """
        self.observer.stop()
        self.observer.join()
        print("Cleaned up observer.")
