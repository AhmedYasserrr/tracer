from abc import ABC, abstractmethod
from typing import Dict, Any, Type
from tracer.db.connection import SessionLocal


class BaseCRUD(ABC):
    """Abstract base class for CRUD operations"""

    def __enter__(self):
        self.session = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    @property
    @abstractmethod
    def model_class(self) -> Type:
        """Return the SQLAlchemy model class for this CRUD"""
        pass

    @abstractmethod
    def add(self, event_details: Dict[str, Any]):
        """
        Add a new entry to the database

        Args:
            event_details: Dictionary containing the event data

        Returns:
            The created entry
        """
        pass

    @abstractmethod
    def get_by_id(self, entry_id: int):
        """
        Get an entry by ID

        Args:
            entry_id: The ID of the entry

        Returns:
            The entry or None if not found
        """
        pass

    @abstractmethod
    def update(self, entry_id: int, update_data: Dict[str, Any]):
        """
        Update an entry

        Args:
            entry_id: The ID of the entry to update
            update_data: Dictionary containing fields to update

        Returns:
            Updated entry or None if not found
        """
        pass

    @abstractmethod
    def delete(self, entry_id: int) -> bool:
        """
        Delete an entry

        Args:
            entry_id: The ID of the entry to delete

        Returns:
            True if deleted, False if not found
        """
        pass
