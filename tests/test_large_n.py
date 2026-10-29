"""Tests for the Phase 7 large-N functions in src/thermodynamics.py (Part 2 j-k)."""

import math

import pytest

from src.combinatorics import ln_omega
from src.thermodynamics import (K_B, delta_entropy, delta_entropy_near_peak, interval_probability,
                                interval_probability_gaussian, ln_omega_small_k, ln_tail_probability,
                                tail_probability_exact,
                                peak_probability, probability, solve_part2_k)


def test_small_k_expansion_matches_exact():
    N = 10**6
    for k in (0, 1, 8, 20, 30):
        assert ln_omega_small_k(N, k) == pytest.approx(ln_omega(N, k), abs=1e-6)


def test_peak_probability_matches_exact():
    for N in (10**4, 10**6):
        assert peak_probability(N) == pytest.approx(probability(N, N // 2), rel=1e-4)


def test_gaussian_interval_matches_exact():
    N, c = 10**4, 5000
    for w in (10, 20, 100):
        exact = interval_probability(N, c - w, c + w)
        assert interval_probability_gaussian(N, -w, w) == pytest.approx(exact, rel=1e-3)


def test_entropy_near_peak_matches_exact():
    N, c = 10**6, 500000
    for d in (10, 25, 100):
        assert delta_entropy_near_peak(N, d, 0) == pytest.approx(delta_entropy(N, c + d, c), abs=1e-6)


def test_tail_probability():
    N, c, d = 10**4, 5000, 100
    exact = 1 - interval_probability(N, c - d + 1, c + d - 1)
    assert math.exp(ln_tail_probability(N, d)) == pytest.approx(exact, rel=1e-3)
    # the asymptotic branch joins the erfc branch smoothly at x = 26
    N = 1e6
    below, above = ln_tail_probability(N, 25.99 * math.sqrt(N / 2) + 0.5), ln_tail_probability(N, 26.01 * math.sqrt(N / 2) + 0.5)
    assert above < below and below - above == pytest.approx(2 * 26 * 0.02, rel=1e-2)


def test_thermodynamic_limit_answers():
    r = solve_part2_k(1e23)
    assert r["sigma"] == pytest.approx(1.5811e11, rel=1e-4)
    assert r["2b_P_peak"] == pytest.approx(math.sqrt(2 / (math.pi * 1e23)))
    # fixed-width intervals around the peak hold a vanishing fraction of the states: ~ (2w + 1) P_peak
    assert r["2c_dP"] == pytest.approx(21 * r["2b_P_peak"], rel=1e-6)
    assert r["2d_dP"] == pytest.approx(41 * r["2b_P_peak"], rel=1e-6)
    # fixed offsets from the peak cost no entropy; the ordered state costs N k_B ln 2
    assert abs(r["2e_dS_kB"]) < 1e-19 and abs(r["2f_dS_kB"]) < 1e-19
    assert r["2g_dS_JK"] == pytest.approx(K_B * 1e23 * math.log(2), rel=1e-9)
    assert r["2a_log10_P30"] == pytest.approx(-1e23 * math.log10(2), rel=1e-9)
    assert r["2i_ratio_half_N_pm10"] == pytest.approx(1.0, abs=1e-15)


def test_tail_probability_exact_sum():
    # N = 121: |k - 60.5| >= 1.21 leaves out only k = 60, 61
    assert tail_probability_exact(121, 1.21) == pytest.approx(1 - probability(121, 60) - probability(121, 61))
    assert tail_probability_exact(121, 0) == 1.0
    assert tail_probability_exact(4, 2) == pytest.approx(2 / 16)  # k = 0 or 4


def test_tail_probability_odd_n_lattice():
    # odd N: distances are half-integers, so d = 1.21 must count from 1.5, not 1.21 (review of PR #7)
    for d, rel in ((1.21, 1e-3), (3.0, 1e-3), (10.0, 1e-2)):  # the old cutoff was 5 % off at d = 1.21
        assert math.exp(ln_tail_probability(121, d)) == pytest.approx(tail_probability_exact(121, d), rel=rel)
    for N in (121, 10**4):
        assert ln_tail_probability(N, 0) == 0.0  # P(|k - N/2| >= 0) = 1
