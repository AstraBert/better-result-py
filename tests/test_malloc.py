import tracemalloc
from typing import Never

import pytest

from better_result import Result

from .conftest import ResultWithTb


def raises() -> Never:
    raise ValueError("something went wrong")


def calls_raises() -> Never:
    raises()


def fn() -> Never:
    calls_raises()


@pytest.fixture(autouse=True)
def reset_tracemalloc():
    tracemalloc.start()
    yield
    tracemalloc.stop()
    tracemalloc.clear_traces()


def measure_allocs(fn, n=10_000):
    tracemalloc.clear_traces()
    for _ in range(n):
        fn()
    snapshot = tracemalloc.take_snapshot()
    return sum(stat.size for stat in snapshot.statistics("lineno"))


def test_malloc_comparison() -> None:
    no_tb = measure_allocs(lambda: Result(fn))
    with_tb = measure_allocs(lambda: ResultWithTb(fn))

    print(f"\nNo Traceback:   {no_tb / 1024:.2f} KB")
    print(f"With Traceback: {with_tb / 1024:.2f} KB")
    print(f"Delta (with - no):   {(with_tb - no_tb) / 1024:.2f} KB")

    assert no_tb < with_tb
