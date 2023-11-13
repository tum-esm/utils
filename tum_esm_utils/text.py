"""Functions used for text manipulation/processing.

Implements: `get_random_string`, `pad_string`, `is_date_string`,
`date_range`, `is_datetime_string`, `is_rfc3339_datetime_string`,
`date_is_too_recent`, `insert_replacements`."""

from __future__ import annotations
from typing import Literal
import re
import datetime
import random
import string
import warnings


def get_random_string(length: int, forbidden: list[str] = []) -> str:
    """Return a random string from lowercase letter, the strings
    from the list passed as `forbidden` will not be generated"""
    output: str = ""
    while True:
        output = "".join(random.choices(string.ascii_lowercase, k=length))
        if output not in forbidden:
            break
    return output


def pad_string(
    text: str,
    min_width: int,
    pad_position: Literal["left", "right"] = "left",
    fill_char: Literal["0", " ", "-", "_"] = " ",
) -> str:
    if len(text) >= min_width:
        return text
    else:
        pad = fill_char * (min_width - len(text))
        return (pad + text) if (pad_position == "left") else (text + pad)


def is_date_string(date_string: str) -> bool:
    """Returns `True` if string is in a valid `YYYYMMDD` format"""
    try:
        datetime.datetime.strptime(date_string, "%Y%m%d")
        return True
    except ValueError:
        return False


def date_range(from_date_string: str, to_date_string: str) -> list[str]:
    """Returns a list of dates between `from_date_string` and `to_date_string`.

    Example:

    ```python
    date_range("20210101", "20210103") == ["20210101", "20210102", "20210103"]
    ```
    """

    assert is_date_string(
        from_date_string
    ), "from_date_string is not a valid date"
    assert is_date_string(to_date_string), "to_date_string is not a valid date"
    assert (
        from_date_string <= to_date_string
    ), "from_date_string cannot be after to_date_string"

    output = []
    for date in range(int(from_date_string), int(to_date_string) + 1):
        if is_date_string(str(date)):
            output.append(str(date))
    return output


def is_datetime_string(datetime_string: str) -> bool:
    """Returns `True` if string is in a valid `YYYYMMDD HH:mm:ss` format"""

    warnings.warn(
        "Use `is_rfc3339_datetime_string` instead", DeprecationWarning
    )
    try:
        datetime.datetime.strptime(datetime_string, "%Y%m%d %H:%M:%S")
        return True
    except ValueError:
        return False


def is_rfc3339_datetime_string(rfc3339_datetime_string: str) -> bool:
    """Returns `True` if string is in a valid `YYYY-MM-DDTHH:mm:ssZ` (RFC3339)
    format. Caution: The appendix of `+00:00` is required for UTC!"""
    try:
        assert re.match(
            r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\+|\-)\d{2}:\d{2}$",
            rfc3339_datetime_string,
        )
        datetime.datetime.fromisoformat(rfc3339_datetime_string)
        return True
    except (ValueError, AssertionError):
        return False


def date_is_too_recent(
    date_string: str,
    min_days_delay: int = 1,
) -> bool:
    """A min delay of two days means 20220101 will be too recent
    any time before 20220103 00:00 (start of day)"""
    date_object = datetime.datetime.strptime(
        date_string, "%Y%m%d"
    )  # will have the time 00:00:00
    return (datetime.datetime.now() - date_object).days >= min_days_delay


def insert_replacements(content: str, replacements: dict[str, str]) -> str:
    """For every key in replacements, replaces `%key$` in the
    content with its value."""

    for key, value in replacements.items():
        content = content.replace(f"%{key}%", value)
    return content
