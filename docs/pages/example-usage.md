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

detection_results = tum_esm_utils.em27.detect_corrupt_opus_files(
    "/path/to/a/folder/with/interferograms"
)
assert detection_results == {
    'md20220409s0e00a.0199': [
        'Charfilter "DUR" is missing',
        'Charfilter "GBW" is missing',
        'Charfilter "GFW" is missing',
        'Charfilter "HFL" is missing',
        'Charfilter "LWN" is missing',
        'Charfilter "TSC" is missing',
        'Differing sizes of dual channel IFGs!',
        'IFG size too small!',
        'Inconsistent dualifg!',
        'Inconsistent parameter kind in OPUS file!'
    ],
    'comb_invparms_ma_SN061_210329-210329.csv': [
        'File not even readible by the parser'
    ],
    'comb_invparms_mc_SN115_220602-220602.csv': [
        'File not even readible by the parser'
    ],
    'md20220409s0e00a.0200': [
        'File not even readible by the parser'
    ]
}
```

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

## Plotting

A very simple wrapper around `matplotlib` to creater prettier plots with less code.

```python
import tum_esm_utils

# apply some nice styles to axis/labels/etc.
tum_esm_utils.plotting.apply_better_defaults(font_family="Roboto")

with tum_esm_utils.plotting.create_figure(
    "some-path-to-figure.png",
    width=10,
    height=6,
) as fig:
    axis1 = tum_esm_utils.plotting.add_subplot(
        fig, (2, 1, 1), title="Test Plot", xlabel="X", ylabel="Y"
    )
    axis1.plot([1, 2, 3], [1, 2, 3])

    axis2 = tum_esm_utils.plotting.add_subplot(
        fig, (2, 1, 2), title="Test Plot 2", xlabel="X", ylabel="Y"
    )
    axis2.plot([1, 2, 3], [3, 2, 1])
```

You have to have the optional `plotting` dependencies installed for this to work:

```bash
pip install "tum-esm-utils[plotting]"
# or
pdm add "tum-esm-utils[plotting]"
```

## Exponential Backoff

When an error occurs in your code, it might be wise to wait a bit before trying again. Using the `ExponentialBackoff` class, you can
make your code wait for a certain amount of time before trying again – with an exponential increase in waiting time on every retry. I.e.,
first, wait 1 minute, then 4 minutes, then 15 minutes, etc..

```python
import tum_esm_utils

logger = ...

# both arguments are optional
exponential_backoff = tum_esm_utils.timing.ExponentialBackoff(
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

## OPUS HTTP Interface

When you start OPUS with `/HTTPSERVER=on opus.exe`, you can control OPUS via HTTP. We recommend using the HTTP interface over the DDE interface, because the DDE standard is at its end-of-life for decades now.

```python
import time
from tum_esm_utils.opus import OpusHTTPInterface

version = OpusHTTPInterface.get_version()
language = OpusHTTPInterface.get_language()
username = OpusHTTPInterface.get_username()

OpusHTTPInterface.load_experiment("somepath.xmp")
macro_id = OpusHTTPInterface.start_macro("somepath.mtx")
time.sleep(5)

assert OpusHTTPInterface.macro_is_running(macro_id)
time.sleep(5)

OpusHTTPInterface.stop_macro(macro_id)
time.sleep(5)

assert not OpusHTTPInterface.macro_is_running(macro_id)
```

Have a look at the API reference, what commands, we implemented. Use the `OpusHTTPInterface.request` or `OpusHTTPInterface.request_without_retry` to send any command using the HTTP interface.
