# EXP-003 — Initial Results

## Dataset

The deterministic sweep contains 350 rows: 10 predeclared prime moduli multiplied by 35 bases (2–36).

## Exact findings

For a prime modulus m:

- If base b is divisible by m, the coefficient sequence is 1, 0, 0, ...; its preperiod is 1 and period is 1.
- If b is not divisible by m, the sequence is purely periodic; its period is the multiplicative order of b modulo m.
- Therefore, the coefficient count for coprime base/modulus pairs is the multiplicative order of b modulo m.

The minimum coefficient count in the declared search range is one for every tested modulus. This occurs whenever b ≡ 1 (mod m), because every coefficient b^k mod m is then 1. The first such base in the range is m + 1 for each tested prime modulus.

This is an expected algebraic control, not a novel mathematical discovery. It confirms that the search and scoring procedure can recover a known simple representation for the specified modular task.

## Decimal baseline

Base 10 is included for every modulus. Its coefficient counts are:

| Modulus | Decimal coefficient count | Decimal is minimal? |
|---:|---:|:---:|
| 3 | 1 | Yes |
| 5 | 2 | No |
| 7 | 6 | No |
| 11 | 2 | No |
| 13 | 6 | No |
| 17 | 16 | No |
| 19 | 18 | No |
| 23 | 22 | No |
| 29 | 28 | No |
| 31 | 15 | No |

For example, modulo 3, 10 ≡ 1 (mod 3), so every coefficient is 1 and the residue rule reduces to the digit sum modulo 3. Modulo 7, the powers of 10 cycle with period 6, so six coefficients are needed for the direct positional coefficient cycle.

## What this does and does not show

The experiment demonstrates that representation choice can change the compactness of an exact rule for a specified task. The preferred base depends on the modulus and task. It does not show that a single base is best for all tasks, nor that a shorter coefficient cycle always means faster human or machine computation.

The score is a transparent structural proxy, not a full Minimum Description Length (MDL) code. It does not charge for encoding the modulus, base, operators, or the rule "repeat this cycle". The result should therefore be described as coefficient-cycle compactness, not total description length.

The experiment is intentionally a baseline/control. Because the search includes bases congruent to 1 modulo each modulus, the trivial one-coefficient solution is guaranteed in this parameter range. A harder follow-up should compare constrained base families or task sets where this shortcut is not available.

## Independent correctness check

The implementation includes a little-endian digit evaluator that uses the detected coefficient cycle. Tests compare its result against direct integer remainder for values 0–99 and bases 2–12, and test invalid digits and parameters.

## Next validation

- Expand beyond prime moduli only after the prime-modulus baseline is stable.
- Add runtime measurements separately from the symbolic coefficient-count metric.
- Design a second task where the trivial congruence b ≡ 1 (mod m) shortcut is excluded by a predeclared admissible-base constraint.
