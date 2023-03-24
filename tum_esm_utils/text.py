from datetime import datetime
import random
import string
from typing import Literal
import pendulum


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
        pendulum.from_format(date_string, "YYYYMMDD")
        return True
    except ValueError:
        return False


def is_datetime_string(datetime_string: str) -> bool:
    """Returns `True` if string is in a valid `YYYYMMDD HH:mm:ss` format"""
    try:
        pendulum.from_format(datetime_string, "YYYYMMDD HH:mm:ss")
        return True
    except ValueError:
        return False


def is_rfc3339_datetime_string(rfc3339_datetime_string: str) -> bool:
    """Returns `True` if string is in a valid `YYYY-MM-DDTHH:mm:ssZ` (RFC3339)
    format. Caution: The appendix of `+00:00` is required for UTC!"""
    try:
        pendulum.from_format(rfc3339_datetime_string, fmt="YYYY-MM-DDTHH:mm:ssZ")
        return True
    except ValueError:
        return False


def date_is_too_recent(
    date_string: str,
    min_days_delay: int = 1,
) -> bool:
    """A min delay of two days means 20220101 will be too recent
    any time before 20220103 00:00 (start of day)"""
    date_object = datetime.strptime(
        date_string, "%Y%m%d"
    )  # will have the time 00:00:00
    return (datetime.now() - date_object).days >= min_days_delay


def insert_replacements(content: str, replacements: dict[str, str]) -> str:
    """For every key in replacements, replaces `%key$` in the
    content with its value."""

    for key, value in replacements.items():
        content = content.replace(f"%{key}%", value)
    return content
