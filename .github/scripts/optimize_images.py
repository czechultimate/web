#!/usr/bin/env python3
"""Shrink images larger than 2000 px or 1 MB and strip their metadata, including GPS location.

Usage: optimize_images.py [path ...]   (defaults to the current directory)
"""
import io
import os
import sys

from PIL import Image, ImageOps

MAX_SIDE = 2000
MAX_BYTES = 1_000_000
QUALITY = 82
# Re-encoding an already optimized JPEG saves a few percent and only loses quality.
MIN_SAVING = 0.9
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
SKIP_DIRS = {"_site", "node_modules"}
GPS_IFD = 0x8825
ORIENTATION = 0x0112


def iter_images(paths):
    for path in paths:
        if os.path.isfile(path):
            yield path
            continue
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in SKIP_DIRS]
            for name in files:
                if os.path.splitext(name)[1].lower() in EXTENSIONS:
                    yield os.path.join(root, name)


def optimize(path):
    size = os.path.getsize(path)
    with Image.open(path) as im:
        if getattr(im, "n_frames", 1) > 1:
            return None
        exif = im.getexif()
        has_gps = GPS_IFD in exif
        too_big = max(im.size) > MAX_SIDE or size > MAX_BYTES
        if not (too_big or has_gps):
            return None

        fmt = im.format
        icc = im.info.get("icc_profile")
        buf = io.BytesIO()
        if fmt == "JPEG" and not too_big and exif.get(ORIENTATION, 1) == 1:
            im.save(buf, "JPEG", quality="keep", optimize=True, icc_profile=icc)
        else:
            out = ImageOps.exif_transpose(im)
            if max(out.size) > MAX_SIDE:
                if out.mode == "P":
                    out = out.convert("RGBA")
                out.thumbnail((MAX_SIDE, MAX_SIDE), Image.Resampling.LANCZOS)
            if fmt == "JPEG":
                out.save(buf, "JPEG", quality=QUALITY, optimize=True, progressive=True, icc_profile=icc)
            elif fmt == "PNG":
                out.save(buf, "PNG", optimize=True, icc_profile=icc)
            elif fmt == "WEBP":
                out.save(buf, "WEBP", quality=QUALITY, method=6, icc_profile=icc)
            else:
                return None

    data = buf.getvalue()
    if not has_gps and len(data) > size * MIN_SAVING:
        return None
    with open(path, "wb") as f:
        f.write(data)
    return size, len(data)


def main():
    saved = 0
    for path in iter_images(sys.argv[1:] or ["."]):
        try:
            result = optimize(path)
        except (OSError, ValueError) as e:
            print(f"skipped {path}: {e}", file=sys.stderr)
            continue
        if result:
            before, after = result
            saved += before - after
            print(f"{path}: {before // 1024} kB -> {after // 1024} kB")
    print(f"saved {saved / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
