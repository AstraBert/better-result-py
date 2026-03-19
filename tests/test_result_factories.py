import asyncio
from types import NoneType
from typing import Type

import pytest

from better_result import AsyncResult, Result
from better_result.result import Unset, UnsetType


def sync_always_ok(x: int) -> int:
    return x + x


def sync_sometimes_err(x: int) -> float:
    return x / x


def sync_always_error(x: int) -> float:
    return x / 0


async def async_always_ok(x: int) -> int:
    await asyncio.sleep(0.01)
    return x + x


async def async_sometimes_err(x: int) -> float:
    await asyncio.sleep(0.01)
    return x / x


async def async_always_error(x: int) -> float:
    await asyncio.sleep(0.01)
    return x / 0


@pytest.mark.parametrize(
    ("x", "is_ok", "ok", "err"),
    [
        (0, True, 0, None),
        (1, True, 2, None),
        (2, True, 4, None),
    ],
)
def test_result_ok(x: int, is_ok: bool, ok: int, err: Exception | None) -> None:
    result = Result(sync_always_ok, x)
    assert result.is_ok() == is_ok
    assert result.is_err() == (not is_ok)
    assert result.ok == ok
    assert result.err == err


@pytest.mark.parametrize(
    ("x", "is_ok", "ok", "err"),
    [
        (0, False, Unset, ZeroDivisionError),
        (1, True, 1, NoneType),
        (2, True, 1, NoneType),
    ],
)
def test_result_ok_and_err(
    x: int, is_ok: bool, ok: int, err: Type[Exception] | Type[NoneType]
) -> None:
    result = Result(sync_sometimes_err, x)
    assert result.is_ok() == is_ok
    assert result.is_err() == (not is_ok)
    assert result.ok == ok
    assert isinstance(result.err, err)


@pytest.mark.parametrize(
    ("x", "is_ok", "ok", "err"),
    [
        (0, False, Unset, ZeroDivisionError),
        (1, False, Unset, ZeroDivisionError),
        (2, False, Unset, ZeroDivisionError),
    ],
)
def test_result_err(x: int, is_ok: bool, ok: UnsetType, err: Type[Exception]) -> None:
    result = Result(sync_always_error, x)
    assert result.is_ok() == is_ok
    assert result.is_err() == (not is_ok)
    assert result.ok == ok
    assert isinstance(result.err, err)


@pytest.mark.parametrize(
    ("x", "is_ok", "ok", "err"),
    [
        (0, True, 0, None),
        (1, True, 2, None),
        (2, True, 4, None),
    ],
)
@pytest.mark.asyncio
async def test_async_result_ok(
    x: int, is_ok: bool, ok: int, err: Exception | None
) -> None:
    result = await AsyncResult(async_always_ok, x)
    assert result.is_ok() == is_ok
    assert result.is_err() == (not is_ok)
    assert result.ok == ok
    assert result.err == err


@pytest.mark.parametrize(
    ("x", "is_ok", "ok", "err"),
    [
        (0, False, Unset, ZeroDivisionError),
        (1, True, 1, NoneType),
        (2, True, 1, NoneType),
    ],
)
@pytest.mark.asyncio
async def test_async_result_ok_and_err(
    x: int, is_ok: bool, ok: int, err: Type[Exception] | Type[NoneType]
) -> None:
    result = await AsyncResult(async_sometimes_err, x)
    assert result.is_ok() == is_ok
    assert result.is_err() == (not is_ok)
    assert result.ok == ok
    assert isinstance(result.err, err)


@pytest.mark.parametrize(
    ("x", "is_ok", "ok", "err"),
    [
        (0, False, Unset, ZeroDivisionError),
        (1, False, Unset, ZeroDivisionError),
        (2, False, Unset, ZeroDivisionError),
    ],
)
@pytest.mark.asyncio
async def test_async_result_err(
    x: int, is_ok: bool, ok: UnsetType, err: Type[Exception]
) -> None:
    result = await AsyncResult(async_always_error, x)
    assert result.is_ok() == is_ok
    assert result.is_err() == (not is_ok)
    assert result.ok == ok
    assert isinstance(result.err, err)
