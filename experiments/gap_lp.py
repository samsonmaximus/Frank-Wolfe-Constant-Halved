"""Variance-relaxation LP for the Frank–Wolfe min duality gap (L=D=1, h_k = 2/(k+2)).
Valid inequalities (all from problems/frank-wolfe-constant/proof.md plus the definition of the FW gap
g_k = <grad f(x_k), x_k - s_k> >= e_k):
  e_{k+1} <= e_k - h_k g_k + (h_k^2/2) d_k            (descent lemma, exact LMO step)
  0 <= d_k <= W_k,  W_{k+1} = h_k + (1-h_k) W_k - h_k(1-h_k) d_k,  W_0 = 1   (variance bookkeeping)
  e_k >= 0, g_k >= e_k
Maximise t s.t. g_k >= t for k = 0..N  (=> upper bound on min_{0<=k<=N} g_k, any instance).
Report (N+2)*t."""
import numpy as np, sys
from scipy.optimize import linprog
def lp(N):
    # variables: e_0..e_N, g_0..g_N, d_0..d_{N-1}, t
    ne, ng, nd = N + 1, N + 1, N
    nv = ne + ng + nd + 1
    E = lambda k: k; Gi = lambda k: ne + k; D = lambda k: ne + ng + k; T = nv - 1
    A = []; bvec = []
    def row(): return np.zeros(nv)
    # W_k affine in d: W_k = c_k + sum_j a_kj d_j
    c = 1.0; a = np.zeros(nd); Wc = []; Wa = []
    for k in range(N):
        Wc.append(c); Wa.append(a.copy())
        h = 2 / (k + 2)
        c = h + (1 - h) * c; a = (1 - h) * a; a[k] -= h * (1 - h)
    for k in range(N):
        h = 2 / (k + 2)
        r = row(); r[E(k + 1)] = 1; r[E(k)] = -1; r[Gi(k)] = h; r[D(k)] = -h * h / 2; A.append(r); bvec.append(0)
        r = row(); r[D(k)] = 1; r[D(0):D(0) + nd] -= Wa[k]; A.append(r); bvec.append(Wc[k])   # d_k <= W_k
    for k in range(N + 1):
        r = row(); r[E(k)] = 1; r[Gi(k)] = -1; A.append(r); bvec.append(0)        # e_k <= g_k
        r = row(); r[T] = 1; r[Gi(k)] = -1; A.append(r); bvec.append(0)           # t <= g_k
    obj = np.zeros(nv); obj[T] = -1
    bounds = [(0, None)] * (ne + ng + nd) + [(None, None)]
    res = linprog(obj, A_ub=np.array(A), b_ub=np.array(bvec), bounds=bounds, method="highs")
    return -res.fun
for N in [int(a) for a in sys.argv[1:]]:
    t = lp(N); print(f"N={N:5d}  LP bound on min gap = {t:.6f}  (N+2)*t = {(N+2)*t:.5f}   [PEP ~1.665, Jaggi 6.75]", flush=True)
