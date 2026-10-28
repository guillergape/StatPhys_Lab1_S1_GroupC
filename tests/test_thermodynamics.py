"""Unit tests for src/thermodynamics.py.

Phase 4 of StatPhys Lab 1: Probabilities and thermodynamic quantities.
Checks:
- Exact fractions against small-N manual values (N = 4, N = 5 Table 1).
- Normalisation: sum_{k=0}^N P(N, k) = 1.
- Binary symmetry: P(N, k) = P(N, N - k).
- Interval cumulative probabilities and boundary conditions.
- Team NIA digits, harmonic mean M, and team N = 100 + M = 121.
- Input validation and exception handling.
- Delta entropy antisymmetry and sign.
"""

import math
import pytest

from src.thermodynamics import (
    delta_entropy,
    harmonic_mean,
    interval_probability,
    ln_omega,
    probability,
    solve_part2_a_to_d,
    team_M,
    team_N,
    team_nia_digits,
)


def test_team_nia_and_system_size():
    """Verify NIA digits, harmonic mean calculation, and N = 100 + M."""
    digits_dict = team_nia_digits()
    assert digits_dict["Guillermo García Pelayo"] == 69
    assert digits_dict["Andrés Mármol del Amo"] == 22
    assert digits_dict["Héctor Armenteros Arauzo"] == 9
    assert digits_dict["Carlos Cordero López"] == 45

    digits = list(digits_dict.values())
    m_float = harmonic_mean(digits)
    # 4 / (1/69 + 1/22 + 1/9 + 1/45) = 20.6952965...
    assert math.isclose(m_float, 20.6952965, rel_tol=1e-5)
    assert team_M() == 21
    assert team_N() == 121


def test_probability_small_n_exact_fractions():
    """Check P(N, k) against exact known fractions for N = 4 and N = 5."""
    # N = 4: 2**4 = 16
    expected_n4 = [1 / 16, 4 / 16, 6 / 16, 4 / 16, 1 / 16]
    for k in range(5):
        assert math.isclose(probability(4, k), expected_n4[k], rel_tol=1e-12)

    # N = 5: Table 1 of lab manual: 1, 5, 10, 10, 5, 1 / 32
    expected_n5 = [1 / 32, 5 / 32, 10 / 32, 10 / 32, 5 / 32, 1 / 32]
    for k in range(6):
        assert math.isclose(probability(5, k), expected_n5[k], rel_tol=1e-12)


@pytest.mark.parametrize("N", [5, 10, 20, 50, 121])
def test_probabilities_sum_to_one(N):
    """Ensure sum_{k=0}^N P(N, k) is normalised to unity."""
    total = sum(probability(N, k) for k in range(N + 1))
    assert math.isclose(total, 1.0, rel_tol=1e-13, abs_tol=1e-13)


@pytest.mark.parametrize("N", [7, 14, 50, 121])
def test_probability_symmetry(N):
    """Verify binary symmetry P(N, k) == P(N, N - k) for all k."""
    for k in range(N // 2 + 1):
        assert math.isclose(probability(N, k), probability(N, N - k), rel_tol=1e-12)


def test_interval_probability():
    """Test interval cumulative probabilities and partition properties."""
    N = 121
    # Full interval must equal 1
    assert math.isclose(interval_probability(N, 0, N), 1.0, rel_tol=1e-13)

    # Single point matches scalar probability
    assert math.isclose(interval_probability(N, 30, 30), probability(N, 30), rel_tol=1e-12)

    # Partition additivity: [0, 60] + [61, 121] = 1
    p_left = interval_probability(N, 0, 60)
    p_right = interval_probability(N, 61, 121)
    assert math.isclose(p_left + p_right, 1.0, rel_tol=1e-13)
    # By symmetry, each half for odd N = 121 must equal 0.5 exactly
    assert math.isclose(p_left, 0.5, rel_tol=1e-12)
    assert math.isclose(p_right, 0.5, rel_tol=1e-12)


def test_solve_part2_answers():
    """Verify specific answers for Part 2 questions (a) through (d)."""
    ans = solve_part2_a_to_d(121)
    assert ans["N"] == 121
    # 2a: P(k=30) is ~ 8.49e-9
    assert math.isclose(ans["2a_p30"], 8.4900937e-9, rel_tol=1e-5)

    # 2b: Degenerate peak at k=60 and k=61
    assert ans["k_peak_low"] == 60
    assert ans["k_peak_high"] == 61
    assert math.isclose(ans["2b_p_peak"], 0.0720893, rel_tol=1e-5)

    # 2c: Heads interval covers > 90%
    assert 0.90 < ans["2c_dp_symmetric"] < 0.96

    # 2d: Tails interval covers > 99.9%
    assert 0.999 < ans["2d_dp_symmetric"] < 1.0


def test_invalid_arguments():
    """Check ValueError on out-of-range arguments."""
    with pytest.raises(ValueError):
        probability(10, -1)
    with pytest.raises(ValueError):
        probability(10, 11)
    with pytest.raises(ValueError):
        interval_probability(10, 5, 4)
    with pytest.raises(ValueError):
        interval_probability(10, -1, 5)
    with pytest.raises(ValueError):
        harmonic_mean([])
    with pytest.raises(ValueError):
        harmonic_mean([10, -2])


def test_delta_entropy():
    """Test entropy differences: antisymmetry, null on self, and positivity from peak."""
    N = 121
    # Identity
    assert math.isclose(delta_entropy(N, 60, 60), 0.0, abs_tol=1e-12)

    # Antisymmetry
    ds_60_30 = delta_entropy(N, 60, 30)
    ds_30_60 = delta_entropy(N, 30, 60)
    assert math.isclose(ds_60_30, -ds_30_60, rel_tol=1e-12)

    # S(60) > S(30), so Delta S = S(60) - S(30) > 0
    assert ds_60_30 > 0.0
