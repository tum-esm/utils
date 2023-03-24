import json
import os
from typing import Any


def load_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def dump_file(path: str, content: str) -> None:
    with open(path, "w") as f:
        f.write(content)


def load_json_file(path: str) -> Any:
    with open(path, "r") as f:
        return json.load(f)


def dump_json_file(path: str, content: Any) -> None:
    with open(path, "w") as f:
        json.dump(content, f)


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
