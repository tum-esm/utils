import pytest
import tum_esm_utils


@pytest.mark.quick
def test_request_github_file() -> None:
    c1 = tum_esm_utils.code.request_github_file(
        repository="tum-esm/em27-retrieval-pipeline",
        filepath="pyproject.toml",
        branch_name="main",
    )
    assert len(c1.replace(" ", "")) > 0, "String c1 is empty"

    c2 = tum_esm_utils.code.request_github_file(
        repository="tum-esm/em27-retrieval-pipeline",
        filepath="tests/__init__.py",
        branch_name="main",
    )
    assert len(c2.replace(" ", "")) > 0, "String c2 is empty"

    c3 = tum_esm_utils.code.request_gitlab_file(
        repository="coccon-kit/proffastpylot",
        filepath="README.md",
        branch_name="master",
        hostname="gitlab.eudat.eu",
    )
    assert len(c3.replace(" ", "")) > 0, "String c3 is empty"

    c4 = tum_esm_utils.code.request_gitlab_file(
        repository="coccon-kit/proffastpylot",
        filepath="prfpylot/ILSList.csv",
        branch_name="master",
        hostname="gitlab.eudat.eu",
    )
    assert len(c4.replace(" ", "")) > 0, "String c4 is empty"
