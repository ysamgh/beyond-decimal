# EXP-002 — Mersenne Numbers Across Positional Bases

## Research question
How do the digit-level descriptions of Mersenne numbers change across positional bases, while their underlying integer properties remain fixed?

## Mathematical object
For integer exponent n >= 1, define M_n = 2^n - 1. In base 2, M_n is represented by exactly n consecutive ones:
2^n - 1 = 1 + 2 + 4 + ... + 2^(n-1).

This identity explains the binary pattern. It is not an empirical discovery.

## Pre-registered features
For each exponent and each selected base:
- numeral and digit length;
- digit sum;
- whether all displayed digits are identical;
- primality of the integer value;
- primality of the exponent;
- binary numeral and whether it consists entirely of ones.

Primality is computed from the integer value, never inferred from digit features.

## Protocol
1. Generate exponents 1 through the configured maximum.
2. Compute M_n exactly using integer arithmetic.
3. Encode each value in each selected base from 2 through 36.
4. Compute representation-dependent features from the numeral.
5. Compute value-level primality from M_n.
6. Export one CSV row per exponent/base pair.
7. Check that the binary all-ones property holds for every generated Mersenne value.

## Reproduction
Install the package and run:
`python -m beyond_decimal.experiments.mersenne --max-exponent 16 --output research/results/EXP-002-mersenne-base-sweep.csv`

The default experiment has 16 exponents and 35 bases, producing 560 rows.

## Mathematical controls and limitations
- The binary all-ones pattern follows directly from the geometric sum identity.
- M_n can be composite; for example M_4 = 15 = 3 * 5 and M_6 = 63 = 7 * 9.
- If M_n is prime and n > 1, then n must be prime. The converse is false: M_11 = 2047 = 23 * 89.
- A repeated-digit numeral is a property of the chosen representation, not a new arithmetic property of the integer.
- This experiment uses trial division for primality and is suitable only for modest exponents. It is not a Mersenne-prime search implementation.
- Searching many bases creates multiple-comparison risk. Any apparent pattern requires a separately specified confirmatory experiment.

## Interpretation target
The experiment is a controlled demonstration of representation dependence. It does not claim that a preferred base reveals a new theorem. A later study may ask whether a task-aware representation selector improves a defined prediction or compression task.

## Status
Protocol, implementation, and tests added. Results are generated deterministically by the reproduction command.
