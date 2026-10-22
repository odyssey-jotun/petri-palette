#!/usr/bin/env python3
"""Builds every page of Science You Can See.

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
SITE_NAME = "Science You Can See"
AUTHOR = "Lily Butler"
SITE = "https://odyssey-jotun.github.io/science-you-can-see/"
TODAY = "2026-10-22"

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
    {"id": "goggle-series", "name": "The Goggle Series",
     "intro": "Three cells whose shape tells a story about health and disease, from cells that will not stop dividing to red blood cells bent out of shape.",
     "pieces": [
         {"id": "cancer-cells", "title": "Cancer Cells", "meta": "Goggles 1", "draw": "cancer", "art": None,
          "text": "Cancer cells keep dividing after the signals that stop healthy cells have shut off. Under a microscope they often look irregular, with large, uneven nuclei, and they crowd the healthy tissue around them.",
          "see": "Look for the uneven shapes and oversized nuclei."},
         {"id": "flat-cells", "title": "Flat Cells", "meta": "Goggles 2", "draw": "flat", "art": None,
          "text": "Flat cells, called squamous cells, are thin and shaped like scales. They line surfaces such as the outer layer of skin, the inside of the mouth and the tiny air sacs of the lungs.",
          "see": "Look for the thin, tile-like cells pressed edge to edge."},
         {"id": "sickle-cells", "title": "Sickle Cells", "meta": "Goggles 3", "draw": "sickle", "art": None,
          "text": "Healthy red blood cells are round, flexible discs. In sickle cell disease, an inherited change in the hemoglobin gene makes red blood cells stiff and curved like a crescent, so they can stick in small blood vessels and block blood flow.",
          "see": "Look for the crescent cells beside the round ones."},
     ]},
    {"id": "mitosis", "name": "Mitosis",
     "intro": "One cell becoming two, painted as five stages. Human cells carry 46 chromosomes, so the paintings show only a handful to keep each stage easy to read.",
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
     "intro": "How a gene becomes a protein. In the nucleus, a gene's DNA is copied into messenger RNA (transcription). A ribosome then reads that RNA and links amino acids into a protein (translation).",
     "pieces": [
         {"id": "protein-1", "title": "DNA to RNA", "meta": "Painting in progress", "draw": "dna", "art": None,
          "text": "Inside the nucleus, the DNA double helix unzips and one strand is copied into a single strand of messenger RNA.",
          "see": ""},
         {"id": "protein-2", "title": "Leaving the Nucleus", "meta": "Painting in progress", "draw": "mrna", "art": None,
          "text": "The messenger RNA travels out of the nucleus and into the cytoplasm, where the cell builds its proteins.",
          "see": ""},
         {"id": "protein-3", "title": "The Ribosome", "meta": "Painting in progress", "draw": "ribosome", "art": None,
          "text": "A ribosome reads the RNA three letters at a time and links one amino acid for each, folding the chain into a working protein.",
          "see": ""},
     ]},
]
N_PIECES = sum(len(s["pieces"]) for s in SERIES)
WORDS = {3: "three", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}

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


def head(title, desc, path="", schema=None, hero=None, sizes=HOME_SIZES):
    url = SITE + path
    graph = [{"@type": "WebSite", "@id": SITE + "#site", "url": SITE, "name": SITE_NAME,
              "description": "Paintings of cells, mitosis and protein synthesis that make biology easier to picture, with the research behind the project.",
              "author": {"@id": SITE + "#lily"}, "inLanguage": "en-US"}, PERSON]
    graph += schema or []
    preload = ""
    if hero:
        preload = (f'<link rel="preload" as="image" type="image/webp" href="images/{hero}-960.webp" '
                   f'imagesrcset="{srcset(hero, HERO_W)}" imagesizes="{sizes}" fetchpriority="high">\n')
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
<meta name="theme-color" content="#F6F4EF">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}images/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Two young visitors on a gallery bench looking at a painting">
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


PAGES = [("index.html", "Home"), ("exhibit.html", "The Exhibit"), ("research.html", "The Research")]


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
    <p>{SITE_NAME}, an art and science project by {AUTHOR}. Research figures come from the Nation's Report Card, the OECD and peer-reviewed studies, cited on each page.</p>
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


def cta(heading, text, href, label):
    return f"""
<section class="closing">
  <div class="wrap">
    <h2>{heading}</h2>
    <p>{text}</p>
    <div class="btn-row"><a href="{href}" class="btn">{label}</a></div>
  </div>
</section>
"""


# ---------------------------------------------------------------- icons
def svg(body, vb="0 0 48 48", sw="2.6"):
    return (f'<svg viewBox="{vb}" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{body}</svg>')


MARK = ('<svg class="mark" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="9" fill="#1F3D63"/>'
        '<circle cx="16" cy="16" r="9.5" fill="none" stroke="#EEF2F6" stroke-width="2"/>'
        '<circle cx="17.5" cy="14.5" r="3.6" fill="#E58AA6"/></svg>')
ICON_SCORE = svg('<path d="M6 40h36"/><path d="M10 34V20M20 34V12M30 34v-8M40 34v-4"/><path d="M8 10l12 6 10 10 10 4"/>')
ICON_SPARK = svg('<circle cx="24" cy="24" r="17"/><path d="M17 30c2 -2 4.5-3 7-3s5 1 7 3"/><path d="M18 19v1M30 19v1"/>')
ICON_EYE = svg('<path d="M4 24s7-12 20-12 20 12 20 12-7 12-20 12S4 24 4 24z"/><circle cx="24" cy="24" r="6"/>')
ICON_GOGGLES = svg('<path d="M4 22c0-4 3-6 7-6h26c4 0 7 2 7 6v4c0 4-3 6-7 6h-6c-3 0-4-4-7-4s-4 4-7 4h-6c-4 0-7-2-7-6z"/><circle cx="14" cy="24" r="4"/><circle cx="34" cy="24" r="4"/>')
ICON_SPLIT = svg('<path d="M24 8c-8 0-14 7-14 16s6 16 14 16"/><path d="M24 8c8 0 14 7 14 16s-6 16-14 16"/><path d="M24 12v24" stroke-dasharray="3 4"/>')
ICON_HELIX = svg('<path d="M14 6c0 12 20 12 20 24S14 42 14 42"/><path d="M34 6c0 12-20 12-20 24s20 12 20 12"/><path d="M17 12h14M20 18h8M20 30h8M17 36h14"/>')
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
        frame = (f'<figure class="frame art"><img src="images/art/{p["art"]}" width="960" height="1200" '
                 f'alt="{AUTHOR}\'s painting of {p["title"].lower()}" loading="lazy" decoding="async"></figure>')
    else:
        frame = f'<figure class="frame">{draw(p["draw"])}<figcaption class="soon">Painting coming soon</figcaption></figure>'
    see = f'\n          <p class="see">{p["see"]}</p>' if p["see"] else ""
    return f"""      <article class="piece" id="{p["id"]}">
        {frame}
        <div class="label">
          <h3>{p["title"]}</h3>
          <p class="meta">{p["meta"]} &middot; {AUTHOR}</p>
          <p>{p["text"]}</p>{see}
        </div>
      </article>"""


# ---------------------------------------------------------------- home
def index():
    t = f"Science Art Exhibit: Paintings of Cells and Mitosis | {SITE_NAME}"
    d = ("Paintings of cancer cells, sickle cells, the stages of mitosis and protein synthesis by student artist "
         f"{AUTHOR}, made to help students picture the biology they are asked to learn.")
    schema = [page_schema("WebPage", "", t, d, {"about": "Science art for biology education"})]
    return head(t, d, "", schema, hero="hero-gallery-bench") + nav("index.html") + f"""
<main id="main">

<header class="hero">
  <div class="wrap">
    <div class="hero-text">
      <h1>Paintings that let students see the cells biology class talks about</h1>
      <p class="lede">{SITE_NAME} is a student art exhibit of sickle cells, cancer cells, the stages of mitosis and the path from gene to protein. Each painting comes with a short title card that explains what is on the canvas.</p>
      <div class="btn-row center">
        <a href="exhibit.html" class="btn">Walk through the exhibit</a>
      </div>
    </div>
    {hero_img("hero-gallery-bench", "Two young visitors sitting on a white gallery bench, studying a painting on the wall", HOME_SIZES, "hero-photo wide")}
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
        <h3>Fewer students enjoy science at all</h3>
        <p>In 2019, 52% of eighth graders said they enjoyed science activities. By 2024 it was 42%, and interest in what they learn in science class fell from 47% to 39%.</p>
        <p class="of">of eighth graders say they enjoy science activities</p>
      </div>
      <div class="card">
        <div class="icon">{ICON_EYE}</div>
        <p class="num">&minus;5 pts</p>
        <h3>Biology is hard to learn when nobody can picture it</h3>
        <p>Cells, chromosomes and proteins are invisible to the eye, and fewer eighth graders now say they often use experimental evidence to explain why something happens.</p>
        <p class="of">drop since 2019 in students who often use evidence from experiments</p>
      </div>
    </div>
    <p class="punch">No student should give up on biology because nobody ever showed them what a cell looks like.</p>
  </div>
</section>

<section id="about">
  <div class="wrap split">
    <div class="about-text">
      <h2>A painter who has also worked in a cancer research lab</h2>
      <p class="name-line">I'm {AUTHOR}, a senior at Episcopal Collegiate School in Little Rock, and I paint the parts of biology that are hardest to imagine.</p>
      <p>I won Best in Class in Biology as a freshman and in Genetics as a junior, and one of my paintings was shown at the Arkansas Museum of Fine Arts in ninth grade. This project is where those two halves meet: I paint the cells and processes that are hardest to imagine, so more students can see that science is within their reach.</p>
      <p>This past summer I spent six weeks as a Stephens Summer Science Scholar at the University of Arkansas for Medical Sciences, researching metastatic melanoma and ER stress in a working lab, and presented my research at the UAMS undergraduate research symposium.</p>
    </div>
    {photo("microscope", "A researcher in a lab coat and blue gloves looking through a microscope")}
  </div>
  <div class="wrap">
    <ul class="strip">
      <li><span class="n">176 hrs</span><span class="t">of cancer research at UAMS the summer before senior year</span></li>
      <li><span class="n">{N_PIECES}</span><span class="t">paintings across {WORDS[len(SERIES)]} series of cells and cell processes</span></li>
      <li><span class="n">AMFA</span><span class="t">one of my paintings was shown at the Arkansas Museum of Fine Arts</span></li>
    </ul>
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
        <p>Next time your biology teacher brings up mitosis, red blood cells or protein synthesis, you will already have an image to hang the terms on.</p>
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
      <h2>Three series of science paintings</h2>
      <p>The exhibit follows cells from the shapes that signal disease to the moment one cell becomes two.</p>
    </div>
    <div class="cards">
      <a class="card" href="exhibit.html#goggle-series">
        <div class="icon">{ICON_GOGGLES}</div>
        <h3>The Goggle Series</h3>
        <p>Cancer cells, flat cells and sickle cells, three cells whose shape tells a story about health.</p>
      </a>
      <a class="card" href="exhibit.html#mitosis">
        <div class="icon">{ICON_SPLIT}</div>
        <h3>Mitosis</h3>
        <p>Interphase, prophase, metaphase, anaphase and telophase, painted stage by stage.</p>
      </a>
      <a class="card" href="exhibit.html#protein-transcription">
        <div class="icon">{ICON_HELIX}</div>
        <h3>Protein Transcription</h3>
        <p>How a gene's DNA is copied into RNA and built into a protein.</p>
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
""" + cta("See the cells for yourself",
          f"{WORDS.get(N_PIECES, N_PIECES).capitalize()} paintings, each with a title card that explains the science in a minute or less.",
          "exhibit.html", "Walk through the exhibit") + sources(["nagb", "edsource"]) + "\n</main>\n" + foot()


# ---------------------------------------------------------------- exhibit
def exhibit():
    t = f"Cell Paintings: Sickle Cells, Cancer Cells and the Stages of Mitosis | {SITE_NAME}"
    d = ("A science art exhibit by student artist " + AUTHOR + ": paintings of cancer cells, flat cells and sickle cells, "
         "the five stages of mitosis and protein synthesis, each with a plain-language title card.")
    items = [{"@type": "ListItem", "position": i, "name": p["title"], "url": SITE + "exhibit.html#" + p["id"]}
             for i, p in enumerate((p for s in SERIES for p in s["pieces"]), 1)]
    schema = [page_schema("CollectionPage", "exhibit.html", t, d,
                          {"mainEntity": {"@type": "ItemList", "itemListElement": items}}),
              crumbs("The Exhibit", "exhibit.html")]
    walls = []
    for s in SERIES:
        cls = "wall five" if len(s["pieces"]) == 5 else "wall"
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
      <h1>Paintings of cells, mitosis and the path from gene to protein</h1>
      <p class="lede">{N_PIECES} paintings in {WORDS[len(SERIES)]} series. Read each title card beside its painting, the way you would in a museum.</p>
      <div class="btn-row center">
        <a href="#goggle-series" class="btn">Start with the Goggle Series</a>
      </div>
    </div>
    {hero_img("hero-bright-gallery", "A visitor standing in a bright gallery, looking at a wall of colorful paintings", PAGE_SIZES)}
  </div>
</header>
{"".join(walls)}
""" + cta("Why these paintings matter",
          "Student interest in science has dropped since 2019. See the research that shaped this exhibit and what studies say about learning science through art.",
          "research.html", "Read the research") + "\n</main>\n" + foot()


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
    t = f"Why Students Lose Interest in Science, and How Art Can Help | {SITE_NAME}"
    d = ("What the 2024 Nation's Report Card says about eighth grade science scores and enjoyment, why interest drops as "
         "science turns abstract, and what studies show about learning science through art and drawing.")
    schema = [page_schema("Article", "research.html", t, d, {"about": "Student engagement in science education"}),
              crumbs("The Research", "research.html")]
    return head(t, d, "research.html", schema, hero="hero-boy-painting", sizes=PAGE_SIZES) + nav("research.html") + f"""
<main id="main">

<header class="page-hero">
  <div class="wrap split">
    <div>
      <h1>Why students lose interest in science, and how art can help</h1>
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
      <h2>Fewer students enjoy science, and fewer do hands-on science</h2>
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


FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="9" fill="#1F3D63"/>'
           '<circle cx="16" cy="16" r="9.5" fill="none" stroke="#EEF2F6" stroke-width="2"/>'
           '<circle cx="17.5" cy="14.5" r="3.6" fill="#E58AA6"/></svg>\n')

if __name__ == "__main__":
    out = {"index.html": index, "exhibit.html": exhibit, "research.html": research}
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
