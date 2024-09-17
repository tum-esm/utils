"""Functions used for timing or time calculations.

Implements: `date_range`, `ensure_section_duration`, `set_alarm`,
`clear_alarm`, `wait_for_condition`"""

from typing import Any, Callable, Generator, Optional
import contextlib
import datetime
import re
import signal
import time
import pytz


def date_range(
    from_date: datetime.date,
    to_date: datetime.date,
) -> list[datetime.date]:
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


_ISO_8601_PATTERN_1 = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?$"
)
_ISO_8601_PATTERN_2 = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$"
)
_ISO_8601_PATTERN_3 = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(\+|-)\d{2}:\d{2}$"
)
_ISO_8601_PATTERN_4 = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(\+|-)\d{4}$"
)
_ISO_8601_PATTERN_5 = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(\+|-)\d{2}$"
)


def parse_iso_8601_datetime(s: str) -> datetime.datetime:
    """Parse a datetime string from various formats and return a datetime object.
    
    ISO 8601 supports time zones as `<time>Z`, `<time>±hh:mm`, `<time>±hhmm` and
    `<time>±hh`. However, only the second format is supported by `datetime.datetime.fromisoformat()`
    (`HH[:MM[:SS[.fff[fff]]]][+HH:MM[:SS[.ffffff]]]`).
    
    This function supports parsing alll ISO 8601 time formats."""

    if _ISO_8601_PATTERN_1.match(s) is not None:
        return datetime.datetime.fromisoformat(s)
    elif _ISO_8601_PATTERN_2.match(s) is not None:
        return datetime.datetime.fromisoformat(s[:-1] + "+00:00")
    elif _ISO_8601_PATTERN_3.match(s) is not None:
        return datetime.datetime.fromisoformat(s)
    elif _ISO_8601_PATTERN_4.match(s) is not None:
        return datetime.datetime.fromisoformat(s[:-2] + ":" + s[-2 :])
    elif _ISO_8601_PATTERN_5.match(s) is not None:
        return datetime.datetime.fromisoformat(s + ":00")
    else:
        raise ValueError(f"Invalid datetime string: {s}")


def datetime_span_intersection(
    dt_span_1: tuple[datetime.datetime, datetime.datetime],
    dt_span_2: tuple[datetime.datetime, datetime.datetime],
) -> Optional[tuple[datetime.datetime, datetime.datetime]]:
    """Check if two datetime spans overlap.
    
    Args:
        dt_span_1: The first datetime span (start, end).
        dt_span_2: The second datetime span (start, end).
    
    Returns:
        The intersection of the two datetime spans or None if they do
        not overlap. Returns None if the intersection is a single point.
    """

    if dt_span_1[0] > dt_span_1[1]:
        raise ValueError("Invalid dt_span_1: start time is after end time")
    if dt_span_2[0] > dt_span_2[1]:
        raise ValueError("Invalid dt_span_2: start time is after end time")

    if dt_span_1[0] >= dt_span_2[1]:
        return None

    if dt_span_1[1] <= dt_span_2[0]:
        return None

    min_start = max(dt_span_1[0], dt_span_2[0])
    max_end = min(dt_span_1[1], dt_span_2[1])
    if min_start == max_end:
        return None
    return (min_start, max_end)


def date_span_intersection(
    d_span_1: tuple[datetime.date, datetime.date],
    d_span_2: tuple[datetime.date, datetime.date],
) -> Optional[tuple[datetime.date, datetime.date]]:
    """Check if two date spans overlap. This functions behaves
    differently from `datetime_span_intersection` in that it
    returns a single point as an intersection if the two date
    spans overlap at a single date.
    
    Args:
        d_span_1: The first date span (start, end).
        d_span_2: The second date span (start, end).
    
    Returns:
        The intersection of the two date spans or None if they do
        not overlap.
    """

    dt_intersection = datetime_span_intersection(
        (
            datetime.datetime.combine(d_span_1[0], datetime.time.min),
            datetime.datetime.combine(d_span_1[1], datetime.time.max)
        ),
        (
            datetime.datetime.combine(d_span_2[0], datetime.time.min),
            datetime.datetime.combine(d_span_2[1], datetime.time.max),
        ),
    )
    if dt_intersection is None:
        return None
    return (dt_intersection[0].date(), dt_intersection[1].date())
