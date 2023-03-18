from typing import Any, Optional
import requests


def request_github_file(
    github_repository: str,
    filepath: str,
    access_token: Optional[str] = None,
) -> str:
    """Sends a request and returns the content of the response, in unicode."""
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
