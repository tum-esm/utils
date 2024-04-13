"""Implements validator utils for use with pydantic models.

Implements: `StrictFilePath`, `StrictDirectoryPath`"""

from __future__ import annotations
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
