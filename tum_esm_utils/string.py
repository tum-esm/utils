import random
import string


def get_random_string(length: int, forbidden: list[str] = []) -> str:
    """Return a random string from lowercase letter, the strings
    from the list passed as `forbidden` will not be generated"""
    output: str = ""
    while True:
        output = "".join(random.choices(string.ascii_lowercase, k=length))
        if output not in forbidden:
            break
    return output
