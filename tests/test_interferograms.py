import os
from tum_esm_utils.interferograms import detect_corrupt_ifgs
import tempfile


def test_detect_corrupt_ifgs() -> None:
    """create a temporary directory with a file that
    is not an interferogram at all"""
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "test_ifg"), "w") as f:
            f.write("corrupt interferogram")
        assert len(detect_corrupt_ifgs(tmpdir)) == 0
