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


"""Characters replaced by their ASCII counterparts in `simplify_string_characters`."""
SIMPLE_STRING_REPLACEMENTS: dict[str, str] = {
    'ö': 'oe',
    'ø': 'o',
    'ä': 'ae',
    'å': 'a',
    'ü': 'ue',
    'ß': 'ss',
    ",": "",
    'é': 'e',
    'ë': 'e',
    ":": "-",
    "(": "-",
    ")": "-",
    'š': "s",
    '.': "-",
    "/": "-",
    'ó': "o",
    'ð': "d",
    'á': "a",
    "–": "-",
    "ł": "l",
    "‐": "-",
    "’": "",
    "'": "",
    "?": "-",
    "!": "-",
    "ò": "o",
    "&": "-and-",
    "ñ": "n",
    "δ": "d",
    "í": "i",
    "ř": "r",
    "è": "e",
    "₂": "2",
    "₃": "3",
    "₄": "4",
    "₅": "5",
    "₆": "6",
    "₇": "7",
    "₈": "8",
    "₉": "9",
    "ç": "c",
    "ú": "u",
    "“": "",
    "”": "",
    "∆": "d",
}


def simplify_string_characters(
    s: str,
    additional_replacements: dict[str, str] = {},
) -> str:
    """Simplify a string by replacing special characters with their ASCII counterparts
    and removing unwanted characters.
    
    For example, `simplify_string_characters("Héllo, wörld!")` will return `"hello-woerld"`.
    
    Args:
        s: The string to simplify.
        additional_replacements: A dictionary of additional replacements to apply. 
                                 `{ "ö": "oe" }` will replace `ö` with `oe`.
    
    Returns: The simplified string.
    """

    all_replacements = {**SIMPLE_STRING_REPLACEMENTS}
    all_replacements.update(additional_replacements)

    s = s.lower().replace(" ", "-")
    for key, value in all_replacements.items():
        s = s.replace(key, value)
    s = s.lower().replace(" ", "-")
    while "--" in s:
        s = s.replace("--", "-")
    s = s.strip("-")
    allowed_chars = "abcdefghijklmnopqrstuvwxyz0123456789-_@"
    dirty = [c for c in s if c not in allowed_chars]
    if len(dirty) > 0:
        raise Exception(
            f"Found invalid non-replaced characters in name: {dirty} ({s})"
        )
    return s


def replace_consecutive_characters(
    s: str, characters: list[str] = [" ", "-"]
) -> str:
    """Replace consecutiv characters in a string (e.g. "hello---world" -> "hello-world"
    or "hello   world" -> "hello world").
    
    Args:
        s: The string to process.
        characters: A list of characters to replace duplicates of.
    
    Returns:
        The string with duplicate characters replaced.
    """

    for c in characters:
        while c + c in s:
            s = s.replace(c + c, c)
    return s
