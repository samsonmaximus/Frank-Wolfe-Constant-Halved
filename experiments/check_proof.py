"""Exact (Fraction) checks of the potential argument for many N:
 alpha_N=0, alpha_k = 2(k+1)/(k+2) + alpha_{k+1} (k/(k+2))^2  (k=N-1..1)
 need alpha_{k+1} <= (k+1)(k+2)/k for k=1..N-1 (d-coefficient >= 0), and alpha_k <= k+1.
 bound: E_N <= E_1 + alpha_1 W_1 + sum_{k=1}^{N-1} alpha_{k+1} h_k  with E_1<=1, W_1=1; compare to N + H_{N-1}/3."""
from fractions import Fraction as Fr
import random
def check(N):
    a=[Fr(0)]*(N+1)
    for k in range(N-1,0,-1): a[k]=Fr(2*(k+1),k+2)+a[k+1]*Fr(k,k+2)**2
    cond=all(a[k+1]<=Fr((k+1)*(k+2),k) for k in range(1,N))
    cond2=all(a[k]<=k+1 for k in range(2,N+1))
    bound=1+a[1]+sum(a[k+1]*Fr(2,k+2) for k in range(1,N))
    H=sum(Fr(1,j) for j in range(1,N))
    return cond,cond2,bound==N+H/3
bad=[N for N in list(range(1,200))+[500,1000] if not all(check(N))]
print("all exact checks pass" if not bad else f"FAIL at {bad}")
# Monte-Carlo: random feasible (d_k in [0,W_k]) paths never exceed bound
import math
for trial in range(20000):
    N=random.randint(1,60); W=1.0; e=0.5*random.random()  # e_1 <= 1/2
    W=1.0
    for k in range(1,N):
        h=2/(k+2); d=W*random.random()**random.choice([0.2,1,5])
        e=(1-h)*e+h*h*d/2; W=h+(1-h)*W-h*(1-h)*d
    H=sum(1/j for j in range(1,N))
    assert e <= (N+H/3)/(N*(N+1))+1e-12, (N,e)
print("random paths OK")
