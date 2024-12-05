"""Datastructures not in the standard library.

Implements: `RingList`, `merge_dicts`"""

from __future__ import annotations
from typing import Any


class RingList:
    def __init__(self, max_size: int):
        """Initialize a RingList with a maximum size."""

        assert max_size > 0, "a max_size of zero doesn't make any sense"
        self._max_size: int = max_size
        self._data: list[float] = [0 for _ in range(max_size)]
        self._current_index: int = -1  # -1 means empty

    def clear(self) -> None:
        """Removes all elements from the list."""

        self._current_index = -1

    def is_full(self) -> bool:
        """Returns True if the list is full."""

        return self._current_index >= (self._max_size - 1)

    def append(self, x: float) -> None:
        """Appends an element to the list."""
        self._current_index += 1
        bounded_current_index = self._current_index % self._max_size
        self._data[bounded_current_index] = x

    def get(self) -> list[float]:
        """Returns the list of elements."""
        # list is full
        if self._current_index >= (self._max_size - 1):
            bounded_current_index = self._current_index % self._max_size
            return (
                self._data[bounded_current_index + 1 : self._max_size + 1]
                + self._data[0 : bounded_current_index + 1]
            )

        # list is not empty but not full
        elif self._current_index >= 0:
            return self._data[0 : self._current_index + 1]

        # list is empty
        return []

    def sum(self) -> float:
        """Returns the max size of the list"""
        return sum(self.get())

    def get_max_size(self) -> int:
        return self._max_size

    def set_max_size(self, new_max_size: int) -> None:
        """Sets a new max size fo the list."""
        current_list = self.get()
        self._max_size = new_max_size
        self._data = [0] * new_max_size
        self._current_index = -1
        for item in current_list:
            self.append(item)

    def __str__(self) -> str:
        return str(self.get())


def merge_dicts(old_object: Any, new_object: Any) -> Any:
    """
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
    """

    if old_object is None or new_object is None:
        return new_object

    # merging is only possible when both are dicts
    if (type(old_object) == dict) and (type(new_object) == dict):
        updated_dict = {}

        old_keys = set(old_object.keys())
        new_keys = set(new_object.keys())

        # recursively merge keys that are in both dicts
        for k in old_keys.intersection(new_keys):
            updated_dict[k] = merge_dicts(old_object[k], new_object[k])

        # simple add keys that are only in one of the dicts
        for k in new_keys.difference(old_keys):
            updated_dict[k] = new_object[k]
        for k in old_keys.difference(new_keys):
            updated_dict[k] = old_object[k]

        return updated_dict
    else:
        return new_object
