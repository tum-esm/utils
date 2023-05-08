<!-- markdownlint-disable -->

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/shell.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `shell`
Implements custom logging functionality, because the standard logging module is hard to configure for special cases. 

Implements: `run_shell_command`, `CommandLineException`, `get_hostname`, `get_commit_sha`, `change_file_permissions` 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/shell.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `run_shell_command`

```python
run_shell_command(
    command: str,
    working_directory: Optional[str] = None,
    executable: str = '/bin/bash'
) → str
```

runs a shell command and raises a `CommandLineException` if the return code is not zero, returns the stdout. Uses `/bin/bash` by default. 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/shell.py#L54"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `get_hostname`

```python
get_hostname() → str
```

returns the hostname of the device, removes network postfix (`somename.local`) if present. Only works reliably, when the hostname doesn't contain a dot. 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/shell.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `get_commit_sha`

```python
get_commit_sha() → Optional[str]
```

Get the current commit sha of the repository. Returns `None` if there is not git repository in any parent directory. 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/shell.py#L83"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `change_file_permissions`

```python
change_file_permissions(file_path: str, permission_string: str) → None
```

Change a file's system permissions. 

Example permission_strings: `--x------`, `rwxr-xr-x`, `rw-r--r--`. 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/shell.py#L14"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `CommandLineException`




<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/shell.py#L15"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `__init__`

```python
__init__(value: str, details: Optional[str] = None) → None
```









