import os
import tempfile
import polars as pl
import tum_esm_utils

PROJECT_DIR = tum_esm_utils.files.get_parent_dir_path(__file__, current_depth=2)


def test_get_parent_dir_path() -> None:
    parent_dir = tum_esm_utils.files.get_parent_dir_path(
        __file__, current_depth=1
    )
    assert parent_dir == os.path.dirname(os.path.abspath(__file__))

    parent_parent_dir = tum_esm_utils.files.get_parent_dir_path(
        __file__, current_depth=2
    )
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
    df = tum_esm_utils.files.load_raw_proffast_output(path)
    assert isinstance(df, pl.DataFrame)
    assert df.shape == (5, 11)  # 5 rows, 11 columns
    assert df.columns == ["utc"] + list(data_column_names.keys())

    # load the temporary file with a subset of columns
    df = tum_esm_utils.files.load_raw_proffast_output(
        path, selected_columns=["gnd_p", "gnd_t", "xair", "xch4_s5p"]
    )
    assert isinstance(df, pl.DataFrame)
    assert df.shape == (5, 5)  # 5 rows, 5 columns
    assert df.columns == ["utc", "gnd_p", "gnd_t", "xair", "xch4_s5p"]


def test_rel_to_abs_path() -> None:
    a1 = tum_esm_utils.files.rel_to_abs_path("tests/data/some.csv")
    a2 = tum_esm_utils.files.rel_to_abs_path("tests", "data", "some.csv")
    a3 = tum_esm_utils.files.rel_to_abs_path("tests", "data/some.csv")
    a4 = tum_esm_utils.files.rel_to_abs_path("tests/data", "some.csv")
    a5 = tum_esm_utils.files.rel_to_abs_path("tests/data/", "some.csv")
    a6 = tum_esm_utils.files.rel_to_abs_path(
        "..", "tests", "tests", "data", "some.csv"
    )
    a7 = tum_esm_utils.files.rel_to_abs_path(
        "..", "tests", "tests", "data", "..", "data", "some.csv"
    )
    assert a1 == a2 == a3 == a4 == a5 == a6 == a7

    expected = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "tests", "data", "some.csv"
    )
    assert a1 == expected


def test_read_last_n_lines() -> None:
    with tempfile.TemporaryDirectory() as d:
        filepath = os.path.join(d, "file.txt")
        with open(filepath, "w") as f:
            for i in range(10):
                f.write(f"{i} {'c'*(i+1)}\n")

        r1 = tum_esm_utils.files.read_last_n_lines(
            filepath,
            3,
            ignore_trailing_whitespace=True,
        )
        print(f"r1 = {r1}")
        assert r1 == [
            "7 cccccccc",
            "8 ccccccccc",
            "9 cccccccccc",
        ]

        r2 = tum_esm_utils.files.read_last_n_lines(
            filepath,
            3,
            ignore_trailing_whitespace=False,
        )
        print(f"r2 = {r2}")
        assert r2 == [
            "8 ccccccccc",
            "9 cccccccccc",
            "",
        ]

        with open(filepath, "w") as f:
            for i in range(3):
                f.write(f"{i} {'c'*(i+1)}\n")

        r3 = tum_esm_utils.files.read_last_n_lines(
            filepath,
            2,
            ignore_trailing_whitespace=True,
        )
        print(f"r3 = {r3}")
        assert r3 == ["1 cc", "2 ccc"]

        r4 = tum_esm_utils.files.read_last_n_lines(
            filepath,
            3,
            ignore_trailing_whitespace=True,
        )
        print(f"r4 = {r4}")
        assert r4 == ["0 c", "1 cc", "2 ccc"]

        r5 = tum_esm_utils.files.read_last_n_lines(
            filepath,
            4,
            ignore_trailing_whitespace=True,
        )
        print(f"r5 = {r5}")
        assert r5 == ["0 c", "1 cc", "2 ccc"]
