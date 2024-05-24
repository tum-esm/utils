"""Functions for interacting with EM27 interferograms.

Implements: `detect_corrupt_opus_files`, `load_proffast2_result`.

This requires you to install this utils library with the optional `polars` dependency:

```bash
pip install "tum_esm_utils[polars]"
# or
pdm add "tum_esm_utils[polars]"
```"""

from __future__ import annotations
from typing import Any, Literal
import os
import subprocess
from typing_extensions import deprecated
import filelock
import tum_esm_utils
import polars as pl

_PARSER_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "opus_file_validator"
)


def _compile_fortran_code(
    silent: bool = True,
    fortran_compiler: Literal["gfortran", "gfortran-9"] = "gfortran",
    force_recompile: bool = False,
) -> None:
    if force_recompile or (
        not os.path.isfile(os.path.join(_PARSER_DIR, "opus_file_validator"))
    ):
        if not silent:
            print("compiling fortran code")

        command = (
            f"{fortran_compiler} -nocpp -O3 -o ./opus_file_validator " +
            f"glob_prepro6.F90 glob_OPUSparms6.F90 opus_file_validator.F90"
        )
        p = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=_PARSER_DIR,
            env=os.environ.copy(),
        )
        if p.returncode != 0:
            stdout = p.stdout.decode("utf-8", errors="replace").strip()
            stderr = p.stderr.decode("utf-8", errors="replace").strip()
            raise Exception(
                f"command '{command}' failed with exit code {p.returncode}, " +
                f"stderr: {stderr}, stout:{stdout}",
            )


def detect_corrupt_opus_files(
    ifg_directory: str,
    silent: bool = True,
    fortran_compiler: Literal["gfortran", "gfortran-9"] = "gfortran",
    force_recompile: bool = False,
) -> dict[str, list[str]]:
    """Returns dict[filename, list[error_messages]] for all
    corrupt opus files in the given directory.

    It will compile the fortran code using a given compiler
    to perform this task. The fortran code is derived from
    the preprocess source code of Proffast 2
    (https://www.imk-asf.kit.edu/english/3225.php). We use
    it because the retrieval using Proffast 2 will fail if
    there are corrupt interferograms in the input.
    
    Args:
        ifg_directory:     The directory containing the interferograms.
        silent:            If set to False, print additional information.
        fortran_compiler:  The fortran compiler to use.
        force_recompile:   If set to True, the fortran code will be recompiled.

    Returns:
        A dictionary containing corrupt filenames as keys and a list of error
        messages as values."""

    # compiling the fortran code in a semaphore
    with filelock.FileLock(
        os.path.join(_PARSER_DIR, "opus_file_validator.lock"),
        timeout=30,
    ):
        _compile_fortran_code(
            silent=silent,
            fortran_compiler=fortran_compiler,
            force_recompile=force_recompile
        )

    # list directory files
    filepaths = list(
        sorted([
            fp for fp in
            [f"{ifg_directory}/{x}" for x in os.listdir(ifg_directory)]
            if os.path.isfile(fp)
        ])
    )

    # write input file for parser in a semaphore
    with filelock.FileLock(f"{_PARSER_DIR}/opus_file_validator.lock"):
        random_id = tum_esm_utils.text.get_random_string(
            10,
            forbidden=[
                f.replace("opus_file_validator.inp.", "")
                for f in os.listdir(_PARSER_DIR)
                if f.startswith("opus_file_validator.inp.")
            ],
        )
        input_file_path = f"{_PARSER_DIR}/opus_file_validator.inp.{random_id}"

        with open(f"{_PARSER_DIR}/opus_file_validator.template.inp", "r") as f:
            template_content = f.read()
        with open(input_file_path, "w") as f:
            f.write(
                template_content.replace("%IFG_LIST%", "\n".join(filepaths))
            )

    # run the parser
    process = subprocess.run(
        ["./opus_file_validator", input_file_path],
        cwd=_PARSER_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    os.remove(input_file_path)
    stdout = process.stdout.decode()
    stderr = process.stderr.decode()

    if not process.returncode == 0:
        raise RuntimeError(
            f"Opus File Parser failed with exit code {process.returncode}, " +
            f"stderr: {stderr}, stdout: {stdout}",
        )

    # locate the block of verification results
    if ((stdout.count("--- Start verifying file integrities ---") != 1) or
        (stdout.count("--- Done verifying file integrities ---") != 1)):
        raise Exception("This is a bug in the `tum_esm_utils` library")
    verification_block = stdout.split(
        "--- Start verifying file integrities ---"
    )[1].split("--- Done verifying file integrities ---")[0].strip("\t\n ")

    # parse the verification results
    results: dict[str, list[str]] = {}
    checked_files: set[str] = set(filepaths)
    if "\n\n" in verification_block:
        file_verification_blocks = verification_block.split("\n\n")
        for block in file_verification_blocks:
            lines = block.split("\n")
            is_corrupt = len(lines) > 2
            filepath = lines[0].split('"')[1]
            if is_corrupt:
                results[os.path.basename(filepath)] = lines[1 :-1]
            checked_files.remove(filepath)

    # every file not mentioned in the verification results failed during reading it
    for filepath in checked_files:
        results[os.path.basename(filepath)] = [
            "File not even readible by the parser"
        ]

    # save the raw output for debugging purposes
    with open(os.path.join(_PARSER_DIR, "output.txt"), "w") as f:
        f.write(stdout)

    return results


@deprecated(
    "This will be removed in the next breaking release. Please use " +
    "the identical function `detect_corrupt_opus_files` instead."
)
def detect_corrupt_ifgs(
    ifg_directory: str,
    silent: bool = True,
    fortran_compiler: Literal["gfortran", "gfortran-9"] = "gfortran",
    force_recompile: bool = False,
) -> dict[str, list[str]]:
    """Returns dict[filename, list[error_messages]] for all
    corrupt opus files in the given directory.

    It will compile the fortran code using a given compiler
    to perform this task. The fortran code is derived from
    the preprocess source code of Proffast 2
    (https://www.imk-asf.kit.edu/english/3225.php). We use
    it because the retrieval using Proffast 2 will fail if
    there are corrupt interferograms in the input.
    
    Args:
        ifg_directory:     The directory containing the interferograms.
        silent:            If set to False, print additional information.
        fortran_compiler:  The fortran compiler to use.
        force_recompile:   If set to True, the fortran code will be recompiled.

    Returns:
        A dictionary containing corrupt filenames as keys and a list of error
        messages as values."""
    return detect_corrupt_opus_files(
        ifg_directory=ifg_directory,
        silent=silent,
        fortran_compiler=fortran_compiler,
        force_recompile=force_recompile,
    )


def load_proffast2_result(path: str) -> pl.DataFrame:
    """Loads the output of Proffast 2 into a polars DataFrame.

    Args:
        path: The path to the Proffast 2 output file.
    
    Returns:
        A polars DataFrame containing all columns.
    """

    column_names = [
        "JulianDate", "UTtimeh", "gndP", "gndT", "latdeg", "londeg", "altim",
        "appSZA", "azimuth", "XH2O", "XAIR", "XCO2", "XCH4", "XCO2_STR", "XCO",
        "XCH4_S5P", "H2O", "O2", "CO2", "CH4", "CO", "CH4_S5P"
    ]
    df = pl.read_csv(
        path,
        has_header=True,
        separator=",",
        dtypes={
            "UTC": pl.Datetime,
            " LocalTime": pl.Utf8,
            " spectrum": pl.Utf8,
            **{f" {cn}": pl.Float32
               for cn in column_names},
        }
    ).drop(" JulianDate", " UTtimeh")
    return df.rename({
        " LocalTime": "LocalTime",
        " spectrum": "spectrum",
        **{f" {cn}": cn
           for cn in column_names if f" {cn}" in df.columns},
    }).with_columns(
        pl.col("LocalTime").str.strptime(
            dtype=pl.Datetime, format=" %Y-%m-%d %H:%M:%S"
        ),
    )
