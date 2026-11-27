import csv

import pytest

from beyond_decimal.experiments.mdl_sensitivity import (
    SCHEMES,
    delta_code_length,
    describe_rule,
    gamma_code_length,
    run_replication,
    run_sensitivity,
    select_base,
)
from beyond_decimal.experiments.task_search import TRAIN_MODULI, TEST_MODULI


def test_gamma_and_delta_reference_lengths():
    assert [gamma_code_length(n) for n in range(1, 9)] == [1, 3, 3, 5, 5, 5, 5, 7]
    assert [delta_code_length(n) for n in range(1, 9)] == [1, 4, 4, 5, 5, 5, 5, 8]


@pytest.mark.parametrize("encoder", [gamma_code_length, delta_code_length])
@pytest.mark.parametrize("value", [0, -1, True, 2.5])
def test_prefix_code_length_rejects_invalid_values(encoder, value):
    with pytest.raises(ValueError):
        encoder(value)


def test_coefficient_gamma_plus_one_handles_zero():
    item = describe_rule(2, 7, "gamma_metadata_gamma_coefficients")
    assert item["coefficient_mode"] == "gamma_plus_one"
    assert item["coefficient_bits"] > 0
    assert item["total_bits"] == (
        item["model_bits"] + item["metadata_bits"] + item["coefficient_bits"]
    )


def test_all_four_schemes_select_only_from_training_set():
    for scheme in SCHEMES:
        selected, scores = select_base(TRAIN_MODULI, range(2, 37), scheme)
        assert 2 <= selected <= 36
        assert len(scores) == 35
        assert all(len(values) == len(TRAIN_MODULI) for values in scores.values())
    assert set(TRAIN_MODULI).isdisjoint(TEST_MODULI)


def test_sensitivity_exports_expected_rows_and_selected_holdout(tmp_path):
    path = tmp_path / "sensitivity.csv"
    assert run_sensitivity(path) == 4 * 35 * (len(TRAIN_MODULI) + len(TEST_MODULI))
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for scheme in SCHEMES:
        selected_test = [
            row for row in rows
            if row["scheme"] == scheme and row["split"] == "test"
            and row["selected_on_training"] == "true"
        ]
        assert len(selected_test) == len(TEST_MODULI)


def test_replication_contains_locked_base_nine(tmp_path):
    path = tmp_path / "replication.csv"
    count = run_replication(path)
    assert count >= 4 * 3 * 16
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for scheme in SCHEMES:
        locked = [
            row for row in rows
            if row["scheme"] == scheme and row["role"] == "locked_base9"
        ]
        assert len(locked) == 16
        assert {row["base"] for row in locked} == {"9"}
