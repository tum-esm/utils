"""Context managers for common tasks.

Implements: `ensure_section_duration`, `set_alarm`, `clear_alarm`."""

from typing import Generator
import contextlib
import warnings
from . import timing


@contextlib.contextmanager
def ensure_section_duration(duration: float) -> Generator[None, None, None]:
    """Make sure that the duration of the section is at least the given duration.

    Usage example - do one measurement every 6 seconds:

    ```python
    with ensure_section_duration(6):
        do_measurement()
    ```
    """

    warnings.warn(
        "`context.ensure_section_duration` is deprecated, " +
        "use `timing.ensure_section_duration` instead",
        DeprecationWarning,
    )
    with timing.ensure_section_duration(duration):
        yield


def set_alarm(timeout: int, label: str) -> None:
    """Set an alarm that will raise a `TimeoutError` after
    `timeout` seconds. The message will be formatted as
    `{label} took too long (timed out after {timeout} seconds)`."""

    warnings.warn(
        "`context.set_alarm` is deprecated, " +
        "use `timing.set_alarm` instead",
        DeprecationWarning,
    )
    timing.set_alarm(timeout, label)


def clear_alarm() -> None:
    """Clear the alarm set by `set_alarm`."""

    warnings.warn(
        "`context.clear_alarm` is deprecated, " +
        "use `timing.clear_alarm` instead",
        DeprecationWarning,
    )
    timing.clear_alarm()
