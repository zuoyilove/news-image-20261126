"""news-image-20261126 entry (Python 3.13, standard library only).

The entry image is the entry.png beside this file: a newspaper front page
summing up Thursday 26 November 2026 -- the Wall Street rout (Nasdaq
-3.1%, Nvidia -8.7%, new Section 301 tariffs on 14 partners), the FCC
clearing SpaceX's 1m-satellite Starmind plan, Shenzhou-24 docking at
Tiangong with Pakistan's first astronaut, the Cairo Ring Road tanker fire
(31 killed), and the Australia-Solomon Islands security pact, plus a
ticker of the day's other headlines.

The program copies that image, byte for byte, to entry.png inside the
output directory (MAKEFUN_OUTPUT_DIR outside the grader, /output inside
it). It writes the same bytes on every run, so the two grading runs are
identical. No network, no extra files, no randomness.
"""

import hashlib
import os
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
MAX_BYTES = 1_048_576
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def check_image(data: bytes) -> None:
    """Fail loudly instead of shipping a bad image.

    The gate takes a whole PNG of at most 1 MiB and 1024 by 1024 pixels,
    so verify the magic, the IHDR size and the byte count here, before
    anything is written to the output directory.
    """
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.png is {len(data)} bytes, over the 1 MiB cap")
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise SystemExit(
            f"entry.png is {width}x{height}, expected "
            f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    data = SOURCE.read_bytes()
    check_image(data)
    target = out_dir / "entry.png"
    # Write to a temp file in the same directory, then rename: the rename
    # is atomic, so a reader never observes a half-written image, and the
    # size check proves the copy is whole before it becomes visible.
    tmp = target.with_suffix(".tmp")
    tmp.write_bytes(data)
    if tmp.stat().st_size != len(data):
        raise SystemExit("short write while copying entry.png")
    tmp.replace(target)
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {target} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
