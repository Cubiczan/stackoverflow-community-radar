# Elementary-proof sketch: Ramanujan’s CF for ζ(3, x+1)

**Target:** [MO 462327](https://mathoverflow.net/questions/462327)  
**Notebook:** Berndt, *Ramanujan’s Notebooks* Part II, Ch. 12, Entry **32(iii)**, eq. (32.4)  
**Local parse:** `data/parsed/part-2/full.md` (~pp. 164–167)  
**Status:** Sketch toward an elementary route; Berndt’s Γ/ψ proof remains the standard complete argument. This note motivates an Apéry-style integer path + analytic continuation, avoiding unexplained Gamma ratios as the *starting* point.

---

## Statement (corrected form)

For \(\operatorname{Re} x > -\tfrac12\),

\[
\zeta(3,x+1)=\sum_{k=1}^{\infty}\frac{1}{(x+k)^3}
=\cfrac{1}{P(0,x)-\cfrac{1^6}{P(1,x)-\cfrac{2^6}{P(2,x)-\cfrac{3^6}{P(3,x)-\cdots}}}}
\tag{R}
\]

where

\[
P(n,x)=n^3+(n+1)^3+(4n+2)\,x(x+1).
\]

Equivalently (MO’s \(v=2x(x+1)\) form),

\[
P(n,x)=(2n+1)\bigl(v+n^2+n+1\bigr)=n^3+(n+1)^3+(2n+1)v.
\]

Berndt also records a companion CF with numerators \(1^3,1^3,2^3,2^3,\ldots\) (first line of (32.4)); the sixth-power form is obtained from it by the standard even/odd contraction (his Entry 14). Ramanujan’s notebook copy of the second CF is slightly wrong (Berndt, p. 149); use \(P(n,x)\) as above.

At \(x=1\), (R) is the continued fraction underlying Apéry’s irrationality proof of \(\zeta(3)\).

---

## Strategy (elementary spine)

Goal: prove (R) for positive integers \(x=i\in\mathbb{N}\) by finite combinatorial identities (Apéry / interpolation), then extend to \(\operatorname{Re} x>-1/2\) by a growth + uniqueness argument (Carlson). No Gamma ratios appear until (optionally) one wants Berndt’s closed-form identification with \(\psi''\).

### Step 0 — Why a cubic CF is natural

The remainder after \(N\) terms,

\[
R_N(x)=\sum_{k=N+1}^{\infty}(x+k)^{-3},
\]

satisfies a rough asymptotic \(R_N\sim\tfrac12 N^{-2}\). Apéry-type accelerations replace the remainder by a ratio of polynomial recurrences of order 2 in a discrete parameter, which *contracts* to a continued fraction whose partial denominators are cubic in the index — exactly the shape of \(P(n,x)\). So the target form is forced by degree counting, not pulled from a hat.

### Step 1 — Integer specialisation via Apéry interpolation

Following Rajkumar (arXiv:1212.5881), construct a family of continued fractions for \(\zeta(3)\) by interpolating finite truncations. In that framework one obtains sequences \((p_{i,j}),(q_{i,j})\) such that, for each positive integer \(i\),

\[
\frac{p_{i,1}}{q_{i,1}}
\]

matches the first convergent pattern of (R) at \(x=i\), and inductively the full CF identity

\[
\zeta(3,i+1)=\cfrac{1}{P(0,i)-\cfrac{1^6}{P(1,i)-\cfrac{2^6}{P(2,i)-\cdots}}}
\tag{R\(_i\)}
\]

holds. Concretely (Rajkumar, around (22)):

- \(q_{i,0}=1\), \(p_{i,0}=\sum_{n\le i}n^{-3}\);
- \(q_{i,1}=P(0,i)\), \(p_{i,1}=P(0,i)\,p_{i,0}+1\);

and the same recurrence that generates Apéry’s \((a_n),(b_n)\) produces the higher convergents of (R\(_i\)).

**Motivation:** for integer \(x=i\), \(\zeta(3,i+1)=\zeta(3)-\sum_{k=1}^{i}k^{-3}\) is a finite correction of \(\zeta(3)\); Apéry’s CF machinery already encodes \(\zeta(3)\), so the correction must be absorbed into the *first* partial denominators — which is exactly what replacing the constant \(P(n,0)\) by \(P(n,i)\) does.

### Step 2 — Equivalence of the two CF shapes

Berndt’s first CF in (32.4) (cube numerators, alternating \(1\) and linear-in-\(x(x+1)\) denominators) is related to (R) by the classical contraction of a 2-periodic continued fraction (Entry 14 / Euler–Minding). Sketch:

1. Write the cube-numerator CF as an equivalent “even part” by combining two steps.
2. Clear the resulting rational factors; numerators become sixth powers \(n^6\), denominators become \(P(n,x)\).

This step is purely formal CF algebra (no analysis, no special functions).

### Step 3 — Analytic continuation / uniqueness

Both sides of (R) are meromorphic (in fact holomorphic for \(\operatorname{Re} x>-1/2\) after removing the obvious poles of individual summands at negative integers). They agree on the positive integers \(\{1,2,3,\ldots\}\) by Step 1.

If one controls the growth of the continued-fraction side in vertical strips (partial quotients \(\sim 4n^3\), convergents grow at most like a double exponential of controlled order), Carlson’s theorem supplies uniqueness and yields (R) on \(\operatorname{Re} x>-1/2\).

*(Berndt’s route instead identifies the CF with \(-\tfrac12\psi''(x+1)\) by a Gamma-ratio limit from Entry 35; that is shorter once Entry 35 is granted, but Entry 35 is the “rabbit.” The Apéry path explains why the CF exists before naming \(\psi\).)*

### Step 4 — Sanity checks

| Specialisation | Result |
|----------------|--------|
| \(x=1\) | Apéry CF for \(\zeta(3)\) |
| \(x=0\) | Euler-type CF for \(\zeta(3)\) (separate classical derivation) |
| Large \(n\) asymptotics of \(P(n,x)\) | \(\sim 2n^3\), consistent with \(\zeta(3,x+1)\sim\int^\infty t^{-3}\,dt\) |

Numerical: truncate (R) at \(N=20\) for \(x=\tfrac12\); compare to direct summation of \(\zeta(3,\tfrac32)\).

---

## What this sketch does *not* claim

- A fully expanded elementary write-up of Rajkumar’s interpolation lemmas (those still need to be checked line-by-line).
- An elementary substitute for Entry 35 itself.
- A proof for non-integer \(x\) that avoids *some* complex-analytic input (Carlson or an equivalent Phragmén–Lindelöf bound).

For MO 462327, the honest answer is: **yes, there is a conceptually elementary spine** (Apéry interpolation at integers → contraction → Carlson), documented in Rajkumar arXiv:1212.5881 and linked by Zudilin’s surveys; Berndt’s Γ-proof remains the cleanest complete reference once Entry 35 is accepted.

---

## References

1. B. C. Berndt, *Ramanujan’s Notebooks, Part II*, Springer, Entry 32(iii).
2. K. Rajkumar, *A simplification of Apéry’s proof of the irrationality of ζ(3)*, arXiv:1212.5881.
3. W. Zudilin, notes on Ramanujan and odd zeta values (survey linking (R) to Apéry).
4. R. Apéry, *Irrationalité de ζ(2) et ζ(3)*, Astérisque 61 (1979).
5. MO 462327; MSE discussion of the \(x=1\) CF.

## KG links

- `formula:berndt-part2-ch12-entry32iii`
- `mo:462327`
- Proof artifact: this file
