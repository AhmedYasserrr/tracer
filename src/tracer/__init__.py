"""
Tracer package for system activity monitoring and logging.

This package provides functionality for tracing and logging system activities,
with components for configuration, command parsing, and core tracing operations.
"""

from .config import LogDomain, get_log_file
from .cli.command_parser import CommandParser
from .tracer_core import TracerCore

__all__ = [
    "LogDomain",
    "get_log_file",
    "CommandParser",
    "TracerCore",
]

__version__ = "0.1.0"
