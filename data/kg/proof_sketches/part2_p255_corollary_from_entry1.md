# Deriving (1.3) from (1.1) — Part II, p. 255

**Status: derivation verified numerically; two analytic steps still need rigorous
justification. This is not yet a proof.**

## The open remark

Berndt, *Ramanujan's Notebooks* Part II, p. 255. After the Corollary to Entry 1,
Ramanujan writes:

> "Similarly any function whose denominator is in the form of a product can be
> expressed as the sum of partial fractions and many other theorems may be
> deduced from the result."

Berndt: *"But nonetheless, we have been unable to prove that (1.3) is a corollary
of (1.1)."* He instead gives a proof of (1.3) due to R. J. Evans, by a different
route.

So (1.3) is **true and proved**. What is unresolved is Ramanujan's claimed
*deduction* of it from (1.1) by partial fractions.

## Notation

    mu_n = n(n+1)/2        nu_n = sqrt(n(n+1))     so  nu_n^2 = 2 mu_n

Entry 1 (1.1), for z^2 != -n(n+1)/2:

    z^-2 prod_{n>=1} (1 + z^2/mu_n)^-1  =  sum_{n>=0} (-1)^n (2n+1)/(z^2 + mu_n)

Inside his proof of (1.1) Berndt establishes the equivalent form

    2 pi sech(pi sqrt(2t^2 - 1/4))  =  sum_{m>=0} (-1)^m (2m+1)/(t^2 + mu_m)   (*)

Corollary (1.3), for Re z > 0, with

    A := sum_{n>=1} (-1)^{n+1}(2n+1) / ( nu_n (e^{2 pi z nu_n} - 1) )
    B := (1/z) sum_{n>=1} sech( (pi/z) sqrt(n^2 - z^2/4) )

    A + B = 1/(2 pi z) + pi z/6 - C                                          (1.3)

    C = 1/2 + (1/2) sum*_{n>=1} (-1)^{n+1}(2n+1)/nu_n                        (1.4)

where `sum*` means terms added in successive pairs (the series does not converge
otherwise, since (2n+1)/nu_n -> 2).

## The derivation

**Step 1 — the sech in (1.3) is the sech in (*).**

    (pi/z) sqrt(n^2 - z^2/4) = pi sqrt(n^2/z^2 - 1/4) = pi sqrt(2t^2 - 1/4)
    with t = n/(z sqrt 2).

This is the step Ramanujan's remark points at: B is built from the very function
whose partial-fraction expansion (1.1) supplies.

**Step 2 — expand each sech by (*) and sum over n.**

    B = (z/pi) sum_{n>=1} sum_{m>=0} (-1)^m (2m+1) / (n^2 + z^2 m(m+1))

The `m = 0` term is (z/pi) * sum_n 1/n^2 = (z/pi)(pi^2/6) = **pi z/6**.

**Step 3 — inner sum in closed form.** For a = z nu_m,

    sum_{n>=1} 1/(n^2 + a^2) = pi coth(pi a)/(2a) - 1/(2a^2)

giving two pieces:

    piece1 = sum_{m>=1} (-1)^m (2m+1) coth(pi z nu_m) / (2 nu_m)
    piece2 = -(1/(2 pi z)) sum_{m>=1} (-1)^m (2m+1)/(m(m+1))

**Step 4 — piece2 is elementary.** Since (2m+1)/(m(m+1)) = 1/m + 1/(m+1),

    sum_{m>=1} (-1)^m (1/m + 1/(m+1)) = -ln2 + (ln2 - 1) = -1

so piece2 = **1/(2 pi z)**.

**Step 5 — split coth.** With coth(x) = 1 + 2/(e^{2x} - 1),

    piece1 = -(1/2) S - A,     S := sum_{m>=1} (-1)^{m+1}(2m+1)/nu_m

**Step 6 — the regularisation, and the whole difficulty.** S does not converge:
its terms tend to 2. It must be read in the Abel/Cesaro sense, and

    S_Abel = S_paired + 1      (verified numerically: difference = 1 to 6 digits)

Since (1.4) gives S_paired = 2C - 1, we get **S_Abel = 2C**, hence
-(1/2) S = -C.

**Collecting:**

    B = pi z/6 + piece1 + piece2 = pi z/6 - C - A + 1/(2 pi z)

    ==>  A + B = 1/(2 pi z) + pi z/6 - C          which is (1.3).   []

## Numerical verification

`scripts/verify_part2_p255.py`, at z = 0.7, 1.0, 1.3:

- (1.3) itself holds to ~1.6e-12 (residual is truncation in the paired sum for C).
- piece1 = -(1/2)S - A to 1e-15.
- piece2 = 1/(2 pi z) to 3e-7.
- pi z/6 + piece1 + piece2 = B to 3e-7.
- S_Abel - S_paired = 0.999994 -> 1.
- S_Cesaro = 1.0932389960 = 2C exactly.

## What is still missing

Two steps are formal, and closing them is the actual remaining work:

1. **Step 2 interchanges** sum_n and sum_m in a double series that is not
   absolutely convergent. Summing m naively (truncating at fixed M rather than
   Cesaro-averaging) shifts the answer by exactly 1/2 -- so the interchange is
   genuinely order-sensitive and cannot be waved through.
2. **Step 6 regularises** a divergent series. The natural fix is to insert r^m,
   do everything for r < 1 where all rearrangements are legitimate, then let
   r -> 1^-; this requires showing the limit exists and matches the direct sums.

Both are plausibly provable by the convergence-factor route. Until they are, this
is a verified derivation *route*, not a proof -- and the fact that both delicate
points contribute exactly 1/2 is likely why the deduction was set aside.
