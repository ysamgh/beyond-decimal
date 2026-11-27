# EXP-003 — Initial Results

## Dataset

The deterministic sweep contains 350 rows: 10 predeclared prime moduli multiplied by 35 bases (2–36).

## Exact findings

For a prime modulus m:

- If base b is divisible by m, the coefficient sequence is 1, 0, 0, ...; its preperiod is 1 and period is 1.
- If b is not divisible by m, the sequence is purely periodic; its period is the multiplicative order of b modulo m.
- Therefore, the coefficient count for coprime base/modulus pairs is the multiplicative order of b modulo m.

This gives a direct mathematical interpretation to the primary metric. The best bases are not universal: the minimum depends on the selected modulus and on the specified modular-residue task.

## Decimal baseline

Base 10 is included for every modulus. For example, modulo 3, 10 ≡ 1 (mod 3), so every coefficient is 1 and the residue rule reduces to the digit sum modulo 3. Modulo 7, the powers of 10 cycle with period 6, so six coefficients are needed for the direct positional coefficient cycle.

## What this does and does not show

The experiment demonstrates that representation choice can change the compactness of an exact rule for a specified task. It does not show that a single base is best for all tasks, nor that a shorter coefficient cycle always means faster human or machine computation.

The score is a transparent structural proxy, not a full Minimum Description Length (MDL) code. It does not charge for encoding the modulus, base, operators, or the rule "repeat this cycle". The result should therefore be described as coefficient-cycle compactness, not total description length.

## Next validation

- Add independent property tests comparing the cycle-based residue computation with Python's integer remainder.
- Expand beyond prime moduli only after the prime-modulus baseline is stable.
- Add runtime measurements separately from the symbolic coefficient-count metric.
