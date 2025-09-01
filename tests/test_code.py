import os
import tempfile
import pytest
import tum_esm_utils.code


@pytest.mark.order(3)
@pytest.mark.quick
def test_request_github_file() -> None:
    c1 = tum_esm_utils.code.request_github_file(
        repository="tum-esm/utils",
        filepath="pyproject.toml",
        branch_name="main",
        access_token=os.getenv("GITHUB_API_TOKEN", None),
    )
    assert len(c1.replace(" ", "")) > 0, "String c1 is empty"

    c2 = tum_esm_utils.code.request_github_file(
        repository="tum-esm/utils",
        filepath="tum_esm_utils/__init__.py",
        branch_name="main",
        access_token=os.getenv("GITHUB_API_TOKEN", None),
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


@pytest.mark.order(3)
@pytest.mark.quick
@pytest.mark.skipif(os.name != "posix", reason="Not working on Windows")
def test_download_github_release_asset() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        for finalname in [None, "anothername.exe"]:
            tum_esm_utils.code.download_github_release_asset(
                repository="tum-esm/utils",
                asset_name="tum-esm-group-icon-download-test.png",
                final_name=finalname,
                dst_dir=tmpdir,
                access_token=os.getenv("GITHUB_API_TOKEN", None),
            )
            if finalname is None:
                finalname = "tum-esm-group-icon-download-test.png"
            assert os.path.isfile(os.path.join(tmpdir, finalname)), "File not found"
            assert os.path.getsize(os.path.join(tmpdir, finalname)) > 512, (
                "File size is less than 512B"
            )
