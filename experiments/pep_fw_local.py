"""Relaxed PEP: only 'local' constraints. Variants control which constraints are kept.
interp: smooth-convex interpolation among {x_0..x_N, x*} (all pairs) -- kept.
LMO_k vs {x*, x_k} only;  x* optimality vs {x_k, s_k};  diam: ||s_k-x*||,||x_k-x*||,||s_k-x_k|| <= 1."""
import numpy as np, cvxpy as cp, sys
def solve(N, ell=2.0, interp="all"):
    nb=1+N+(N+1)+1
    e=lambda i: np.eye(nb)[i]
    X0=e(0); S=[e(1+j) for j in range(N)]; Gs=[e(1+N+i) for i in range(N+1)]; Gstar=e(2*N+2)
    xs=[X0]
    for k in range(N):
        h=ell/(k+ell); xs.append((1-h)*xs[-1]+h*S[k])
    z=np.zeros(nb)
    G=cp.Variable((nb,nb),PSD=True); f=cp.Variable(N+1); ip=lambda a,b:a@G@b
    pts=[(xs[i],Gs[i],f[i]) for i in range(N+1)]+[(z,Gstar,0)]
    cons=[]
    idx=range(len(pts))
    for i in idx:
        for j in idx:
            if i==j: continue
            if interp=="consecutive" and not (abs(i-j)==1 or i==N+1 or j==N+1): continue
            xi,gi,fi=pts[i]; xj,gj,fj=pts[j]
            cons.append(fi>=fj+ip(gj,xi-xj)+0.5*ip(gi-gj,gi-gj))
    cons.append(ip(X0,X0)<=1)
    for k in range(N):
        cons+= [ip(Gs[k],S[k])<=ip(Gs[k],z), ip(Gs[k],S[k])<=ip(Gs[k],xs[k])]
        cons+= [ip(Gstar,S[k])>=0, ip(S[k],S[k])<=1, ip(S[k]-xs[k],S[k]-xs[k])<=1]
    cons.append(ip(Gstar,X0)>=0)
    p=cp.Problem(cp.Maximize(f[N]),cons); p.solve(solver="CLARABEL")
    return p.value
for N in [int(a) for a in sys.argv[1:]]:
    a=solve(N,interp="all"); b=solve(N,interp="consecutive")
    print(f"N={N} local-all-interp: {a:.6f} ((N+1)w={ (N+1)*a:.4f})   local-consecutive: {b:.6f} ((N+1)w={(N+1)*b:.4f})",flush=True)
