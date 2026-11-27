# Roadmap

## Foundation v0.1
- [x] Define research question and scope.
- [x] Document value/representation distinction.
- [x] Establish evidence and exactness policies.
- [x] Implement signed integer conversion for bases 2–36.
- [x] Implement a simple exact primality baseline.
- [x] Add unit tests and continuous integration configuration.
- [x] Execute the repository test suite in GitHub Actions (Python 3.11, 3.12, and 3.13).
- [x] Add first reproducible experiment report (EXP-001 protocol and executable EXP-002 study).

## Milestone 0.2 — Baseline experiments
- [x] Generate Mersenne values and representations across bases 2–36.
- [x] Separate digit features from value-level properties.
- [x] Add deterministic CSV export for Mersenne sweeps.
- [ ] Record runtime and complexity baselines.
- [x] Add cross-modulus held-out base-selection experiment (EXP-004).

## Milestone 0.3 — Pattern analysis
- [x] Define initial pre-registered feature families for EXP-002.
- [ ] Add sequence-level pattern metrics.
- [ ] Add held-out validation and false-discovery controls.
- [x] Publish reproducible experiment script, protocol, dataset, and results report.
- [x] Add modular residue coefficient-cycle analysis with a declared search space.

## Milestone 0.4 — Representation search
- [x] Define a task-specific representation objective.
- [x] Implement a transparent base-selection baseline for modular residue rules.
- [x] Compare fixed-base and task-aware selection on a pre-registered held-out modulus set (EXP-004).
- [ ] Evaluate full description length and search cost.

## Milestone 0.5 — AI-assisted conjecturing
- [ ] Integrate symbolic regression only after baselines exist.
- [ ] Store conjectures as structured records.
- [ ] Add counterexample search and independent verification.
- [ ] Separate model-generated text from verified claims.

## Deferred tracks
Irrational constants, continued fractions, algebraic representations, coordinate/matrix/graph transforms, and Lean proof formalization.
