# `tum_esm_utils.opus.file_interface` API Reference


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

