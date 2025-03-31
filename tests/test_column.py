import datetime
import os
import random
import numpy as np
import pytest
import tum_esm_utils

base = tum_esm_utils.files.rel_to_abs_path("./data/column")


@pytest.mark.order(3)
def test_astronomy() -> None:
    f = tum_esm_utils.files.rel_to_abs_path("../tum_esm_utils/column/de421.bsp")
    if os.path.isfile(f):
        os.remove(f)
    astronomy = tum_esm_utils.column.astronomy.Astronomy()
    assert os.path.isfile(f)
    lat = 48.151
    lon = 11.369
    alt = 539
    for year in range(2020, 2051):
        elevation, azimuth = astronomy.get_sun_position(
            lat,
            lon,
            alt,
            datetime.datetime(
                year=year,
                month=random.randint(1, 12),
                day=random.randint(1, 28),
                hour=random.randint(0, 23),
                minute=random.randint(0, 59),
                second=random.randint(0, 59),
            ).astimezone(datetime.timezone.utc),
        )
        assert -90 <= elevation <= 90
        assert 0 <= azimuth <= 360


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
