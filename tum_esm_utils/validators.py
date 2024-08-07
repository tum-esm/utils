"""Implements validator utils for use with pydantic models.

Implements: `StrictFilePath`, `StrictDirectoryPath`"""

from __future__ import annotations
from typing import Literal, Optional
import os
import pydantic


class StrictFilePath(pydantic.RootModel[str]):
    """A pydantic model that validates a file path.
    
    Example usage:
    
    ```python
    class MyModel(pyndatic.BaseModel):
        path: StrictFilePath

    m = MyModel(path='/path/to/file') # validates that the file exists
    ```

    The validation can be ignored by setting the context variable:

    ```python
    m = MyModel.model_validate(
        {"path": "somenonexistingpath"},
        context={"ignore-path-existence": True},
    ) # does not raise an error
    ```
    """

    root: str

    @pydantic.field_validator('root')
    @classmethod
    def path_should_exist(cls, v: str, info: pydantic.ValidationInfo) -> str:
        ignore_path_existence = (
            info.context.get('ignore-path-existence') == True
        ) if isinstance(info.context, dict) else False
        if (not ignore_path_existence) and (not os.path.isfile(v)):
            raise ValueError('File does not exist')
        return v


class StrictDirectoryPath(pydantic.RootModel[str]):
    """A pydantic model that validates a directory path.
    
    Example usage:
    
    ```python
    class MyModel(pyndatic.BaseModel):
        path: StrictDirectoryPath

    m = MyModel(path='/path/to/directory') # validates that the directory exists
    ```

    The validation can be ignored by setting the context variable:

    ```python
    m = MyModel.model_validate(
        {"path": "somenonexistingpath"},
        context={"ignore-path-existence": True},
    ) # does not raise an error
    ```
    """

    root: str

    @pydantic.field_validator('root')
    @classmethod
    def path_should_exist(cls, v: str, info: pydantic.ValidationInfo) -> str:
        ignore_path_existence = (
            info.context.get('ignore-path-existence') == True
        ) if isinstance(info.context, dict) else False
        if (not ignore_path_existence) and (not os.path.isdir(v)):
            raise ValueError('Directory does not exist')
        return v


class Version(pydantic.RootModel[str]):
    """A version string in the format of MAJOR.MINOR.PATCH[-(alpha|beta|rc).N]"""

    root: str = pydantic.Field(
        ...,
        pattern=r"^\d+\.\d+\.\d+(-(alpha|beta|rc)\.\d+)?$",
        examples=["1.2.3", "4.5.6-alpha.78", "7.8.9-beta.10", "11.12.13-rc.14"],
    )

    def as_tag(self) -> str:
        """Return the version string as a tag, i.e. vMAJOR.MINOR.PATCH..."""
        return "v" + self.root

    def as_identifier(self) -> str:
        """Return the version string as a number, i.e. MAJOR.MINOR.PATCH..."""
        return self.root

    def _split(
        self
    ) -> tuple[int, int, int, Optional[tuple[Literal["alpha", "beta", "rc"],
                                             int]]]:
        """Split the version string into MAJOR, MINOR, PATCH, and TAG"""
        version, tag = self.root.split("-") if "-" in self.root else (
            self.root, ""
        )
        major, minor, patch = map(int, version.split("."))
        if "-" in self.root:
            tags = tag.split(".")
            return major, minor, patch, (tags[0], int(tags[1]))  # type: ignore
        else:
            return major, minor, patch, None

    # add comparisons
    def __lt__(self, other: Version) -> bool:
        self_major, self_minor, self_patch, self_tag = self._split()
        other_major, other_minor, other_patch, other_tag = other._split()

        if self_major != other_major:
            return self_major < other_major
        if self_minor != other_minor:
            return self_minor < other_minor
        if self_patch != other_patch:
            return self_patch < other_patch

        if self_tag is None:
            return False

        if other_tag is None:
            return True

        assert (self_tag is not None) and (other_tag is not None)
        self_tag_type, self_tag_number = self_tag
        other_tag_type, other_tag_number = other_tag

        if (self_tag_type == "alpha") and (other_tag_type in ["beta", "rc"]):
            return True
        if (self_tag_type == "beta") and (other_tag_type == "rc"):
            return True
        if (self_tag_type == "beta") and (other_tag_type == "alpha"):
            return False
        if (self_tag_type == "rc") and (other_tag_type in ["alpha", "beta"]):
            return False

        assert self_tag_type == other_tag_type
        return self_tag_number < other_tag_number

    def __le__(self, other: Version) -> bool:
        return (self < other) or (self == other)

    def __gt__(self, other: Version) -> bool:
        return not (self <= other)

    def __ge__(self, other: Version) -> bool:
        return not (self < other)
