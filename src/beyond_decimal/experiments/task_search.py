"""EXP-004: select a numeral base on training moduli and evaluate on holdout."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from statistics import mean
from typing import Iterable

TRAIN_MODULI = (37, 41, 43, 47, 53, 59, 61, 67)
TEST_MODULI = (71, 73, 79, 83, 89, 97, 101, 103)
DEFAULT_BASES = range(2, 37)


def coefficient_cycle_length(base: int, modulus: int) -> tuple[int, int, int]:
    """Return preperiod, period, and total coefficient count for b**k mod m."""
    if isinstance(base, bool) or not isinstance(base, int) or base < 2:
        raise ValueError("base must be an integer >= 2")
    if isinstance(modulus, bool) or not isinstance(modulus, int) or modulus < 2:
        raise ValueError("modulus must be an integer >= 2")

    seen: dict[int, int] = {}
    residue = 1 % modulus
    count = 0
    while residue not in seen:
        seen[residue] = count
        count += 1
        residue = (residue * base) % modulus
    preperiod = seen[residue]
    period = count - preperiod
    return preperiod, period, count


def select_base(
    training_moduli: Iterable[int] = TRAIN_MODULI,
    bases: Iterable[int] = DEFAULT_BASES,
) -> tuple[int, dict[int, tuple[int, int, int]]]:
    """Select by mean training cycle length, then max, then lower base."""
    moduli = tuple(training_moduli)
    candidates = tuple(bases)
    if not moduli or not candidates:
        raise ValueError("training_moduli and bases must not be empty")
    for modulus in moduli:
        if isinstance(modulus, bool) or not isinstance(modulus, int) or modulus < 2:
            raise ValueError("each modulus must be an integer >= 2")
    for base in candidates:
        if isinstance(base, bool) or not isinstance(base, int) or base < 2:
            raise ValueError("each base must be an integer >= 2")

    scores = {}
    for base in candidates:
        scores[base] = {
            modulus: coefficient_cycle_length(base, modulus)
            for modulus in moduli
        }
    selected = min(
        candidates,
        key=lambda base: (
            mean(item[2] for item in scores[base].values()),
            max(item[2] for item in scores[base].values()),
            base,
        ),
    )
    return selected, scores[selected]


def run_cross_modulus_search(
    output_path: str | Path,
    training_moduli: Iterable[int] = TRAIN_MODULI,
    test_moduli: Iterable[int] = TEST_MODULI,
    bases: Iterable[int] = DEFAULT_BASES,
) -> int:
    """Write every base/modulus result and mark the train-selected base."""
    train = tuple(training_moduli)
    test = tuple(test_moduli)
    candidates = tuple(bases)
    if not train or not test or not candidates:
        raise ValueError("training moduli, test moduli, and bases must not be empty")
    if set(train) & set(test):
        raise ValueError("training and test moduli must be disjoint")
    if any(isinstance(m, bool) or not isinstance(m, int) or m < 2 for m in train + test):
        raise ValueError("all moduli must be integers >= 2")
    if any(isinstance(b, bool) or not isinstance(b, int) or b < 2 for b in candidates):
        raise ValueError("all bases must be integers >= 2")

    selected, _ = select_base(train, candidates)
    rows: list[dict[str, object]] = []
    for split, moduli in (("train", train), ("test", test)):
        for base in candidates:
            for modulus in moduli:
                preperiod, period, count = coefficient_cycle_length(base, modulus)
                rows.append({
                    "split": split,
                    "base": base,
                    "modulus": modulus,
                    "preperiod": preperiod,
                    "period": period,
                    "coefficient_count": count,
                    "selected_on_training": str(base == selected).lower(),
                    "baseline": str(base in (2, 10)).lower(),
                })

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "split", "base", "modulus", "preperiod", "period",
        "coefficient_count", "selected_on_training", "baseline",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run EXP-004 cross-modulus held-out base search."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("research/results/EXP-004-cross-modulus-base-search.csv"),
    )
    args = parser.parse_args()
    count = run_cross_modulus_search(args.output)
    print(f"Wrote {count} rows to {args.output}")


if __name__ == "__main__":
    main()
