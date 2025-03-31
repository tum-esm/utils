import pytest
import tum_esm_utils


@pytest.mark.order(3)
@pytest.mark.quick
def test_merge_dicts() -> None:
    assert tum_esm_utils.datastructures.merge_dicts(
        old_object={
            "a": 3,
            "b": {"c": 50, "e": None},
            "c": "test",
        },
        new_object={
            "b": {"e": 80},
        },
    ) == {
        "a": 3,
        "b": {"c": 50, "e": 80},
        "c": "test",
    }

    assert tum_esm_utils.datastructures.merge_dicts(
        old_object={
            "a": [1, 2, 3],
        },
        new_object={
            "b": {"e": 80},
        },
    ) == {
        "a": [1, 2, 3],
        "b": {"e": 80},
    }

    assert tum_esm_utils.datastructures.merge_dicts(
        old_object={
            "a": [1, 2, 3],
        },
        new_object={
            "a": {"e": 80},
        },
    ) == {
        "a": {"e": 80},
    }
