# EXP-003 — Task-Aware Base Search for Modular Residue Rules

## Research question

For the fixed task "compute an integer's residue modulo m from its base-b digits", do some positional bases yield a shorter exact coefficient-cycle description than others?

## Mathematical basis

If an integer has base-b expansion n = sum(d_k * b^k), then:

n mod m = sum(d_k * (b^k mod m)) mod m.

The sequence c_k = b^k mod m is eventually periodic because it takes values in the finite set {0, ..., m-1}. Its exact preperiod μ and period λ determine a finite coefficient description: c_0 through c_(μ+λ-1), after which the period repeats.

This experiment measures the coefficient sequence, not the complexity of the complete integer or the difficulty of every possible divisibility test.

## Pre-registered search space

- Moduli: 3, 5, 7, 11, 13, 17, 19, 23, 29, and 31.
- Bases: every integer base from 2 through 36.
- One row per modulus/base pair: 350 rows.
- Arithmetic: exact integer modular arithmetic only.

## Pre-registered expectation

For every tested prime modulus m, the search range contains base b = m + 1. Since b ≡ 1 (mod m), its coefficient sequence is constant 1 and has coefficient count 1. The experiment is therefore a baseline/control for the implementation and scoring rule, not a search expected to discover an unknown theorem.

## Primary metric

Coefficient count = μ + λ, the number of coefficients needed to state the non-repeating prefix and one complete cycle.

Tie-breakers, in order:
1. smaller μ (preperiod);
2. smaller λ (period).

All bases tied at the lexicographic minimum are marked as minimal. No arbitrary weighted sum is used.

## Baselines and controls

- Decimal base 10 is the fixed baseline for every modulus.
- The search compares the full declared base range, not a hand-picked subset.
- For prime modulus m and base b not divisible by m, μ = 0 and λ is the multiplicative order of b modulo m.
- If m divides b, the sequence reaches zero after one step (μ = 1, λ = 1).
- The same exact recurrence is used for every base.

## Interpretation policy

A shorter coefficient cycle is a compact description of this specific modular residue rule. It does not establish that the base is universally better, that mental calculation is easier, or that the represented integer has a new property. Results are descriptive and task-dependent.

The search space is finite and explicitly declared. The experiment does not use AI, learned scoring, or post-hoc feature selection.

## Reproduction

`python -m beyond_decimal.experiments.modular --max-base 36 --output research/results/EXP-003-modular-base-sweep.csv`

## Output schema

`modulus, base, preperiod, period, coefficient_count, coefficients, is_minimal`

## Limitations

The selected moduli are a small, predeclared set of primes. The metric counts coefficients and ignores the cost of writing the base, modulus, arithmetic operators, or a rule for generating coefficients. A more complete description-length model would need a declared code for all these elements. The experiment does not claim an information-theoretic optimum.
