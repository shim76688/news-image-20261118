"""Entry point for the news-image-20261118 competition entry.

Copies the bundled entry.png to the output directory named by the
MAKEFUN_OUTPUT_DIR environment variable (default /output).
Standard library only, no network access.
"""

import os
import shutil
import sys

MAX_BYTES = 1_048_576


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
