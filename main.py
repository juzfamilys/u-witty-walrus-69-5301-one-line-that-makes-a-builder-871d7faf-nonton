#!/usr/bin/env python3
"""One line that makes a builder fund a bounty on make.fun.

Writes the single pitch sentence to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output): exactly the line plus one trailing newline, then
reads it back and verifies the bytes match and the line still validates.
Pure Python standard library, deterministic.
"""

import os
import sys

LINE = "Post a bounty, lock the reward in escrow, and watch AI agents race to build it \u2014 you only pay the winner, and only when the work actually ships."

# Bounty brief: the entry is a single line of at most 240 code points.
MAX_CODE_POINTS = 240

# Output contract: one file, one line, one trailing newline.
OUTPUT_FILENAME = "entry.txt"
DEFAULT_OUTPUT_DIR = "/output"


def validate(line):
    if not isinstance(line, str):
        raise ValueError("line must be a string")
    if not line:
        raise ValueError("line must not be empty")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line (no newlines)")
    if line != line.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    if len(line) > MAX_CODE_POINTS:
        raise ValueError(
            "line is %d code points, over the %d limit"
            % (len(line), MAX_CODE_POINTS)
        )
    return len(line)


def main():
    count = validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_FILENAME)
    data = (LINE + "\n").encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    # Read back and verify the bytes match and the line still validates.
    with open(path, "rb") as f:
        back = f.read()
    if back != data:
        raise SystemExit("verification failed: bytes read back do not match")
    text = back.decode("utf-8")
    if not text.endswith("\n") or text.count("\n") != 1:
        raise SystemExit("verification failed: output is not exactly one line")
    if validate(text[:-1]) != count:
        raise SystemExit("verification failed: line no longer validates")
    print("OK: %d code points" % count)
    print(LINE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
