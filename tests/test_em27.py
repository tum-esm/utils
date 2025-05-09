import os
import tempfile

import pytest
import tum_esm_utils

_PROJECT_DIR = tum_esm_utils.files.get_parent_dir_path(__file__, current_depth=2)


@pytest.mark.order(4)
def test_detect_corrupt_ifgs() -> None:
    """create a temporary directory with a file that
    is not an interferogram at all"""

    with tempfile.TemporaryDirectory() as tmpdir:
        assert len(tum_esm_utils.em27.detect_corrupt_opus_files(tmpdir)) == 0
        test_file_name = os.path.join(tmpdir, "test_ifg")
        with open(test_file_name, "w") as f:
            f.write("corrupt interferogram")
        assert set(tum_esm_utils.em27.detect_corrupt_opus_files(tmpdir).keys()) == {"test_ifg"}

    detection_results = tum_esm_utils.em27.detect_corrupt_opus_files(
        tum_esm_utils.files.rel_to_abs_path("./data/ifgs")
    )
    assert set(detection_results.keys()) == set(
        [
            "md20220409s0e00a.0199",
            "md20220409s0e00a.0200",
            "md20220409s0e00a.0198.json",
        ]
    )


@pytest.mark.order(3)
@pytest.mark.quick
def test_load_proffast2_result() -> None:
    input_dir = tum_esm_utils.files.rel_to_abs_path("./data/proffast")
    files = [f for f in os.listdir(input_dir) if f.startswith("comb_inv") and f.endswith(".csv")]
    for f in files:
        df = tum_esm_utils.em27.load_proffast2_result(os.path.join(input_dir, f))
        assert len(df) > 2
        assert "UTC" in df.columns
        assert "XCO2" in df.columns
