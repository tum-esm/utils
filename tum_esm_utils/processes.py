"""Functions to start and terminate background processes.

Implements: `get_process_pids`, `start_background_process`,
`terminate_process`"""

from __future__ import annotations
from typing import Optional
import os
import time
import psutil


def get_process_pids(script_path: str) -> list[int]:
    """Return a list of PIDs that have the given script as their entrypoint.

    Args:
        script_path: The absolute path of the python file entrypoint."""

    pids: list[int] = []
    for p in psutil.process_iter():
        try:
            if p.cmdline()[1] == script_path:
                pids.append(p.pid)
        except (
            psutil.AccessDenied,
            psutil.ZombieProcess,
            psutil.NoSuchProcess,
            IndexError,
        ):
            pass
    return pids


def start_background_process(
    interpreter_path: str, script_path: str, waiting_period: float = 0.5
) -> int:
    """Start a new background process with nohup with a given python
    interpreter and script path. The script paths parent directory
    will be used as the working directory for the process.

    Args:
        interpreter_path: The absolute path of the python interpreter.
        script_path:      The absolute path of the python file entrypoint.
        waiting_period:   The waiting period in seconds after starting
                          the process.

    Returns: The PID of the started process.
    """

    existing_pids = get_process_pids(script_path)
    assert len(existing_pids) == 0, "process is already running"

    cwd = os.path.dirname(script_path)
    os.system(f"cd {cwd} && nohup {interpreter_path} {script_path} &")
    time.sleep(waiting_period)

    new_pids = get_process_pids(script_path)
    assert (
        len(new_pids) == 1
    ), f"multiple processes found ({new_pids}), when there should only be one"

    return new_pids[0]


def terminate_process(
    script_path: str,
    termination_timeout: Optional[int] = None,
) -> list[int]:
    """Terminate all processes that have the given script as their
    entrypoint. Returns the list of terminated PIDs.

    If `termination_timeout` is not None, the processes will be
    terminated forcefully after the given timeout (in seconds).

    Args:
        script_path:         The absolute path of the python file entrypoint.
        termination_timeout: The timeout in seconds after which the
                             processes will be terminated forcefully.

    Returns:
        The list of terminated PIDs."""

    processes_to_terminate: list[psutil.Process] = []

    # terminate the processes gracefully
    for p in psutil.process_iter():
        try:
            if p.cmdline()[1] == script_path:
                processes_to_terminate.append(p)
                p.terminate()
        except (
            psutil.AccessDenied,
            psutil.ZombieProcess,
            psutil.NoSuchProcess,
            IndexError,
        ):
            pass

    # kill the processes using SIGKILL after a timeout
    if termination_timeout is not None:
        t1 = time.time()
        while True:
            try:
                if (time.time() - t1) > termination_timeout:
                    for p in processes_to_terminate:
                        if p.is_running():
                            p.kill()
                if any([p.is_running() for p in processes_to_terminate]):
                    time.sleep(1)
                else:
                    # all processes have gracefully terminated
                    break
            except (
                psutil.AccessDenied,
                psutil.ZombieProcess,
                psutil.NoSuchProcess,
                IndexError,
            ):
                pass

    return [p.pid for p in processes_to_terminate]
