# A halved constant for vanilla Frank–Wolfe

Status: **full proof; independent referee: CORRECT (referee_report.md); prior-art check pending.**

## Setting
‖·‖ is the Euclidean norm (needed for the variance identity). f convex, L-smooth on C (‖∇f(x)−∇f(y)‖ ≤ L‖x−y‖
for x,y ∈ C); C ⊂ R^d compact convex, diameter D; x_0 ∈ C; exact linear minimization oracle; f* = min_C f at x*.
Frank–Wolfe: s_k ∈ argmin_{s∈C} ⟨∇f(x_k), s⟩, x_{k+1} = x_k + h_k (s_k − x_k), h_k = 2/(k+2).
Write e_k = f(x_k) − f*, H_m = Σ_{j=1}^m 1/j (H_0 = 0).

## Theorem
For every N ≥ 1,

  f(x_N) − f* ≤ L D² · (N + H_{N−1}/3) / (N (N+1)).

In particular f(x_N) − f* ≤ (L D²/(N+1))·(1 + H_{N−1}/(3N)) ≤ (4/3)·L D²/(N+1), and
limsup_N N·(f(x_N) − f*)/(LD²) ≤ 1, half the classical constant 2 from 2LD²/(N+2) (Jaggi 2013).
Among step rules h_k = ℓ/(k+ℓ), the same argument's asymptotic constant is minimized at ℓ = 2 (numerical LP).

## Proof
By scaling (f ↦ f/(LD²), x ↦ x/D) assume L = D = 1.

**Step 1 (descent).** By L-smoothness, optimality of s_k for the linear oracle, and convexity,
  f(x_{k+1}) ≤ f(x_k) + h_k⟨∇f(x_k), s_k − x_k⟩ + (h_k²/2)δ_k,   δ_k := ‖s_k − x_k‖²,
  ⟨∇f(x_k), s_k − x_k⟩ ≤ ⟨∇f(x_k), x* − x_k⟩ ≤ f* − f(x_k).
Hence  e_{k+1} ≤ (1 − h_k) e_k + (h_k²/2) δ_k.                                     (1)

**Step 2 (variance bookkeeping).** Define probability measures μ_0 = δ_{x_0},
μ_{k+1} = (1−h_k) μ_k + h_k δ_{s_k}. By induction μ_k is supported in C and has mean x_k.
Let V_k = E_{Y∼μ_k} ‖Y − x_k‖². For any point s, E‖s − Y‖² = ‖s − x_k‖² + V_k, so with s = s_k ∈ C and
supp μ_k ⊂ C (all distances ≤ D = 1):
  δ_k = E‖s_k − Y‖² − V_k ≤ 1 − V_k.                                                (2)
The variance of the mixture μ_{k+1} (mean x_{k+1}, with x_{k+1} − x_k = h_k(s_k − x_k) and
s_k − x_{k+1} = (1−h_k)(s_k − x_k)) is
  V_{k+1} = (1−h_k)[V_k + h_k² δ_k] + h_k (1−h_k)² δ_k = (1−h_k) V_k + h_k(1−h_k) δ_k.     (3)
Put W_k := 1 − V_k. Then (2),(3) read
  0 ≤ δ_k ≤ W_k,   W_{k+1} = h_k + (1−h_k) W_k − h_k(1−h_k) δ_k.                 (4)

**Step 3 (first step).** h_0 = 1, so x_1 = s_0, e_1 ≤ δ_0/2 ≤ 1/2 by (1),(2) (V_0 = 0), and μ_1 = δ_{s_0}, so W_1 = 1.

**Step 4 (potential).** Let E_k = k(k+1) e_k. For k ≥ 1, multiplying (1) by (k+1)(k+2) and using
(k+1)(k+2)(1−h_k) = k(k+1), (k+1)(k+2) h_k²/2 = 2(k+1)/(k+2):
  E_{k+1} ≤ E_k + (2(k+1)/(k+2)) δ_k.                                               (5)
Fix N ≥ 2 and define α_N = 0 and, for k = N−1, …, 1,
  α_k = 2(k+1)/(k+2) + α_{k+1} (k/(k+2))².                                          (6)
*Lemma.* α_k ≤ k+1 for 2 ≤ k ≤ N. (Backward induction: α_N = 0; if α_{k+1} ≤ k+2 then
α_k ≤ 2 + k²/(k+2) ≤ k+1 ⇔ 2k+4 ≤ 3k+2 ⇔ k ≥ 2.)
Let Φ_k = E_k + α_k W_k. Using (5),(4),
  Φ_{k+1} ≤ E_k + c_k δ_k + α_{k+1}(h_k + (1−h_k) W_k),  c_k := 2(k+1)/(k+2) − α_{k+1} h_k(1−h_k).
Since h_k(1−h_k) = 2k/(k+2)² and α_{k+1} ≤ k+2 (Lemma; also trivially for k+1 = N),
c_k ≥ 2(k+1)/(k+2) − 2k/(k+2) > 0, so by δ_k ≤ W_k,
  Φ_{k+1} ≤ E_k + α_{k+1} h_k + W_k [c_k + α_{k+1}(1−h_k)] = Φ_k + α_{k+1} h_k,
because c_k + α_{k+1}(1−h_k) = 2(k+1)/(k+2) + α_{k+1}(1−h_k)² = α_k by (6). Summing, with
Φ_1 = E_1 + α_1 W_1 ≤ 1 + α_1 (Step 3) and Φ_N = E_N (α_N = 0):
  E_N ≤ B_N := 1 + α_1 + Σ_{k=1}^{N−1} α_{k+1} h_k.                                   (7)

**Step 5 (evaluating B_N).** Consider the numbers Ē_1 = 1, W̄_1 = 1, δ̄_k = W̄_k,
W̄_{k+1} = h_k + (1−h_k)² W̄_k, Ē_{k+1} = Ē_k + (2(k+1)/(k+2)) W̄_k. For these, every inequality in
Step 4 is an equality, so Ē_N = B_N. By induction W̄_k = (k+2)(3k+1)/(6k(k+1)):
indeed 2/(k+2) + (k/(k+2))²·(k+2)(3k+1)/(6k(k+1)) = (3k²+13k+12)/(6(k+1)(k+2)) = (k+3)(3k+4)/(6(k+1)(k+2)).
Hence the increment is (2(k+1)/(k+2)) W̄_k = (3k+1)/(3k) = 1 + 1/(3k), and
  B_N = Ē_N = 1 + Σ_{k=1}^{N−1} (1 + 1/(3k)) = N + H_{N−1}/3.
With (7), e_N = E_N/(N(N+1)) ≤ (N + H_{N−1}/3)/(N(N+1)). (N = 1 is Step 3.) ∎

## Remarks
- Exact rational checks of (6), the Lemma, c_k > 0 and B_N = N + H_{N−1}/3 for N ≤ 199, 500, 1000:
  `experiments/check_proof.py`; 20k random feasible paths never exceed the bound.
- Not tight: the exact PEP worst case (`experiments/pep_fw.py`, Clarabel) gives (N+2)·w_N ≈ 0.905 at N = 20–40,
  so the true asymptotic constant c* = lim N·w_N appears to be ≈ 0.9–0.95 < 1. Our bound is the exact value of
  the "variance relaxation" (LP in `experiments/variance_lp.py`), which keeps only (1)–(4).
- Ablation (`experiments/pep_fw_ablate.py`): the improvement over 2LD²/N comes entirely from the pairwise
  diameter constraints among {x_0, s_0, s_1, …}; LMO cross-constraints and x*-optimality are ~irrelevant.
  The variance argument is exactly a way of using those pairwise constraints.

## Follow-up (2026-10-20): the variance bound is optimal for the descent-lemma approach
`experiments/geo_relax.py`: keep only the per-step descent inequality (1) and ALL pairwise distance
constraints ‖p_a − p_b‖ ≤ D among {x_0, s_0, …, s_{N−1}} (an SDP over their Gram matrix). Its value equals
(N + H_{N−1}/3)/(N(N+1)) to solver precision for N = 2, 3, 5, 10, 20, 40. Hence no further use of the geometry
of C can beat our theorem; any improvement toward the PEP value (≈ 0.9/N) must exploit the smooth-convex
interpolation coupling between iterations (the descent lemma (1) is where the remaining slack lives).

## Corollary (2026-10-21): the Frank–Wolfe duality gap
Let g_k := max_{s∈C} ⟨∇f(x_k), x_k − s⟩ = ⟨∇f(x_k), x_k − s_k⟩ (the FW gap). For every N ≥ 1,

  min_{0≤k≤N} g_k ≤ 3 L D² / (N+1).

For comparison, Jaggi 2013, Thm 2 gives 6.75 LD²/(N+2).

**Proof.** (L = D = 1.) The descent lemma gives h_k g_k ≤ e_k − e_{k+1} + h_k² ‖s_k−x_k‖²/2 ≤ e_k − e_{k+1} + h_k²/2.
Summing over K0 ≤ k ≤ N and using e_{N+1} ≥ 0:
  (min_{K0≤k≤N} g_k) · Σ_{k=K0}^N h_k ≤ e_{K0} + ½ Σ_{k=K0}^N h_k².
Bound e_{K0} by the Theorem: e_{K0} ≤ (K0 + H_{K0−1}/3)/(K0(K0+1)).
- N ≤ 400: optimise K0 in exact rational arithmetic (`experiments/gap_corollary.py`). The worst value of (N+1)·bound is 2.8984 < 3.
- N > 400: take m = K0 = ⌈N/2⌉ ≥ 200.
  - ½Σ h_k² = Σ 2/(k+2)² ≤ 2/(m+1) − 2/(N+2).
  - e_m ≤ (1/(m+1))(1 + (1+ln m)/(3m)) ≤ 1.0105/(m+1).
  - 1/(m+1) ≤ 2/(N+2).
  So the numerator is ≤ (4 + 0.021)/(N+2).
  - Σ h_k ≥ 2 ln((N+3)/(m+2)) ≥ 2 ln(2·403/405) ≥ 1.37639.
  Hence min g_k ≤ 2.9214/(N+2) < 3/(N+1). ∎

The asymptotic constant of this argument is min_θ (3/θ − 2)/(2 ln(1/θ)) ≈ 2.885 (θ ≈ 0.52).

The full variance relaxation, an LP that also uses δ_k ≤ D² − V_k inside the sum (`experiments/gap_lp.py`), gives (N+2)·min g ≈ 2.16
at N = 3000, still decreasing. The classical relaxation (δ_k ≤ D²) gives ≈ 4.30. PEP numerics (scouting2/exp_opt/fw_gap_big.txt)
give ≈ 1.665.
