<!-- markdownlint-disable -->

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/logger.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `logger`
Implements custom logging functionality, because the standard logging module is hard to configure for special cases. 

Implements: `Logger` 



---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/logger.py#L52"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Logger`




<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/logger.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    origin: str,
    logfile_directory: str,
    write_to_files: bool = True,
    print_to_console: bool = False
) → None
```








---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/logger.py#L77"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `debug`

```python
debug(message: str, details: Optional[str] = None) → None
```

writes a debug log line 

---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/logger.py#L101"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `error`

```python
error(message: str, details: Optional[str] = None) → None
```

writes an error log line, sends the message via MQTT when config is passed (required for revision number) 

---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/logger.py#L111"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `exception`

```python
exception(label: Optional[str] = None, details: Optional[str] = None) → None
```

logs the traceback of an exception; output will be formatted like this: 

```
(label, )ZeroDivisionError: division by zer

--- details: -----------------
...

--- traceback: ---------------
...

------------------------------
``` 

---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/logger.py#L73"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `horizontal_line`

```python
horizontal_line(fill_char: Literal['-', '=', '.', '_'] = '=') → None
```

writes a horizonal line wiht `-`/`=`/... characters 

---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/logger.py#L85"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `info`

```python
info(message: str, details: Optional[str] = None) → None
```

writes an info log line 

---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/logger.py#L93"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `warning`

```python
warning(message: str, details: Optional[str] = None) → None
```

writes a warning log line 


