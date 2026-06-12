# `tum_esm_utils.validators` API Reference


Implements validator utils for use with pydantic models.

Implements: `StrictFilePath`, `StrictDirectoryPath`


### `StrictFilePath` Objects

```python
class StrictFilePath(pydantic.RootModel[str])
```

A pydantic model that validates a file path.

Example usage:

```python
class MyModel(pydantic.BaseModel):
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


### `StrictDirectoryPath` Objects

```python
class StrictDirectoryPath(pydantic.RootModel[str])
```

A pydantic model that validates a directory path.

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


### `Version` Objects

```python
class Version(pydantic.RootModel[str])
```

A version string in the format of MAJOR.MINOR.PATCH[-(alpha|beta|rc).N]


##### `as_tag`

```python
def as_tag() -> str
```

Return the version string as a tag, i.e. vMAJOR.MINOR.PATCH...


##### `as_identifier`

```python
def as_identifier() -> str
```

Return the version string as a number, i.e. MAJOR.MINOR.PATCH...


### `StricterBaseModel` Objects

```python
class StricterBaseModel(pydantic.BaseModel)
```

The same as pydantic.BaseModel, but with stricter rules. It does not
allow extra fields and validates assignments after initialization.


### `StrictIPv4Adress` Objects

```python
class StrictIPv4Adress(pydantic.RootModel[str])
```

A pydantic model that validates an IPv4 address.

Example usage:

```python
class MyModel(pyndatic.BaseModel):
    ip: StrictIPv4Adress

m = MyModel(ip='192.186.2.1')
m = MyModel(ip='192.186.2.1:22')
```

