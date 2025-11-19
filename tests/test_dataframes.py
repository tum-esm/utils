import datetime
import pytest
import polars as pl
import tum_esm_utils.dataframes


@pytest.mark.order(3)
@pytest.mark.quick
def test_fill_df_time_gaps_with_nans() -> None:
    # Create a dataframe with a time gap
    df = pl.DataFrame(
        {
            "utc": [
                datetime.datetime(2024, 1, 1, 0, 0, 0),
                datetime.datetime(2024, 1, 1, 0, 0, 10),  # gap > 5 seconds
                datetime.datetime(2024, 1, 1, 0, 0, 11),
            ],
            "value": [1, 2, 3],
        }
    )
    result = tum_esm_utils.dataframes.fill_df_time_gaps_with_nans(
        df, time_col="utc", max_gap_seconds=5
    )
    # There should be a NaN row inserted after the first row
    assert result.shape[0] == 4
    # The inserted row should have None in 'value'
    inserted_row = result.filter(pl.col("utc").eq(datetime.datetime(2024, 1, 1, 0, 0, 9)))
    assert inserted_row["value"][0] is None
