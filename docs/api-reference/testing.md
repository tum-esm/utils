<!-- markdownlint-disable -->

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/testing.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `testing`
Functions commonly used in testing scripts. 

Implements: `expect_file_contents`, `wait_for_condition` 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/testing.py#L9"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `expect_file_contents`

```python
expect_file_contents(
    filepath: str,
    required_content_blocks: list[str] = [],
    forbidden_content_blocks: list[str] = []
) → None
```

Assert that the given file contains all of the required content blocks, and/or none of the forbidden content blocks. 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/testing.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `wait_for_condition`

```python
wait_for_condition(
    is_successful: Callable[[], bool],
    timeout_message: str,
    timeout_seconds: float = 5
) → None
```

Wait for the given condition to be true, or raise a TimeoutError if the condition is not met within the given timeout. 

The condition is checked every 0.25 seconds. 


