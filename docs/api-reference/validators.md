<!-- markdownlint-disable -->

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/validators.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `validators`





---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/validators.py#L17"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `validate_bool`

```python
validate_bool() → Callable[[Any, bool], bool]
```






---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/validators.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `validate_float`

```python
validate_float(
    nullable: bool = False,
    minimum: Optional[float] = None,
    maximum: Optional[float] = None
) → Callable[[Any, float], float]
```






---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/validators.py#L48"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `validate_int`

```python
validate_int(
    nullable: bool = False,
    minimum: Optional[int] = None,
    maximum: Optional[int] = None,
    allowed: Optional[list[int]] = None,
    forbidden: Optional[list[int]] = None
) → Callable[[Any, Optional[int]], Optional[int]]
```






---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/validators.py#L76"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `validate_str`

```python
validate_str(
    nullable: bool = False,
    min_len: Optional[float] = None,
    max_len: Optional[float] = None,
    allowed: Optional[list[str]] = None,
    regex: Optional[str] = None,
    is_numeric: bool = False,
    is_directory: bool = False,
    is_file: bool = False,
    is_date_string: bool = False
) → Callable[[Any, str], str]
```






