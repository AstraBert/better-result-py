from typing import Any, Awaitable, Callable, Generic, TypeVar

# ======================================
# Types
# ======================================

T = TypeVar("T")


class UnsetType:
    """
    Sentinel type used to describe an `ok` value when an error has happened.
    """

    pass


Unset = UnsetType()

# ======================================
# Errors
# ======================================


class UnsetError(Exception):
    """
    Raised when a result is Unset even if no error was thrown.
    """

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __repr__(self) -> str:
        return "Result is Unset even if no error was raised"

    def __str__(self) -> str:
        return "Result is Unset even if no error was raised"


class ExpectError(Exception):
    """
    Raised when .expect() resolves to an error.
    """

    def __init__(self, message: str) -> None:
        self.message = message

    def __repr__(self) -> str:
        return self.message

    def __str__(self) -> str:
        return self.message


# ======================================
# Base class
# ======================================


class BaseResult(Generic[T]):
    """
    Base representation of the Rust result type.

    Attributes:
        ok (T | UnsetType): the result of an operation, or `Unset` if the operation threw an error.
        err (Exception | None): an exception thrown by an operation, or `None` if the operation did not throw exceptions.
    """

    def __init__(self, ok: T | UnsetType, err: Exception | None) -> None:
        self.ok = ok
        self.err = err

    def is_ok(self) -> bool:
        """
        Check if the result is ok and its value is not Unset.

        Returns:
            bool: True if there result is ok and set, False otherwise.
        """
        return self.err is None and not isinstance(self.ok, UnsetType)

    def is_err(self) -> bool:
        """
        Check if there was an exception or the result is Unset.

        Returns:
            bool: True if there was an exception or the result is Unset, False otherwise.
        """
        return self.err is not None or isinstance(self.ok, UnsetType)

    def unwrap(self) -> T:
        """
        Unwrap a result, throwing an exception if the `err` attribute is not None, or if the result is Unset.

        Returns:
            T: the typed result.

        Raises:
            Exception: exception from `err`.
            UnsetError: exception if the result is Unset.
        """
        if self.err is not None:
            raise self.err
        if not isinstance(self.ok, UnsetType):
            return self.ok
        raise UnsetError()

    def unwrap_or(self, default: T) -> T:
        """
        Unwrap a result, falling back to a default if the `err` attribute is not None, or if the result is Unset.

        Returns:
            T: the typed result (or the provided default).
        """
        if self.err is not None or isinstance(self.ok, UnsetType):
            return default
        return self.ok

    def expect(self, message: str) -> T:
        """
        Unwrap a result, always throwing an exception of type ExpectError (with a custom message) if the `err` attribute is not None or if the result is Unset.

        Returns:
            T: typed result.

        Raises:
            ExpectError: error with the provided custom message.
        """
        if self.err is not None:
            raise ExpectError(message) from self.err
        if isinstance(self.ok, UnsetType):
            raise ExpectError(message) from UnsetError()
        return self.ok


# ======================================
# Ok/Err Classes (for control flow)
# ======================================


class ResultError(Exception):
    """
    Custom error raised by `Err` when only an error message is passed to its constructor.
    """

    def __init__(self, message: str) -> None:
        self.message: str = message

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return self.message


class Ok(BaseResult[T]):
    """
    Subclass of BaseResult to represent the success value of an operation.

    Attributes:
        ok (T): the result of the operation.
    """

    def __init__(self, ok: T) -> None:
        super().__init__(ok, None)


class Err(BaseResult[T]):
    """
    Subclass of BaseResult to represent the failure value of an operation.

    Attributes:
        err (Exception): the exception raised by the operation
    """

    def __init__(
        self, error_message: str | None = None, *, err: Exception | None = None
    ) -> None:
        """
        Initialize the `Err` class.

        Args:
            error_message (str | None): error message, gets transformed into a ResultError when it is raised as an exception (during unwraps). Optional
            err (Exception | None): exception to be raised. Optional (one of `error_message` and `err` should be set).
        """
        if error_message is not None:
            super().__init__(Unset, ResultError(error_message))
        elif err is not None:
            super().__init__(Unset, err)
        else:
            raise RuntimeError(
                "`Err` should be initialized with either an error message or an exception"
            )


# ======================================
# Sync/Async Factories
# ======================================


def Result(fn: Callable[..., T], *args: Any, **kwargs: Any) -> BaseResult[T]:
    """
    Construct a base result from the execution of a synchronous function.

    Args:
        fn (Callable[..., T]): synchronous function.
        *args: arbitrary number of positional arguments (passed to the function).
        **kwargs: arbitrary number of keyword arguments (passed to the function).

    Returns:
        BaseResult[T]: the result of the function, wrapped in BaseResult.

    NOTE: this implementation does not preserve error stack traces for performance optimization, thus it should be used
    only for control flow and not for post-mortem debugging
    """

    try:
        output = fn(*args, **kwargs)
        error = None
    except Exception as e:
        output = Unset
        e.__traceback__ = None
        error = e
    return BaseResult[T](ok=output, err=error)


async def AsyncResult(
    fn: Callable[..., Awaitable[T]],
    *args: Any,
    **kwargs: Any,
) -> BaseResult[T]:
    """
    Construct a base result from the execution of an asynchronous function.

    Args:
        fn (Callable[..., Awaitable[T]]): asynchronous function.
        *args: arbitrary number of positional arguments (passed to the function).
        **kwargs: arbitrary number of keyword arguments (passed to the function).

    Returns:
        BaseResult[T]: the result of the function, wrapped in BaseResult.

    NOTE: this implementation does not preserve error stack traces for performance optimization, thus it should be used
    only for control flow and not for post-mortem debugging
    """
    try:
        output = await fn(*args, **kwargs)
        error = None
    except Exception as e:
        output = Unset
        e.__traceback__ = None
        error = e
    return BaseResult[T](ok=output, err=error)


if __name__ == "__main__":

    def something(i: int) -> BaseResult[int]:
        if i == 0:
            return Err("an error occurred")
        else:
            return Ok(i)
