# EXP-005 — Independent Replication of the Locked Base-9 Result

## Research question

Does the base selected by EXP-004 (base 9) retain a lower modular coefficient-cycle cost on a second, independent set of prime moduli?

## Locked prediction and protocol

Before evaluating the new set, lock the selected base to 9. Do not rerun selection or change the base based on these results.

- Locked candidate: base 9.
- Fixed baselines: base 2 and base 10.
- New replication moduli: 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191.
- All moduli are prime and exceed all three bases.
- Primary metric: mean coefficient-cycle length across the 16 moduli.
- Secondary metric: maximum coefficient-cycle length.
- Arithmetic: exact integer modular arithmetic.

This is a replication of the EXP-004 result under the same metric, not a new base-selection exercise.

## Interpretation policy

The candidate base was selected using EXP-004 training data and is frozen here. The replication set is disjoint from both EXP-004 training and test moduli. Report all per-modulus results. A favorable outcome supports repeatability only within this narrowly defined task family and finite sample; it does not imply universal base superiority, lower runtime, or easier mental arithmetic.

## Reproduction

`python -m beyond_decimal.experiments.replication --output research/results/EXP-005-base9-replication.csv`
