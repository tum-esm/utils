import time
from typing import Callable


def expect_file_contents(
    filepath: str,
    required_content_blocks: list[str] = [],
    forbidden_content_blocks: list[str] = [],
) -> None:
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
) -> None:
    start_time = time.time()
    while True:
        if is_successful():
            break
        if (time.time() - start_time) > timeout_seconds:
            raise TimeoutError(timeout_message)
        time.sleep(0.25)
