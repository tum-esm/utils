import os
import sys
import time

import pytest
import tum_esm_utils
from tum_esm_utils.processes import get_process_pids, start_background_process, terminate_process

PROJECT_DIR = tum_esm_utils.files.get_parent_dir_path(__file__, current_depth=2)

SCRIPT_PATH = os.path.join(PROJECT_DIR, "tests", "scripts", "dummy_process.py")
SCRIPT_PATH_WITH_GRACE = os.path.join(
    PROJECT_DIR, "tests", "scripts", "dummy_process_with_grace.py"
)


@pytest.mark.order(4)
def test_ungraceful_process() -> None:
    terminate_process(SCRIPT_PATH)
    time.sleep(0.1)

    expected_pid = start_background_process(sys.executable, SCRIPT_PATH)
    time.sleep(0.1)

    assert get_process_pids(SCRIPT_PATH) == [expected_pid]
    time.sleep(0.1)

    assert terminate_process(SCRIPT_PATH) == [expected_pid]
    time.sleep(0.1)

    assert get_process_pids(SCRIPT_PATH) == []


@pytest.mark.order(4)
def test_graceful_process() -> None:
    expected_pid = start_background_process(sys.executable, SCRIPT_PATH_WITH_GRACE)
    time.sleep(0.1)

    assert get_process_pids(SCRIPT_PATH_WITH_GRACE) == [expected_pid]
    time.sleep(0.1)

    # cannot terminate because teardown takes long
    assert terminate_process(SCRIPT_PATH_WITH_GRACE) == [expected_pid]
    time.sleep(0.5)
    assert get_process_pids(SCRIPT_PATH_WITH_GRACE) == [expected_pid]

    # hard kill works
    assert terminate_process(SCRIPT_PATH_WITH_GRACE, termination_timeout=0) == [expected_pid]
    time.sleep(0.1)
    assert get_process_pids(SCRIPT_PATH_WITH_GRACE) == []
