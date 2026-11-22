"""make.fun news-image-20261122 entry: write the day's front page to /output/entry.png.

Standard library only, no network. The image is committed next to this file,
so every run writes exactly the same bytes.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main():
    # /output is the harness location; OUTPUT_DIR only exists for local testing.
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SOURCE, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
