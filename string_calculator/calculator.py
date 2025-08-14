from __future__ import annotations

import re
from typing import Callable, Iterable, List


class StringCalculator:
    """
    String Calculator kata implemented in Python.

    Public API:
      - add(numbers: str) -> int
      - get_called_count() -> int
      - add_listener(callback: Callable[[str, int], None]) -> None  # Pythonic "event"
    """

    _DEFAULT_DELIMITERS = [",", "\n"]

    def __init__(self) -> None:
        self._called_count = 0
        self._listeners: List[Callable[[str, int], None]] = []

    # region Public API

    def add(self, numbers: str | None) -> int:
        """Add all numbers found in the input string using the kata's delimiter rules."""
        if numbers is None:
            numbers = ""

        tokens = self._tokenize(numbers)
        values = self._to_ints(tokens)

        negatives = [n for n in values if n < 0]
        if negatives:
            msg = "negatives not allowed: " + ",".join(str(n) for n in negatives)
            raise ValueError(msg)

        # Ignore numbers > 1000
        result = sum(n for n in values if n <= 1000)

        self._called_count += 1
        self._fire_event(numbers, result)

        return result

    def get_called_count(self) -> int:
        """Return how many times add() was invoked."""
        return self._called_count

    def add_listener(self, callback: Callable[[str, int], None]) -> None:
        """Subscribe a listener that receives (input, result) after each successful add()."""
        if not callable(callback):
            raise TypeError("callback must be callable")
        self._listeners.append(callback)

    # endregion

    # region Internals

    def _fire_event(self, input_str: str, result: int) -> None:
        for cb in list(self._listeners):
            try:
                cb(input_str, result)
            except Exception:
                # Don't let a bad listener break add(); ignore listener exceptions.
                pass

    def _tokenize(self, s: str) -> List[str]:
        """
        Split input into tokens according to the kata rules:
          - Default delimiters: comma and newline
          - Custom header: starting with '//' and ending at first newline
              * Single-char: //;\n
              * Any-length: //[***]\n
              * Multiple: //[*][%]\n
              * Multiple any-length: //[**][%%]\n
        """
        if s.startswith("//"):
            header, _, rest = s.partition("\n")
            delimiters = self._parse_delimiters(header)
            pattern = self._build_split_pattern(delimiters)
            return [t for t in re.split(pattern, rest) if t != ""]
        else:
            pattern = self._build_split_pattern(self._DEFAULT_DELIMITERS)
            return [t for t in re.split(pattern, s) if t != ""]

    def _parse_delimiters(self, header: str) -> List[str]:
        # header like: //;\n or //[***]\n or //[*][%]\n
        assert header.startswith("//")
        raw = header[2:]
        if raw.startswith("["):
            # One or more [delim] groups
            delims = re.findall(r"\[([^\]]+)\]", raw)
            if not delims:
                raise ValueError("Invalid delimiter header")
            return delims
        else:
            # Single character delimiter
            if len(raw) != 1:
                # Defensive: if someone provides //ab\n treat as full string delimiter
                return [raw]
            return [raw]

    def _build_split_pattern(self, delimiters: Iterable[str]) -> re.Pattern[str]:
        escaped = [re.escape(d) for d in delimiters]
        # Join all delimiters into an alternation group for re.split
        # Using (?:...) non-capturing group
        pattern = r"(?:%s)" % "|".join(escaped)
        return re.compile(pattern)

    def _to_ints(self, tokens: Iterable[str]) -> List[int]:
        values: List[int] = []
        for t in tokens:
            t = t.strip()
            if t == "":
                # We filter empties in _tokenize, but be robust
                continue
            try:
                values.append(int(t))
            except ValueError:
                raise ValueError(f"Invalid number: {t!r}")
        return values

    # endregion
