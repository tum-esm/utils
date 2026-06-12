# `tum_esm_utils.datastructures` API Reference


Datastructures not in the standard library.

Implements: `LazyDict`, `RingList`, `merge_dicts`


### `LazyDict` Objects

```python
class LazyDict(Generic[KeyType, ValueType])
```

A dictionary that loads/computes its values lazily.

The goal is that it only runs this computation or loading operation once and only when it's needed.

Usage:

```python
ld = LazyDict[str,int](lambda key: len(key))
x = ld["hello"]  # computes len("hello") and stores it
y = ld["hello"]  # uses the stored value for "world"
```


##### `__getitem__`

```python
def __getitem__(key: KeyType) -> ValueType
```

Get the value for a given key. Computes and stores it if not already present.


##### `__setitem__`

```python
def __setitem__(key: KeyType, value: ValueType) -> None
```

Set the value for a given key. Overrides any existing value.


##### `__len__`

```python
def __len__() -> int
```

Return the number of stored items.


##### `keys`

```python
def keys() -> list[KeyType]
```

Return all stored keys.


##### `values`

```python
def values() -> list[ValueType]
```

Return all stored values.


### `RingList` Objects

```python
class RingList()
```


##### `__init__`

```python
def __init__(max_size: int)
```

Initialize a RingList with a maximum size.


##### `clear`

```python
def clear() -> None
```

Removes all elements from the list.


##### `is_full`

```python
def is_full() -> bool
```

Returns True if the list is full.


##### `append`

```python
def append(x: float) -> None
```

Appends an element to the list.


##### `get`

```python
def get() -> list[float]
```

Returns the list of elements.


##### `sum`

```python
def sum() -> float
```

Returns the max size of the list


##### `set_max_size`

```python
def set_max_size(new_max_size: int) -> None
```

Sets a new max size to the list.


##### `merge_dicts`

```python
def merge_dicts(old_object: Any, new_object: Any) -> Any
```

For a given dict, update it recursively from a new dict.
It will not add any properties and assert that the types
remain the same (or null). null->int or int->null is possible
but not int->dict or list->int.

example:
```python
merge_dicts(
    old_object={"a": 3, "b": {"c": 50, "e": None}},
    new_object={"b": {"e": 80}},
) == {"a": 3, "b": {"c": 50, "e": 80}}
```


##### `concat_lists`

```python
def concat_lists(*lists: list[T]) -> list[T]
```

Concatenates multiple lists into one list.


##### `chunk_list`

```python
def chunk_list(xs: list[T], n: int) -> list[list[T]]
```

Split a list into chunks of size n.

