import csv

from beyond_decimal.experiments.replication import (
    LOCKED_BASE,
    REPLICATION_MODULI,
    run_replication,
)


def test_replication_uses_locked_base_and_fixed_baselines(tmp_path):
    output = tmp_path / "replication.csv"
    count = run_replication(output)
    assert count == 3 * len(REPLICATION_MODULI)

    with output.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert {int(row["base"]) for row in rows} == {2, LOCKED_BASE, 10}
    assert {int(row["modulus"]) for row in rows} == set(REPLICATION_MODULI)
    assert all(row["preperiod"] == "0" for row in rows)
