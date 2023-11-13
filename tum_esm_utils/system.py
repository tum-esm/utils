"""Common system status related functions.

Implements: `get_cpu_usage`, `get_memory_usage`, `get_disk_space`,
`get_system_battery`, `get_last_boot_time`, `get_utc_offset`"""

from __future__ import annotations
from typing import Any
import psutil
import datetime


def get_cpu_usage() -> list[float]:
    """Returns cpu_percent for all cores as `list[cpu1%, cpu2%,...]`"""
    return psutil.cpu_percent(interval=1, percpu=True)


def get_memory_usage() -> float:
    """Returns the memory usage in %"""
    p = psutil.virtual_memory().percent
    assert isinstance(p, float)
    return p


def get_disk_space() -> float:
    """Returns disk space used in % as float"""
    return psutil.disk_usage("/").percent


def get_system_battery() -> int:
    """Returns system battery in percent in percent.
    Returns 100 if device has no battery."""

    # FIXME: In the next breaking release, return None if device has no battery

    battery_state: Any = psutil.sensors_battery()  # type: ignore
    try:
        assert battery_state is not None
        percent = battery_state.percent
        assert isinstance(percent, int)
        assert 1 <= percent <= 100
        return percent
    except AssertionError:
        return 100


def get_last_boot_time() -> str:
    """Returns last OS boot time."""

    # FIXME: In the next breaking release, convert this to a return a datetime

    return datetime.datetime.fromtimestamp(psutil.boot_time()
                                          ).strftime("%Y-%m-%d %H:%M:%S")


def get_utc_offset() -> float:
    """Returns the UTC offset of the system.

    ```python
    x = get_utc_offset()
    local time == utc time + x
    ```
    """
    return round((datetime.datetime.now() -
                  datetime.datetime.utcnow()).total_seconds() / 3600, 1)
