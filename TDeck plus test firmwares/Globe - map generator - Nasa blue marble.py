#!/usr/bin/env python3
"""
Blue Marble tile generator for the NNOs Globe app.

Output layout (copy the whole "maps" folder to the SD card root):

    maps/bluemarble/palette.bin          768 B, 256 x RGB888, median cut
    maps/bluemarble/CREDITS.txt          NASA attribution
    maps/bluemarble/<T>/info.txt         tile=<T> maxzoom=<Z> cols0=2 rows0=1
    maps/bluemarble/<T>/<z>/<x>/<y>.jpg  equirectangular pyramid

Pyramid: at zoom z there are 2^(z+1) columns and 2^z rows of T x T tiles.
x=0 starts at longitude -180, y=0 starts at latitude +90.

Tiles are baseline JPEG (never progressive): JPEGDEC on the device does not
handle progressive files reliably.

Source image: "Blue Marble: Next Generation", Reto Stoeckli,
NASA Earth Observatory (NASA Goddard Space Flight Center).
"""

import argparse
import sys
import urllib.request
from pathlib import Path

from PIL import Image

# The source is a single large JPEG; without this PIL refuses it as a
# possible decompression bomb.
Image.MAX_IMAGE_PIXELS = None

DEFAULT_URL = (
    "https://eoimages.gsfc.nasa.gov/images/imagerecords/73000/73909/"
    "world.topo.bathy.200412.3x5400x2700.jpg"
)
CREDIT = (
    "Blue Marble: Next Generation was produced by Reto Stoeckli, "
    "NASA Earth Observatory (NASA Goddard Space Flight Center).\n"
    "Source: https://earthobservatory.nasa.gov/features/BlueMarble\n"
)
PALETTE_SAMPLE_WIDTH = 1024   # quantize a downscaled copy: same colours, far faster


def download(url: str, dest: Path) -> Path:
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    print(f"Downloading {url}")
    part = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": "nnos-bluemarble/1.0"})
    with urllib.request.urlopen(req) as resp, open(part, "wb") as out:
        while True:
            chunk = resp.read(1 << 20)
            if not chunk:
                break
            out.write(chunk)
    # Rename only once complete, so an interrupted download is never
    # mistaken for a valid cached file on the next run.
    part.replace(dest)
    return dest


def max_zoom_without_upscale(src_width: int, tile: int) -> int:
    z = 0
    while (2 ** (z + 2)) * tile <= src_width:
        z += 1
    return z


def write_palette(img: Image.Image, path: Path) -> None:
    h = max(1, img.height * PALETTE_SAMPLE_WIDTH // img.width)
    small = img.resize((PALETTE_SAMPLE_WIDTH, h), Image.Resampling.BOX)
    quant = small.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    pal = (quant.getpalette() or [])[: 256 * 3]
    pal += [0] * (256 * 3 - len(pal))   # PIL may return fewer entries
    path.write_bytes(bytes(pal))
    print(f"Palette: {path} ({len(pal)} bytes)")


def generate(img: Image.Image, root: Path, tile: int, max_zoom: int, quality: int) -> None:
    total = 0
    size = 0
    for z in range(max_zoom + 1):
        cols = 2 ** (z + 1)
        rows = 2 ** z
        tw, th = cols * tile, rows * tile
        print(f"Zoom {z}: {tw}x{th}, {cols * rows} tiles")
        level = img.resize((tw, th), Image.Resampling.LANCZOS)
        for x in range(cols):
            col_dir = root / str(z) / str(x)
            col_dir.mkdir(parents=True, exist_ok=True)
            for y in range(rows):
                left, upper = x * tile, y * tile
                t = level.crop((left, upper, left + tile, upper + tile))
                out = col_dir / f"{y}.jpg"
                t.save(out, "JPEG", quality=quality, optimize=True,
                       progressive=False, subsampling=2)
                total += 1
                size += out.stat().st_size
    (root / "info.txt").write_text(
        f"tile={tile}\nmaxzoom={max_zoom}\ncols0=2\nrows0=1\n", encoding="ascii"
    )
    print(f"{total} tiles, {size / 1024 / 1024:.1f} MB")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tile", type=int, choices=(128, 256), default=128)
    ap.add_argument("--max-zoom", type=int, default=4)
    ap.add_argument("--quality", type=int, default=75)
    ap.add_argument("--out", type=Path, default=Path("sdcard"))
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--cache", type=Path, default=Path("blue_marble_raw.jpg"))
    ap.add_argument("--allow-upscale", action="store_true",
                    help="keep zoom levels wider than the source image")
    args = ap.parse_args()

    src = Image.open(download(args.url, args.cache)).convert("RGB")
    print(f"Source: {src.width}x{src.height}")

    limit = max_zoom_without_upscale(src.width, args.tile)
    max_zoom = args.max_zoom
    if max_zoom > limit and not args.allow_upscale:
        print(f"Capping max zoom {max_zoom} -> {limit}: higher levels would only "
              f"upscale a {src.width} px source (use --allow-upscale to keep them)")
        max_zoom = limit

    base = args.out / "maps" / "bluemarble"
    base.mkdir(parents=True, exist_ok=True)
    (base / "CREDITS.txt").write_text(CREDIT, encoding="ascii")
    write_palette(src, base / "palette.bin")
    generate(src, base / str(args.tile), args.tile, max_zoom, args.quality)
    print(f"Done. Copy '{args.out / 'maps'}' to the SD card root.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
