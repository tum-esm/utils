import re
import tum_esm_utils


def test_get_random_string() -> None:
    assert len(tum_esm_utils.text.get_random_string(length=5)) == 5


def test_pad_string() -> None:
    assert (
        tum_esm_utils.text.pad_string("hello", min_width=10, pad_position="left", fill_char="-")
        == "-----hello"
    )
    assert (
        tum_esm_utils.text.pad_string("hello", min_width=10, pad_position="right", fill_char="-")
        == "hello-----"
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
        tum_esm_utils.text.insert_replacements("Hello %YOU%!", {"YOU": "replacement"})
        == "Hello replacement!"
    )


def test_simplify_string_characters() -> None:
    assert tum_esm_utils.text.simplify_string_characters("Héllö wörld!") == "helloe-woerld"
    assert tum_esm_utils.text.simplify_string_characters("Høllå world!") == "holla-world"

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

    assert (
        tum_esm_utils.text.simplify_string_characters("úed", additional_replacements=({"e": "3"}))
        == "u3d"
    )


def test_replace_consecutive_characters() -> None:
    assert tum_esm_utils.text.replace_consecutive_characters("he--llo---world") == "he-llo-world"
    assert (
        tum_esm_utils.text.replace_consecutive_characters("  has--  spaced  --  ")
        == " has- spaced - "
    )
    assert (
        tum_esm_utils.text.replace_consecutive_characters(
            "boooogie-------man---like", characters=["o", "-"]
        )
        == "bogie-man-like"
    )


def test_container_adjectives_and_names() -> None:
    min_ord, max_ord = ord("a"), ord("z")
    for s in tum_esm_utils.text.CONTAINER_ADJECTIVES.union(tum_esm_utils.text.CONTAINER_NAMES):
        for c in s:
            assert min_ord <= ord(c) <= max_ord, f"Invalid character: {c}"


def test_container_name_generation() -> None:
    label_pattern = re.compile(r"^[a-z]+-[a-z]+$")
    for _ in range(1000):
        label = tum_esm_utils.text.RandomLabelGenerator.generate_fully_random()
        assert label_pattern.match(label), f"Invalid label: {label}"
        adjective, name = label.split("-")
        assert (
            adjective in tum_esm_utils.text.CONTAINER_ADJECTIVES
        ), f"Invalid adjective: {adjective}"
        assert name in tum_esm_utils.text.CONTAINER_NAMES, f"Invalid name: {name}"

    used_labels = set()
    generator = tum_esm_utils.text.RandomLabelGenerator(
        adjectives=set(["a", "b", "c"]), names=set(["d", "e", "f"])
    )
    for i in range(3):
        label = generator.generate()
        assert label not in used_labels, f"Duplicate label: {label}"
        used_labels.add(label)
        adjective, name = label.split("-")
        assert adjective in ["a", "b", "c"], f"Invalid adjective: {adjective}"
        assert name in ["d", "e", "f"], f"Invalid name: {name}"

    used_adjectives = set([label.split("-")[0] for label in used_labels])
    assert len(used_adjectives) == 3, f"Not all adjectives are used equally: {used_adjectives}"

    for i in range(6):
        label = generator.generate()
        assert label not in used_labels, f"Duplicate label: {label}"
        used_labels.add(label)
        adjective, name = label.split("-")
        assert adjective in ["a", "b", "c"], f"Invalid adjective: {adjective}"
        assert name in ["d", "e", "f"], f"Invalid name: {name}"

    try:
        generator.generate()
        assert False, "The generator should have raised an exception"
    except RuntimeError:
        pass

    generator.free("b-d")
    label = generator.generate()
    assert label == "b-d", f"Invalid label: {label}"

    try:
        generator.generate()
        assert False, "The generator should have raised an exception"
    except RuntimeError:
        pass

    for label in used_labels:
        generator.free(label)
    used_labels.clear()

    for i in range(3):
        label = generator.generate()
        assert label not in used_labels, f"Duplicate label: {label}"
        used_labels.add(label)
        adjective, name = label.split("-")
        assert adjective in ["a", "b", "c"], f"Invalid adjective: {adjective}"
        assert name in ["d", "e", "f"], f"Invalid name: {name}"

    used_adjectives = set([label.split("-")[0] for label in used_labels])
    assert len(used_adjectives) == 3, f"Not all adjectives are used equally: {used_adjectives}"

    for i in range(6):
        label = generator.generate()
        assert label not in used_labels, f"Duplicate label: {label}"
        used_labels.add(label)
        adjective, name = label.split("-")
        assert adjective in ["a", "b", "c"], f"Invalid adjective: {adjective}"
        assert name in ["d", "e", "f"], f"Invalid name: {name}"

    generator = tum_esm_utils.text.RandomLabelGenerator()
    for i in range(10):
        label1 = generator.generate()
        generator.free(label1)
        label2 = generator.generate()
        generator.free(label2)
        print(label1, label2)
        same_adjective = label1.split("-")[0] == label2.split("-")[0]
        if not same_adjective:
            break
        if i == 9:
            raise AssertionError(
                f"Generator always uses the same adjective first: {label1.split('-')[0]}"
            )
