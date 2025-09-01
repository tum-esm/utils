from typing import Optional
import os
import time
import sqlite3


class SQLiteLock:
    """A file lock based on SQLite transactions.

    The alternative `filelock` package tends to deadlock on our low-spec-CPU
    windows machines. The package `portalocker` uses the `pywin32` package
    which I am not a big fan of due to its documentation and testing quality.

    Usage example:

    ````python
    lock = tum_esm_utils.sqlitelock.SQLiteLock("sqlitelock.lock", timeout=5)

    try:
        with lock:
            # critical section
            pass
    except TimeoutError:
        # could not be acquired within 5 seconds
        pass
    ```

    This function is tested on Windows, Linux."""

    def __init__(
        self,
        filepath: str = "sqlitelock.lock",
        timeout: float = 10,
        poll_interval: float = 0.1,
    ) -> None:
        """Initialize the SqliteFileLock.

        Args:
            filepath: The path to the SQLite database file used for locking.
            timeout: The maximum time to wait for acquiring the lock in seconds.
            poll_interval: The interval between lock acquisition attempts in seconds.
        """

        self.timeout = timeout
        self.poll_interval = poll_interval
        self.is_locked: bool = False

        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # open the connection
        self.conn: sqlite3.Connection = sqlite3.connect(filepath, timeout=0)

    def acquire(self, timeout: Optional[float] = None) -> None:
        """Acquire the lock.

        Args:
            timeout: Optional timeout in seconds. If None, uses the default timeout set during initialization.

        Raises:
            TimeoutError: If the lock could not be acquired within the specified timeout.
        """

        used_timeout = self.timeout
        if timeout is not None:
            used_timeout = timeout
        start_time = time.time()

        while True:
            try:
                self.conn.execute("BEGIN EXCLUSIVE")
                self.is_locked = True
                # Success: we now hold the lock until we end the transaction.
                return True
            except sqlite3.OperationalError:
                if (time.time() - start_time) >= used_timeout:
                    raise TimeoutError(
                        f"Could not acquire SqliteFileLock within {used_timeout} seconds."
                    )
                time.sleep(self.poll_interval)

    def release(self) -> None:
        """Release the lock."""

        try:
            self.is_locked = False
            self.conn.execute("ROLLBACK")
        except (sqlite3.OperationalError, sqlite3.ProgrammingError):
            pass

    def is_locked(self) -> bool:
        """Check if the lock is currently held by any process."""

        if self.is_locked:
            return True

        is_locked: bool = False
        try:
            self.acquire(timeout=0)
            is_locked = False
            self.release()
        except TimeoutError:
            is_locked = True
        return is_locked

    def __enter__(self) -> None:
        self.acquire()

    def __exit__(self, exc_type, exc, tb) -> None:
        self.release()

    def __del__(self):
        try:
            self.release()
            self.conn.close()
        except (sqlite3.OperationalError, sqlite3.ProgrammingError):
            pass
