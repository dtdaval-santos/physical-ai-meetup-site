# Image guide

Every file in `assets/images/` is a **placeholder** right now — a dark tile with its own filename and
required dimensions printed on it. To use a real photo, **save your image with exactly the same filename
and drop it in the same folder, overwriting the placeholder.** No HTML changes needed.

## What goes where

| File (in `assets/images/`) | Size (px) | Where it appears | What to use |
|---|---|---|---|
| `hero-community.jpg` | 1600 × 900 | Big image under the hero headline | Wide shot of a full room at a meetup — people visible, venue readable |
| `event-sydney.jpg` | 800 × 600 | Sydney chapter card | Photo from a Sydney event |
| `event-melbourne.jpg` | 800 × 600 | Melbourne chapter card | Photo from a Melbourne event |
| `event-perth.jpg` | 800 × 600 | Perth chapter card | Photo from a Perth event |
| `gallery-1.jpg` | 900 × 600 | "Community in action" — slot 1 | Speaker mid-talk, slide visible behind them |
| `gallery-2.jpg` | 900 × 600 | "Community in action" — slot 2 | Networking / pizza, people talking |
| `gallery-3.jpg` | 900 × 600 | "Community in action" — slot 3 | Open mic demo, someone showing hardware |
| `sponsor-logo-1.png` … `-6.png` | 400 × 160 | Sponsor wall ("Who we've worked with") | Sponsor logos, **transparent PNG**, logo centred with breathing room |
| `og-image.jpg` | 1200 × 630 | Link preview when the site is shared on LinkedIn/Slack | Branded card: logo + "Physical AI Meetup" + one line |

Chapter photos are cropped to 4:3 and gallery photos to 3:2 by CSS, so keep the subject near the centre.
Sponsor logos display greyscale and turn full-colour on hover — that's intentional, it keeps a mixed
logo wall looking tidy.

## Adding or removing sponsor logos

The wall is a 6-column grid. To use fewer, delete the extra `<img>` lines in `index.html`
(search for `sponsor-logos`). To add more, copy an existing line and increment the number,
then add the matching PNG file.

## File size budget

The page's own code (HTML + CSS) is about **35 KB**. To keep a first visit comfortably light, aim for:

- `hero-community.jpg` — under 200 KB
- each chapter / gallery photo — under 120 KB
- each sponsor logo — under 30 KB
- `og-image.jpg` — under 150 KB

Everything below the hero is lazy-loaded, so only the hero image and the logo actually load up front.

Easy ways to compress: [Squoosh](https://squoosh.app) (drag in, export at ~75% quality), or on your Mac:

```bash
# resize + compress a photo to the right width
sips -Z 1600 photo.jpg --out assets/images/hero-community.jpg
```

If you want smaller files still, export as `.webp` instead — but then update the filename in
`index.html` to match (e.g. `hero-community.webp`).

## Favicon

Already done — generated from `assets/source/Logo no words.png` with the black background removed:

- `assets/icons/favicon.ico` (16/32/48 px, what the browser tab uses)
- `assets/icons/favicon-16x16.png`, `favicon-32x32.png`, `favicon-192x192.png`, `favicon-512x512.png`
- `assets/icons/apple-touch-icon.png` (180 px, dark background — iOS ignores transparency)
- `assets/icons/logo-mark.png` (transparent, used in the nav bar and footer)

To regenerate them after a logo change, re-run `tools/make-icons.py`.
