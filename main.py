"""make.fun news-image-20261122 entry: copy the day's front page to the output.

Standard library only, no network. The rendered image is committed next to
this file, so every run writes exactly the same bytes.
"""

import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
IMAGE = os.path.join(BASE, "entry.png")


def main():
    # The harness writes to /output; OUTPUT_DIR exists only for local testing.
    destination = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(destination, exist_ok=True)
    shutil.copyfile(IMAGE, os.path.join(destination, "entry.png"))


if __name__ == "__main__":
    main()
