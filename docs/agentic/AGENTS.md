# TUM ESM Utils Agent Guide

## Purpose

This library is a collection of small Python utilities used in research projects by the Professorship of Environmental Sensing and Modeling at the Technical University of Munich. It centralizes reusable helpers so downstream projects can depend on tested, documented primitives instead of carrying local utility copies.

## Documentation Structure

- `example-usage.md` contains the same examples as the human-facing documentation page.
- `modules/` contains one API reference file per documented submodule. File names match Python import paths below `tum_esm_utils`, for example `modules/column.astronomy.md` documents `tum_esm_utils.column.astronomy`.
- This `AGENTS.md` file lists the documented modules and their module docstrings so agents can choose the narrowest API file before reading detailed references.

## Modules

## `tum_esm_utils.code`

API reference: [modules/code.md](modules/code.md)

Functions for interacting with GitHub and GitLab.

Implements: `request_github_file`, `request_gitlab_file`

## `tum_esm_utils.column`

API reference: [modules/column.md](modules/column.md)

Functions related to column observation data.

## `tum_esm_utils.column.astronomy`

API reference: [modules/column.astronomy.md](modules/column.astronomy.md)

Functions to perform astronomical calculations

## `tum_esm_utils.column.averaging_kernel`

API reference: [modules/column.averaging_kernel.md](modules/column.averaging_kernel.md)

Functions to store, load and apply a column averaging kernel.

## `tum_esm_utils.column.ncep_profiles`

API reference: [modules/column.ncep_profiles.md](modules/column.ncep_profiles.md)

Functions to read NCEP profiles.

## `tum_esm_utils.dataframes`

API reference: [modules/dataframes.md](modules/dataframes.md)

Dataframe-related utility functions.

Implements: `fill_df_time_gaps_with_nans`

This requires you to install this utils library with the optional `polars` dependency:

```bash
pip install "tum_esm_utils[polars]"
# or
uv add "tum_esm_utils[polars]"
```

## `tum_esm_utils.datastructures`

API reference: [modules/datastructures.md](modules/datastructures.md)

Datastructures not in the standard library.

Implements: `LazyDict`, `RingList`, `merge_dicts`

## `tum_esm_utils.decorators`

API reference: [modules/decorators.md](modules/decorators.md)

Decorators that can be used wrap functions.

Implements: `with_filelock`

## `tum_esm_utils.em27`

API reference: [modules/em27.md](modules/em27.md)

Functions for interacting with EM27 interferograms.

Implements: `detect_corrupt_opus_files`, `load_proffast2_result`.

This requires you to install this utils library with the optional `em27` dependency:

```bash
pip install "tum_esm_utils[em27]"
# or
uv add "tum_esm_utils[em27]"
```

## `tum_esm_utils.files`

API reference: [modules/files.md](modules/files.md)

File-related utility functions.

Implements: `load_file`, `dump_file`, `load_json_file`,
`dump_json_file`, `get_parent_dir_path`, `get_dir_checksum`,
`get_file_checksum`, `rel_to_abs_path`, `read_last_n_lines`,
`expect_file_contents`, `render_directory_tree`, `list_directory`

## `tum_esm_utils.mathematics`

API reference: [modules/mathematics.md](modules/mathematics.md)

Mathematical functions.

Implements: `distance_between_angles`

## `tum_esm_utils.netcdf`

API reference: [modules/netcdf.md](modules/netcdf.md)

A thin wrapper over the netCDF4 library to make working with NetCDF files easier.

Implements: `NetCDFFile`, `remove_elements_from_netcdf_file`, `compress_netcdf_file`.

This requires you to install this utils library with the optional `netcdf` dependencies:

```bash
pip install "tum_esm_utils[netcdf]"
# or
uv add "tum_esm_utils[netcdf]"
```

## `tum_esm_utils.opus`

API reference: [modules/opus.md](modules/opus.md)

Functions for interacting with OPUS files.

Implements: `OpusFile`, `OpusHTTPInterface`.

Read https://tccon-wiki.caltech.edu/Main/I2SAndOPUSHeaders for more information
about the file parameters. This requires you to install this utils library with
the optional `opus` dependency:

```bash
pip install "tum_esm_utils[opus]"
# or
uv add "tum_esm_utils[opus]"
```

Credits to Friedrich Klappenbach (friedrich.klappenbach@tum.de) for decoding the OPUS file
format.

## `tum_esm_utils.opus.file_interface`

API reference: [modules/opus.file_interface.md](modules/opus.file_interface.md)

Functions for interacting with OPUS files.

## `tum_esm_utils.opus.http_interface`

API reference: [modules/opus.http_interface.md](modules/opus.http_interface.md)

Provides a HTTP interface to OPUS.

## `tum_esm_utils.plotting`

API reference: [modules/plotting.md](modules/plotting.md)

Better defaults for matplotlib plots and utilities for creating and saving figures.

Implements: `apply_better_defaults`, `create_figure`, `add_subplot`

This requires you to install this utils library with the optional `plotting` dependencies:

```bash
pip install "tum_esm_utils[plotting]"
# or
uv add "tum_esm_utils[plotting]"
```

## `tum_esm_utils.processes`

API reference: [modules/processes.md](modules/processes.md)

Functions to start and terminate background processes.

Implements: `get_process_pids`, `start_background_process`,
`terminate_process`

## `tum_esm_utils.rebinning`

API reference: [modules/rebinning.md](modules/rebinning.md)

Functions to rebin binned data points

Implements: `rebin_1d`, `rebin_2d`.

This requires you to install this utils library with the optional `modeling` dependency:

```bash
pip install "tum_esm_utils[modeling]"
# or
uv add "tum_esm_utils[modeling]"
```

## `tum_esm_utils.shell`

API reference: [modules/shell.md](modules/shell.md)

Implements custom logging functionality, because the
standard logging module is hard to configure for special
cases.

Implements: `run_shell_command`, `CommandLineException`,
`get_hostname`, `get_commit_sha`, `change_file_permissions`

## `tum_esm_utils.sqlitelock`

API reference: [modules/sqlitelock.md](modules/sqlitelock.md)

No module docstring available.

## `tum_esm_utils.system`

API reference: [modules/system.md](modules/system.md)

Common system status related functions.

Implements: `get_cpu_usage`, `get_memory_usage`, `get_disk_space`,
`get_system_battery`, `get_last_boot_time`, `get_utc_offset`

## `tum_esm_utils.text`

API reference: [modules/text.md](modules/text.md)

Functions used for text manipulation/processing.

Implements: `get_random_string`, `pad_string`, `is_date_string`,
`is_rfc3339_datetime_string`, `insert_replacements`, `simplify_string_characters`,
`replace_consecutive_characters`, `RandomLabelGenerator`

## `tum_esm_utils.timing`

API reference: [modules/timing.md](modules/timing.md)

Functions used for timing or time calculations.

Implements: `date_range`, `ensure_section_duration`, `set_alarm`,
`clear_alarm`, `wait_for_condition`, `ExponentialBackoff`

## `tum_esm_utils.validators`

API reference: [modules/validators.md](modules/validators.md)

Implements validator utils for use with pydantic models.

Implements: `StrictFilePath`, `StrictDirectoryPath`
