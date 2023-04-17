<!-- markdownlint-disable -->

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/text.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `text`





---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/text.py#L8"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_random_string`

```python
get_random_string(length: int, forbidden: list[str] = []) → str
```

Return a random string from lowercase letter, the strings from the list passed as `forbidden` will not be generated 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/text.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `pad_string`

```python
pad_string(
    text: str,
    min_width: int,
    pad_position: Literal['left', 'right'] = 'left',
    fill_char: Literal['0', ' ', '-', '_'] = ' '
) → str
```






---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/text.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `is_date_string`

```python
is_date_string(date_string: str) → bool
```

Returns `True` if string is in a valid `YYYYMMDD` format 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/text.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `date_range`

```python
date_range(from_date_string: str, to_date_string: str) → list[str]
```

Returns a list of dates between `from_date_string` and `to_date_string`. 



**Example:**
 

```python
date_range("20210101", "20210103") == ["20210101", "20210102", "20210103"]
``` 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/text.py#L64"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `is_datetime_string`

```python
is_datetime_string(datetime_string: str) → bool
```

Returns `True` if string is in a valid `YYYYMMDD HH:mm:ss` format 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/text.py#L73"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `is_rfc3339_datetime_string`

```python
is_rfc3339_datetime_string(rfc3339_datetime_string: str) → bool
```

Returns `True` if string is in a valid `YYYY-MM-DDTHH:mm:ssZ` (RFC3339) format. Caution: The appendix of `+00:00` is required for UTC! 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/text.py#L83"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `date_is_too_recent`

```python
date_is_too_recent(date_string: str, min_days_delay: int = 1) → bool
```

A min delay of two days means 20220101 will be too recent any time before 20220103 00:00 (start of day) 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/text.py#L95"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `insert_replacements`

```python
insert_replacements(content: str, replacements: dict[str, str]) → str
```

For every key in replacements, replaces `%key$` in the content with its value. 


