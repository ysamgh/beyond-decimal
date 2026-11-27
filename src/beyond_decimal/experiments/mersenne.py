"""EXP-002: representation sweep for Mersenne numbers."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from beyond_decimal.number_theory import is_prime
from beyond_decimal.representations import format_integer

_DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _digit_sum(numeral: str) -> int:
    return sum(_DIGITS.index(char) for char in numeral)


def run_mersenne_sweep(
    max_exponent: int,
    output_path: str | Path,
    bases=range(2, 37),
) -> int:
    """Write M_n = 2**n - 1 in each selected base.

    Primality is evaluated on the integer value, not its numeral. The
    implementation uses trial division and is intended for modest exponents.
    """
    if isinstance(max_exponent, bool) or not isinstance(max_exponent, int) or max_exponent < 1:
        raise ValueError("max_exponent must be a positive integer")

    selected_bases = tuple(bases)
    if not selected_bases:
        raise ValueError("bases must not be empty")
    for base in selected_bases:
        if isinstance(base, bool) or not isinstance(base, int) or not 2 <= base <= 36:
            raise ValueError("each base must be an integer from 2 through 36")

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "exponent", "exponent_is_prime", "value_decimal", "base", "numeral",
        "digit_length", "digit_sum", "is_repeated_digit",
        "binary_numeral", "binary_is_all_ones", "value_is_prime",
    ]
    row_count = 0

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for exponent in range(1, max_exponent + 1):
            value = (1 << exponent) - 1
            binary = format_integer(value, 2)
            value_is_prime = is_prime(value)
            exponent_is_prime = is_prime(exponent)
            for base in selected_bases:
                numeral = format_integer(value, base)
                writer.writerow({
                    "exponent": exponent,
                    "exponent_is_prime": str(exponent_is_prime).lower(),
                    "value_decimal": value,
                    "base": base,
                    "numeral": numeral,
                    "digit_length": len(numeral),
                    "digit_sum": _digit_sum(numeral),
                    "is_repeated_digit": str(len(set(numeral)) == 1).lower(),
                    "binary_numeral": binary,
                    "binary_is_all_ones": str(set(binary) == {"1"}).lower(),
                    "value_is_prime": str(value_is_prime).lower(),
                })
                row_count += 1
    return row_count


def main() -> None:
    parser = argparse.ArgumentParser(description="Run EXP-002 Mersenne base sweep.")
    parser.add_argument("--max-exponent", type=int, default=16)
    parser.add_argument("--output", type=Path, default=Path("results/EXP-002-mersenne.csv"))
    args = parser.parse_args()
    count = run_mersenne_sweep(args.max_exponent, args.output)
    print(f"Wrote {count} rows to {args.output}")


if __name__ == "__main__":
    main()
