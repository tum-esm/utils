<!-- markdownlint-disable -->

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/files.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `files`
File-related utility functions. 

Implements: `load_file`, `dump_file`, `load_json_file`, `dump_json_file`, `get_parent_dir_path`, `get_dir_checksum`, `get_file_checksum`, `load_raw_proffast_output` 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/files.py#L15"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `load_file`

```python
load_file(path: str) → str
```






---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/files.py#L20"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `dump_file`

```python
dump_file(path: str, content: str) → None
```






---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/files.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `load_json_file`

```python
load_json_file(path: str) → Any
```






---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/files.py#L30"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `dump_json_file`

```python
dump_json_file(path: str, content: Any, indent: Optional[int] = 4) → None
```






---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/files.py#L35"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_parent_dir_path`

```python
get_parent_dir_path(script_path: str, current_depth: int = 1) → str
```

Get the absolute path of a parent directory based on the current script path. Simply pass the `__file__` variable of the current script to this function. Depth of 1 will return the direct parent directory of the current script. 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/files.py#L47"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_dir_checksum`

```python
get_dir_checksum(path: str) → str
```

Get the checksum of a directory using md5deep. 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/files.py#L56"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_file_checksum`

```python
get_file_checksum(path: str) → str
```

Get the checksum of a file using MD5 from `haslib`. 

Significantly faster than `get_dir_checksum` since it does not spawn a new process. 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/files.py#L67"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `load_raw_proffast_output`

```python
load_raw_proffast_output(
    path: str,
    selected_columns: list[str] = ['gnd_p', 'gnd_t', 'app_sza', 'azimuth', 'xh2o', 'xair', 'xco2', 'xch4', 'xco', 'xch4_s5p']
) → DataFrame
```

Returns a raw proffast output file as a dataframe. 

you can pass `selected_columns` to only keep some columns - the `utc` column will always be included. Example: 

```
utc                     gnd_p    gnd_t    app_sza   ...
2021-10-20 07:00:23     950.91   289.05   78.45     ...
2021-10-20 07:00:38     950.91   289.05   78.42     ...
2021-10-20 07:01:24     950.91   289.05   78.31     ...
...                     ...      ...      ...       ...
[1204 rows x 8 columns]
``` 


