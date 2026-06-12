# `tum_esm_utils.dataframes` API Reference


Dataframe-related utility functions.

Implements: `fill_df_time_gaps_with_nans`

This requires you to install this utils library with the optional `polars` dependency:

```bash
pip install "tum_esm_utils[polars]"
## `or`
uv add "tum_esm_utils[polars]"
```


##### `fill_df_time_gaps_with_nans`

```python
def fill_df_time_gaps_with_nans(df: pl.DataFrame, time_col: str,
                                max_gap_seconds: int) -> pl.DataFrame
```

Fill time gaps in a dataframe with NaN rows. This is very useful for plotting dataframes where time gaps should be visible.

**Arguments**:

- `df` - The input dataframe.
- `time_col` - The name of the time column.
- `max_gap_seconds` - The maximum gap in seconds to fill with NaN rows.

