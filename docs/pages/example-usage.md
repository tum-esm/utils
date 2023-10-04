# Example Usage

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

## Test Which Interferograms Cannot Be Processed by Proffast `2.\*`

The following code will run a modified code of the Proffast 2.\* preprocessor that now only does the parsing of interferograms to check whether it can read them. This is useful because Proffast itself will fail for the whole day of measurements if there is a single interferogram it cannot read.

```python
import tum_esm_utils

test_data_path = os.path.join("/path/to/a/folder/with/interferograms")
detection_results = tum_esm_utils.interferograms.detect_corrupt_ifgs(
    test_data_path
)
assert detection_results == {
    "md20220409s0e00a.0199": [
        "charfilter 'GFW' is missing",
        "charfilter 'GBW' is missing",
        "charfilter 'HFL' is missing",
        "charfilter 'LWN' is missing",
        "charfilter 'TSC' is missing",
    ]
}
```

The detection result means that the file `/path/to/a/folder/with/interferograms/md20220409s0e00a.0199` could not be read.

## Ring List

We did not find a simple python implementation of a ring list - also called ring buffer - yet. Hence, we implemented one ourselves which is well tested.

```python
import tum_esm_utils

ring_list = tum_esm_utils.datastructures.RingList(4)

# list is empty at first
print(ring_list.get())           # []
print(ring_list.get_max_size())  # 4
print(ring_list.is_full())       # False

# appending one element
ring_list.append(23.5)
assert ring_list.get() == [23.5]

ring_list.append(3)
ring_list.append(4)
ring_list.append(18)
print(ring_list.get())      # [23.5, 3, 4, 18]
print(ring_list.is_full())  # True

# the ring list will always discard the oldest element once
# you append new elements to a full list. Of course it does
# not copy all elements but only modifies the internal pointers

ring_list.append(4)
print(ring_list.get())      # [3, 4, 18, 4]

ring_list.append(5)
print(ring_list.get())      # [4, 18, 4, 5]
print(ring_list.sum())      # 31
```

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
