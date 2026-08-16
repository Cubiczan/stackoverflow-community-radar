# MathOverflow draft 2 — Part II p. 341, Entry 12(x)

**Status: draft. Not yet posted.**

Tags: `nt.number-theory` `analytic-number-theory` `divisor-sums` `elementary-proofs` `modular-forms`

---

## Title

Elementary proof of Ramanujan's convolution identity for $\sigma_1$ and $\sigma_3$?

## Body

Berndt, *Ramanujan's Notebooks* Part II, p. 341, records that Entry 12(x) is
equivalent to the identity

$$\sum_{k=0}^{n}\sigma_1(2k+1)\,\sigma_3(n-k)=\frac{1}{240}\,\sigma_5(2n+1),\qquad n\ge0,$$

where $\sigma_3(0)=\tfrac1{240}$.

The history is unusual. Ramanujan stated Entry 12(x) in [11] (Collected Papers,
p. 146) **without proof**, and indicated that he had *two* proofs, one of which
was elementary and the other using elliptic functions — but he gave no hint of
either. The proofs now in the literature are:

- D. Masser's proof;
- a proof via modular forms on $\Gamma_0(2)$ constructed by A. O. L. Atkin;
- a proof in V. Ramamani's thesis using the theory of elliptic functions.

Berndt remarks that it is very unlikely that Masser's or Atkin's proof is either
of Ramanujan's, and writes:

> "It would be interesting to have an elementary proof of this identity and hence
> of Entry 12(x) as well."

**Question.** Is an elementary proof known — elementary in the sense of avoiding
modular forms and elliptic function theory, i.e. by manipulation of divisor sums,
lattice point counting, or a combinatorial/bijective argument?

The identity has the flavour of the classical convolution identities

$$\sum_{k=0}^{n}\sigma_1(k)\sigma_1(n-k)=\tfrac5{12}\sigma_3(n)-\tfrac1{12}(6n-1)\sigma_1(n),$$

several of which do admit elementary proofs, so it is not obvious that this one
must be transcendental in nature. The restriction to odd arguments $\sigma_1(2k+1)$
and $\sigma_5(2n+1)$ is what makes it look like a $\Gamma_0(2)$ statement, and is
presumably why Atkin's proof takes that route.

Secondary: identities of this convolution type also arise in statistical
mechanics and conformal field theory — Baxter's corner transfer matrix method
famously produced new proofs of the Rogers-Ramanujan identities. I would be
interested if this identity has such an interpretation, though I recognise that
would not be "elementary" in Ramanujan's sense either.

References: B. C. Berndt, *Ramanujan's Notebooks, Part II*, Springer, Ch. 14/15;
Ramanujan, *Collected Papers*, p. 146.
