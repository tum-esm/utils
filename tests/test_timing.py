from __future__ import annotations
import time
import tum_esm_utils
import datetime

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


# write a unit test for the function `date_range` in `tum_esm_utils/text.py`
# write a bunch of sample inputs and expected outputs
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


def test_parse_timezone_string() -> None:
    assert tum_esm_utils.timing.parse_timezone_string(
        "CET", datetime.datetime(2000, 1, 1)
    ) == 1
    assert tum_esm_utils.timing.parse_timezone_string(
        "CET+3", datetime.datetime(2000, 1, 1)
    ) == 4
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
    dts[0] = dts[0].astimezone(datetime.timezone.utc)

    assert all([dt == dts[0] for dt in dts[1 :]])

    strings = [
        "2019-07-05T03:01:11Z",
        "2019-07-05T03:01:11+03:40",
        "2019-07-05T03:01:11+0340",
        "2019-07-05T03:01:11+03",
    ]
    dts = [tum_esm_utils.timing.parse_iso_8601_datetime(s) for s in strings]

    assert dts[0].tzinfo is not None
    dts[0] = dts[0].astimezone(datetime.timezone.utc
                              ) - datetime.timedelta(hours=3, minutes=40)
    dts[3] = dts[3] - datetime.timedelta(minutes=40)

    assert all([dt == dts[0] for dt in dts[1 :]])
