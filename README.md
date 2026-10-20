# StatPhys_Lab1_S1_GroupC

Statistical Physics (UC3M 2026/27), Lab 1: *Microstates of a System of Coins*. Section 1, Group C: Andrés Mármol, Héctor Armenteros, Carlos Cordero, Guillermo García.

## Setup
```
conda env create -f environment.yml
conda activate statphys_lab1
```
In VS Code: `Ctrl+Shift+P` → *Python: Select Interpreter* → `statphys_lab1`.

## Workflow
- Never push to `main`: work on a branch (`feature/<topic>`), open a Pull Request, get one teammate's approval, then merge.
- Log every AI query in `AI_STATEMENT.md` (prompt, generated code, what we changed).
- Run `python main.py` and `pytest` before opening a PR.

## Layout
`src/` code · `tests/` pytest · `notebooks/` exploration · `report/` LaTeX (`main.tex`, vector figures in `figures/`)
