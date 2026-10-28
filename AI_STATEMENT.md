# AI Statement and Prompt Log

Statistical Physics Lab 1, Section 1, Group C. Following Phase 3 of the Lab 1 Project Guidelines, every AI query is logged here: the prompt, what the AI generated, and what the team changed or verified.

**Policy:** AI tools are used as assistants only. Every AI-generated piece of logic must be covered by a unit test in `tests/` and understood by every member before it is merged.

## Entry format
Copy this block for each new query.

```
### <n>. <short title>
- Date / member / tool:
- Prompt:
- Generated:
- Team changes and verification:
```

---

## Log

### Session 1 · 20 Oct 2026 · Guillermo García · Claude Code (Claude Opus 5.5)

**Original prompt (verbatim, teammates' email addresses removed):**

> organize all the files of lab 1 stats numerical lab, create a folder for it. follow the isntructions for creating all the environments as specified in the report and create the repository and share the link with my mates (andres marmol [email], hector armenteros [email], carlos cordero [email]) por correo
> this prompts include them as well as separate prompts (rephrase them correctly so they are good include) in the prompt log

The same request, split into separate prompts and rephrased:

### 1. Organise the lab files
- **Prompt:** "Gather every file of the Statistical Physics Lab 1 (numerical lab) into a dedicated folder: the lab manual, the group list, the project guidelines and the report template."
- **Generated:** a local folder with the four Aula Global PDFs (*First Practice*, *Lab_1_Stat_Physics_Groups*, *Lab_Project*, *Lab_1_Repot*). No code.
- **Team changes and verification:** none needed.

### 2. Set up the reproducible environment (Phase 1)
- **Prompt:** "Following Phase 1 of the Lab 1 Project Guidelines, write the `environment.yml` file and build the `statphys_lab1` Conda environment (Python 3.11, numpy, scipy, matplotlib, pytest, jupyter)."
- **Generated:** `environment.yml`, copied from the guidelines with two typos fixed (`conda -forge` → `conda-forge`, `python =3.11` → `python=3.11`), and the environment built with `conda env create -f environment.yml`.
- **Team changes and verification:** each member builds it on their own laptop and selects it as the VS Code interpreter.

### 3. Create the repository and its layout (Phases 2 and 4)
- **Prompt:** "Following Phases 2 and 4, create the GitHub repository `StatPhys_Lab1_S1_GroupC` with a Python/LaTeX `.gitignore` and the required folder layout (`src/`, `tests/`, `notebooks/`, `report/`, `main.py`), protect `main` so that changes only enter through reviewed pull requests, and add the team as collaborators."
- **Generated:** `.gitignore`, `README.md` (setup and workflow), this file, the empty module files of the required layout (docstrings only, no physics or algorithm code) and a `report/main.tex` skeleton with the section titles of the report template.
- **Team changes and verification:** all the lab code (enumeration, log-space combinatorics, thermodynamics, tests) is still to be written by the team.

### 4. Share the repository with the team
- **Prompt:** "Write an email to my three teammates with the repository link, asking for their GitHub usernames so they can be added as collaborators."
- **Generated:** an email draft (reviewed and sent by Guillermo).
- **Team changes and verification:** none.

### 5. Divide the lab into phases
- **Date / member / tool:** 20 Oct 2026 · Guillermo García · Claude Code (Claude Opus 5.5)
- **Original prompt (verbatim):** "voy a dividirlo en fases" / "dividelo en fases"
- **Prompt (rephrased):** "Divide the lab into phases following the Lab 1 Project Guidelines and the lab manual: what each phase does, which lab questions it answers, which files it owns, its deadline, and the function signatures the phases share."
- **Generated:** `PLAN.md` (phase table with dependencies and deadlines, shared signatures, task of each phase quoting the manual's questions). No physics or algorithm code.
- **Team changes and verification:** the split into phases was the team's idea; we checked every lab question (Part 1 a–e, Part 2 a–k) is covered by exactly one phase.

### 6. One branch per member
- **Date / member / tool:** 20 Oct 2026 · Guillermo García · Claude Code (Claude Opus 5.5)
- **Original prompt (verbatim):** "vamos a dividir el trabajo en ramas una para cada persona"
- **Prompt (rephrased):** "Create a feature branch for each piece of work so that every member works on their own branch and merges through a reviewed pull request."
- **Generated:** the branches `feature/bitwise-enumeration`, `feature/log-combinatorics`, `feature/probabilities`, `feature/latex-report`, `feature/entropy`, `feature/large-n`, `feature/integration`, all created from `main`.
- **Team changes and verification:** none.

### 7. Distribute the phases among the members
- **Date / member / tool:** 20 Oct 2026 · Guillermo García · Claude Code (Claude Opus 5.5)
- **Original prompt (verbatim):** "distribuye las fases para cada persona, primero la mia luego andres y luego ya hector y carlos en el orden que quieras / si hay mas de 4 fases pues que se distribuyan mas o menos equitativamente, un poco mas a andres, luego yo y luego carlos y hector"
- **Prompt (rephrased):** "Assign the phases to the four of us in the order Guillermo, Andrés, then Héctor and Carlos, roughly evenly, with a bit more for Andrés, then me, then Carlos and Héctor, and pick a reviewer for each member's pull requests."
- **Generated:** the Owner column and the Team table (reviewers) in `PLAN.md`.
- **Team changes and verification:** owners can be swapped by editing `PLAN.md`.

### 9. Phase 3: log-space combinatorics (Part 1 c, d, e)
- **Date / member / tool:** 24 Oct 2026 · Andrés Mármol · Claude Code (Claude Opus 5.5)
- **Original prompt (verbatim):** "busca en mi github o en mi correo un proyecto que me compartió guillermo, clonalo, cambiate a mi rama y haz mi parte"
- **Prompt (rephrased):** "Implement Phase 3 of our plan: `ln_omega(N, k)` with `math.lgamma`, a single vector-PDF plot of Ω(N, k) against k for N = 20, 50, 80, 100 (question 1c), measurements of the largest N we can practically compute and plot and of what limits it (float overflow, cost of exact `math.comb`, log-space precision; question 1d), and the large-N (N ∼ 10²³) Gaussian behaviour of the distribution (question 1e). Add pytest tests and write the results in the report section."
- **Generated:** `src/combinatorics.py`: `ln_omega`, `ln_omega_array` (vectorised with `scipy.special.gammaln`), `gaussian_ln_omega` (Stirling/Gaussian limit), `largest_float_N`, `time_exact_row`, `ln_omega_error`, `plot_macrostate_distribution`; `tests/test_combinatorics.py` (8 tests); `report/figures/macrostate_distribution.pdf`; `report/sections/feature-log-combinatorics.tex`.
- **Team changes and verification:** `pytest`: 8 passed (`exp(ln_omega)` equals `math.comb(N, k)` to 1e-11 for every k and N ≤ 100, heads/tails symmetry, edges k = 0, 1, N, invalid k rejected, vectorised = scalar, float64 overflow exactly at N = 1030, Gaussian limit within 10/N near the peak, figure saved as PDF). Every number in the report section comes from `python -m src.combinatorics` and timing runs on Andrés's laptop (Apple M4 Max, 48 GB). The section compiles with pdfLaTeX (TinyTeX 2026) under the preamble of `report/main.tex`; the compile check caught `\lesssim` (needs `amssymb`, not loaded) and an equation 127 pt too wide, both fixed. Tests re-run in the `statphys_lab1` conda environment: 8 passed.

### 10. Phase 4: Probabilities (Part 2 a–d) and N = 100 + M
- **Date / member / tool:** 28 Oct 2026 · Héctor Armenteros · Google Antigravity (Gemini 3.8 Flash)
- **Original prompt (verbatim):** "sus dígitos son 45; haz todo lo que has dicho al final"
- **Prompt (rephrased):** "Implement Phase 4 of our plan: `team_N()` with N = 100 + M from the harmonic mean of the team's NIA digits (69, 22, 09, 45), `probability(N, k)` and `interval_probability(N, k1, k2)` in log space via `ln_omega`, answers to questions 2a (P(k=30)), 2b (most probable macrostate P(k=N/2)), 2c (heads interval [N/2-10, N/2+10]) and 2d (tails interval [N/2-20, N/2+20] and heads/tails symmetry). Add unit tests with pytest, write the LaTeX report section, push the branch to GitHub and open a Pull Request requesting review from Guillermo."
- **Generated:** `src/thermodynamics.py`: `harmonic_mean`, `team_nia_digits`, `team_M`, `team_N`, `probability`, `interval_probability`, `delta_entropy`, `solve_part2_a_to_d`; `tests/test_thermodynamics.py` (15 unit tests); `report/sections/feature-probabilities.tex`; updated `PLAN.md` (Phase 4 marked `done`, NIAs updated).
- **Team changes and verification:** `pytest`: 15 passed in the Python 3.11 environment (normalisation sum P_k = 1 to 1e-13, binary symmetry P(k) = P(N-k), exact fractions for N=4 and N=5, interval probability additivity, delta entropy antisymmetry, input error handling). Every number in `report/sections/feature-probabilities.tex` was generated by `python -m src.thermodynamics`. The branch is pushed to `origin/feature/probabilities` and a Pull Request opened targeting `main` with `guillergape` assigned as reviewer.

### 11. Phase 6: entropy and thermodynamic implications (Part 2 e–i)
- **Date / member / tool:** 28 Oct 2026 · Andrés Mármol · Claude Code (Claude Opus 5.5)
- **Original prompt (verbatim):** "ya ha terminado hector su parte. Haz otro PR con reviewer guille"
- **Prompt (rephrased):** "Implement Phase 6 of our plan on top of Phases 3 and 4: the entropy differences ΔS = k_B (ln Ω(k1) − ln Ω(k2)) in units of k_B and J/K for questions 2e, 2f and 2g, the mean waiting time to get only 8 heads tossing the N coins once per second compared with the age of the Universe (2h), and how much more likely the most probable macrostate is than M ± 10 heads, also under the N/2 ± 10 reading (2i). Handle the odd N = 121, add pytest tests, write the report section and open a pull request with Guillermo as reviewer."
- **Generated:** `src/thermodynamics.py` (appended, Héctor's Phase 4 code untouched): `K_B`, `AGE_OF_UNIVERSE_S`, `likelihood_ratio`, `waiting_time`, `solve_part2_e_to_i` and its lines in `__main__`; `tests/test_entropy.py` (7 tests); `report/sections/feature-entropy.tex`. The branch merges `feature/log-combinatorics` (Phase 3) and `feature/probabilities` (Phase 4), with the `PLAN.md` and `AI_STATEMENT.md` conflicts resolved by keeping both sides.
- **Team changes and verification:** `pytest`: 30 passed in the `statphys_lab1` conda env (ratio = P(k1)/P(k2) = exp(ΔS/k_B), exact small-N ratio, waiting time = 1/P including a 3-coin case, J/K = k_B × units of k_B, signs of 2e–2g, the N/2 ± 10 pair symmetric, even N collapses the degenerate peak). A first version paired k = 50 and 70 for "N/2 ± 10", which are not symmetric about 60.5 and gave different ratios (6.12 vs 4.40); corrected to the mirror pair 51 and 70. Every number in the report section comes from `python -m src.thermodynamics`; the section compiles with pdfLaTeX under the preamble of `report/main.tex`.
