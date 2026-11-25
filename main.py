#!/usr/bin/env python3
"""Entrypoint for the news-image-20261124 entry.

The graded program has one job: place this repository's front-page
image where the grader looks for it. The picture itself is drawn
ahead of time by draw.py and stored beside this file as entry.png,
so all that is left at run time is a faithful byte copy.

Where the copy lands:
  * the directory named by the MAKEFUN_OUTPUT_DIR environment
    variable, when that variable is set, or
  * /output otherwise.

The copy is plain bytes end to end -- no decoding, no re-encoding --
so repeated runs deliver exactly the same file.
"""

import os
import shutil
import sys

IMAGE_NAME = "entry.png"
FALLBACK_DIR = "/output"


def source_path():
    """The image shipped in this repository, next to this script."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, IMAGE_NAME)


def target_path():
    """Where the grader expects the image to appear."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or FALLBACK_DIR
    return os.path.join(out_dir, IMAGE_NAME)


def main():
    src = source_path()
    dst = target_path()
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)
    # A short copy would hand the grader a broken image; refuse to
    # report success unless every byte made the trip.
    if os.path.getsize(dst) != os.path.getsize(src):
        raise IOError("delivered image is incomplete: %s" % dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
