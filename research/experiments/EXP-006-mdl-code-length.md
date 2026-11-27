# EXP-006 — Explicit Code-Length Objective for Modular Coefficient Rules

**Status:** completed computational study; interpretation remains task-specific.

## Research question

Does the base selected by EXP-004 remain favorable when the objective charges for more than coefficient-cycle count?

## Frozen coding scheme

Each rule describes the coefficient sequence for evaluating positional digits modulo an integer modulus. The serialized description is a two-part code with the following fields, in order:

1. An 8-bit fixed model identifier.
2. The numeral base (b), encoded with Elias gamma coding.
3. The modulus (m), encoded with Elias gamma coding.
4. The preperiod (mu+1), encoded with Elias gamma coding.
5. The period (lambda), encoded with Elias gamma coding.
6. Exactly (mu+lambda) coefficients, each in a fixed-width unsigned field of (w=\lceil\log_2 m\rceil) bits.

For positive integer (x), Elias gamma length is
[
L_\gamma(x)=2\lfloor\log_2 x\rfloor+1.
]

The total is
[
L=8+L_\gamma(b)+L_\gamma(m)+L_\gamma(\mu+1)
+L_\gamma(\lambda)+w(\mu+\lambda).
]

The 8-bit model identifier is a fixed overhead shared by every candidate. Base and modulus costs are both charged. The coefficient count need not be separately encoded because it is determined by the decoded preperiod and period. Each coefficient lies in ([0,m-1]), so the fixed-width field is sufficient. Unused bit patterns, if any, are simply invalid codewords.

This is a reproducible, task-specific two-part code. It is **not** a claim to have solved universal MDL: it does not search over all possible model families, code designs, decoders, or algorithmic programs. The model identifier is fixed overhead, not a learned model-selection penalty.

## Protocol

- Candidate bases: 2 through 36.
- Training moduli: 37, 41, 43, 47, 53, 59, 61, 67.
- Held-out moduli: 71, 73, 79, 83, 89, 97, 101, 103.
- Replication moduli: 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191.
- Select by mean total bits on training moduli; tie-break by maximum training code length, then lower base.
- Do not use held-out or replication data for selection.
- EXP-005's base 9 is evaluated unchanged on the independent replication set.
- Exact integer modular arithmetic only.

## What is and is not charged

Charged: model tag, base, modulus, preperiod metadata, period metadata, and all coefficient values.

Not charged: the source code implementing the decoder, the experiment runner, CSV/container overhead, file names, software runtime, and the cost of discovering the selected base. Those are separate engineering/search costs and must not be silently conflated with the encoded rule length.

## Outputs

- `research/results/EXP-006-mdl-base-search.csv`: all 35 bases across train and held-out moduli, with component-level bit accounting.
- `research/results/EXP-006-mdl-replication.csv`: locked base 9 and fixed baselines on the independent replication moduli.
- `research/experiments/EXP-006-results.md`: summary and limitations.

## Interpretation boundary

A shorter code under this frozen scheme means only that this particular coefficient-cycle rule is shorter under this particular serialization. It does not establish that the numeral system is generally simpler, faster, more human-readable, or mathematically superior. Runtime and search cost require separate measurements.
