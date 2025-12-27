from typing import Optional, List, Dict, Any, Type
from datetime import datetime
from tracer.db.models import FileLog
from tracer.db.connection import SessionLocal


class FileCRUD:
    """CRUD operations for FileLog (file_system table)"""

    def __enter__(self):
        self.session = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    @property
    def model_class(self) -> Type[FileLog]:
        return FileLog

    def add(self, event_details: Dict[str, Any]) -> FileLog:
        """
        Add a new file system event to the database

        Args:
            event_details: Dictionary containing:
                - event: str - The event type
                - name: str - The file/directory name
                - is_directory: bool - Whether it's a directory
                - full_path: str - The full path
                - timestamp: datetime (optional) - Event timestamp

        Returns:
            FileLog: The created file log entry
        """
        try:
            # Add timestamp if not provided
            if "timestamp" not in event_details:
                event_details["timestamp"] = datetime.utcnow()

            file_log = FileLog(**event_details)
            self.session.add(file_log)
            self.session.commit()
            self.session.refresh(file_log)
            return file_log

        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, log_id: int) -> Optional[FileLog]:
        """
        Get a file log entry by ID

        Args:
            log_id: The ID of the log entry

        Returns:
            FileLog or None if not found
        """
        return self.session.query(FileLog).filter(FileLog.id == log_id).first()

    def get_by_path(self, full_path: str) -> List[FileLog]:
        """
        Get all file log entries for a specific path

        Args:
            full_path: The full path to search for

        Returns:
            List of FileLog entries
        """
        return self.session.query(FileLog).filter(FileLog.full_path == full_path).all()

    def get_by_event_type(self, event_type: str) -> List[FileLog]:
        """
        Get all file log entries for a specific event type

        Args:
            event_type: The event type to search for

        Returns:
            List of FileLog entries
        """
        return self.session.query(FileLog).filter(FileLog.event == event_type).all()

    def get_entries_by_date_range(
        self, start_date: datetime, end_date: datetime
    ) -> List[FileLog]:
        """
        Get file log entries within a date range

        Args:
            start_date: Start of the date range
            end_date: End of the date range

        Returns:
            List of FileLog entries within the date range
        """
        return (
            self.session.query(FileLog)
            .filter(FileLog.timestamp >= start_date)
            .filter(FileLog.timestamp <= end_date)
            .order_by(FileLog.timestamp.desc())
            .all()
        )

    def update(self, log_id: int, update_data: Dict[str, Any]) -> Optional[FileLog]:
        """
        Update a file log entry

        Args:
            log_id: The ID of the log entry to update
            update_data: Dictionary containing fields to update

        Returns:
            Updated FileLog entry or None if not found
        """
        try:
            file_log = self.session.query(FileLog).filter(FileLog.id == log_id).first()
            if not file_log:
                return None

            # Update only provided fields
            for key, value in update_data.items():
                if hasattr(file_log, key):
                    setattr(file_log, key, value)

            self.session.commit()
            self.session.refresh(file_log)
            return file_log

        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, log_id: int) -> bool:
        """
        Delete a file log entry

        Args:
            log_id: The ID of the log entry to delete

        Returns:
            True if deleted, False if not found
        """
        try:
            file_log = self.session.query(FileLog).filter(FileLog.id == log_id).first()
            if not file_log:
                return False

            self.session.delete(file_log)
            self.session.commit()
            return True

        except Exception as e:
            self.session.rollback()
            raise e

    def delete_by_path(self, full_path: str) -> int:
        """
        Delete all file log entries for a specific path

        Args:
            full_path: The full path to delete entries for

        Returns:
            Number of deleted entries
        """
        try:
            count = (
                self.session.query(FileLog)
                .filter(FileLog.full_path == full_path)
                .count()
            )
            self.session.query(FileLog).filter(FileLog.full_path == full_path).delete()
            self.session.commit()
            return count

        except Exception as e:
            self.session.rollback()
            raise e
