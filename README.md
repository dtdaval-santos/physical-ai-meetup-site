# Physical AI Meetup — website

Sponsor-facing landing page and chapter linktree for the Physical AI Meetup community
(Sydney · Melbourne · Perth, with New Zealand planned).

Plain static HTML and CSS. No build step, no framework, no dependencies — what's in this repo is
exactly what gets served.

## Structure

```
index.html                  the whole page
assets/css/style.css        all styling (brand colours defined at the top)
assets/icons/               favicons + nav logo, generated from the source logo
assets/images/              photo + sponsor-logo placeholders — see IMAGES.md
assets/source/              original logo artwork (not used directly by the page)
tools/make-icons.py         regenerates the favicon set if the logo changes
site.webmanifest            icons + theme colour for mobile home-screen installs
_headers                    Cloudflare Pages caching and security headers
robots.txt                  allows all crawlers
```

## Editing

**Replacing photos** — see [IMAGES.md](IMAGES.md). Keep the filename, drop the file in, done.

**Brand colours** — the top of `assets/css/style.css`:

```css
--accent:   #4FC8EC;   /* logo cyan   */
--accent-2: #7A2BD6;   /* logo purple */
```

Both are sampled from the official logo, so the site matches the mark.

**Links that still need filling in** — search `index.html` for `TODO`:

- Meetup group URL and Eventbrite link for each of Sydney, Melbourne, Perth
- the contact address in the "Email Us" button (currently `hello@example.com`)

## Previewing locally

```bash
cd "path/to/this/folder"
python3 -m http.server 8000
# then open http://localhost:8000
```

Opening `index.html` by double-clicking mostly works too, but a local server matches how
Cloudflare will actually serve it.

## Deployment

Hosted on Cloudflare Pages, connected to this GitHub repo. Every push to `main` triggers a
redeploy — there's no build command and the output directory is the repo root.

See [DEPLOY.md](DEPLOY.md) for the full setup and custom-domain steps.
