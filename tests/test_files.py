import os
import polars as pl
from tum_esm_utils.files import get_parent_dir_path, load_raw_proffast_output

PROJECT_DIR = get_parent_dir_path(__file__, current_depth=2)


def test_get_parent_dir_path() -> None:
    parent_dir = get_parent_dir_path(__file__, current_depth=1)
    assert parent_dir == os.path.dirname(os.path.abspath(__file__))

    parent_parent_dir = get_parent_dir_path(__file__, current_depth=2)
    assert parent_parent_dir == os.path.dirname(parent_dir)


# test load_raw_proffast_output by generating a valid temporary file
# and trying to load it with all columns and a subset of columns
# use the polars library
def test_load_raw_proffast_output() -> None:
    data_column_names = {
        "gnd_p": " gndP",
        "gnd_t": " gndT",
        "app_sza": " appSZA",
        "azimuth": " azimuth",
        "xh2o": " XH2O",
        "xair": " XAIR",
        "xco2": " XCO2",
        "xch4": " XCH4",
        "xco": " XCO",
        "xch4_s5p": " XCH4_S5P",
    }

    path = os.path.join(
        PROJECT_DIR,
        "tests",
        "data",
        "comb_invparms_ma_SN061_210329-210329.csv",
    )

    # load the temporary file
    df = load_raw_proffast_output(path)
    assert isinstance(df, pl.DataFrame)
    assert df.shape == (5, 11)  # 5 rows, 11 columns
    assert df.columns == ["utc"] + list(data_column_names.keys())

    # load the temporary file with a subset of columns
    df = load_raw_proffast_output(
        path, selected_columns=["gnd_p", "gnd_t", "xair", "xch4_s5p"]
    )
    assert isinstance(df, pl.DataFrame)
    assert df.shape == (5, 5)  # 5 rows, 5 columns
    assert df.columns == ["utc", "gnd_p", "gnd_t", "xair", "xch4_s5p"]
