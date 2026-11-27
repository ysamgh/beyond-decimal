"""Exact conversion between signed integers and positional bases 2..36."""

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_BASE_MIN = 2
_BASE_MAX = len(DIGITS)


def _validate_base(base: int) -> None:
    if isinstance(base, bool) or not isinstance(base, int):
        raise TypeError("base must be an integer")
    if not _BASE_MIN <= base <= _BASE_MAX:
        raise ValueError(f"base must be between {_BASE_MIN} and {_BASE_MAX}")


def format_integer(value: int, base: int) -> str:
    """Return the canonical uppercase base representation of an integer."""
    _validate_base(base)
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("value must be an integer")
    if value == 0:
        return "0"
    sign = "-" if value < 0 else ""
    remaining = abs(value)
    digits: list[str] = []
    while remaining:
        remaining, remainder = divmod(remaining, base)
        digits.append(DIGITS[remainder])
    return sign + "".join(reversed(digits))


def parse_integer(numeral: str, base: int) -> int:
    """Parse a base integer numeral; accepts either letter case."""
    _validate_base(base)
    if not isinstance(numeral, str):
        raise TypeError("numeral must be a string")
    if not numeral:
        raise ValueError("numeral must not be empty")
    text = numeral.upper()
    sign = 1
    if text[0] in "+-":
        sign = -1 if text[0] == "-" else 1
        text = text[1:]
    if not text:
        raise ValueError("numeral must contain at least one digit")
    value = 0
    for char in text:
        digit = DIGITS.find(char)
        if digit < 0 or digit >= base:
            raise ValueError(f"digit {char!r} is not valid in base {base}")
        value = value * base + digit
    return sign * value
