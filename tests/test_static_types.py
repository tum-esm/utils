import os
import shutil
import sys
import pytest

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _rmdir(path: str) -> None:
    path = os.path.join(PROJECT_DIR, path)
    if os.path.isdir(path):
        shutil.rmtree(path)


@pytest.mark.order(1)
def test_static_types() -> None:
    _rmdir(".mypy_cache/3.*/tum_esm_utils")
    _rmdir(".mypy_cache/3.*/tests")

    for path in ["tests/", "tum_esm_utils/"]:
        print(f"Checking {path} ...")
        assert os.system(f"cd {PROJECT_DIR} && {sys.executable} -m mypy {path}") == 0
