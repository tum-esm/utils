import os
import tum_esm_utils
from tum_esm_utils.interferograms import detect_corrupt_ifgs
import tempfile

_PROJECT_DIR = tum_esm_utils.files.get_parent_dir_path(
    __file__, current_depth=2
)


def test_detect_corrupt_ifgs() -> None:
    """create a temporary directory with a file that
    is not an interferogram at all"""
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "test_ifg"), "w") as f:
            f.write("corrupt interferogram")
        assert len(detect_corrupt_ifgs(tmpdir)) == 0

    test_data_path = os.path.join(_PROJECT_DIR, "tests", "data")
    detection_results = detect_corrupt_ifgs(test_data_path)
    assert detection_results == {
        "md20220409s0e00a.0199": [
            "charfilter 'GFW' is missing",
            "charfilter 'GBW' is missing",
            "charfilter 'HFL' is missing",
            "charfilter 'LWN' is missing",
            "charfilter 'TSC' is missing",
        ]
    }
