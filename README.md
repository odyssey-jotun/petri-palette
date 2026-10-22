# Science You Can See

Passion-project site for Lily Butler: an art exhibit of cells and cell processes (the Goggle Series, Mitosis, Protein Transcription) with plain-language title cards, plus the research on why students lose interest in science. Built from Lily's doc "Research Questions to Answer" (research notes and exhibit plan) and her activities list.

## Live preview

https://odyssey-jotun.github.io/science-you-can-see/

The repository is public and GitHub Pages serves `main` at root. Pushing to `main` redeploys. Every page is `noindex,nofollow` and `robots.txt` disallows all until Lily approves the copy and her paintings are in. To open it to search, change the robots meta in `head()` to `index,follow,max-image-preview:large` and the robots.txt text in `build.py` to `Allow: /` plus the sitemap line.

## Pages

| Page | What it is |
| --- | --- |
| `index.html` | StoryBrand home: people-photo hero, the problem (three icon cards with NAEP numbers: external, internal, philosophical), Lily as guide in her first person, a three-step plan, the three series, what is at stake, closing call to action |
| `exhibit.html` | The exhibit: every painting in a frame with a museum-style title card. Frames show a line drawing until the painting is scanned |
| `research.html` | NAEP 2024 science results, the 2019 vs 2024 enjoyment chart, why interest drops as science turns abstract, math and screen-time context, and studies on learning science through art |

## Editing

All pages, `sitemap.xml`, `robots.txt` and `favicon.svg` are generated. Change copy or facts in `build.py`, then run:

    python3 build.py

Styles live in `styles.css` and are minified and inlined by the build.

- Site name: `SITE_NAME` at the top of `build.py`. "Science You Can See" is a working name; Lily's activities list still has "?Title of Website".
- Adding a painting: put the scan in `images/art/` (portrait 4:5, about 1200px tall, .webp or .jpg) and set `"art"` on that piece in `SERIES`. Painting titles and dates go in `"title"` and `"meta"`.
- Photos: `python3 tools/photos.py` crops and grades the Unsplash originals in `images/originals/` (gitignored).
- Fonts: Newsreader (headings) and Public Sans (body), self-hosted and subset. After adding new symbols, run `python3 tools/subset_fonts.py` (needs `pip install fonttools brotli`).

## Rules this site follows

- Every figure is checked against its source and cited in plain text. The site has zero external links.
- Left off on purpose: Lily's doc cites a PubMed Central link (PMC6559120) for "low-income schools offer fewer advanced STEM courses". That link is an unrelated paper about postdoctoral women, so the claim is not on the site. Her screen-time link pointed to an NIH preprint; the PISA figures are cited to the OECD instead.
- Hero photos show people. Photos have rounded corners and a light color pass.
- No em dashes, no small uppercase labels above headings, no bold phrases inside sentences.

## Open questions for Lily

- The site name, and the gallery where the paintings will hang ("Organized gallery showing at ___").
- What "Goggle Series" means visually. The copy does not guess.
- Titles for the three Protein Transcription paintings. The current titles (DNA to RNA, Leaving the Nucleus, The Ribosome) are placeholders. Strictly, transcription only makes the RNA; translation builds the protein, so the series intro explains both.
- "Flat cells" is written up as squamous cells. Confirm that is what she means.
- Her first-person section was drafted from her activities list and needs her approval, plus a real photo of her (the current microscope photo is stock).

## Photos

All from Unsplash under the Unsplash licence, cropped and color-graded.

| File | Used on | Unsplash ID | Photographer |
| --- | --- | --- | --- |
| `hero-gallery-bench`, `og.jpg` | Home hero | `ABdRtZKWJfE` | Eri Pançi |
| `hero-bright-gallery` | Exhibit hero | `qxvOmDuQDsg` | Caroline Badran |
| `hero-boy-painting` | Research hero | `hbZOr0FfNNE` | Egor Myznik |
| `microscope` | Home, Lily's section | `6q5QG8iIgRo` | Trust Katsande |
| `watercolor` | Research, art section | `YKLkzMuEA8Q` | Madalyn Cox |
