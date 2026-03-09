import os
import sys
import pytest

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.mark.order(1)
@pytest.mark.quick
def test_ruff_linting() -> None:
    assert os.system(f"cd {PROJECT_DIR} && {sys.executable} -m ruff check") == 0  # pyright: ignore[reportDeprecated]
