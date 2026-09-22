#!/usr/bin/env python3
"""Fail-closed numeric assertion for the Part II p. 255 derivation check.

`data/kg/proof_sketches/part2_p255_corollary_from_entry1.md` states the
derivation of (1.3) from (1.1) is "verified numerically". The underlying
script, `scripts/verify_part2_p255.py`, only prints its comparisons; this
wrapper imports the same functions and refuses (exit 1) unless every printed
invariant holds within tolerance:

- S_cesaro - S_paired == 1            (predicted exactly 1;   observed ~1e-12)
- A + B == 1/(2 pi z) + pi z/6 - C    (identity of (1.3);      observed ~4e-13)
- piece1 == -(1/2) S - A              (decomposition identity; observed ~1e-16)
- piece2 == 1/(2 pi z)                ((C,1)-truncated;        observed ~5e-7)
- pi z/6 + piece1 + piece2 == B       ((C,1)-truncated;        observed ~5e-7)

Two tolerance tiers: 1e-9 for exact identities, 1e-5 for comparisons affected
by the (C,1) averaging truncation (observed <= 5e-7 on the committed
derivation — a real mathematical error would show O(1) deviation). Double
precision and stdlib-only, matching the derivation check; runs offline.
"""
from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
TOL_EXACT = 1e-9
TOL_CESARO = 1e-5
Z_VALUES = (0.7, 1.0, 1.3)


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "verify_part2_p255", SCRIPTS_DIR / "verify_part2_p255.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load verify_part2_p255.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    mod = _load_module()
    failures: list[str] = []

    c = mod.constant_C()
    s_paired = 2 * c - 1
    s_cesaro = mod.cesaro(lambda m: (-1) ** (m + 1) * (2 * m + 1) / mod.nu(m))

    gap = s_cesaro - s_paired
    if not math.isclose(gap, 1.0, abs_tol=TOL_EXACT, rel_tol=0.0):
        failures.append(f"S_cesaro - S_paired = {gap:.12f}, expected 1")

    for z in Z_VALUES:
        a, b = mod.sum_A(z), mod.sum_B(z)
        piece1 = mod.cesaro(
            lambda m, z=z: (-1) ** m
            * (2 * m + 1)
            / math.tanh(math.pi * z * mod.nu(m))
            / (2 * mod.nu(m))
        )
        s2 = 0.0
        for m in range(1, 500_000):
            s2 += (-1) ** m * (2 * m + 1) / (mod.nu(m) ** 2)
        piece2 = -s2 / (2 * math.pi * z)

        lhs = a + b
        rhs = 1 / (2 * math.pi * z) + math.pi * z / 6 - c
        if not math.isclose(lhs, rhs, abs_tol=TOL_EXACT, rel_tol=0.0):
            failures.append(f"z={z}: A+B ({lhs:.12f}) != RHS ({rhs:.12f})")

        half_s_minus_a = -s_cesaro / 2 - a
        if not math.isclose(piece1, half_s_minus_a, abs_tol=TOL_EXACT, rel_tol=0.0):
            failures.append(
                f"z={z}: piece1 ({piece1:.12f}) != -(1/2)S - A ({half_s_minus_a:.12f})"
            )

        expected_piece2 = 1 / (2 * math.pi * z)
        if not math.isclose(piece2, expected_piece2, abs_tol=TOL_CESARO, rel_tol=0.0):
            failures.append(
                f"z={z}: piece2 ({piece2:.12f}) != 1/(2 pi z) ({expected_piece2:.12f})"
            )

        recon = math.pi * z / 6 + piece1 + piece2
        if not math.isclose(recon, b, abs_tol=TOL_CESARO, rel_tol=0.0):
            failures.append(f"z={z}: reconstruction ({recon:.12f}) != B ({b:.12f})")

    if failures:
        print("FAIL: p.255 derivation numeric invariants violated:")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print(
        "p.255 derivation verified numerically: S_cesaro - S_paired = 1 and the "
        f"(1.3) identity holds for z in {Z_VALUES} within tolerance"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
