<!-- markdownlint-disable -->

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/datastructures.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `datastructures`
Datastructures not in the standard library. 

Implements: `RingList` 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/datastructures.py#L66"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `merge_dicts`

```python
merge_dicts(old_object: Any, new_object: Any) → Any
```

For a given dict, update it recursively from a new dict. It will not add any properties and assert that the types remain the same (or null). null->int or int->null is possible but not int->dict or list->int. 



**example:**
 ```python
merge_dicts(
     old_object={"a": 3, "b": {"c": 50, "e": None}},
     new_object={"b": {"e": 80}},
) == {"a": 3, "b": {"c": 50, "e": 80}}
``` 


---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/datastructures.py#L8"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `RingList`




<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/datastructures.py#L9"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `__init__`

```python
__init__(max_size: int)
```








---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/datastructures.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `append`

```python
append(x: float) → None
```

appends an element to the list 

---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/datastructures.py#L15"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `clear`

```python
clear() → None
```

removes all elements 

---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/datastructures.py#L29"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `get`

```python
get() → list[float]
```

returns the list of elements 

---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/datastructures.py#L50"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `get_max_size`

```python
get_max_size() → int
```





---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/datastructures.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `is_full`

```python
is_full() → bool
```

returns true if list is full 

---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/datastructures.py#L53"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `set_max_size`

```python
set_max_size(new_max_size: int) → None
```

sets a new max size 

---

<a href="https://github.com/tum-esm/utils/tree/main/tum_esm_utils/datastructures.py#L46"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `sum`

```python
sum() → float
```

returns the max size of the list 


