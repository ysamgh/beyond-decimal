# EXP-002 — Initial Results

## Run configuration
- Exponents: 1 through 16, inclusive.
- Integer bases: 2 through 36, inclusive.
- Rows: 16 × 35 = 560.
- Arithmetic: exact Python integers.
- Output: `research/results/EXP-002-mersenne-base-sweep.csv`.

## Observations
1. All 560 rows report the binary representation as all ones. This is expected from the identity M_n = 2^n - 1 = 1 + 2 + ... + 2^(n-1); it validates the generator but is not a new discovery.
2. 159 of 560 exponent/base pairs have a numeral consisting of a single repeated digit. This feature is representation-dependent and varies substantially by base.
3. In base 10, repeated-digit representations occur for exponents 1, 2, and 3 in this finite sample only.
4. Among n = 1..16, the Mersenne values classified as prime are M_2 = 3, M_3 = 7, M_5 = 31, M_7 = 127, and M_13 = 8191.
5. M_11 = 2047 is composite (23 × 89), despite the exponent 11 being prime. This is a direct reminder that prime exponents do not guarantee Mersenne primes.

## Interpretation
The experiment demonstrates a clear distinction between a value-level property (primality) and a representation-level feature (repeated digits). The same integer can have different digit patterns in different bases, while its primality remains fixed.

The count 159/560 is descriptive only. It must not be interpreted as evidence that a particular base is intrinsically superior. The search covered many base/exponent combinations, and no task-specific objective or null model was used to establish significance.

## Reproduction
`python -m beyond_decimal.experiments.mersenne --max-exponent 16 --output results/EXP-002-mersenne.csv`

## Limitations
- The exponent range is intentionally small.
- Primality uses trial division, not a specialized Mersenne-primality algorithm.
- The experiment tests a known sequence and does not search for unknown mathematical laws.
- Repeated-digit status is a simple feature, not a principled description-length measure.
- Results are not a proof of any general statement beyond the elementary identity used to construct the sequence.

## Status
Initial deterministic dataset committed. Automated test results for the latest commit are pending.
