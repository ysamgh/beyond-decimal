import csv

import pytest

from beyond_decimal.experiments.task_search import (
    TEST_MODULI,
    TRAIN_MODULI,
    coefficient_cycle_length,
    run_cross_modulus_search,
    select_base,
)


def test_coefficient_cycle_length_matches_known_orders():
    assert coefficient_cycle_length(10, 7) == (0, 6, 6)
    assert coefficient_cycle_length(10, 3) == (0, 1, 1)
    assert coefficient_cycle_length(2, 5) == (0, 4, 4)


def test_training_selection_is_deterministic_and_does_not_use_test_set():
    selected, scores = select_base()
    assert selected == 9
    assert len(scores) == len(TRAIN_MODULI)
    assert all(preperiod == 0 for preperiod, _, _ in scores.values())


def test_held_out_evaluation_and_fixed_baselines(tmp_path):
    output = tmp_path / "exp004.csv"
    count = run_cross_modulus_search(output)
    assert count == 35 * (len(TRAIN_MODULI) + len(TEST_MODULI))

    with output.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    test_rows = [row for row in rows if row["split"] == "test"]
    selected_rows = [row for row in test_rows if row["selected_on_training"] == "true"]
    decimal_rows = [row for row in test_rows if row["base"] == "10"]
    assert len(selected_rows) == len(TEST_MODULI)
    assert sum(int(row["coefficient_count"]) for row in selected_rows) / len(selected_rows) == 32
    assert sum(int(row["coefficient_count"]) for row in decimal_rows) / len(decimal_rows) == 34.375


@pytest.mark.parametrize("base,modulus", [(1, 7), (True, 7), (10, 1), (10, False)])
def test_cycle_length_rejects_invalid_inputs(base, modulus):
    with pytest.raises(ValueError):
        coefficient_cycle_length(base, modulus)


def test_search_rejects_overlapping_splits_and_empty_candidates(tmp_path):
    with pytest.raises(ValueError):
        run_cross_modulus_search(tmp_path / "bad.csv", [7], [7], [2, 3])
    with pytest.raises(ValueError):
        run_cross_modulus_search(tmp_path / "bad.csv", [7], [11], [])
