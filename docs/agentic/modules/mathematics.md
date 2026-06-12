# `tum_esm_utils.mathematics` API Reference


Mathematical functions.

Implements: `distance_between_angles`


##### `distance_between_angles`

```python
def distance_between_angles(angle_1: float, angle_2: float) -> float
```

Calculate the directional distance (in degrees) between two angles.


##### `divides_evenly`

```python
def divides_evenly(dividend: float,
                   divisor: float,
                   precision: int = 6) -> bool
```

Check if divisor divides dividend evenly.

Normally this shoudld be done by `dividend % divisor == 0`, but this
can lead to floating point errors, i.e. `1 % 0.1 == 0.09999999999999998`.
Using `math.fmod` also does not seem to work correctly with floats.

