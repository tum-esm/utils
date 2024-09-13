"""File-related utility functions.

Implements: `load_file`, `dump_file`, `load_json_file`,
`dump_json_file`, `get_parent_dir_path`, `get_dir_checksum`,
`get_file_checksum`, `rel_to_abs_path`, `read_last_n_lines`,
`expect_file_contents`, `render_directory_tree`, `list_directory`"""

from __future__ import annotations
from typing import Any, Optional
import fnmatch
import re
import traceback
import hashlib
import json
import os
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


def rel_to_abs_path(*path: str) -> str:
    """Convert a path relative to the caller's file to an absolute path.
    
    Inside file `/home/somedir/somepath/somefile.py`, calling
    `rel_to_abs_path("..", "config", "config.json")` will
    return `/home/somedir/config/config.json`.
    
    Credits to https://stackoverflow.com/a/59004672/8255842"""

    return os.path.normpath(
        os.path.join(
            os.path.dirname(traceback.extract_stack()[-2].filename),
            *path,
        )
    )


def read_last_n_lines(
    file_path: str,
    n: int,
    ignore_trailing_whitespace: bool = False,
) -> list[str]:
    """Read the last `n` lines of a file.

    The function returns less than `n` lines if the file has less than `n` lines.
    The last element in the list is the last line of the file.
    
    This function uses seeking in order not to read the full file. The simple
    approach of reading the last 10 lines would be:

    ```python
    with open(path, "r") as f:
        return f.read().split("\\n")[:-10]
    ```

    However, this would read the full file and if we only need to read 10 lines
    out of a 2GB file, this would be a big waste of resources.
    
    The `ignore_trailing_whitespace` option to crop off trailing whitespace, i.e.
    only return the last `n` lines that are not empty or only contain whitespace."""

    with open(file_path, "rb") as f:
        f.seek(-1, os.SEEK_END)

        if ignore_trailing_whitespace:
            while f.read(1) in [b"\n", b" ", b"\t"]:
                try:
                    f.seek(-2, os.SEEK_CUR)
                except OSError:
                    # reached the beginning of the file
                    return [""]

            f.seek(-1, os.SEEK_CUR)
            # now the cursor is right before the last
            # character that is not a newline or a space

        last_characters: bytes = b""
        new_line_chars_seen: int = 0

        while True:
            try:
                new_character = f.read(1)
                if new_character == b"\n":
                    new_line_chars_seen += 1
                if new_line_chars_seen == n:
                    break
                last_characters += new_character
                f.seek(-2, os.SEEK_CUR)
            except OSError:
                # reached the beginning of the file
                break

    return last_characters.decode()[::-1].split("\n")


def expect_file_contents(
    filepath: str,
    required_content_blocks: list[str] = [],
    forbidden_content_blocks: list[str] = [],
) -> None:
    """Assert that the given file contains all of the required content
    blocks, and/or none of the forbidden content blocks.
    
    Args:
        filepath:                 The path to the file.
        required_content_blocks:  A list of strings that must be present in the file.
        forbidden_content_blocks: A list of strings that must not be present in the file.
    """

    with open(filepath, "r") as f:
        file_content = f.read()

    for b in required_content_blocks:
        assert b in file_content, f'required log content block not found "{b}"'

    for b in forbidden_content_blocks:
        assert b not in file_content, f'forbidden log content block found "{b}"'


def render_directory_tree(
    root: str,
    ignore: list[str] = [],
    max_depth: Optional[int] = None,
    root_alias: Optional[str] = None,
    directory_prefix: Optional[str] = "📁 ",
    file_prefix: Optional[str] = "📄 ",
) -> Optional[str]:
    """Render a file tree as a string.
    
    Example:
    
    ```
    📁 <config.general.data.results>
    ├─── 📁 bundle
    │    ├─── 📄 __init__.py
    │    ├─── 📄 load_results.py
    │    └─── 📄 main.py
    ├─── 📁 profiles
    │    ├─── 📄 __init__.py
    │    ├─── 📄 cache.py
    │    ├─── 📄 download_logic.py
    │    ├─── 📄 generate_queries.py
    │    ├─── 📄 main.py
    │    ├─── 📄 std_site_logic.py
    │    └─── 📄 upload_logic.py
    ├─── 📁 retrieval
    │    ├─── 📁 algorithms
    ...
    ```
    
    Args:
        root:              The root directory to render.
        ignore:            A list of patterns to ignore. If the basename of a directory
                           matches any of the patterns, the directory is ignored.
        max_depth:         The maximum depth to render. If `None`, render the full tree.
        root_alias:        An alias for the root directory. If `None`, the basename of
                           the root directory is used. In the example above, the root
                           directory is was aliased to `<config.general.data.results>`.
        directory_prefix:  The prefix to use for directories.
        file_prefix:       The prefix to use for files.
    
    Returns: The directory tree as a string. If the root directory is ignored, `None`.
    """

    if any([
        fnmatch.fnmatch(os.path.basename(root), pattern) for pattern in ignore
    ]):
        return None

    root_name = os.path.basename(root) if root_alias is None else root_alias

    if directory_prefix is None:
        directory_prefix = ""
    if file_prefix is None:
        file_prefix = ""

    if os.path.isdir(root):
        out = f"{directory_prefix}{root_name}"
        if max_depth == 0:
            return out

        sublists: list[str] = []
        for item in sorted(os.listdir(root)):
            sd = render_directory_tree(
                os.path.join(root, item),
                ignore=ignore,
                max_depth=(max_depth - 1) if max_depth is not None else None
            )
            if sd is not None:
                sublists.append(sd)

        sublists = sorted(sublists)
        for i, item in enumerate(sublists):
            for j, line in enumerate(item.split("\n")):
                prefix: str
                if i < (len(sublists) - 1):
                    if j == 0:
                        prefix = "├───"
                    else:
                        prefix = "│   "
                else:
                    if j == 0:
                        prefix = "└───"
                    else:
                        prefix = "    "
                out += f"\n{prefix} {line}"
        return out
    if os.path.isfile(root):
        return f"{file_prefix}{root_name}"
    return ""


def list_directory(
    path: str,
    regex: Optional[str] = None,
    ignore: Optional[list[str]] = None,
    include_directories: bool = True,
    include_files: bool = True,
    include_links: bool = True,
) -> list[str]:
    """List the contents of a directory based on certain criteria. Like `os.listdir`
    with superpowers. You can filter the list by a regex or you can ignore Unix shell
    style patterns like `*.lock`.
    
    Args:
        path:                 The path to the directory.
        regex:                A regex pattern to match the item names against.
        ignore:               A list of patterns to ignore. If the basename of an item
                              matches any of the patterns, the item is ignored.
        include_directories:  Whether to include directories in the output.
        include_files:        Whether to include files in the output.
        include_links:        Whether to include symbolic links in the output.
    
    Returns: A list of items in the directory that match the criteria.
    """

    assert os.path.isdir(path), f"Path {path} is not a directory"
    files = os.listdir(path)
    if regex is not None:
        files = [f for f in files if re.match(regex, f)]
    if ignore is not None:
        files = [
            f for f in files
            if not any([fnmatch.fnmatch(f, pattern) for pattern in ignore])
        ]
    if not include_directories:
        files = [f for f in files if not os.path.isdir(os.path.join(path, f))]
    if not include_files:
        files = [f for f in files if not os.path.isfile(os.path.join(path, f))]
    if not include_links:
        files = [f for f in files if not os.path.islink(os.path.join(path, f))]

    return files
