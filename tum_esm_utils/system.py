"""Common system status related functions.

Implements: `get_cpu_usage`, `get_memory_usage`, `get_disk_space`,
`get_system_battery`, `get_last_boot_time`, `get_utc_offset`"""

from __future__ import annotations
from typing import Any, Optional
import time
import psutil
import datetime


def get_cpu_usage() -> list[float]:
    """Checks the CPU usage of the system.

    Returns:
        The CPU usage in percent for each core."""

    return psutil.cpu_percent(interval=1, percpu=True)


def get_memory_usage() -> float:
    """Checks the memory usage of the system.

    Returns:
        The memory usage in percent."""

    p = psutil.virtual_memory().percent
    assert isinstance(p, float)
    return p


def get_disk_space(path: str = "/") -> float:
    """Checks the disk space of a given path.

    Args:
        path: The path to check the disk space for.

    Returns:
        The available disk space in percent."""

    return psutil.disk_usage(path).percent


def get_system_battery() -> Optional[int]:
    """Checks the system battery.
    
    Returns:
        The battery state in percent if available, else None."""

    battery_state: Any = psutil.sensors_battery()  # type: ignore
    try:
        assert battery_state is not None
        percent = battery_state.percent
        assert isinstance(percent, int)
        assert 1 <= percent <= 100
        return percent
    except AssertionError:
        return None


def get_last_boot_time() -> datetime.datetime:
    """Checks the last boot time of the system."""

    return datetime.datetime.fromtimestamp(psutil.boot_time())


def get_utc_offset() -> float:
    """Returns the UTC offset of the system.

    ```python
    x = get_utc_offset()
    local time == utc time + x
    ```
    
    Credits to https://stackoverflow.com/a/35058476/8255842
    
    Returns:
        The UTC offset in hours."""

    return round((-time.timezone) / 3600, 3)
