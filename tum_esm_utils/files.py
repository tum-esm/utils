"""File-related utility functions.

Implements: `load_file`, `dump_file`, `load_json_file`,
`dump_json_file`, `get_parent_dir_path`, `get_dir_checksum`,
`get_file_checksum`, `load_raw_proffast_output`"""

from __future__ import annotations
from typing import Any, Optional
import hashlib
import json
import os
import polars as pl
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


def load_raw_proffast_output(
    path: str,
    selected_columns: list[str] = [
        "gnd_p",
        "gnd_t",
        "app_sza",
        "azimuth",
        "xh2o",
        "xair",
        "xco2",
        "xch4",
        "xco",
        "xch4_s5p",
    ],
) -> pl.DataFrame:
    """
    Returns a raw proffast output file as a dataframe.

    you can pass `selected_columns` to only keep some columns - the
    `utc` column will always be included. Example:

    ```
    utc                     gnd_p    gnd_t    app_sza   ...
    2021-10-20 07:00:23     950.91   289.05   78.45     ...
    2021-10-20 07:00:38     950.91   289.05   78.42     ...
    2021-10-20 07:01:24     950.91   289.05   78.31     ...
    ...                     ...      ...      ...       ...
    [1204 rows x 8 columns]
    ```
    """

    assert os.path.isfile(path), f"{path} is not a file"

    data_column_names = {
        "gnd_p": " gndP",
        "gnd_t": " gndT",
        "app_sza": " appSZA",
        "azimuth": " azimuth",
        "xh2o": " XH2O",
        "xair": " XAIR",
        "xco2": " XCO2",
        "xch4": " XCH4",
        "xco": " XCO",
        "xch4_s5p": " XCH4_S5P",
    }

    assert len(set(selected_columns)) == len(
        selected_columns
    ), "selected_columns cannot contain duplicate items"
    assert set(selected_columns).issubset(set(data_column_names.keys())), (
        f"selected_columns contains invalid items, only the " +
        f"following are allowed: {data_column_names.keys()}"
    )

    df = pl.read_csv(
        path,
        columns=[
            "UTC",
            *list(data_column_names.values()),
        ],
        new_columns=[
            "utc",
            *list(data_column_names.keys()),
        ],
        dtypes={
            "utc": pl.Datetime,
            **{t: pl.Float32
               for t in data_column_names.keys()},
        },
    )

    # only keep the selected columns
    return df.select(["utc", *selected_columns])
