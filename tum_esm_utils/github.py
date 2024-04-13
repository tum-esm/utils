"""Functions for interacting with GitHub.

Implements: `request_github_file`, `request_gitlab_file`"""

from typing import Optional
import requests


def request_github_file(
    repository: str,
    filepath: str,
    access_token: Optional[str] = None,
    branch_name: str = "main",
) -> str:
    """Sends a request and returns the content of the response, as a string.
    Raises an HTTPError if the response status code is not 200.
    
    Args:
        repository:    In the format "owner/repo".
        filepath:      The path to the file in the repository.
        access_token:  The GitHub access token. Only required if the repo is private.
    
    Returns:
        The content of the file as a string.
    """

    response = requests.get(
        f"https://raw.githubusercontent.com/{repository}/{branch_name}/{filepath}",
        headers={
            "Authorization": f"token {access_token}",
            "Accept": "application/text",
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.text


def request_gitlab_file(
    repository: str,
    filepath: str,
    access_token: Optional[str] = None,
    branch_name: str = "main",
    hostname: str = "gitlab.com",
) -> str:
    """Sends a request and returns the content of the response, as a string.
    Raises an HTTPError if the response status code is not 200.
    
    Args:
        repository:    In the format "owner/repo".
        filepath:      The path to the file in the repository.
        access_token:  The GitLab access token. Only required if the repo is private.
        hostname:      The GitLab hostname.
    
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
        timeout=10,
    )
    response.raise_for_status()
    return response.text
