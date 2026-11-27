"""EXP-007: sensitivity analysis across alternative integer code families."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from statistics import mean
from typing import Iterable

from .modular import coefficient_cycle
from .task_search import TRAIN_MODULI, TEST_MODULI
from .replication import REPLICATION_MODULI, LOCKED_BASE

BASELINES = (2, 10)
DEFAULT_BASES = range(2, 37)
SCHEMES = (
    "gamma_metadata_fixed_coefficients",
    "gamma_metadata_gamma_coefficients",
    "delta_metadata_fixed_coefficients",
    "delta_metadata_gamma_coefficients",
)


def gamma_code_length(value: int) -> int:
    """Elias gamma code length for positive integers."""
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError("value must be a positive integer")
    return 2 * (value.bit_length() - 1) + 1


def delta_code_length(value: int) -> int:
    """Elias delta code length for positive integers."""
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError("value must be a positive integer")
    exponent = value.bit_length() - 1
    return gamma_code_length(exponent + 1) + exponent


def describe_rule(base: int, modulus: int, scheme: str) -> dict[str, int | str]:
    """Compute total and component bits under one frozen code combination.

    Metadata (base, modulus, preperiod+1, period) uses gamma or delta.
    Coefficients use either fixed width ceil(log2(modulus)) or Elias gamma
    on coefficient+1 (the +1 maps zero to a positive integer).
    The shared 8-bit model tag is charged in every scheme.
    """
    if scheme not in SCHEMES:
        raise ValueError(f"scheme must be one of {SCHEMES}")
    if isinstance(base, bool) or not isinstance(base, int) or base < 2:
        raise ValueError("base must be an integer >= 2")
    if isinstance(modulus, bool) or not isinstance(modulus, int) or modulus < 2:
        raise ValueError("modulus must be an integer >= 2")

    preperiod, period, coefficients = coefficient_cycle(base, modulus)
    metadata_encoder = delta_code_length if scheme.startswith("delta_") else gamma_code_length
    metadata_bits = (
        metadata_encoder(base) + metadata_encoder(modulus)
        + metadata_encoder(preperiod + 1) + metadata_encoder(period)
    )
    if scheme.endswith("gamma_coefficients"):
        coefficient_bits = sum(gamma_code_length(value + 1) for value in coefficients)
        coefficient_mode = "gamma_plus_one"
    else:
        width = (modulus - 1).bit_length()
        coefficient_bits = len(coefficients) * width
        coefficient_mode = "fixed_width"
    model_bits = 8
    total = model_bits + metadata_bits + coefficient_bits
    return {
        "scheme": scheme,
        "base": base,
        "modulus": modulus,
        "preperiod": preperiod,
        "period": period,
        "coefficient_count": len(coefficients),
        "model_bits": model_bits,
        "metadata_bits": metadata_bits,
        "coefficient_bits": coefficient_bits,
        "total_bits": total,
        "coefficient_mode": coefficient_mode,
    }


def select_base(
    training_moduli: Iterable[int],
    bases: Iterable[int],
    scheme: str,
) -> tuple[int, dict[int, tuple[int, ...]]]:
    """Select a candidate using training moduli only."""
    moduli, candidates = tuple(training_moduli), tuple(bases)
    if not moduli or not candidates:
        raise ValueError("training_moduli and bases must not be empty")
    if len(set(moduli)) != len(moduli) or len(set(candidates)) != len(candidates):
        raise ValueError("moduli and bases must be unique")
    scores = {
        base: tuple(int(describe_rule(base, m, scheme)["total_bits"]) for m in moduli)
        for base in candidates
    }
    selected = min(
        candidates,
        key=lambda b: (mean(scores[b]), max(scores[b]), b),
    )
    return selected, scores


def _write(path: str | Path, rows: list[dict[str, object]]) -> int:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "scheme", "split", "base", "modulus", "preperiod", "period",
        "coefficient_count", "model_bits", "metadata_bits",
        "coefficient_bits", "total_bits", "coefficient_mode",
        "selected_on_training", "role",
    ]
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def run_sensitivity(
    output_path: str | Path,
    training_moduli: Iterable[int] = TRAIN_MODULI,
    test_moduli: Iterable[int] = TEST_MODULI,
    bases: Iterable[int] = DEFAULT_BASES,
) -> int:
    """Run four code schemes; independently select each on the training split."""
    train, test, candidates = tuple(training_moduli), tuple(test_moduli), tuple(bases)
    if not train or not test or not candidates or set(train) & set(test):
        raise ValueError("non-empty, disjoint training and test moduli are required")
    rows: list[dict[str, object]] = []
    for scheme in SCHEMES:
        selected, _ = select_base(train, candidates, scheme)
        for split, moduli in (("train", train), ("test", test)):
            for base in candidates:
                for modulus in moduli:
                    item = describe_rule(base, modulus, scheme)
                    rows.append({
                        **item, "split": split,
                        "selected_on_training": str(base == selected).lower(),
                        "role": "selected" if base == selected else (
                            "fixed_baseline" if base in BASELINES else "candidate"
                        ),
                    })
    return _write(output_path, rows)


def run_replication(output_path: str | Path) -> int:
    """Evaluate train-selected bases, locked base 9, and fixed baselines."""
    rows: list[dict[str, object]] = []
    for scheme in SCHEMES:
        selected, _ = select_base(TRAIN_MODULI, DEFAULT_BASES, scheme)
        evaluated = list(dict.fromkeys((selected, LOCKED_BASE, *BASELINES)))
        for modulus in REPLICATION_MODULI:
            for base in evaluated:
                item = describe_rule(base, modulus, scheme)
                role = (
                    "training_selected" if base == selected else
                    "locked_base9" if base == LOCKED_BASE else
                    "fixed_baseline"
                )
                rows.append({
                    **item, "split": "replication",
                    "selected_on_training": str(base == selected).lower(),
                    "role": role,
                })
    return _write(output_path, rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run EXP-007 code-scheme sensitivity.")
    parser.add_argument("--output", type=Path, default=Path(
        "research/results/EXP-007-code-sensitivity.csv"
    ))
    parser.add_argument("--replication-output", type=Path, default=Path(
        "research/results/EXP-007-replication.csv"
    ))
    args = parser.parse_args()
    first = run_sensitivity(args.output)
    second = run_replication(args.replication_output)
    print(f"Wrote {first} sensitivity rows and {second} replication rows.")


if __name__ == "__main__":
    main()
