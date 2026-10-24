"""Exact rational check of the FW-gap corollary for EVERY N in 1..400 (prefix sums; all K0 tried):
min_{K0<=k<=N} g_k <= [e_{K0} + sum_{k=K0}^N 2/(k+2)^2] / sum_{k=K0}^N 2/(k+2) <= 3/(N+1)."""
from fractions import Fraction as F
NMAX = 400
H = [F(0)] * (NMAX + 2)
for j in range(1, NMAX + 2): H[j] = H[j - 1] + F(1, j)
eb = [None] + [(k + H[k - 1] / 3) / (k * (k + 1)) for k in range(1, NMAX + 1)]
S1 = [F(0)] * (NMAX + 2); S2 = [F(0)] * (NMAX + 2)          # prefix sums over k=0..i-1
for k in range(NMAX + 1):
    S1[k + 1] = S1[k] + F(2, k + 2); S2[k + 1] = S2[k] + F(2, (k + 2) ** 2)
worst = F(0); worstN = None
for N in range(1, NMAX + 1):
    best = min((eb[K0] + S2[N + 1] - S2[K0]) / (S1[N + 1] - S1[K0]) for K0 in range(1, N + 1))
    r = best * (N + 1)
    assert r < 3, (N, float(r))
    if r > worst: worst, worstN = r, N
print(f"ALL N in 1..{NMAX}: (N+1)*bound < 3.  max = {float(worst):.6f} at N = {worstN}")
