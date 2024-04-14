# API Reference 


Python utilities by the Professorship of Environmental
Sensing and Modeling at the Technical University of Munich.

GitHub Repository https://github.com/tum-esm/utils
Documentation: https://tum-esm-utils.netlify.app
PyPI: https://pypi.org/project/tum-esm-utils


## `tum_esm_utils.code`

Functions for interacting with GitHub and GitLab.

Implements: `request_github_file`, `request_gitlab_file`


##### `request_github_file`

```python
def request_github_file(repository: str,
                        filepath: str,
                        access_token: Optional[str] = None,
                        branch_name: str = "main",
                        timeout: int = 10) -> str
```

Sends a request and returns the content of the response, as a string.
Raises an HTTPError if the response status code is not 200.

**Arguments**:

- `repository` - In the format "owner/repo".
- `filepath` - The path to the file in the repository.
- `access_token` - The GitHub access token. Only required if the repo is private.
- `branch_name` - The branch name.
- `timeout` - The request timeout in seconds.
  

**Returns**:

  The content of the file as a string.


##### `request_gitlab_file`

```python
def request_gitlab_file(repository: str,
                        filepath: str,
                        access_token: Optional[str] = None,
                        branch_name: str = "main",
                        hostname: str = "gitlab.com",
                        timeout: int = 10) -> str
```

Sends a request and returns the content of the response, as a string.
Raises an HTTPError if the response status code is not 200.

**Arguments**:

- `repository` - In the format "owner/repo".
- `filepath` - The path to the file in the repository.
- `access_token` - The GitLab access token. Only required if the repo is private.
- `branch_name` - The branch name.
- `hostname` - The GitLab hostname.
- `timeout` - The request timeout in seconds.
  

**Returns**:

  The content of the file as a string.


## `tum_esm_utils.datastructures`

Datastructures not in the standard library.

Implements: `RingList`, `merge_dicts`


## `RingList` Objects

```python
class RingList()
```


##### `clear`

```python
def clear() -> None
```

removes all elements


##### `is_full`

```python
def is_full() -> bool
```

returns true if list is full


##### `append`

```python
def append(x: float) -> None
```

appends an element to the list


##### `get`

```python
def get() -> list[float]
```

returns the list of elements


##### `sum`

```python
def sum() -> float
```

returns the max size of the list


##### `set_max_size`

```python
def set_max_size(new_max_size: int) -> None
```

sets a new max size


##### `merge_dicts`

```python
def merge_dicts(old_object: Any, new_object: Any) -> Any
```

For a given dict, update it recursively from a new dict.
It will not add any properties and assert that the types
remain the same (or null). null->int or int->null is possible
but not int->dict or list->int.

example:
```python
merge_dicts(
    old_object={"a": 3, "b": {"c": 50, "e": None}},
    new_object={"b": {"e": 80}},
) == {"a": 3, "b": {"c": 50, "e": 80}}
```


## `tum_esm_utils.decorators`

Decorators that can be used wrap functions.

Implements: `with_filelock`


## `with_filelock` Objects

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

A timeout of -1 means that the code waits forever.


## `tum_esm_utils.em27`

Functions for interacting with EM27 interferograms.

Implements: `detect_corrupt_ifgs`


##### `detect_corrupt_ifgs`

```python
def detect_corrupt_ifgs(ifg_directory: str,
                        silent: bool = True,
                        fortran_compiler: Literal["gfortran",
                                                  "gfortran-9"] = "gfortran",
                        force_recompile: bool = False) -> dict[str, list[str]]
```

Returns dict[filename, list[error_messages]] for all
corrupt interferograms in the given directory.

It will compile the fortran code using a given compiler
to perform this task. The fortran code is derived from
the preprocess source code of Proffast 2
(https://www.imk-asf.kit.edu/english/3225.php). We use
it because the retrieval using Proffast 2 will fail if
there are corrupt interferograms in the input.


##### `load_proffast2_result`

```python
def load_proffast2_result(path: str) -> Any
```

Loads the output of Proffast 2 into a polars DataFrame.

This requires you to install this utils library with the optional polars dependency:


```bash
pip install "tum_esm_utils[polars]"
## `or`
pdm add "tum_esm_utils[polars]"
```

**Arguments**:

- `path` - The path to the Proffast 2 output file.
  

**Returns**:

  A polars DataFrame containing all columns.
  

**Raises**:

- `ImportError` - If the polars library is not installed.


## `tum_esm_utils.files`

File-related utility functions.

Implements: `load_file`, `dump_file`, `load_json_file`,
`dump_json_file`, `get_parent_dir_path`, `get_dir_checksum`,
`get_file_checksum`, `rel_to_abs_path`


##### `get_parent_dir_path`

```python
def get_parent_dir_path(script_path: str, current_depth: int = 1) -> str
```

Get the absolute path of a parent directory based on the
current script path. Simply pass the `__file__` variable of
the current script to this function. Depth of 1 will return
the direct parent directory of the current script.


##### `get_dir_checksum`

```python
def get_dir_checksum(path: str) -> str
```

Get the checksum of a directory using md5deep.


##### `get_file_checksum`

```python
def get_file_checksum(path: str) -> str
```

Get the checksum of a file using MD5 from `haslib`.

Significantly faster than `get_dir_checksum` since it does
not spawn a new process.


##### `rel_to_abs_path`

```python
def rel_to_abs_path(*path: str) -> str
```

Convert a path relative to the caller's file to an absolute path.

Inside file `/home/somedir/somepath/somefile.py`, calling
`rel_to_abs_path("..", "config", "config.json")` will
return `/home/somedir/config/config.json`.

Credits to https://stackoverflow.com/a/59004672/8255842


##### `read_last_n_lines`

```python
def read_last_n_lines(file_path: str,
                      n: int,
                      ignore_trailing_whitespace: bool = False) -> List[str]
```

Read the last `n` lines of a file.

The function returns less than `n` lines if the file has less than `n` lines.
The last element in the list is the last line of the file.

This function uses seeking in order not to read the full file. The simple
approach of reading the last 10 lines would be:

```python
with open(path, "r") as f:
    return f.read().split("\n")[:-10]
```

However, this would read the full file and if we only need to read 10 lines
out of a 2GB file, this would be a big waste of resources.

The `ignore_trailing_whitespace` option to crop off trailing whitespace, i.e.
only return the last `n` lines that are not empty or only contain whitespace.


## `tum_esm_utils.mathematics`

Mathematical functions.

Implements: `distance_between_angles`


##### `distance_between_angles`

```python
def distance_between_angles(angle_1: float, angle_2: float) -> float
```

calculate the directional distance (in degrees) between two angles


## `tum_esm_utils.plotting`


## `tum_esm_utils.processes`

Functions to start and terminate background processes.

Implements: `get_process_pids`, `start_background_process`,
`terminate_process`


##### `get_process_pids`

```python
def get_process_pids(script_path: str) -> list[int]
```

Return a list of PIDs that have the given script as their entrypoint


##### `start_background_process`

```python
def start_background_process(interpreter_path: str, script_path: str) -> int
```

Start a new background process with nohup with a given python
interpreter and script path. The script paths parent directory
will be used as the working directory for the process.


##### `terminate_process`

```python
def terminate_process(script_path: str,
                      termination_timeout: Optional[int] = None) -> list[int]
```

Terminate all processes that have the given script as their
entrypoint. Returns the list of terminated PIDs.

If `termination_timeout` is not None, the processes will be
terminated forcefully after the given timeout (in seconds).


## `tum_esm_utils.shell`

Implements custom logging functionality, because the
standard logging module is hard to configure for special
cases.

Implements: `run_shell_command`, `CommandLineException`,
`get_hostname`, `get_commit_sha`, `change_file_permissions`


##### `run_shell_command`

```python
def run_shell_command(command: str,
                      working_directory: Optional[str] = None,
                      executable: str = "/bin/bash") -> str
```

runs a shell command and raises a `CommandLineException`
if the return code is not zero, returns the stdout. Uses
`/bin/bash` by default.

**Arguments**:

- `command` - The command to run.
- `working_directory` - The working directory for the command.
- `executable` - The shell executable to use.
  

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


## `tum_esm_utils.system`

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

```python
x = get_utc_offset()
local time == utc time + x
```

Credits to https://stackoverflow.com/a/35058476/8255842


## `tum_esm_utils.testing`

Functions commonly used in testing scripts.

Implements: `expect_file_contents`, `wait_for_condition`


##### `expect_file_contents`

```python
def expect_file_contents(filepath: str,
                         required_content_blocks: list[str] = [],
                         forbidden_content_blocks: list[str] = []) -> None
```

Assert that the given file contains all of the required content
blocks, and/or none of the forbidden content blocks.


##### `wait_for_condition`

```python
def wait_for_condition(is_successful: Callable[[], bool],
                       timeout_message: str,
                       timeout_seconds: float = 5,
                       check_interval_seconds: float = 0.25) -> None
```

Wait for the given condition to be true, or raise a TimeoutError
if the condition is not met within the given timeout.

`check_interval_seconds` controls, how long to wait inbetween
`is_successful()` calls.


## `tum_esm_utils.text`

Functions used for text manipulation/processing.

Implements: `get_random_string`, `pad_string`, `is_date_string`,
`is_rfc3339_datetime_string`, `insert_replacements`


##### `get_random_string`

```python
def get_random_string(length: int, forbidden: list[str] = []) -> str
```

Return a random string from lowercase letter, the strings
from the list passed as `forbidden` will not be generated


##### `is_date_string`

```python
def is_date_string(date_string: str) -> bool
```

Returns `True` if string is in a valid `YYYYMMDD` format


##### `is_rfc3339_datetime_string`

```python
def is_rfc3339_datetime_string(rfc3339_datetime_string: str) -> bool
```

Returns `True` if string is in a valid `YYYY-MM-DDTHH:mm:ssZ` (RFC3339)
format. Caution: The appendix of `+00:00` is required for UTC!


##### `insert_replacements`

```python
def insert_replacements(content: str, replacements: dict[str, str]) -> str
```

For every key in replacements, replaces `%key%` in the
content with its value.


## `tum_esm_utils.timing`

Functions used for timing or time calculations.

Implements: `date_range`, `ensure_section_duration`, `set_alarm`,
`clear_alarm`


##### `date_range`

```python
def date_range(from_date: datetime.date,
               to_date: datetime.date) -> List[datetime.date]
```

Returns a list of dates between from_date and to_date (inclusive).


##### `ensure_section_duration`

```python
@contextlib.contextmanager
def ensure_section_duration(duration: float) -> Generator[None, None, None]
```

Make sure that the duration of the section is at least the given duration.

Usage example - do one measurement every 6 seconds:

```python
with ensure_section_duration(6):
    do_measurement()
```


##### `set_alarm`

```python
def set_alarm(timeout: int, label: str) -> None
```

Set an alarm that will raise a `TimeoutError` after
`timeout` seconds. The message will be formatted as
`{label} took too long (timed out after {timeout} seconds)`.


##### `clear_alarm`

```python
def clear_alarm() -> None
```

Clear the alarm set by `set_alarm`.


##### `parse_timezone_string`

```python
def parse_timezone_string(timezone_string: str,
                          dt: Optional[datetime.datetime] = None) -> float
```

Parse a timezone string and return the offset in hours.

Why does this function exist? The `strptime` function cannot parse strings
other than "±HHMM". This function can also parse strings in the format "±H"
("+2", "-3", "+5.5"), and "±HH:MM".

**Examples**:

  
```python
parse_timezone_string("GMT")        # returns 0
parse_timezone_string("GMT+2")      # returns 2
parse_timezone_string("UTC+2.0")    # returns 2
parse_timezone_string("UTC-02:00")  # returns -2
```
  
  You are required to pass a datetime object in case the utc offset for the
  passed timezone is not constant - e.g. for "Europe/Berlin".


## `tum_esm_utils.validators`

Implements validator utils for use with pydantic models.

Implements: `StrictFilePath`, `StrictDirectoryPath`


## `StrictFilePath` Objects

```python
class StrictFilePath(pydantic.RootModel[str])
```

A pydantic model that validates a file path.

Example usage:

```python
class MyModel(pyndatic.BaseModel):
    path: StrictFilePath

m = MyModel(path='/path/to/file') # validates that the file exists
```

The validation can be ignored by setting the context variable:

```python
m = MyModel.model_validate(
    {"path": "somenonexistingpath"},
    context={"ignore-path-existence": True},
) # does not raise an error
```


## `StrictDirectoryPath` Objects

```python
class StrictDirectoryPath(pydantic.RootModel[str])
```

A pydantic model that validates a directory path.

Example usage:

```python
class MyModel(pyndatic.BaseModel):
    path: StrictDirectoryPath

m = MyModel(path='/path/to/directory') # validates that the directory exists
```

The validation can be ignored by setting the context variable:

```python
m = MyModel.model_validate(
    {"path": "somenonexistingpath"},
    context={"ignore-path-existence": True},
) # does not raise an error
```

