import csv

from beyond_decimal.experiments import run_base_sweep


def test_base_sweep_preserves_primality_and_writes_expected_rows(tmp_path):
    output = tmp_path / "sweep.csv"
    count = run_base_sweep(20, output, bases=[2, 10, 13])
    assert count == 21 * 3

    with output.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == count
    for value in range(21):
        same_value = [row for row in rows if int(row["value_decimal"]) == value]
        assert len({row["is_prime"] for row in same_value}) == 1

    assert next(row for row in rows if row["value_decimal"] == "13" and row["base"] == "13")["numeral"] == "10"
