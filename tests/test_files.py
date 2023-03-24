import os
from tum_esm_utils.files import get_parent_dir_path


def test_get_parent_dir_path() -> None:
    parent_dir = get_parent_dir_path(__file__, current_depth=1)
    assert parent_dir == os.path.dirname(os.path.abspath(__file__))

    parent_parent_dir = get_parent_dir_path(__file__, current_depth=2)
    assert parent_parent_dir == os.path.dirname(parent_dir)
