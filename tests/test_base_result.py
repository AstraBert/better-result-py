import pytest

from better_result.result import BaseResult, ExpectError, Unset, UnsetError, UnsetType


def test_init_ok() -> None:
    result = BaseResult[int](ok=1, err=None)
    assert result.ok == 1
    assert result.err is None
    assert result.is_ok()
    assert not result.is_err()


def test_init_err() -> None:
    result = BaseResult[int](ok=Unset, err=ValueError("this is an error"))
    assert isinstance(result.ok, UnsetType)
    assert isinstance(result.err, ValueError)
    assert str(result.err) == "this is an error"


def test_unwrap_ok() -> None:
    result = BaseResult[int](ok=1, err=None)
    output = result.unwrap()
    assert output == 1


def test_unwrap_unset() -> None:
    result = BaseResult[int](ok=Unset, err=None)
    with pytest.raises(UnsetError, match="Result is Unset even if no error was raised"):
        result.unwrap()


def test_unwrap_err() -> None:
    result = BaseResult[int](ok=Unset, err=ValueError("this is an error"))
    with pytest.raises(ValueError, match="this is an error"):
        result.unwrap()


def test_unwrap_or_ok() -> None:
    result = BaseResult[int](ok=1, err=None)
    output = result.unwrap_or(0)
    assert output == 1


def test_unwrap_or_unset() -> None:
    result = BaseResult[int](ok=Unset, err=None)
    output = result.unwrap_or(0)
    assert output == 0


def test_unwrap_or_err() -> None:
    result = BaseResult[int](ok=Unset, err=ValueError("this is an error"))
    output = result.unwrap_or(0)
    assert output == 0


def test_expect_ok() -> None:
    result = BaseResult[int](ok=1, err=None)
    output = result.expect("Should produce 1")
    assert output == 1


def test_expect_unset() -> None:
    result = BaseResult[int](ok=Unset, err=None)
    with pytest.raises(ExpectError) as exc_info:
        result.expect("Should produce 1")
    assert "Should produce 1" in str(exc_info)
    assert exc_info.value.__cause__ is not None
    assert isinstance(exc_info.value.__cause__, UnsetError)


def test_expect_err() -> None:
    result = BaseResult[int](ok=Unset, err=ValueError("an error occurred"))
    with pytest.raises(ExpectError) as exc_info:
        result.expect("Should produce 1")
    assert "Should produce 1" in str(exc_info)
    assert exc_info.value.__cause__ is not None
    assert isinstance(exc_info.value.__cause__, ValueError)
