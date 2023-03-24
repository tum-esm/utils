<!-- markdownlint-disable -->

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/interferograms.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `interferograms`





---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/interferograms.py#L43"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `detect_corrupt_ifgs`

```python
detect_corrupt_ifgs(
    ifg_directory: str,
    silent: bool = True,
    fortran_compiler: Literal['gfortran', 'gfortran-9'] = 'gfortran'
) → dict[str, list[str]]
```

Returns dict[filename, list[error_messages]] for all corrupt interferograms in the given directory. 


