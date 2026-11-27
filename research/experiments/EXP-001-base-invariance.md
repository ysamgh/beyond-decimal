# EXP-001 — Base Representation and Value-Level Invariance

## Question
Does changing the positional base alter integer-level primality, or only the numeral string and digit-derived features?

## Null expectation
For a fixed integer n, primality is independent of the base used to encode n. The numeral, digit length, and digit sum may vary.

## Protocol
1. Enumerate integers from 0 through a declared maximum.
2. Encode each integer in every selected base from 2 through 36.
3. Compute primality once from the integer value.
4. Compute digit length and digit sum from the numeral.
5. Write one CSV row per integer/base pair.
6. Validate the invariant: all rows for a given integer have identical primality.

## Output schema
value_decimal, base, numeral, digit_length, digit_sum, is_prime.

## Reproduction
Install the package with development dependencies. Then call run_base_sweep(max_value=127, output_path="results/EXP-001.csv").

## Interpretation limits
This experiment is a software and conceptual control, not a search for new prime theory. It demonstrates that digit patterns are representation-dependent while primality is value-dependent. A visually regular numeral is not evidence that its value has a special factorization property.

## Status
Protocol and implementation added. Repository CI execution pending.
