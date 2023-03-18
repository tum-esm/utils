import json
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
