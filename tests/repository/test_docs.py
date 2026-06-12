"""Test whether the automatically generated documentation is up to date.

This is necessary because the documentation build script does not generate
the documentation pages automatically. Otherwise we would have to set up
the full Python environment on the CI server for the documentation build."""

import hashlib
import os
import sys
from typing import List

import pytest

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS_PAGES_DIR = os.path.join(PROJECT_DIR, "docs", "pages")
DOCS_AGENTIC_DIR = os.path.join(PROJECT_DIR, "docs", "agentic")
DOCS_PAGE_FILENAMES = ["index.md", "api-reference.md"]


def get_generated_doc_paths() -> list[str]:
    doc_paths = [os.path.join(DOCS_PAGES_DIR, filename) for filename in DOCS_PAGE_FILENAMES]
    for root, _, filenames in os.walk(DOCS_AGENTIC_DIR):
        for filename in filenames:
            if filename.endswith(".md"):
                doc_paths.append(os.path.join(root, filename))
    return sorted(doc_paths)


def get_checksum(path: str) -> str:
    with open(path, "r") as f:
        content = f.read()
        print(f"Content of {path}:\n{content}")
        return hashlib.md5(content.encode()).hexdigest()


@pytest.mark.order(2)
@pytest.mark.quick
@pytest.mark.skipif(os.name != "posix", reason="Flaky on Windows")
def test_documentation_sync() -> None:
    doc_paths_before = get_generated_doc_paths()
    checksums_before: List[str] = [get_checksum(path) for path in doc_paths_before]

    assert os.system(  # pyright: ignore[reportDeprecated]
        f"{sys.executable} {os.path.join(PROJECT_DIR, 'docs', 'scripts', 'sync-docs.py')}"
    ) == 0

    doc_paths_after = get_generated_doc_paths()
    checksums_after: List[str] = [get_checksum(path) for path in doc_paths_after]

    assert doc_paths_before == doc_paths_after
    assert "".join(checksums_before) == "".join(checksums_after)
