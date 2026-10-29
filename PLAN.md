# Work plan

Deadline: **Tue 3 Nov 2026** (repo URL + report PDF on Aula Global, −1 point per day late). Each member just tells their AI assistant **"hazme la siguiente fase que me toca"**; the procedure it follows is in `AGENTS.md`.

## Team

| Member | GitHub | git user.name | AI tool | Reviews PRs of | NIA last 2 digits |
|---|---|---|---|---|---|
| Guillermo García Pelayo | `guillergape` | GUILLERMO GARCIA PELAYO | Claude Code | Héctor | 69 |
| Andrés Mármol del Amo | `AndreuwMetal` | AndreuwMetal | Claude Code (Max) | Carlos | 22 |
| Héctor Armenteros Arauzo | `HectorArmen` | HectorArmen | GitHub Copilot, Antigravity | Guillermo | 09 |
| Carlos Cordero López | `Carlos8281-progra` | | GitHub Copilot, Antigravity | Andrés | 45 |

Fill in your `git config user.name` and your NIA's last two digits in your first PR.

## Phases

Status is the source of truth for "what's next": `todo` → `done` (set to `done` in the phase's own PR, so it reaches `main` when the PR is merged). Owners can be swapped by editing this table.

| # | Phase | Owner | Branch | Needs | Due | Status |
|---|---|---|---|---|---|---|
| 1 | Setup: environment, repo, layout, AI statement | Guillermo | — | — | 20 Oct | done |
| 2 | Bitwise enumeration (Part 1 a, b) | Guillermo | `feature/bitwise-enumeration` | — | Sun 25 Oct | todo |
| 3 | Log-space combinatorics (Part 1 c, d, e) | Andrés | `feature/log-combinatorics` | — | Sun 25 Oct | done |
| 4 | Probabilities (Part 2 a–d) and N = 100 + M | Héctor | `feature/probabilities` | 3 | Mon 26 Oct | done |
| 5 | Report I: structure, introduction, methodology | Carlos | `feature/latex-report` | — | Sun 25 Oct | todo |
| 6 | Entropy and thermodynamic implications (Part 2 e–i) | Andrés | `feature/entropy` | 3, 4 | Tue 27 Oct | todo |
| 7 | Second Law and large-N limit (Part 2 j, k) | Andrés | `feature/large-n` | 4, 6 | Wed 28 Oct | todo |
| 8 | Integration: `main.py` and vector figures | Guillermo | `feature/integration` | 2, 3, 4, 6 | Thu 29 Oct | todo |
| 9 | Report II: results, conclusion, AI appendix | Carlos | `feature/latex-report` | 5, 7, 8 | Sat 31 Oct | todo |
| 10 | Release: clean-clone check, tag `v1.0`, submit | Héctor | `release/v1.0` (only if fixes are needed) | 1–9 | Mon 2 Nov | todo |
| 11 | Defense rehearsal | everyone | — | 10 | before the session | todo |

## Shared interfaces

Every phase codes against these names, so the branches don't block each other.

```python
# src/microstates.py
def microstates(N: int) -> Iterator[int]            # generator over 0 … 2**N − 1 (bit i = coin i, 1 = heads)
def macrostate_counts(N: int) -> list[int]           # Ω(N, k) for k = 0 … N by full enumeration

# src/combinatorics.py
def ln_omega(N: int, k: int) -> float                # lnΓ(N+1) − lnΓ(k+1) − lnΓ(N−k+1)

# src/thermodynamics.py
def team_N() -> int                                  # 100 + M
def probability(N: int, k: int) -> float             # Ω(N, k) / 2**N, computed in log space
def interval_probability(N: int, k1: int, k2: int) -> float   # Σ_{k=k1}^{k2} P_k
def delta_entropy(N: int, k1: int, k2: int) -> float # ΔS / k_B = ln Ω(k1) − ln Ω(k2)
```

Each physics phase writes its answers (numbers with units and uncertainties, tables, discussion) in its own `report/sections/<branch-name>.tex`; `report/main.tex` only `\input`s them.

## What each phase must do

Lab questions are quoted from the manual (*Microstates of a System of Coins*, V. Tribaldos, 2026).

### Phase 2 · Bitwise enumeration — Guillermo
- `microstates(N)`: generator built on `1 << N`; heads per state with `int.bit_count()`. `macrostate_counts(N)` from it. Memory must stay constant in N.
- **1a** "List all possible outcomes (microstates) for a system of N = 7 coins and, for each macrostate, state the corresponding number of microstates, analogous to the structure of Table 1." → table of the 128 states grouped by k, with Ω.
- **1b** "Determine and report the largest N for which the program can fully enumerate and list all 2^N microstates (you don't have to write them). Provide a rigorous explanation detailing the computational or memory constraints." Benchmark script: time and peak RAM (`time.perf_counter`, `tracemalloc`) for growing N, largest N within **5 min** wall clock (extra point for the best team), extrapolate with the measured time per state. Speed-ups that keep the enumeration real are allowed.
- Tests `tests/test_microstates.py`: sum of counts = 2^N, counts = `math.comb(N, k)` for N ≤ 15, N = 5 matches Table 1 (1, 5, 10, 10, 5, 1).

### Phase 3 · Log-space combinatorics — Andrés
- `ln_omega(N, k)` with `math.lgamma`.
- **1c** "Calculate Ω(N, k) for k heads (k = 0, …, N) for N = 20, 50, 80, and 100. Generate a single plot illustrating the macrostate distribution as a function of k for all four N values." Plotting function that saves a vector PDF to `report/figures/`.
- **1d** "Determine and explain the maximum N that can be practically considered for calculating and plotting the macrostate distribution. Explain the limiting factor." (float overflow of Ω vs ln Ω, number of points to plot, exact `math.comb` cost.)
- **1e** "Discuss, in detail, the expected physical behavior and statistical characteristics of the macrostate distribution when the system size is scaled up to N ∼ 10²³." (Gaussian limit, width √N/2, relative width 1/√N.)
- Tests `tests/test_combinatorics.py`: `exp(ln_omega)` vs `math.comb` for N ≤ 100 (relative tolerance), symmetry k ↔ N − k, edge cases k = 0, N.

### Phase 4 · Probabilities — Héctor
- **N = 100 + M**, M = "the harmonic average of the last two digits of the team members' NIAs", N < 200. Use the four two-digit numbers from the Team table (a digit-by-digit mean breaks on a 0), state the rounding and how odd N is handled (N/2), and write it in the report.
- **2a** P(k = 30). **2b** P(k = N/2), "the most probable macrostate". **2c** ΔP for k1 = N/2 − 10, k2 = N/2 + 10 heads. **2d** ΔP for k1 = N/2 − 20, k2 = N/2 + 20 **tails** (comment on the heads/tails symmetry). P_k = Ω(N, k)/2^N, always via `ln_omega`.
- Tests: probabilities over k sum to 1, symmetry, a small N checked against exact fractions.

### Phase 5 · Report I — Carlos
- `report/main.tex` following the template (*Lab_1_Repot*): title page, Introduction & Objectives, Methodology & Collaborative Workflow (environment, Git branches and PRs, AI protocol, testing), empty results sections that `\input{sections/...}` per phase, Conclusion, appendix with the AI statement. ≈ 5 pages, max 8, excluding the title page.
- Figures always vector PDF from `report/figures/`, every figure and table with units and uncertainties.
- Check it compiles (`latexmk -pdf` or Overleaf).

### Phase 6 · Entropy and thermodynamic implications — Andrés
- ΔS_{k1k2} ≡ S(k1) − S(k2), S = k_B ln Ω (report in J/K and in units of k_B). **2e** k1 = N/2 + 25 vs k2 = N/2. **2f** k1 = N/2 + 10 vs k2 = N/2. **2g** k1 = N/2 vs k2 = 20.
- **2h** "Assuming a tossing rate of N coins per second, calculate the expected waiting time required to randomly achieve a highly ordered state of only 8 heads." (one toss of all N coins per second → mean wait 1/P_8 s; compare with the age of the Universe.)
- **2i** "Quantify how much more likely it is to obtain the most probable macrostate (N/2 heads) compared to a macrostate with M ± 10 heads." (Read it as written, M ± 10; mention if the intended N/2 ± 10 reading changes the conclusion.)
- Tests for `delta_entropy` (sign, antisymmetry, ΔS = 0 for equal k).

### Phase 7 · Second Law and large-N limit — Andrés
- **2j** "Do any of the possible results, including those calculated above, contradict the Second Law of Thermodynamics? Provide a detailed explanation based on the statistical interpretation of entropy."
- **2k** "Re-evaluate the answers to a through j under the condition N ∼ 10²³, or the limit N → ∞." Use Stirling / Gaussian approximations; small functions where numbers are needed, the rest as derivations in `report/sections/feature-large-n.tex`.

### Phase 8 · Integration — Guillermo
- `main.py` runs every answer in order (Part 1 a–e, Part 2 a–k), prints a readable summary and regenerates every figure as vector PDF in `report/figures/`. Runs in < 5 min except the 1b benchmark, which goes behind a flag (`python main.py --benchmark`).
- `pytest` passes on the merged code; fix interface mismatches between modules.

### Phase 9 · Report II — Carlos
- Assemble the results sections, write the Conclusion, check numbering, units, uncertainties, figure references and length. Appendix = `AI_STATEMENT.md` (summary + link to the repo).

### Phase 10 · Release — Héctor
- Fresh clone in a new folder, `conda env create -f environment.yml`, `pytest`, `python main.py`, compile the report. Everything merged into `main`, tag `v1.0` (`git tag v1.0 && git push origin v1.0`), upload repo URL + report PDF to Aula Global and tell the team.

### Phase 11 · Defense rehearsal — everyone
Any member may be picked: each one shows `git log`, runs `main.py` and `pytest` on their own laptop, and explains the bitwise enumeration, the log-Gamma trick and the entropy results, not only their own part.
