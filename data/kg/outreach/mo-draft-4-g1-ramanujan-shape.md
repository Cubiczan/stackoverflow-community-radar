# MathOverflow draft 4 — Part I p. 267, a formula for G(1) of Ramanujan's shape

**Status: draft. Not yet posted.**

Tags: `nt.number-theory` `special-functions` `sequences-and-series` `polylogarithms` `euler-sums`

---

## Title

A formula for $\sum_{k\ge1} h_k/(2k)^3$ resembling Ramanujan's (incorrect) one?

## Body

In Berndt's *Ramanujan's Notebooks* Part I, Chapter 9, Entry 11 defines, for
$-1\le x\le 1$,

$$F(x)=\sum_{k=1}^{\infty}\frac{h_k x^{2k}}{(2k)^2},\qquad G(x)=\sum_{k=1}^{\infty}\frac{h_k x^{2k}}{(2k)^3},$$

where $h_k=1+\tfrac13+\cdots+\tfrac1{2k-1}=H_{2k}-\tfrac12 H_k$ is the odd
harmonic number. The constant $G(1)$ appears as the constant of integration in
Entry 11(ii).

Ramanujan claims (p. 267 of Berndt's edition) that

$$G(1)=\frac{\pi}{4}\sum_{k=0}^{\infty}\frac{(-1)^k}{(4k+1)^3}-\frac{\pi}{3\sqrt3}\sum_{k=0}^{\infty}\frac{1}{(2k+1)^3}.\tag{11.3}$$

**This is false.** Berndt notes $G(1)>0.1529320988\dots$ while the right side of
(11.3) is less than $0.1442780636\dots$. He then writes:

> "We have been unable to find any formula for $G(1)$ which resembles (11.3).
> R. Sitaramachandrarao (personal communication) has derived several expressions
> for $G(1)$ that are related to the Riemann zeta-function and similar types of
> series. Unfortunately, none of Sitaramachandrarao's formulas echoes (11.3)."

**What is easy.** $G(1)$ is a linear Euler sum of weight 4 and does have a closed
form in the standard basis. Writing $A=\sum_{n\ge1}(-1)^{n-1}H_n/n^3$, one has
$G(1)=\tfrac{7\pi^4}{1152}-\tfrac{A}{2}$, hence

$$G(1)=-\frac{53\pi^4}{5760}+\operatorname{Li}_4\!\left(\tfrac12\right)+\frac78\zeta(3)\log 2-\frac{\pi^2}{24}\log^2 2+\frac{1}{24}\log^4 2$$

$$=0.16227193947148339071535955180807120647\dots$$

(verified to 20 digits against a direct summation with Euler–Maclaurin tail).
This is presumably one of Sitaramachandrarao's expressions, and it is exactly the
kind Berndt says does *not* answer the question: it is a polylogarithmic formula,
not one of Ramanujan's shape.

**Question.** Ramanujan's (11.3) has a very specific form: $\pi$ times an
alternating cubic character sum, minus $\pi/(3\sqrt3)$ times $\sum(2k+1)^{-3}=\tfrac78\zeta(3)$.
Is there a *correct* formula for $G(1)$ of that shape — $\pi$ times $L$-values at
3, with a $\sqrt3$ present — and if so, what did Ramanujan get wrong?

The $\pi/(3\sqrt3)$ coefficient is suggestive: $\sqrt3$ points at a character mod
3 or mod 6, whereas the $(4k+1)^{-3}$ sum is mod 4. A formula mixing conductors 3
and 4 is unusual enough that it is hard to believe Ramanujan wrote it down by
accident, which makes me suspect a recoverable near-miss — a wrong constant or a
dropped factor, as happens elsewhere in the notebooks (Berndt identifies exactly
such a slip on p. 255, a neglected factor of $2\sqrt{n(n+1)}$).

Has anyone reverse-engineered what (11.3) was meant to be?

References: B. C. Berndt, *Ramanujan's Notebooks, Part I*, Springer, Ch. 9,
Entry 11 and the commentary on p. 267.
