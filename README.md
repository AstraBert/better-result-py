# better-result-py

> Inspired by [better-result](https://github.com/dmmulroy/better-result)

Yet another implementation of Rust's `Result` type: minimal, dependency-free, and fully-typed. Wraps synchronous and asynchronous functions so exceptions become values rather than control flow.

## Installation

```bash
# with uv
uv add better-result-py
# with pip
pip install better-result-py
```

## Usage

### Synchronous

Wrap any callable with `Result`. If the function raises, `ok` is `Unset` and `err` holds the exception. If it succeeds, `ok` holds the value and `err` is `None`.

```python
from better_result import Result

def divide(a: int, b: int) -> float:
    return a / b

result = Result(divide, 10, 2)
result.is_ok()   # True
result.ok        # 5.0
result.err       # None

result = Result(divide, 10, 0)
result.is_ok()   # False
result.err       # ZeroDivisionError(...)
```

### Asynchronous

`AsyncResult` works the same way for `async` functions.

```python
import asyncio
from better_result import AsyncResult

async def fetch_data(url: str) -> str:
    ...  # may raise

result = await AsyncResult(fetch_data, "https://example.com")

if result.is_ok():
    print(result.ok)
else:
    print(result.err)
```

## Explicit Ok / Err construction

For control-flow patterns where you want to return a typed result directly (without wrapping a callable) use `Ok` and `Err`.

```python
from better_result import Ok, Err, BaseResult

def divide(a: int, b: int) -> BaseResult[float]:
    if b == 0:
        return Err("division by zero")
    return Ok(a / b)

result = divide(10, 2)
result.is_ok()   # True
result.ok        # 5.0

result = divide(10, 0)
result.is_err()  # True
result.err       # ResultError("division by zero")
```

`Err` accepts either a plain string message (wrapped in `ResultError`) or an existing exception via the `err` keyword argument:

```python
Err("something went wrong")          # error_message form
Err(err=ValueError("bad value"))     # exception form
```

## Extracting values

### `unwrap()`

Returns the value or raises the original exception (or `UnsetError` if the result is unset).

```python
value = Result(divide, 10, 2).unwrap()   # 5.0
Result(divide, 10, 0).unwrap()           # raises ZeroDivisionError
```

### `unwrap_or(default)`

Returns the value or falls back to a default on error.

```python
value = Result(divide, 10, 0).unwrap_or(0.0)  # 0.0
```

### `expect(message)`

Like `unwrap()`, but always raises `ExpectError` with a custom message (preserving the original exception as `__cause__`).

```python
result = Result(divide, 10, 0)
result.expect("division must succeed")  # raises ExpectError("division must succeed")
```

## API reference

| Method | Description |
|---|---|
| `is_ok() -> bool` | `True` if no error and value is set |
| `is_err() -> bool` | `True` if an error occurred or value is unset |
| `unwrap() -> T` | Return value or raise |
| `unwrap_or(default: T) -> T` | Return value or default |
| `expect(message: str) -> T` | Return value or raise `ExpectError` |

## Requirements

Python 3.10 or higher. No runtime dependencies.

## Roadmap

Find the full roadmap [here](ROADMAP.md)
