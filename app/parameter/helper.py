

from typing import Tuple


def format_test(name: str, value, format_fn, maybe=False) -> Tuple[str, str]:
    """
    Formats a test value
    """
    if maybe and value is None:
        return (name, "Missing")
    return (name, format_fn(value))

def format_bool(value: bool) -> str:
    if value:
        return "Ja"
    else:
        return "Nej"