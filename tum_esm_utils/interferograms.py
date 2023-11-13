"""Functions for interacting with interferograms.

Implements: `detect_corrupt_ifgs`"""

from __future__ import annotations
from typing import Literal
import os
import re
import subprocess
import filelock
import tum_esm_utils

_PARSER_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "ifg_parser"
)


def _compile_fortran_code(
    silent: bool = True,
    fortran_compiler: Literal["gfortran", "gfortran-9"] = "gfortran",
) -> None:
    if not os.path.isfile(os.path.join(_PARSER_DIR, "ifg_parser")):
        if not silent:
            print("compiling fortran code")

        command = f"{fortran_compiler} -nocpp -O3 -o ./ifg_parser glob_prepro4.F90 glob_OPUSparms.F90 ifg_parser.F90"
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


def _write_input_file(random_id: str, ifgs: list[str]) -> None:
    with open(f"{_PARSER_DIR}/ifg_parser.template.inp", "r") as f:
        template_content = f.read()
    with open(f"{_PARSER_DIR}/ifg_parser.inp.{random_id}", "w") as f:
        f.write(template_content.replace("%IFG_LIST%", "\n".join(ifgs)))


def detect_corrupt_ifgs(
    ifg_directory: str,
    silent: bool = True,
    fortran_compiler: Literal["gfortran", "gfortran-9"] = "gfortran",
) -> dict[str, list[str]]:
    """Returns dict[filename, list[error_messages]] for all
    corrupt interferograms in the given directory.

    It will compile the fortran code using a given compiler
    to perform this task. The fortran code is derived from
    the preprocess source code of Proffast 2
    (https://www.imk-asf.kit.edu/english/3225.php). We use
    it because the retrieval using Proffast 2 will fail if
    there are corrupt interferograms in the input."""

    # compiling fortran code
    _compile_fortran_code(silent=silent, fortran_compiler=fortran_compiler)

    # generate input file
    ifgs = [f"{ifg_directory}/{x}" for x in os.listdir(ifg_directory)]
    ifgs = list(sorted(list(filter(os.path.isfile, ifgs))))

    # run the parser
    results: dict[str, list[str]] = {}
    stdout: str = ""
    while True:
        with filelock.FileLock(f"{_PARSER_DIR}/ifg_parser.inp.lock"):
            random_id = tum_esm_utils.text.get_random_string(
                10,
                forbidden=[
                    f.replace("ifg_parser.inp.", "")
                    for f in os.listdir(_PARSER_DIR)
                    if f.startswith("ifg_parser.inp.")
                ],
            )
            _write_input_file(random_id, ifgs)
        process = subprocess.run(
            ["./ifg_parser", f"ifg_parser.inp.{random_id}"],
            cwd=_PARSER_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        os.remove(f"{_PARSER_DIR}/ifg_parser.inp.{random_id}")
        stdout = process.stdout.decode()
        stderr = process.stderr.decode()
        if process.returncode == 0:
            break
        else:
            # find the filename that caused the error
            failing_filenames = list(
                filter(lambda f: f in ifgs, stderr.split("'"))
            )
            assert (
                "At line 837 of file ifg_parser.F90" in stderr
            ), f"Unknown error behavior: {stderr}"
            assert len(
                failing_filenames
            ) == 1, "invalid filename not found in stderr"
            failing_filepath = failing_filenames[0]

            # remove the error-causing file from the ifg list and try again
            ifgs.remove(failing_filepath)
            failing_filename = failing_filepath.split("/")[-1]
            results[failing_filename] = ["file not processable"]
            if not silent:
                print(f'error with file "{failing_filename}", running again')

    with open(os.path.join(_PARSER_DIR, "output.txt"), "w") as f:
        f.write(stdout)

    file_parsing_block = stdout.split("Done!")[-1]
    file_parsing_lines = file_parsing_block.split("Read OPUS parms:")[1 :]

    # get results from output stream
    for line in file_parsing_lines:
        filename = line[12 :].split("\n")[0].split("/")[-1].replace(")", "")
        parser_output = line[12 :].replace("\n", " ")
        parser_messages = re.findall(
            'charfilter "[^"]+" is missing', parser_output
        )
        if len(parser_messages) > 0:
            results[filename] = [
                ("charfilter '" + x.split('"')[1] + "' is missing")
                for x in parser_messages
            ]

    return results
