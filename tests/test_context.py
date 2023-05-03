import time
import tum_esm_utils

DURATION = 0.75


def test_ensure_section_duration() -> None:
    times: list[float] = []
    for _ in range(3):
        with tum_esm_utils.context.ensure_section_duration(DURATION):
            times.append(time.time())

    assert len(times) == 3
    assert (times[1] - times[0] - DURATION) < 0.02
    assert (times[2] - times[1] - DURATION) < 0.02
