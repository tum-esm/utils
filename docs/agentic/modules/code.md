# `tum_esm_utils.code` API Reference


Functions for interacting with GitHub and GitLab.

Implements: `request_github_file`, `request_gitlab_file`


##### `request_github_file`

```python
def request_github_file(repository: str,
                        filepath: str,
                        access_token: Optional[str] = None,
                        branch_name: str = "main",
                        timeout: int = 10) -> str
```

Sends a request and returns the content of the response, as a string.
Raises an HTTPError if the response status code is not 200.

**Arguments**:

- `repository` - In the format "owner/repo".
- `filepath` - The path to the file in the repository.
- `access_token` - The GitHub access token. Only required if the repo is private.
- `branch_name` - The branch name.
- `timeout` - The request timeout in seconds.
  

**Returns**:

  The content of the file as a string.


##### `download_github_release_asset`

```python
def download_github_release_asset(repository: str,
                                  asset_name: str,
                                  dst_dir: str,
                                  final_name: Optional[str] = None,
                                  access_token: Optional[str] = None,
                                  force: bool = False) -> None
```

Downloads a specific asset from the latest release of a GitHub repository.

Not supported on windows!

**Arguments**:

- `repository` - In the format "owner/repo".
- `asset_name` - The name of the asset to download.
- `dst_dir` - The directory where the asset will be saved.
- `final_name` - Optional final name for the downloaded asset. If None, uses `asset_name`.
- `access_token` - The GitHub access token. Only required if the repo is private.
- `force` - If True, forces the download even if the file already exists.


##### `request_gitlab_file`

```python
def request_gitlab_file(repository: str,
                        filepath: str,
                        access_token: Optional[str] = None,
                        branch_name: str = "main",
                        hostname: str = "gitlab.com",
                        timeout: int = 10) -> str
```

Sends a request and returns the content of the response, as a string.
Raises an HTTPError if the response status code is not 200.

**Arguments**:

- `repository` - In the format "owner/repo".
- `filepath` - The path to the file in the repository.
- `access_token` - The GitLab access token. Only required if the repo is private.
- `branch_name` - The branch name.
- `hostname` - The GitLab hostname.
- `timeout` - The request timeout in seconds.
  

**Returns**:

  The content of the file as a string.

