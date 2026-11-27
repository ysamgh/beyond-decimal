# EXP-006 Results — Explicit Code-Length Objective

## Selection

The frozen two-part code selected **base 9** using training moduli only. Ranking used mean total encoded bits, then maximum training code length, then lower base.

| Base | Mean training bits | Maximum training bits |
|---:|---:|---:|
| 9 | 132.125 | 210 |
| 10 | 219.125 | 398 |
| 2 | 288.500 | 500 |

The selected base was not reselected on either evaluation set.

## Held-out evaluation (EXP-004 test moduli)

| Strategy | Base | Mean total bits | Maximum total bits |
|---|---:|---:|---:|
| Selected candidate | 9 | 262.750 | 390 |
| Decimal | 10 | 279.125 | 714 |
| Binary | 2 | 363.625 | 738 |

Relative to decimal, base 9 reduced mean encoded length by **5.867%** on this held-out set. Relative to binary, the reduction was **27.741%**.

## Independent replication (EXP-005 moduli)

Base 9 remained locked; no selection was performed on these 16 new moduli.

| Strategy | Base | Mean total bits | Maximum total bits |
|---|---:|---:|---:|
| Locked candidate | 9 | 538.938 | 804 |
| Decimal | 10 | 795.063 | 1486 |
| Binary | 2 | 826.938 | 1482 |

Relative to decimal, base 9 reduced mean encoded length by **32.214%**; relative to binary, by **34.827%**.

## Dataset and reproducibility

- Search CSV rows: 560 (35 bases × 16 train/held-out modulus observations).
- Replication CSV rows: 48 (16 moduli × 3 locked strategies).
- Each CSV row records the component bit costs, not only the total.
- Code: `src/beyond_decimal/experiments/mdl.py`.
- Tests: `tests/test_mdl.py`.

## Interpretation and limitations

This result strengthens the narrow EXP-004/005 observation under a more explicit objective. It does **not** establish universal base-9 superiority. The outcome depends on the chosen rule family and the specified two-part code. The fixed 8-bit model tag is common to all candidates; base, modulus, preperiod, period, and coefficient payload are charged. Decoder implementation size, runtime, search cost, and human interpretability are not included. This is not a complete search over MDL model classes or coding schemes.

The next experiment should separately measure wall-clock/runtime and search cost, then stress-test alternative reasonable code designs (for example, a different prefix code or coefficient encoding) before any broader conclusion.
