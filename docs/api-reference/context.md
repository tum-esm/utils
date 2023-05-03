<!-- markdownlint-disable -->

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/context.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `context`





---

<a href="https://github.com/tum-esm/utils/tree/main/context/ensure_section_duration#L6"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `ensure_section_duration`

```python
ensure_section_duration(
    duration: float
) → Generator[NoneType, NoneType, NoneType]
```

Make sure that the duration of the section is at least the given duration. 

Usage example - do one measurement every 6 seconds: 

```python
with ensure_section_duration(6):
     do_measurement()
``` 


