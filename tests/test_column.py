import pytest
import tum_esm_utils

base = tum_esm_utils.files.rel_to_abs_path("./data/column/2024010100_48N012E.")


@pytest.mark.order(3)
def test_load_ggg2020_map() -> None:
    tum_esm_utils.column.ncep_profiles.load_ggg2020_map(base + "map")


@pytest.mark.order(3)
def test_load_ggg2020_mod() -> None:
    tum_esm_utils.column.ncep_profiles.load_ggg2020_mod(base + "mod")


@pytest.mark.order(3)
def test_load_ggg2020_vmr() -> None:
    tum_esm_utils.column.ncep_profiles.load_ggg2020_vmr(base + "vmr")
