<!-- markdownlint-disable -->

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/files.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `files`





---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/files.py#L6"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `load_file`

```python
load_file(path: str) → str
```






---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/files.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `dump_file`

```python
dump_file(path: str, content: str) → None
```






---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/files.py#L16"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `load_json_file`

```python
load_json_file(path: str) → Any
```






---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/files.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `dump_json_file`

```python
dump_json_file(path: str, content: Any) → None
```






---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/files.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_parent_dir_path`

```python
get_parent_dir_path(script_path: str, current_depth: int = 1) → str
```

Get the absolute path of a parent directory based on the current script path. Simply pass the `__file__` variable of the current script to this function. Depth of 1 will return the direct parent directory of the current script. 


