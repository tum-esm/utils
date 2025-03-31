import numpy as np
import pytest
import tum_esm_utils

IFG1 = tum_esm_utils.files.rel_to_abs_path("./data/ifgs/md20220409s0e00a.0198")
IFG2 = tum_esm_utils.files.rel_to_abs_path("./data/ifgs/md20220409s0e00a.0199")
IFG3 = tum_esm_utils.files.rel_to_abs_path("./data/ifgs/md20220409s0e00a.0200")
IFG4 = tum_esm_utils.files.rel_to_abs_path("./data/ifgs/ma20240514s0e00a.0975")


@pytest.mark.order(3)
@pytest.mark.quick
def test_opus_file_reading() -> None:
    for mode in ["skip", "validate", "read"]:
        of = tum_esm_utils.opus.OpusFile.read(IFG1, interferogram_mode=mode)  # type: ignore
        assert (of.interferogram is not None) == (mode == "read")
        of.model_dump()

        # Expect invalid OPUS files to raise a RuntimeError
        try:
            tum_esm_utils.opus.OpusFile.read(IFG2, interferogram_mode=mode)  # type: ignore
            raise Exception("Expected a RuntimeError")
        except RuntimeError:
            pass
        try:
            tum_esm_utils.opus.OpusFile.read(IFG3, interferogram_mode=mode)  # type: ignore
            raise Exception("Expected a RuntimeError")
        except RuntimeError:
            pass

    # Compute peak position of both channels

    ifg = tum_esm_utils.opus.OpusFile.read(IFG4, interferogram_mode="read").interferogram
    assert ifg is not None
    fwd = ifg[0][: ifg.shape[1] // 2]
    assert len(fwd) == 114256
    computed_peak = np.argmax(fwd)
    ifg_center = fwd.shape[0] // 2
    assert abs(computed_peak - ifg_center) < 10
