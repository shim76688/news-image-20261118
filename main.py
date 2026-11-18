"""Entry point for the news-image-20261118 competition entry.

Copies the bundled entry.png to the output directory named by the
MAKEFUN_OUTPUT_DIR environment variable (default /output).
Standard library only, no network access.
"""

import os
import sys

MAX_BYTES = 1_048_576
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def load_entry(source):
    """Read the bundled poster and check it is a PNG within the size cap."""
    with open(source, "rb") as handle:
        data = handle.read()
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("entry.png does not start with the PNG signature")
    if len(data) > MAX_BYTES:
        raise ValueError(
            "entry.png is %d bytes, over the %d byte limit"
            % (len(data), MAX_BYTES)
        )
    return data


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    data = load_entry(source)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as handle:
        handle.write(data)
    os.chmod(target, 0o644)
    return 0


if __name__ == "__main__":
    sys.exit(main())
