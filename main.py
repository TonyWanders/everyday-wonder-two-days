#!/usr/bin/env python3
"""Write one sentence about a small moment of everyday wonder to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The sentence is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, prints it to stdout,
and enforces the competition gate: 1 to 200 characters, not only white space,
a single line. Pass --check to validate without writing anything.
"""

import os
import sys
from pathlib import Path

SENTENCE = "My shadow reached the corner before I did and waited there, already tired of following me."

MIN_CHARS = 1
MAX_CHARS = 200
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 200 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"sentence is {chars} characters, outside 1-200")
    if not text.strip():
        raise ValueError("sentence is only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("sentence must be a single line")
    return chars


def main() -> int:
    if "--check" in sys.argv[1:]:
        try:
            chars = validate(SENTENCE)
        except ValueError as exc:
            print(exc, file=sys.stderr)
            return 1
        print(f"entry is valid: {chars} characters, one line")
        return 0

    try:
        validate(SENTENCE)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(SENTENCE, encoding="utf-8")
    print(SENTENCE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
