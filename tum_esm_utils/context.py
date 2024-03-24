"""Context managers for common tasks.

Implements: `ensure_section_duration`, `set_alarm`, `clear_alarm`.

All functions in this module are deprecated and will be removed in the
next breaking release. Use the functions from the `timing` module instead."""

from typing import Generator
from typing_extensions import deprecated
import contextlib
from . import timing


@deprecated(
    "Will be removed in the next breaking release. Use `timing.ensure_section_duration` instead."
)
@contextlib.contextmanager
def ensure_section_duration(duration: float) -> Generator[None, None, None]:
    """Make sure that the duration of the section is at least the given duration.

    Usage example - do one measurement every 6 seconds:

    ```python
    with ensure_section_duration(6):
        do_measurement()
    ```
    """

    with timing.ensure_section_duration(duration):
        yield


@deprecated(
    "Will be removed in the next breaking release. Use `timing.set_alarm` instead."
)
def set_alarm(timeout: int, label: str) -> None:
    """Set an alarm that will raise a `TimeoutError` after
    `timeout` seconds. The message will be formatted as
    `{label} took too long (timed out after {timeout} seconds)`."""

    timing.set_alarm(timeout, label)


@deprecated(
    "Will be removed in the next breaking release. Use `timing.clear_alarm` instead."
)
def clear_alarm() -> None:
    """Clear the alarm set by `set_alarm`."""

    timing.clear_alarm()
