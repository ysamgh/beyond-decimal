import pytest

from beyond_decimal.representations import format_integer, parse_integer


@pytest.mark.parametrize(
    ("value", "base", "expected"),
    [
        (0, 2, "0"),
        (13, 13, "10"),
        (31, 2, "11111"),
        (255, 16, "FF"),
        (-31, 2, "-11111"),
        (123456789, 36, "21I3V9"),
    ],
)
def test_format_integer(value, base, expected):
    assert format_integer(value, base) == expected


@pytest.mark.parametrize("base", range(2, 37))
@pytest.mark.parametrize("value", [0, 1, -1, 13, -255, 2**128 + 12345])
def test_round_trip(value, base):
    assert parse_integer(format_integer(value, base), base) == value


def test_parse_is_case_insensitive():
    assert parse_integer("ff", 16) == 255


@pytest.mark.parametrize("numeral,base", [("", 10), ("-", 10), ("2", 2), ("G", 16)])
def test_invalid_numerals(numeral, base):
    with pytest.raises(ValueError):
        parse_integer(numeral, base)


@pytest.mark.parametrize("base", [1, 37, 2.5, True])
def test_invalid_bases(base):
    with pytest.raises((TypeError, ValueError)):
        format_integer(10, base)
