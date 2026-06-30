"""Client-side date-range filtering (platform-agnostic).

Reused from douyin-scraper. Xiaohongshu's web API has no native arbitrary-window
parameter, so an inclusive ``YYYY-MM-DD`` window is applied locally against each
note's create timestamp (epoch seconds).

NOTE: Douyin's server-side ``publish_time`` presets (0/1/7/182) do NOT apply to
Xiaohongshu and have been removed here.
"""
import time
from datetime import datetime, timedelta
from typing import Optional, Tuple


def parse_date_to_epoch(date_str: str, end_of_day: bool = False) -> int:
    """Parse 'YYYY-MM-DD' (or 'YYYY/MM/DD') into local-time epoch seconds.

    When ``end_of_day`` is True, return 23:59:59 of that day so the bound is
    inclusive. Raises ``ValueError`` on malformed input.
    """
    cleaned = date_str.strip().replace("/", "-")
    dt = datetime.strptime(cleaned, "%Y-%m-%d")
    if end_of_day:
        dt = dt + timedelta(days=1) - timedelta(seconds=1)
    return int(time.mktime(dt.timetuple()))


def date_bounds(
    start_date: Optional[str], end_date: Optional[str]
) -> Tuple[Optional[int], Optional[int]]:
    """Convert optional start/end date strings into (start_ts, end_ts) epoch
    bounds. Either element is None when its date is not provided. Raises
    ``ValueError`` if the dates are malformed or start is after end."""
    start_ts = parse_date_to_epoch(start_date) if start_date else None
    end_ts = parse_date_to_epoch(end_date, end_of_day=True) if end_date else None
    if start_ts is not None and end_ts is not None and start_ts > end_ts:
        raise ValueError(f"start_date ({start_date}) is after end_date ({end_date})")
    return start_ts, end_ts


def in_date_range(create_ts, start_ts: Optional[int], end_ts: Optional[int]) -> bool:
    """True if ``create_ts`` (epoch seconds) is within [start_ts, end_ts].

    When no bound is set every note passes. A note with no usable timestamp is
    dropped only when a bound is active, since it cannot be verified.
    """
    if start_ts is None and end_ts is None:
        return True
    try:
        create_ts = int(create_ts)
    except (TypeError, ValueError):
        return False
    if create_ts <= 0:
        return False
    if start_ts is not None and create_ts < start_ts:
        return False
    if end_ts is not None and create_ts > end_ts:
        return False
    return True
