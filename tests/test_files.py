import os
import tempfile
import polars as pl
import tum_esm_utils

PROJECT_DIR = tum_esm_utils.files.get_parent_dir_path(__file__, current_depth=2)


def test_get_parent_dir_path() -> None:
    parent_dir = tum_esm_utils.files.get_parent_dir_path(
        __file__, current_depth=1
    )
    assert parent_dir == os.path.dirname(os.path.abspath(__file__))

    parent_parent_dir = tum_esm_utils.files.get_parent_dir_path(
        __file__, current_depth=2
    )
    assert parent_parent_dir == os.path.dirname(parent_dir)


def test_rel_to_abs_path() -> None:
    a1 = tum_esm_utils.files.rel_to_abs_path("tests/data/some.csv")
    a2 = tum_esm_utils.files.rel_to_abs_path("tests", "data", "some.csv")
    a3 = tum_esm_utils.files.rel_to_abs_path("tests", "data/some.csv")
    a4 = tum_esm_utils.files.rel_to_abs_path("tests/data", "some.csv")
    a5 = tum_esm_utils.files.rel_to_abs_path("tests/data/", "some.csv")
    a6 = tum_esm_utils.files.rel_to_abs_path(
        "..", "tests", "tests", "data", "some.csv"
    )
    a7 = tum_esm_utils.files.rel_to_abs_path(
        "..", "tests", "tests", "data", "..", "data", "some.csv"
    )
    assert a1 == a2 == a3 == a4 == a5 == a6 == a7

    expected = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "tests", "data", "some.csv"
    )
    assert a1 == expected


def test_read_last_n_lines() -> None:
    with tempfile.TemporaryDirectory() as d:
        filepath = os.path.join(d, "file.txt")
        with open(filepath, "w") as f:
            for i in range(10):
                f.write(f"{i} {'c'*(i+1)}\n")

        r1 = tum_esm_utils.files.read_last_n_lines(
            filepath,
            3,
            ignore_trailing_whitespace=True,
        )
        print(f"r1 = {r1}")
        assert r1 == [
            "7 cccccccc",
            "8 ccccccccc",
            "9 cccccccccc",
        ]

        r2 = tum_esm_utils.files.read_last_n_lines(
            filepath,
            3,
            ignore_trailing_whitespace=False,
        )
        print(f"r2 = {r2}")
        assert r2 == [
            "8 ccccccccc",
            "9 cccccccccc",
            "",
        ]

        with open(filepath, "w") as f:
            for i in range(3):
                f.write(f"{i} {'c'*(i+1)}\n")

        r3 = tum_esm_utils.files.read_last_n_lines(
            filepath,
            2,
            ignore_trailing_whitespace=True,
        )
        print(f"r3 = {r3}")
        assert r3 == ["1 cc", "2 ccc"]

        r4 = tum_esm_utils.files.read_last_n_lines(
            filepath,
            3,
            ignore_trailing_whitespace=True,
        )
        print(f"r4 = {r4}")
        assert r4 == ["0 c", "1 cc", "2 ccc"]

        r5 = tum_esm_utils.files.read_last_n_lines(
            filepath,
            4,
            ignore_trailing_whitespace=True,
        )
        print(f"r5 = {r5}")
        assert r5 == ["0 c", "1 cc", "2 ccc"]


def test_render_directory_tree() -> None:
    ignore = [
        ".git", ".github", ".vscode", ".venv", "dist", ".pdm-build", "docs"
    ]

    expect = ["📁 tests", "📁 tum_esm_utils", "📄 test_files.py", "📄 .gitignore"]
    tree = tum_esm_utils.files.render_directory_tree(PROJECT_DIR, ignore=ignore)
    assert tree is not None
    print(tree)
    for i in ignore:
        assert f"📁 {i}" not in tree
    for e in expect:
        assert e in tree

    tree = tum_esm_utils.files.render_directory_tree(
        PROJECT_DIR, ignore=ignore, max_depth=1
    )
    assert tree is not None
    print(tree)
    ignore.append("📄 test_files.py")
    expect.remove("📄 test_files.py")
    for i in ignore:
        assert f"📁 {i}" not in tree
    for e in expect:
        assert e in tree
