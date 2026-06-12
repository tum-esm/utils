# `tum_esm_utils.rebinning` API Reference


Functions to rebin binned data points

Implements: `rebin_1d`, `rebin_2d`.

This requires you to install this utils library with the optional `modeling` dependency:

```bash
pip install "tum_esm_utils[modeling]"
## `or`
uv add "tum_esm_utils[modeling]"
```


##### `rebin_1d`

```python
def rebin_1d(arr: np.ndarray[Any, Any],
             new_bin_count: int) -> np.ndarray[Any, Any]
```

Rebins a 1D array to a new number of bins.


##### `rebin_2d`

```python
def rebin_2d(arr: np.ndarray[Any, Any], new_x_bins: int,
             new_y_bins: int) -> np.ndarray[Any, Any]
```

Rebins a 2D array to new number of bins in x and y dimensions.

