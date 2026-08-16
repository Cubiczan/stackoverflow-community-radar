# MathOverflow draft 1 — Part II p. 255 derivation gap

**Status: POSTED 2026-08-16.**

Live: https://mathoverflow.net/questions/514344/can-ramanujans-corollary-to-entry-1-chapter-14-be-deduced-from-the-entry-by-p

Posted by Shyam Desigan. MathOverflow's automated quality check passed with no suggested improvements.

Tags: `nt.number-theory` `special-functions` `sequences-and-series` `ramanujan` `divergent-series`

---

## Title

Can Ramanujan's Corollary to Entry 1 (Chapter 14) be deduced from the entry itself by partial fractions?

## Body

In Berndt's *Ramanujan's Notebooks*, Part II, Chapter 14, Entry 1 states that for
$z^2 \neq -n(n+1)/2$,

$$z^{-2}\prod_{n=1}^{\infty}\left(1+\frac{2z^2}{n(n+1)}\right)^{-1}=\sum_{n=0}^{\infty}\frac{(-1)^n(2n+1)}{z^2+n(n+1)/2}.\tag{1.1}$$

The Corollary states that for $\operatorname{Re} z>0$,

$$\sum_{n=1}^{\infty}\frac{(-1)^{n+1}(2n+1)}{\sqrt{n(n+1)}\left(e^{2\pi z\sqrt{n(n+1)}}-1\right)}+\frac1z\sum_{n=1}^{\infty}\operatorname{sech}\left(\frac{\pi}{z}\sqrt{n^2-\tfrac{z^2}{4}}\right)=\frac{1}{2\pi z}+\frac{\pi z}{6}-C,\tag{1.3}$$

where

$$C=\frac12+\frac12\sideset{}{^*}\sum_{n=1}^{\infty}\frac{(-1)^{n+1}(2n+1)}{\sqrt{n(n+1)}},\tag{1.4}$$

the asterisk indicating that terms are added in successive pairs (the terms tend
to $2$, so the series does not otherwise converge).

After stating the Corollary, Ramanujan remarks:

> "Similarly any function whose denominator is in the form of a product can be
> expressed as the sum of partial fractions and many other theorems may be
> deduced from the result."

Berndt writes (p. 255): **"But nonetheless, we have been unable to prove that
(1.3) is a corollary of (1.1)."** He gives instead a proof of (1.3) due to
R. J. Evans, by a different route.

**My question is about recovering Ramanujan's claimed deduction.**

Write $\nu_n=\sqrt{n(n+1)}$, $\mu_n=n(n+1)/2$. Inside his proof of (1.1) Berndt
establishes the equivalent form

$$2\pi\operatorname{sech}\!\left(\pi\sqrt{2t^2-\tfrac14}\right)=\sum_{m\ge0}\frac{(-1)^m(2m+1)}{t^2+\mu_m}.\tag{$*$}$$

The observation that seems to be the point of Ramanujan's remark is that the
$\operatorname{sech}$ in (1.3) **is** the function in ($*$):

$$\frac{\pi}{z}\sqrt{n^2-\tfrac{z^2}{4}}=\pi\sqrt{2t^2-\tfrac14}\qquad\text{with }t=\frac{n}{z\sqrt2}.$$

So each $\operatorname{sech}$ term expands by (1.1) itself, giving

$$B:=\frac1z\sum_{n\ge1}\operatorname{sech}(\cdots)=\frac{z}{\pi}\sum_{n\ge1}\sum_{m\ge0}\frac{(-1)^m(2m+1)}{n^2+z^2m(m+1)}.$$

The $m=0$ term gives $\frac{z}{\pi}\cdot\frac{\pi^2}{6}=\frac{\pi z}{6}$. For
$m\ge1$, summing over $n$ by
$\sum_{n\ge1}(n^2+a^2)^{-1}=\frac{\pi\coth(\pi a)}{2a}-\frac{1}{2a^2}$ with
$a=z\nu_m$ splits $B$ into

$$\underbrace{\sum_{m\ge1}\frac{(-1)^m(2m+1)\coth(\pi z\nu_m)}{2\nu_m}}_{P_1}\;+\;\underbrace{-\frac{1}{2\pi z}\sum_{m\ge1}\frac{(-1)^m(2m+1)}{m(m+1)}}_{P_2}.$$

$P_2$ is elementary: $\frac{2m+1}{m(m+1)}=\frac1m+\frac1{m+1}$ gives
$\sum_{m\ge1}(-1)^m(\frac1m+\frac1{m+1})=-1$, so $P_2=\frac{1}{2\pi z}$.
Splitting $\coth x=1+\frac{2}{e^{2x}-1}$ turns $P_1$ into $-\tfrac12 S-A$, where
$A$ is the first sum in (1.3) and

$$S=\sum_{m\ge1}\frac{(-1)^{m+1}(2m+1)}{\nu_m}.$$

Collecting gives exactly (1.3) **provided** $-\tfrac12S=-C$, i.e. $S=2C$.

**Here is the subtlety.** $S$ diverges (terms $\to2$). Under the paired summation
of (1.4), $S_{\text{paired}}=2C-1$. Under Abel or Cesàro summation,
$S=2C$. The two differ by exactly $1$ — and it is precisely that $\tfrac12$ which
makes the deduction appear to fail. Numerically (double precision, $z=0.7,1.0,1.3$):

- $S_{\text{Cesàro}}-S_{\text{paired}}=1.000000000001$
- $S_{\text{Cesàro}}-2C=8\times10^{-13}$
- $\frac{\pi z}{6}+P_1+P_2=B$ to $3\times10^{-7}$
- $P_1=-\tfrac12S-A$ to $10^{-15}$

**Questions.**

1. Can the interchange of $\sum_n$ and $\sum_m$ be justified? The double series is
   not absolutely convergent, and summing $m$ by naive truncation rather than
   Cesàro averaging shifts the value by exactly $\tfrac12$, so the order genuinely
   matters.
2. Is there a clean convergence-factor argument — insert $r^m$, work at $r<1$
   where all rearrangements are legitimate, let $r\to1^-$ — that makes both steps
   rigorous and yields $S=2C$ as the correct regularisation?
3. Is this the route Ramanujan intended, and is it what Berndt considered and set
   aside? I would be glad to be told this is already in the literature.

I am not claiming a proof: steps 1 and 2 above are exactly what is missing.
