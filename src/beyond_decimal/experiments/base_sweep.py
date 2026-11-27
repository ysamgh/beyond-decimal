"""EXP-001: compare numeral features while preserving integer values."""

from __future__ import annotations

import csv
from pathlib import Path

from beyond_decimal.number_theory import is_prime
from beyond_decimal.representations import format_integer


def digit_sum(numeral: str, base: int) -> int:
    """Sum digit values in a non-negative canonical numeral."""
    return sum("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(ch) for ch in numeral) if base <= 36 else 0


def run_base_sweep(max_value: int, output_path: str | Path, bases=range(2, 37)) -> int:
    """Write one CSV row per integer/base pair and return the row count.

    The value-level primality column is computed from the integer, not its
    numeral string. Digit sum and length are explicitly representation-level.
    """
    if isinstance(max_value, bool) or not isinstance(max_value, int) or max_value < 0:
        raise ValueError("max_value must be a non-negative integer")
    selected_bases = tuple(bases)
    if not selected_bases:
        raise ValueError("bases must not be empty")
    for base in selected_bases:
        if isinstance(base, bool) or not isinstance(base, int) or not 2 <= base <= 36:
            raise ValueError("each base must be an integer from 2 through 36")

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["value_decimal", "base", "numeral", "digit_length", "digit_sum", "is_prime"]
    rows = 0
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for value in range(max_value + 1):
            prime = is_prime(value)
            for base in selected_bases:
                numeral = format_integer(value, base)
                writer.writerow({
                    "value_decimal": value,
                    "base": base,
                    "numeral": numeral,
                    "digit_length": len(numeral),
                    "digit_sum": digit_sum(numeral, base),
                    "is_prime": str(prime).lower(),
                })
                rows += 1
    return rows
