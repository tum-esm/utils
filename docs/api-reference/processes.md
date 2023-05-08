<!-- markdownlint-disable -->

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/processes.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `processes`
Functions to start and terminate background processes. 

Implements: `get_process_pids`, `start_background_process`, `terminate_process` 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/processes.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `get_process_pids`

```python
get_process_pids(script_path: str) → list[int]
```

Return a list of PIDs that have the given script as their entrypoint 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/processes.py#L29"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `start_background_process`

```python
start_background_process(interpreter_path: str, script_path: str) → int
```

Start a new background process with nohup with a given python interpreter and script path. The script paths parent directory will be used as the working directory for the process. 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/processes.py#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `terminate_process`

```python
terminate_process(script_path: str) → list[int]
```

Terminate all processes that have the given script as their entrypoint. Returns the list of terminated PIDs. 


