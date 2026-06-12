# `tum_esm_utils.processes` API Reference


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

