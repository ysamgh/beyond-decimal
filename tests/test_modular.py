import csv

import pytest

from beyond_decimal.experiments.modular import coefficient_cycle, run_modular_sweep


@pytest.mark.parametrize(
    ("base", "modulus", "expected"),
    [
        (10, 7, (0, 6, (1, 3, 2, 6, 4, 5))),
        (10, 3, (0, 1, (1,))),
        (7, 7, (1, 1, (1, 0))),
        (2, 5, (0, 4, (1, 2, 4, 3))),
    ],
)
def test_coefficient_cycle_exact_values(base, modulus, expected):
    assert coefficient_cycle(base, modulus) == expected


@pytest.mark.parametrize("base,modulus", [(1, 7), (10, 1), (True, 7), (10, False)])
def test_coefficient_cycle_rejects_invalid_inputs(base, modulus):
    with pytest.raises(ValueError):
        coefficient_cycle(base, modulus)


def test_modular_sweep_exports_all_pairs_and_marks_all_ties(tmp_path):
    output = tmp_path / "modular.csv"
    count = run_modular_sweep(output, moduli=[3, 7], bases=[2, 8, 10])
    assert count == 6

    with output.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 6
    mod_7 = [row for row in rows if row["modulus"] == "7"]
    assert all(row["is_minimal"] == "true" for row in mod_7 if row["base"] == "8")
    assert next(row for row in mod_7 if row["base"] == "8")["coefficient_count"] == "1"
    assert next(row for row in mod_7 if row["base"] == "10")["coefficient_count"] == "6"


def test_modular_sweep_rejects_empty_inputs(tmp_path):
    with pytest.raises(ValueError):
        run_modular_sweep(tmp_path / "empty.csv", moduli=[])
    with pytest.raises(ValueError):
        run_modular_sweep(tmp_path / "empty.csv", bases=[])
