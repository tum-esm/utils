# API Reference 


Python utilities by the Professorship of Environmental
Sensing and Modeling at the Technical University of Munich.

GitHub Repository https://github.com/tum-esm/utils
Documentation: https://tum-esm-utils.netlify.app
PyPI: https://pypi.org/project/tum-esm-utils

(Optional) Explicit Imports:

By setting the environment variable `TUM_ESM_UTILS_EXPLICIT_IMPORTS=1`, the
package disables automatic submodule imports. This means you cannot import the
whole package and access submodules directly (e.g., `tum_esm_utils.code` will
not be available after `import tum_esm_utils`). Instead, you must explicitly
import each submodule, e.g. `from tum_esm_utils import code` or
`import tum_esm_utils.code`.

This reduces the import time of the package by up to 60 times


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


##### `download_github_release_asset`

```python
def download_github_release_asset(repository: str,
                                  asset_name: str,
                                  dst_dir: str,
                                  final_name: Optional[str] = None,
                                  access_token: Optional[str] = None,
                                  force: bool = False) -> None
```

Downloads a specific asset from the latest release of a GitHub repository.

Not supported on windows!

**Arguments**:

- `repository` - In the format "owner/repo".
- `asset_name` - The name of the asset to download.
- `dst_dir` - The directory where the asset will be saved.
- `final_name` - Optional final name for the downloaded asset. If None, uses `asset_name`.
- `access_token` - The GitHub access token. Only required if the repo is private.
- `force` - If True, forces the download even if the file already exists.


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


## `tum_esm_utils.column`

Functions related to column observation data.


## `tum_esm_utils.column.astronomy`


### `Astronomy` Objects

```python
class Astronomy()
```

Astronomy utilities.


##### `__init__`

```python
def __init__() -> None
```

Initializes the Astronomy class, downloads the latest `de421.bsp` dataset.


##### `get_sun_position`

```python
def get_sun_position(lat: float, lon: float, alt_asl: float,
                     dt: datetime.datetime) -> tuple[float, float]
```

Computes current sun elevation and azimuth in degrees.


## `tum_esm_utils.column.averaging_kernel`

Functions to store, load and apply a column averaging kernel.


### `ColumnAveragingKernel` Objects

```python
class ColumnAveragingKernel()
```

A class to store, load and apply a column averaging kernel.


##### `__init__`

```python
def __init__(szas: np.ndarray[Any, Any],
             pressures: np.ndarray[Any, Any],
             aks: Optional[np.ndarray[Any, Any]] = None) -> None
```

Initialize the ColumnAveragingKernel.

**Arguments**:

- `szas` - The solar zenith angles (SZAs) in degrees.
- `pressures` - The pressures in hPa.
- `aks` - The averaging kernels. If None, a zero array is created.


##### `apply`

```python
def apply(szas: np.ndarray[Any, Any],
          pressures: np.ndarray[Any, Any]) -> np.ndarray[Any, Any]
```

Compute the averaging kernel for a given set of szas and pressures.


```python
ak.apply(
    szas=np.array([0, 10, 20]),
    pressures=np.array([900, 800, 700])
)
```

**Returns**:

  
```
[
   AK @  0° SZA and 900 hPa,
   AK @ 10° SZA and 800 hPa,
   AK @ 20° SZA and 700 hPa
]
```


##### `dump`

```python
def dump(filepath: str) -> None
```

Dump the ColumnAveragingKernel to a JSON file.


##### `load`

```python
@staticmethod
def load(filepath: str) -> ColumnAveragingKernel
```

Load the ColumnAveragingKernel from a JSON file.


## `tum_esm_utils.column.ncep_profiles`

Functions to read NCEP profiles.


##### `load_ggg2020_map`

```python
def load_ggg2020_map(filepath: str) -> pl.DataFrame
```

Load the Atmospheric profile from a GGG2020 map file.


##### `load_ggg2020_mod`

```python
def load_ggg2020_mod(filepath: str) -> pl.DataFrame
```

Load the Atmospheric profile from a GGG2020 mod file.


##### `load_ggg2020_vmr`

```python
def load_ggg2020_vmr(filepath: str) -> pl.DataFrame
```

Load the Atmospheric profile from a GGG2020 vmr file.


## `tum_esm_utils.datastructures`

Datastructures not in the standard library.

Implements: `RingList`, `merge_dicts`


### `RingList` Objects

```python
class RingList()
```


##### `__init__`

```python
def __init__(max_size: int)
```

Initialize a RingList with a maximum size.


##### `clear`

```python
def clear() -> None
```

Removes all elements from the list.


##### `is_full`

```python
def is_full() -> bool
```

Returns True if the list is full.


##### `append`

```python
def append(x: float) -> None
```

Appends an element to the list.


##### `get`

```python
def get() -> list[float]
```

Returns the list of elements.


##### `sum`

```python
def sum() -> float
```

Returns the max size of the list


##### `set_max_size`

```python
def set_max_size(new_max_size: int) -> None
```

Sets a new max size fo the list.


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


##### `concat_lists`

```python
def concat_lists(*lists: list[T]) -> list[T]
```

Concatenates multiple lists into one list.


##### `chunk_list`

```python
def chunk_list(xs: list[T], n: int) -> list[list[T]]
```

Split a list into chunks of size n.


## `tum_esm_utils.decorators`

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


## `tum_esm_utils.em27`

Functions for interacting with EM27 interferograms.

Implements: `detect_corrupt_opus_files`, `load_proffast2_result`.

This requires you to install this utils library with the optional `em27` dependency:

```bash
pip install "tum_esm_utils[em27]"
## `or`
pdm add "tum_esm_utils[em27]"
```


##### `detect_corrupt_opus_files`

```python
def detect_corrupt_opus_files(
        ifg_directory: str,
        silent: bool = True,
        fortran_compiler: Literal["gfortran", "gfortran-9"] = "gfortran",
        force_recompile: bool = False) -> dict[str, list[str]]
```

Returns dict[filename, list[error_messages]] for all
corrupt opus files in the given directory.

It will compile the fortran code using a given compiler
to perform this task. The fortran code is derived from
the preprocess source code of Proffast 2
(https://www.imk-asf.kit.edu/english/3225.php). We use
it because the retrieval using Proffast 2 will fail if
there are corrupt interferograms in the input.

**Arguments**:

- `ifg_directory` - The directory containing the interferograms.
- `silent` - If set to False, print additional information.
- `fortran_compiler` - The fortran compiler to use.
- `force_recompile` - If set to True, the fortran code will be recompiled.
  

**Returns**:

  A dictionary containing corrupt filenames as keys and a list of error
  messages as values.


##### `detect_corrupt_ifgs`

```python
@deprecated("This will be removed in the next breaking release. Please use " +
            "the identical function `detect_corrupt_opus_files` instead.")
def detect_corrupt_ifgs(ifg_directory: str,
                        silent: bool = True,
                        fortran_compiler: Literal["gfortran",
                                                  "gfortran-9"] = "gfortran",
                        force_recompile: bool = False) -> dict[str, list[str]]
```

Returns dict[filename, list[error_messages]] for all
corrupt opus files in the given directory.

It will compile the fortran code using a given compiler
to perform this task. The fortran code is derived from
the preprocess source code of Proffast 2
(https://www.imk-asf.kit.edu/english/3225.php). We use
it because the retrieval using Proffast 2 will fail if
there are corrupt interferograms in the input.

**Arguments**:

- `ifg_directory` - The directory containing the interferograms.
- `silent` - If set to False, print additional information.
- `fortran_compiler` - The fortran compiler to use.
- `force_recompile` - If set to True, the fortran code will be recompiled.
  

**Returns**:

  A dictionary containing corrupt filenames as keys and a list of error
  messages as values.


##### `load_proffast2_result`

```python
def load_proffast2_result(path: str) -> pl.DataFrame
```

Loads the output of Proffast 2 into a polars DataFrame.

**Arguments**:

- `path` - The path to the Proffast 2 output file.
  

**Returns**:

  A polars DataFrame containing all columns.


##### `SERIAL_NUMBERS`

The serial numbers of the EM27 devices.


##### `COLORS`

Colors recommended for plotting the EM27 data.


##### `COLORS_LIGHT`

Lighter colors recommended for plotting the EM27 data.


##### `COLORS_DARK`

Darker colors recommended for plotting the EM27 data.


##### `PROFFAST_MULTIPLIERS`

Multiplication factors for the EM27 data retrieved using Proffast to bring the data in a common unit.


##### `PROFFAST_UNITS`

Units for the EM27 data retrieved using Proffast after applying the multiplication factor.


## `tum_esm_utils.files`

File-related utility functions.

Implements: `load_file`, `dump_file`, `load_json_file`,
`dump_json_file`, `get_parent_dir_path`, `get_dir_checksum`,
`get_file_checksum`, `rel_to_abs_path`, `read_last_n_lines`,
`expect_file_contents`, `render_directory_tree`, `list_directory`


##### `load_file`

```python
def load_file(path: str) -> str
```

Load the content of a file.


##### `dump_file`

```python
def dump_file(path: str, content: str) -> None
```

Dump content to a file.


##### `load_binary_file`

```python
def load_binary_file(path: str) -> bytes
```

Load binary content of a file.


##### `dump_binary_file`

```python
def dump_binary_file(path: str, content: bytes) -> None
```

Dump binary content to a file.


##### `load_json_file`

```python
def load_json_file(path: str) -> Any
```

Load the content of a JSON file.


##### `dump_json_file`

```python
def dump_json_file(path: str, content: Any, indent: Optional[int] = 4) -> None
```

Dump content to a JSON file.


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
                      ignore_trailing_whitespace: bool = False) -> list[str]
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


##### `expect_file_contents`

```python
def expect_file_contents(filepath: str,
                         required_content_blocks: list[str] = [],
                         forbidden_content_blocks: list[str] = []) -> None
```

Assert that the given file contains all of the required content
blocks, and/or none of the forbidden content blocks.

**Arguments**:

- `filepath` - The path to the file.
- `required_content_blocks` - A list of strings that must be present in the file.
- `forbidden_content_blocks` - A list of strings that must not be present in the file.


##### `render_directory_tree`

```python
def render_directory_tree(root: str,
                          ignore: list[str] = [],
                          max_depth: Optional[int] = None,
                          root_alias: Optional[str] = None,
                          directory_prefix: Optional[str] = "📁 ",
                          file_prefix: Optional[str] = "📄 ") -> Optional[str]
```

Render a file tree as a string.

**Example**:

  
```
📁 <config.general.data.results>
├─── 📁 bundle
│    ├─── 📄 __init__.py
│    ├─── 📄 load_results.py
│    └─── 📄 main.py
├─── 📁 profiles
│    ├─── 📄 __init__.py
│    ├─── 📄 cache.py
│    ├─── 📄 download_logic.py
│    ├─── 📄 generate_queries.py
│    ├─── 📄 main.py
│    ├─── 📄 std_site_logic.py
│    └─── 📄 upload_logic.py
├─── 📁 retrieval
│    ├─── 📁 algorithms
...
```
  

**Arguments**:

- `root` - The root directory to render.
- `ignore` - A list of patterns to ignore. If the basename of a directory
  matches any of the patterns, the directory is ignored.
- `max_depth` - The maximum depth to render. If `None`, render the full tree.
- `root_alias` - An alias for the root directory. If `None`, the basename of
  the root directory is used. In the example above, the root
  directory is was aliased to `<config.general.data.results>`.
- `directory_prefix` - The prefix to use for directories.
- `file_prefix` - The prefix to use for files.
  
- `Returns` - The directory tree as a string. If the root directory is ignored, `None`.


##### `list_directory`

```python
def list_directory(path: str,
                   regex: Optional[str] = None,
                   ignore: Optional[list[str]] = None,
                   include_directories: bool = True,
                   include_files: bool = True,
                   include_links: bool = True) -> list[str]
```

List the contents of a directory based on certain criteria. Like `os.listdir`
with superpowers. You can filter the list by a regex or you can ignore Unix shell
style patterns like `*.lock`.

**Arguments**:

- `path` - The path to the directory.
- `regex` - A regex pattern to match the item names against.
- `ignore` - A list of patterns to ignore. If the basename of an item
  matches any of the patterns, the item is ignored.
- `include_directories` - Whether to include directories in the output.
- `include_files` - Whether to include files in the output.
- `include_links` - Whether to include symbolic links in the output.
  
- `Returns` - A list of items in the directory that match the criteria.


## `tum_esm_utils.mathematics`

Mathematical functions.

Implements: `distance_between_angles`


##### `distance_between_angles`

```python
def distance_between_angles(angle_1: float, angle_2: float) -> float
```

Calculate the directional distance (in degrees) between two angles.


##### `divides_evenly`

```python
def divides_evenly(dividend: float,
                   divisor: float,
                   precision: int = 6) -> bool
```

Check if divisor divides dividend evenly.

Normally this shoudld be done by `dividend % divisor == 0`, but this
can lead to floating point errors, i.e. `1 % 0.1 == 0.09999999999999998`.
Using `math.fmod` also does not seem to work correctly with floats.


## `tum_esm_utils.opus`

Functions for interacting with OPUS files.

Implements: `OpusFile`, `OpusHTTPInterface`.

Read https://tccon-wiki.caltech.edu/Main/I2SAndOPUSHeaders for more information
about the file parameters. This requires you to install this utils library with
the optional `opus` dependency:

```bash
pip install "tum_esm_utils[opus]"
## `or`
pdm add "tum_esm_utils[opus]"
```

Credits to Friedrich Klappenbach (friedrich.klappenbach@tum.de) for decoding the OPUS file
format.


## `tum_esm_utils.opus.file_interface`

Functions for interacting with OPUS files.


### `OpusFile` Objects

```python
class OpusFile(pydantic.BaseModel)
```

Interact with OPUS spectrum files.

Credits to Friedrich Klappenbach (friedrich.klappenbach@tum.de) for decoding the OPUS file format.


##### `read`

```python
@staticmethod
def read(filepath: str,
         measurement_timestamp_mode: Literal["start", "end"] = "start",
         interferogram_mode: Literal["skip", "validate", "read"] = "read",
         read_all_channels: bool = True) -> OpusFile
```

Read an interferogram file.

**Arguments**:

- `filepath` - Path to the OPUS file.
- `measurement_timestamp_mode` - Whether the timestamps in the interferograms
  indicate the start or end of the measurement
- `interferogram_mode` - How to handle the interferogram data. "skip"
  will not read the interferogram data, "validate"
  will read the first and last block to check
  for errors during writing, "read" will read
  the entire interferogram. "read" takes about
  11-12 times longer than "skip", "validate" is
  about 20% slower than "skip".
- `read_all_channels` - Whether to read all channels in the file or
  only the first one.
  

**Returns**:

  An OpusFile object, optionally containing the interferogram data (in read mode)


## `tum_esm_utils.opus.http_interface`

Provides a HTTP interface to OPUS.


### `OpusHTTPInterface` Objects

```python
class OpusHTTPInterface()
```

Interface to the OPUS HTTP interface.

It uses the socket library, because the HTTP interface of OPUS does not
reuturn valid HTTP/1 or HTTP/2 headers. It opens and closes a new socket
because OPUS closes the socket after the answer has been sent.

**Raises**:

- `ConnectionError` - If the connection to the OPUS HTTP interface fails or
  if the response is invalid.


##### `request`

```python
@staticmethod
@tenacity.retry(
    retry=tenacity.retry_if_exception_type(ConnectionError),
    reraise=True,
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_fixed(5),
)
def request(request: str,
            timeout: float = 10.0,
            expect_ok: bool = False) -> list[str]
```

Send a request to the OPUS HTTP interface and return the answer.

Commands will be send to `GET http://localhost/OpusCommand.htm?<request>`.
This function will retry the request up to 3 times and wait 5 seconds
inbetween retries.

**Arguments**:

- `request` - The request to send.
- `timeout` - The time to wait for the answer.
- `expect_ok` - Whether the first line of the answer should be "OK".
  

**Returns**:

  The answer lines.


##### `request_without_retry`

```python
@staticmethod
def request_without_retry(request: str,
                          timeout: float = 10.0,
                          expect_ok: bool = False) -> list[str]
```

Send a request to the OPUS HTTP interface and return the answer.

Commands will be send to `GET http://localhost/OpusCommand.htm?<request>`.

**Arguments**:

- `request` - The request to send.
- `timeout` - The time to wait for the answer.
- `expect_ok` - Whether the first line of the answer should be "OK".
  

**Returns**:

  The answer lines.


##### `get_version`

```python
@staticmethod
def get_version() -> str
```

Get the version number, like `20190310`.


##### `get_version_extended`

```python
@staticmethod
def get_version_extended() -> str
```

Get the extended version number, like `8.2 Build: 8, 2, 28 20190310`.


##### `is_working`

```python
@staticmethod
def is_working() -> bool
```

Check if the OPUS HTTP interface is working. Does NOT raise a
`ConnectionError` but only returns `True` or `False`.


##### `get_main_thread_id`

```python
@staticmethod
def get_main_thread_id() -> int
```

Get the process ID of the main thread of OPUS.


##### `some_macro_is_running`

```python
@staticmethod
def some_macro_is_running() -> bool
```

Check if any macro is currently running.

In theory, we could also check whether the correct macro is running using
`READ_PARAMETER MPT` and `READ_PARAMETER MFN`. However, these variables do
not seem to be updated right away, so we cannot rely on them.


##### `get_loaded_experiment`

```python
@staticmethod
def get_loaded_experiment() -> str
```

Get the path to the currently loaded experiment.


##### `load_experiment`

```python
@staticmethod
def load_experiment(experiment_path: str) -> None
```

Load an experiment file.


##### `start_macro`

```python
@staticmethod
def start_macro(macro_path: str) -> int
```

Start a macro. Returns the macro ID.


##### `macro_is_running`

```python
@staticmethod
def macro_is_running(macro_id: int) -> bool
```

Check if the given macro is running. It runs `MACRO_RESULTS <macro_id>`
under the hood. The OPUS documentation is ambiguous about the return value.
It seems that 0 means "there is no result yet", i.e. the macro is still running


##### `stop_macro`

```python
@staticmethod
def stop_macro(macro_path_or_id: str | int) -> None
```

Stop a macro given by its path or ID.

Stopping a macro by its ID only works for our OPUS 8.X installations,
but not our OPUS 7.X installations. Hence, it is recommended to always
stop it by path.


##### `unload_all_files`

```python
@staticmethod
def unload_all_files() -> None
```

Unload all files. This should be done before closing it.


##### `close_opus`

```python
@staticmethod
def close_opus() -> None
```

Close OPUS.


##### `set_parameter_mode`

```python
@staticmethod
def set_parameter_mode(variant: Literal["file", "opus"]) -> None
```

Set the parameter mode to `FILE_PARAMETERS` or `OPUS_PARAMETERS`.


##### `read_parameter`

```python
@staticmethod
def read_parameter(parameter: str) -> str
```

Read the value of a parameter.


##### `write_parameter`

```python
@staticmethod
def write_parameter(parameter: str, value: str | int | float) -> None
```

Update the value of a parameter.


##### `get_language`

```python
@staticmethod
def get_language() -> str
```

Get the current language.


##### `get_username`

```python
@staticmethod
def get_username() -> str
```

Get the current username.


##### `get_path`

```python
@staticmethod
def get_path(literal: Literal["opus", "base", "data", "work"]) -> str
```

Get the path to the given directory.


##### `set_processing_mode`

```python
@staticmethod
def set_processing_mode(
        mode: Literal["command", "execute", "request"]) -> None
```

Set the processing mode to `COMMAND_MODE`, `EXECUTE_MODE`, or `REQUEST_MODE`.


##### `command_line`

```python
@staticmethod
def command_line(command: str) -> Optional[str]
```

Execute a command line command, i.e. `COMMAND_LINE <command>`.


## `tum_esm_utils.plotting`

Better defaults for matplotlib plots and utilities for creating and saving figures.

Implements: `apply_better_defaults`, `create_figure`, `add_subplot`

This requires you to install this utils library with the optional `plotting` dependencies:

```bash
pip install "tum_esm_utils[plotting]"
## `or`
pdm add "tum_esm_utils[plotting]"
```


##### `apply_better_defaults`

```python
def apply_better_defaults(font_family: Optional[str] = "Roboto") -> None
```

Apply better defaults to matplotlib plots.

**Arguments**:

- `font_family` - The font family to use for the plots. If None, the default
  settings are not changed.


##### `create_figure`

```python
@contextlib.contextmanager
def create_figure(path: str,
                  title: Optional[str] = None,
                  width: float = 10,
                  height: float = 10,
                  suptitle_y: float = 0.97,
                  padding: float = 2,
                  dpi: int = 250) -> Generator[plt.Figure, None, None]
```

Create a figure for plotting.

Usage:

```python
with create_figure("path/to/figure.png", title="Title") as fig:
    ...
```

**Arguments**:

- `path` - The path to save the figure to.
- `title` - The title of the figure.
- `width` - The width of the figure.
- `height` - The height of the figure.
- `suptitle_y` - The y-coordinate of the figure title.
- `padding` - The padding of the figure.
- `dpi` - The DPI of the figure.


##### `add_subplot`

```python
def add_subplot(fig: plt.Figure,
                position: tuple[int, int, int]
                | matplotlib.gridspec.SubplotSpec,
                title: Optional[str] = None,
                xlabel: Optional[str] = None,
                ylabel: Optional[str] = None,
                **kwargs: dict[str, Any]) -> plt.Axes
```

Add a subplot to a figure.

Use a gridspec for more control:


```python
gs = matplotlib.gridspec.GridSpec(4, 1, height_ratios=[1, 2, 2, 2])
add_subplot(fig, gs[0], ...)
```

**Arguments**:

- `fig` - The figure to add the subplot to.
- `position` - The position of the subplot. The tuple should contain three
  integers (rows, columns, index). You can also pass a gridspec
  subplot spec.
- `title` - The title of the subplot.
- `xlabel` - The x-axis label of the subplot.
- `ylabel` - The y-axis label of the subplot.
- `**kwargs` - Additional keyword arguments for the subplot.
  

**Returns**:

  An axis object for the new subplot.
  

**Raises**:

- `ValueError` - If the index of the subplot is invalid.


##### `add_colorpatch_legend`

```python
def add_colorpatch_legend(fig: plt.Figure,
                          handles: list[tuple[
                              str,
                              Union[
                                  str,
                                  tuple[float, float, float],
                                  tuple[float, float, float, float],
                              ],
                          ]],
                          ncols: Optional[int] = None,
                          location: str = "upper left") -> None
```

Add a color patch legend to a figure.

**Arguments**:

- `fig` - The figure to add the legend to.
- `handles` - A list of tuples containing the label and color of each patch
  (e.g. `[("Label 1", "red"), ("Label 2", "blue")]`). You can pass any color
  that is accepted by matplotlib.
- `ncols` - The number of columns in the legend.
- `location` - The location of the legend.


## `tum_esm_utils.processes`

Functions to start and terminate background processes.

Implements: `get_process_pids`, `start_background_process`,
`terminate_process`


##### `get_process_pids`

```python
def get_process_pids(script_path: str) -> list[int]
```

Return a list of PIDs that have the given script as their entrypoint.

**Arguments**:

- `script_path` - The absolute path of the python file entrypoint.


##### `start_background_process`

```python
def start_background_process(interpreter_path: str,
                             script_path: str,
                             waiting_period: float = 0.5) -> int
```

Start a new background process with nohup with a given python
interpreter and script path. The script paths parent directory
will be used as the working directory for the process.

**Arguments**:

- `interpreter_path` - The absolute path of the python interpreter.
- `script_path` - The absolute path of the python file entrypoint.
- `waiting_period` - The waiting period in seconds after starting
  the process.
  
- `Returns` - The PID of the started process.


##### `terminate_process`

```python
def terminate_process(script_path: str,
                      termination_timeout: Optional[int] = None) -> list[int]
```

Terminate all processes that have the given script as their
entrypoint. Returns the list of terminated PIDs.

If `termination_timeout` is not None, the processes will be
terminated forcefully after the given timeout (in seconds).

**Arguments**:

- `script_path` - The absolute path of the python file entrypoint.
- `termination_timeout` - The timeout in seconds after which the
  processes will be terminated forcefully.
  

**Returns**:

  The list of terminated PIDs.


## `tum_esm_utils.shell`

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


## `tum_esm_utils.sqlitelock`


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


## `tum_esm_utils.text`

Functions used for text manipulation/processing.

Implements: `get_random_string`, `pad_string`, `is_date_string`,
`is_rfc3339_datetime_string`, `insert_replacements`, `simplify_string_characters`,
`replace_consecutive_characters`, `RandomLabelGenerator`


##### `get_random_string`

```python
def get_random_string(length: int, forbidden: list[str] = []) -> str
```

Return a random string from lowercase letters.

**Arguments**:

- `length` - The length of the random string.
- `forbidden` - A list of strings that should not be generated.
  

**Returns**:

  A random string.


##### `pad_string`

```python
def pad_string(text: str,
               min_width: int,
               pad_position: Literal["left", "right"] = "left",
               fill_char: Literal["0", " ", "-", "_"] = " ") -> str
```

Pad a string with a fill character to a minimum width.

**Arguments**:

- `text` - The text to pad.
- `min_width` - The minimum width of the text.
- `pad_position` - The position of the padding. Either "left" or "right".
- `fill_char` - The character to use for padding.
  

**Returns**:

  The padded string.


##### `is_date_string`

```python
def is_date_string(date_string: str) -> bool
```

Returns `True` if string is in a valid `YYYYMMDD` format.


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


##### `simplify_string_characters`

```python
def simplify_string_characters(s: str,
                               additional_replacements: dict[str,
                                                             str] = {}) -> str
```

Simplify a string by replacing special characters with their ASCII counterparts
and removing unwanted characters.

For example, `simplify_string_characters("Héllo, wörld!")` will return `"hello-woerld"`.

**Arguments**:

- `s` - The string to simplify.
- `additional_replacements` - A dictionary of additional replacements to apply.
  `{ "ö": "oe" }` will replace `ö` with `oe`.
  
- `Returns` - The simplified string.


##### `replace_consecutive_characters`

```python
def replace_consecutive_characters(s: str,
                                   characters: list[str] = [" ", "-"]) -> str
```

Replace consecutiv characters in a string (e.g. "hello---world" -> "hello-world"
or "hello   world" -> "hello world").

**Arguments**:

- `s` - The string to process.
- `characters` - A list of characters to replace duplicates of.
  

**Returns**:

  The string with duplicate characters replaced.


### `RandomLabelGenerator` Objects

```python
class RandomLabelGenerator()
```

A class to generate random labels that follow the Docker style naming of
containers, e.g `admiring-archimedes` or `happy-tesla`.

**Usage with tracking duplicates:**

```python
generator = RandomLabelGenerator()
label = generator.generate()
another_label = generator.generate()  # Will not be the same as `label`
generator.free(label)  # Free the label to be used again
```

**Usage without tracking duplicates:**

```python
label = RandomLabelGenerator.generate_fully_random()
```

Source for the names and adjectives: https://github.com/moby/moby/blob/master/pkg/namesgenerator/names-generator.go


##### `__init__`

```python
def __init__(occupied_labels: set[str] | list[str] = set(),
             adjectives: set[str] | list[str] = CONTAINER_ADJECTIVES,
             names: set[str] | list[str] = CONTAINER_NAMES) -> None
```

Initialize the label generator.


##### `generate`

```python
def generate() -> str
```

Generate a random label that is not already occupied.


##### `free`

```python
def free(label: str) -> None
```

Free a label to be used again.


##### `generate_fully_random`

```python
@staticmethod
def generate_fully_random(
        adjectives: set[str] | list[str] = CONTAINER_ADJECTIVES,
        names: set[str] | list[str] = CONTAINER_NAMES) -> str
```

Get a random label without tracking duplicates.

Use an instance of `RandomLabelGenerator` if you want to avoid
duplicates by tracking occupied labels.


## `tum_esm_utils.timing`

Functions used for timing or time calculations.

Implements: `date_range`, `ensure_section_duration`, `set_alarm`,
`clear_alarm`, `wait_for_condition`, `ExponentialBackoff`


##### `date_range`

```python
def date_range(from_date: datetime.date,
               to_date: datetime.date) -> list[datetime.date]
```

Returns a list of dates between from_date and to_date (inclusive).


##### `time_range`

```python
def time_range(from_time: datetime.time, to_time: datetime.time,
               time_step: datetime.timedelta) -> list[datetime.time]
```

Returns a list of times between from_time and to_time (inclusive).


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


##### `wait_for_condition`

```python
def wait_for_condition(is_successful: Callable[[], bool],
                       timeout_message: str,
                       timeout_seconds: float = 5,
                       check_interval_seconds: float = 0.25) -> None
```

Wait for the given condition to be true, or raise a TimeoutError
if the condition is not met within the given timeout. The condition
is passed as a function that will be called periodically.

**Arguments**:

- `is_successful` - A function that returns True if the condition is met.
- `timeout_message` - The message to include in the TimeoutError.
- `timeout_seconds` - The maximum time to wait for the condition to be met.
- `check_interval_seconds` - How long to wait inbetween `is_successful()` calls.


##### `parse_iso_8601_datetime`

```python
def parse_iso_8601_datetime(s: str) -> datetime.datetime
```

Parse a datetime string from various formats and return a datetime object.

ISO 8601 supports time zones as `<time>Z`, `<time>±hh:mm`, `<time>±hhmm` and
`<time>±hh`. However, only the second format is supported by `datetime.datetime.fromisoformat()`
(`HH[:MM[:SS[.fff[fff]]]][+HH:MM[:SS[.ffffff]]]`).

This function supports parsing alll ISO 8601 time formats.


##### `datetime_span_intersection`

```python
def datetime_span_intersection(
    dt_span_1: tuple[datetime.datetime,
                     datetime.datetime], dt_span_2: tuple[datetime.datetime,
                                                          datetime.datetime]
) -> Optional[tuple[datetime.datetime, datetime.datetime]]
```

Check if two datetime spans overlap.

**Arguments**:

- `dt_span_1` - The first datetime span (start, end).
- `dt_span_2` - The second datetime span (start, end).
  

**Returns**:

  The intersection of the two datetime spans or None if they do
  not overlap. Returns None if the intersection is a single point.


##### `date_span_intersection`

```python
def date_span_intersection(
    d_span_1: tuple[datetime.date,
                    datetime.date], d_span_2: tuple[datetime.date,
                                                    datetime.date]
) -> Optional[tuple[datetime.date, datetime.date]]
```

Check if two date spans overlap. This functions behaves
differently from `datetime_span_intersection` in that it
returns a single point as an intersection if the two date
spans overlap at a single date.

**Arguments**:

- `d_span_1` - The first date span (start, end).
- `d_span_2` - The second date span (start, end).
  

**Returns**:

  The intersection of the two date spans or None if they do
  not overlap.


### `ExponentialBackoff` Objects

```python
class ExponentialBackoff()
```

Exponential backoff e.g. when errors occur. First try again in 1 minute,
then 4 minutes, then 15 minutes, etc.. Usage:

```python
exponential_backoff = ExponentialBackoff(
    log_info=logger.info, buckets= [60, 240, 900, 3600, 14400]
)

while True:
    try:
        # do something that might fail
        exponential_backoff.reset()
    except Exception as e:
        logger.exception(e)
        exponential_backoff.sleep()
```


##### `__init__`

```python
def __init__(log_info: Optional[Callable[[str], None]] = None,
             buckets: list[int] = [60, 240, 900, 3600, 14400]) -> None
```

Create a new exponential backoff object.

**Arguments**:

- `log_info` - The function to call when logging information.
- `buckets` - The buckets to use for the exponential backoff.


##### `sleep`

```python
def sleep(max_sleep_time: Optional[float] = None) -> float
```

Wait and increase the wait time to the next bucket.

**Arguments**:

- `max_sleep_time` - The maximum time to sleep. If None, no maximum is set.
  

**Returns**:

  The amount of seconds waited.


##### `reset`

```python
def reset() -> None
```

Reset the waiting period to the first bucket


##### `timed_section`

```python
@contextlib.contextmanager
def timed_section(label: str) -> Generator[None, None, None]
```

Time a section of code and print the duration.
Usage example:

```python
with timed_section("my_section"):
    do_something()
```


## `tum_esm_utils.validators`

Implements validator utils for use with pydantic models.

Implements: `StrictFilePath`, `StrictDirectoryPath`


### `StrictFilePath` Objects

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


### `StrictDirectoryPath` Objects

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


### `Version` Objects

```python
class Version(pydantic.RootModel[str])
```

A version string in the format of MAJOR.MINOR.PATCH[-(alpha|beta|rc).N]


##### `as_tag`

```python
def as_tag() -> str
```

Return the version string as a tag, i.e. vMAJOR.MINOR.PATCH...


##### `as_identifier`

```python
def as_identifier() -> str
```

Return the version string as a number, i.e. MAJOR.MINOR.PATCH...


### `StricterBaseModel` Objects

```python
class StricterBaseModel(pydantic.BaseModel)
```

The same as pydantic.BaseModel, but with stricter rules. It does not
allow extra fields and validates assignments after initialization.


### `StrictIPv4Adress` Objects

```python
class StrictIPv4Adress(pydantic.RootModel[str])
```

A pydantic model that validates an IPv4 address.

Example usage:

```python
class MyModel(pyndatic.BaseModel):
    ip: StrictIPv4Adress

m = MyModel(ip='192.186.2.1')
m = MyModel(ip='192.186.2.1:22')
```

