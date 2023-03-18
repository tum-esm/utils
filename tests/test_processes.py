import os
import sys
import time
import tum_esm_utils


SCRIPT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "scripts",
    "dummy_process_script.py",
)


def test_processes() -> None:
    expected_pid = tum_esm_utils.processes.start_background_process(
        sys.executable, SCRIPT_PATH
    )

    time.sleep(1)

    assert tum_esm_utils.processes.get_process_pids(SCRIPT_PATH) == [expected_pid]
    assert tum_esm_utils.processes.terminate_process(SCRIPT_PATH) == [expected_pid]
    assert tum_esm_utils.processes.get_process_pids(SCRIPT_PATH) == []
