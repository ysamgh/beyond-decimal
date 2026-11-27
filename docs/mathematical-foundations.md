# Mathematical Foundations

## Values and numerals
A numeral is not the number itself. It is a finite symbolic representation interpreted under a rule system.

For an integer written in base b with digits a_k through a_0:

N = sum(i=0..k) a_i * b^i

Here b is an integer at least 2 and each digit satisfies 0 <= a_i < b. The same integer has different numeral strings in different bases. The value is invariant; the digit sequence is not.

## Example: 13 and the numeral 10
In base 13, numeral 10 denotes 1*13 + 0 = 13. Since 13 is prime, that numeral denotes a prime value in base 13. In base 10, numeral 10 denotes ten, which is composite.

Primality does not change with the base. The same character string denotes different values under different interpretation rules.

## Prime numbers
For an integer n > 1, primality means that n has exactly two positive divisors, 1 and n. A base conversion preserves n, so it preserves primality. Digit patterns may help notice candidate structure, but they do not redefine primality.

## Mersenne numbers
M_n = 2^n - 1, for n >= 1. Its values begin 1, 3, 7, 15, 31, 63, 127, ... . In binary, 2^n - 1 is represented by n consecutive ones. This follows from 1 + 2 + ... + 2^(n-1) = 2^n - 1.

Not every Mersenne number is prime: 63 = 7 * 9. The value 1 is neither prime nor composite.

## Irrational constants and base expansions
A real number has a base-b expansion. The digits depend on b, while the represented real value does not. An irrational number has a non-terminating, non-periodic expansion in every integer base b >= 2.

A finite prefix cannot establish randomness, normality, or absence of deeper structure. Digit statistics require appropriate null models.

## Invariance and representation dependence
Classify every feature as value-invariant, invariant under a declared transformation, representation-dependent, or task-dependent. Examples of representation-dependent features include digit sum, digit length, and runs of repeated digits.
