# Research Agenda

## Problem statement
Mathematical objects can be represented in many ways: positional numeral systems, algebraic expressions, coordinate systems, matrices, graphs, symbolic expressions, and transforms. The object and its representation must be distinguished.

This project studies whether systematic search over admissible representations can improve discovery, recognition, compression, or explanation of mathematical structure.

## Primary research question
For a specified mathematical task, can an alternative representation make a relevant structure easier to detect or describe, and can that advantage be measured reproducibly?

The word easier must be operationalized. Candidate measures include description length, feature separability, search time, sample complexity, model complexity, and human interpretability.

## Subquestions
1. How do positional bases affect digit-level patterns of the same integer or sequence?
2. Which observed patterns are invariant under base conversion, and which are notation artifacts?
3. Can representation-selection algorithms predict which base is useful for a specified task?
4. Can symbolic regression recover known sequence laws from transformed observations?
5. Can a system generate conjectures and search efficiently for counterexamples?
6. Do non-positional representations offer measurable advantages beyond numeral-base changes?

## Initial scope
In scope: integer positional bases 2–36, signed integer conversion, primality as a value-level property, digit features, and Mersenne numbers as a controlled case study.

Deferred: irrational-constant expansions, continued fractions, symbolic algebra search, Fourier and coordinate transforms, graph and matrix representations, neural models, multi-agent systems, and formal proof automation.

## Contribution target
A reproducible framework for comparing representations against task-specific objectives, with controls against false discovery and notation artifacts. A new theorem is not assumed or promised.
