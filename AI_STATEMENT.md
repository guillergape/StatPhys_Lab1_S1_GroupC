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
