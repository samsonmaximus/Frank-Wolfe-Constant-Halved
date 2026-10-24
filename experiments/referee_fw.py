"""Independent referee test of the FW bound  e_N <= L D^2 (N + H_{N-1}/3)/(N(N+1)).
Written from scratch; does not import anything from experiments/.
"""
import numpy as np
from fractions import Fraction as Fr
from scipy.optimize import minimize

rng = np.random.default_rng(12345)

def H(m):
    return sum(1.0 / j for j in range(1, m + 1))

def bound(N):
    return (N + H(N - 1) / 3.0) / (N * (N + 1))

# ---------- exact rational re-check of Step 4/5 algebra ----------
def exact_check(Nmax=300):
    for N in range(2, Nmax + 1):
        h = lambda k: Fr(2, k + 2)
        al = {N: Fr(0)}
        for k in range(N - 1, 0, -1):
            al[k] = Fr(2 * (k + 1), k + 2) + al[k + 1] * Fr(k, k + 2) ** 2
        for k in range(1, N + 1):
            assert al[k] >= 0
            if k >= 2:
                assert al[k] <= k + 1
        for k in range(1, N):
            ck = Fr(2 * (k + 1), k + 2) - al[k + 1] * h(k) * (1 - h(k))
            assert ck > 0
            assert ck + al[k + 1] * (1 - h(k)) == al[k]
        B = 1 + al[1] + sum(al[k + 1] * h(k) for k in range(1, N))
        target = N + sum(Fr(1, j) for j in range(1, N)) / 3
        assert B == target, (N, B, target)
        # Wbar closed form
        W = Fr(1)
        for k in range(1, N):
            assert W == Fr((k + 2) * (3 * k + 1), 6 * k * (k + 1))
            W = h(k) + (1 - h(k)) ** 2 * W
    return True

# ---------- Frank-Wolfe ----------
def fw_poly(A, b, V, x0, N, adversarial_ties=True, tol=1e-12):
    """V: (m,d) vertices. Ties in LMO broken toward the farthest vertex."""
    x = x0.copy()
    for k in range(N):
        g = A @ x - b
        vals = V @ g
        mn = vals.min()
        cand = np.where(vals <= mn + tol * (1 + abs(mn)))[0]
        if adversarial_ties and len(cand) > 1:
            dists = ((V[cand] - x) ** 2).sum(1)
            j = cand[np.argmax(dists)]
        else:
            j = cand[0]
        h = 2.0 / (k + 2)
        x = x + h * (V[j] - x)
    return x

def f(A, b, x):
    return 0.5 * x @ A @ x - b @ x

def fstar_poly(A, b, V):
    m = V.shape[0]
    obj = lambda lam: f(A, b, V.T @ lam)
    grad = lambda lam: V @ (A @ (V.T @ lam) - b)
    best = None
    for _ in range(3):
        l0 = rng.dirichlet(np.ones(m))
        r = minimize(obj, l0, jac=grad, method='SLSQP',
                     bounds=[(0, 1)] * m,
                     constraints=[{'type': 'eq', 'fun': lambda l: l.sum() - 1, 'jac': lambda l: np.ones(m)}],
                     options={'ftol': 1e-15, 'maxiter': 2000})
        lam = np.clip(r.x, 0, None); lam /= lam.sum()
        xh = V.T @ lam
        if best is None or f(A, b, xh) < f(A, b, best):
            best = xh
    # conservative LOWER bound on f*: f(xh) + min_v <grad, v - xh>  (convexity)
    g = A @ best - b
    lb = f(A, b, best) + (V @ g - g @ best).min()
    return lb, f(A, b, best)

def diam(V):
    d2 = ((V[:, None, :] - V[None, :, :]) ** 2).sum(-1)
    return np.sqrt(d2.max())

def rand_psd(d, kind):
    if kind == 'rank1':
        u = rng.normal(size=d); A = np.outer(u, u)
    elif kind == 'diag':
        A = np.diag(rng.uniform(0, 1, d))
    else:
        M = rng.normal(size=(d, d)); A = M @ M.T
    return A / np.linalg.norm(A, 2)

def ratio_poly(A, b, V, x0, N):
    L = np.linalg.norm(A, 2); D = diam(V)
    lb, _ = fstar_poly(A, b, V)
    xN = fw_poly(A, b, V, x0, N)
    return (f(A, b, xN) - lb) / (L * D * D)

# ---------- ball ----------
def fw_ball(A, b, c, r, x0, N):
    x = x0.copy()
    for k in range(N):
        g = A @ x - b
        ng = np.linalg.norm(g)
        if ng < 1e-14:
            # every point is an LMO solution: adversarially jump far away
            u = rng.normal(size=len(x)); u /= np.linalg.norm(u)
            s = c + r * u
        else:
            s = c - r * g / ng
        x = x + 2.0 / (k + 2) * (s - x)
    return x

def fstar_ball(A, b, c, r):
    d = len(c)
    cons = [{'type': 'ineq', 'fun': lambda x: r * r - ((x - c) ** 2).sum(), 'jac': lambda x: -2 * (x - c)}]
    rr = minimize(lambda x: f(A, b, x), c, jac=lambda x: A @ x - b, method='SLSQP', constraints=cons,
                  options={'ftol': 1e-15, 'maxiter': 2000})
    xh = rr.x
    if ((xh - c) ** 2).sum() > r * r:
        xh = c + r * (xh - c) / np.linalg.norm(xh - c)
    g = A @ xh - b
    lb = f(A, b, xh) + (g @ c - r * np.linalg.norm(g) - g @ xh)
    return lb

Ns = [1, 2, 3, 4, 5, 7, 10, 15, 20, 40]

def random_tests(trials=4000):
    worst = {N: 0.0 for N in Ns}
    viol = 0
    for t in range(trials):
        d = int(rng.integers(1, 6))
        m = int(rng.integers(2, 8)) if d > 1 else 2
        V = rng.normal(size=(m, d)) if rng.random() < 0.7 else rng.uniform(-1, 1, (m, d))
        A = rand_psd(d, rng.choice(['rank1', 'diag', 'full']))
        # b so that unconstrained optimum A^+ b is near/inside/outside C
        target = V.mean(0) + rng.normal(size=d) * rng.choice([0.0, 0.3, 1.0, 3.0])
        b = A @ target
        if rng.random() < 0.5:
            x0 = V[rng.integers(m)]
        else:
            x0 = V.T @ rng.dirichlet(np.ones(m))
        for N in Ns:
            rt = ratio_poly(A, b, V, x0, N)
            worst[N] = max(worst[N], rt)
            if rt > bound(N) + 1e-9:
                viol += 1
                print('VIOLATION poly', N, rt, bound(N))
    return worst, viol

def ball_tests(trials=1500):
    worst = {N: 0.0 for N in Ns}; viol = 0
    for t in range(trials):
        d = int(rng.integers(2, 5)); r = 0.5; c = np.zeros(d)
        A = rand_psd(d, rng.choice(['rank1', 'diag', 'full']))
        b = A @ (rng.normal(size=d) * rng.choice([0.0, 0.2, 0.5, 2.0]))
        u = rng.normal(size=d); u /= np.linalg.norm(u)
        x0 = c + r * u * rng.uniform(0, 1)
        lb = fstar_ball(A, b, c, r)
        for N in Ns:
            xN = fw_ball(A, b, c, r, x0, N)
            rt = (f(A, b, xN) - lb) / 1.0  # L=1, D=2r=1
            worst[N] = max(worst[N], rt)
            if rt > bound(N) + 1e-9:
                viol += 1; print('VIOLATION ball', N, rt, bound(N))
    return worst, viol

def tie_tests():
    """f = 1/2 x^2 on [-1/2,1/2], x0 = 0 = x*: gradient zero -> adversarial tie gives s=+-1/2."""
    out = {}
    V = np.array([[-0.5], [0.5]]); A = np.eye(1); b = np.zeros(1)
    for N in Ns:
        xN = fw_poly(A, b, V, np.zeros(1), N)
        out[N] = f(A, b, xN) - 0.0
        assert out[N] <= bound(N) + 1e-12
    return out

def adversarial_search(N, iters=1500, restarts=6):
    """Hill-climb over 2-D instances (triangle/quad, PSD A, b, x0 weights) to maximise ratio."""
    best_all = 0.0
    for rs in range(restarts):
        d = 2; m = 3 + rs % 3
        P = rng.normal(size=m * d + 3 + d + m)
        def unpack(P):
            V = P[:m * d].reshape(m, d)
            a11, a12, a22 = P[m * d:m * d + 3]
            M = np.array([[a11, a12], [0, a22]]); A = M @ M.T + 1e-12 * np.eye(2)
            A /= np.linalg.norm(A, 2)
            tgt = P[m * d + 3:m * d + 3 + d]
            w = np.exp(P[m * d + 3 + d:]); w /= w.sum()
            return V, A, A @ tgt, V.T @ w
        def score(P):
            V, A, b, x0 = unpack(P)
            if diam(V) < 1e-6: return 0.0
            return ratio_poly(A, b, V, x0, N)
        cur = score(P); step = 0.5
        for it in range(iters):
            Q = P + step * rng.normal(size=P.shape)
            s = score(Q)
            if s > cur:
                P, cur = Q, s
            elif it % 200 == 199:
                step *= 0.6
        best_all = max(best_all, cur)
    return best_all

def oned_worst(N, grid=401):
    """1-D: C=[0,1], f=1/2(x-a)^2 (L=1,D=1), x0 in {0,1}, a on grid; exact f*."""
    best = 0.0
    for a in np.linspace(-1, 2, grid):
        for x0 in (0.0, 1.0):
            x = x0
            for k in range(N):
                g = x - a
                s = 0.0 if g > 0 else (1.0 if g < 0 else (1.0 if x < 0.5 else 0.0))
                x += 2.0 / (k + 2) * (s - x)
            xs = min(max(a, 0), 1)
            best = max(best, 0.5 * (x - a) ** 2 - 0.5 * (xs - a) ** 2)
    return best

if __name__ == '__main__':
    print('exact rational check N<=300:', exact_check(300))
    pep = {2: 0.31261699, 3: 0.22784810, 5: 0.14621246, 10: 0.07828955, 20: 0.04132259, 40: 0.02156374}
    print('PEP comparison:')
    for N, w in pep.items():
        print(f'  N={N:3d} bound={bound(N):.8f} pep={w:.8f} margin={bound(N)-w:.6f} classical={2/(N+2):.6f}')
        assert bound(N) > w
    print('tie test:', {k: round(v, 6) for k, v in tie_tests().items()})
    print('1-D worst (grid):', {N: round(oned_worst(N), 6) for N in [1, 2, 3, 5, 10, 20]})
    w, v = random_tests(); print('random polytopes worst:', {k: round(x, 6) for k, x in w.items()}, 'violations', v)
    w, v = ball_tests(); print('balls worst:', {k: round(x, 6) for k, x in w.items()}, 'violations', v)
    for N in [1, 2, 3, 5, 10]:
        s = adversarial_search(N)
        print(f'adversarial 2-D N={N}: {s:.6f}  bound {bound(N):.6f}  pep {pep.get(N, float("nan"))}')
