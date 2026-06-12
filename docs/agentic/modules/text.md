# `tum_esm_utils.text` API Reference


Functions used for text manipulation/processing.

Implements: `get_random_string`, `pad_string`, `is_date_string`,
`is_rfc3339_datetime_string`, `insert_replacements`, `simplify_string_characters`,
`replace_consecutive_characters`, `RandomLabelGenerator`


##### `get_random_string`

```python
def get_random_string(length: int, forbidden: list[str] = []) -> str
```

Return a random string from lowercase letters.

**Arguments**:

- `length` - The length of the random string.
- `forbidden` - A list of strings that should not be generated.
  

**Returns**:

  A random string.


##### `pad_string`

```python
def pad_string(text: str,
               min_width: int,
               pad_position: Literal["left", "right"] = "left",
               fill_char: Literal["0", " ", "-", "_"] = " ") -> str
```

Pad a string with a fill character to a minimum width.

**Arguments**:

- `text` - The text to pad.
- `min_width` - The minimum width of the text.
- `pad_position` - The position of the padding. Either "left" or "right".
- `fill_char` - The character to use for padding.
  

**Returns**:

  The padded string.


##### `is_date_string`

```python
def is_date_string(date_string: str) -> bool
```

Returns `True` if string is in a valid `YYYYMMDD` format.


##### `is_rfc3339_datetime_string`

```python
def is_rfc3339_datetime_string(rfc3339_datetime_string: str) -> bool
```

Returns `True` if string is in a valid `YYYY-MM-DDTHH:mm:ssZ` (RFC3339)
format. Caution: The appendix of `+00:00` is required for UTC!


##### `insert_replacements`

```python
def insert_replacements(content: str, replacements: dict[str, str]) -> str
```

For every key in replacements, replaces `%key%` in the
content with its value.


##### `simplify_string_characters`

```python
def simplify_string_characters(s: str,
                               additional_replacements: dict[str,
                                                             str] = {}) -> str
```

Simplify a string by replacing special characters with their ASCII counterparts
and removing unwanted characters.

For example, `simplify_string_characters("Héllo, wörld!")` will return `"hello-woerld"`.

**Arguments**:

- `s` - The string to simplify.
- `additional_replacements` - A dictionary of additional replacements to apply.
  `{ "ö": "oe" }` will replace `ö` with `oe`.
  
- `Returns` - The simplified string.


##### `replace_consecutive_characters`

```python
def replace_consecutive_characters(s: str,
                                   characters: list[str] = [" ", "-"]) -> str
```

Replace consecutiv characters in a string (e.g. "hello---world" -> "hello-world"
or "hello   world" -> "hello world").

**Arguments**:

- `s` - The string to process.
- `characters` - A list of characters to replace duplicates of.
  

**Returns**:

  The string with duplicate characters replaced.


### `RandomLabelGenerator` Objects

```python
class RandomLabelGenerator()
```

A class to generate random labels that follow the Docker style naming of
containers, e.g `admiring-archimedes` or `happy-tesla`.

**Usage with tracking duplicates:**

```python
generator = RandomLabelGenerator()
label = generator.generate()
another_label = generator.generate()  # Will not be the same as `label`
generator.free(label)  # Free the label to be used again
```

**Usage without tracking duplicates:**

```python
label = RandomLabelGenerator.generate_fully_random()
```

Source for the names and adjectives: https://github.com/moby/moby/blob/master/pkg/namesgenerator/names-generator.go


##### `__init__`

```python
def __init__(occupied_labels: set[str] | list[str] = set(),
             adjectives: set[str] | list[str] = CONTAINER_ADJECTIVES,
             names: set[str] | list[str] = CONTAINER_NAMES) -> None
```

Initialize the label generator.


##### `generate`

```python
def generate() -> str
```

Generate a random label that is not already occupied.


##### `free`

```python
def free(label: str) -> None
```

Free a label to be used again.


##### `generate_fully_random`

```python
@staticmethod
def generate_fully_random(
        adjectives: set[str] | list[str] = CONTAINER_ADJECTIVES,
        names: set[str] | list[str] = CONTAINER_NAMES) -> str
```

Get a random label without tracking duplicates.

Use an instance of `RandomLabelGenerator` if you want to avoid
duplicates by tracking occupied labels.

