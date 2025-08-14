# String Calculator (Python, TDD with pytest)

This is a Python implementation of the classic **String Calculator** kata using **Test-Driven Development**.  
It mirrors the full spec from the prompt, adapted idiomatically to Python.

## Features implemented

1. `StringCalculator.add(numbers: str) -> int`
   - Supports 0, 1, or many numbers separated by delimiters.
   - Default delimiters: `,` and newline `\n`.
   - Custom delimiter syntax:
     - Single delimiter: `//;\n1;2`
     - Any-length delimiter: `//[***]\n1***2***3`
     - Multiple delimiters: `//[*][%]\n1*2%3`
     - Multiple any-length delimiters: `//[**][%%]\n1**2%%3`
   - Newlines between numbers are supported (e.g. `1\n2,3` = 6).
   - Numbers > 1000 are ignored.
   - Negative numbers raise: `ValueError("negatives not allowed: -1,-2")` with **all** negatives listed.
2. `StringCalculator.get_called_count() -> int` returns how many times `add()` was called.
3. **Event/callback** (Pythonic equivalent of .NET event): subscribe with `add_listener(fn)`.
   - Listener signature: `fn(input: str, result: int)`.
   - Fired after every successful `add()`.

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -U pip
pip install -r requirements.txt
pytest -q
```

## Requirements

- Python 3.9+
- `pytest`

## Running tests verbosely

```bash
pytest -vv
```

- `pytest -vv` passing output.
- The final test summary.
