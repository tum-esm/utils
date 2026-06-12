# `tum_esm_utils.sqlitelock` API Reference



### `SQLiteLock` Objects

```python
class SQLiteLock()
```

A file lock based on SQLite transactions.

The alternative `filelock` package tends to deadlock on our low-spec-CPU
windows machines. The package `portalocker` uses the `pywin32` package
which I am not a big fan of due to its documentation and testing quality.

Usage example:

```python
lock = tum_esm_utils.sqlitelock.SQLiteLock("sqlitelock.lock", timeout=5)

try:
    with lock:
        # critical section
        pass
except TimeoutError:
    # could not be acquired within 5 seconds
    pass
```

This function is tested on Windows, Linux.


##### `__init__`

```python
def __init__(filepath: str = "sqlitelock.lock",
             timeout: float = 10,
             poll_interval: float = 0.1) -> None
```

Initialize the SqliteFileLock.

**Arguments**:

- `filepath` - The path to the SQLite database file used for locking.
- `timeout` - The maximum time to wait for acquiring the lock in seconds.
- `poll_interval` - The interval between lock acquisition attempts in seconds.


##### `acquire`

```python
def acquire(timeout: Optional[float] = None) -> None
```

Acquire the lock.

**Arguments**:

- `timeout` - Optional timeout in seconds. If None, uses the default timeout set during initialization.
  

**Raises**:

- `TimeoutError` - If the lock could not be acquired within the specified timeout.


##### `release`

```python
def release() -> None
```

Release the lock.


##### `is_locked`

```python
def is_locked() -> bool
```

Check if the lock is currently held by any process.

