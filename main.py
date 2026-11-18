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
python:3.13 image with a read-only repo directory. After copying it
verifies the output's SHA-256 against the expected hash and fails
loudly on any mismatch, so a truncated or corrupted copy can never
pass silently. Copying the same file twice writes byte-identical
output, and nothing is written outside MAKEFUN_OUTPUT_DIR.

Run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))

# SHA-256 of entry.png as rendered offline (render.py, deterministic).
# The copy is verified against this after writing, so a truncated or
# corrupted entry can never pass silently through the grader.
EXPECTED_SHA256 = ("90c72e14533fc42c9956f149988b220d500d5162fde70f59ad"
                   "844bcdedee4aa3")


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(outdir, "entry.png")
    shutil.copyfile(src, dst)
    # Integrity check: the copied file must be byte-identical to the
    # entry that was reviewed. Fail loudly instead of handing the
    # grader a truncated or corrupted image.
    digest = hashlib.sha256()
    with open(dst, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    if digest.hexdigest() != EXPECTED_SHA256:
        raise SystemExit(
            "entry.png integrity check failed: copied file does not "
            "match the expected SHA-256; refusing to report success")


if __name__ == "__main__":
    main()
