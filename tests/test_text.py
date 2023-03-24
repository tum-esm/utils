import tum_esm_utils


def test_get_random_string() -> None:
    assert len(tum_esm_utils.text.get_random_string(length=5)) == 5


def test_pad_string() -> None:
    assert (
        tum_esm_utils.text.pad_string(
            "hello", min_width=10, pad_position="left", fill_char="-"
        )
        == "-----hello"
    )
    assert (
        tum_esm_utils.text.pad_string(
            "hello", min_width=10, pad_position="right", fill_char="-"
        )
        == "hello-----"
    )


def test_is_date_string() -> None:
    assert tum_esm_utils.text.is_date_string("20230101")
    assert not tum_esm_utils.text.is_date_string("20231301")
    assert not tum_esm_utils.text.is_date_string("20230132")


def test_is_datetime_string() -> None:
    assert tum_esm_utils.text.is_datetime_string("20230101 00:00:00")
    assert not tum_esm_utils.text.is_datetime_string("20231301 00:00:00")
    assert not tum_esm_utils.text.is_datetime_string("20230132 00:00:00")

    assert tum_esm_utils.text.is_datetime_string("20230101 13:47:59")
    assert not tum_esm_utils.text.is_datetime_string("20230101 24:47:59")
    assert not tum_esm_utils.text.is_datetime_string("20230101 13:60:59")
    assert not tum_esm_utils.text.is_datetime_string("20230101 13:47:65")


def test_is_rfc3339_datetime_string() -> None:
    assert tum_esm_utils.text.is_rfc3339_datetime_string("1990-12-31T23:59:59+00:00")
    assert tum_esm_utils.text.is_rfc3339_datetime_string("2021-01-01T00:00:00+01:00")
    assert tum_esm_utils.text.is_rfc3339_datetime_string("2021-01-01T00:00:00-01:00")
    assert not tum_esm_utils.text.is_rfc3339_datetime_string("2021-01-01T00:00:00")
    assert not tum_esm_utils.text.is_rfc3339_datetime_string(
        "2021-01-01T00:00:65+01:00"
    )


def test_insert_replacements() -> None:
    assert (
        tum_esm_utils.text.insert_replacements("Hello %YOU%!", {"YOU": "replacement"})
        == "Hello replacement!"
    )
