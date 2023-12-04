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

## Test Which Interferograms Cannot Be Processed by Proffast 2

The following code will run a modified code of the [Proffast 2](https://www.imk-asf.kit.edu/english/3225.php) preprocessor that now only does the parsing of interferograms to check whether it can read them. This is useful because Proffast itself will fail for the whole day of measurements if there is a single interferogram it cannot read.

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

The detection result means the file `/path/to/a/folder/with/interferograms/md20220409s0e00a.0199` could not be read.

## Ring List

We have yet to find a simple Python implementation of a ring list - also called [circular buffer](https://en.wikipedia.org/wiki/Circular_buffer). Hence, we implemented a well-tested one ourselves.

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
# you append new elements to a full list. Of course, it does
# not copy all elements but only modifies the internal pointers.

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

We found the `logging` module from the standard Python library hard to configure when other subprojects or libraries also use it. Additionally, we wanted to have an automatic archiving functionality.

Hence, this class is a simple reimplementation of the logging module's core features.

```python
from tum_esm_utils.logger import Logger

my_logger = Logger(
    origin = "my_logger",
    logfile_directory = "/tmp/logs"
)
```

The log lines of the last hour can be found in `/tmp/logs/current-logs.log`. All older log lines can be found in `/tmp/logs/archive/YYYYMMDD.log` (`/tmp ...` is used in the example code above).

Regular log lines (debug, info, warning, error):

```python
my_logger.debug("hello")
my_logger.info("hello")
my_logger.warning("hello")
my_logger.error("hello")
```

```log
time UTC±X - origin - level - message
```

You can give the more details to each log type:

```python
my_logger.debug("hello", details="some elaborate details on what happened")
```

```log
time UTC±X - origin - DEBUG - hello
--- details: ---------------------------
some elaborate details on what happened
----------------------------------------
```

Exception logging:

```python
try:
    30 / 0
except Exception:
    my_logger.exception(
        label="custom label",
        details="some elaborate details on what happened"
    )
```

```log
time UTC±X - origin - EXCEPTION - custom label, ZeroDivisionError: division by zero
--- details: ---------------------------
some elaborate details on what happened
--- traceback: -------------------------
...
----------------------------------------
```

## Strict Path Validation with Pydantic

Pydantic has a lot of field validators (number must be greater equal, etc.),
but on string fields it does not have a validator "should be existing file/dir
path". One would have to add a `@field_validator("path field 1", ...)` validator
function to each model that uses file paths to be validated on model loading.

```python
from tum_esm_utils.validators import StrictFilePath, StrictDirectoryPath

class Config(pydantic.BaseModel):
    f: StrictFilePath
    d: StrictDirectoryPath

# it can be parsed just like a string
c = Config.model_validate({"f": "pyproject.toml", "d": "packages"})
alternative_c = Config(f="netlify.toml", d="packages")

# the value now has to be accessed by `<field>.root`
print(type(c.f))       # <class '__main__.StrictFilePath'>
print(type(c.f.root))  # <class 'str'>

# but the exported dicts do not show any sign that the
# respective fields are anything more than a regular string
print(c.model_dump_json())  # {"f": "netlify.toml", "d": "src"}

# you can turn off the file path validation at validation time if you want
c = Config.model_validate(
    {"f": "netlify.tom", "d": "package"},
    context={"ignore-path-existence": True},
)
```

## Get Absolute Paths

The following code snippet only work, when calling the script from the
same directory:

```python
with open("./somedir/some_file.txt", "r") as f:
    print(f.read())
```

But when you call this script from another directory, it will fail because
the path is relative to the current working directory.

Converting the relative path to an absolute path will fix this. The directory
which this path is relative to is always the directory of the script that calls
this function.

```python
from tum_esm_utils.files import rel_to_abs_path

with open(rel_to_abs_path("./somedir/some_file.txt"), "r") as f:
    print(f.read())

# or

with open(rel_to_abs_path("somedir/some_file.txt"), "r") as f:
    print(f.read())

# or

with open(rel_to_abs_path("somedir", "some_file.txt"), "r") as f:
    print(f.read())
```

## Set alarms to catch infinite loops

The following code will raise a `TimeoutError` if the function `my_function`
takes longer than 10 seconds to execute:

```python
from tum_esm_utils.context import set_alarm, clear_alarm

set_alarm(10, "some section name")
my_function()
clear_alarm()

# if my_function takes longer than 10 seconds, raises:
# TimeoutError("some section name took too long (timed out after 10 seconds)")
```
