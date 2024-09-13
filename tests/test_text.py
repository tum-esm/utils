import tum_esm_utils


def test_get_random_string() -> None:
    assert len(tum_esm_utils.text.get_random_string(length=5)) == 5


def test_pad_string() -> None:
    assert (
        tum_esm_utils.text.pad_string(
            "hello", min_width=10, pad_position="left", fill_char="-"
        ) == "-----hello"
    )
    assert (
        tum_esm_utils.text.pad_string(
            "hello", min_width=10, pad_position="right", fill_char="-"
        ) == "hello-----"
    )


def test_is_date_string() -> None:
    assert tum_esm_utils.text.is_date_string("20230101")
    assert not tum_esm_utils.text.is_date_string("20231301")
    assert not tum_esm_utils.text.is_date_string("20230132")


def test_is_rfc3339_datetime_string() -> None:
    assert not tum_esm_utils.text.is_rfc3339_datetime_string(
        "1990-12-31T23:59:59Z",
    )
    assert tum_esm_utils.text.is_rfc3339_datetime_string(
        "1990-12-31T23:59:59+00:00",
    )
    assert tum_esm_utils.text.is_rfc3339_datetime_string(
        "2021-01-01T00:00:00+01:00",
    )
    assert tum_esm_utils.text.is_rfc3339_datetime_string(
        "2021-01-01T00:00:00-01:00",
    )
    assert not tum_esm_utils.text.is_rfc3339_datetime_string(
        "2021-01-01T00:00:00",
    )
    assert not tum_esm_utils.text.is_rfc3339_datetime_string(
        "2021-01-01T00:00:65+01:00",
    )


def test_insert_replacements() -> None:
    assert (
        tum_esm_utils.text.insert_replacements(
            "Hello %YOU%!", {"YOU": "replacement"}
        ) == "Hello replacement!"
    )


def test_simplify_string_characters() -> None:
    assert tum_esm_utils.text.simplify_string_characters(
        "Héllö wörld!"
    ) == "helloe-woerld"
    assert tum_esm_utils.text.simplify_string_characters(
        "Høllå world!"
    ) == "holla-world"

    assert tum_esm_utils.text.simplify_string_characters(
        "-".join(tum_esm_utils.text.SIMPLE_STRING_REPLACEMENTS.values())
    ) == tum_esm_utils.text.replace_consecutive_characters(
        "-".join(tum_esm_utils.text.SIMPLE_STRING_REPLACEMENTS.values())
    ).strip("-")

    assert tum_esm_utils.text.simplify_string_characters(
        "-".join(tum_esm_utils.text.SIMPLE_STRING_REPLACEMENTS.keys())
    ) == tum_esm_utils.text.replace_consecutive_characters(
        "-".join(tum_esm_utils.text.SIMPLE_STRING_REPLACEMENTS.values())
    ).strip("-")

    assert tum_esm_utils.text.simplify_string_characters(
        "úed", additional_replacements=({"e": "3"})
    ) == "u3d"


def test_replace_consecutive_characters() -> None:
    assert tum_esm_utils.text.replace_consecutive_characters(
        "he--llo---world"
    ) == "he-llo-world"
    assert tum_esm_utils.text.replace_consecutive_characters(
        "  has--  spaced  --  "
    ) == " has- spaced - "
    assert tum_esm_utils.text.replace_consecutive_characters(
        "boooogie-------man---like", characters=["o", "-"]
    ) == "bogie-man-like"
