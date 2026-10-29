"""Tests for src/combinatorics.py (log space vs exact integers)."""

import math

import numpy as np
import pytest

from src.combinatorics import (gaussian_ln_omega, largest_float_N, ln_omega, ln_omega_array,
                               plot_macrostate_distribution)


def test_matches_exact_comb():
    for N in range(0, 101):
        for k in range(N + 1):
            assert math.exp(ln_omega(N, k)) == pytest.approx(math.comb(N, k), rel=1e-11)


def test_symmetry_heads_tails():
    for N in (1, 7, 50, 1001):
        for k in range(N + 1):
            assert ln_omega(N, k) == pytest.approx(ln_omega(N, N - k), abs=1e-9)


def test_edges():
    for N in (0, 1, 20, 10**6):
        assert ln_omega(N, 0) == ln_omega(N, N) == 0.0  # a single microstate: all tails / all heads
    for N in (1, 20, 10**6):
        assert ln_omega(N, 1) == pytest.approx(math.log(N))


def test_out_of_range_k():
    for k in (-1, 6):
        with pytest.raises(ValueError):
            ln_omega(5, k)


def test_array_matches_scalar():
    for N in (0, 20, 100, 1500):
        assert np.allclose(ln_omega_array(N), [ln_omega(N, k) for k in range(N + 1)], rtol=1e-12, atol=1e-9)


def test_float_overflow_limit():
    N = largest_float_N()
    assert N == 1029
    float(math.comb(N, N // 2))  # still a finite float64
    with pytest.raises(OverflowError):
        float(math.comb(N + 1, (N + 1) // 2))


def test_gaussian_limit():
    # near the peak the Gaussian approximation of ln Omega is off by O(1/N)
    for N in (10**4, 10**6):
        for dk in (0, math.isqrt(N) // 2):
            k = N // 2 + dk
            assert gaussian_ln_omega(N, k) == pytest.approx(ln_omega(N, k), abs=10 / N)


def test_plot_writes_vector_pdf(tmp_path):
    path = plot_macrostate_distribution(path=tmp_path / "dist.pdf")
    assert path.read_bytes()[:4] == b"%PDF"
