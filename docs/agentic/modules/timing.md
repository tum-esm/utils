# `tum_esm_utils.timing` API Reference


Functions used for timing or time calculations.

Implements: `date_range`, `ensure_section_duration`, `set_alarm`,
`clear_alarm`, `wait_for_condition`, `ExponentialBackoff`


##### `date_range`

```python
def date_range(from_date: datetime.date,
               to_date: datetime.date) -> list[datetime.date]
```

Returns a list of dates between from_date and to_date (inclusive).


##### `time_range`

```python
def time_range(from_time: datetime.time, to_time: datetime.time,
               time_step: datetime.timedelta) -> list[datetime.time]
```

Returns a list of times between from_time and to_time (inclusive).


##### `datetime_range`

```python
def datetime_range(from_dt: datetime.datetime, to_dt: datetime.datetime,
                   time_step: datetime.timedelta) -> list[datetime.datetime]
```

Returns a list of datetimes between from_dt and to_dt (inclusive).


##### `ensure_section_duration`

```python
@contextlib.contextmanager
def ensure_section_duration(duration: float) -> Generator[None, None, None]
```

Make sure that the duration of the section is at least the given duration.

Usage example - do one measurement every 6 seconds:

```python
with ensure_section_duration(6):
    do_measurement()
```


##### `set_alarm`

```python
def set_alarm(timeout: int, label: str) -> None
```

Set an alarm that will raise a `TimeoutError` after
`timeout` seconds. The message will be formatted as
`{label} took too long (timed out after {timeout} seconds)`.


##### `clear_alarm`

```python
def clear_alarm() -> None
```

Clear the alarm set by `set_alarm`.


##### `parse_timezone_string`

```python
def parse_timezone_string(timezone_string: str,
                          dt: Optional[datetime.datetime] = None) -> float
```

Parse a timezone string and return the offset in hours.

Why does this function exist? The `strptime` function cannot parse strings
other than "±HHMM". This function can also parse strings in the format "±H"
("+2", "-3", "+5.5"), and "±HH:MM".

**Examples**:

  
```python
parse_timezone_string("GMT")        # returns 0
parse_timezone_string("GMT+2")      # returns 2
parse_timezone_string("UTC+2.0")    # returns 2
parse_timezone_string("UTC-02:00")  # returns -2
```
  
  You are required to pass a datetime object in case the utc offset for the
  passed timezone is not constant - e.g. for "Europe/Berlin".


##### `wait_for_condition`

```python
def wait_for_condition(is_successful: Callable[[], bool],
                       timeout_message: str,
                       timeout_seconds: float = 5,
                       check_interval_seconds: float = 0.25) -> float
```

Wait for the given condition to be true, or raise a TimeoutError
if the condition is not met within the given timeout. The condition
is passed as a function that will be called periodically.

**Arguments**:

- `is_successful` - A function that returns True if the condition is met.
- `timeout_message` - The message to include in the TimeoutError.
- `timeout_seconds` - The maximum time to wait for the condition to be met.
- `check_interval_seconds` - How long to wait inbetween `is_successful()` calls.
  
- `Returns` - The time it took for the condition to be met in seconds.


##### `parse_iso_8601_datetime`

```python
def parse_iso_8601_datetime(s: str) -> datetime.datetime
```

Parse a datetime string from various formats and return a datetime object.

ISO 8601 supports time zones as `<time>Z`, `<time>±hh:mm`, `<time>±hhmm` and
`<time>±hh`. However, only the second format is supported by `datetime.datetime.fromisoformat()`
(`HH[:MM[:SS[.fff[fff]]]][+HH:MM[:SS[.ffffff]]]`).

This function supports parsing alll ISO 8601 time formats.


##### `datetime_span_intersection`

```python
def datetime_span_intersection(
    dt_span_1: tuple[datetime.datetime,
                     datetime.datetime], dt_span_2: tuple[datetime.datetime,
                                                          datetime.datetime]
) -> Optional[tuple[datetime.datetime, datetime.datetime]]
```

Check if two datetime spans overlap.

**Arguments**:

- `dt_span_1` - The first datetime span (start, end).
- `dt_span_2` - The second datetime span (start, end).
  

**Returns**:

  The intersection of the two datetime spans or None if they do
  not overlap. Returns None if the intersection is a single point.


##### `date_span_intersection`

```python
def date_span_intersection(
    d_span_1: tuple[datetime.date,
                    datetime.date], d_span_2: tuple[datetime.date,
                                                    datetime.date]
) -> Optional[tuple[datetime.date, datetime.date]]
```

Check if two date spans overlap. This functions behaves
differently from `datetime_span_intersection` in that it
returns a single point as an intersection if the two date
spans overlap at a single date.

**Arguments**:

- `d_span_1` - The first date span (start, end).
- `d_span_2` - The second date span (start, end).
  

**Returns**:

  The intersection of the two date spans or None if they do
  not overlap.


### `ExponentialBackoff` Objects

```python
class ExponentialBackoff()
```

Exponential backoff e.g. when errors occur. First try again in 1 minute,
then 4 minutes, then 15 minutes, etc.. Usage:

```python
exponential_backoff = ExponentialBackoff(
    log_info=logger.info, buckets= [60, 240, 900, 3600, 14400]
)

while True:
    try:
        # do something that might fail
        exponential_backoff.reset()
    except Exception as e:
        logger.exception(e)
        exponential_backoff.sleep()
```


##### `__init__`

```python
def __init__(log_info: Optional[Callable[[str], None]] = None,
             buckets: list[int] = [60, 240, 900, 3600, 14400]) -> None
```

Create a new exponential backoff object.

**Arguments**:

- `log_info` - The function to call when logging information.
- `buckets` - The buckets to use for the exponential backoff.


##### `sleep`

```python
def sleep(max_sleep_time: Optional[float] = None) -> float
```

Wait and increase the wait time to the next bucket.

**Arguments**:

- `max_sleep_time` - The maximum time to sleep. If None, no maximum is set.
  

**Returns**:

  The amount of seconds waited.


##### `reset`

```python
def reset() -> None
```

Reset the waiting period to the first bucket


##### `timed_section`

```python
@contextlib.contextmanager
def timed_section(label: str) -> Generator[None, None, None]
```

Time a section of code and print the duration.
Usage example:

```python
with timed_section("my_section"):
    do_something()
```


##### `datetime_to_julian_day_number`

```python
def datetime_to_julian_day_number(
        dt: datetime.datetime, variant: Literal["JDN", "MJD",
                                                "MJD2K"]) -> float
```

Convert a datetime to a Julian Day Number (JDN) or MJD/MJD2K.

The Julian Day Number (JDN) is the continuous count of days since the beginning
of the Julian Period on January 1, 4713 BC. THe modified variant MJD starts
counting from November 17, 1858 at 00:00:00 UTC, and MJD2K starts counting
from January 1, 2000 at 00:00:00 UTC.

**Arguments**:

- `dt` - The datetime to convert.
- `variant` - The variant of the Julian Day Number ("JDN", "MJD", "MJD2K").
  

**Returns**:

  The Julian Day Number as a float.


##### `julian_day_number_to_datetime`

```python
def julian_day_number_to_datetime(
        jdn: float, variant: Literal["JDN", "MJD",
                                     "MJD2K"]) -> datetime.datetime
```

Convert a Julian Day Number (JDN) or MJD/MJD2K to a datetime.

The Julian Day Number (JDN) is the continuous count of days since the beginning
of the Julian Period on January 1, 4713 BC. THe modified variant MJD starts
counting from November 17, 1858 at 00:00:00 UTC, and MJD2K starts counting
from January 1, 2000 at 00:00:00 UTC.

This function was validated against
https://ssd.jpl.nasa.gov/tools/jdc/#/cd

**Arguments**:

- `jdn` - The Julian Day Number to convert.
- `variant` - The variant of the Julian Day Number ("JDN", "MJD", "MJD2K").
  

**Returns**:

  The corresponding datetime.

