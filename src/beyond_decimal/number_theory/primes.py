"""Simple deterministic primality baseline for arbitrary-size Python integers."""


def is_prime(n: int) -> bool:
    """Return whether n is prime using trial division up to sqrt(n).

    This is a correctness-oriented baseline, not a high-performance algorithm.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    divisor = 5
    while divisor * divisor <= n:
        if n % divisor == 0 or n % (divisor + 2) == 0:
            return False
        divisor += 6
    return True
