import os
import numpy as np
import pytest
import tum_esm_utils

base = tum_esm_utils.files.rel_to_abs_path("./data/column")


@pytest.mark.order(3)
def test_load_ggg2020_map() -> None:
    tum_esm_utils.column.ncep_profiles.load_ggg2020_map(
        os.path.join(base, "2024010100_48N012E.map")
    )


@pytest.mark.order(3)
def test_load_ggg2020_mod() -> None:
    tum_esm_utils.column.ncep_profiles.load_ggg2020_mod(
        os.path.join(base, "2024010100_48N012E.mod")
    )


@pytest.mark.order(3)
def test_load_ggg2020_vmr() -> None:
    tum_esm_utils.column.ncep_profiles.load_ggg2020_vmr(
        os.path.join(base, "2024010100_48N012E.vmr")
    )


@pytest.mark.order(3)
def test_averaging_kernel() -> None:
    cak = tum_esm_utils.column.averaging_kernel.ColumnAveragingKernel.load(
        os.path.join(base, "ma_avk_CO_2019.json")
    )
    factors = cak.apply(szas=np.array([10, 20, 30]), pressures=np.array([900, 800, 700]))
    assert factors.shape == (3,)
    for f in factors:
        assert 0.01 <= f <= 2.00, f"Factors should be between 0.01 and 2.00 (got {f})"
