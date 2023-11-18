"""Functions commonly used in testing scripts.

Implements: `expect_file_contents`, `wait_for_condition`"""

from __future__ import annotations
from typing import Callable
import time


def expect_file_contents(
    filepath: str,
    required_content_blocks: list[str] = [],
    forbidden_content_blocks: list[str] = [],
) -> None:
    """Assert that the given file contains all of the required content
    blocks, and/or none of the forbidden content blocks."""

    with open(filepath, "r") as f:
        file_content = f.read()

    for b in required_content_blocks:
        assert b in file_content, f'required log content block not found "{b}"'

    for b in forbidden_content_blocks:
        assert b not in file_content, f'forbidden log content block found "{b}"'


def wait_for_condition(
    is_successful: Callable[[], bool],
    timeout_message: str,
    timeout_seconds: float = 5,
    check_interval_seconds: float = 0.25,
) -> None:
    """Wait for the given condition to be true, or raise a TimeoutError
    if the condition is not met within the given timeout.

    `check_interval_seconds` controls, how long to wait inbetween
    `is_successful()` calls."""

    start_time = time.time()
    while True:
        if is_successful():
            break
        if (time.time() - start_time) > timeout_seconds:
            raise TimeoutError(timeout_message)
        time.sleep(check_interval_seconds)
