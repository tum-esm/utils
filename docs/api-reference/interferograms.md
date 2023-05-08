<!-- markdownlint-disable -->

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/interferograms.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `interferograms`
Functions for interacting with interferograms. 

Implements: `detect_corrupt_ifgs` 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/interferograms.py#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `detect_corrupt_ifgs`

```python
detect_corrupt_ifgs(
    ifg_directory: str,
    silent: bool = True,
    fortran_compiler: Literal['gfortran', 'gfortran-9'] = 'gfortran'
) → dict[str, list[str]]
```

Returns dict[filename, list[error_messages]] for all corrupt interferograms in the given directory. 

It will compile the fortran code using a given compiler to perform this task. The fortran code is derived from the preprocess source code of Proffast 2 (https://www.imk-asf.kit.edu/english/3225.php). We use it because the retrieval using Proffast 2 will fail if there are corrupt interferograms in the input. 


