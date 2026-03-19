from typing import Any, Awaitable, Callable, Generic, TypeVar

# ======================================
# Types
# ======================================

T = TypeVar("T")


class UnsetType:
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
    def __init__(self, ok: T | UnsetType, err: Exception | None) -> None:
        self.ok = ok
        self.err = err

    def is_ok(self) -> bool:
        return self.err is None

    def is_err(self) -> bool:
        return self.err is not None

    def unwrap(self) -> T:
        if self.err is not None:
            raise self.err
        if not isinstance(self.ok, UnsetType):
            return self.ok
        raise UnsetError()

    def unwrap_or(self, default: T) -> T:
        if self.err is not None or isinstance(self.ok, UnsetType):
            return default
        return self.ok

    def expect(self, message: str) -> T:
        if self.err is not None:
            raise ExpectError(message) from self.err
        if isinstance(self.ok, UnsetType):
            raise ExpectError(message) from UnsetError()
        return self.ok


# ======================================
# Sync/Async Factories
# ======================================


def Result(fn: Callable[..., T], *args: Any, **kwargs: Any) -> BaseResult[T]:
    try:
        output = fn(*args, **kwargs)
        error = None
    except Exception as e:
        output = Unset
        error = e
    return BaseResult[T](ok=output, err=error)


async def AsyncResult(
    fn: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any
) -> BaseResult[T]:
    try:
        output = await fn(*args, **kwargs)
        error = None
    except Exception as e:
        output = Unset
        error = e
    return BaseResult[T](ok=output, err=error)
