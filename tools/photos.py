#!/usr/bin/env python3
"""Crop, color-grade and export the site photos from images/originals/ (gitignored).
Run from the repo root: python3 tools/photos.py
"""
from PIL import Image, ImageOps, ImageEnhance

def grade(im):
    # Neutral on purpose: no warm shift, so gallery walls stay lab white.
    im = ImageOps.autocontrast(im.convert("RGB"), cutoff=0.6)
    return ImageEnhance.Color(im).enhance(1.08)

def crop(im, ratio, fx=0.5, fy=0.5):
    w, h = im.size
    if w / h > ratio:
        nw = int(h * ratio); x = int((w - nw) * fx); return im.crop((x, 0, x + nw, h))
    nh = int(w / ratio); y = int((h - nh) * fy); return im.crop((0, y, w, y + nh))

# name: (source id, ratio, focus x, focus y, kind)
JOBS = {
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

# Link preview image (og.jpg): her DNA painting hung on the site's Prussian
# blue, with the same thin gilt line the frames use. Her art, never her face.
from PIL import ImageDraw, ImageFilter
card = Image.new("RGB", (1200, 630), (10, 36, 64))
art = Image.open("images/art/originals/dna-helix.png").convert("RGB")
h = 560
art = art.resize((round(art.width * h / art.height), h), Image.LANCZOS)
x, y = (1200 - art.width) // 2, (630 - h) // 2
shadow = Image.new("L", (1200, 630), 0)
ImageDraw.Draw(shadow).rectangle((x + 6, y + 18, x + art.width + 6, y + h + 18), fill=150)
card.paste((3, 12, 24), (0, 0), shadow.filter(ImageFilter.GaussianBlur(18)))
card.paste(art, (x, y))
ImageDraw.Draw(card).rectangle((x, y, x + art.width - 1, y + h - 1), outline=(201, 162, 63), width=3)
card.save("images/og.jpg", quality=86)
print("wrote og.jpg")
