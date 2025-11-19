"""Dataframe-related utility functions.

Implements: `fill_df_time_gaps_with_nans`

This requires you to install this utils library with the optional `polars` dependency:

```bash
pip install "tum_esm_utils[polars]"
# or
pdm add "tum_esm_utils[polars]"
```
"""

import datetime
import polars as pl


def fill_df_time_gaps_with_nans(
    df: pl.DataFrame,
    time_col: str,
    max_gap_seconds: int,
) -> pl.DataFrame:
    """Fill time gaps in a dataframe with NaN rows. This is very useful for plotting dataframes where time gaps should be visible.

    Args:
        df: The input dataframe.
        time_col: The name of the time column.
        max_gap_seconds: The maximum gap in seconds to fill with NaN rows."""

    assert max_gap_seconds > 1, "max_gap_seconds must be greater than 1"
    gaps_in_df = df.select(
        time_col,
        pl.col(time_col).diff().dt.total_seconds().alias(f"{time_col}_diff_seconds"),
    ).filter(
        pl.col(f"{time_col}_diff_seconds").gt(max_gap_seconds),
    )["utc"] - datetime.timedelta(seconds=1)
    gap_df = pl.DataFrame(
        {
            time_col: gaps_in_df,
            **{c: [None] * len(gaps_in_df) for c in df.columns if c != time_col},
        }
    )
    df_with_gaps = pl.concat([df, gap_df], how="vertical").sort(time_col)
    return df_with_gaps
