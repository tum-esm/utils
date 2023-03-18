import psutil
from datetime import datetime


def get_cpu_usage() -> list[float]:
    """returns cpu_percent for all cores -> list [cpu1%, cpu2%,...]"""
    return psutil.cpu_percent(interval=1, percpu=True)  # type: ignore


def get_memory_usage() -> float:
    """returns -> tuple (total, available, percent, used, free, active, inactive,
    buffers, cached, shared, slab)
    """
    v_memory = psutil.virtual_memory()
    return v_memory.percent


def get_disk_space() -> float:
    """Returns disk space used in % as float.
    -> tuple (total, used, free, percent)"""
    disk = psutil.disk_usage("/")
    return disk.percent


def get_system_battery() -> int:
    """
    Returns system battery in percent as an integer (1-100).
    Returns 100 if device has no battery.
    """
    battery_state: psutil.sbattery | None = psutil.sensors_battery()  # type:ignore
    if battery_state is not None:
        return battery_state.percent  # type:ignore
    return 100


def get_last_boot_time() -> str:
    """Returns last OS boot time."""
    return datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")


def get_utc_offset() -> float:
    """Returns the UTC offset of the system"""
    return round((datetime.now() - datetime.utcnow()).total_seconds() / 3600, 1)
