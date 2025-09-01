from __future__ import annotations
from typing import Optional
import os
import time
import pytest
import queue
import multiprocessing
import threading

os.environ["TUM_ESM_UTILS_EXPLICIT_IMPORTS"] = "1"
import tum_esm_utils.files
import tum_esm_utils.sqlitelock

lock_multiplier = 4
multiprocessing.set_start_method("spawn", force=True)
res_queue_th: queue.Queue[int] = queue.Queue()
res_queue_mp: queue.Queue[int] = multiprocessing.Queue()  # type: ignore
lockfile_path = tum_esm_utils.files.rel_to_abs_path("./pytest_sqlitelock_test.lock")


def count_queue_items(q: queue.Queue[int]) -> int:
    c = 0
    while True:
        try:
            q.get_nowait()
            c += 1
        except queue.Empty:
            return c


def f(delay: int = 0, q: Optional[queue.Queue[int]] = None) -> int:
    """this funtion will sleep for the amount passed as `delay`, put
    1 into the passed queue (optional) and return 1. It will raise a
    timeout exception when the filelock-aquiring takes longer than
    one second."""

    lock = tum_esm_utils.sqlitelock.SQLiteLock(filepath=lockfile_path, timeout=1 * lock_multiplier)

    try:
        with lock:
            time.sleep(delay)
            if q is not None:
                q.put(1)
        return 1
    except TimeoutError:
        pass
        return 0


@pytest.mark.order(4)
@pytest.mark.quick
def test_sqlitelock_without_concurrency() -> None:
    assert f() == 1
    # calling again to make sure that lock opens again
    assert f() == 1


@pytest.mark.order(4)
@pytest.mark.multithreaded
def test_sqlitelock_with_threading() -> None:
    lock = tum_esm_utils.sqlitelock.SQLiteLock(filepath=lockfile_path, timeout=1)
    assert not lock.is_locked(), "Lock should not be locked"

    t1 = threading.Thread(target=f, kwargs={"delay": 1 * lock_multiplier, "q": res_queue_th})
    t2 = threading.Thread(target=f, kwargs={"delay": 1 * lock_multiplier, "q": res_queue_th})
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    assert count_queue_items(res_queue_th) == 2

    assert not lock.is_locked(), "Lock should not be locked"

    t3 = threading.Thread(target=f, kwargs={"delay": 2 * lock_multiplier, "q": res_queue_th})
    t4 = threading.Thread(target=f, kwargs={"delay": 2 * lock_multiplier, "q": res_queue_th})
    t3.start()
    t4.start()
    t3.join()
    t4.join()
    assert count_queue_items(res_queue_th) == 1

    assert not lock.is_locked(), "Lock should not be locked"


@pytest.mark.order(4)
@pytest.mark.multithreaded
def test_filelock_with_multiprocessing() -> None:
    lock = tum_esm_utils.sqlitelock.SQLiteLock(filepath=lockfile_path, timeout=1.5)
    assert not lock.is_locked(), "Lock should not be locked"

    t1 = multiprocessing.Process(target=f, kwargs={"delay": 1 * lock_multiplier, "q": res_queue_mp})
    t2 = multiprocessing.Process(target=f, kwargs={"delay": 1 * lock_multiplier, "q": res_queue_mp})
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    assert count_queue_items(res_queue_mp) == 2

    assert not lock.is_locked(), "Lock should not be locked"

    t3 = multiprocessing.Process(target=f, kwargs={"delay": 2 * lock_multiplier, "q": res_queue_mp})
    t4 = multiprocessing.Process(target=f, kwargs={"delay": 2 * lock_multiplier, "q": res_queue_mp})
    t3.start()
    t4.start()
    t3.join()
    t4.join()
    assert count_queue_items(res_queue_mp) == 1

    assert not lock.is_locked(), "Lock should not be locked"
