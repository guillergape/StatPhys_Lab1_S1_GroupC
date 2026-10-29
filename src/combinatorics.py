"""Binomial multiplicities Omega(N, k), exact and in log space.

Omega(N, k) = N! / (k! (N - k)!) overflows a float64 for N >= 1030, so it is handled
through its logarithm, ln Omega = lnGamma(N+1) - lnGamma(k+1) - lnGamma(N-k+1),
which stays a modest number (~ N ln 2) for any N.
"""

import math
import sys
import time
from pathlib import Path

import numpy as np
from scipy.special import gammaln

FIGURES = Path(__file__).resolve().parent.parent / "report" / "figures"
LN_FLOAT_MAX = math.log(sys.float_info.max)  # ~709.78: exp of anything larger is inf


def ln_omega(N: int, k: int) -> float:
    """ln Omega(N, k) with the log-Gamma function (Gamma(n + 1) = n!)."""
    if not 0 <= k <= N:
        raise ValueError(f"need 0 <= k <= N, got N={N}, k={k}")
    return math.lgamma(N + 1) - math.lgamma(k + 1) - math.lgamma(N - k + 1)


def ln_omega_array(N: int) -> np.ndarray:
    """ln Omega(N, k) for every k = 0 ... N at once (vectorised ln_omega)."""
    k = np.arange(N + 1, dtype=np.float64)
    return gammaln(N + 1.0) - gammaln(k + 1) - gammaln(N - k + 1)


def gaussian_ln_omega(N: int, k: float) -> float:
    """Large-N (Stirling + Gaussian) approximation of ln Omega(N, k):
    N ln 2 + (1/2) ln(2 / (pi N)) - 2 (k - N/2)^2 / N, i.e. a Gaussian of mean N/2 and sigma sqrt(N)/2.
    """
    return N * math.log(2) + 0.5 * math.log(2 / (math.pi * N)) - 2 * (k - N / 2) ** 2 / N


def largest_float_N() -> int:
    """Largest N for which every Omega(N, k) fits in a float64 (the peak k = N/2 overflows first)."""
    N = 1
    while ln_omega(N + 1, (N + 1) // 2) <= LN_FLOAT_MAX:
        N += 1
    return N


def time_exact_row(N: int) -> float:
    """Seconds to compute the whole row math.comb(N, k), k = 0 ... N, with exact big integers."""
    t0 = time.perf_counter()
    for k in range(N + 1):
        math.comb(N, k)
    return time.perf_counter() - t0


def ln_omega_error(N: int) -> float:
    """|ln_omega(N, N/2) - ln(exact integer)|: rounding error of the log-Gamma difference."""
    return abs(ln_omega(N, N // 2) - math.log(math.comb(N, N // 2)))


def plot_macrostate_distribution(Ns: tuple[int, ...] = (20, 50, 80, 100),
                                 path: Path = FIGURES / "macrostate_distribution.pdf") -> Path:
    """Question 1c: Omega(N, k) against k for every N in Ns on one log-scale plot, saved as vector PDF."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 4))
    for N in Ns:
        ax.semilogy(np.arange(N + 1), np.exp(ln_omega_array(N)), "o-", ms=2.5, lw=1, label=f"$N={N}$")
    ax.set_xlabel("Number of heads $k$")
    ax.set_ylabel(r"Multiplicity $\Omega(N,k)$")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)
    return path


if __name__ == "__main__":
    for N in (20, 50, 80, 100):
        k = N // 2
        print(f"N = {N:3d}   Omega(N, {k}) = {math.comb(N, k):.6e}   ln Omega = {ln_omega(N, k):.4f}")
    print("figure:", plot_macrostate_distribution())
    print("largest N with Omega in float64:", largest_float_N())
    for N in (1_000, 5_000, 10_000, 20_000):
        print(f"exact math.comb row, N = {N:6d}: {time_exact_row(N):7.2f} s", flush=True)
    for N in (10**3, 10**4, 10**5, 10**6):
        print(f"|error ln Omega(N, N/2)|, N = 1e{round(math.log10(N))}: {ln_omega_error(N):.1e}", flush=True)
    for e in (8, 10, 12, 13, 14, 15, 16):
        N = 10**e
        err = ln_omega(N, N // 2) - gaussian_ln_omega(N, N // 2)
        print(f"N = 1e{e}: ln_omega - gaussian = {err:+.2e}   ulp(lnGamma(N+1)) = {math.ulp(math.lgamma(N + 1)):.1e}")
