"""Tight PEP for vanilla Frank-Wolfe, h_k = l/(k+l), f convex L-smooth on R^d, C compact convex, diam D.
Normalize L=D=1, x*=0. Vertices of C: x0, s_0..s_{N-1}, x*. Iterates x_{k+1}=(1-h_k)x_k+h_k s_k.
Variables: Gram G of basis [x0, s_0..s_{N-1}, g_0..g_N, g*], function values f_0..f_N (f*=0)."""
import numpy as np, cvxpy as cp, sys
def solve(N, ell=2.0, solver="CLARABEL", verbose=False):
    nb = 1 + N + (N+1) + 1
    def e(i): v=np.zeros(nb); v[i]=1; return v
    X0=e(0); S=[e(1+j) for j in range(N)]; Gs=[e(1+N+i) for i in range(N+1)]; Gstar=e(1+N+N+1)
    xs=[X0]
    for k in range(N):
        h=ell/(k+ell); xs.append((1-h)*xs[-1]+h*S[k])
    xstar=np.zeros(nb)
    G=cp.Variable((nb,nb),PSD=True); f=cp.Variable(N+1)
    ip=lambda a,b: a@G@b
    pts=[(xs[i],Gs[i],f[i]) for i in range(N+1)]+[(xstar,Gstar,0)]
    cons=[]
    for i,(xi,gi,fi) in enumerate(pts):
        for j,(xj,gj,fj) in enumerate(pts):
            if i!=j: cons.append(fi>=fj+ip(gj,xi-xj)+0.5*ip(gi-gj,gi-gj))
    verts=[X0]+S+[xstar]
    for k in range(N):
        for p in verts: cons.append(ip(Gs[k],S[k])<=ip(Gs[k],p))
    for p in verts: cons.append(ip(Gstar,p-xstar)>=0)
    for a in range(len(verts)):
        for b in range(a+1,len(verts)):
            d=verts[a]-verts[b]; cons.append(ip(d,d)<=1)
    prob=cp.Problem(cp.Maximize(f[N]),cons)
    prob.solve(solver=solver,verbose=verbose)
    return prob.value, G.value, f.value, prob, cons
if __name__=="__main__":
    for N in [int(a) for a in sys.argv[1:]]:
        w,*_=solve(N)
        print(f"N={N:3d}  w_N={w:.8f}  N*w_N={N*w:.6f}  (N+2)*w_N={(N+2)*w:.6f}  Jaggi 2/(N+2)={2/(N+2):.6f}",flush=True)
