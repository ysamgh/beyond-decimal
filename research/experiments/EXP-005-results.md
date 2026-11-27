# EXP-005 — Independent Replication Results

## Execution summary

The locked base-9 candidate was evaluated on 16 new prime moduli, disjoint from the EXP-004 training and test sets. The base was not reselected.

| Strategy | Base | Mean coefficient count | Maximum coefficient count |
|---|---:|---:|---:|
| Locked candidate | 9 | 63.625 | 95 |
| Fixed decimal baseline | 10 | 96.438 | 180 |
| Fixed binary baseline | 2 | 99.875 | 180 |

The base-9 mean coefficient count is approximately 34.0% lower than decimal and 36.3% lower than binary on this replication set. Its maximum is 47.2% lower than the maximum for either fixed baseline.

## Per-modulus results

| Modulus | Base 9 | Base 10 | Base 2 |
|---:|---:|---:|---:|
| 107 | 53 | 53 | 106 |
| 109 | 27 | 108 | 36 |
| 113 | 56 | 112 | 28 |
| 127 | 63 | 42 | 7 |
| 131 | 65 | 130 | 130 |
| 137 | 68 | 8 | 68 |
| 139 | 69 | 46 | 138 |
| 149 | 74 | 148 | 148 |
| 151 | 25 | 75 | 15 |
| 157 | 39 | 78 | 52 |
| 163 | 81 | 81 | 162 |
| 167 | 83 | 166 | 83 |
| 173 | 86 | 43 | 172 |
| 179 | 89 | 178 | 178 |
| 181 | 45 | 180 | 180 |
| 191 | 95 | 95 | 95 |

Base 9 does not win on every modulus. It ties decimal at modulus 107, and loses to binary on some moduli. The aggregate advantage is therefore a property of this test set and metric, not pointwise dominance.

## Interpretation

The independent replication supports the EXP-004 observation that base 9 has a lower aggregate coefficient-cycle cost than decimal and binary for this modular-residue task family. The result is stronger than the original eight-modulus test because the candidate remained locked and the new moduli were not used during selection.

It still does not establish universal base superiority. The metric is multiplicative-order/cycle length, not wall-clock runtime, human usability, or a complete description-length measure. No statistical significance claim is made.

## Limitations

- One candidate was locked from a previous finite experiment.
- The replication family contains 16 prime moduli in a bounded range.
- The baselines are only binary and decimal.
- Coefficient count ignores base/modulus encoding cost and algorithmic overhead.
- Further replication should use a broader pre-registered modulus family and additional representation tasks.

## Reproduction

`python -m beyond_decimal.experiments.replication --output research/results/EXP-005-base9-replication.csv`
