import csv

import pytest

from beyond_decimal.experiments.mdl import (
    describe_rule,
    gamma_code_length,
    run_mdl_replication,
    run_mdl_search,
    select_mdl_base,
)
from beyond_decimal.experiments.task_search import TRAIN_MODULI, TEST_MODULI


def test_elias_gamma_lengths():
    assert [gamma_code_length(n) for n in range(1, 9)] == [1, 3, 3, 5, 5, 5, 5, 7]


@pytest.mark.parametrize("value", [0, -1, True, 1.5])
def test_gamma_rejects_non_positive_integers(value):
    with pytest.raises(ValueError):
        gamma_code_length(value)


def test_rule_bit_accounting_is_exact_and_includes_metadata():
    item = describe_rule(10, 7)
    assert item["preperiod"] == 0
    assert item["period"] == 6
    assert item["coefficient_count"] == 6
    assert item["coefficient_width_bits"] == 3
    assert item["coefficient_bits"] == 18
    assert item["total_bits"] == sum(item[key] for key in (
        "model_bits", "base_bits", "modulus_bits", "preperiod_bits",
        "period_bits", "coefficient_bits",
    ))


def test_selection_is_training_only_and_deterministic():
    selected, scores = select_mdl_base()
    assert selected == 9
    assert len(scores) == 35
    assert all(len(scores[base]) == len(TRAIN_MODULI) for base in scores)
    # The held-out set is not an argument to the selector.
    assert set(TRAIN_MODULI).isdisjoint(TEST_MODULI)


def test_search_exports_full_train_and_test_accounting(tmp_path):
    path = tmp_path / "exp006.csv"
    count = run_mdl_search(path)
    assert count == 35 * (len(TRAIN_MODULI) + len(TEST_MODULI))
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    selected_test = [
        row for row in rows
        if row["split"] == "test" and row["selected_on_training"] == "true"
    ]
    assert len(selected_test) == len(TEST_MODULI)
    assert all(row["base"] == "9" for row in selected_test)
    assert all(int(row["total_bits"]) > int(row["coefficient_bits"]) for row in rows)


def test_replication_locks_base_nine(tmp_path):
    path = tmp_path / "replication.csv"
    assert run_mdl_replication(path) == 16 * 3
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert sum(row["role"] == "locked_candidate" for row in rows) == 16
    assert {row["base"] for row in rows if row["role"] == "locked_candidate"} == {"9"}
