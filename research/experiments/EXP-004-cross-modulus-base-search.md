# EXP-004 — Cross-Modulus Base Selection with a Held-Out Test Set

## Research question

Can one positional base selected on a fixed training set of modular-residue tasks reduce the coefficient-cycle cost on unseen moduli compared with fixed binary and decimal baselines?

## Task definition

For each prime modulus m, represent an integer in base b and compute its residue modulo m using the exact positional coefficient sequence:

n mod m = sum(d_k * (b^k mod m)) mod m.

The structural cost is the number of coefficients in the eventual cycle of b^k mod m. For the prime moduli used here, all candidate bases are smaller than every modulus, so each sequence is purely periodic and the coefficient count equals the multiplicative order of b modulo m.

This is a narrow, explicitly defined computational task. It is not a general measure of human or machine computational difficulty.

## Pre-registered split

- Training moduli: 37, 41, 43, 47, 53, 59, 61, 67.
- Held-out test moduli: 71, 73, 79, 83, 89, 97, 101, 103.
- Candidate bases: every integer from 2 through 36.
- Fixed baselines: base 2 and base 10.
- Candidate selection: minimize mean training coefficient count; break ties by lower maximum training coefficient count, then lower numeric base.
- No test modulus may influence selection or tie-breaking.

All moduli are prime and exceed the maximum candidate base. This excludes the trivial b ≡ 1 (mod m) and b ≡ 0 (mod m) controls encountered in EXP-003.

## Primary endpoint

Mean coefficient count over the eight held-out moduli for the single base selected on training data.

## Secondary endpoint

Maximum coefficient count over the held-out moduli. Report per-modulus values and both fixed baselines. No arbitrary weighted score is used.

## Reproducibility and controls

- Exact integer modular arithmetic only.
- Complete candidate-by-modulus output is retained.
- Training and test sets are fixed in this protocol.
- Selection is performed only on training data.
- The held-out results are descriptive; the test set is small and deliberately finite.
- No randomization, AI model, or learned parameter is used.

## Interpretation policy

A lower held-out coefficient count supports only this narrow task and metric. It does not imply universal superiority of a base, lower wall-clock runtime, or improved human divisibility performance. The coefficient count omits the cost of specifying the base, modulus, arithmetic procedure, and cycle-generation algorithm.

## Reproduction

`python -m beyond_decimal.experiments.task_search --output research/results/EXP-004-cross-modulus-base-search.csv`
