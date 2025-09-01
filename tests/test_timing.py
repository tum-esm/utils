from __future__ import annotations
import time
from typing import Callable

import pytest
import tum_esm_utils.timing
import datetime

DURATION = 0.75


@pytest.mark.order(4)
def test_ensure_section_duration() -> None:
    times: list[float] = []
    for _ in range(3):
        with tum_esm_utils.timing.ensure_section_duration(DURATION):
            times.append(time.time())

    assert len(times) == 3
    assert (times[1] - times[0] - DURATION) < 0.02
    assert (times[2] - times[1] - DURATION) < 0.02


@pytest.mark.order(4)
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


@pytest.mark.order(4)
def test_clear_alarm() -> None:
    def func() -> None:
        time.sleep(1.5)

    tum_esm_utils.timing.set_alarm(1, "test")
    tum_esm_utils.timing.clear_alarm()
    func()


@pytest.mark.order(3)
@pytest.mark.quick
def test_date_range() -> None:
    assert tum_esm_utils.timing.date_range(
        datetime.date(2021, 1, 1), datetime.date(2021, 1, 1)
    ) == [datetime.date(2021, 1, 1)]
    assert tum_esm_utils.timing.date_range(
        datetime.date(2021, 1, 1), datetime.date(2021, 1, 2)
    ) == [
        datetime.date(2021, 1, 1),
        datetime.date(2021, 1, 2),
    ]
    assert tum_esm_utils.timing.date_range(
        datetime.date(2021, 1, 1), datetime.date(2021, 1, 3)
    ) == [
        datetime.date(2021, 1, 1),
        datetime.date(2021, 1, 2),
        datetime.date(2021, 1, 3),
    ]

    # test for inputs that are in different months
    assert tum_esm_utils.timing.date_range(
        datetime.date(2021, 1, 28), datetime.date(2021, 2, 2)
    ) == [
        datetime.date(2021, 1, 28),
        datetime.date(2021, 1, 29),
        datetime.date(2021, 1, 30),
        datetime.date(2021, 1, 31),
        datetime.date(2021, 2, 1),
        datetime.date(2021, 2, 2),
    ]

    # test for inputs that are in different years
    assert tum_esm_utils.timing.date_range(
        datetime.date(2021, 12, 28), datetime.date(2022, 1, 3)
    ) == [
        datetime.date(2021, 12, 28),
        datetime.date(2021, 12, 29),
        datetime.date(2021, 12, 30),
        datetime.date(2021, 12, 31),
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
    ]


@pytest.mark.order(3)
@pytest.mark.quick
def test_time_range() -> None:
    ts = tum_esm_utils.timing.time_range(
        datetime.time(12, 0),
        datetime.time(13, 0),
        datetime.timedelta(minutes=10),
    )
    assert ts == [
        datetime.time(12, 0),
        datetime.time(12, 10),
        datetime.time(12, 20),
        datetime.time(12, 30),
        datetime.time(12, 40),
        datetime.time(12, 50),
        datetime.time(13, 0),
    ]

    ts = tum_esm_utils.timing.time_range(
        datetime.time(12, 0),
        datetime.time(13, 0),
        datetime.timedelta(minutes=15),
    )
    assert ts == [
        datetime.time(12, 0),
        datetime.time(12, 15),
        datetime.time(12, 30),
        datetime.time(12, 45),
        datetime.time(13, 0),
    ]

    ts = tum_esm_utils.timing.time_range(
        datetime.time(12, 0),
        datetime.time(12, 0),
        datetime.timedelta(minutes=30),
    )
    assert ts == [datetime.time(12, 0)]

    ts = tum_esm_utils.timing.time_range(
        datetime.time(12, 0),
        datetime.time(15, 0),
        datetime.timedelta(hours=1),
    )
    assert ts == [
        datetime.time(12, 0),
        datetime.time(13, 0),
        datetime.time(14, 0),
        datetime.time(15, 0),
    ]

    ts = tum_esm_utils.timing.time_range(
        datetime.time(12, 0),
        datetime.time(18, 30),
        datetime.timedelta(minutes=90),
    )
    assert ts == [
        datetime.time(12, 0),
        datetime.time(13, 30),
        datetime.time(15, 0),
        datetime.time(16, 30),
        datetime.time(18, 0),
    ]


@pytest.mark.order(3)
@pytest.mark.quick
def test_parse_timezone_string() -> None:
    assert tum_esm_utils.timing.parse_timezone_string("CET", datetime.datetime(2000, 1, 1)) == 1
    assert tum_esm_utils.timing.parse_timezone_string("CET+3", datetime.datetime(2000, 1, 1)) == 4
    assert tum_esm_utils.timing.parse_timezone_string("GMT+2") == 2
    assert tum_esm_utils.timing.parse_timezone_string("UTC-2") == -2
    assert tum_esm_utils.timing.parse_timezone_string("UTC+2.0") == 2
    assert tum_esm_utils.timing.parse_timezone_string("UTC-02:00") == -2
    assert tum_esm_utils.timing.parse_timezone_string("UTC+05:30") == 5.5
    assert tum_esm_utils.timing.parse_timezone_string("UTC-05:30") == -5.5
    assert tum_esm_utils.timing.parse_timezone_string("UTC+5.5") == 5.5
    assert tum_esm_utils.timing.parse_timezone_string("UTC-5.5") == -5.5
    assert tum_esm_utils.timing.parse_timezone_string("UTC+05.5") == 5.5
    assert tum_esm_utils.timing.parse_timezone_string("UTC-05.5") == -5.5


@pytest.mark.order(3)
@pytest.mark.quick
def test_parse_iso_8601_datetime() -> None:
    strings = [
        "2021-01-01T00:00:00",
        "2021-01-01T00:00:00Z",
        "2021-01-01T00:00:00+00:00",
        "2021-01-01T00:00:00+0000",
        "2021-01-01T00:00:00+00",
    ]
    dts = [tum_esm_utils.timing.parse_iso_8601_datetime(s) for s in strings]

    assert dts[0].tzinfo is None
    dts[0] = dts[0].astimezone()
    local_utc_offset = dts[0].utcoffset().total_seconds()  # type: ignore
    dts[0] = (dts[0] + datetime.timedelta(seconds=local_utc_offset)).astimezone(
        datetime.timezone.utc
    )

    assert all([dt == dts[0] for dt in dts[1:]])

    strings = [
        "2019-07-05T03:01:11Z",
        "2019-07-05T03:01:11+03:40",
        "2019-07-05T03:01:11+0340",
        "2019-07-05T03:01:11+03",
    ]
    dts = [tum_esm_utils.timing.parse_iso_8601_datetime(s) for s in strings]

    assert dts[0].tzinfo is not None
    dts[0] = dts[0].astimezone(datetime.timezone.utc) - datetime.timedelta(hours=3, minutes=40)
    dts[3] = dts[3] - datetime.timedelta(minutes=40)

    assert all([dt == dts[0] for dt in dts[1:]])


@pytest.mark.order(3)
@pytest.mark.quick
def test_datetime_span_intersection() -> None:
    d: Callable[[int], datetime.datetime] = lambda _d: datetime.datetime(2021, 1, _d + 1)

    test_cases = [
        # no overlap no gap
        ((d(0), d(1)), (d(1), d(2)), None),
        # no overlap with gap
        ((d(5), d(9)), (d(12), d(15)), None),
        # same size, partially overlapping
        ((d(0), d(2)), (d(1), d(3)), (d(1), d(2))),
        # same size t1 == t2
        ((d(0), d(2)), (d(0), d(2)), (d(0), d(2))),
        # one is inside the other
        ((d(0), d(4)), (d(1), d(3)), (d(1), d(3))),
        # one is inside the other and zero length
        ((d(0), d(4)), (d(1), d(1)), None),
    ]
    for i, (dt_span_1, dt_span_2, expected) in enumerate(test_cases):
        assert tum_esm_utils.timing.datetime_span_intersection(dt_span_1, dt_span_2) == expected, (
            f"Test case {i}a failed"
        )
        assert tum_esm_utils.timing.datetime_span_intersection(dt_span_2, dt_span_1) == expected, (
            f"Test case {i}b failed"
        )


@pytest.mark.order(3)
@pytest.mark.quick
def test_date_span_intersection() -> None:
    d: Callable[[int], datetime.date] = lambda _d: datetime.date(2021, 1, _d + 1)

    test_cases = [
        # no overlap no gap
        ((d(0), d(1)), (d(1), d(2)), (d(1), d(1))),
        # no overlap with gap
        ((d(5), d(9)), (d(12), d(15)), None),
        # same size, partially overlapping
        ((d(0), d(2)), (d(1), d(3)), (d(1), d(2))),
        # same size t1 == t2
        ((d(0), d(2)), (d(0), d(2)), (d(0), d(2))),
        # one is inside the other
        ((d(0), d(4)), (d(1), d(3)), (d(1), d(3))),
        # one is inside the other and zero length
        ((d(0), d(4)), (d(1), d(1)), (d(1), d(1))),
    ]
    for i, (dt_span_1, dt_span_2, expected) in enumerate(test_cases):
        assert tum_esm_utils.timing.date_span_intersection(dt_span_1, dt_span_2) == expected, (
            f"Test case {i}a failed"
        )
        assert tum_esm_utils.timing.date_span_intersection(dt_span_2, dt_span_1) == expected, (
            f"Test case {i}b failed"
        )
