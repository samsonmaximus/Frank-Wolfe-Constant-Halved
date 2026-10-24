"""Variance-recursion bound (L=D=1). State (e_k, V_k) affine in d. Maximize e_N s.t. 0<=d_k<=1-V_k.
Build e_N = c.d, V_k = A_k.d explicitly (no recursion depth issues)."""
import numpy as np, scipy.optimize as so, sys
def lp(N, ell=2.0):
    ce=np.zeros(N); cV=np.zeros(N); A=[]; 
    for k in range(N):
        h=ell/(k+ell)
        A.append(cV.copy())                    # V_k as function of d
        ce=(1-h)*ce; ce[k]+=h*h/2
        cV=(1-h)*cV; cV[k]+=h*(1-h)
    # constraints d_k + V_k(d) <= 1
    Aub=np.array([A[k]+np.eye(N)[k] for k in range(N)]); bub=np.ones(N)
    r=so.linprog(-ce,A_ub=Aub,b_ub=bub,bounds=[(0,None)]*N,method="highs")
    return -r.fun, r.x
if __name__=="__main__":
    for N in [10,40,100,300,1000,3000]:
        v,d=lp(N)
        act=np.isclose(d+0,0)
        print(f"N={N:5d} (N+1)LP={(N+1)*v:.6f}  N*LP={N*v:.6f}  first d: {np.round(d[:6],4)}  #zero d={act.sum()}",flush=True)
