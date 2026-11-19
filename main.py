#!/usr/bin/env python3
"""news-image-20261119 entry: copy the rendered summary image to /output/entry.png.

Runs on Python 3.13 with the standard library only and no network. The image
(entry.png) was drawn locally by render.py from the verified news of Thursday
19 November 2026; this program only copies its exact bytes, so both grader
runs write identical output. After copying it verifies the copy byte for byte
(SHA-256 of source and destination must match) and refuses an oversize file,
so a truncated or corrupt write can never pass silently as a valid entry.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
MAX_BYTES = 1048576  # 1 MiB cap from the competition rules


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


src = os.path.join(HERE, "entry.png")
dst = os.path.join(OUT, "entry.png")

os.makedirs(OUT, exist_ok=True)
shutil.copyfile(src, dst)

# Verify the copy byte for byte; both grader runs must write the same bytes.
if sha256_of(src) != sha256_of(dst):
    raise SystemExit("entry.png copy mismatch: destination differs from source")
if os.path.getsize(dst) > MAX_BYTES:
    raise SystemExit("entry.png exceeds the 1 MiB cap")
print(f"wrote {dst} ({os.path.getsize(dst)} bytes, sha256 {sha256_of(dst)[:16]}...)")
