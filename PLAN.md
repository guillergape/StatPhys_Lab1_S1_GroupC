# Work plan

Deadline: **Tue 3 Nov 2026** (repo URL + report PDF on Aula Global, −1 point per day late). Phase numbers follow the Lab 1 Project Guidelines.

## Branches (one per person)

| Branch | Owner | Files | Lab questions |
|---|---|---|---|
| `feature/bitwise-enumeration` | Guillermo | `src/microstates.py`, `tests/test_microstates.py` | Part 1 a, b |
| `feature/log-combinatorics` | Andrés | `src/combinatorics.py`, `tests/test_combinatorics.py` | Part 1 c, d, e |
| `feature/thermodynamics` | Héctor | `src/thermodynamics.py` (+ its tests) | Part 2 a–k |
| `feature/latex-report` | Carlos | `report/`, `main.py` | report, figures, integration |

Swapping owners only means editing this table. Nobody pushes to `main`: every branch enters through a PR approved by another member.

## Shared interfaces (agree before coding, so the branches don't block each other)

```python
# src/microstates.py
def microstates(N: int) -> Iterator[int]            # generator over 0 … 2**N − 1 (bit i = coin i, 1 = heads)
def macrostate_counts(N: int) -> list[int]           # Ω(N, k) for k = 0 … N by full enumeration

# src/combinatorics.py
def ln_omega(N: int, k: int) -> float                # lnΓ(N+1) − lnΓ(k+1) − lnΓ(N−k+1)

# src/thermodynamics.py
def probability(N: int, k: int) -> float             # Ω(N, k) / 2**N, computed in log space
def delta_entropy(N: int, k1: int, k2: int) -> float # ΔS / k_B = ln Ω1 − ln Ω2
```

## Phases

### Phase 1–4 · Setup (done 20 Oct, Guillermo)
Environment, repository, protected `main`, layout, AI statement. Everyone: clone, `conda env create -f environment.yml`, select the interpreter in VS Code, `git checkout <your branch>`.

> Prompt: "Divide the lab into phases and create one feature branch per team member, with the files and lab questions each one owns and the function signatures we share."

### Phase 5a · Bitwise enumeration — Guillermo, by Tue 27 Oct
Generator over `1 << N` states, popcount per state, N = 7 table, largest N within 5 min with time and RAM measured (extra point for the largest N in the group).

> Prompt: "Explain how to enumerate the 2^N microstates of N coins with bitwise operations and a Python generator so memory stays constant, and how to measure the run time and peak RAM of the enumeration. Don't write the function for me; review mine afterwards."

### Phase 5b · Log-space combinatorics — Andrés, by Tue 27 Oct
`ln_omega` with `math.lgamma`, Ω(N, k) plot for N = 20, 50, 80, 100 (normalised so the curves compare), largest N for the distribution and its limiting factor, the N ~ 10²³ limit. Tests: `ln_omega` against `math.comb` for small N.

> Prompt: "Explain why computing Ω(N, k) with factorials overflows for large N and how the log-Gamma form avoids it, and what a pytest should check to prove the log-space values match the exact integers."

### Phase 5c · Thermodynamics — Héctor, by Tue 27 Oct
N = 100 + M (M = harmonic mean of the last two digits of the four NIAs: collect them first). Probabilities, ΔP intervals, ΔS = k_B ln(Ω1/Ω2), waiting time for 8 heads, ratios, Second Law discussion, N → ∞ limit. Uses `ln_omega` from Phase 5b (stub it until that PR is merged).

> Prompt: "Explain how to get probabilities of macrostates and their intervals from ln Ω without overflow, and how to estimate the waiting time to see a given macrostate when N coins are thrown per second."

### Phase 6 · Report and integration — Carlos, from now to Sat 31 Oct
Intro, objectives and methodology now (they don't depend on results); `main.py` calls the three modules and saves every figure as vector PDF in `report/figures/`; results sections once the PRs are merged; appendix = this repo's `AI_STATEMENT.md`.

> Prompt: "Review the structure of our LaTeX report against the template and tell me what each section needs; check that every figure is a vector PDF with units and uncertainties stated."

### Phase 7 · Merge and submit — everyone, Thu 29 Oct → Mon 2 Nov
PRs reviewed and merged by Thu 29 Oct; all tests pass on a clean clone; tag `v1.0`; submit repo URL + PDF.

> Prompt: "Check that main.py and pytest run from a clean clone of the repository, and list anything missing before tagging v1.0."

### Phase 8 · Oral defense — everyone
Any member may be chosen: each one must be able to show `git log`, run `main.py` and the tests on their own laptop, and explain all three algorithms, not only their own.

> Prompt: "Ask me the questions a teacher would ask about our enumeration, log-space combinatorics and entropy results, one at a time, and correct my answers."

Every prompt actually used goes into `AI_STATEMENT.md` with what it generated and what we changed.
