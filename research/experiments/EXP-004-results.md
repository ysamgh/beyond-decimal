# EXP-004 — Cross-Modulus Base Selection: Results

## Execution summary

The pre-registered experiment generated 560 rows: 35 candidate bases × 8 training moduli plus 35 candidate bases × 8 held-out moduli. Selection used training data only.

- Selected base: **9**
- Training mean coefficient count: **16.000**
- Training maximum coefficient count: **29**

## Held-out comparison

| Strategy | Base | Mean coefficient count | Maximum coefficient count |
|---|---:|---:|---:|
| Task-aware selection (training only) | 9 | 32.000 | 50 |
| Fixed decimal baseline | 10 | 34.375 | 96 |
| Fixed binary baseline | 2 | 46.875 | 100 |

On these eight held-out moduli, the selected base reduces mean coefficient count by approximately 6.9% relative to decimal and by approximately 31.7% relative to binary. The maximum coefficient count is 50, compared with 96 for decimal and 100 for binary.

## Interpretation

This is evidence of a narrow, task-specific improvement in the declared coefficient-cycle metric on this fixed held-out set. It is not evidence of a universally superior base, and it does not demonstrate lower runtime or easier human calculation.

The result is particularly important because EXP-004 excludes the trivial congruence controls from EXP-003: every modulus is prime and greater than every candidate base. Thus no candidate base can be congruent to 1 or 0 modulo a tested modulus.

The search selects base 9 from training moduli. Its held-out mean is lower than decimal, but the improvement is modest (6.9%) and based on only eight test moduli. The maximum-cycle difference is larger, but also highly dependent on this finite set.

## Limitations and anti-overclaim safeguards

- Only eight training and eight test moduli were used.
- The 35 candidate bases were searched on training data; the held-out set was not used for selection.
- The score counts coefficients, not the full cost of describing or applying the rule.
- No runtime benchmark or human-factors experiment was conducted.
- The test set is fixed and finite; replication on additional pre-registered moduli is required.
- The candidate range and modulus range limit external validity.

## Conclusion

EXP-004 demonstrates a reproducible task-aware selection pipeline and a preliminary held-out advantage for base 9 under the specified metric. Treat this as a benchmark result to replicate, not a mathematical theorem or general recommendation to use base 9.

## Reproduction

`python -m beyond_decimal.experiments.task_search --output research/results/EXP-004-cross-modulus-base-search.csv`
