# `tum_esm_utils.decorators` API Reference


Decorators that can be used wrap functions.

Implements: `with_filelock`


### `with_filelock` Objects

```python
class with_filelock()
```

FileLock = Mark, that a file is being used and other programs
should not interfere. A file "*.lock" will be created and the
content of this file will make the wrapped function possibly
wait until other programs are done using it.

See https://en.wikipedia.org/wiki/Semaphore_(programming).


Credits for the typing of higher level decorators goes to
https://github.com/python/mypy/issues/1551#issuecomment-253978622.


##### `__init__`

```python
def __init__(lockfile_path: str, timeout: float = -1) -> None
```

Create a new filelock decorator.

A timeout of -1 means that the code waits forever.

**Arguments**:

- `lockfile_path` - The path to the lockfile.
- `timeout` - The time to wait for the lock in seconds.

