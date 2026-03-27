import pytest

from better_result.result import BaseResult, Err, ExpectError, Ok, ResultError


def always_success(i: int) -> BaseResult[int]:
    return Ok(i + i)


def sometimes_success(i: int) -> BaseResult[float]:
    if i == 0:
        return Err("Cannot divide by zero")
    else:
        return Ok(i / i)


def always_failure() -> BaseResult[float]:
    return Err("Impossible to perform the requested operation")


def uses_exception(x: int, y: int) -> BaseResult[float]:
    if y == 0:
        return Err(err=ZeroDivisionError("Cannot divide by zero"))
    else:
        return Ok(x / y)


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        (0, 0),
        (1, 2),
        (2, 4),
    ],
)
def test_alwyas_success(arg: int, expected: int) -> None:
    result = always_success(arg)
    assert result.is_ok()
    assert not result.is_err()
    assert result.ok == expected
    assert result.unwrap() == expected
    assert result.unwrap_or(-1) == expected
    assert result.expect(f"should return {expected}") == expected


@pytest.mark.parametrize(
    ("arg", "is_err"),
    [
        (0, True),
        (1, False),
        (2, False),
    ],
)
def test_sometimes_success(arg: int, is_err: bool) -> None:
    result = sometimes_success(arg)
    assert result.is_ok() == (not is_err)
    assert result.is_err() == is_err
    if not is_err:
        expected = arg / arg
        assert result.ok == expected
        assert result.unwrap() == expected
        assert result.unwrap_or(-1) == expected
        assert result.expect(f"Shoudl return {expected}") == expected
    else:
        with pytest.raises(ResultError, match="Cannot divide by zero"):
            result.unwrap()
        assert result.unwrap_or(-1) == -1
        with pytest.raises(ExpectError, match="Should return something") as exc_info:
            result.expect("Should return something")
        assert exc_info.value.__cause__ is not None
        assert isinstance(exc_info.value.__cause__, ResultError)


def test_always_failure() -> None:
    result = always_failure()
    assert result.is_err()
    assert not result.is_ok()
    with pytest.raises(
        ResultError, match="Impossible to perform the requested operation"
    ):
        result.unwrap()
    assert result.unwrap_or(-1) == -1
    with pytest.raises(ExpectError, match="Should return something") as exc_info:
        result.expect("Should return something")
    assert exc_info.value.__cause__ is not None
    assert isinstance(exc_info.value.__cause__, ResultError)


@pytest.mark.parametrize(
    ("x", "y", "is_err"),
    [
        (1, 0, True),
        (1, 1, False),
    ],
)
def test_uses_exception(x: int, y: int, is_err: bool) -> None:
    result = uses_exception(x, y)
    assert result.is_err() == is_err
    assert result.is_ok() == (not is_err)
    if is_err:
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            result.unwrap()
        assert result.unwrap_or(-1) == -1
        with pytest.raises(ExpectError, match="Should return something") as exc_info:
            result.expect("Should return something")
        assert exc_info.value.__cause__ is not None
        assert isinstance(exc_info.value.__cause__, ZeroDivisionError)
    else:
        expected = x / y
        assert result.unwrap() == expected
        assert result.unwrap_or(-1) == expected
        assert result.expect(f"Should return {expected}") == expected
