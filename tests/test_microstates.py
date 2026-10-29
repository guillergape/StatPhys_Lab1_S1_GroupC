"""Tests for src/microstates.py."""

import math
import tracemalloc

from src.microstates import (macrostate_counts, macrostate_counts_fast, macrostates_table,
                             microstates, peak_memory, time_count, to_string)


def test_counts_sum_to_2_power_N():
    for N in range(0, 13):
        assert sum(macrostate_counts(N)) == 2**N


def test_counts_are_binomial():
    for N in range(0, 16):
        assert macrostate_counts(N) == [math.comb(N, k) for k in range(N + 1)]


def test_table_1_of_the_manual():
    assert macrostate_counts(5) == [1, 5, 10, 10, 5, 1]


def test_fast_matches_generator():
    for N in (1, 7, 15):
        assert macrostate_counts_fast(N, workers=1) == macrostate_counts(N)
    # more states than one numpy block, split over 3 processes
    assert macrostate_counts_fast(23, workers=3) == [math.comb(23, k) for k in range(24)]


def test_every_microstate_listed_once():
    table = macrostates_table(7)
    states = [s for row in table for s in row]
    assert len(states) == len(set(states)) == 128
    assert all(s.count("H") == k for k, row in enumerate(table) for s in row)


def test_bits_to_string():
    assert to_string(0b00101, 5) == "HTHTT"
    assert list(microstates(2)) == [0, 1, 2, 3]


def test_timing_and_memory_are_measured_apart():
    # timing must not run under tracemalloc, which slows pure Python ~9x
    seen = []
    time_count(lambda N: seen.append(tracemalloc.is_tracing()), 10)
    peak_memory(lambda N: seen.append(tracemalloc.is_tracing()), 10)
    assert seen == [False, True] and not tracemalloc.is_tracing()
    # one numpy block (2^22 states) costs the same memory whatever N is
    assert 30 < peak_memory(lambda N: macrostate_counts_fast(N, workers=1), 22) < 200
