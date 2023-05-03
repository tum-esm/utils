import hashlib
import json
import os
from typing import Any, Optional

import tum_esm_utils


def load_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def dump_file(path: str, content: str) -> None:
    with open(path, "w") as f:
        f.write(content)


def load_json_file(path: str) -> Any:
    with open(path, "r") as f:
        return json.load(f)


def dump_json_file(path: str, content: Any, indent: Optional[int] = 4) -> None:
    with open(path, "w") as f:
        json.dump(content, f, indent=indent)


def get_parent_dir_path(script_path: str, current_depth: int = 1) -> str:
    """Get the absolute path of a parent directory based on the
    current script path. Simply pass the `__file__` variable of
    the current script to this function. Depth of 1 will return
    the direct parent directory of the current script."""
    assert current_depth > 0, "depth must be greater than 0"
    output = os.path.dirname(os.path.abspath(script_path))
    for _ in range(current_depth - 1):
        output = os.path.dirname(output)
    return output


def get_dir_checksum(path: str) -> str:
    """Get the checksum of a directory using md5deep."""

    assert os.path.isdir(path), f"{path} is not a directory"
    return tum_esm_utils.shell.run_shell_command(
        f"md5deep -r -b {path} | sort -u | md5sum"
    )


def get_file_checksum(path: str) -> str:
    """Get the checksum of a file using MD5 from `haslib`.

    Significantly faster than `get_dir_checksum` since it does
    not spawn a new process."""

    assert os.path.isfile(path), f"{path} is not a file"
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()
