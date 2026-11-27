"""EXP-003: base-dependent coefficient cycles for modular arithmetic."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable

DEFAULT_MODULI = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31)


def coefficient_cycle(base: int, modulus: int) -> tuple[int, int, tuple[int, ...]]:
    """Return (preperiod, period, coefficients) for base**k mod modulus.

    The sequence starts at k=0. The returned coefficients contain exactly
    the non-repeating prefix followed by one complete cycle.
    """
    if isinstance(base, bool) or not isinstance(base, int) or base < 2:
        raise ValueError("base must be an integer >= 2")
    if isinstance(modulus, bool) or not isinstance(modulus, int) or modulus < 2:
        raise ValueError("modulus must be an integer >= 2")

    first_seen: dict[int, int] = {}
    coefficients: list[int] = []
    residue = 1 % modulus
    while residue not in first_seen:
        first_seen[residue] = len(coefficients)
        coefficients.append(residue)
        residue = (residue * base) % modulus

    preperiod = first_seen[residue]
    period = len(coefficients) - preperiod
    return preperiod, period, tuple(coefficients)


def evaluate_residue_digits(
    digits: Iterable[int], base: int, modulus: int
) -> int:
    """Evaluate little-endian base digits modulo modulus using the cycle."""
    if isinstance(base, bool) or not isinstance(base, int) or base < 2:
        raise ValueError("base must be an integer >= 2")
    if isinstance(modulus, bool) or not isinstance(modulus, int) or modulus < 2:
        raise ValueError("modulus must be an integer >= 2")
    selected_digits = tuple(digits)
    for digit in selected_digits:
        if isinstance(digit, bool) or not isinstance(digit, int) or not 0 <= digit < base:
            raise ValueError("each digit must be an integer in [0, base)")
    preperiod, period, coefficients = coefficient_cycle(base, modulus)
    total = 0
    for index, digit in enumerate(selected_digits):
        coefficient_index = (
            index if index < preperiod
            else preperiod + (index - preperiod) % period
        )
        total = (total + digit * coefficients[coefficient_index]) % modulus
    return total


def run_modular_sweep(
    output_path: str | Path,
    moduli: Iterable[int] = DEFAULT_MODULI,
    bases: Iterable[int] = range(2, 37),
) -> int:
    """Export exact modular coefficient-cycle metrics for each modulus/base."""
    selected_moduli = tuple(moduli)
    selected_bases = tuple(bases)
    if not selected_moduli:
        raise ValueError("moduli must not be empty")
    if not selected_bases:
        raise ValueError("bases must not be empty")
    for modulus in selected_moduli:
        if isinstance(modulus, bool) or not isinstance(modulus, int) or modulus < 2:
            raise ValueError("each modulus must be an integer >= 2")
    for base in selected_bases:
        if isinstance(base, bool) or not isinstance(base, int) or base < 2:
            raise ValueError("each base must be an integer >= 2")

    rows: list[dict[str, object]] = []
    for modulus in selected_moduli:
        metrics = []
        for base in selected_bases:
            preperiod, period, coefficients = coefficient_cycle(base, modulus)
            metrics.append({
                "modulus": modulus,
                "base": base,
                "preperiod": preperiod,
                "period": period,
                "coefficient_count": len(coefficients),
                "coefficients": " ".join(map(str, coefficients)),
            })
        best_score = min(
            (row["coefficient_count"], row["preperiod"], row["period"])
            for row in metrics
        )
        for row in metrics:
            row["is_minimal"] = str(
                (row["coefficient_count"], row["preperiod"], row["period"])
                == best_score
            ).lower()
            rows.append(row)

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "modulus", "base", "preperiod", "period", "coefficient_count",
        "coefficients", "is_minimal",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run EXP-003 modular coefficient-cycle base sweep."
    )
    parser.add_argument("--output", type=Path, default=Path(
        "research/results/EXP-003-modular-base-sweep.csv"
    ))
    parser.add_argument("--max-base", type=int, default=36)
    args = parser.parse_args()
    if args.max_base < 2:
        parser.error("--max-base must be >= 2")
    count = run_modular_sweep(args.output, bases=range(2, args.max_base + 1))
    print(f"Wrote {count} rows to {args.output}")


if __name__ == "__main__":
    main()
