# Halving the Constant in the Frank–Wolfe Rate

The Frank–Wolfe method with step size 2/(k+2) has carried the guarantee
f(x_N) − f* ≤ 2LD²/(N+2) since Jaggi (2013). No method of its kind can beat
LD²/(4N), so the open question was the constant. This preprint proves
    f(x_N) − f*  ≤  LD² (N + H_{N−1}/3) / (N(N+1)),

where H_m is the m-th harmonic number. The bound is exact at N = 1 and tends to
LD²/N, half the classical constant. To guarantee an error of 1% of LD², the
classical bound needs 198 iterations; this one needs 101. The same argument
lowers the constant for the Frank–Wolfe gap from 27/4 to 3.

The idea: each iterate is a weighted average of earlier points. The more spread
out those points are, the shorter the next step must be, so long steps now force
short steps later.

**Paper:** [`paper/frank_wolfe_constant.pdf`](paper/frank_wolfe_constant.pdf)
(LaTeX source alongside).

## Status

The proof was found and checked with Opus 5.5. Every identity in it is
checked in exact rational arithmetic (`check_proof.py`), and an AI referee
re-derived it line by line ([`referee_report.md`](referee_report.md), which reviews
the earlier write-up [`proof.md`](proof.md))

## Reproducing

Python 3.11 or later:

```
pip install -r requirements.txt
cd experiments
python check_proof.py             # exact checks of every identity in the proof
python gap_corollary_all.py       # exact check of the gap corollary for N <= 400
python pep_fw.py 1 2 3 5 10 20    # exact worst case by PEP (Table 1)
python variance_lp.py             # the variance linear program
```

Tested with numpy 2.5.3, scipy 1.18.1 and cvxpy 1.9.3 (Clarabel solver).

| Script                                | What it checks                                                                 |
| ------------------------------------- | ------------------------------------------------------------------------------ |
| `check_proof.py`                      | the recursion, Lemma 3, c_k > 0 and B_N = N + H_{N−1}/3, exactly               |
| `gap_corollary_all.py`                | Corollary 5 for every N ≤ 400, exactly                                         |
| `pep_fw.py`                           | the performance-estimation values w_N of Table 1                               |
| `pep_fw_ablate.py`, `pep_fw_local.py` | the constraint-ablation experiments of Remark 4                                |
| `variance_lp.py`                      | the linear program behind the proof, for general step sizes                    |
| `gap_lp.py`                           | the variance relaxation for the gap                                            |
| `referee_fw.py`                       | an independent check that runs Frank–Wolfe on random and adversarial instances |

## License

Code: MIT (see `LICENSE`). Paper: © 2026 Samson Fraser, CC BY 4.0.
