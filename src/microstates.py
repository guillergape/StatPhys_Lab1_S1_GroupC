"""Microstate enumeration (bitwise shifts + generators).

A microstate of N coins is an integer s in 0 ... 2**N - 1: bit i of s is coin i
(1 = heads, 0 = tails), so the macrostate k (number of heads) is s.bit_count().
"""

import os
import time
import tracemalloc
from collections.abc import Iterator
from concurrent.futures import ProcessPoolExecutor

import numpy as np

CHUNK = 1 << 22  # states per numpy block: ~38 MB per block, whatever N is


def microstates(N: int) -> Iterator[int]:
    """Yield every microstate of N coins, one at a time (constant memory in N)."""
    yield from range(1 << N)


def to_string(state: int, N: int) -> str:
    """Microstate as a string of H/T, coin 0 first (e.g. 0b00101, N=5 -> 'HTHTT')."""
    return "".join("H" if state >> i & 1 else "T" for i in range(N))


def macrostate_counts(N: int) -> list[int]:
    """Omega(N, k) for k = 0 ... N, counting the heads of every microstate."""
    counts = [0] * (N + 1)
    for s in microstates(N):
        counts[s.bit_count()] += 1
    return counts


def macrostates_table(N: int) -> list[list[str]]:
    """Every microstate as an H/T string, grouped by macrostate: table[k] = states with k heads."""
    table = [[] for _ in range(N + 1)]
    for s in microstates(N):
        table[s.bit_count()].append(to_string(s, N))
    return table


def _count_block(N: int, start: int, stop: int) -> np.ndarray:
    """Heads histogram of the microstates start ... stop - 1, one numpy block at a time."""
    counts = np.zeros(N + 1, dtype=np.int64)
    for a in range(start, stop, CHUNK):
        states = np.arange(a, min(a + CHUNK, stop), dtype=np.uint64)
        counts += np.bincount(np.bitwise_count(states), minlength=N + 1)
    return counts


def macrostate_counts_fast(N: int, workers: int | None = None) -> list[int]:
    """Same result as macrostate_counts, but every state is generated and counted
    with numpy (popcount in C) and the range 0 ... 2**N - 1 is split among CPU cores.
    Still a full enumeration: each of the 2**N states is built and its heads counted.
    """
    total = 1 << N
    workers = workers or os.cpu_count() or 1
    if total <= CHUNK or workers == 1:
        return _count_block(N, 0, total).tolist()
    step = -(-total // workers)
    bounds = [(N, a, min(a + step, total)) for a in range(0, total, step)]
    with ProcessPoolExecutor(workers) as pool:
        return sum(pool.map(_count_block, *zip(*bounds))).tolist()


def measure(count, N: int) -> tuple[float, float]:
    """Wall time (s) and peak traced memory (MB) of count(N), main process only."""
    tracemalloc.start()
    t0 = time.perf_counter()
    count(N)
    t = time.perf_counter() - t0
    peak = tracemalloc.get_traced_memory()[1] / 1e6
    tracemalloc.stop()
    return t, peak


def benchmark(count=macrostate_counts_fast, N0: int = 16, budget: float = 300.0) -> list[tuple[int, float, float]]:
    """Run count(N) for N = N0, N0+1, ... while the next N is predicted to fit in `budget`
    seconds (time doubles with each extra coin). Returns rows (N, seconds, peak MB) and prints them.
    """
    rows, N = [], N0
    while True:
        t, mb = measure(count, N)
        rows.append((N, t, mb))
        print(f"N = {N:2d}   {t:9.3f} s   {t / 2**N * 1e9:6.2f} ns/state   peak {mb:7.1f} MB", flush=True)
        if 2 * t > budget:
            return rows
        N += 1


if __name__ == "__main__":
    benchmark()
