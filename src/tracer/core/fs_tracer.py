from tracer.core.base_tracer import BaseTracer
from tracer.store.log_writer import LogWriter
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
import os
import time


class WatchdogEventHandler(FileSystemEventHandler):
    def __init__(self, writer: LogWriter, log_file: str):
        self.writer = writer
        self.log_file = os.path.abspath(log_file)

    def dispatch(self, event: FileSystemEvent):
        full_path = os.path.abspath(event.src_path)
        if full_path == self.log_file:
            return  # Skip events on the log file

        event_details = {
            "event_type": event.event_type,
            "is_directory": event.is_directory,
            "full_path": full_path,
            "name": os.path.basename(full_path),
            "path": os.path.dirname(full_path),
        }

        print(event_details)
        self.writer.append(event_details)


class FileTracer(BaseTracer):
    def __init__(self, writer: LogWriter, dir_to_watch: str):
        """
        Initialize the FileTracer.

        Args:
            writer (LogWriter): The log writer instance for appending events.
            dir_to_watch (str): The directory to monitor.
        """
        super().__init__(writer)
        self.dir_to_watch = dir_to_watch
        self.log_file = self.writer.file_path
        self.event_handler = WatchdogEventHandler(writer, self.log_file)
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
            self.cleanup()

    def cleanup(self):
        """
        Clean up resources and stop the observer.
        """
        self.observer.stop()
        self.observer.join()
        print("Cleaned up observer.")
