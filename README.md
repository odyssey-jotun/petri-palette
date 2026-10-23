# Petri Palette

Lily Butler's art and science site: an exhibit of her paintings of cells and cell processes (the Goggle Series, Mitosis, Protein Transcription) with plain-language title cards, a digital exhibit of the wider science art genre, and the research on why students lose interest in science. The repo was `science-you-can-see` before 2026-10-23.

Every page is written in the first person ("I"). The name appears only in the "I'm Lily Butler" introductions.

The StoryBrand framework the copy follows is in `BRANDSCRIPT.md`. Change the script first, then the copy.

## Live preview

https://odyssey-jotun.github.io/petri-palette/

The repository is public and GitHub Pages serves `main` at root. Pushing to `main` redeploys. Every page is `noindex,nofollow` and `robots.txt` disallows all until the paintings are in and the site is ready to launch. To open it to search, change the robots meta in `head()` to `index,follow,max-image-preview:large` and the robots.txt text in `build.py` to `Allow: /` plus the sitemap line.

## Pages

| Page | What it is |
| --- | --- |
| `index.html` | StoryBrand home: people-photo hero, the problem (three icon cards with NAEP numbers: external, internal, philosophical), the guide section in first person, a three-step plan, the three series, what is at stake, closing call to action |
| `exhibit.html` | The exhibit: every painting in a frame with a museum-style title card. Frames show a line drawing until the painting is scanned |
| `artists.html` | The genre exhibit: three rooms of openly licensed science art (Hooke, Flemming, Cajal; Goodsell, Harris; Odra Noel, Magrath), agar art, six more artists described in words only, and where Petri Palette fits in. Pieces pair with the matching painting in the exhibit |
| `research.html` | NAEP 2024 science results, the 2019 vs 2024 enjoyment chart, why interest drops as science turns abstract, math and screen-time context, and studies on learning science through art |

## Editing

All pages, `sitemap.xml`, `robots.txt` and `favicon.svg` are generated. Change copy or facts in `build.py`, then run:

    python3 build.py

Styles live in `styles.css` and are minified and inlined by the build.

- Site name: `SITE_NAME` at the top of `build.py`.
- Artists page: rooms in `GENRE`, the petri dish section in `AGAR`, word-only artists in `MORE_ARTISTS`. Artwork originals live in `images/genre/originals/` (gitignored); `python3 tools/genre.py` crops and exports them without any color change.
- Adding a painting: put the scan in `images/art/` (portrait 4:5, about 1200px tall, .webp or .jpg) and set `"art"` on that piece in `SERIES`. Painting titles and dates go in `"title"` and `"meta"`.
- Photos: `python3 tools/photos.py` crops and grades the Unsplash originals in `images/originals/` (gitignored).
- Fonts: Newsreader (headings) and Public Sans (body), self-hosted and subset. After adding new symbols, run `python3 tools/subset_fonts.py` (needs `pip install fonttools brotli`).

## Rules this site follows

- Every figure is checked against its source and cited in plain text. The site has zero external links.
- Left off on purpose: the claim that low-income schools offer fewer advanced STEM courses, because the PubMed Central paper first found for it (PMC6559120) is an unrelated study. The PISA screen-time figures are cited to the OECD rather than an NIH preprint.
- Hero photos show people. Photos have rounded corners and a light color pass.
- No em dashes, no small uppercase labels above headings, no bold phrases inside sentences.


## Photos

Stock photos are from Unsplash under the Unsplash licence. The home hero, the About story photo and `og.jpg` are Lily's own portraits (`lily-column`, `lily-wall`), cropped in `tools/photos.py`.

| File | Used on | Unsplash ID | Photographer |
| --- | --- | --- | --- |
| `hero-bright-gallery` | Exhibit hero | `qxvOmDuQDsg` | Caroline Badran |
| `hero-boy-painting` | Research hero | `hbZOr0FfNNE` | Egor Myznik |
| `microscope` | Not used (the about section shows the DNA painting) | `6q5QG8iIgRo` | Trust Katsande |
| `watercolor` | Research, art section | `YKLkzMuEA8Q` | Madalyn Cox |
| `hero-gallery-visitor` | Artists hero | `AlLKJ292jOQ` | Pauline Loroy |

## Artwork on the Artists page

Only public domain or openly licensed images are shown. Credits are on the page in plain text. Artists whose work is all rights reserved (Klari Reis, Michele Banks, Greg Dunn, Hunter Cole, Luke Jerram, Rogan Brown) are described in words until there is permission to show an image.

| File | Work | License | Source page (not linked from the site) |
| --- | --- | --- | --- |
| `hooke-cork` | Robert Hooke, Micrographia, Schem. XI, 1665 | Public domain | commons.wikimedia.org/wiki/File:Micrographia_Schem_11.jpg |
| `flemming-mitosis` | Walther Flemming, Zellsubstanz, Kern und Zelltheilung, Tafel IIIb, 1882 (cropped) | CC BY 4.0 | commons.wikimedia.org/wiki/File:Zellsubstanz,_Kern_und_Zelltheilung_Wellcome_L0060921.jpg |
| `cajal-purkinje` | Santiago Ramón y Cajal, Purkinje neurons, about 1900 | Public domain | commons.wikimedia.org/wiki/File:Santiago_Ramon_y_Cajal_nerve_cells_in_the_brain.jpg |
| `goodsell-ecoli` | David S. Goodsell, Escherichia coli Bacterium, 2021 | CC BY 4.0 | pdb101.rcsb.org/sci-art/goodsell-gallery/escherichia-coli-bacterium |
| `goodsell-mycoplasma` | David S. Goodsell, Mycoplasma mycoides, 2011 | CC BY 4.0 | pdb101.rcsb.org/sci-art/goodsell-gallery/mycoplasma-mycoides |
| `harris-retina` | Prof. Bill Harris, Cell fates in zebrafish retina | CC BY 4.0 | wellcomecollection.org/works/uj3g2dhy |
| `noel-t-cell` | Odra Noel, St George and the dragon | CC BY-NC 4.0 | wellcomecollection.org/works/pvnkqcuu |
| `noel-blood` | Odra Noel, Blood cells through the microscope | CC BY-NC 4.0 | wellcomecollection.org/works/fyx7mvcz |
| `magrath-neurones` | Stephen Magrath, Neurones connecting | CC0 | wellcomecollection.org/works/af25gh35 |
| `agar-butterfly` | Ajay Kumar Chaurasiya, Microbial Art, 2021 (cropped) | CC BY-SA 4.0 | commons.wikimedia.org/wiki/File:Microbial_Art.jpg |

The two Odra Noel paintings are non-commercial only. If the site ever sells anything, replace them or ask her.
