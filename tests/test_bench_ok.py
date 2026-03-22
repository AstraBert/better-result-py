from pytest_benchmark.fixture import BenchmarkFixture

from better_result import Result

from .conftest import ResultWithTb


def returns() -> int:
    return 0


def test_bench_success_no_tb(benchmark: BenchmarkFixture) -> None:
    benchmark(Result, returns)


def test_bench_success_with_tb(benchmark: BenchmarkFixture) -> None:
    benchmark(ResultWithTb, returns)
