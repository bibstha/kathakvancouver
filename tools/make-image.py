#!/usr/bin/env python3
"""Build the three widths that a card plate or an event tile needs.

    tools/make-image.py SOURCE assets/artists/slug --fit
    tools/make-image.py SOURCE assets/artists/slug --crop 0,220,1711,1503
    tools/make-image.py SOURCE assets/artists/slug --pad

--fit   centre-crop to 4:3.
--crop  crop to the given box first. The box must already be 4:3.
--pad   contain the image on a white ground. For a logo.

The output is slug-400.jpg, slug-600.jpg and slug-900.jpg. The widths follow
the plate: a card is at most 340 CSS px wide and an event tile is 240, so 600
covers a 2x screen and 900 covers a 3x one. See docs/styleguide.md 4.11.
"""
import argparse, os
from PIL import Image, ImageChops, ImageOps

WIDTHS = (400, 600, 900)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("dest", help="path without the width suffix or extension")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--fit", action="store_true")
    g.add_argument("--crop", help="x0,y0,x1,y1")
    g.add_argument("--pad", action="store_true")
    ap.add_argument("--focus", default="0.5,0.5", help="--fit centring, 0-1")
    a = ap.parse_args()

    im = Image.open(a.source).convert("RGB")
    if a.crop:
        im = im.crop(tuple(int(v) for v in a.crop.split(",")))
    elif a.pad:
        # Trim the flat border a logo usually carries, then centre it.
        box = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255)))
        box = box.convert("L").point(lambda p: 255 if p > 12 else 0).getbbox()
        if box:
            im = im.crop(box)

    for w in WIDTHS:
        h = round(w * 3 / 4)
        if a.pad:
            tile = im.copy()
            tile.thumbnail((round(w * 0.86), round(h * 0.86)), Image.LANCZOS)
            out = Image.new("RGB", (w, h), (255, 255, 255))
            out.paste(tile, ((w - tile.width) // 2, (h - tile.height) // 2))
        elif a.crop:
            out = im.resize((w, h), Image.LANCZOS)
        else:
            fx, fy = (float(v) for v in a.focus.split(","))
            out = ImageOps.fit(im, (w, h), Image.LANCZOS, centering=(fx, fy))
        path = f"{a.dest}-{w}.jpg"
        out.save(path, "JPEG", quality=84, optimize=True, progressive=True)
        print(f"{path}  {w}x{h}  {os.path.getsize(path) // 1024}K")


if __name__ == "__main__":
    main()
