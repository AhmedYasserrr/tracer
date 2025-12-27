from typing import Type
from tracer.db.crud.base_crud import BaseCRUD
from tracer.db.crud.fs_crud import FileCRUD
from tracer.config import LogDomain


def get_crud_class(domain: LogDomain) -> Type[BaseCRUD]:
    """
    Factory function to get the appropriate CRUD class based on LogDomain

    Args:
        domain: The LogDomain enum value

    Returns:
        The appropriate CRUD class

    Raises:
        ValueError: If domain is not supported
    """
    if domain == LogDomain.FS:
        return FileCRUD
    else:
        raise ValueError(f"Unsupported domain: {domain}")


__all__ = ["get_crud_class", "BaseCRUD", "FileCRUD"]
