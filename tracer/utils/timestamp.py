from datetime import datetime, timedelta, timezone
import re
from typing import Optional, Union

# ========== Helpers ==========

def now_iso() -> str:
    """Returns current time in ISO format (UTC)."""
    return datetime.now(tz=timezone.utc).isoformat()

def parse_iso(ts: str) -> datetime:
    """Parses ISO 8601 string or fuzzy time like '5m ago', 'yesterday'."""
    ts = ts.strip().lower()

    # Handle fuzzy inputs like '5m ago', '2h ago', etc.
    match = re.match(r"(\d+)([smhd])\s*ago", ts)
    if match:
        num, unit = match.groups()
        delta = _get_timedelta(int(num), unit)
        return datetime.now(tz=timezone.utc) - delta

    if ts == "now":
        return datetime.now(tz=timezone.utc)

    if ts == "yesterday":
        return datetime.now(tz=timezone.utc) - timedelta(days=1)

    # Fall back to ISO format
    try:
        return datetime.fromisoformat(ts)  # No change needed here, still valid.
    except ValueError:
        raise ValueError(f"Invalid timestamp format: {ts}")

def is_in_range(ts: Union[str, datetime], start: Optional[str], end: Optional[str]) -> bool:
    """Checks if a timestamp is in a given range (start and end optional)."""
    if isinstance(ts, str):
        ts = parse_iso(ts)
    if start and ts < parse_iso(start):
        return False
    if end and ts > parse_iso(end):
        return False
    return True

# ========== Internal ==========

def _get_timedelta(num: int, unit: str) -> timedelta:
    """Helper to convert unit shorthand to timedelta."""
    if unit == "s":
        return timedelta(seconds=num)
    elif unit == "m":
        return timedelta(minutes=num)
    elif unit == "h":
        return timedelta(hours=num)
    elif unit == "d":
        return timedelta(days=num)
    raise ValueError(f"Unknown time unit: {unit}")
