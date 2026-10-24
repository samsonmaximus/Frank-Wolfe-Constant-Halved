# Referee report: "A halved constant for vanilla Frank–Wolfe" (proof.md)

**Verdict: CORRECT.** No gap found. Some minor presentation issues are listed at the end.

## 1. Line-by-line check

**Step 1 (descent).** The descent lemma is applied on the segment [x_k, x_{k+1}] ⊂ C (C is convex and h_k ∈ (0,1]). LMO optimality gives ⟨∇f(x_k), s_k − x_k⟩ ≤ ⟨∇f(x_k), x* − x_k⟩. Convexity gives this is ≤ f* − f(x_k). So (1) e_{k+1} ≤ (1−h_k)e_k + (h_k²/2)δ_k holds. The step uses only that inequality, not uniqueness of s_k, so any LMO tie-breaking is covered. ✔

**(2).** Y ~ μ_k has mean x_k, so E‖s−Y‖² = ‖s−x_k‖² − 2⟨s−x_k, E(Y−x_k)⟩ + E‖Y−x_k‖² = ‖s−x_k‖² + V_k. Both s_k and supp μ_k lie in C, so ‖s_k−Y‖ ≤ D = 1. That gives δ_k ≤ 1 − V_k. The support claim holds by induction, since μ_0 = δ_{x_0} needs x_0 ∈ C and s_k ∈ C. The mean claim also holds by induction: mean(μ_{k+1}) = (1−h)x_k + h s_k = x_{k+1}. ✔

**(3), re-derived.** For a mixture, Var = Σ w_i [Var_i + ‖mean_i − x_{k+1}‖²]. The component μ_k has weight 1−h, variance V_k, and ‖x_k − x_{k+1}‖² = h²δ. The component δ_{s_k} has weight h, variance 0, and ‖s_k − x_{k+1}‖² = (1−h)²δ. So
V_{k+1} = (1−h)V_k + (1−h)h²δ + h(1−h)²δ = (1−h)V_k + h(1−h)δ[h + 1 − h] = (1−h)V_k + h(1−h)δ. ✔

**(4).** W_{k+1} = 1 − (1−h)(1−W_k) − h(1−h)δ = h + (1−h)W_k − h(1−h)δ. ✔ Also W_k = 1 − V_k ≥ 0, because V_k is an average of squared distances between points of C, so V_k ≤ 1. Equivalently, 0 ≤ δ_k ≤ W_k. As it turns out, the argument never needs W_k ≥ 0 separately: W_k only enters through equalities and through c_kδ_k ≤ c_kW_k.

**Step 3.** h_0 = 1, so x_1 = s_0 and (1) gives e_1 ≤ δ_0/2 ≤ 1/2, using V_0 = 0. Then μ_1 = δ_{s_0}, so V_1 = 0 and W_1 = 1. ✔ This also gives E_1 = 2e_1 ≤ 1, which is used for Φ_1.

**(5).** (k+1)(k+2)·k/(k+2) = k(k+1) and (k+1)(k+2)·(1/2)·4/(k+2)² = 2(k+1)/(k+2). ✔

**(6) and the Lemma.** α_k ≥ 0 for all k, since it is a sum of nonnegative terms starting from α_N = 0. For the induction step, if α_{k+1} ≤ k+2 then α_k ≤ 2(k+1)/(k+2) + k²/(k+2) ≤ 2 + k²/(k+2). The last quantity is ≤ k+1 iff k² + 2k + 4 ≤ k² + 3k + 2 iff k ≥ 2. ✔

The exact expression gives more: (k² + 2k + 2)/(k+2) ≤ k+1 holds for every k ≥ 0. So the restriction k ≥ 2 comes only from the crude bound 2(k+1)/(k+2) ≤ 2 and is harmless.

The step only needs α_{k+1} ≤ k+2 for 1 ≤ k ≤ N−1, i.e. for indices 2..N, which is exactly what the Lemma covers. Edge cases:
- k+1 = N: α_N = 0. ✔
- N = 2: α_2 = 0, α_1 = 4/3, B_2 = 1 + 4/3 + 0 = 7/3 = 2 + H_1/3. ✔
- N = 1: handled by Step 3, where the bound is 1/2. ✔

**c_k sign.** h(1−h) = 2k/(k+2)², so c_k ≥ 2(k+1)/(k+2) − (k+2)·2k/(k+2)² = 2/(k+2) > 0. ✔

**Identity.** c_k + α_{k+1}(1−h) = 2(k+1)/(k+2) + α_{k+1}[(1−h) − h(1−h)] = 2(k+1)/(k+2) + α_{k+1}(1−h)² = α_k. ✔

**Telescoping.** Φ_{k+1} ≤ Φ_k + α_{k+1}h_k for k = 1..N−1. With Φ_1 ≤ 1 + α_1 (this uses E_1 ≤ 1, W_1 = 1 and α_1 ≥ 0) and Φ_N = E_N, we get (7). ✔

**Step 5.** With δ̄ = W̄, each inequality used in Step 4 is an equality: (5) by definition, c_kδ̄_k = c_kW̄_k, and Φ̄_1 = 1 + α_1. Hence Φ̄_{k+1} = Φ̄_k + α_{k+1}h_k exactly, and Ē_N = B_N. ✔

- **W̄ induction.** W̄_1 = 3·4/(6·2) = 1. Then 2/(k+2) + k(3k+1)/(6(k+1)(k+2)) = (12k + 12 + 3k² + k)/(6(k+1)(k+2)) = (3k² + 13k + 12)/(…), and 3k² + 13k + 12 = (k+3)(3k+4). ✔
- **Increment.** 2(k+1)/(k+2) · (k+2)(3k+1)/(6k(k+1)) = (3k+1)/(3k). ✔
- **Total.** B_N = 1 + (N−1) + H_{N−1}/3 = N + H_{N−1}/3. ✔
- **Corollaries.** (N + H/3)/(N(N+1)) = (1 + H_{N−1}/(3N))/(N+1), and this is ≤ (4/3)/(N+1) because H_{N−1} ≤ N. ✔

I also checked the algebra in exact rationals (my own code) for every N ≤ 300: α_k ≥ 0, α_k ≤ k+1 for k ≥ 2, c_k > 0, the identity c_k + α_{k+1}(1−h_k) = α_k, the closed form of W̄_k, and B_N = N + H_{N−1}/3. All pass.

## 2. Independent numerical test (experiments/referee_fw.py, written from scratch)

This is vanilla Frank–Wolfe on convex quadratics f = ½xᵀAx − bᵀx, with A PSD scaled so that ‖A‖₂ = L = 1. Test details:
- **D for polytopes:** the maximum pairwise vertex distance.
- **D for balls:** 2r = 1.
- **f\*:** computed with SLSQP and then replaced by a certified *lower bound*, f(x̂) + min_v⟨∇f(x̂), v − x̂⟩. This makes the measured error conservative.
- **Tie-breaking:** LMO ties go to the vertex farthest from x_k. When ∇f = 0 on a ball, the iterate jumps to a random boundary point.

| test | instances | violations | worst ratio vs bound |
|---|---|---|---|
| random polytopes, d=1..5, 2..7 vertices, rank-1/diag/full A, x0 a vertex or interior point, N ∈ {1,2,3,4,5,7,10,15,20,40} | 4000 × 10 | 0 | N=1: 0.494/0.5; N=2: 0.216/0.389; N=10: 0.0145/0.0995 |
| balls, d=2..4 | 1500 × 10 | 0 | N=2: 0.220/0.389 |
| 1-D, C=[0,1], f=½(x−a)², grid over a and x0 | 802 per N | 0 | N=1: 0.495; N=2: 0.219 |
| adversarial tie (x0 = x\* = 0, ∇f = 0) | – | 0 | N=1: 0.125 |
| hill-climbing over 2-D instances (A, b, vertices, x0) | 6 restarts × 1500 | 0 | N=1: 0.4975/0.5; N=2: 0.231; N=3: 0.132; N=5: 0.049; N=10: 0.022 |

All quadratic instances stay well below both the bound and the PEP values. That is expected, because the PEP worst case is a non-quadratic function. For N=1 the bound of 1/2 is approached (0.4975), which matches Step 3 being tight.

## 3. PEP comparison (L = D = 1)

| N | bound | PEP w_N | margin |
|---|---|---|---|
| 2 | 0.38888889 | 0.31261699 | 0.0763 |
| 3 | 0.29166667 | 0.22784810 | 0.0638 |
| 5 | 0.18981481 | 0.14621246 | 0.0436 |
| 10 | 0.09948172 | 0.07828955 | 0.0212 |
| 20 | 0.05043471 | 0.04132259 | 0.0091 |
| 40 | 0.02525479 | 0.02156374 | 0.0037 |

The bound exceeds w_N in every case, so it is consistent with the PEP values. It is also below the classical 2/(N+2) for all N ≥ 1.

## 4. Hidden assumptions and minor issues

- **Euclidean norm.** The variance identity in (2) and (3) needs an inner-product norm. L-smoothness and D must both be taken in ‖·‖₂. This is implicit and should be stated.
- **Smoothness only on C is enough.** f only needs to be differentiable, convex and L-smooth on (a neighbourhood of) C, because every point used lies in C. f* is attained because C is compact and f is continuous. x_0 ∈ C is used essentially, for supp μ_0 ⊂ C.
- **Exact LMO.** The proof needs an exact LMO. Any tie-breaking is fine, but an approximate LMO is not covered.
- **Wording.** In the Theorem, "f(x_N) − f* = (1+o(1))-bounded by LD²/N" is awkward. Suggest "≤ (1+o(1)) LD²/N".
- **Lemma range is understated.** The Lemma's bound actually holds for all k ≥ 1, since α_1 ≤ 2 is true. It is only stated for k ≥ 2, which costs nothing.
- **h_k is not involved.** The step size enters only through the identities in (5), (6) and Step 5, all of which were verified.

Conclusion: the proof is complete and correct as written, under the standard Euclidean setting.

## Addendum (2026-10-21): Corollary (FW gap ≤ 3LD²/(N+1))
Checked in the main session (referee agents unavailable):
- `experiments/gap_corollary_all.py`: exact rational optimisation over K0 for EVERY N ≤ 400; max (N+1)·bound = 2.898393 (N = 49) < 3.
- Tail N > 400, re-derived by hand:
  - Σ_{k≥m} 2/(k+2)² ≤ 2/(m+1) − 2/(N+2) (telescoping);
  - H_{m−1} ≤ 1 + ln m, so ε_m ≤ (1+ln 200)/600 = 0.010497;
  - 1/(m+1) ≤ 2/(N+2) for m = ⌈N/2⌉;
  - Σ h_k ≥ 2∫_{m+2}^{N+3} dt/t, with (N+3)/(m+2) ≥ 2(N+3)/(N+5) increasing in N;
  - 2 ln(806/405) = 1.37639. Result: 4.021/1.37639 = 2.9214 < 3. PASS.
- Ingredients: the descent lemma uses only ‖s_k − x_k‖ ≤ D and the exact LMO (g_k = ⟨∇f(x_k), x_k − s_k⟩). x_{N+1} ∈ C is defined, so e_{N+1} ≥ 0. PASS.
Verdict for the corollary: CORRECT. Novelty: improves Jaggi's 27/4. The best published FW-gap constant (Freund–Grigas?) was not verified;
check before submission.
