from __future__ import annotations
import time
import tum_esm_utils

DURATION = 0.75


def test_ensure_section_duration() -> None:
    times: list[float] = []
    for _ in range(3):
        with tum_esm_utils.timing.ensure_section_duration(DURATION):
            times.append(time.time())

    assert len(times) == 3
    assert (times[1] - times[0] - DURATION) < 0.02
    assert (times[2] - times[1] - DURATION) < 0.02


def test_set_alarm() -> None:
    def func() -> None:
        time.sleep(1.5)

    tum_esm_utils.timing.set_alarm(1, "test")
    try:
        func()
    except TimeoutError as e:
        assert str(e) == "test took too long (timed out after 1 seconds)"
    else:
        raise AssertionError("TimeoutError not raised")


def test_clear_alarm() -> None:
    def func() -> None:
        time.sleep(1.5)

    tum_esm_utils.timing.set_alarm(1, "test")
    tum_esm_utils.timing.clear_alarm()
    func()
