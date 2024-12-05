import os
import tempfile
import tum_esm_utils

_PROJECT_DIR = tum_esm_utils.files.get_parent_dir_path(__file__, current_depth=2)


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
        tum_esm_utils.files.rel_to_abs_path("./data")
    )
    assert set(detection_results.keys()) == set(
        [
            "comb_invparms_ma_SN061_210329-210329.csv",
            "comb_invparms_mc_SN115_220602-220602.csv",
            "md20220409s0e00a.0199",
            "md20220409s0e00a.0200",
            "md20220409s0e00a.0198.json",
        ]
    )


def test_load_proffast2_result() -> None:
    input_dir = tum_esm_utils.files.rel_to_abs_path("./data")
    files = [f for f in os.listdir(input_dir) if f.startswith("comb_inv") and f.endswith(".csv")]
    for f in files:
        df = tum_esm_utils.em27.load_proffast2_result(os.path.join(input_dir, f))
        assert len(df) > 2
        assert "UTC" in df.columns
        assert "XCO2" in df.columns
