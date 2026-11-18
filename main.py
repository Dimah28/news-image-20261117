#!/usr/bin/env python3
"""The World in One Day -- Tuesday 17 November 2026.

Entry for the make.fun bounty "Sum up 17 November's world news in
one image" (news-image-20261117).

The image is the entry.png beside this file, rendered offline with
Pillow and DejaVu fonts (a dense newspaper front page: 43 real
stories from Tuesday 17 November 2026 -- 3 hero stories, 10
illustrated panels, a numbered world map and a 30-item "also on"
list). The program itself is standard library only: it copies
entry.png into MAKEFUN_OUTPUT_DIR, so it runs in the grader's stock
python:3.13 image with a read-only repo directory. Copying the same
file twice writes byte-identical output, and nothing is written
outside MAKEFUN_OUTPUT_DIR.

Run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"),
                    os.path.join(outdir, "entry.png"))


if __name__ == "__main__":
    main()
