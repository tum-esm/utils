"""Implements custom logging functionality, because the
standard logging module is hard to configure for special
cases.

Implements: `run_shell_command`, `CommandLineException`,
`get_hostname`, `get_commit_sha`, `change_file_permissions`"""

from typing import Callable, Literal, Optional
import os
import re
import subprocess


class CommandLineException(Exception):
    """Exception raised for errors in the command line."""

    def __init__(self, value: str, details: Optional[str] = None) -> None:
        self.value = value
        self.details = details
        Exception.__init__(self)

    def __str__(self) -> str:
        return repr(self.value)


def run_shell_command(
    command: str,
    working_directory: Optional[str] = None,
    executable: str = "/bin/bash",
) -> str:
    """runs a shell command and raises a `CommandLineException`
    if the return code is not zero, returns the stdout. Uses
    `/bin/bash` by default.

    Args:
        command:           The command to run.
        working_directory: The working directory for the command.
        executable:        The shell executable to use.

    Returns:
        The stdout of the command as a string."""

    p = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=working_directory,
        env=os.environ.copy(),
        executable=executable,
    )
    stdout = p.stdout.decode("utf-8", errors="replace").strip()
    stderr = p.stderr.decode("utf-8", errors="replace").strip()

    if p.returncode != 0:
        raise CommandLineException(
            f"command '{command}' failed with exit code {p.returncode}",
            details=f"\nstderr:\n{stderr}\nstout:\n{stdout}",
        )

    return stdout


def get_hostname() -> str:
    """returns the hostname of the device, removes network
    postfix (`somename.local`) if present. Only works reliably,
    when the hostname doesn't contain a dot."""

    raw = run_shell_command("hostname")
    return (raw.split(".")[0]) if ("." in raw) else raw


def get_commit_sha(variant: Literal["short", "long"] = "short") -> Optional[str]:
    """Get the current commit sha of the repository. Returns
    `None` if there is not git repository in any parent directory.

    Args:
        variant:  "short" or "long" to specify the length of the sha.

    Returns:
        The commit sha as a string, or `None` if there is no git
        repository in the parent directories."""

    p = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD"] + (["--short"] if variant == "short" else []),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    stdout = p.stdout.decode().strip("\n ")
    if (p.returncode != 0) or ("fatal: not a git repository" in stdout):
        return None

    assert len(stdout) > 0
    return stdout


_permission_string_pattern = re.compile(r"^((r|-)(w|-)(x|-)){3}$")


def change_file_permissions(file_path: str, permission_string: str) -> None:
    """Change a file's system permissions.

    Example permission_strings: `--x------`, `rwxr-xr-x`, `rw-r--r--`.

    Args:
        file_path:         The path to the file.
        permission_string: The new permission string."""

    assert _permission_string_pattern.match(permission_string), "Invalid permission string"

    permission_str_to_bit: Callable[[str], int] = lambda p: sum(
        [int(c) for c in p.replace("r", "4").replace("w", "2").replace("x", "1").replace("-", "0")]
    )
    os.chmod(
        file_path,
        64 * permission_str_to_bit(permission_string[:3])
        + 8 * permission_str_to_bit(permission_string[3:6])
        + permission_str_to_bit(permission_string[6:]),
    )
