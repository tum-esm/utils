# `tum_esm_utils.column.astronomy` API Reference


Functions to perform astronomical calculations


### `Astronomy` Objects

```python
class Astronomy()
```

Astronomy utilities.


##### `__init__`

```python
def __init__() -> None
```

Initializes the Astronomy class, downloads the latest `de421.bsp` dataset.


##### `get_sun_position`

```python
def get_sun_position(lat: float, lon: float, alt_asl: float,
                     dt: datetime.datetime) -> tuple[float, float]
```

Computes current sun elevation and azimuth in degrees.

