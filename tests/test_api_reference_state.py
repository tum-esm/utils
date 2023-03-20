import os
import tum_esm_utils

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_api_reference_state() -> None:
    checksum_before_update = tum_esm_utils.shell.run_shell_command(
        "find docs/api-reference -type f -exec md5sum {} + | LC_ALL=C sort | md5sum",
        working_directory=PROJECT_DIR,
    )

    tum_esm_utils.shell.run_shell_command(
        "bash scripts/update_api_reference.sh", working_directory=PROJECT_DIR
    )

    checksum_after_update = tum_esm_utils.shell.run_shell_command(
        "find docs/api-reference -type f -exec md5sum {} + | LC_ALL=C sort | md5sum",
        working_directory=PROJECT_DIR,
    )

    assert (
        checksum_before_update == checksum_after_update
    ), "API reference is not up to date"
