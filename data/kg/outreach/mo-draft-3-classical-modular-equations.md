# MathOverflow draft 3 — the method-gap cluster (6 sites, one question)

**Status: draft. Not yet posted.**

Deliberately ONE question, not six. All six are the same request — a proof by
means available to Ramanujan of a modular equation Berndt could only reach via
modular forms. Six near-identical posts would read as spam and close as
duplicates of each other.

Tags: `nt.number-theory` `modular-forms` `theta-functions` `special-functions` `ho.history-overview`

---

## Title

Classical proofs of the modular equations Berndt could only prove via modular forms?

## Body

Throughout *Ramanujan's Notebooks*, Berndt repeatedly proves a modular equation
using the theory of modular forms while noting that he could not find a proof by
means available to Ramanujan, and flagging this as unsatisfactory. The clearest
statement is Part V, p. 71:

> "Unfortunately, we have been unable to prove them by methods familiar to
> Ramanujan and so have resorted to the theory of modular forms for our proofs.
> **It would be of considerable interest if more instructive proofs could be
> found.**"

Systematically mining the commentary across all five volumes turns up exactly six
such sites:

| Volume | Page | Result | Berndt's wording |
|---|---|---|---|
| III | 491 | Entry 8(i), 8(iii) | "unable to prove either (i) or (iii) using (2.3) or (5.3)" — deferred to Section 11, modular forms |
| IV | 102 | Entry 39 | "unable to prove Entry 39 by using **classical methods**" |
| IV | 124 | Entries 68–72 | "unable to prove the remaining five $P$–$Q$ eta-function identities by employing the classical theory of theta-functions ... **in the spirit of Ramanujan**" |
| V | 71 | Theorems 7.9, 7.10 | "unable to prove them by methods familiar to Ramanujan" |
| V | 184 | modular equations from Notebook 1, pp. 86, 88 (Schläfli-type) | "regrettable that we are unable to prove some of Ramanujan's modular equations by methods familiar to Ramanujan" |
| V | 199 | Entries 43–52 | "unable to prove Entries 43–52 by employing **ideas known to Ramanujan**" |

Two representative statements. Part IV, Entry 39 (p. 330 of the notebook): with

$$u=\frac{f(-q)f(-q^5)}{q^{1/2}f(-q^3)f(-q^{15})},\qquad v=\frac{f(-q^{1/3})f(-q^{5/3})}{q^{2/3}f(-q^3)f(-q^{15})},$$

then $u^4-3u^2v=v^3+3v^2+9v$.

Part V, Theorem 7.9 (p. 259): if $\alpha,\beta,\gamma,\delta$ have degrees
1, 2, 4, 8 and $m_1,m_2$ are the multipliers associated with the pairs
$(\alpha,\beta)$, $(\gamma,\delta)$, then

$$\frac{1-(\alpha\delta)^{1/3}-\{(1-\alpha)(1-\delta)\}^{1/3}}{3\{\beta\gamma(1-\beta)(1-\gamma)\}^{1/6}}=\frac{m_2}{m_1}.$$

**Questions.**

1. Have any of these six been given a classical proof since the notebooks were
   edited — by theta-function manipulation, Schläfli/Weber/Russell-type methods,
   or the parametrisations Ramanujan himself used elsewhere?
2. Is there a structural reason to expect some of them *cannot* be reached
   classically, or is this purely a matter of nobody having found the right
   parametrisation?

A remark on scope. Berndt's criterion is specifically "methods available to
Ramanujan". Proofs from adjacent fields — Baxter's corner transfer matrix method,
which produced new proofs of the Rogers–Ramanujan identities, or Bethe-ansatz and
CFT-character arguments — would certainly be of interest, but I recognise they
are arguably as anachronistic as the modular-forms proofs Berndt is trying to
avoid, so they would not close the gap as he poses it.

A separate curiosity from the same discussion (Part V, p. 184): Ramanujan records
a modular equation of **degree 49** on p. 298 of the first notebook, and Berndt
writes that apparently no one else had found one of that degree, adding "even at
this writing, we know of no other modular equation of degree 49." Is that still
the case?

References: B. C. Berndt, *Ramanujan's Notebooks*, Parts III, IV, V, Springer.
