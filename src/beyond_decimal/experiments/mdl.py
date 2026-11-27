"""EXP-006: explicit two-part code length for modular coefficient-cycle rules.

This is a task-specific coding objective, not a claim of universal or
model-class-complete Minimum Description Length.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from statistics import mean
from typing import Iterable

from .modular import coefficient_cycle
from .task_search import TRAIN_MODULI, TEST_MODULI
from .replication import REPLICATION_MODULI, LOCKED_BASE

MODEL_ID_BITS = 8
DEFAULT_BASES = range(2, 37)
BASELINES = (2, 10)


def gamma_code_length(value: int) -> int:
    """Bit length of Elias gamma code for a positive integer."""
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError("gamma-coded value must be a positive integer")
    return 2 * (value.bit_length() - 1) + 1


def describe_rule(base: int, modulus: int) -> dict[str, int]:
    """Return the exact bit accounting for one modular coefficient-cycle rule.

    The code is: fixed 8-bit model identifier; Elias-gamma-coded base,
    modulus, preperiod+1, and period; then one fixed-width field per
    coefficient. The coefficient width is ceil(log2(modulus)); the number
    of fields is preperiod+period and is therefore known from the metadata.
    """
    if isinstance(base, bool) or not isinstance(base, int) or base < 2:
        raise ValueError("base must be an integer >= 2")
    if isinstance(modulus, bool) or not isinstance(modulus, int) or modulus < 2:
        raise ValueError("modulus must be an integer >= 2")

    preperiod, period, coefficients = coefficient_cycle(base, modulus)
    count = len(coefficients)
    width = (modulus - 1).bit_length()
    model_bits = MODEL_ID_BITS
    base_bits = gamma_code_length(base)
    modulus_bits = gamma_code_length(modulus)
    preperiod_bits = gamma_code_length(preperiod + 1)
    period_bits = gamma_code_length(period)
    coefficient_bits = count * width
    total_bits = (
        model_bits + base_bits + modulus_bits + preperiod_bits
        + period_bits + coefficient_bits
    )
    return {
        "base": base,
        "modulus": modulus,
        "preperiod": preperiod,
        "period": period,
        "coefficient_count": count,
        "coefficient_width_bits": width,
        "model_bits": model_bits,
        "base_bits": base_bits,
        "modulus_bits": modulus_bits,
        "preperiod_bits": preperiod_bits,
        "period_bits": period_bits,
        "coefficient_bits": coefficient_bits,
        "total_bits": total_bits,
    }


def select_mdl_base(
    training_moduli: Iterable[int] = TRAIN_MODULI,
    bases: Iterable[int] = DEFAULT_BASES,
) -> tuple[int, dict[int, tuple[int, ...]]]:
    """Select the base by mean total code length, then maximum, then base."""
    moduli, candidates = tuple(training_moduli), tuple(bases)
    if not moduli or not candidates:
        raise ValueError("training_moduli and bases must not be empty")
    if len(set(moduli)) != len(moduli):
        raise ValueError("training moduli must be unique")
    if any(isinstance(m, bool) or not isinstance(m, int) or m < 2 for m in moduli):
        raise ValueError("each modulus must be an integer >= 2")
    if len(set(candidates)) != len(candidates):
        raise ValueError("candidate bases must be unique")
    if any(isinstance(b, bool) or not isinstance(b, int) or b < 2 for b in candidates):
        raise ValueError("each base must be an integer >= 2")
    scores = {
        base: tuple(describe_rule(base, modulus)["total_bits"] for modulus in moduli)
        for base in candidates
    }
    selected = min(
        candidates,
        key=lambda base: (mean(scores[base]), max(scores[base]), base),
    )
    return selected, scores


def _write_rows(path: str | Path, rows: list[dict[str, int | str]]) -> int:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "split", "base", "modulus", "preperiod", "period",
        "coefficient_count", "coefficient_width_bits", "model_bits",
        "base_bits", "modulus_bits", "preperiod_bits", "period_bits",
        "coefficient_bits", "total_bits", "selected_on_training", "role",
    ]
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def run_mdl_search(
    output_path: str | Path,
    training_moduli: Iterable[int] = TRAIN_MODULI,
    test_moduli: Iterable[int] = TEST_MODULI,
    bases: Iterable[int] = DEFAULT_BASES,
) -> int:
    """Select only on training moduli and export all train/test code lengths."""
    train, test, candidates = tuple(training_moduli), tuple(test_moduli), tuple(bases)
    if not train or not test or not candidates:
        raise ValueError("training moduli, test moduli, and bases must not be empty")
    if set(train) & set(test):
        raise ValueError("training and test moduli must be disjoint")
    selected, _ = select_mdl_base(train, candidates)
    rows: list[dict[str, int | str]] = []
    for split, moduli in (("train", train), ("test", test)):
        for base in candidates:
            for modulus in moduli:
                item = describe_rule(base, modulus)
                rows.append({
                    "split": split, **item,
                    "selected_on_training": str(base == selected).lower(),
                    "role": "selected" if base == selected else (
                        "fixed_baseline" if base in BASELINES else "candidate"
                    ),
                })
    return _write_rows(output_path, rows)


def run_mdl_replication(output_path: str | Path) -> int:
    """Evaluate locked EXP-004 base 9 without reselection on new moduli."""
    rows: list[dict[str, int | str]] = []
    for modulus in REPLICATION_MODULI:
        for base in (LOCKED_BASE, *BASELINES):
            item = describe_rule(base, modulus)
            rows.append({
                "split": "replication", **item,
                "selected_on_training": "locked" if base == LOCKED_BASE else "false",
                "role": "locked_candidate" if base == LOCKED_BASE else "fixed_baseline",
            })
    return _write_rows(output_path, rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run EXP-006 explicit code-length study.")
    parser.add_argument("--output", type=Path, default=Path(
        "research/results/EXP-006-mdl-base-search.csv"
    ))
    parser.add_argument("--replication-output", type=Path, default=Path(
        "research/results/EXP-006-mdl-replication.csv"
    ))
    args = parser.parse_args()
    count = run_mdl_search(args.output)
    replicated = run_mdl_replication(args.replication_output)
    print(f"Wrote {count} search rows and {replicated} replication rows.")


if __name__ == "__main__":
    main()
