import os
import subprocess
from typing import Optional


class CommandLineException(Exception):
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
    `/bin/bash` by default."""

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


def get_commit_sha() -> Optional[str]:
    """Get the current commit sha of the repository. Returns
    `None` if there is not git repository in any parent directory."""

    p = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD", "--short"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    stdout = p.stdout.decode().strip("\n ")
    if (p.returncode != 0) or ("fatal: not a git repository" in stdout):
        return None

    assert len(stdout) > 0
    return stdout
