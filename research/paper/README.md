# First arXiv Paper — Research Protocol

**Project:** Beyond Decimal  
**Status:** Protocol draft; not a submission-ready manuscript  
**Target output:** One reproducible computational research paper  
**Working title:** *Task-Specific Description Lengths of Modular Coefficient Cycles Across Positional Bases: A Held-Out and Independent Replication Study*

## 1. Scope decision

The first paper will be deliberately narrower than the long-term Beyond Decimal vision.

It will study one precise question:

> For the modular coefficient-cycle task already implemented in EXP-004–006, how sensitive is the selected positional base and its apparent compression advantage to the choice of an explicit, decodable description-length scheme?

The paper will not claim that base 9 is universally optimal, that decimal notation constrains human thought, or that a general AI system has discovered a new mathematical law.

The long-term autonomous research system is a separate engineering/research programme. The first paper will establish a trustworthy benchmark and evidence protocol that such a system can later use.

## 2. Current evidence (from EXP-004–006)

The existing draft branch `research/foundation-v0.1` contains:
- A base-selection experiment with a training/held-out split.
- A locked-base independent replication on 16 additional moduli.
- EXP-006's task-specific two-part code, charging for model identifier, base, modulus, preperiod, period, and coefficient payload.
- CSV outputs with component-level bit accounting and automated tests.

Reported EXP-006 means:
- Held-out: base 9 = 262.750 bits; base 10 = 279.125; base 2 = 363.625.
- Independent replication: base 9 = 538.938 bits; base 10 = 795.063; base 2 = 826.938.

These are preliminary reported results, not yet independently audited for the paper. The manuscript must regenerate all tables from a clean checkout and preserve the exact commit, environment, command, and output hashes.

## 3. Primary research questions

**RQ1 — Coding-scheme sensitivity:** Does the base selected on training moduli remain the same under multiple defensible, explicitly specified, uniquely decodable code-length schemes?

**RQ2 — Generalization:** Does the training-selected base retain a shorter mean description length on untouched held-out and independent replication moduli?

**RQ3 — Cost accounting:** How do encoded rule length, search cost, runtime, and implementation/decoder complexity differ when measured separately?

**RQ4 — Robustness:** Which parts of the result are stable across modulus ranges, candidate-base ranges, train/test partitions, and reasonable coding choices?

## 4. Hypotheses (to be preregistered before new confirmatory runs)

- H1: Under the currently frozen EXP-006 code, the training-selected base has lower mean code length than the fixed decimal and binary baselines on held-out data.
- H2: The ranking is not invariant to all reasonable code designs; report the degree of sensitivity rather than hiding it.
- H3: Any compression advantage in encoded rule length does not automatically imply lower search runtime or lower total computational cost.
- H4: A result that survives untouched evaluation and independent replication is stronger evidence than a result selected and evaluated on the same moduli.

The hypotheses may be rejected. Do not change them after inspecting confirmatory results without clearly marking the analysis as exploratory.

## 5. Required experiments before manuscript freeze

### EXP-007 — Alternative code-design sensitivity
Implement at least two additional uniquely decodable metadata code designs (for example, Elias delta and a clearly specified alternative universal integer code). Keep the model family, candidate bases, coefficient-cycle definition, and data splits fixed. Document every charged field. Verify decoder round trips and Kraft/unique-decodability assumptions where applicable.

### EXP-008 — Coefficient payload sensitivity
Compare the current fixed-width coefficient payload with at least one valid alternative encoding. The alternative must be specified exactly and be uniquely decodable. Include all metadata needed to decode it. Do not compare raw bit counts from incompatible or incomplete codes.

### EXP-009 — Search-cost accounting
Measure wall-clock time, number of candidate evaluations, memory where practical, and hardware/software environment. Report encoded rule length separately from the cost of discovering the rule. Include a fixed, reproducible benchmark protocol.

### EXP-010 — Robustness and partition sensitivity
Use additional preregistered modulus ranges or repeated partitions. Keep the final independent replication set untouched until the protocol and implementation are frozen. Avoid treating correlated observations as independent statistical replicates.

### EXP-011 — Negative controls
Include controls where digit-level patterns should not be interpreted as value-level mathematical laws. Verify that all value-level properties are computed from the underlying integer, not inferred from its numeral string. Include counterexample searches for any generated conjecture.

## 6. Methodological requirements

1. **Representation invariance:** For each integer, verify encode/decode round trips exactly.
2. **Separation of levels:** Distinguish value-level facts from representation-dependent features.
3. **No test leakage:** Candidate selection must use training data only. Held-out and replication data must never influence selection.
4. **Full search disclosure:** Record every base, modulus, feature, coding scheme, parameter, and failed run considered.
5. **Pre-registration:** Freeze primary outcomes and analysis choices before confirmatory evaluation.
6. **Exact arithmetic:** Use integer arithmetic for modular calculations and bit lengths.
7. **Reproducibility:** A clean checkout must regenerate tables and figures with documented commands.
8. **Negative and null results:** Report results that weaken or fail to support the hypotheses.
9. **No overclaiming:** A shorter code under a specified code is not universal simplicity, mathematical truth, or human cognitive advantage.
10. **AI provenance:** If AI is later used for hypothesis generation, record model/provider/version, prompts, generated candidates, human decisions, and independent verification. AI output is not proof.

## 7. Literature review workstream

Before claiming novelty, search and synthesize primary sources on:
- Minimum Description Length and two-part codes.
- Universal integer codes and prefix-free coding.
- Modular arithmetic and periodic coefficient sequences.
- Automated theory exploration and computational experimentation.
- Multiple testing, data leakage, and reproducibility in computational discovery.

For each source, record the exact claim it supports, the relation to this paper, and what it does not establish. Compare the proposed task and coding objective with prior work. Do not use an AI-generated bibliography without checking every source and bibliographic field.

## 8. Manuscript structure

1. Title and abstract
2. Introduction and precise contribution
3. Related work
4. Mathematical and computational definitions
5. Experimental protocol and coding schemes
6. Data splits and leakage controls
7. Results
8. Sensitivity and robustness analyses
9. Runtime and search-cost analysis
10. Limitations and threats to validity
11. Reproducibility statement
12. Conclusion
13. References

The abstract must be written only after confirmatory experiments are complete.

## 9. Proposed arXiv classification

Candidate primary category: **math.NT** (Number Theory).  
Possible secondary category: **cs.CC** (Computational Complexity) only if the final paper makes a substantive, well-supported contribution relevant to that category. Do not select categories merely to broaden visibility. Confirm the current category taxonomy and endorsement requirement during submission.

## 10. Acceptance gates (internal; not arXiv acceptance criteria)

Do not submit until all are true:
- [ ] Research question and contribution are narrow and explicit.
- [ ] Related-work review is complete and novelty claims are defensible.
- [ ] EXP-006 results regenerate from a clean checkout.
- [ ] Alternative coding schemes are implemented and validated.
- [ ] Search cost is measured separately from encoded length.
- [ ] Confirmatory splits and independent replication are untouched.
- [ ] Tests pass; data, scripts, environment, and commit are archived.
- [ ] All tables and figures are generated from committed data.
- [ ] Limitations and negative results are explicit.
- [ ] Manuscript compiles from source in a clean environment.
- [ ] Author identity, affiliation wording, ORCID, and license choice are confirmed by the author.
- [ ] arXiv category and any required endorsement are confirmed.

## 11. Milestones

| Milestone | Deliverable | Exit condition |
|---|---|---|
| M0 | Research protocol | Questions, hypotheses, and gates frozen |
| M1 | Literature map | Relevant prior work read and novelty gap stated |
| M2 | EXP-007–008 | Alternative codes validated |
| M3 | EXP-009–011 | Cost, robustness, and negative controls complete |
| M4 | Results package | Clean reproduction and independent audit |
| M5 | Manuscript v1 | Full LaTeX draft and bibliography |
| M6 | Pre-submission review | Technical, mathematical, and language review |
| M7 | arXiv submission | Author submits and responds to any endorsement/moderation requirements |

## 12. Roles and human oversight

The AI research assistant may search literature, draft protocols, implement experiments, run tests, prepare figures, and draft manuscript text. The human author must decide the research question, inspect the evidence, verify claims and citations, approve authorship and license, and personally submit the paper. No AI agent may fabricate data, citations, proofs, or claim scientific validation without evidence.

## 13. Immediate next action

Audit the EXP-006 implementation and outputs, then implement EXP-007 with a second code design while keeping the current training, held-out, and replication sets fixed. Do not merge the existing foundation PR or submit to arXiv merely because the initial result looks favorable.
