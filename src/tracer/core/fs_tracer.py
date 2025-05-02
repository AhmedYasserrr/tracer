from tracer.core.base_tracer import BaseTracer
from tracer.store.log_writer import LogWriter
import os
from inotify_simple import INotify, flags

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
        self.inotify = INotify()
        self.watch_descriptors = {}

    def add_watch_recursive(self, path: str, watch_flags: int):
        """
        Add inotify watches to a directory and its subdirectories.

        Args:
            path (str): The root directory to watch.
            watch_flags (int): The inotify flags to monitor.

        Returns:
            dict: A mapping of watch descriptors to directory paths.
        """
        watch_descriptors = {}
        log_file_parent = os.path.dirname(os.path.abspath(self.log_file))
        
        for root, dirs, files in os.walk(path):
            if os.path.abspath(root) == log_file_parent:
                continue
            try:
                wd = self.inotify.add_watch(root, watch_flags)
                watch_descriptors[wd] = root
                print(f"Added watch to: {root}")
            except Exception as e:
                print(f"Failed to add watch to {root}: {e}")
        return watch_descriptors
    
    def handle_event(self, event, watch_flags):
        """
        Handle a single inotify event.

        Args:
            event: The inotify event.
            watch_flags: The flags being monitored.
        """
        path = self.watch_descriptors.get(event.wd, "Unknown")
        event_flags = flags.from_mask(event.mask)
        event_name = event.name if event.name else "<root>"
        full_path = os.path.join(path, event_name)

        # Skip events on the log file
        if os.path.abspath(full_path) == self.log_file:
            return

        event_details = {
            "event_flags": [flag.name for flag in event_flags],
            "path": path,
            "name": event_name,
            "full_path": full_path,
        }

        print(event_details)
        self.writer.append(event_details)

        # Handle new subdirectory creation
        if flags.CREATE in event_flags and os.path.isdir(full_path):
            try:
                new_wd = self.inotify.add_watch(full_path, watch_flags)
                self.watch_descriptors[new_wd] = full_path
                print(f"Added watch for new directory: {full_path}")
            except Exception as e:
                print(f"Failed to add watch for new directory {full_path}: {e}")


    def start(self):
        """
        Start monitoring the directory and its subdirectories.
        """
        if not self.dir_to_watch:
            raise ValueError("No directory specified to watch.")

        # Define the flags to watch for
        watch_flags = flags.CREATE | flags.DELETE | flags.MODIFY | flags.ATTRIB | flags.CLOSE_WRITE

        # Add recursive watches
        self.watch_descriptors = self.add_watch_recursive(self.dir_to_watch, watch_flags)
        print(f"Started monitoring: {self.dir_to_watch} (and subdirectories)")

        try:
            while True:
                for event in self.inotify.read():
                    self.handle_event(event, watch_flags)
        except KeyboardInterrupt:
            print("Stopping monitoring...")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """
        Clean up resources and remove all watches.
        """
        for wd in list(self.watch_descriptors.keys()):
            try:
                self.inotify.rm_watch(wd)
            except Exception as e:
                print(f"Failed to remove watch for {self.watch_descriptors[wd]}: {e}")
        print("Cleaned up all watches.")