import contextlib
import datetime
import signal
import time
from typing import Any, Generator, List


def date_range(
    from_date: datetime.date,
    to_date: datetime.date,
) -> List[datetime.date]:
    """Returns a list of dates between from_date and to_date (inclusive)."""
    delta = to_date - from_date
    assert delta.days >= 0, "from_date must be before to_date"
    return [
        from_date + datetime.timedelta(days=i) for i in range(delta.days + 1)
    ]


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
