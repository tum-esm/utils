"""Functions to rebin binned data poins

Implements: `rebin_1d`, `rebin_2d`.

This requires you to install this utils library with the optional `modeling` dependency:

```bash
pip install "tum_esm_utils[modeling]"
# or
pdm add "tum_esm_utils[modeling]"
```"""

from typing import Any
import numpy as np


def _rebin_first_dimension(
    arr: np.ndarray[Any, Any],
    new_bin_count: int,
) -> np.ndarray[Any, Any]:
    """Internal rebinning function."""

    old_bin_count = len(arr)
    new_bins = np.zeros(shape=(new_bin_count, *arr.shape[1:]), dtype=np.float64)
    scale = old_bin_count / new_bin_count
    for i in range(new_bin_count):
        start = i * scale
        end = (i + 1) * scale
        left = int(np.floor(start))
        right = int(np.floor(end))

        if left == right:
            new_bins[i] += arr[left] * (end - start)
        else:
            new_bins[i] += arr[left] * (left + 1 - start)
            for j in range(left + 1, right):
                new_bins[i] += arr[j]
            if right < old_bin_count:
                new_bins[i] += arr[right] * (end - right)
    return new_bins


def rebin_1d(
    arr: np.ndarray[Any, Any],
    new_bin_count: int,
) -> np.ndarray[Any, Any]:
    """Rebins a 1D array to a new number of bins."""
    if len(arr.shape) != 1:
        raise ValueError("Input array must be 1D.")
    return _rebin_first_dimension(arr, new_bin_count)


def rebin_2d(
    arr: np.ndarray[Any, Any],
    new_x_bins: int,
    new_y_bins: int,
) -> np.ndarray[Any, Any]:
    """Rebins a 2D array to new number of bins in x and y dimensions."""
    return _rebin_first_dimension(_rebin_first_dimension(arr.T, new_x_bins).T, new_y_bins)
