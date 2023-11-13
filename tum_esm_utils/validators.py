"""Implements validator functions for use with pydantic models.

Implements: `validate_bool`, `validate_float`, `validate_int`,
`validate_str`, `validate_list`"""

from __future__ import annotations
from typing import Any, Callable, Optional, TypeVar
import os
import re
import datetime
import warnings


# duplicate method because lazydocs complains when using relative imports
def _is_date_string(date_string: str) -> bool:
    """Returns true if string is in `YYYYMMDD` format and date exists"""
    try:
        datetime.datetime.strptime(date_string, "%Y%m%d")
        return True
    except (AssertionError, ValueError):
        return False


# duplicate method because lazydocs complains when using relative imports
def _is_datetime_string(datetime_string: str) -> bool:
    """Returns true if string is in `YYYYMMDD HH:mm:ss` format and date exists"""

    warnings.warn(
        "Use `is_rfc3339_datetime_string` instead", DeprecationWarning
    )
    try:
        datetime.datetime.strptime(datetime_string, "%Y%m%d %H:%M:%S")
        return True
    except (AssertionError, ValueError):
        return False


# duplicate method because lazydocs complains when using relative imports
def _is_rfc3339_datetime_string(datetime_string: str) -> bool:
    """Returns true if string is in `YYYY-MM-DDTHH:mm:ssZ` (RFC3339)
    format and date exists. Caution: The appendix of `+00:00` is required for UTC!"""
    try:
        assert re.match(
            r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\+|\-)\d{2}:\d{2}$",
            datetime_string,
        )
        datetime.datetime.fromisoformat(datetime_string)
        return True
    except (ValueError, AssertionError):
        return False


def validate_bool() -> Callable[[Any, bool], bool]:
    def f(cls: Any, v: Any) -> bool:
        if not isinstance(v, bool):
            raise ValueError(f'"{v}" is not a boolean')
        return v

    return f


def validate_float(
    nullable: bool = False,
    minimum: Optional[float] = None,
    maximum: Optional[float] = None,
) -> Callable[[Any, float], float]:
    def f(cls: Any, v: float) -> float:
        if v is None:
            if nullable:
                return v
            else:
                raise ValueError(f"value cannot be None")
        if not isinstance(v, (int, float)):
            raise ValueError(f'"{v}" is not a float')
        if minimum is not None and v < minimum:
            raise ValueError(f'"{v}" is smaller than {minimum}')
        if maximum is not None and v > maximum:
            raise ValueError(f'"{v}" is larger than {maximum}')
        return v

    return f


def validate_int(
    nullable: bool = False,
    minimum: Optional[int] = None,
    maximum: Optional[int] = None,
    allowed: Optional[list[int]] = None,
    forbidden: Optional[list[int]] = None,
) -> Callable[[Any, Optional[int]], Optional[int]]:
    def f(cls: Any, v: Optional[int]) -> Optional[int]:
        if v is None:
            if nullable:
                return v
            else:
                raise ValueError(f"value cannot be None")
        if not isinstance(v, int):
            raise ValueError(f'"{v}" is not an integer')
        if minimum is not None and v < minimum:
            raise ValueError(f'"{v}" is smaller than {minimum}')
        if maximum is not None and v > maximum:
            raise ValueError(f'"{v}" is larger than {maximum}')
        if allowed is not None and v not in allowed:
            raise ValueError(f'"{v}" is not allowed (not one of {allowed})')
        if forbidden is not None and v in forbidden:
            raise ValueError(f'"{v}" is forbidden)')
        return v

    return f


def validate_str(
    nullable: bool = False,
    min_len: Optional[float] = None,
    max_len: Optional[float] = None,
    regex: Optional[str] = None,
    is_numeric: bool = False,
    is_directory: bool = False,
    is_file: bool = False,
    is_date_string: bool = False,
    is_datetime_string: bool = False,
    is_rfc3339_datetime_string: bool = False,
    allowed: Optional[list[str]] = None,
    forbidden: Optional[list[str]] = None,
) -> Callable[[Any, str], str]:
    def f(cls: Any, v: str) -> str:
        if v is None:
            if nullable:
                return v
            else:
                raise ValueError(f"value cannot be None")
        if not isinstance(v, str):
            raise ValueError(f'"{v}" is not a string')

        # length and regex validation
        if min_len is not None and len(v) < min_len:
            raise ValueError(f'"{v}" has less than {min_len} characters')
        if max_len is not None and len(v) > max_len:
            raise ValueError(f'"{v}" has more than {max_len} characters')
        if regex is not None and re.compile(regex).match(v) is None:
            raise ValueError(f'"{v}" does not match the regex "{regex}"')
        if is_numeric and not v.isnumeric():
            raise ValueError(f'"{v}" is not numeric')

        # directory and file validation
        if is_directory and not os.path.isdir(v):
            raise ValueError(f'"{v}" is not a directory')
        if is_file and not os.path.isfile(v):
            raise ValueError(f'"{v}" is not a file')

        # date and datetime string validation
        if is_date_string and not _is_date_string(v):
            raise ValueError(f'"{v}" is not a date string ("YYYYMMDD")')
        if is_datetime_string and not _is_datetime_string(v):
            raise ValueError(
                f'"{v}" is not a datetime string ("YYYYMMDD HH:mm:ss")'
            )
        if is_rfc3339_datetime_string and not _is_rfc3339_datetime_string(v):
            raise ValueError(
                f'"{v}" is not a datetime string ("YYYY-MM-DDTHH:mm:ssZ")'
            )

        # allowed and forbidden values
        if allowed is not None and v not in allowed:
            raise ValueError(f'"{v}" is not allowed (not one of {allowed})')
        if forbidden is not None and v in forbidden:
            raise ValueError(f'"{v}" is forbidden)')
        return v

    return f


T = TypeVar("T")


def validate_list(
    min_len: Optional[float] = None,
    max_len: Optional[float] = None,
    allowed: Optional[list[T]] = None,
    required: Optional[list[T]] = None,
    forbidden: Optional[list[T]] = None,
) -> Callable[[Any, list[T]], list[T]]:
    def f(cls: Any, v: list[T]) -> list[T]:
        if not isinstance(v, list):
            raise ValueError(f'"{v}" is not a list')
        if min_len is not None and len(v) < min_len:
            raise ValueError(f'"{v}" has less than {min_len} elements')
        if max_len is not None and len(v) > max_len:
            raise ValueError(f'"{v}" has more than {max_len} elements')
        if allowed is not None:
            for item in v:
                if item not in allowed:
                    raise ValueError(f'"{item}" is not allowed')
        if required is not None:
            for item in required:
                if item not in v:
                    raise ValueError(f'"{v}" has to include "{item}"')
        if forbidden is not None:
            for item in forbidden:
                if item in v:
                    raise ValueError(f'"{v}" should not include "{item}"')
        return v

    return f
