from typing import Never

from pytest_benchmark.fixture import BenchmarkFixture

from better_result import Result

from .conftest import ResultWithTb


def raises() -> Never:
    raise ValueError("Something went wrong")


def test_bench_err_no_tb(benchmark: BenchmarkFixture) -> None:
    benchmark(Result, raises)


def test_bench_err_with_tb(benchmark: BenchmarkFixture) -> None:
    benchmark(ResultWithTb, raises)
