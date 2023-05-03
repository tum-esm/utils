<!-- markdownlint-disable -->

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/decorators.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `decorators`





---

<a href="https://github.com/tum-esm/utils/tree/main/decorators/ensure_section_duration#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/decorators.py#L12"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `with_filelock`
FileLock = Mark, that a file is being used and other programs should not interfere. A file "*.lock" will be created and the content of this file will make the wrapped function possibly wait until other programs are done using it. 

See https://en.wikipedia.org/wiki/Semaphore_(programming) 

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/decorators.py#L22"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(lockfile_path: str, timeout: float = -1) → None
```

A timeout of -1 means that the code waits forever. 





