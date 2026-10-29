"""Entry point: runs every lab question in order and saves the figures to report/figures/.

    python main.py               Part 1 a-e and Part 2 a-k (about a minute)
    python main.py --benchmark   also question 1b's enumeration benchmark (up to ~5 min more)
"""
import argparse
import runpy
import warnings
from pathlib import Path

import numpy as np

from src.combinatorics import FIGURES
from src.microstates import benchmark, macrostate_counts, macrostates_table
from src.thermodynamics import probability, solve_part2_a_to_d

# runpy re-runs modules already imported above; harmless here, they only define functions
warnings.filterwarnings("ignore", message=".*found in sys.modules", category=RuntimeWarning)


def plot_probability_distribution(path: Path = FIGURES / "probability_distribution.pdf") -> Path:
    """P_k against k for the team's N, with the intervals of questions 2c and 2d shaded."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    r = solve_part2_a_to_d()
    N = r["N"]
    k = np.arange(N + 1)
    P = np.array([probability(N, int(i)) for i in k])
    fig, ax = plt.subplots(figsize=(6, 4))
    # 2d counts tails, but P(tails = t) = P(heads = t), so its band is the same range of k
    for (lo, hi), q, var, colour in ((r["2d_range_sym"], "2d", "N-k", "tab:orange"),
                                     (r["2c_range_sym"], "2c", "k", "tab:blue")):
        mask = (k >= lo) & (k <= hi)
        ax.fill_between(k[mask], P[mask], step="mid", alpha=0.4, color=colour,
                        label=f"({q[1]}) ${lo} \\leq {var} \\leq {hi}$: $\\Delta P = {r[q + '_dp_symmetric']:.4f}$")
    ax.step(k, P, where="mid", color="k", lw=1)
    ax.axvline(30, color="tab:red", ls="--", lw=1, label=f"(a) $k = 30$: $P = {r['2a_p30']:.2e}$")
    ax.set_xlabel("Number of heads $k$")
    ax.set_ylabel(f"Probability $P_k$ ($N = {N}$)")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)
    return path


def part1(run_benchmark: bool) -> None:
    print("=== Part 1a: microstates of N = 7 coins (H = heads, T = tails, coin 0 first) ===")
    for k, states in enumerate(macrostates_table(7)):
        print(f"k = {k}   Omega = {len(states):2d}   " + " ".join(states))
    print(f"total = {sum(macrostate_counts(7))} = 2^7")

    print("\n=== Part 1b: largest N fully enumerated in 5 min ===")
    if run_benchmark:
        benchmark()
    else:
        print("skipped (takes up to ~5 min): run `python main.py --benchmark`")

    print("\n=== Part 1c-e: log-space combinatorics ===")
    runpy.run_module("src.combinatorics", run_name="__main__")


def part2() -> None:
    print("\n=== Part 2a-k: probabilities, entropy, Second Law and large N ===")
    runpy.run_module("src.thermodynamics", run_name="__main__")
    print("figure:", plot_probability_distribution())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--benchmark", action="store_true", help="also run question 1b's 5-minute benchmark")
    args = parser.parse_args()
    part1(args.benchmark)
    part2()
