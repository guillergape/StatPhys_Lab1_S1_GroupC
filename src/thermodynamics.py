"""Probabilities, Boltzmann entropy and thermodynamic-limit estimates.

Phase 4 of StatPhys Lab 1 (Héctor Armenteros).
System size N = 100 + M where M is the harmonic average of the last two digits
of the team members' NIAs:
- Guillermo García Pelayo: 69
- Andrés Mármol del Amo: 22
- Héctor Armenteros Arauzo: 09 (treated as 9)
- Carlos Cordero López: 45

Harmonic mean: M = 4 / (1/69 + 1/22 + 1/9 + 1/45) = 20.695297... -> rounded to 21.
System size: N = 100 + 21 = 121.
"""

from __future__ import annotations

import math
from typing import Any, Mapping, Sequence

# Fallback ln_omega if Phase 3 (src.combinatorics) has not been merged into main yet.
try:
    from src.combinatorics import ln_omega as _src_ln_omega

    if abs(_src_ln_omega(4, 2) - math.log(6.0)) < 1e-10:
        ln_omega = _src_ln_omega
    else:
        raise ImportError
except (ImportError, AttributeError, Exception):
    def ln_omega(N: int, k: int) -> float:
        """ln Omega(N, k) using math.lgamma: ln Gamma(N+1) - ln Gamma(k+1) - ln Gamma(N-k+1)."""
        if not (0 <= k <= N):
            raise ValueError(f"need 0 <= k <= N, got N={N}, k={k}")
        return math.lgamma(N + 1) - math.lgamma(k + 1) - math.lgamma(N - k + 1)


def harmonic_mean(digits: Sequence[float]) -> float:
    """Compute the harmonic mean H = len(digits) / sum(1 / d)."""
    if not digits:
        raise ValueError("Cannot compute harmonic mean of an empty sequence")
    if any(d <= 0 for d in digits):
        raise ValueError(f"Harmonic mean requires positive values, got {digits}")
    return len(digits) / sum(1.0 / float(d) for d in digits)


def team_nia_digits() -> dict[str, int]:
    """Return the team members and the last two digits of their NIAs."""
    return {
        "Guillermo García Pelayo": 69,
        "Andrés Mármol del Amo": 22,
        "Héctor Armenteros Arauzo": 9,
        "Carlos Cordero López": 45,
    }


def team_M() -> int:
    """Return the integer M from the harmonic mean of the team's NIA digits.

    Exact value: 4 / (1/69 + 1/22 + 1/9 + 1/45) = 20.6952965...
    Rounded to nearest integer: 21.
    """
    digits = list(team_nia_digits().values())
    return round(harmonic_mean(digits))


def team_N() -> int:
    """Return the team system size N = 100 + M = 121 coins."""
    return 100 + team_M()


def probability(N: int, k: int) -> float:
    """Macrostate probability P(N, k) = Omega(N, k) / 2**N computed in log space."""
    if not (0 <= k <= N):
        raise ValueError(f"need 0 <= k <= N, got N={N}, k={k}")
    ln_p = ln_omega(N, k) - float(N) * math.log(2.0)
    return math.exp(ln_p)


def interval_probability(N: int, k1: int, k2: int) -> float:
    """Cumulative probability sum_{k=k1}^{k2} P(N, k) for k in [k1, k2]."""
    if not (0 <= k1 <= k2 <= N):
        raise ValueError(f"need 0 <= k1 <= k2 <= N, got N={N}, k1={k1}, k2={k2}")
    return sum(probability(N, k) for k in range(k1, k2 + 1))


def delta_entropy(N: int, k1: int, k2: int) -> float:
    """Dimensionless entropy change Delta S / k_B = ln Omega(N, k1) - ln Omega(N, k2)."""
    if not (0 <= k1 <= N and 0 <= k2 <= N):
        raise ValueError(f"k1 and k2 must be in [0, N], got N={N}, k1={k1}, k2={k2}")
    return ln_omega(N, k1) - ln_omega(N, k2)


def solve_part2_a_to_d(N: int | None = None) -> dict[str, Any]:
    """Calculate and return numerical answers for Part 2 questions (a) through (d)."""
    if N is None:
        N = team_N()

    # 2a: P(k = 30)
    p_30 = probability(N, 30)

    # 2b: P(k = N/2), the most probable macrostate
    # For odd N, N/2 is half-integer (e.g. 60.5). Peak is degenerate at k = floor(N/2) and ceil(N/2).
    k_peak_low = N // 2
    k_peak_high = (N + 1) // 2
    p_peak = probability(N, k_peak_low)  # equals probability(N, k_peak_high) by symmetry

    # 2c: Delta P for k1 = N/2 - 10, k2 = N/2 + 10 heads
    # Symmetric continuous interval [N/2 - 10, N/2 + 10] covers integers:
    k1_sym = math.ceil(N / 2.0 - 10.0)
    k2_sym = math.floor(N / 2.0 + 10.0)
    dp_c_symmetric = interval_probability(N, k1_sym, k2_sym)
    dp_c_mode = interval_probability(N, k_peak_low - 10, k_peak_low + 10)

    # 2d: Delta P for t1 = N/2 - 20, t2 = N/2 + 20 tails
    # Tails t = N - k. By symmetry, P(tails = t) == P(heads = t).
    t1_sym = math.ceil(N / 2.0 - 20.0)
    t2_sym = math.floor(N / 2.0 + 20.0)
    dp_d_symmetric = interval_probability(N, t1_sym, t2_sym)
    dp_d_mode = interval_probability(N, k_peak_low - 20, k_peak_low + 20)

    return {
        "N": N,
        "k_peak_low": k_peak_low,
        "k_peak_high": k_peak_high,
        "2a_p30": p_30,
        "2b_p_peak": p_peak,
        "2c_range_sym": (k1_sym, k2_sym),
        "2c_dp_symmetric": dp_c_symmetric,
        "2c_dp_mode": dp_c_mode,
        "2d_range_sym": (t1_sym, t2_sym),
        "2d_dp_symmetric": dp_d_symmetric,
        "2d_dp_mode": dp_d_mode,
    }



# --- Phase 6 (Andrés): entropy and thermodynamic implications, Part 2 e-i ---

K_B = 1.380649e-23  # Boltzmann constant in J/K (exact since the 2019 SI redefinition)
AGE_OF_UNIVERSE_S = 13.787e9 * 365.25 * 86400  # 13.787 +- 0.020 Gyr (Planck 2018), in seconds


def likelihood_ratio(N: int, k1: int, k2: int) -> float:
    """How many times more likely macrostate k1 is than k2: P(k1) / P(k2) = exp(Delta S / k_B)."""
    return math.exp(delta_entropy(N, k1, k2))


def waiting_time(N: int, k: int, tosses_per_second: float = 1.0) -> float:
    """Mean time (s) until a toss of all N coins lands exactly on k heads.

    Each toss is an independent trial with success probability P(N, k), so the number of
    tosses until the first success is geometric with mean 1 / P(N, k).
    """
    return 1.0 / (probability(N, k) * tosses_per_second)


def solve_part2_e_to_i(N: int | None = None) -> dict[str, Any]:
    """Numerical answers for Part 2 questions (e) through (i).

    For odd N, "N/2" is the degenerate peak k = N//2 = (N+1)//2 (same Omega), and
    "N/2 + d" is taken as N//2 + d; the other neighbour (N+1)//2 + d is returned too.
    "N/2 - d" is (N+1)//2 - d, the mirror image of N//2 + d (same Omega).
    """
    if N is None:
        N = team_N()
    lo, hi = N // 2, (N + 1) // 2
    M = N - 100

    def ds(k1: int, k2: int) -> tuple[float, float]:
        s = delta_entropy(N, k1, k2)
        return s, s * K_B

    return {
        "N": N,
        "k_half": (lo, hi),
        "2e": {"k1": lo + 25, "k2": lo, "dS": ds(lo + 25, lo), "dS_alt": ds(hi + 25, lo)},
        "2f": {"k1": lo + 10, "k2": lo, "dS": ds(lo + 10, lo), "dS_alt": ds(hi + 10, lo)},
        "2g": {"k1": lo, "k2": 20, "dS": ds(lo, 20)},
        "2h": {"P8": probability(N, 8), "wait_s": waiting_time(N, 8),
               "wait_over_universe_age": waiting_time(N, 8) / AGE_OF_UNIVERSE_S,
               "P_le_8": interval_probability(N, 0, 8)},
        "2i": {"as_written": {k: likelihood_ratio(N, lo, k) for k in (M - 10, M + 10)},
               "half_N_reading": {k: likelihood_ratio(N, lo, k) for k in (hi - 10, lo + 10)}},
    }


# --- Phase 7 (Andrés): Second Law and the large-N limit, Part 2 j-k ---
# For N ~ 1e23, lgamma(N + 1) has a rounding error of ~1e9 and k = N/2 + 25 is not even
# representable as a float, so everything below works with offsets d = k - N/2 and with
# entropy differences taken analytically, never as a difference of two huge numbers.

def ln_omega_small_k(N: float, k: int) -> float:
    """ln Omega(N, k) for k << N: k ln N - ln k! - k (k - 1) / (2N), from ln(N - i) = ln N - i/N."""
    return k * math.log(N) - math.lgamma(k + 1) - k * (k - 1) / (2 * N)


def ln_probability_small_k(N: float, k: int) -> float:
    """ln P(N, k) = ln Omega(N, k) - N ln 2 for k << N."""
    return ln_omega_small_k(N, k) - N * math.log(2)


def peak_probability(N: float) -> float:
    """P(N, N/2) ~ sqrt(2 / (pi N)) for large N (Stirling)."""
    return math.sqrt(2 / (math.pi * N))


def delta_entropy_near_peak(N: float, d1: float, d2: float) -> float:
    """Delta S / k_B between k1 = N/2 + d1 and k2 = N/2 + d2 in the Gaussian limit: -2 (d1^2 - d2^2) / N."""
    return -2 * (d1 * d1 - d2 * d2) / N


def interval_probability_gaussian(N: float, d_lo: float, d_hi: float) -> float:
    """P(d_lo <= k - N/2 <= d_hi) in the Gaussian limit (sigma = sqrt(N)/2, continuity correction 1/2)."""
    scale = math.sqrt(N / 2)  # sigma * sqrt(2)
    return 0.5 * (math.erf((d_hi + 0.5) / scale) - math.erf((d_lo - 0.5) / scale))


def tail_probability_exact(N: int, d: float) -> float:
    """P(|k - N/2| >= d) as an exact sum over k (for N small enough to sum)."""
    c = N / 2
    inner_lo, inner_hi = math.floor(c - d) + 1, math.ceil(c + d) - 1  # the k with |k - N/2| < d
    if inner_lo > inner_hi:
        return 1.0
    return 1.0 - interval_probability(N, max(inner_lo, 0), min(inner_hi, N))


def ln_tail_probability(N: float, d: float) -> float:
    """ln P(|k - N/2| >= d) in the Gaussian limit, = ln erfc(x) with x = (D - 1/2) / (sigma sqrt 2).

    The distances |k - N/2| live on a lattice: integers for even N, half-integers for odd N.
    d is first rounded up to the nearest lattice distance D, then the continuity correction 1/2
    is applied (as in interval_probability_gaussian). erfc underflows for x > ~27, so beyond that
    the asymptotic ln erfc(x) ~ -x^2 - ln(x sqrt(pi)) is used.
    """
    offset = 0.5 if N % 2 else 0.0
    D = math.ceil(d - offset) + offset
    if D <= offset:  # every macrostate is at least this far from N/2
        return 0.0
    x = (D - 0.5) / math.sqrt(N / 2)
    if x < 26:
        return math.log(math.erfc(x))
    return -x * x - math.log(x * math.sqrt(math.pi))


def solve_part2_k(N: float = 1e23) -> dict[str, Any]:
    """Questions (a)-(i) re-evaluated in the large-N limit (question k). Tiny or huge numbers as ln or log10."""
    log10 = math.log(10)
    ln_peak_omega = N * math.log(2) + 0.5 * math.log(2 / (math.pi * N))
    return {
        "N": N,
        "sigma": math.sqrt(N) / 2,
        "2a_log10_P30": ln_probability_small_k(N, 30) / log10,
        "2b_P_peak": peak_probability(N),
        "2c_dP": interval_probability_gaussian(N, -10, 10),
        "2d_dP": interval_probability_gaussian(N, -20, 20),
        "2e_dS_kB": delta_entropy_near_peak(N, 25, 0),
        "2f_dS_kB": delta_entropy_near_peak(N, 10, 0),
        "2g_dS_kB": ln_peak_omega - ln_omega_small_k(N, 20),
        "2g_dS_JK": K_B * (ln_peak_omega - ln_omega_small_k(N, 20)),
        "2h_log10_wait_s": -ln_probability_small_k(N, 8) / log10,
        "2i_log10_ratio_k11": (ln_peak_omega - ln_omega_small_k(N, 11)) / log10,
        "2i_ratio_half_N_pm10": math.exp(-delta_entropy_near_peak(N, 10, 0)),
        "2j_ln_P_1percent": ln_tail_probability(N, 0.01 * N),
    }


if __name__ == "__main__":
    results = solve_part2_a_to_d()
    print(f"Team N: {results['N']} (M = {team_M()})")
    print(f"2a: P(k=30) = {results['2a_p30']:.6e}")
    print(f"2b: Most probable macrostate k = {results['k_peak_low']}, {results['k_peak_high']}:")
    print(f"    P(k={results['k_peak_low']}) = {results['2b_p_peak']:.6f}")
    print(f"2c: Delta P (heads in {results['2c_range_sym']}): {results['2c_dp_symmetric']:.6f} "
          f"(mode range [{results['k_peak_low']-10}, {results['k_peak_low']+10}]: {results['2c_dp_mode']:.6f})")
    print(f"2d: Delta P (tails in {results['2d_range_sym']}): {results['2d_dp_symmetric']:.6f} "
          f"(mode range [{results['k_peak_low']-20}, {results['k_peak_low']+20}]: {results['2d_dp_mode']:.6f})")
    r = solve_part2_e_to_i()
    for q in ("2e", "2f", "2g"):
        d = r[q]
        alt = f"   (k1 = {d['k1'] + 1}: {d['dS_alt'][0]:+.4f} k_B)" if "dS_alt" in d else ""
        print(f"{q}: k1 = {d['k1']}, k2 = {d['k2']}: dS = {d['dS'][0]:+.4f} k_B = {d['dS'][1]:+.4e} J/K{alt}")
    h = r["2h"]
    print(f"2h: P(k=8) = {h['P8']:.6e}, mean wait = {h['wait_s']:.4e} s = "
          f"{h['wait_over_universe_age']:.3e} ages of the Universe; P(k<=8) = {h['P_le_8']:.6e}")
    for reading, ratios in r["2i"].items():
        print(f"2i ({reading}): " + ", ".join(f"P({r['k_half'][0]})/P({k}) = {v:.6e}" for k, v in ratios.items()))
    big = solve_part2_k()
    print(f"2k (N = {big['N']:.0e}): " + ", ".join(f"{key} = {v:.4e}" for key, v in big.items() if key != "N"))
    for n in (121, 10**4):
        print(f"2j: P(|k - N/2| >= 1% of N), N = {n}: P = {tail_probability_exact(n, 0.01 * n):.6f} (exact sum), "
              f"Gaussian {math.exp(ln_tail_probability(n, 0.01 * n)):.6f}")
    print(f"2j: P(|k - N/2| >= 1% of N), N = 1e23: ln P = {ln_tail_probability(1e23, 1e21):.4e} (Gaussian)")
    print(f"2j: P(|k - 60.5| >= 24.5), N = 121: {tail_probability_exact(121, 24.5):.6e} (exact sum)")
