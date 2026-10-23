#!/usr/bin/env python3
"""Crop, color-grade and export the site photos from images/originals/ (gitignored).
Run from the repo root: python3 tools/photos.py
"""
from PIL import Image, ImageOps, ImageEnhance

def grade(im):
    im = ImageOps.autocontrast(im.convert("RGB"), cutoff=0.6)
    im = ImageEnhance.Color(im).enhance(1.08)
    r, g, b = im.split()
    r = r.point(lambda v: min(255, int(v * 1.025)))
    b = b.point(lambda v: int(v * 0.98))
    return Image.merge("RGB", (r, g, b))

def crop(im, ratio, fx=0.5, fy=0.5):
    w, h = im.size
    if w / h > ratio:
        nw = int(h * ratio); x = int((w - nw) * fx); return im.crop((x, 0, x + nw, h))
    nh = int(w / ratio); y = int((h - nh) * fy); return im.crop((0, y, w, y + nh))

# name: (source id, ratio, focus x, focus y, kind)
JOBS = {
    "hero-gallery-bench": ("ABdRtZKWJfE", 3 / 2, 0.5, 0.55, "hero"),
    "hero-bright-gallery": ("qxvOmDuQDsg", 3 / 2, 0.5, 0.55, "hero"),
    "hero-boy-painting": ("hbZOr0FfNNE", 3 / 2, 0.5, 0.45, "hero"),
    "microscope": ("6q5QG8iIgRo", 4 / 3, 0.6, 0.4, "photo"),
    "watercolor": ("YKLkzMuEA8Q", 4 / 3, 0.5, 0.5, "photo"),
    "hero-gallery-visitor": ("AlLKJ292jOQ", 3 / 2, 0.55, 0.5, "hero"),
}
for name, (src, ratio, fx, fy, kind) in JOBS.items():
    im = grade(crop(Image.open(f"images/originals/{src}.jpg"), ratio, fx, fy))
    widths = (600, 800, 960, 1200) if kind == "hero" else (600, 900)
    for w in widths:
        im.resize((w, round(w / ratio)), Image.LANCZOS).save(f"images/{name}-{w}.webp", quality=78, method=6)
    if name == "hero-gallery-bench":
        crop(im, 1200 / 630).resize((1200, 630), Image.LANCZOS).save("images/og.jpg", quality=82)
    print("wrote", name)

# Portraits of Lily (4:5), cropped tight with explicit boxes in original pixels.
PORTRAITS = {
    "lily-wall": ("lily-wall", (1093, 865, 5100, 5874)),
    "lily-column": ("lily-column", (785, 610, 4098, 4752)),
}
for name, (src, box) in PORTRAITS.items():
    im = grade(Image.open(f"images/originals/{src}.jpg").crop(box))
    for w in (480, 680, 800):
        im.resize((w, round(w * 5 / 4)), Image.LANCZOS).save(f"images/{name}-{w}.webp", quality=70, method=6)
    print("wrote", name)
