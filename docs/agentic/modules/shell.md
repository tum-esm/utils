# `tum_esm_utils.shell` API Reference


Implements custom logging functionality, because the
standard logging module is hard to configure for special
cases.

Implements: `run_shell_command`, `CommandLineException`,
`get_hostname`, `get_commit_sha`, `change_file_permissions`


### `CommandLineException` Objects

```python
class CommandLineException(Exception)
```

Exception raised for errors in the command line.


##### `run_shell_command`

```python
def run_shell_command(
        command: str,
        working_directory: Optional[str] = None,
        executable: Optional[str] = "/bin/bash",
        environment_variables: Optional[dict[str, str]] = None) -> str
```

runs a shell command and raises a `CommandLineException`
if the return code is not zero, returns the stdout. Uses
`/bin/bash` by default.

**Arguments**:

- `command` - The command to run.
- `working_directory` - The working directory for the command.
- `executable` - The shell executable to use.
- `environment_variables` - A dictionary of environment variables to set for the command.
  

**Returns**:

  The stdout of the command as a string.


##### `get_hostname`

```python
def get_hostname() -> str
```

returns the hostname of the device, removes network
postfix (`somename.local`) if present. Only works reliably,
when the hostname doesn't contain a dot.


##### `get_commit_sha`

```python
def get_commit_sha(
        variant: Literal["short", "long"] = "short") -> Optional[str]
```

Get the current commit sha of the repository. Returns
`None` if there is not git repository in any parent directory.

**Arguments**:

- `variant` - "short" or "long" to specify the length of the sha.
  

**Returns**:

  The commit sha as a string, or `None` if there is no git
  repository in the parent directories.


##### `change_file_permissions`

```python
def change_file_permissions(file_path: str, permission_string: str) -> None
```

Change a file's system permissions.

Example permission_strings: `--x------`, `rwxr-xr-x`, `rw-r--r--`.

**Arguments**:

- `file_path` - The path to the file.
- `permission_string` - The new permission string.

