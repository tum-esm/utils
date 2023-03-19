# Example Usage

## Custom Logger

The `logging` module from the standard Python library is kind of annoying to configure when other subprojects or libraries are using it as well. Additionally, we wanted to have an automatic archiving functionality.

Hence, this class is a simple reimplementation of the logging module's core features.

```python
from tum_esm_utils.logger import Logger

my_logger = Logger(
    origin = "my_logger",
    logfile_directory = "/tmp/logs"
)

my_logger.debug("hello")
my_logger.info("hello")
my_logger.warning("hello")
my_logger.error("hello")

try:
    30 / 0
except Exception:
    logger.exception(label="customlabel")
```

<hr>

## Start Background Processes

```python
from tum_esm_utils.processes import (
    start_background_process,
    get_process_pids,
    terminate_process
)

# start a process using nohup and get its process-id
new_pid = start_background_process(
    sys.executable, SCRIPT_PATH
)

# pid should be returned from this list
assert get_process_pids(SCRIPT_PATH) == [new_pid]

# terminate the process
terminated_pids = terminate_process(SCRIPT_PATH)
assert terminated_pids == [new_pid]

# pid list should be empty
assert get_process_pids(SCRIPT_PATH) == []
```

<hr>

## Insert Text Replacements

```python
from tum_esm_utils.text import insert_replacements

template = """
Dear %YOU%,

thanks for reading this %TEXT_TYPE%!

Best,
%ME%
"""

replacements = {
    "ME": "person A",
    "YOU": "person B",
    "TEXT_TYPE": "letter",
}

# replace all items in here
filled_template = insert_replacements(template, replacements)
```
