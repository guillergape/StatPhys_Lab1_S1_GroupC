"""Tests for the Phase 6 functions in src/thermodynamics.py (Part 2 e-i)."""

import math

import pytest

from src.thermodynamics import (AGE_OF_UNIVERSE_S, K_B, delta_entropy, likelihood_ratio, probability,
                                solve_part2_e_to_i, waiting_time)


def test_likelihood_ratio_is_probability_ratio():
    for N, k1, k2 in ((10, 5, 2), (121, 60, 11), (121, 85, 60)):
        assert likelihood_ratio(N, k1, k2) == pytest.approx(probability(N, k1) / probability(N, k2), rel=1e-12)
        assert math.log(likelihood_ratio(N, k1, k2)) == pytest.approx(delta_entropy(N, k1, k2), abs=1e-12)


def test_likelihood_ratio_exact_small_n():
    # Omega(6, 3) / Omega(6, 1) = 20 / 6
    assert likelihood_ratio(6, 3, 1) == pytest.approx(20 / 6, rel=1e-12)


def test_waiting_time_is_inverse_probability():
    assert waiting_time(3, 0) == pytest.approx(8.0)  # P(all tails) = 1/8 -> 8 tosses on average
    assert waiting_time(3, 0, tosses_per_second=2.0) == pytest.approx(4.0)
    assert waiting_time(121, 8) == pytest.approx(1 / probability(121, 8), rel=1e-12)


def test_age_of_universe_in_seconds():
    assert AGE_OF_UNIVERSE_S == pytest.approx(4.35e17, rel=1e-2)


def test_entropy_answers_team_n():
    r = solve_part2_e_to_i(121)
    assert r["k_half"] == (60, 61)
    # moving away from the peak lowers the entropy; moving towards it raises it
    assert r["2e"]["dS"][0] < r["2f"]["dS"][0] < 0 < r["2g"]["dS"][0]
    for q in ("2e", "2f", "2g"):
        s_kb, s_jk = r[q]["dS"]
        assert s_jk == pytest.approx(s_kb * K_B)
    # the farther neighbour of a half-integer target has the lower entropy
    assert r["2e"]["dS_alt"][0] < r["2e"]["dS"][0]
    assert r["2h"]["wait_over_universe_age"] > 1
    assert r["2h"]["P_le_8"] > r["2h"]["P8"]


def test_half_n_reading_is_symmetric():
    # k = 51 and k = 70 are mirror images for N = 121 (51 + 70 = N), so their ratios match
    ratios = solve_part2_e_to_i(121)["2i"]["half_N_reading"]
    assert list(ratios) == [51, 70]
    assert ratios[51] == pytest.approx(ratios[70], rel=1e-12)


def test_even_n_degenerate_peak_collapses():
    r = solve_part2_e_to_i(150)  # M = 50
    assert r["k_half"] == (75, 75)
    assert r["2e"]["dS"] == r["2e"]["dS_alt"]
