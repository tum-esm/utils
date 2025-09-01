import os
import tempfile

import pytest
import tum_esm_utils.shell


@pytest.mark.order(3)
@pytest.mark.quick
def test_change_file_permissions() -> None:
    with tempfile.TemporaryFile() as f:
        # try to change the permissions of the file
        # in an invalid way and check if the function
        # raises and AssertionError
        for invalid_permission_string in ["", "r", "rw", "rwxrwxrww"]:
            try:
                tum_esm_utils.shell.change_file_permissions(f.name, invalid_permission_string)
                raise Exception("change_file_permissions did not raise an AssertionError")
            except AssertionError:
                pass

        permission_strings = ["---", "--x", "-w-", "-wx", "r--", "r-x", "rw-", "rwx"]
        permission_bits = [0, 1, 2, 3, 4, 5, 6, 7]

        for i in range(8):
            for j in range(8):
                for k in range(8):
                    tum_esm_utils.shell.change_file_permissions(
                        f.name,
                        permission_strings[i] + permission_strings[j] + permission_strings[k],
                    )
                    assert (
                        oct(os.stat(f.name).st_mode)[5:]
                        == f"{permission_bits[i]}{permission_bits[j]}{permission_bits[k]}"
                    )
