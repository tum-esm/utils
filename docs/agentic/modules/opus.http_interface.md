# `tum_esm_utils.opus.http_interface` API Reference


Provides a HTTP interface to OPUS.


### `OpusHTTPInterface` Objects

```python
class OpusHTTPInterface()
```

Interface to the OPUS HTTP interface.

It uses the socket library, because the HTTP interface of OPUS does not
return valid HTTP/1 or HTTP/2 headers. It opens and closes a new socket
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

Commands will be sent to `GET http://localhost/OpusCommand.htm?<request>`.
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

