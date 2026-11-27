"""EXP-005: independent replication with the EXP-004 base locked at 9."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from .task_search import coefficient_cycle_length

REPLICATION_MODULI = (
    107, 109, 113, 127, 131, 137, 139, 149,
    151, 157, 163, 167, 173, 179, 181, 191,
)
LOCKED_BASE = 9
BASELINES = (2, 10)


def run_replication(output_path: str | Path) -> int:
    """Export per-modulus cycle lengths for locked base 9 and fixed baselines."""
    rows = []
    for modulus in REPLICATION_MODULI:
        for base in (LOCKED_BASE, *BASELINES):
            preperiod, period, count = coefficient_cycle_length(base, modulus)
            rows.append({
                "modulus": modulus,
                "base": base,
                "preperiod": preperiod,
                "period": period,
                "coefficient_count": count,
                "role": "locked_candidate" if base == LOCKED_BASE else "fixed_baseline",
            })

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["modulus", "base", "preperiod", "period", "coefficient_count", "role"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run EXP-005 locked-base independent replication."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("research/results/EXP-005-base9-replication.csv"),
    )
    args = parser.parse_args()
    count = run_replication(args.output)
    print(f"Wrote {count} rows to {args.output}")


if __name__ == "__main__":
    main()
