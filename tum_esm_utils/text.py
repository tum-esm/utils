from datetime import datetime
import random
import string
from typing import Literal


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
    """Returns true if string is in `YYYYMMDD` format and date exists"""
    try:
        datetime.strptime(date_string, "%Y%m%d")
        return True
    except (AssertionError, ValueError):
        return False


def insert_replacements(content: str, replacements: dict[str, str]) -> str:
    """For every key in replacements, replaces `%key$` in the
    content with its value."""

    for key, value in replacements.items():
        content = content.replace(f"%{key}%", value)
    return content
