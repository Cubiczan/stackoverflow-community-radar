"""Numerically verify the derivation of (1.3) from (1.1), Part II p. 255.

See data/kg/proof_sketches/part2_p255_corollary_from_entry1.md.

Double precision throughout: we only need to distinguish 0 from 1/2, and the
Abel/Cesaro sums converge far too slowly for high-precision arithmetic to be
worth it. Alternating series whose terms tend to a nonzero constant are summed
by (C,1) averaging of partial sums.
"""

from __future__ import annotations

import math

PI = math.pi


def nu(n: float) -> float:
    return math.sqrt(n * (n + 1.0))


def cesaro(term, n_terms: int = 200_000, window: int = 400) -> float:
    """(C,1) average of the last `window` partial sums."""
    total = 0.0
    tail: list[float] = []
    for m in range(1, n_terms + 1):
        total += term(m)
        if m > n_terms - window:
            tail.append(total)
    return sum(tail) / len(tail)


def sum_A(z: float, n_terms: int = 200_000) -> float:
    s = 0.0
    for n in range(1, n_terms + 1):
        v = nu(n)
        e = math.exp(2 * PI * z * v)
        if math.isinf(e):
            break
        t = (-1) ** (n + 1) * (2 * n + 1) / (v * (e - 1))
        s += t
        if abs(t) < 1e-18:
            break
    return s


def sum_B(z: float, n_terms: int = 200_000) -> float:
    s = 0.0
    for n in range(1, n_terms + 1):
        t = 1.0 / math.cosh((PI / z) * math.sqrt(n * n - z * z / 4))
        s += t
        if t < 1e-18:
            break
    return s / z


def constant_C(n_terms: int = 400_000) -> float:
    """C per (1.4): terms added in successive pairs."""
    s = 0.0
    for k in range(1, n_terms + 1, 2):
        s += (2 * k + 1) / nu(k) - (2 * (k + 1) + 1) / nu(k + 1)
    return 0.5 + s / 2


def main() -> None:
    C = constant_C()
    S_paired = 2 * C - 1
    S_cesaro = cesaro(lambda m: (-1) ** (m + 1) * (2 * m + 1) / nu(m))

    print(f"C  (paired, per 1.4)   = {C:.12f}   [Berndt: 0.54661949...]")
    print(f"S_paired = 2C - 1      = {S_paired:.12f}")
    print(f"S_cesaro               = {S_cesaro:.12f}")
    print(f"S_cesaro - S_paired    = {S_cesaro - S_paired:.12f}   [predicted exactly 1]")
    print(f"S_cesaro - 2C          = {S_cesaro - 2 * C:.3e}   [predicted 0]")
    print()

    s2 = 0.0
    for m in range(1, 500_000):
        s2 += (-1) ** m * (2 * m + 1) / (nu(m) ** 2)

    for z in (0.7, 1.0, 1.3):
        A, B = sum_A(z), sum_B(z)
        piece1 = cesaro(
            lambda m: (-1) ** m * (2 * m + 1) / math.tanh(PI * z * nu(m)) / (2 * nu(m))
        )
        piece2 = -s2 / (2 * PI * z)
        lhs = A + B
        rhs = 1 / (2 * PI * z) + PI * z / 6 - C

        print(f"z = {z}")
        print(f"  (1.3):  A+B = {lhs:.12f}   RHS = {rhs:.12f}   diff = {lhs - rhs:.3e}")
        print(f"  piece1 = {piece1:.12f}   -(1/2)S - A = {-S_cesaro / 2 - A:.12f}"
              f"   diff = {piece1 - (-S_cesaro / 2 - A):.3e}")
        print(f"  piece2 = {piece2:.12f}   1/(2 pi z)  = {1 / (2 * PI * z):.12f}"
              f"   diff = {piece2 - 1 / (2 * PI * z):.3e}")
        recon = PI * z / 6 + piece1 + piece2
        print(f"  pi z/6 + piece1 + piece2 = {recon:.12f}   B = {B:.12f}"
              f"   diff = {recon - B:.3e}")
        print()


if __name__ == "__main__":
    main()
