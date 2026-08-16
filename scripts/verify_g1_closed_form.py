from mpmath import mp, mpf, log, pi, zeta, polylog, nsum, inf, harmonic

mp.dps = 50
L = log(2)

# G(1) = 7pi^4/1152 - A/2 with A = sum (-1)^{n-1} H_n/n^3
A = (11*pi**4)/360 - 2*polylog(4, mpf(1)/2) - mpf(7)/4*zeta(3)*L + pi**2/12*L**2 - L**4/12
G_exact = 7*pi**4/1152 - A/2

# fully expanded form
G_expanded = (-53*pi**4/5760 + polylog(4, mpf(1)/2) + mpf(7)/8*zeta(3)*L
              - pi**2/24*L**2 + L**4/24)

print("G(1) = 7pi^4/1152 - A/2 =", G_exact)
print("G(1) expanded            =", G_expanded)
print("agreement                =", G_exact - G_expanded)
print()
# independent check: brute force with Euler-Maclaurin tail correction
def brute(N=2000000):
    s = mpf(0); h = mpf(0)
    for k in range(1, N+1):
        h += mpf(1)/(2*k-1)
        s += h/(2*k)**3
    # tail: h_k ~ (log(4k)+euler)/2 ; sum_{k>N} (log(4k)+g)/(16 k^3)
    from mpmath import euler as g
    tail = (log(4*N)+g)/(32*mpf(N)**2) + (1)/(64*mpf(N)**2)
    return s, s + tail
b, bc = brute()
print("brute partial (2e6)      =", b)
print("brute + tail estimate    =", bc)
print("vs closed form           =", G_exact, "  diff =", bc - G_exact)
