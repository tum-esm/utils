<!-- markdownlint-disable -->

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/testing.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `testing`





---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/testing.py#L5"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `expect_file_contents`

```python
expect_file_contents(
    filepath: str,
    required_content_blocks: list[str] = [],
    forbidden_content_blocks: list[str] = []
) → None
```






---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/testing.py#L20"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `wait_for_condition`

```python
wait_for_condition(
    is_successful: Callable[[], bool],
    timeout_message: str,
    timeout_seconds: float = 5
) → None
```






