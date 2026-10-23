#!/usr/bin/env python3
"""Crop and export the artwork on the Artists page from images/genre/originals/ (gitignored).
Run from the repo root: python3 tools/genre.py

Every image here is public domain or openly licensed. The license and credit
for each one live with the piece in GENRE in build.py and in the README.
Artwork is never color-graded; only cropped and resized.
"""
from PIL import Image

# name: (original file, crop box in original pixels or None)
JOBS = {
    "hooke-cork": ("hooke-schem11.jpg", (30, 195, 1168, 1328)),
    "flemming-mitosis": ("flemming-cell-division.jpg", (1035, 175, 1715, 1140)),
    "cajal-purkinje": ("cajal-purkinje-neurons.jpg", None),
    "goodsell-ecoli": ("goodsell-ecoli-bacterium.jpg", None),
    "goodsell-mycoplasma": ("goodsell-mycoplasma-mycoides.jpg", None),
    "harris-retina": ("harris-zebrafish-retina.jpg", None),
    "noel-t-cell": ("noel-tcell-cancer.jpg", None),
    "noel-blood": ("noel-blood-cells.jpg", None),
    "magrath-neurones": ("magrath-neurones-connecting.jpg", (0, 0, 1930, 1507)),
    "agar-butterfly": ("chaurasiya-agar-butterfly.jpg", (215, 0, 1655, 1440)),
}

for name, (src, box) in JOBS.items():
    im = Image.open(f"images/genre/originals/{src}").convert("RGB")
    if box:
        im = im.crop(box)
    for w in (600, 1000):
        w2 = min(w, im.width)  # a small scan keeps its own width
        out = im.resize((w2, round(im.height * w2 / im.width)), Image.LANCZOS)
        out.save(f"images/genre/{name}-{w}.webp", quality=80, method=6)
    print("wrote", name, im.size)
