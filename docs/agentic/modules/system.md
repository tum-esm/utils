# `tum_esm_utils.system` API Reference


Common system status related functions.

Implements: `get_cpu_usage`, `get_memory_usage`, `get_disk_space`,
`get_system_battery`, `get_last_boot_time`, `get_utc_offset`


##### `get_cpu_usage`

```python
def get_cpu_usage() -> list[float]
```

Checks the CPU usage of the system.

**Returns**:

  The CPU usage in percent for each core.


##### `get_memory_usage`

```python
def get_memory_usage() -> float
```

Checks the memory usage of the system.

**Returns**:

  The memory usage in percent.


##### `get_physical_memory_usage`

```python
def get_physical_memory_usage() -> float
```

Returns the memory usage (physical memory) of the current process in MB.


##### `get_disk_space`

```python
def get_disk_space(path: str = "/") -> float
```

Checks the disk space of a given path.

**Arguments**:

- `path` - The path to check the disk space for.
  

**Returns**:

  The available disk space in percent.


##### `get_system_battery`

```python
def get_system_battery() -> Optional[int]
```

Checks the system battery.

**Returns**:

  The battery state in percent if available, else None.


##### `get_last_boot_time`

```python
def get_last_boot_time() -> datetime.datetime
```

Checks the last boot time of the system.


##### `get_utc_offset`

```python
def get_utc_offset() -> float
```

Returns the UTC offset of the system.


Credits to https://stackoverflow.com/a/35058476/8255842

```python
x = get_utc_offset()
local time == utc time + x
```

**Returns**:

  The UTC offset in hours.

