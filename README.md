# Physical AI Meetup — website

Sponsor-facing landing page and chapter directory for the Physical AI Meetup community
(Sydney · Melbourne · Perth · Canberra · Auckland, with Brisbane, Adelaide and Christchurch flagged
as coming soon).

Plain static HTML and CSS. No build step, no framework, no dependencies, no third-party requests —
what's in this repo is exactly what gets served.

## Structure

```
index.html                  the whole page
assets/css/style.css        all styling; design tokens at the top
assets/css/fonts.css        @font-face rules for the self-hosted fonts
assets/fonts/               Syne, Inter, JetBrains Mono (Latin subsets, woff2)
assets/icons/               favicons + nav logo, generated from the source logo
assets/images/              photos and sponsor logos — see IMAGES.md
assets/source/              original logo artwork (not used directly by the page)
tools/make-icons.py         regenerates the favicon set if the logo changes
site.webmanifest            icons + theme colour for mobile home-screen installs
_headers                    Cloudflare Pages caching and security headers
robots.txt                  allows all crawlers
_archive/                   old builds and original full-size photos (gitignored)
```

## Design system

Tokens are declared at the top of `assets/css/style.css` and match the design language of the
existing physicalaimeetup.com build, so anything added later stays consistent:

```css
--pai-accent:            #00C8D7;   /* cyan   */
--pai-accent-secondary:  #7040C8;   /* purple */
--pai-bg:                #080E1A;   /* navy   */
--pai-surface-card:      #111E2D;
--pai-font-display:      'Syne';        /* headings, city names, stat numbers */
--pai-font-body:         'Inter';       /* body copy, buttons, nav */
--pai-font-mono:         'JetBrains Mono'; /* eyebrows, labels, captions */
```

Fonts are self-hosted in `assets/fonts/` rather than pulled from Google — same files, but no
third-party request and nothing to break if that CDN is blocked. Only the Latin subset downloads
for normal English copy; the `-ext` files load only if an extended-Latin character appears.

## Editing

**Photos** — see [IMAGES.md](IMAGES.md). Keep the filename, drop the file in, done.

**Content that still needs your input** — search `index.html` for `TODO`:

- the contact address behind "Request an information packet" and "Let's collaborate"
  (currently `hello@physicalaimeetup.com`, which may not be a real inbox)

## Previewing locally

```bash
cd "path/to/this/folder"
python3 -m http.server 8000
# then open http://localhost:8000
```

## Deployment

Static hosting on Cloudflare Pages, connected to this GitHub repo. Every push to `main` redeploys —
no build command, output directory is the repo root. See [DEPLOY.md](DEPLOY.md).
