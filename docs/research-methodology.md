# Research Methodology

## Experimental unit
Every experiment must define its research question, hypothesis, objects, admissible representations, transformations, data provenance, baselines, controls, metrics, stopping conditions, software versions, parameters, outputs, limitations, and reproduction instructions.

## Comparison protocol
Hold underlying integer values fixed. Only their representations may vary.

For each value n and base b:
1. Encode n in base b.
2. Decode the numeral and assert the result equals n.
3. Compute value-level properties from n, not from the numeral string.
4. Compute representation-dependent features from the numeral string.
5. Store both result classes separately.

## Baselines
Compare decimal, binary, all supported bases in a declared range, and a task-specific algorithm that does not use digit features.

## Metrics
Possible metrics include round-trip correctness, feature regularity, description length under a declared coding scheme, search runtime, memory, hypothesis precision, false-discovery rate, held-out generalization, counterexamples found, and proof status. Define metrics before inspecting results.

## Discovery and verification
Evidence stages:
- OBSERVED: a pattern appears in finite data.
- CONJECTURED: a precise general statement is proposed.
- STRESS_TESTED: broader tests and counterexample searches have run.
- PROVEN: a valid mathematical proof has been supplied and checked.
- REFUTED: a counterexample disproves the conjecture.

Passing finite tests never establishes a universal theorem.

## Multiple testing
Searching many bases, features, ranges, and models increases accidental-pattern risk. Record the full search space, separate exploratory from confirmatory experiments, and validate findings on held-out data.

## Exactness policy
Use integers for integer arithmetic and rationals for exact rational calculations. Do not use binary floating point for base conversion or exact divisibility. For irrational constants, record precision, algorithm, rounding mode, and error bounds.
