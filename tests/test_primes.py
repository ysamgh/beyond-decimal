import pytest

from beyond_decimal.number_theory import is_prime


@pytest.mark.parametrize("n", [-10, 0, 1, 4, 9, 15, 21, 25, 49, 63, 100])
def test_composites_and_non_primes(n):
    assert is_prime(n) is False


@pytest.mark.parametrize("n", [2, 3, 5, 7, 13, 31, 127, 997])
def test_primes(n):
    assert is_prime(n) is True


def test_rejects_non_integer():
    with pytest.raises(TypeError):
        is_prime(3.0)
