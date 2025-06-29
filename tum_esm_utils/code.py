"""Functions for interacting with GitHub and GitLab.

Implements: `request_github_file`, `request_gitlab_file`"""

import json
import os
from typing import Optional

import tum_esm_utils


def request_github_file(
    repository: str,
    filepath: str,
    access_token: Optional[str] = None,
    branch_name: str = "main",
    timeout: int = 10,
) -> str:
    """Sends a request and returns the content of the response, as a string.
    Raises an HTTPError if the response status code is not 200.

    Args:
        repository:    In the format "owner/repo".
        filepath:      The path to the file in the repository.
        access_token:  The GitHub access token. Only required if the repo is private.
        branch_name:   The branch name.
        timeout:       The request timeout in seconds.

    Returns:
        The content of the file as a string.
    """

    import requests

    headers = {
        "Accept": "application/text",
    }
    if access_token is not None:
        headers["Authorization"] = f"token {access_token}"

    response = requests.get(
        f"https://raw.githubusercontent.com/{repository}/{branch_name}/{filepath}",
        headers=headers,
        timeout=timeout,
        allow_redirects=True,
    )
    response.raise_for_status()
    return response.text


def download_github_release_asset(
    repository: str,
    asset_name: str,
    dst_dir: str,
    final_name: Optional[str] = None,
    access_token: Optional[str] = None,
    force: bool = False,
) -> None:
    """Downloads a specific asset from the latest release of a GitHub repository.

    Args:
        repository:    In the format "owner/repo".
        asset_name:    The name of the asset to download.
        dst_dir:       The directory where the asset will be saved.
        final_name:    Optional final name for the downloaded asset. If None, uses `asset_name`.
        access_token:  The GitHub access token. Only required if the repo is private.
        force:         If True, forces the download even if the file already exists.
    """

    if final_name is None:
        final_name = asset_name
    if os.path.exists(os.path.join(dst_dir, final_name)) and not force:
        return

    try:
        releases = json.loads(
            tum_esm_utils.shell.run_shell_command(
                (
                    f"curl -L "
                    + f'-H "Accept: application/vnd.github+json" '
                    + (f'-H "Authorization: Bearer {access_token}" ' if access_token else "")
                    + ' -H "X-GitHub-Api-Version: 2022-11-28" '
                    + f"https://api.github.com/repos/{repository}/releases"
                )
            )
        )
    except:
        raise RuntimeError(
            f"Repository '{repository}' not found or access token does not have the required permissions."
        )

    url: Optional[str] = None
    for o in sorted(releases, key=lambda x: x["published_at"], reverse=True):
        for asset in o["assets"]:
            if asset["name"] == asset_name:
                url = asset["url"]
                break
    if url is None:
        raise RuntimeError(
            f"Asset '{asset_name}' not found in any release of repository '{repository}'."
        )

    tum_esm_utils.shell.run_shell_command(
        f"curl -L "
        + (f'-H "Authorization: Bearer {access_token}" ' if access_token else "")
        + f'-H "Accept: application/octet-stream" '
        + f"-o {asset_name} "
        + url,
        working_directory=dst_dir,
    )
    if final_name != asset_name:
        final_path = os.path.join(dst_dir, final_name)
        if os.path.exists(final_path):
            os.remove(final_path)
        os.rename(os.path.join(dst_dir, asset_name), final_path)


def request_gitlab_file(
    repository: str,
    filepath: str,
    access_token: Optional[str] = None,
    branch_name: str = "main",
    hostname: str = "gitlab.com",
    timeout: int = 10,
) -> str:
    """Sends a request and returns the content of the response, as a string.
    Raises an HTTPError if the response status code is not 200.

    Args:
        repository:    In the format "owner/repo".
        filepath:      The path to the file in the repository.
        access_token:  The GitLab access token. Only required if the repo is private.
        branch_name:   The branch name.
        hostname:      The GitLab hostname.
        timeout:       The request timeout in seconds.

    Returns:
        The content of the file as a string.
    """

    import requests

    auth_param: str = ""
    if access_token is not None:
        auth_param = f"?private_token={access_token}"
    response = requests.get(
        f"https://{hostname}/{repository}/-/raw/{branch_name}/{filepath}{auth_param}",
        headers={
            "Accept": "application/text",
        },
        timeout=timeout,
    )
    response.raise_for_status()
    return response.text
