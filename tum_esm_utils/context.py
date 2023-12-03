"""Context managers for common tasks.

Implements: `ensure_section_duration`, `set_alarm`, `clear_alarm`."""

import signal
from typing import Any, Generator
import contextlib
import time


@contextlib.contextmanager
def ensure_section_duration(duration: float) -> Generator[None, None, None]:
    """Make sure that the duration of the section is at least the given duration.

    Usage example - do one measurement every 6 seconds:

    ```python
    with ensure_section_duration(6):
        do_measurement()
    ```
    """

    start_time = time.time()
    yield
    remaining_loop_time = start_time + duration - time.time()
    if remaining_loop_time > 0:
        time.sleep(remaining_loop_time)


def set_alarm(timeout: int, label: str) -> None:
    """Set an alarm that will raise a `TimeoutError` after
    `timeout` seconds. The message will be formatted as
    `{label} took too long (timed out after {timeout} seconds)`."""
    def alarm_handler(*args: Any) -> None:
        raise TimeoutError(
            f"{label} took too long (timed out after {timeout} seconds)"
        )

    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(timeout)


def clear_alarm() -> None:
    """Clear the alarm set by `set_alarm`."""

    signal.alarm(0)
