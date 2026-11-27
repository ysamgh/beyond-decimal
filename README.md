# Beyond Decimal

An AI-assisted computational research laboratory for mathematical representation and discovery.

**Research question:** Can changing the representation of a mathematical object make structure easier to detect, describe, or discover, without changing the underlying object?

The project begins with positional numeral systems and exact integer arithmetic. It will expand only when experiments justify additional representation families.

## Principles
1. A numeral is an encoding of a value. Changing its base does not change the integer it denotes.
2. Computational evidence can suggest a conjecture; it does not establish a universal theorem.
3. Use exact integer and rational arithmetic wherever possible.
4. Make experiments reproducible: record inputs, methods, versions, parameters, outputs, and limitations.
5. Measure usefulness relative to a specified task and explicit metrics.
6. Treat AI as a hypothesis generator, not a mathematical authority.

## Initial scope
- Positional bases 2–36.
- Exact conversion of signed integers.
- Value-level properties such as primality.
- Digit-level feature extraction and pattern analysis.
- Controlled experiments on known sequences and modular-residue tasks, including Mersenne numbers and held-out base selection.

## Quick start
Requires Python 3.11 or newer.

Install: python -m pip install -e ".[dev]"
Test: pytest

Example API: format_integer(31, 2) returns 11111; parse_integer("11111", 2) returns 31; is_prime(31) returns True.

## Repository map
- docs/: research agenda, mathematical foundations, methodology, hypotheses, glossary, roadmap.
- research/: literature review, questions, experiment protocols, findings, and deterministic datasets.
- src/beyond_decimal/: reusable computational library.
- tests/: correctness and regression tests.
- notebooks/: exploratory work; conclusions must be transferred into reproducible experiments.

## What this project does not claim
- Decimal notation changes mathematical truth.
- A finite pattern proves a general law.
- A visually simple digit string is necessarily a simpler mathematical description.
- An AI-generated conjecture is new, correct, or proven.

Status: Foundation v0.1 with EXP-001–EXP-005 baselines. Current milestone: validate task-aware representation selection with held-out data—not autonomous theorem discovery.

See docs/research-agenda.md, docs/research-methodology.md, and docs/roadmap.md.
