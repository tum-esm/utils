"""Functions used for text manipulation/processing.

Implements: `get_random_string`, `pad_string`, `is_date_string`,
`is_rfc3339_datetime_string`, `insert_replacements`"""

from __future__ import annotations
from typing import Literal
import re
import datetime
import random
import string


def get_random_string(length: int, forbidden: list[str] = []) -> str:
    """Return a random string from lowercase letters.
    
    Args:
        length:     The length of the random string.
        forbidden:  A list of strings that should not be generated.
    
    Returns:
        A random string."""

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
    """Pad a string with a fill character to a minimum width.

    Args:
        text:         The text to pad.
        min_width:    The minimum width of the text.
        pad_position: The position of the padding. Either "left" or "right".
        fill_char:    The character to use for padding.
    
    Returns:
        The padded string."""

    if len(text) >= min_width:
        return text
    else:
        pad = fill_char * (min_width - len(text))
        return (pad + text) if (pad_position == "left") else (text + pad)


def is_date_string(date_string: str) -> bool:
    """Returns `True` if string is in a valid `YYYYMMDD` format."""
    try:
        datetime.datetime.strptime(date_string, "%Y%m%d")
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


def insert_replacements(content: str, replacements: dict[str, str]) -> str:
    """For every key in replacements, replaces `%key%` in the
    content with its value."""

    for key, value in replacements.items():
        content = content.replace(f"%{key}%", value)
    return content
