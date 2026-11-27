import csv

import pytest

from beyond_decimal.experiments.mersenne import run_mersenne_sweep


def test_mersenne_sweep_generates_expected_values_and_features(tmp_path):
    output = tmp_path / "mersenne.csv"
    count = run_mersenne_sweep(7, output, bases=[2, 10, 13])
    assert count == 7 * 3

    with output.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == count
    for exponent in range(1, 8):
        same_exponent = [row for row in rows if int(row["exponent"]) == exponent]
        assert len({row["value_decimal"] for row in same_exponent}) == 1
        assert len({row["value_is_prime"] for row in same_exponent}) == 1
        assert all(row["binary_is_all_ones"] == "true" for row in same_exponent)

    row_4_base_10 = next(
        row for row in rows
        if row["exponent"] == "4" and row["base"] == "10"
    )
    assert row_4_base_10["value_decimal"] == "15"
    assert row_4_base_10["numeral"] == "15"
    assert row_4_base_10["value_is_prime"] == "false"


@pytest.mark.parametrize("bad_exponent", [0, -1, 1.5, True])
def test_rejects_invalid_exponents(tmp_path, bad_exponent):
    with pytest.raises(ValueError):
        run_mersenne_sweep(bad_exponent, tmp_path / "out.csv", bases=[2])


def test_rejects_invalid_bases(tmp_path):
    with pytest.raises(ValueError):
        run_mersenne_sweep(3, tmp_path / "out.csv", bases=[1, 2])
