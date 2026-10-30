# Instructions for AI assistants (Claude Code, GitHub Copilot, Antigravity…)

Statistical Physics Lab 1 (UC3M, Section 1 – Group C): N-coin microstates, log-space combinatorics and entropy, in Python + LaTeX. The plan, owners, shared function signatures and the full task of every phase are in `PLAN.md`. Talk to the member in the language they write in; code, comments, commits and the report are in English.

## "Do my next phase" (in any language)

1. **Sync:** `git fetch origin`. Read `PLAN.md` **from `origin/main`** (`git show origin/main:PLAN.md`), not from the current branch.
2. **Who is asking:** match `gh api user --jq .login` (if `gh` is installed) or `git config user.name` / `user.email` against the Team table. If the member said their name, use that. If nothing matches, ask who they are and stop.
3. **Which phase:** the member's first phase whose status on `origin/main` is not `done`. If that phase's branch on origin already has `done` in its own `PLAN.md`, it is waiting for review: tell the member to ask their reviewer, and move to their next phase. If its "Needs" phases are not `done` on `main`, say which ones are missing; work on it anyway only if it can be coded against the shared signatures in `PLAN.md` (never edit another phase's files to fill the gap). Tell the member in one line which phase you're starting and why.
4. **Branch:** `git checkout <branch>` (create it from `origin/main` if it doesn't exist), then `git merge origin/main`. Never commit to `main`.
5. **Environment:** run everything in the `statphys_lab1` Conda environment (`conda activate statphys_lab1`; create it with `conda env create -f environment.yml` if missing).
6. **Do the phase** exactly as described under its section in `PLAN.md`:
   - Typed functions with docstrings, in the module the phase owns, using the shared signatures unchanged.
   - Every new function gets pytest tests in `tests/`. Run `pytest` until it passes.
   - Numbers and discussion for the report go in `report/sections/<branch-name>.tex` (e.g. `feature-probabilities.tex`), with units and uncertainties. Figures as vector PDF in `report/figures/`.
   - Only touch the files of your phase, plus `PLAN.md` (your row) and `AI_STATEMENT.md`.
7. **Log it in `AI_STATEMENT.md`** with the entry format there: date, member, tool; **Prompt** = what the member asked for, in their own voice and first person (e.g. "Implement Phase 2 of our plan: …", summarising the phase task); **Generated** = files and functions; **Team changes and verification** = tests run and their result, anything the member changed or rejected.
8. **Close the phase:** set the phase's status to `done` in `PLAN.md` (fill in the member's git user.name / NIA digits if missing), commit with a clear message, `git push -u origin <branch>`, and open a PR to `main` with the reviewer from the Team table (`gh pr create --base main --reviewer <github user>`; without `gh`, give the member the PR link GitHub printed on push).
9. **Explain it to the member** (they may be the one picked for the oral defense): what each function does and why (bitwise generator, log-Gamma, the physics of each answer), the key results, and three questions the teacher could ask, with short answers. Remind them to read the code before asking for the review.

## Rules
- Never push to `main`, force-push, rewrite history or delete branches.
- Never edit another member's phase files; if their code has a bug that blocks you, tell the member and describe the fix for its owner.
- Don't invent results: every number in the report comes from running the code.
