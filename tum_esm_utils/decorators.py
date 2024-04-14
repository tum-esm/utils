"""Decorators that can be used wrap functions.

Implements: `with_filelock`"""

from __future__ import annotations
from typing import Any, Callable, TypeVar, cast
import filelock
import functools

F = TypeVar("F", bound=Callable[..., Any])


class with_filelock:
    """FileLock = Mark, that a file is being used and other programs
    should not interfere. A file "*.lock" will be created and the
    content of this file will make the wrapped function possibly
    wait until other programs are done using it.

    See https://en.wikipedia.org/wiki/Semaphore_(programming).
    
    
    Credits for the typing of higher level decorators goes to
    https://github.com/python/mypy/issues/1551#issuecomment-253978622.
    """
    def __init__(self, lockfile_path: str, timeout: float = -1) -> None:
        """Create a new filelock decorator.
        
        A timeout of -1 means that the code waits forever.
        
        Args:
            lockfile_path: The path to the lockfile.
            timeout:       The time to wait for the lock in seconds."""

        self.lockfile_path: str = lockfile_path
        self.timeout: float = timeout

    def __call__(self, f: F) -> F:
        @functools.wraps(f)
        def wrapper(*args: tuple[Any], **kwargs: dict[str, Any]) -> Any:
            with filelock.FileLock(self.lockfile_path, timeout=self.timeout):
                return f(*args, **kwargs)

        return cast(F, wrapper)
