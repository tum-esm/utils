# `tum_esm_utils.files` API Reference


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


##### `load_toml_file`

```python
def load_toml_file(path: str) -> Any
```

Load the content of a TOML file.


##### `dump_toml_file`

```python
def dump_toml_file(path: str, content: Any) -> None
```

Dump content to a TOML file.


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

