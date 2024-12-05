"""Functions used for text manipulation/processing.

Implements: `get_random_string`, `pad_string`, `is_date_string`,
`is_rfc3339_datetime_string`, `insert_replacements`, `simplify_string_characters`,
`replace_consecutive_characters`, `RandomLabelGenerator`"""

from __future__ import annotations
from typing import Literal
import re
import datetime
import random
import string


def get_random_string(length: int, forbidden: list[str] = []) -> str:
    """Return a random string from lowercase letters.

    Args:
        length:     The length of the random string.
        forbidden:  A list of strings that should not be generated.

    Returns:
        A random string."""

    output: str = ""
    while True:
        output = "".join(random.choices(string.ascii_lowercase, k=length))
        if output not in forbidden:
            break
    return output


def pad_string(
    text: str,
    min_width: int,
    pad_position: Literal["left", "right"] = "left",
    fill_char: Literal["0", " ", "-", "_"] = " ",
) -> str:
    """Pad a string with a fill character to a minimum width.

    Args:
        text:         The text to pad.
        min_width:    The minimum width of the text.
        pad_position: The position of the padding. Either "left" or "right".
        fill_char:    The character to use for padding.

    Returns:
        The padded string."""

    if len(text) >= min_width:
        return text
    else:
        pad = fill_char * (min_width - len(text))
        return (pad + text) if (pad_position == "left") else (text + pad)


def is_date_string(date_string: str) -> bool:
    """Returns `True` if string is in a valid `YYYYMMDD` format."""
    try:
        datetime.datetime.strptime(date_string, "%Y%m%d")
        return True
    except ValueError:
        return False


def is_rfc3339_datetime_string(rfc3339_datetime_string: str) -> bool:
    """Returns `True` if string is in a valid `YYYY-MM-DDTHH:mm:ssZ` (RFC3339)
    format. Caution: The appendix of `+00:00` is required for UTC!"""
    try:
        assert re.match(
            r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\+|\-)\d{2}:\d{2}$",
            rfc3339_datetime_string,
        )
        datetime.datetime.fromisoformat(rfc3339_datetime_string)
        return True
    except (ValueError, AssertionError):
        return False


def insert_replacements(content: str, replacements: dict[str, str]) -> str:
    """For every key in replacements, replaces `%key%` in the
    content with its value."""

    for key, value in replacements.items():
        content = content.replace(f"%{key}%", value)
    return content


"""Characters replaced by their ASCII counterparts in `simplify_string_characters`."""
SIMPLE_STRING_REPLACEMENTS: dict[str, str] = {
    "ö": "oe",
    "ø": "o",
    "ä": "ae",
    "å": "a",
    "ü": "ue",
    "ß": "ss",
    ",": "",
    "é": "e",
    "ë": "e",
    ":": "-",
    "(": "-",
    ")": "-",
    "š": "s",
    ".": "-",
    "/": "-",
    "ó": "o",
    "ð": "d",
    "á": "a",
    "–": "-",
    "ł": "l",
    "‐": "-",
    "’": "",
    "'": "",
    "?": "-",
    "!": "-",
    "ò": "o",
    "&": "-and-",
    "ñ": "n",
    "δ": "d",
    "í": "i",
    "ř": "r",
    "è": "e",
    "₂": "2",
    "₃": "3",
    "₄": "4",
    "₅": "5",
    "₆": "6",
    "₇": "7",
    "₈": "8",
    "₉": "9",
    "ç": "c",
    "ú": "u",
    "“": "",
    "”": "",
    "∆": "d",
}


def simplify_string_characters(
    s: str,
    additional_replacements: dict[str, str] = {},
) -> str:
    """Simplify a string by replacing special characters with their ASCII counterparts
    and removing unwanted characters.

    For example, `simplify_string_characters("Héllo, wörld!")` will return `"hello-woerld"`.

    Args:
        s: The string to simplify.
        additional_replacements: A dictionary of additional replacements to apply.
                                 `{ "ö": "oe" }` will replace `ö` with `oe`.

    Returns: The simplified string.
    """

    all_replacements = {**SIMPLE_STRING_REPLACEMENTS}
    all_replacements.update(additional_replacements)

    s = s.lower().replace(" ", "-")
    for key, value in all_replacements.items():
        s = s.replace(key, value)
    s = s.lower().replace(" ", "-")
    while "--" in s:
        s = s.replace("--", "-")
    s = s.strip("-")
    allowed_chars = "abcdefghijklmnopqrstuvwxyz0123456789-_@"
    dirty = [c for c in s if c not in allowed_chars]
    if len(dirty) > 0:
        raise Exception(f"Found invalid non-replaced characters in name: {dirty} ({s})")
    return s


def replace_consecutive_characters(s: str, characters: list[str] = [" ", "-"]) -> str:
    """Replace consecutiv characters in a string (e.g. "hello---world" -> "hello-world"
    or "hello   world" -> "hello world").

    Args:
        s: The string to process.
        characters: A list of characters to replace duplicates of.

    Returns:
        The string with duplicate characters replaced.
    """

    for c in characters:
        while c + c in s:
            s = s.replace(c + c, c)
    return s


# fmt: off
CONTAINER_ADJECTIVES = set([
    "admiring", "adoring", "affectionate", "agitated", "amazing", "angry",
    "awesome", "beautiful", "blissful", "bold", "boring", "brave", "busy",
    "charming", "clever", "compassionate", "competent", "condescending",
    "confident", "cool", "cranky", "crazy", "dazzling", "determined",
    "distracted", "dreamy", "eager", "ecstatic", "elastic", "elated", "elegant",
    "eloquent", "epic", "exciting", "fervent", "festive", "flamboyant",
    "focused", "friendly", "frosty", "funny", "gallant", "gifted", "goofy",
    "gracious", "great", "happy", "hardcore", "heuristic", "hopeful", "hungry",
    "infallible", "inspiring", "intelligent", "interesting", "jolly", "jovial",
    "keen", "kind", "laughing", "loving", "lucid", "magical", "modest",
    "musing", "mystifying", "naughty", "nervous", "nice", "nifty", "nostalgic",
    "objective", "optimistic", "peaceful", "pedantic", "pensive", "practical",
    "priceless", "quirky", "quizzical", "recursing", "relaxed", "reverent",
    "romantic", "sad", "serene", "sharp", "silly", "sleepy", "stoic", "strange",
    "stupefied", "suspicious", "sweet", "tender", "thirsty", "trusting",
    "unruffled", "upbeat", "vibrant", "vigilant", "vigorous", "wizardly",
    "wonderful", "xenodochial", "youthful", "zealous", "zen"
])

CONTAINER_NAMES = set([
    "agnesi", "albattani", "allen", "almeida", "antonelli", "archimedes",
    "ardinghelli", "aryabhata", "austin", "babbage", "banach", "banzai",
    "bardeen", "bartik", "bassi", "beaver", "bell", "benz", "bhabha",
    "bhaskara", "black", "blackburn", "blackwell", "bohr", "booth", "borg",
    "bose", "bouman", "boyd", "brahmagupta", "brattain", "brown", "buck",
    "burnell", "cannon", "carson", "cartwright", "carver", "cerf",
    "chandrasekhar", "chaplygin", "chatelet", "chatterjee", "chaum",
    "chebyshev", "clarke", "cohen", "colden", "cori", "cray", "curie", "curran",
    "darwin", "davinci", "dewdney", "dhawan", "diffie", "dijkstra", "dirac",
    "driscoll", "dubinsky", "easley", "edison", "einstein", "elbakyan",
    "elgamal", "elion", "ellis", "engelbart", "euclid", "euler", "faraday",
    "feistel", "fermat", "fermi", "feynman", "franklin", "gagarin", "galileo",
    "galois", "ganguly", "gates", "gauss", "germain", "goldberg", "goldstine",
    "goldwasser", "golick", "goodall", "gould", "greider", "grothendieck",
    "haibt", "hamilton", "haslett", "hawking", "heisenberg", "hellman",
    "hermann", "herschel", "hertz", "heyrovsky", "hodgkin", "hofstadter",
    "hoover", "hopper", "hugle", "hypatia", "ishizaka", "jackson", "jang",
    "jemison", "jennings", "jepsen", "johnson", "joliot", "jones", "kalam",
    "kapitsa", "kare", "keldysh", "keller", "kepler", "khayyam", "khorana",
    "kilby", "kirch", "knuth", "kowalevski", "lalande", "lamarr", "lamport",
    "leakey", "leavitt", "lederberg", "lehmann", "lewin", "lichterman",
    "liskov", "lovelace", "lumiere", "mahavira", "margulis", "matsumoto",
    "maxwell", "mayer", "mccarthy", "mcclintock", "mclaren", "mclean",
    "mcnulty", "meitner", "mendel", "mendeleev", "meninsky", "merkle",
    "mestorf", "mirzakhani", "montalcini", "moore", "morse", "moser", "murdock",
    "napier", "nash", "neumann", "newton", "nightingale", "nobel", "noether",
    "northcutt", "noyce", "panini", "pare", "pascal", "pasteur", "payne",
    "perlman", "pike", "poincare", "poitras", "proskuriakova", "ptolemy",
    "raman", "ramanujan", "rhodes", "ride", "ritchie", "robinson", "roentgen",
    "rosalind", "rubin", "saha", "sammet", "sanderson", "satoshi", "shamir",
    "shannon", "shaw", "shirley", "shockley", "shtern", "sinoussi", "snyder",
    "solomon", "spence", "stonebraker", "sutherland", "swanson", "swartz",
    "swirles", "taussig", "tesla", "tharp", "thompson", "torvalds", "tu",
    "turing", "varahamihira", "vaughan", "villani", "visvesvaraya", "volhard",
    "wescoff", "wilbur", "wiles", "williams", "williamson", "wilson", "wing",
    "wozniak", "wright", "wu", "yalow", "yonath", "zhukovsky"
])
# fmt: on


class RandomLabelGenerator:
    """A class to generate random labels that follow the Docker style naming of
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
    """

    def __init__(
        self,
        occupied_labels: set[str] | list[str] = set(),
        adjectives: set[str] | list[str] = CONTAINER_ADJECTIVES,
        names: set[str] | list[str] = CONTAINER_NAMES,
    ) -> None:
        """Initialize the label generator."""

        self.occupied_labels = set(occupied_labels)
        self.adjective_usage_counts: dict[str, int] = {a: 0 for a in adjectives}
        self.adjectives = set(adjectives)
        self.names = set(names)
        for label in occupied_labels:
            assert re.match(r"^[a-z]+-[a-z]+$", label), f"Invalid label: {label}"
            adjective, name = label.split("-")
            assert adjective in adjectives, f"Invalid adjective: {adjective}"
            assert name in names, f"Invalid name: {name}"
            self.adjective_usage_counts[adjective] += 1

    def generate(self) -> str:
        """Generate a random label that is not already occupied."""

        if len(self.occupied_labels) == (len(self.adjectives) * len(self.names)):
            raise RuntimeError("All possible labels are used")

        min_usage_count = min(self.adjective_usage_counts.items(), key=lambda x: x[1])[1]
        available_adjectives = [
            a for a, c in self.adjective_usage_counts.items() if c == min_usage_count
        ]
        random_adjective = random.choice(available_adjectives)

        used_names = set(
            [x.split("-")[1] for x in self.occupied_labels if x.startswith(random_adjective + "-")]
        )
        random_name = random.choice(list(self.names - used_names))

        new_label = f"{random_adjective}-{random_name}"
        assert new_label not in self.occupied_labels, "This should not happen"
        self.occupied_labels.add(new_label)

        self.adjective_usage_counts[random_adjective] += 1
        return new_label

    def free(self, label: str) -> None:
        """Free a label to be used again."""

        self.occupied_labels.remove(label)
        self.adjective_usage_counts[label.split("-")[0]] -= 1

    @staticmethod
    def generate_fully_random(
        adjectives: set[str] | list[str] = CONTAINER_ADJECTIVES,
        names: set[str] | list[str] = CONTAINER_NAMES,
    ) -> str:
        """Get a random label without tracking duplicates.

        Use an instance of `RandomLabelGenerator` if you want to avoid
        duplicates by tracking occupied labels."""

        adjective = random.choice(list(adjectives))
        name = random.choice(list(names))
        return f"{adjective}-{name}"
