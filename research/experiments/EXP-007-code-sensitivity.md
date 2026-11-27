# EXP-007 — Sensitivity to Alternative Coding Schemes

**Status:** computational study; four predeclared code combinations.

## Question

Does the favorable result for base 9 under EXP-006 persist when reasonable parts of the code are changed?

## Frozen scheme grid

We cross two metadata encoders with two coefficient encoders:

| Dimension | Choice A | Choice B |
|---|---|---|
| Metadata (base, modulus, preperiod+1, period) | Elias gamma | Elias delta |
| Coefficient payload | Fixed-width unsigned fields | Elias gamma of coefficient+1 |

Elias gamma length for positive integer (n):
[
L_\gamma(n)=2\lfloor\log_2 n\rfloor+1.
]

Elias delta length:
[
L_\delta(n)=L_\gamma(1+\lfloor\log_2 n\rfloor)+\lfloor\log_2 n\rfloor.
]

For gamma-coded coefficients, encode (c+1) so zero coefficients are represented legally. For fixed-width coefficients, use (w=\lceil\log_2 m\rceil) bits per coefficient. All schemes charge the same 8-bit model identifier. All charge base and modulus metadata.

## Protocol

- Candidate bases: 2–36.
- Training moduli: EXP-004 training set.
- Held-out moduli: EXP-004 test set.
- Independent replication: EXP-005's 16 disjoint moduli.
- Each coding scheme independently selects a base using training mean total bits; ties break by maximum training length, then lower base.
- Evaluate each selected base on held-out moduli without reselection.
- On replication moduli, report the scheme-specific training-selected base, locked EXP-006 base 9, and fixed baselines 2 and 10 (deduplicated if they coincide).
- Exact modular arithmetic; no floating-point approximation in the encoded bit counts.

## Interpretation

The four combinations are a deliberately small sensitivity grid, not an exhaustive set of possible codes. A result that changes across schemes demonstrates metric dependence. A result stable across these choices is stronger robustness evidence but still only applies to this task family and candidate range. Decoder implementation size, wall-clock runtime, and search cost are not included.
