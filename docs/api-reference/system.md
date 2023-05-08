<!-- markdownlint-disable -->

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/system.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `system`
Common system status related functions. 

Implements: `get_cpu_usage`, `get_memory_usage`, `get_disk_space`, `get_system_battery`, `get_last_boot_time`, `get_utc_offset` 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/system.py#L10"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_cpu_usage`

```python
get_cpu_usage() → list[float]
```

returns cpu_percent for all cores -> list [cpu1%, cpu2%,...] 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/system.py#L15"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_memory_usage`

```python
get_memory_usage() → float
```

returns -> tuple (total, available, percent, used, free, active, inactive, buffers, cached, shared, slab) 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/system.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_disk_space`

```python
get_disk_space() → float
```

Returns disk space used in % as float. 
-> tuple (total, used, free, percent) 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/system.py#L30"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_system_battery`

```python
get_system_battery() → int
```

Returns system battery in percent as an integer (1-100). Returns 100 if device has no battery. 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/system.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_last_boot_time`

```python
get_last_boot_time() → str
```

Returns last OS boot time. 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/system.py#L46"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_utc_offset`

```python
get_utc_offset() → float
```

Returns the UTC offset of the system 


