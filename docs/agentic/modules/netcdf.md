# `tum_esm_utils.netcdf` API Reference


A thin wrapper over the netCDF4 library to make working with NetCDF files easier.

Implements: `NetCDFFile`, `remove_elements_from_netcdf_file`, `compress_netcdf_file`.

This requires you to install this utils library with the optional `netcdf` dependencies:

```bash
pip install "tum_esm_utils[netcdf]"
## `or`
uv add "tum_esm_utils[netcdf]"
```


### `NetCDFFile` Objects

```python
class NetCDFFile()
```


##### `__init__`

```python
def __init__(
    filepath: str,
    parallel: bool = False,
    diskless: bool = False,
    mode: Literal["r", "w", "r+", "a", "x", "rs", "ws", "r+s", "as"] = "r"
) -> None
```

A simple wrapper around netCDF4.Dataset to make the interaction with NetCDF files easier.

If writing to a new file, it will first write to the filepath+ ".tmp" and  rename it to the final
filepath when closing the file. This ensures that the final filepath will only exist if the file
was written completely. In append mode, the filepath is not changes.


##### `create_dimension`

```python
def create_dimension(name: str, size: int) -> None
```

Create a new dimension in the NetCDF file.

**Raises**:

- `ValueError` - If the dimension already exists
- `RuntimeError` - If the NetCDF file is not opened in write mode.


##### `create_variable`

```python
def create_variable(name: str,
                    dimensions: tuple[nc.Dimension | str, ...],
                    units: str,
                    long_name: Optional[str] = None,
                    description: Optional[str] = None,
                    fill_value: Optional[float | int] = None,
                    chunk_dimensions: list[str] = [],
                    datatype: Literal["f4", "f8", "i4", "i8"] = "f4",
                    zlib: bool = True,
                    compression: Optional[Literal[
                        "zlib",
                        "szip",
                        "zstd",
                        "bzip2",
                        "blosc_lz",
                        "blosc_lz4",
                        "blosc_lz4hc",
                        "blosc_zlib",
                        "blosc_zstd",
                    ]] = None,
                    compression_level: Optional[int] = 2) -> None
```

Create a new variable in the NetCDF file.

We added the `zlib` argument a while ago, but should support different
compression types without a breaking release. The `compression` argument
is set to `None` by default, but will override the `zlib` argument if it
is set. To disable compression, set `zlib` to `False` and leave
`compression` at `None`.

**Raises**:

- `ValueError` - If the variable already exists or if a dimension is not found.
- `RuntimeError` - If the NetCDF file is not opened in write mode.


##### `import_dimension`

```python
def import_dimension(dimension: nc.Dimension,
                     new_name: Optional[str] = None) -> None
```

Import a dimension from another NetCDF file.

**Raises**:

- `ValueError` - If the dimension already exists.
- `RuntimeError` - If the NetCDF file is not opened in write mode.


##### `import_variable`

```python
def import_variable(variable: "nc.Variable[Any]",
                    new_name: Optional[str] = None,
                    zlib: bool = True,
                    compression_level: int = 2) -> None
```

Import a variable from another NetCDF file.

**Raises**:

- `ValueError` - If the variable already exists.
- `RuntimeError` - If the NetCDF file is not opened in write mode.


##### `add_attribute`

```python
def add_attribute(key: str, value: str, allow_overwrite: bool = False) -> None
```

Add a global attribute to the NetCDF file.

**Raises**:

- `ValueError` - If the attribute already exists and `allow_overwrite` is False.
- `RuntimeError` - If the NetCDF file is not opened in write mode.


##### `close`

```python
def close() -> None
```

Close the NetCDF file, possibly renaming the temporary file to the final filepath.


##### `discard`

```python
def discard() -> None
```

Discard the NetCDF file, closing it and removing the temporary file if it exists.


##### `__getitem__`

```python
def __getitem__(key: str) -> "nc.Variable[Any]"
```

Get a variable from the NetCDF file.


##### `remove_elements_from_netcdf_file`

```python
def remove_elements_from_netcdf_file(source_filepath: str,
                                     destination_filepath: str,
                                     variables_to_remove: list[str] = [],
                                     dimensions_to_remove: list[str] = [],
                                     attributes_to_remove: list[str] = [],
                                     compression_level: int = 2) -> None
```

Create a new NetCDF file by copying an existing one, but removing specified variables, dimensions, and attributes. This is useful because NetCDF4 does not support removing elements from an existing file.

**Raises**:

- `FileNotFoundError` - If the source file does not exist.
- `FileExistsError` - If the destination file already exists.


##### `compress_netcdf_file`

```python
def compress_netcdf_file(source_filepath: str,
                         destination_filepath: str,
                         compression_level: int = 2) -> None
```

Compress an existing NetCDF file by creating a new one with the specified compression level. This is useful because some NetCDF4 files given to you might not be (very well) compressed.

**Raises**:

- `FileNotFoundError` - If the source file does not exist.
- `FileExistsError` - If the destination file already exists.

