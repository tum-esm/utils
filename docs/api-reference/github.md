<!-- markdownlint-disable -->

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/github.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `github`
Functions for interacting with GitHub. 

Implements: `request_github_file` 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/github.py#L9"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `request_github_file`

```python
request_github_file(
    github_repository: str,
    filepath: str,
    access_token: Optional[str] = None
) → str
```

Sends a request and returns the content of the response, as a string. Raises an HTTPError if the response status code is not 200. 


