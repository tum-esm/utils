# `tum_esm_utils.column.averaging_kernel` API Reference


Functions to store, load and apply a column averaging kernel.


### `ColumnAveragingKernel` Objects

```python
class ColumnAveragingKernel()
```

A class to store, load and apply a column averaging kernel.


##### `__init__`

```python
def __init__(szas: np.ndarray[Any, Any],
             pressures: np.ndarray[Any, Any],
             aks: Optional[np.ndarray[Any, Any]] = None) -> None
```

Initialize the ColumnAveragingKernel.

**Arguments**:

- `szas` - The solar zenith angles (SZAs) in degrees.
- `pressures` - The pressures in hPa.
- `aks` - The averaging kernels. If None, a zero array is created.


##### `apply`

```python
def apply(szas: np.ndarray[Any, Any],
          pressures: np.ndarray[Any, Any]) -> np.ndarray[Any, Any]
```

Compute the averaging kernel for a given set of szas and pressures.


```python
ak.apply(
    szas=np.array([0, 10, 20]),
    pressures=np.array([900, 800, 700])
)
```

**Returns**:

  
```
[
   AK @  0° SZA and 900 hPa,
   AK @ 10° SZA and 800 hPa,
   AK @ 20° SZA and 700 hPa
]
```


##### `dump`

```python
def dump(filepath: str) -> None
```

Dump the ColumnAveragingKernel to a JSON file.


##### `load`

```python
@staticmethod
def load(filepath: str) -> ColumnAveragingKernel
```

Load the ColumnAveragingKernel from a JSON file.

