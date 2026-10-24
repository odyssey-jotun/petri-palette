#!/usr/bin/env python3
"""Builds every page of Petri Palette.

Run: python3 build.py
The site name lives in SITE_NAME below. Change it there, rebuild, and every
page title, heading, wordmark, footer and JSON-LD block follows. Facts and
copy live in this file too, so a correction is made once.

Lily's paintings: drop each scanned painting into images/art/ as a .webp or
.jpg (about 1200px on the long side, portrait 4:5 looks best) and set its file
name in "art" on the piece below. Until then the frame shows a line drawing.
"""
import json
import re

# ---------------------------------------------------------------- settings
SITE_NAME = "Petri Palette"
AUTHOR = "Lily Butler"
SITE = "https://odyssey-jotun.github.io/petri-palette/"
TODAY = "2026-10-23"

# Sources, cited in plain text. No links on purpose (see README).
SOURCES = {
    "nagb": "National Assessment Governing Board. <em>5 Things You Need to Know About NAEP Science Results</em> (2024 Nation's Report Card, grade 8 science). nagb.gov, 2025.",
    "edsource": "Gallegos, Emma. <em>Enjoyment of science plummeted along with scores on 8th grade national test.</em> EdSource, September 9, 2025.",
    "ltt": "National Center for Education Statistics. <em>NAEP Long-Term Trend Assessment Results: Reading and Mathematics, Age 13</em> (2023). nationsreportcard.gov.",
    "potvin": "Potvin, Patrice, and Abdelkrim Hasni. <em>Interest, motivation and attitude towards science and technology at K-12 levels: a systematic review of 12 years of educational research.</em> Studies in Science Education 50, no. 1 (2014).",
    "pisa": "OECD. <em>PISA 2022 Results</em> (press release, December 5, 2023). oecd.org.",
    "hardiman": "Hardiman, Mariale, Luke Rinne, and Julia Yarmolinskaya. <em>The Effects of Arts Integration on Long-Term Retention of Academic Content.</em> Mind, Brain, and Education 8, no. 3 (2014).",
    "ainsworth": "Ainsworth, Shaaron, Vaughan Prain, and Russell Tytler. <em>Drawing to Learn in Science.</em> Science 333, no. 6046 (2011).",
}

# ---------------------------------------------------------------- the exhibit
# Each series is one wall of the exhibit. Each piece is one painting.
# "art": file name in images/art/ once Lily's painting is scanned, else None.
# "title" stays as the subject until Lily names the painting.
SERIES = [
    {"id": "mitosis", "name": "Mitosis",
     "intro": "One cell becoming two, painted as five stages. Human cells carry 46 chromosomes, so I painted only a handful to keep each stage easy to read.",
     "pieces": [
         {"id": "interphase", "title": "Interphase", "meta": "Before mitosis", "draw": "interphase", "art": None,
          "text": "The cell grows and copies its DNA. The chromosomes are loose, stringy and tangled together, so no single one stands out yet.",
          "see": "Look for the messy, jumbled strands."},
         {"id": "prophase", "title": "Prophase", "meta": "Stage 1", "draw": "prophase", "art": None,
          "text": "The copied chromosomes coil up tight enough to see, and spindle fibers begin to form at opposite ends of the cell.",
          "see": "Look for the X-shaped chromosomes floating free."},
         {"id": "metaphase", "title": "Metaphase", "meta": "Stage 2", "draw": "metaphase", "art": None,
          "text": "The chromosomes line up across the middle of the cell. Each one is two identical sister chromatids joined at the center, with spindle fibers attached from both sides.",
          "see": "Look for the line of chromosomes down the middle."},
         {"id": "anaphase", "title": "Anaphase", "meta": "Stage 3", "draw": "anaphase", "art": None,
          "text": "The spindle fibers pull the sister chromatids apart, and each half moves toward an opposite end of the cell.",
          "see": "Look for the chromatids pulling away from each other."},
         {"id": "telophase", "title": "Telophase", "meta": "Stage 4", "draw": "telophase", "art": None,
          "text": "A new nucleus forms at each end, and the cell pinches in at the middle until it splits into two cells.",
          "see": "Look for the pinch in the middle."},
     ]},
    {"id": "protein-transcription", "name": "Protein Transcription",
     "intro": "How a gene becomes a protein. In the nucleus, a gene's DNA is copied into messenger RNA (transcription). A ribosome then reads that RNA and links amino acids into a protein (translation), and the Golgi apparatus packages the finished protein.",
     "pieces": [
         {"id": "dna-to-rna", "title": "DNA to RNA", "meta": "Transcription", "draw": "dna", "art": ("dna-helix.webp", 711, 890),
          "alt": "a gold DNA double helix unzipping across a blue cloud on a dark background, with colored base pairs and a new strand inside",
          "text": "Inside the nucleus, the DNA double helix unzips, and one strand is copied into a single strand of messenger RNA. That copy carries the gene's instructions out of the nucleus.",
          "see": "Look for the new strand forming inside the open section of the helix."},
         {"id": "golgi-apparatus", "title": "The Golgi Apparatus", "meta": "Packaging", "draw": "mrna", "art": ("golgi-apparatus.webp", 713, 694),
          "alt": "a stack of curved dark and red-orange sacs on a teal background, ringed by round orange vesicles",
          "text": "Newly made proteins pass through the Golgi apparatus, a stack of flattened sacs that sorts and packages them. Small bubbles called vesicles bud off the edges and carry the finished proteins where they need to go.",
          "see": "Look for the stacked sacs and the round vesicles around them."},
     ]},
]
N_PIECES = sum(len(s["pieces"]) for s in SERIES)
WORDS = {2: "two", 3: "three", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}

# ---------------------------------------------------------------- helpers
CSS = None


def css():
    """styles.css, minified and inlined so no stylesheet blocks first paint."""
    global CSS
    if CSS is None:
        t = open("styles.css").read()
        t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)
        t = re.sub(r"\s+", " ", t)
        t = re.sub(r"\s*([{};:,>])\s*", r"\1", t).replace(";}", "}")
        CSS = t.strip()
    return CSS


def srcset(name, widths):
    return ", ".join(f"images/{name}-{w}.webp {w}w" for w in widths)


HERO_W = (600, 800, 960, 1200)
HOME_SIZES = "(max-width: 620px) calc(100vw - 40px), (max-width: 1136px) calc(100vw - 56px), 1080px"
PAGE_SIZES = "(max-width: 860px) calc(100vw - 40px), 500px"


def hero_img(name, alt, sizes, cls="hero-photo"):
    return (f'<figure class="{cls}"><img src="images/{name}-960.webp" srcset="{srcset(name, HERO_W)}" '
            f'sizes="{sizes}" width="1200" height="800" alt="{alt}" fetchpriority="high" decoding="async"></figure>')


def photo(name, alt, sizes="(max-width: 860px) calc(100vw - 40px), 520px"):
    return (f'<figure class="photo"><img src="images/{name}-900.webp" srcset="{srcset(name, (600, 900))}" '
            f'sizes="{sizes}" width="900" height="675" alt="{alt}" loading="lazy" decoding="async"></figure>')


PERSON = {
    "@type": "Person", "@id": SITE + "#lily", "name": AUTHOR,
    "description": f"High school senior, painter and student researcher who created {SITE_NAME}, an art exhibit of cells, mitosis and protein synthesis.",
    "url": SITE + "#about",
}


def head(title, desc, path="", schema=None, hero=None, sizes=HOME_SIZES, preload_html=""):
    url = SITE + path
    graph = [{"@type": "WebSite", "@id": SITE + "#site", "url": SITE, "name": SITE_NAME,
              "description": "Paintings of cells, mitosis and protein synthesis that make biology easier to picture, with the research behind the project.",
              "author": {"@id": SITE + "#lily"}, "inLanguage": "en-US"}, PERSON]
    graph += schema or []
    preload = ""
    if hero:
        preload = (f'<link rel="preload" as="image" type="image/webp" href="images/{hero}-960.webp" '
                   f'imagesrcset="{srcset(hero, HERO_W)}" imagesizes="{sizes}" fetchpriority="high">\n')
    preload = preload or preload_html
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, separators=(",", ":"))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex,nofollow">
<link rel="canonical" href="{url}">
<meta name="author" content="{AUTHOR}">
<meta name="theme-color" content="#FFFFFF">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}images/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Lily Butler, the student artist behind Petri Palette, smiling outside a brick building">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
{preload}<link rel="preload" href="fonts/newsreader.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/public-sans.woff2" as="font" type="font/woff2" crossorigin>
<style>{css()}</style>
<script type="application/ld+json">{ld}</script>
</head>
<body>

<a class="skip" href="#main">Skip to content</a>
"""


def page_schema(kind, path, title, desc, extra=None):
    d = {"@type": kind, "@id": SITE + path + "#page", "url": SITE + path, "name": title, "headline": title,
         "description": desc, "isPartOf": {"@id": SITE + "#site"}, "author": {"@id": SITE + "#lily"},
         "inLanguage": "en-US", "datePublished": TODAY, "dateModified": TODAY,
         "image": SITE + "images/og.jpg"}
    d.update(extra or {})
    return d


def crumbs(name, path):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
        {"@type": "ListItem", "position": 2, "name": name, "item": SITE + path}]}


PAGES = [("index.html", "Home"), ("exhibit.html", "Exhibit"), ("artists.html", "Artists"), ("research.html", "Research"), ("about.html", "About")]


def wordmark():
    words = SITE_NAME.split()
    if len(words) > 1:
        return f'<span>{" ".join(words[:-1])} <span class="last">{words[-1]}</span></span>'
    return f"<span>{SITE_NAME}</span>"


def nav(current):
    lis = []
    for href, label in PAGES:
        cur = ' aria-current="page"' if href == current else ""
        lis.append(f'      <li><a href="{href}"{cur}>{label}</a></li>')
    return f"""<nav class="site" aria-label="Primary">
  <div class="wrap">
    <a class="wordmark" href="index.html">{MARK}{wordmark()}</a>
    <ul>
{chr(10).join(lis)}
    </ul>
  </div>
</nav>
"""


def foot():
    lis = "\n".join(f'      <li><a href="{h}">{l}</a></li>' for h, l in PAGES)
    return f"""
<footer>
  <div class="wrap">
    <p>I'm {AUTHOR}, and {SITE_NAME} is my art and science project. My research figures come from the Nation's Report Card, the OECD and peer-reviewed studies, cited on each page.</p>
    <ul>
{lis}
    </ul>
  </div>
</footer>

</body>
</html>
"""


def sources(keys, heading="Sources", note=""):
    lis = "\n".join(f"      <li>{SOURCES[k]}</li>" for k in keys)
    note = f'\n    <p class="cite-line">{note}</p>' if note else ""
    return f"""
<section class="refs" id="sources">
  <div class="wrap">
    <h2>{heading}</h2>
    <ol>
{lis}
    </ol>{note}
  </div>
</section>
"""


def cta(heading, text, href, label, second=None):
    extra = f'<a href="{second[0]}" class="btn ghost">{second[1]}</a>' if second else ""
    return f"""
<section class="closing">
  <div class="wrap">
    <h2>{heading}</h2>
    <p>{text}</p>
    <div class="btn-row"><a href="{href}" class="btn">{label}</a>{extra}</div>
  </div>
</section>
"""


# ---------------------------------------------------------------- icons
def svg(body, vb="0 0 48 48", sw="2.6"):
    return (f'<svg viewBox="{vb}" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{body}</svg>')


# A petri dish holding three dabs of paint in colors from Lily's paintings.
DISH = ('<rect width="32" height="32" rx="9" fill="#1F3D63"/>'
        '<circle cx="16" cy="16" r="10.5" fill="none" stroke="#EEF2F6" stroke-width="2"/>'
        '<circle cx="12.6" cy="13.4" r="3.1" fill="#E8C77A"/><circle cx="19.6" cy="12.8" r="2.6" fill="#E0533A"/>'
        '<circle cx="16.6" cy="19.8" r="3" fill="#5BB4E0"/>')
MARK = f'<svg class="mark" viewBox="0 0 32 32" aria-hidden="true">{DISH}</svg>'
ICON_SCORE = svg('<path d="M6 40h36"/><path d="M10 34V20M20 34V12M30 34v-8M40 34v-4"/><path d="M8 10l12 6 10 10 10 4"/>')
ICON_SPARK = svg('<circle cx="24" cy="24" r="17"/><path d="M17 30c2 -2 4.5-3 7-3s5 1 7 3"/><path d="M18 19v1M30 19v1"/>')
ICON_EYE = svg('<path d="M4 24s7-12 20-12 20 12 20 12-7 12-20 12S4 24 4 24z"/><circle cx="24" cy="24" r="6"/>')
ICON_GOGGLES = svg('<path d="M4 22c0-4 3-6 7-6h26c4 0 7 2 7 6v4c0 4-3 6-7 6h-6c-3 0-4-4-7-4s-4 4-7 4h-6c-4 0-7-2-7-6z"/><circle cx="14" cy="24" r="4"/><circle cx="34" cy="24" r="4"/>')
ICON_SPLIT = svg('<path d="M24 8c-8 0-14 7-14 16s6 16 14 16"/><path d="M24 8c8 0 14 7 14 16s-6 16-14 16"/><path d="M24 12v24" stroke-dasharray="3 4"/>')
ICON_HELIX = svg('<path d="M14 6c0 12 20 12 20 24S14 42 14 42"/><path d="M34 6c0 12-20 12-20 24s20 12 20 12"/><path d="M17 12h14M20 18h8M20 30h8M17 36h14"/>')
ICON_BRUSH = svg('<path d="M30 8l10 10-16 16-10-10z"/><path d="M14 24c-6 0-8 4-8 8 0 3-1 6-2 8 6 0 14-1 16-7"/><path d="M26 12l10 10"/>')
ICON_SCOPE = svg('<path d="M20 6l8 4-8 16-8-4z"/><path d="M22 26c6 2 10 7 10 12"/><path d="M8 42h32"/><path d="M14 36h20"/><circle cx="34" cy="20" r="3"/>')
ICON_DISH = svg('<ellipse cx="24" cy="28" rx="19" ry="9"/><path d="M5 28v4c0 5 8.5 9 19 9s19-4 19-9v-4"/><circle cx="17" cy="27" r="2.6"/><circle cx="27" cy="25" r="2"/><circle cx="30" cy="30" r="2.4"/>')
ICON_BALL = svg('<circle cx="24" cy="24" r="18"/><path d="M24 15l7 5-3 8h-8l-3-8z"/><path d="M24 6v9M31 20l9-4M28 28l6 8M20 28l-6 8M17 20l-9-4"/>')
ICON_PAW = svg('<ellipse cx="24" cy="32" rx="8" ry="7"/><circle cx="12.5" cy="21" r="3.6"/><circle cx="19.5" cy="12.5" r="3.6"/><circle cx="28.5" cy="12.5" r="3.6"/><circle cx="35.5" cy="21" r="3.6"/>')
ICON_COLUMN = svg('<path d="M9 13h30M12 13l12-7 12 7"/><path d="M13 17h22M16 17v19M24 17v19M32 17v19"/><path d="M12 36h24M9 41h30"/>')
CHECK = svg('<path d="M10 25l9 9 19-20"/>', sw="3.4")
CROSS = svg('<path d="M14 14l20 20M34 14L14 34"/>', sw="3.4")


# Line drawings that hold each frame until Lily's painting is scanned.
def chromo(x, y, r=0, s=1.0):
    return (f'<g transform="translate({x} {y}) rotate({r}) scale({s})">'
            f'<path d="M-4-7Q0 0 4 7M4-7Q0 0-4 7" stroke-width="3.2"/></g>')


def half(x, y, r=0):
    return f'<g transform="translate({x} {y}) rotate({r})"><path d="M-4-6Q0 0 4-6" stroke-width="3.2"/></g>'


def draw(kind):
    b = ""
    if kind == "cancer":
        b = ('<path d="M22 30c6-14 24-18 36-12s20 4 22 16-4 20 0 30-10 22-24 18-20 2-28-8-14-14-10-24 0-10 4-20z"/>'
             '<path d="M40 38c6-6 16-4 18 4s-2 16-10 16-14-12-8-20z" fill="currentColor" fill-opacity=".18"/>'
             '<circle cx="36" cy="66" r="5"/><circle cx="64" cy="30" r="4"/>')
    elif kind == "flat":
        for row, y in enumerate((30, 48, 66)):
            off = 11 if row % 2 else 0
            for x in (22, 44, 66):
                b += (f'<path d="M{x + off - 9} {y}l6-7h12l6 7-6 7h-12z"/>'
                      f'<ellipse cx="{x + off + 3}" cy="{y}" rx="3.5" ry="2" fill="currentColor" fill-opacity=".3"/>')
    elif kind == "sickle":
        b = ('<path d="M18 60c6 14 26 20 40 10 12-8 16-22 12-34-4 12-14 22-28 24-10 2-18 2-24 0z"/>'
             '<circle cx="34" cy="30" r="13"/><circle cx="34" cy="30" r="5" stroke-dasharray="2 3"/>'
             '<circle cx="74" cy="72" r="10"/><circle cx="74" cy="72" r="4" stroke-dasharray="2 3"/>')
    elif kind == "interphase":
        b = ('<circle cx="50" cy="50" r="40"/><circle cx="50" cy="50" r="22" fill="currentColor" fill-opacity=".08"/>'
             '<path d="M36 44c4-6 8 6 12 0s8 6 12 0M34 54c5 4 9-6 14-2s8 6 14 0M40 62c4-3 8 3 12 0s6-4 10 0" stroke-width="2"/>')
    elif kind == "prophase":
        b = ('<circle cx="50" cy="50" r="40"/><circle cx="50" cy="50" r="24" stroke-dasharray="3 5"/>'
             + chromo(40, 40, 20) + chromo(60, 44, -30) + chromo(46, 60, 70) + chromo(62, 62, 10)
             + '<path d="M14 50l8-6M14 50l8 6M86 50l-8-6M86 50l-8 6" stroke-width="1.6"/>')
    elif kind == "metaphase":
        b = ('<circle cx="50" cy="50" r="40"/><path d="M50 16v68" stroke-dasharray="2 4" stroke-width="1.4"/>'
             + "".join(chromo(50, y, 90) for y in (30, 43, 56, 69))
             + "".join(f'<path d="M14 50L44 {y}M86 50L56 {y}" stroke-width="1.4"/>' for y in (30, 43, 56, 69)))
    elif kind == "anaphase":
        b = ('<ellipse cx="50" cy="50" rx="44" ry="34"/>'
             + "".join(half(30, y, -90) + half(70, y, 90) for y in (34, 46, 58, 70))
             + "".join(f'<path d="M10 50L26 {y}M90 50L74 {y}" stroke-width="1.4"/>' for y in (34, 46, 58, 70)))
    elif kind == "telophase":
        b = ('<path d="M50 30c-6-12-20-16-32-8s-14 30 0 40 26 4 32-8c6 12 20 16 32 8s14-30 0-40-26-4-32 8z"/>'
             '<circle cx="28" cy="46" r="12" fill="currentColor" fill-opacity=".1"/><circle cx="72" cy="46" r="12" fill="currentColor" fill-opacity=".1"/>'
             '<path d="M22 44c3-3 6 3 9 0s4-2 6 0M66 44c3-3 6 3 9 0s4-2 6 0" stroke-width="1.8"/>')
    elif kind == "dna":
        b = ('<path d="M24 10c0 20 30 20 30 40s-30 20-30 40"/><path d="M54 10c0 20-30 20-30 40"/>'
             '<path d="M30 18h18M34 26h10M34 74h10M30 82h18"/>'
             '<path d="M54 50c8 0 12 6 22 6" stroke-dasharray="1 0"/><path d="M60 56v6M66 57v6M72 57v6" stroke-width="2"/>')
    elif kind == "mrna":
        b = ('<circle cx="34" cy="40" r="24" stroke-dasharray="4 4"/>'
             '<path d="M40 44c10 6 18-6 28 2s10 18 22 18" />'
             '<path d="M48 50v6M56 48v6M64 46v6M72 52v6M80 60v6" stroke-width="2"/>')
    elif kind == "ribosome":
        b = ('<ellipse cx="50" cy="40" rx="24" ry="14" fill="currentColor" fill-opacity=".1"/>'
             '<ellipse cx="50" cy="60" rx="30" ry="12" fill="currentColor" fill-opacity=".1"/>'
             '<path d="M8 52h84" stroke-width="2"/>'
             '<path d="M50 26c-4-6 2-10 0-14s6-6 6-10" stroke-width="2"/>'
             '<circle cx="50" cy="12" r="3"/><circle cx="56" cy="4" r="3"/>')
    return f'<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{b}</svg>'


def piece_html(p):
    if p["art"]:
        src, w, h = p["art"]
        frame = (f'<figure class="frame art" style="aspect-ratio:{w}/{h}"><img src="images/art/{src}" width="{w}" height="{h}" '
                 f'alt="My painting: {p["alt"]}" loading="lazy" decoding="async"></figure>')
    else:
        frame = f'<figure class="frame">{draw(p["draw"])}<figcaption class="soon">Painting coming soon</figcaption></figure>'
    see = f'\n          <p class="see">{p["see"]}</p>' if p["see"] else ""
    return f"""      <article class="piece" id="{p["id"]}">
        {frame}
        <div class="label">
          <h3>{p["title"]}</h3>
          <p class="meta">{p["meta"]}</p>
          <p>{p["text"]}</p>{see}
        </div>
      </article>"""


# ---------------------------------------------------------------- home
# Home hero: headline and one button, then Lily and her painting side by side.
TRIP_SIZES = "(max-width: 860px) 46vw, 320px"


def index():
    t = f"Science Art Exhibit: Paintings of Cells and Mitosis | {SITE_NAME}"
    d = ("My paintings of the stages of mitosis and the path from gene to protein, "
         "made to help students picture the biology they are asked to learn.")
    schema = [page_schema("WebPage", "", t, d, {"about": "Science art for biology education"})]
    pre = ('<link rel="preload" as="image" type="image/webp" href="images/lily-column-800.webp" '
           'imagesrcset="images/lily-column-480.webp 480w, images/lily-column-680.webp 680w, images/lily-column-800.webp 800w" '
           f'imagesizes="{TRIP_SIZES}" fetchpriority="high">\n')
    return head(t, d, "", schema, preload_html=pre) + nav("index.html") + f"""
<main id="main">

<header class="studio-hero">
  <div class="wrap hero2">
    <div class="hero2-text">
      <h1>Paintings that help students remember cell biology</h1>
      <div class="btn-row center">
        <a href="exhibit.html" class="btn light">Walk through the exhibit</a>
      </div>
    </div>
    <div class="diptych">
      <figure class="trip-photo"><img src="images/lily-column-800.webp" srcset="images/lily-column-480.webp 480w, images/lily-column-680.webp 680w, images/lily-column-800.webp 800w" sizes="{TRIP_SIZES}" width="800" height="1000" alt="Lily Butler, the student artist behind Petri Palette, in a white top, leaning against a white column and smiling" fetchpriority="high" decoding="async"></figure>
      <figure class="canvas"><img src="images/art/dna-helix.webp" srcset="images/art/dna-helix-520.webp 520w, images/art/dna-helix.webp 711w" sizes="{TRIP_SIZES}" width="711" height="890" alt="My painting of a gold DNA double helix unzipping across a blue cloud" decoding="async"></figure>
    </div>
  </div>
</header>

<section id="problem" class="band">
  <div class="wrap">
    <div class="section-head center">
      <h2>Students across the country are losing interest in science</h2>
      <p>Somewhere in middle school, science turns into things too small to see, and too many students decide it is not for them.</p>
    </div>
    <div class="cards">
      <div class="card">
        <div class="icon">{ICON_SCORE}</div>
        <p class="num">38%</p>
        <h3>Science scores have slid back to 2009</h3>
        <p>The average eighth grade science score fell 4 points between 2019 and 2024. The share scoring below NAEP Basic is the highest since 2011.</p>
        <p class="of">of U.S. eighth graders scored below Basic in science in 2024</p>
      </div>
      <div class="card">
        <div class="icon">{ICON_SPARK}</div>
        <p class="num">42%</p>
        <h3>Students decide science is not for them</h3>
        <p>In 2019, 52% of eighth graders said they enjoyed science activities. By 2024 it was 42%, and interest in what they learn in science class fell from 47% to 39%.</p>
        <p class="of">of eighth graders say they enjoy science activities</p>
      </div>
      <div class="card">
        <div class="icon">{ICON_EYE}</div>
        <p class="num">&minus;5 pts</p>
        <h3>Every student deserves to see what they are learning</h3>
        <p>Cells, chromosomes and proteins are invisible to the eye, and fewer eighth graders now say they often use experimental evidence to explain why something happens. Too much of biology arrives as words with nothing to look at.</p>
        <p class="of">drop since 2019 in students who often use evidence from experiments</p>
      </div>
    </div>
  </div>
</section>

<section id="about">
  <div class="wrap split">
    <div class="about-text">
      <h2>Why I paint the inside of the cell</h2>
      <p>I'm a senior at Episcopal Collegiate School in Little Rock. When I read the research on why students give up on science, it kept pointing to one moment: biology moves inside the cell, nothing can be seen anymore, and class turns into memorizing words.</p>
      <p>So I paint that part. My notes for mitosis read like stage directions: stringy and jumbled for interphase, loose and floaty for prophase, bouncy for anaphase, pinched for telophase. The summer before senior year I studied melanoma in a cancer research lab at UAMS, and in ninth grade one of my paintings was shown at the Arkansas Museum of Fine Arts. Petri Palette is where those two halves meet.</p>
      <div class="btn-row center"><a href="about.html" class="btn ghost">More about me</a></div>
    </div>
    <figure class="frame art about-art" style="aspect-ratio:711/890"><img src="images/art/dna-helix.webp" width="711" height="890" alt="My painting of a gold DNA double helix unzipping across a blue cloud" loading="lazy" decoding="async"></figure>
  </div>
</section>

<section id="plan" class="band">
  <div class="wrap">
    <div class="section-head center">
      <h2>How to learn a cell by looking at it first</h2>
      <p>Three steps turn a vocabulary list into a picture you can remember.</p>
    </div>
    <ol class="steps">
      <li>
        <h3>Look at the painting</h3>
        <p>Start with the shapes and colors. Notice what looks crowded, bent, split or stretched before you read a single word.</p>
      </li>
      <li>
        <h3>Read the title card</h3>
        <p>Every painting has a short card that names the cell or stage and explains what is happening in plain language.</p>
      </li>
      <li>
        <h3>Take the picture back to class</h3>
        <p>Next time your biology teacher brings up mitosis or protein synthesis, you will already have an image to hang the terms on.</p>
      </li>
    </ol>
    <div class="btn-row center">
      <a href="exhibit.html" class="btn">Walk through the exhibit</a>
    </div>
  </div>
</section>

<section id="series">
  <div class="wrap">
    <div class="section-head center">
      <h2>Two series of science paintings</h2>
      <p>My exhibit follows one cell becoming two, then a gene becoming a protein.</p>
    </div>
    <div class="cards two">
      <a class="card" href="exhibit.html#mitosis">
        <div class="icon">{ICON_SPLIT}</div>
        <h3>Mitosis</h3>
        <p>Interphase, prophase, metaphase, anaphase and telophase, painted stage by stage.</p>
      </a>
      <a class="card" href="exhibit.html#protein-transcription">
        <div class="icon">{ICON_HELIX}</div>
        <h3>Protein Transcription</h3>
        <p>How a gene's DNA is copied into RNA, built into a protein and packaged by the Golgi apparatus.</p>
      </a>
    </div>
  </div>
</section>

<section id="stakes" class="after">
  <div class="wrap">
    <div class="section-head center">
      <h2>What changes when students can see the science</h2>
    </div>
    <div class="stakes">
      <div class="stake">
        <h3>When cells stay invisible</h3>
        <ul class="outcomes">
          <li>{CROSS}<span>Biology turns into a list of words to memorize the night before a test.</span></li>
          <li>{CROSS}<span>Students decide they are not science people and stop signing up for science classes.</span></li>
          <li>{CROSS}<span>Careers in medicine and research start to feel out of reach.</span></li>
        </ul>
      </div>
      <div class="stake good">
        <h3>When you can picture them</h3>
        <ul class="outcomes">
          <li>{CHECK}<span>You remember what happens in each stage of mitosis because you have seen it.</span></li>
          <li>{CHECK}<span>You walk into biology class with an image for every term.</span></li>
          <li>{CHECK}<span>You start to see science as something you can understand and enjoy.</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>
""" + cta("From one cell splitting in two to a gene becoming a protein",
          f"{WORDS.get(N_PIECES, N_PIECES).capitalize()} paintings, each with a title card that explains the science in a minute or less.",
          "exhibit.html", "Walk through the exhibit", ("artists.html", "Meet the artists who paint cells")) + sources(["nagb", "edsource"]) + "\n</main>\n" + foot()


# ---------------------------------------------------------------- exhibit
def exhibit():
    t = f"Cell Paintings: The Stages of Mitosis and Protein Synthesis | {SITE_NAME}"
    d = ("My science art exhibit: paintings of "
         "the five stages of mitosis and protein synthesis, each with a plain-language title card.")
    items = [{"@type": "ListItem", "position": i, "name": p["title"], "url": SITE + "exhibit.html#" + p["id"]}
             for i, p in enumerate((p for s in SERIES for p in s["pieces"]), 1)]
    schema = [page_schema("CollectionPage", "exhibit.html", t, d,
                          {"mainEntity": {"@type": "ItemList", "itemListElement": items}}),
              crumbs("The Exhibit", "exhibit.html")]
    walls = []
    for s in SERIES:
        cls = {5: "wall five", 2: "wall two"}.get(len(s["pieces"]), "wall")
        band = ' band' if s["id"] == "mitosis" else ""
        walls.append(f"""
<section class="series{band}" id="{s["id"]}">
  <div class="wrap">
    <div class="section-head center">
      <h2>{s["name"]}</h2>
      <p>{s["intro"]}</p>
    </div>
    <div class="{cls}">
{chr(10).join(piece_html(p) for p in s["pieces"])}
    </div>
  </div>
</section>""")
    return head(t, d, "exhibit.html", schema, hero="hero-bright-gallery", sizes=PAGE_SIZES) + nav("exhibit.html") + f"""
<main id="main">

<header class="page-hero">
  <div class="wrap split">
    <div>
      <h1>Mitosis and protein synthesis, painted</h1>
      <p class="lede">My {WORDS[N_PIECES]} paintings, in {WORDS[len(SERIES)]} series. Read each title card beside its painting, the way you would in a museum.</p>
      <div class="btn-row center">
        <a href="#mitosis" class="btn">Start with mitosis</a>
      </div>
    </div>
    {hero_img("hero-bright-gallery", "A visitor standing in a bright gallery, looking at a wall of colorful paintings", PAGE_SIZES)}
  </div>
</header>
{"".join(walls)}
""" + cta("Eighth graders who enjoy science fell from 52% to 42%",
          "That drop happened between 2019 and 2024. See the research that shaped my exhibit and what studies say about learning science through art.",
          "research.html", "Read the research") + "\n</main>\n" + foot()


# ---------------------------------------------------------------- artists
# The Artists page: a digital exhibit of the genre Petri Palette belongs to.
# Every image is public domain or openly licensed, credited in plain text.
# Artists whose work is all rights reserved are described in words only
# (MORE_ARTISTS) until Lily has their permission to show an image.
ARTISTS_HERO = "hero-gallery-visitor"
ARTISTS_HERO_ALT = "A young woman in a bright gallery studying a framed painting on the wall"
ARTISTS_HERO_CREDIT = "Pauline Loroy, Unsplash."
ARTISTS_H1 = "Artists have painted cells for more than 350 years"
ARTISTS_LEDE = ("My paintings belong to a genre called science art, or SciArt, that began with a drawing of cork in 1665. "
                "In this gallery I gathered the scientists and artists who paint cells, microbes and the molecules inside them, "
                "and wrote a title card for every piece.")

WHY_HEAD = "Biology learned what cells look like from drawings"
WHY_LEDE = "Before cameras could be fitted to microscopes, a drawing was the only way to show anyone else what a cell looked like."
WHY = [
    {"icon": ICON_SCOPE, "title": "Drawings came first",
     "text": "Robert Hooke's 1665 drawing of cork gave biology the word cell. Santiago Ram&oacute;n y Cajal's drawings of nerve cells, "
             "made for work that shared the 1906 Nobel Prize in Physiology or Medicine, are still in use today."},
    {"icon": ICON_HELIX, "title": "Scientists still paint",
     "text": "David Goodsell holds a PhD in biochemistry, Greg Dunn a doctorate in neuroscience, and Hunter Cole a PhD in genetics. "
             "Each one turns what they know from the lab into art."},
    {"icon": ICON_EYE, "title": "Pictures help science stick",
     "text": "In a randomized study of fifth graders, science units taught with the arts built in led to better retention two months "
             "later for students reading below grade level."},
]

PAIR_MITOSIS = ("exhibit.html#mitosis", "Mitosis series")
GENRE = [
    {"id": "drawn-at-the-microscope", "name": "Drawn at the microscope",
     "intro": "The first pictures of cells were made by scientists who looked through a lens and drew what they saw. Their drawings taught the world what a cell looks like.",
     "pieces": [
         {"id": "hooke-cork", "img": ("hooke-cork", 1000, 996), "title": "Cork, from Micrographia",
          "artist": "Robert Hooke", "date": "1665, printed plate",
          "alt": "Hooke's drawing of two slices of cork inside a black circle, one showing rows of small boxes and the other a honeycomb of round holes",
          "text": "Hooke was apprenticed to a painter at 13 before he turned to science, and he drew the plates for his book himself. In a thin slice of cork he saw rows of tiny boxes that reminded him of the small rooms in a monastery, and he called them cells. The word stuck.",
          "credit": "Public domain",
          "source": "Robert Hooke, Micrographia (1665), Schem. XI. Scan: National Library of Wales. Public domain, via Wikimedia Commons."},
         {"id": "flemming-mitosis", "img": ("flemming-mitosis", 680, 965), "title": "Cell Division, Plate IIIb",
          "artist": "Walther Flemming", "date": "1882, printed plate",
          "alt": "Flemming's drawings of dividing cells, with dark thread-like chromosomes gathering, lining up, pulling apart and finally splitting into two cells",
          "text": "Flemming drew dividing cells stage by stage, from chromosomes bunched in the middle to a cell pinching in two. In the same book he named the process mitosis, from the Greek word for thread.",
          "pair": PAIR_MITOSIS, "credit": "CC BY 4.0, Wellcome Collection",
          "source": "Walther Flemming, Zellsubstanz, Kern und Zelltheilung (1882), Tafel IIIb, cropped from the two-page spread. Wellcome Collection, CC BY 4.0, via Wikimedia Commons."},
         {"id": "cajal-purkinje", "img": ("cajal-purkinje", 1000, 660), "title": "Purkinje Neurons",
          "artist": "Santiago Ram&oacute;n y Cajal", "date": "about 1900, drawing",
          "alt": "Cajal's drawing of dark nerve cells with long tails and tangled branches on yellowed paper, labeled with letters",
          "text": "Cajal, a Spanish physician and keen painter, stained brain tissue so single nerve cells turned black, then drew them. Purkinje neurons sit in the cerebellum, the part of the brain that coordinates movement. Cajal shared the 1906 Nobel Prize with Camillo Golgi, the scientist the Golgi apparatus is named after.",
          "pair": ("exhibit.html#golgi-apparatus", "Golgi Apparatus painting"), "credit": "Public domain",
          "source": "Santiago Ram&oacute;n y Cajal, Purkinje neurons, about 1900. Cajal Institute (CSIC), Madrid. Public domain, via Wikimedia Commons."},
     ]},
    {"id": "inside-the-cell", "name": "Painting the inside of a cell",
     "intro": "Scientist painters today work from research data and lab images to show what no single microscope picture can: a whole cell, with every part in its place.",
     "pieces": [
         {"id": "goodsell-ecoli", "img": ("goodsell-ecoli", 1000, 1000), "title": "Escherichia coli Bacterium",
          "artist": "David S. Goodsell", "date": "2021, watercolor",
          "alt": "Goodsell's watercolor cross-section of a bacterium: a green cell wall, a yellow tangle of DNA, and crowds of purple, blue and orange molecules",
          "text": "Goodsell, a biochemist at Scripps Research, paints part of a living cell magnified about a million times, with molecules placed from research data. Here an E. coli cell is cut open: the green wall, the yellow tangle of DNA, and reddish purple ribosomes that build proteins.",
          "pair": ("exhibit.html#protein-transcription", "Protein Transcription series"), "credit": "CC BY 4.0, RCSB Protein Data Bank",
          "source": "Illustration by David S. Goodsell, RCSB Protein Data Bank. doi: 10.2210/rcsb_pdb/goodsell-gallery-028. CC BY 4.0."},
         {"id": "goodsell-mycoplasma", "img": ("goodsell-mycoplasma", 1000, 975), "title": "Mycoplasma mycoides",
          "artist": "David S. Goodsell", "date": "2011, watercolor",
          "alt": "Goodsell's watercolor of a whole round bacterial cell with a fuzzy green edge, packed inside with yellow strands and pink and blue molecules",
          "text": "This painting shows an entire bacterial cell about 300 nanometers across, small enough that a thousand of them in a row would still be thinner than a credit card is thick.",
          "credit": "CC BY 4.0, RCSB Protein Data Bank",
          "source": "Illustration by David S. Goodsell, The Scripps Research Institute. doi: 10.2210/rcsb_pdb/goodsell-gallery-011. CC BY 4.0."},
         {"id": "harris-retina", "img": ("harris-retina", 1000, 1243), "title": "Cell Fates in Zebrafish Retina",
          "artist": "Prof. Bill Harris", "date": "acrylic painting",
          "alt": "A bright acrylic painting of rows of cells in three layers, each cell outlined in a different color with a colored nucleus",
          "text": "An impression of a nearly mature zebrafish retina, its cells settled into three layers and colored by type. The painting was inspired by the multicolored fluorescent proteins researchers use to label different kinds of cells.",
          "credit": "CC BY 4.0, Wellcome Collection",
          "source": "Cell fates in zebrafish retina, acrylic painting. Prof. Bill Harris. CC BY 4.0. Source: Wellcome Collection."},
     ]},
    {"id": "cells-as-fine-art", "name": "Cells as fine art",
     "intro": "Some painters treat cells the way other artists treat landscapes and portraits, choosing them for their color, shape and drama.",
     "pieces": [
         {"id": "noel-t-cell", "img": ("noel-t-cell", 1000, 1001), "title": "St George and the Dragon",
          "artist": "Odra Noel", "date": "paint on silk",
          "alt": "A pale blue immune cell reaching out to a green cancer cell on a background of swirling peach tissue",
          "text": "Noel trained as a doctor and earned a PhD in basic science before she began painting cells on silk. Here a killer T cell, one of the immune system's defenders, destroys a cancer cell, cast as the knight and the dragon.",
          "credit": "CC BY-NC 4.0, Wellcome Collection",
          "source": "St George and the dragon: T lymphocyte killing a cancer cell. Odra Noel. CC BY-NC 4.0. Source: Wellcome Collection."},
         {"id": "noel-blood", "img": ("noel-blood", 1000, 1198), "title": "Blood Cells Through the Microscope",
          "artist": "Odra Noel", "date": "paint on silk",
          "alt": "Round magenta red blood cells drifting past a blue white blood cell on a pale yellow background",
          "text": "Part of this painting is what a microscope shows and part is the artist's impression of blood cells and the structures around them.",
          "credit": "CC BY-NC 4.0, Wellcome Collection",
          "source": "Blood cells through the microscope. Odra Noel. CC BY-NC 4.0. Source: Wellcome Collection."},
         {"id": "magrath-neurones", "img": ("magrath-neurones", 1000, 781), "title": "Neurones Connecting",
          "artist": "Stephen Magrath", "date": "ink on paper",
          "alt": "Two deep blue nerve cells with pink centers reaching toward each other with long branching arms on white paper",
          "text": "Neurons are the cells of the nervous system, and they carry information as electrical signals. This painting shows two of them reaching toward each other, the way nerve cells connect to pass a message along.",
          "credit": "CC0, Wellcome Collection",
          "source": "Neurones connecting, artwork. Stephen Magrath. CC0 1.0. Source: Wellcome Collection."},
     ]},
]

AGAR = {"img": ("agar-butterfly", 1000, 1000),
        "alt": "A red butterfly grown from living microbes on the agar in a round glass petri dish",
        "source": "Microbial Art, Ajay Kumar Chaurasiya, 2021. CC BY-SA 4.0, via Wikimedia Commons. Cropped; the crop is shared under the same license."}

MORE_LEDE = "Their work is protected by copyright, so I describe it here in words. Every one of them is worth looking up."
MORE_ARTISTS = [
    {"name": "Klari Reis", "where": "Epoxy paintings in petri dishes, San Francisco",
     "text": "Reis pours dyed epoxy into plastic petri dishes and hangs them by the dozen. The work began after she was diagnosed with Crohn's disease and a doctor let her watch her own cells react to different drugs under a microscope."},
    {"name": "Michele Banks", "where": "Watercolor cells and viruses, Washington, DC",
     "text": "Banks lets wet watercolor bleed into branching patterns that look like blood vessels and brain cells. She has said her best known paintings are her images of mitosis."},
    {"name": "Greg Dunn", "where": "Neurons in ink and gold, Philadelphia",
     "text": "Dunn earned a doctorate in neuroscience and paints neurons in Japanese sumi-e ink, often on gold leaf. The style began by accident, when he blew on wet ink and it spread into shapes like nerve cells."},
    {"name": "Hunter Cole", "where": "Drawings in glowing bacteria, North Carolina",
     "text": "Cole, a geneticist, paints with bioluminescent bacteria on petri dishes. The drawings glow blue-green and fade over about two weeks as the bacteria run out of food, so she photographs them while they last."},
    {"name": "Luke Jerram", "where": "Glass sculptures of microbes, Bristol, England",
     "text": "Jerram, who is color-blind, designs clear glass sculptures of viruses and microbes with virologists. He leaves out color on purpose, to question the bright false colors in many pictures of microbes."},
    {"name": "Rogan Brown", "where": "Paper sculptures of microbes, France",
     "text": "Brown cuts layered paper into microbes and cells by hand or by laser. His sculpture Outbreak (2014) took about four months to plan, cut and assemble, and he names Ernst Haeckel as an inspiration."},
]

FITS_HEAD = "Where my paintings fit in"
FITS_BODY = """      <p>I'm Lily Butler, a high school senior, and Petri Palette is my small addition to this tradition. I paint the cell processes high school biology asks students to learn: the stages of mitosis and the path from gene to protein.</p>
      <p>Each of my paintings hangs beside a title card that explains the science in plain language. My painting of the Golgi apparatus, shown here, pictures the organelle named for Camillo Golgi, who shared the 1906 Nobel Prize with Cajal.</p>"""


def genre_piece(p):
    name, w, h = p["img"]
    pair = ""
    if p.get("pair"):
        pair = f'\n          <p class="see">Pairs with my <a href="{p["pair"][0]}">{p["pair"][1]}</a>.</p>'

    sizes = "(max-width: 620px) calc(100vw - 40px), (max-width: 900px) 45vw, 340px"
    return f"""      <article class="piece" id="{p["id"]}">
        <figure class="frame art" style="aspect-ratio:{w}/{h}"><img src="images/genre/{name}-600.webp" srcset="images/genre/{name}-600.webp 600w, images/genre/{name}-1000.webp {w}w" sizes="{sizes}" width="{w}" height="{h}" alt="{p["alt"]}" loading="lazy" decoding="async"></figure>
        <div class="label">
          <h3>{p["title"]}</h3>
          <p class="meta">{p["artist"]} &middot; {p["date"]}</p>
          <p>{p["text"]}</p>{pair}
          <p class="credit">{p["credit"]}</p>
        </div>
      </article>"""


def artists():
    t = f"Science Art: Artists Who Paint Cells and Microbes | {SITE_NAME}"
    d = ("A digital exhibit of science art, from Robert Hooke's 1665 drawing of cork cells to painters working today: "
         "the artists and scientists who paint cells, microbes and the molecules inside them.")
    items = [{"@type": "ListItem", "position": i, "name": f'{p["title"]}, {p["artist"]}', "url": SITE + "artists.html#" + p["id"]}
             for i, p in enumerate((p for r in GENRE for p in r["pieces"]), 1)]
    schema = [page_schema("CollectionPage", "artists.html", t, d,
                          {"mainEntity": {"@type": "ItemList", "itemListElement": items}}),
              crumbs("The Artists", "artists.html")]
    why = "\n".join(f"""      <div class="card">
        <div class="icon">{c["icon"]}</div>
        <h3>{c["title"]}</h3>
        <p>{c["text"]}</p>
      </div>""" for c in WHY)
    rooms = []
    for i, r in enumerate(GENRE):
        band = " band" if i % 2 else ""
        rooms.append(f"""
<section class="series{band}" id="{r["id"]}">
  <div class="wrap">
    <div class="section-head center">
      <h2>{r["name"]}</h2>
      <p>{r["intro"]}</p>
    </div>
    <div class="wall">
{chr(10).join(genre_piece(p) for p in r["pieces"])}
    </div>
  </div>
</section>""")
    more = "\n".join(f"""      <div class="card">
        <div class="icon">{ICON_BRUSH}</div>
        <h3>{a["name"]}</h3>
        <p class="where">{a["where"]}</p>
        <p>{a["text"]}</p>
      </div>""" for a in MORE_ARTISTS)
    credits = "\n".join(f'      <li>{p["source"]}</li>' for r in GENRE for p in r["pieces"])
    first = GENRE[0]["id"] if GENRE else ""
    return head(t, d, "artists.html", schema, hero=ARTISTS_HERO, sizes=PAGE_SIZES) + nav("artists.html") + f"""
<main id="main">

<header class="page-hero">
  <div class="wrap split">
    <div>
      <h1>{ARTISTS_H1}</h1>
      <p class="lede">{ARTISTS_LEDE}</p>
      <div class="btn-row center">
        <a href="#{first}" class="btn">Walk through the gallery</a>
      </div>
    </div>
    {hero_img(ARTISTS_HERO, ARTISTS_HERO_ALT, PAGE_SIZES)}
  </div>
</header>

<section id="why" class="band">
  <div class="wrap">
    <div class="section-head center">
      <h2>{WHY_HEAD}</h2>
      <p>{WHY_LEDE}</p>
    </div>
    <div class="cards">
{why}
    </div>
  </div>
</section>
{"".join(rooms)}

<section id="petri-dish-art" class="band">
  <div class="wrap split">
    <figure class="frame art about-art" style="aspect-ratio:1/1"><img src="images/genre/agar-butterfly-600.webp" srcset="images/genre/agar-butterfly-600.webp 600w, images/genre/agar-butterfly-1000.webp 1000w" sizes="(max-width: 620px) calc(100vw - 40px), 400px" width="1000" height="1000" alt="{AGAR["alt"]}" loading="lazy" decoding="async"></figure>
    <div>
      <h2>When the petri dish becomes the palette</h2>
      <p>Microbiologists paint too, with living microbes for paint and a petri dish of agar for a canvas. Ajay Kumar Chaurasiya grew this butterfly in 2021. Alexander Fleming, who discovered penicillin, made germ paintings on agar with colored bacteria, and since 2015 the American Society for Microbiology has run an Agar Art contest. Its 2024 contest drew a record 445 entries.</p>
      <p class="cite-line">Sources: American Society for Microbiology, Agar Art contest results, 2024; Hektoen International, Sir Alexander Fleming, 2020.</p>
    </div>
  </div>
</section>

<section id="more-artists">
  <div class="wrap">
    <div class="section-head center">
      <h2>More artists working in the genre</h2>
      <p>{MORE_LEDE}</p>
    </div>
    <div class="cards">
{more}
    </div>
  </div>
</section>

<section id="lily" class="band">
  <div class="wrap split flip">
    <figure class="frame art about-art" style="aspect-ratio:713/694"><img src="images/art/golgi-apparatus.webp" width="713" height="694" alt="My painting of the Golgi apparatus: stacked dark and red-orange sacs on a teal background, ringed by round vesicles" loading="lazy" decoding="async"></figure>
    <div>
      <h2>{FITS_HEAD}</h2>
{FITS_BODY}
    </div>
  </div>
</section>
""" + cta(f"{WORDS.get(N_PIECES, N_PIECES).capitalize()} paintings of the cells biology class teaches",
          "The stages of mitosis and the path from gene to protein, each with a title card I wrote.",
          "exhibit.html", "Walk through the exhibit", ("research.html", "Read the research")) + f"""
<section class="refs" id="credits">
  <div class="wrap">
    <h2>Image credits</h2>
    <ol>
{credits}
      <li>{AGAR["source"]}</li>
      <li>Photo at the top of the page: {ARTISTS_HERO_CREDIT}</li>
    </ol>
  </div>
</section>
</main>
""" + foot()


# ---------------------------------------------------------------- about
LILY_SIZES = "(max-width: 860px) min(calc(100vw - 40px), 400px), 440px"


def portrait(name, alt, cls="photo portrait", eager=False):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<figure class="{cls}"><img src="images/{name}-800.webp" srcset="images/{name}-480.webp 480w, images/{name}-680.webp 680w, images/{name}-800.webp 800w" '
            f'sizes="{LILY_SIZES}" width="800" height="1000" alt="{alt}" {load} decoding="async"></figure>')


# Scroll depth for the About hero: elements with data-depth drift by scrollY * depth.
PARALLAX_JS = """<script>
(()=>{if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
const els=[...document.querySelectorAll('[data-depth]')];let t=0;
const f=()=>{t=0;const y=Math.min(scrollY,700);for(const e of els)e.style.translate='0 '+(y*e.dataset.depth).toFixed(1)+'px'};
addEventListener('scroll',()=>{if(!t)t=requestAnimationFrame(f)},{passive:true});})();
</script>"""


def about():
    t = f"About Me: {AUTHOR}, Student Painter and Researcher | {SITE_NAME}"
    d = ("I'm Lily Butler. Biology class asks students to learn cells they have never seen, so I paint them, "
         "one stage at a time, with a title card that explains each one.")
    schema = [page_schema("AboutPage", "about.html", t, d, {"mainEntity": {"@id": SITE + "#lily"}}),
              crumbs("About", "about.html")]
    pre = ('<link rel="preload" as="image" type="image/webp" href="images/art/dna-helix.webp" '
           'imagesrcset="images/art/dna-helix-520.webp 520w, images/art/dna-helix.webp 711w" '
           'imagesizes="(max-width: 860px) 72vw, 470px" fetchpriority="high">\n')
    return head(t, d, "about.html", schema, preload_html=pre) + nav("about.html") + f"""
<main id="main">

<header class="studio-hero">
  <div class="wrap studio">
    <div class="studio-text">
      <h1>I paint the cells biology class asks students to memorize</h1>
      <p class="lede">I'm Lily Butler, a senior in Little Rock. Biology class asks students to learn cells they have never seen, so I paint them one stage at a time, and the next student who meets mitosis already has a picture of it.</p>
      <div class="btn-row center">
        <a href="exhibit.html" class="btn light">Walk through my exhibit</a>
      </div>
    </div>
    <div class="studio-art">
      <figure class="canvas" data-depth="0.05"><img src="images/art/dna-helix.webp" srcset="images/art/dna-helix-520.webp 520w, images/art/dna-helix.webp 711w" sizes="(max-width: 860px) 72vw, 470px" width="711" height="890" alt="My painting of a gold DNA double helix unzipping across a blue cloud" fetchpriority="high" decoding="async"></figure>
      <p class="studio-card" data-depth="-0.05"><strong>DNA to RNA</strong><span>From my Protein Transcription series</span></p>
    </div>
  </div>
</header>
{PARALLAX_JS}

<section id="story">
  <div class="wrap split flip">
    {portrait("lily-wall", "Lily Butler in a blue floral dress, sitting on a stone wall in a park and smiling")}
    <div>
      <h2>How Petri Palette started</h2>
      <p>Before I painted anything, I read the research on why students give up on science. It kept pointing to the same moment. Biology is easy to like while it is about hearts, frogs and weather. Then it moves inside the cell, into chromosomes and proteins nobody can see, and class turns into memorizing words.</p>
      <p>The summer before my senior year, I spent six weeks in a cancer research lab at UAMS, studying melanoma and the part of the cell that folds new proteins. When I plan a painting now, I write down how it should feel: interphase is stringy and jumbled, prophase is loose and floaty, anaphase is bouncy, telophase is pinched. Then I write a title card short enough to read in a minute.</p>
    </div>
  </div>
</section>
""" + cta(f"{WORDS[N_PIECES].capitalize()} paintings, one title card each",
          "The stages of mitosis and the path from gene to protein.",
          "exhibit.html", "Walk through my exhibit", ("artists.html", "Meet the artists who paint cells")) + "\n</main>\n" + foot()


# ---------------------------------------------------------------- research
def bars(rows):
    out = []
    for label, a, b in rows:
        out.append(f"""        <div class="row">
          <h4>{label}</h4>
          <div class="pair">
            <div class="barline"><span>2019</span><div class="track"><span class="bar y19" style="width:{a}%" title="2019: {a}%">{a}%</span></div></div>
            <div class="barline"><span>2024</span><div class="track"><span class="bar y24" style="width:{b}%" title="2024: {b}%">{b}%</span></div></div>
          </div>
        </div>""")
    return "\n".join(out)


def research():
    t = f"How Art Can Keep Students Interested in Science | {SITE_NAME}"
    d = ("What the 2024 Nation's Report Card says about eighth grade science scores and enjoyment, why interest drops as "
         "science turns abstract, and what studies show about learning science through art and drawing.")
    schema = [page_schema("Article", "research.html", t, d, {"about": "Student engagement in science education"}),
              crumbs("The Research", "research.html")]
    return head(t, d, "research.html", schema, hero="hero-boy-painting", sizes=PAGE_SIZES) + nav("research.html") + f"""
<main id="main">

<header class="page-hero">
  <div class="wrap split">
    <div>
      <h1>How art can keep students interested in science</h1>
      <p class="lede">Before painting a single cell, I looked at what national test data and education research say about students and science. Here is what I found.</p>
    </div>
    {hero_img("hero-boy-painting", "A boy in a dark hoodie standing close to a large painting in a museum", PAGE_SIZES)}
  </div>
</header>

<section id="scores" class="band">
  <div class="wrap">
    <div class="section-head center">
      <h2>Eighth grade science scores are the lowest in fifteen years</h2>
      <p>The Nation's Report Card tested eighth grade science in 2024 for the first time since the pandemic.</p>
    </div>
    <div class="cards">
      <div class="card">
        <p class="num">&minus;4</p>
        <h3>Points lost since 2019</h3>
        <p>The average score is now equal to the 2009 average.</p>
      </div>
      <div class="card">
        <p class="num">38%</p>
        <h3>Below NAEP Basic</h3>
        <p>The highest share of eighth graders below Basic since 2011.</p>
      </div>
      <div class="card">
        <p class="num">Record low</p>
        <h3>For struggling students</h3>
        <p>Scores at the 10th and 25th percentiles were the lowest ever reported, so the gap between the highest and lowest scorers is widening.</p>
      </div>
    </div>
    <p class="cite-line" style="text-align:center">Source: National Assessment Governing Board, 5 Things You Need to Know About NAEP Science Results.</p>
  </div>
</section>

<section id="enjoyment">
  <div class="wrap split">
    <figure class="chart">
      <h3>Eighth graders who enjoy science, 2019 and 2024</h3>
      <p class="sub">Share of students answering yes, from the NAEP student survey.</p>
      <ul class="legend"><li><i class="y19"></i>2019</li><li><i class="y24"></i>2024</li></ul>
      <div class="bars">
{bars([("Enjoy science activities", 52, 42), ("Interested in what they learn in science class", 47, 39)])}
      </div>
      <p class="cite-line">Source: EdSource (Emma Gallegos), reporting 2024 NAEP survey results, September 9, 2025.</p>
    </figure>
    <div>
      <h2>Fewer eighth graders enjoy science than in 2019</h2>
      <p>Scores were only half of the story. The same 2024 survey showed students losing interest: 10 points fewer said they enjoy science activities, and 8 points fewer said they are interested in what they learn in class.</p>
      <p>Fewer students also reported often doing the work scientists do. Using evidence from experiments to explain why something happens fell 5 percentage points from 2019, and using information to disagree about a scientific idea fell 4 points.</p>
    </div>
  </div>
</section>

<section id="abstract" class="band">
  <div class="wrap prose">
    <h2>Interest drops when science turns abstract</h2>
    <p>Students tend to like science early on, when it is about bodies, animals and weather they can see for themselves. A systematic review of twelve years of research found that interest in science and technology declines as students move up through school, and the decline grows clearer as students move into secondary school.</p>
    <p>That timing matches what changes in the classroom. Science shifts from things students can observe to mechanisms they cannot: chemical reactions, enzymes, chromosomes, DNA. Biology stays relatable while it is about the heart or a frog, and turns abstract once it moves inside the cell, which is exactly where this exhibit is set.</p>
    <p class="cite-line">Source: Potvin and Hasni, Studies in Science Education, 2014.</p>
    <div class="facts">
      <div class="fact">
        <h3>Math loss reaches biology too</h3>
        <p>Thirteen-year-olds' math scores dropped 9 points between 2020 and 2023 on the NAEP long-term trend test. Biology and chemistry lean on math, so that loss carries into science class.</p>
        <p class="cite-line">Source: NCES, NAEP Long-Term Trend, 2023.</p>
      </div>
      <div class="fact">
        <h3>Screens compete for attention</h3>
        <p>In PISA 2022, students who spent up to an hour a day on devices for fun scored 49 points higher in math than those who spent five to seven hours, and about 45% felt nervous without their phone nearby. The study shows a correlation and does not prove that screens cause lower scores.</p>
        <p class="cite-line">Source: OECD, PISA 2022 Results.</p>
      </div>
    </div>
  </div>
</section>

<section id="art">
  <div class="wrap split flip">
    {photo("watercolor", "A young student painting with watercolors at a table by a window")}
    <div>
      <h2>What studies say about learning science through art</h2>
      <p>Science art is a real area of education research. In a randomized study of fifth graders, units taught with the arts built in led to the same learning at first as regular science units, and better retention two months later for students who read below grade level.</p>
      <p>A 2011 paper in the journal Science argued that drawing belongs in science class next to reading, writing and talking, because scientists themselves think and explain with pictures.</p>
      <p class="cite-line">Sources: Hardiman, Rinne and Yarmolinskaya, Mind, Brain, and Education, 2014; Ainsworth, Prain and Tytler, Science, 2011.</p>
    </div>
  </div>
</section>
""" + cta("See the research turned into paintings",
          "Cells, chromosomes and proteins, painted at a size you can study.",
          "exhibit.html", "Walk through the exhibit") + sources(
        ["nagb", "edsource", "potvin", "ltt", "pisa", "hardiman", "ainsworth"],
        note="Photos: Unsplash (Eri Pan&ccedil;i, Caroline Badran, Egor Myznik, Trust Katsande, Madalyn Cox).") + "\n</main>\n" + foot()


def sitemap():
    urls = "\n".join(f"  <url><loc>{SITE}{'' if h == 'index.html' else h}</loc><lastmod>{TODAY}</lastmod></url>" for h, _ in PAGES)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n'


FAVICON = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">{DISH}</svg>\n'

if __name__ == "__main__":
    out = {"index.html": index, "exhibit.html": exhibit, "artists.html": artists, "research.html": research, "about.html": about}
    for name, fn in out.items():
        with open(name, "w") as f:
            f.write(fn())
        print("wrote", name)
    with open("sitemap.xml", "w") as f:
        f.write(sitemap())
    # Preview stays out of search until Lily approves the copy and the paintings are in.
    with open("robots.txt", "w") as f:
        f.write("User-agent: *\nDisallow: /\n")
    with open("favicon.svg", "w") as f:
        f.write(FAVICON)
    print("wrote sitemap.xml, robots.txt, favicon.svg")
