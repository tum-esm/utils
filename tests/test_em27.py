import os
import tempfile
import tum_esm_utils

_PROJECT_DIR = tum_esm_utils.files.get_parent_dir_path(
    __file__, current_depth=2
)


def test_detect_corrupt_ifgs() -> None:
    """create a temporary directory with a file that
    is not an interferogram at all"""

    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "test_ifg"), "w") as f:
            f.write("corrupt interferogram")
        assert len(tum_esm_utils.em27.detect_corrupt_ifgs(tmpdir)) == 0

    test_data_path = os.path.join(_PROJECT_DIR, "tests", "data")
    detection_results = tum_esm_utils.em27.detect_corrupt_ifgs(test_data_path)
    assert detection_results == {
        "md20220409s0e00a.0199": [
            "charfilter 'GFW' is missing",
            "charfilter 'GBW' is missing",
            "charfilter 'HFL' is missing",
            "charfilter 'LWN' is missing",
            "charfilter 'TSC' is missing",
        ]
    }


def test_load_proffast2_result() -> None:
    input_dir = tum_esm_utils.files.rel_to_abs_path("./data")
    files = [
        f for f in os.listdir(input_dir)
        if f.startswith("comb_inv") and f.endswith(".csv")
    ]
    for f in files:
        df = tum_esm_utils.em27.load_proffast2_result(
            os.path.join(input_dir, f)
        )
        assert len(df) > 2
        assert "UTC" in df.columns
        assert "XCO2" in df.columns
