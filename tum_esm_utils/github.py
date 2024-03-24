"""Functions for interacting with GitHub.

Implements: `request_github_file`"""

from typing import Optional
import requests


def request_github_file(
    github_repository: str,
    filepath: str,
    access_token: Optional[str] = None,
) -> str:
    """Sends a request and returns the content of the response,
    as a string. Raises an HTTPError if the response status code
    is not 200.
    
    Args:
        github_repository:  In the format "owner/repo".
        filepath:           The path to the file in the repository.
        access_token:       The GitHub access token. Only required if
                            the repo is private.
    
    Returns:
        The content of the file as a string.
    """

    response = requests.get(
        f"https://raw.githubusercontent.com/{github_repository}/main/{filepath}",
        headers={
            "Authorization": f"token {access_token}",
            "Accept": "application/text",
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.text


# TODO: add "request gitlab file"
