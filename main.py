#!/usr/bin/env python3
"""news-image-20261126: ship the day's front page to /output/entry.png.

The artwork (entry.png, drawn and verified when this entry was built)
sits next to this file in the repository. This program is stdlib-only:
it validates the PNG (signature, dimensions, size cap) and copies it
to the output directory atomically, so the grading sandbox needs no
third-party packages. Deterministic: same input, same bytes out.
"""

import hashlib
import os
import struct
import sys

EXPECTED_SIZE = (1024, 1024)
MAX_BYTES = 1048576
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def png_dimensions(data):
    """Read width/height from the IHDR chunk of a PNG byte string."""
    if data[:8] != PNG_SIGNATURE:
        raise ValueError("not a PNG file")
    if data[12:16] != b"IHDR":
        raise ValueError("first chunk is not IHDR")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(here, "entry.png")
    try:
        with open(src_path, "rb") as fh:
            data = fh.read()
        if len(data) > MAX_BYTES:
            raise ValueError("entry.png is over the 1 MiB cap")
        dims = png_dimensions(data)
        if dims != EXPECTED_SIZE:
            raise ValueError("entry.png is %dx%d, expected %dx%d"
                             % (dims + EXPECTED_SIZE))
    except (OSError, ValueError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    tmp_path = out_path + ".tmp"
    with open(tmp_path, "wb") as fh:
        fh.write(data)
    os.replace(tmp_path, out_path)

    print(
        "wrote %s (%d bytes, %dx%d, sha256 %s)"
        % (out_path, len(data), dims[0], dims[1],
           hashlib.sha256(data).hexdigest())
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
