from __future__ import annotations
from typing import Optional
import time
import queue
import tum_esm_utils
import multiprocessing
import threading
import tum_esm_utils

multiprocessing.set_start_method("spawn", force=True)
res_queue_th: queue.Queue[int] = queue.Queue()
res_queue_mp: queue.Queue[int] = multiprocessing.Queue()  # type: ignore
lockfile_path = tum_esm_utils.files.rel_to_abs_path("./sqlitelock.lock")


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

    lock = tum_esm_utils.sqlitelock.SQLiteLock(filepath=lockfile_path, timeout=1)

    try:
        with lock:
            print("acquired lock")
            time.sleep(delay)
            if q is not None:
                q.put(1)
            return 1
    except TimeoutError:
        pass


def test_filelock_without_concurrency() -> None:
    assert f() == 1
    # calling again to make sure that lock opens again
    assert f() == 1


def test_filelock_with_threading() -> None:
    lock = tum_esm_utils.sqlitelock.SQLiteLock(filepath=lockfile_path, timeout=1)
    assert not lock.is_locked(), "Lock should not be locked"

    t1 = threading.Thread(target=f, kwargs={"delay": 0.5, "q": res_queue_th})
    t2 = threading.Thread(target=f, kwargs={"delay": 0.5, "q": res_queue_th})
    t1.start()
    t2.start()
    time.sleep(0.1)
    assert lock.is_locked(), "Lock should be locked"
    t1.join()
    t2.join()
    assert count_queue_items(res_queue_th) == 2

    assert not lock.is_locked(), "Lock should not be locked"

    t3 = threading.Thread(target=f, kwargs={"delay": 1.5, "q": res_queue_th})
    t4 = threading.Thread(target=f, kwargs={"delay": 1.5, "q": res_queue_th})
    t3.start()
    t4.start()
    time.sleep(0.1)
    assert lock.is_locked(), "Lock should be locked"
    t3.join()
    t4.join()
    assert count_queue_items(res_queue_th) == 1

    assert not lock.is_locked(), "Lock should not be locked"


def test_filelock_with_multiprocessing() -> None:
    lock = tum_esm_utils.sqlitelock.SQLiteLock(filepath=lockfile_path, timeout=1)
    assert not lock.is_locked(), "Lock should not be locked"

    t1 = multiprocessing.Process(target=f, kwargs={"delay": 0.5, "q": res_queue_mp})
    t2 = multiprocessing.Process(target=f, kwargs={"delay": 0.5, "q": res_queue_mp})
    t1.start()
    t2.start()
    time.sleep(0.1)
    assert lock.is_locked(), "Lock should be locked"
    t1.join()
    t2.join()
    assert count_queue_items(res_queue_mp) == 2

    assert not lock.is_locked(), "Lock should not be locked"

    t3 = multiprocessing.Process(target=f, kwargs={"delay": 1.5, "q": res_queue_mp})
    t4 = multiprocessing.Process(target=f, kwargs={"delay": 1.5, "q": res_queue_mp})
    t3.start()
    t4.start()
    time.sleep(0.1)
    assert lock.is_locked(), "Lock should be locked"
    t3.join()
    t4.join()
    assert count_queue_items(res_queue_mp) == 1

    assert not lock.is_locked(), "Lock should not be locked"
