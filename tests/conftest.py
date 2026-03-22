from typing import Any, Callable

from better_result.result import BaseResult, T, Unset


def ResultWithTb(fn: Callable[..., T], *args: Any, **kwargs: Any) -> BaseResult[T]:
    """
    Construct a base result from the execution of a synchronous function.

    Args:
        fn (Callable[..., T]): synchronous function.
        *args: arbitrary number of positional arguments (passed to the function).
        **kwargs: arbitrary number of keyword arguments (passed to the function).

    Returns:
        BaseResult[T]: the result of the function, wrapped in BaseResult.
    """

    try:
        output = fn(*args, **kwargs)
        error = None
    except Exception as e:
        output = Unset
        error = e
    return BaseResult[T](ok=output, err=error)
