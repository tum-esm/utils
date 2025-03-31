from __future__ import annotations
from typing import Optional
import os
import time
import queue

import pytest
import tum_esm_utils
import multiprocessing

multiprocessing.set_start_method("spawn", force=True)

import threading

TIMEOUT_UNIT = 0.5
res_queue_th: queue.Queue[int] = queue.Queue()
res_queue_mp: queue.Queue[int] = multiprocessing.Queue()  # type: ignore
lockfile_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "pytest_filelock_test.lock",
)


def count_queue_items(q: queue.Queue[int]) -> int:
    c = 0
    while True:
        try:
            q.get_nowait()
            c += 1
        except queue.Empty:
            return c


@tum_esm_utils.decorators.with_filelock(lockfile_path=lockfile_path, timeout=TIMEOUT_UNIT * 2)
def f(delay: int = 0, q: Optional[queue.Queue[int]] = None) -> int:
    """this funtion will sleep for the amount passed as `delay`, put
    1 into the passed queue (optional) and return 1. It will raise a
    timeout exception when the filelock-aquiring takes longer than
    one second."""

    time.sleep(TIMEOUT_UNIT * delay)
    if q is not None:
        q.put(1)
    return 1


@pytest.mark.order(4)
def test_filelock_without_concurrency() -> None:
    assert f() == 1

    # calling again to make sure that lock opens again
    assert f() == 1


@pytest.mark.order(4)
@pytest.mark.multithreaded
def test_filelock_with_threading() -> None:
    """takes quite long because I had to increase `TIMEOUT_UNIT`
    to `3` for it to work on GitHub's CI small runners"""

    t1 = threading.Thread(target=f, kwargs={"delay": 1, "q": res_queue_th})
    t2 = threading.Thread(target=f, kwargs={"delay": 1, "q": res_queue_th})
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    assert count_queue_items(res_queue_th) == 2

    t3 = threading.Thread(target=f, kwargs={"delay": 3, "q": res_queue_th})
    t4 = threading.Thread(target=f, kwargs={"delay": 3, "q": res_queue_th})
    t3.start()
    t4.start()
    t3.join()
    t4.join()
    assert count_queue_items(res_queue_th) == 1


@pytest.mark.order(4)
@pytest.mark.multithreaded
def test_filelock_with_multiprocessing() -> None:
    """takes quite long because I had to increase `TIMEOUT_UNIT`
    to `3` for it to work on GitHub's CI small runners"""

    t1 = multiprocessing.Process(target=f, kwargs={"delay": 1, "q": res_queue_mp})
    t2 = multiprocessing.Process(target=f, kwargs={"delay": 1, "q": res_queue_mp})
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    assert count_queue_items(res_queue_mp) == 2

    t3 = multiprocessing.Process(target=f, kwargs={"delay": 3, "q": res_queue_mp})
    t4 = multiprocessing.Process(target=f, kwargs={"delay": 3, "q": res_queue_mp})
    t3.start()
    t4.start()
    t3.join()
    t4.join()
    assert count_queue_items(res_queue_mp) == 1
