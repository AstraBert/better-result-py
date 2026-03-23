# Roadmap for `better-result-py` 

| Feature | Target Version | Released with Version | Release Deadline* |
|---------|----------------|-----------------------|-------------------|
| `Ok` and `Err` subclasses of `BaseResult` |  1.1.0 |  NA | 1st April 2026 |
| Extend methods for `BaseResult` (for instance: `map`, `and_then`, `inspect`) | 1.2.0 | NA | 30th April 2026 |
| Transition the `Result` and `AsyncResult` factories to decorator (maintaining backward compatibility) | 1.3.0 | NA | 15th May 2026 | 
| Add a `match` method for `BaseResult`  | 1.3.1 | NA | 1st June 2026 |

* Not strict deadlines: this means that a release migth be going out some days before or some days after the reported date

## Feature design

### `Ok` and `Err`

Should be standalone subclasses employed by users for control flow:

```python
def divide(x: int, y: int) -> float:
    if y == 0:
        return Err[str]("ZeroDivision Error")
    else:
        return Ok[float](x / y)
```

They should use generic typing to respect the super class `BaseResult`

### Decorators

The decorators should be `as_result` and `as_async_result` and should work like this:

```python
@as_result(*exceptions) # -> exceptions is a list of BaseException. Defaults to Exception if not provided
def fn() -> int:
    return 1
    
result = fn() # -> Returns a BaseResult
result.is_ok() # -> True
result.ok # -> 1 
```

### `match` method

It should take two callables, one for `err` and one for `ok`. The callable for `err` should default to a function that raises the error:

```python
def takes_error(e: Exception) -> str:
    return e.__repr__()
    
def print_result(r: Any) -> None:
    print(r)

result.match(
    err=takes_err,
    ok=print_result,
)

result.match(
    ok=print_result
) # -> this will raise an error if err is not None
```

## Contribution Guidelines

What is reported in [CONTRIBUTING.md](./CONTRIBUTING.md) holds true, with a few more rules: 

- Fully AI-generated (no human oversight or correction) PRs will be closed at the discretion of the repository admin. Opening multiple of these PRs might result in a temporary or permanent ban of the contributor.
- Pinging maintainers/repository admin for reviews is not allowed within the first 24 hours of opening a PR: if maintainers did not review your PR within 24 hours, you can ping them. Pings before the 24 hours deadline will result in a temporary ban, up to 60 days.
- PRs should address only one feature/issue. PRs that add/remove/refactor more than 50% of the current codebase (based on number of diff lines) will be discarded and you will be encouraged to break the changes down in smaller PRs.
- PRs should be fully tested, and, if needed, add performance benchmarks in `test_bench_*` or `test_malloc`.
- Changes should be documented in the README, if they affect the user-facing API

### How do we determine if a PR is AI generated?

The following indicators will be used to determine whether a PR is fully AI-generate or not:

- AI agent listed as co-author or sole author of a commit
- Multi-line, extremely-well formatted commit messages
- LLM-generated PR descriptions
- LLM-generated PR comments
