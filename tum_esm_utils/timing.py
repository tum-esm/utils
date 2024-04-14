"""Functions used for timing or time calculations.

Implements: `date_range`, `ensure_section_duration`, `set_alarm`,
`clear_alarm`, `wait_for_condition`"""

from typing import Any, Callable, Generator, List, Optional
import contextlib
import datetime
import re
import signal
import time
import pytz


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


def parse_timezone_string(
    timezone_string: str,
    dt: Optional[datetime.datetime] = None,
) -> float:
    """Parse a timezone string and return the offset in hours.

    Why does this function exist? The `strptime` function cannot parse strings
    other than "±HHMM". This function can also parse strings in the format "±H"
    ("+2", "-3", "+5.5"), and "±HH:MM".

    Examples:

    ```python
    parse_timezone_string("GMT")        # returns 0
    parse_timezone_string("GMT+2")      # returns 2
    parse_timezone_string("UTC+2.0")    # returns 2
    parse_timezone_string("UTC-02:00")  # returns -2
    ```

    You are required to pass a datetime object in case the utc offset for the
    passed timezone is not constant - e.g. for "Europe/Berlin"."""

    offset: float = 0
    zone_string: str

    # parse the offset string
    number_of_offset_signs = timezone_string.count("+") + timezone_string.count(
        "-"
    )
    if number_of_offset_signs == 0:
        zone_string = timezone_string
    elif number_of_offset_signs == 1:
        s2 = timezone_string.split(
            "+"
        ) if "+" in timezone_string else timezone_string.split("-")
        assert len(s2) == 2
        zone_string = s2[0]
        offset_string = s2[1]

        # parse the offset string
        if re.match(r"^\d{1,2}(\.\d{1})?$", offset_string):
            offset = float(offset_string)
        elif re.match(r"^\d{2}:\d{2}$", offset_string):
            offset = float(offset_string.split(":")[0]
                          ) + float(offset_string.split(":")[1]) / 60
        elif re.match(r"^\d{4}$", offset_string):
            offset = float(offset_string[: 2]) + float(offset_string[2 :]) / 60
        else:
            raise ValueError(f'Invalid offset string: "{offset_string}"')
        if "-" in timezone_string:
            offset = -offset
    else:
        raise ValueError(f'Invalid timezone string: "{timezone_string}"')

    # parse the time zone string
    try:
        tz = pytz.timezone(zone_string)
    except pytz.UnknownTimeZoneError:
        raise ValueError(
            f'Unknown time zone: "{zone_string}", the available time zones are: {pytz.all_timezones}'
        )
    td = tz.utcoffset(dt)
    assert td is not None, f'Zone "{zone_string}" requires a datetime object to calculate the offset.'
    offset += td.total_seconds() / 3600
    return offset


def wait_for_condition(
    is_successful: Callable[[], bool],
    timeout_message: str,
    timeout_seconds: float = 5,
    check_interval_seconds: float = 0.25,
) -> None:
    """Wait for the given condition to be true, or raise a TimeoutError
    if the condition is not met within the given timeout. The condition
    is passed as a function that will be called periodically.
    
    Args:
        is_successful:             A function that returns True if the condition is met.
        timeout_message:           The message to include in the TimeoutError.
        timeout_seconds:           The maximum time to wait for the condition to be met.
        check_interval_seconds:    How long to wait inbetween `is_successful()` calls."""

    start_time = time.time()
    while True:
        if is_successful():
            break
        if (time.time() - start_time) > timeout_seconds:
            raise TimeoutError(timeout_message)
        time.sleep(check_interval_seconds)
