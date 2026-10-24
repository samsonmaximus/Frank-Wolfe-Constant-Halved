import numpy as np, cvxpy as cp, sys
def solve(N, keep, ell=2.0):
    nb=1+N+(N+1)+1; e=lambda i: np.eye(nb)[i]
    X0=e(0); S=[e(1+j) for j in range(N)]; Gs=[e(1+N+i) for i in range(N+1)]; Gstar=e(2*N+2)
    xs=[X0]
    for k in range(N):
        h=ell/(k+ell); xs.append((1-h)*xs[-1]+h*S[k])
    z=np.zeros(nb); G=cp.Variable((nb,nb),PSD=True); f=cp.Variable(N+1); ip=lambda a,b:a@G@b
    pts=[(xs[i],Gs[i],f[i]) for i in range(N+1)]+[(z,Gstar,0)]
    cons=[]
    for i,(xi,gi,fi) in enumerate(pts):
        for j,(xj,gj,fj) in enumerate(pts):
            if i!=j: cons.append(fi>=fj+ip(gj,xi-xj)+0.5*ip(gi-gj,gi-gj))
    verts=[X0]+S+[z]
    # local base
    cons.append(ip(X0,X0)<=1); cons.append(ip(Gstar,X0)>=0)
    for k in range(N):
        cons+= [ip(Gs[k],S[k])<=ip(Gs[k],z), ip(Gs[k],S[k])<=ip(Gs[k],xs[k]), ip(Gstar,S[k])>=0,
                ip(S[k],S[k])<=1, ip(S[k]-xs[k],S[k]-xs[k])<=1]
    if "lmo" in keep:
        for k in range(N):
            for p in verts: cons.append(ip(Gs[k],S[k])<=ip(Gs[k],p))
    if "diam" in keep:
        for a in range(len(verts)):
            for b in range(a+1,len(verts)):
                d=verts[a]-verts[b]; cons.append(ip(d,d)<=1)
    if "opt" in keep:
        for p in verts: cons.append(ip(Gstar,p)>=0)
    p=cp.Problem(cp.Maximize(f[N]),cons); p.solve(solver="CLARABEL"); return p.value
N=int(sys.argv[1])
for keep in [(),("lmo",),("diam",),("opt",),("lmo","diam"),("lmo","opt"),("diam","opt"),("lmo","diam","opt")]:
    v=solve(N,keep); print(N,keep,f"{v:.6f}  (N+1)w={(N+1)*v:.4f}",flush=True)
