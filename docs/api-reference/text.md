<!-- markdownlint-disable -->

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/text.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `text`





---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/text.py#L7"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_random_string`

```python
get_random_string(length: int, forbidden: list[str] = []) → str
```

Return a random string from lowercase letter, the strings from the list passed as `forbidden` will not be generated 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/text.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/text.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `is_date_string`

```python
is_date_string(date_string: str) → bool
```

Returns true if string is in `YYYYMMDD` format and date exists 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/text.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `insert_replacements`

```python
insert_replacements(content: str, replacements: dict[str, str]) → str
```

For every key in replacements, replaces `%key$` in the content with its value. 

