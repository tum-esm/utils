from tum_esm_utils.datastructures import merge_dicts


def test_merge_dicts() -> None:
    assert merge_dicts(
        old_object={"a": 3, "b": {"c": 50, "e": None}},
        new_object={"b": {"e": 80}},
    ) == {"a": 3, "b": {"c": 50, "e": 80}}

    assert merge_dicts(
        old_object={"a": [1, 2, 3]},
        new_object={"b": {"e": 80}},
    ) == {"a": [1, 2, 3], "b": {"e": 80}}

    assert merge_dicts(
        old_object={"a": [1, 2, 3]},
        new_object={"a": {"e": 80}},
    ) == {"a": {"e": 80}}
