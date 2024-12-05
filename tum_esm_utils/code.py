"""Functions for interacting with GitHub and GitLab.

Implements: `request_github_file`, `request_gitlab_file`"""

from typing import Optional
import requests


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
