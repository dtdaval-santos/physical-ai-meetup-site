# Physical AI Meetup website — guide & deployment

Sponsor-facing landing page and chapter directory for the Physical AI Meetup community
(Sydney · Melbourne · Perth · Canberra · Auckland, with Brisbane, Adelaide and Christchurch flagged
as coming soon).

Plain static HTML and CSS. No build step, no framework, no dependencies, no third-party requests —
what's in this repo is exactly what gets served.

> Last checked against the Cloudflare dashboard: 13 Oct 2026. Cloudflare changes its dashboard and
> defaults fairly often, so if something below no longer matches what you see, trust the dashboard
> and update this file.

---

## 1. How it's connected

```
Local folder ──git push──▶ GitHub (main) ──auto build──▶ Cloudflare Worker ──▶ physicalaimeetup.com
 …/PAI Organiser/Website    dtdaval-santos/              physical-ai-meetup-site
                            physical-ai-meetup-site
```

- **Cloudflare project:** a **Worker with static assets** named `physical-ai-meetup-site` — *not* a
  Pages project. (Earlier versions of this file described Pages; that was wrong for this setup.)
- **Git connection:** the Worker's Builds settings are linked to the GitHub repo above.
  **Production branch: `main`.** Builds are enabled.
- **Build settings** (Worker → Settings → Builds):

  | Setting | Value |
  |---|---|
  | Build command | *(none)* |
  | Deploy command | `npx wrangler deploy` |
  | Version command | `npx wrangler versions upload` |
  | Root directory | `/` |
  | Build watch paths | include `*` |

- **Pushes to other branches** are built as non-production versions ("Builds for non-production
  branches" is ticked). They do not go live.
- **Deploy history** (Worker → Deployments): the first two deploys (Sept 2026) were manual uploads
  from the dashboard; the third was the first automatic Git build from `main`.

> **Don't use "New deployment" / manual upload for routine changes.** A later push to `main` will
> overwrite it, and the dashboard and GitHub will disagree about what's live.

## 2. Everyday workflow

```bash
cd "/Users/dominiquedavalsantos/Documents/Claude/Projects/PAI Organiser/Website"
git status                      # see what changed
# ...edit files...
git add -A
git commit -m "Describe the change"
git push
```

Then, in Cloudflare: **Workers & Pages → physical-ai-meetup-site → Deployments**. A new row from
branch `main` should appear and turn **Ready** within a minute or two. Check the live site —
hard-refresh (Cmd+Shift+R) if you changed an image or CSS, because those are cached for a long time.

**Rollback:** Deployments tab → pick an earlier version → roll back / redeploy. (Exact button labels
differ between dashboard versions.) Also remember that `git revert` + push is a clean way to undo.

**Which copy is the latest?** They should always match. To check quickly:

```bash
git fetch && git status -sb     # "## main...origin/main" with no [ahead/behind] = in sync with GitHub
```

and compare the newest row in Deployments against `git log -1`.

## 3. If something goes wrong

| Symptom | Things to check |
|---|---|
| Pushed but the site didn't change | Did the push succeed (`git status -sb`)? Is there a new row in Deployments? Is it branch `main`? Hard-refresh. |
| Deployment shows **Failed** | Open the build log from the Deployments row. Check *Settings → Builds* still matches the table in §1. |
| Old image still showing | Assets are cached for a year as `immutable` (see `_headers`), so a browser that has seen the old file keeps it even after a deploy — and so do your visitors. **When you replace an image but keep its filename, change its `src` in `index.html` to add or bump a version suffix, e.g. `sponsor-logo-1.png?v=3`** (or give the file a new name). A hard-refresh only fixes your own browser. |
| Page looks unstyled / broken images | A filename or path changed. Paths are case-sensitive on the server (`Logo.png` ≠ `logo.png`). |
| A file you expected isn't live | Check `.gitignore` — `_archive/`, `Claude outputs/` and `node_modules/` never deploy. |

## 4. Optional hardening: add a `wrangler.jsonc` (not done yet)

The deploy command is `npx wrangler deploy`, but the repo has **no wrangler config file**. The
deploys have worked, which suggests Cloudflare detects a static-assets site on its own. The risk is
that this implicit behaviour is Cloudflare's to change.

A small explicit config would remove the guesswork. It would look roughly like this — **this is an
untested sketch; check Cloudflare's current "Workers static assets" docs before using it**:

```jsonc
{
  "name": "physical-ai-meetup-site",
  "compatibility_date": "2026-09-11",
  "assets": { "directory": "./" }
}
```

Things to settle before adding it: `directory: "./"` would publish *everything* in the repo root
(including `DEPLOY.md`, `README.md`, `tools/`), so a tidier fix is moving the site into a `public/`
folder and pointing `directory` there. Because that's a structural change, do it as its own commit,
watch the resulting deployment, and be ready to roll back. The `name` must match the existing Worker
or Cloudflare will create a different one.

---

## 5. Project structure

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
_headers                    caching and security headers (see note below)
robots.txt                  allows all crawlers
_archive/                   old builds and original full-size photos (gitignored)
```

`_headers` sets assets to cache for a year and HTML to always revalidate, plus `nosniff` and a
referrer policy. Its first comment line still says "Cloudflare Pages". As far as I know, Workers
static assets also read a `_headers` file in the same format, and the live HTML does return
`max-age=0, must-revalidate`, but I haven't confirmed the asset caching rule is applied — check a
response header on an image if it matters.

## 6. Design system

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

## 7. Editing content

**Photos and sponsor logos** — see [IMAGES.md](IMAGES.md). Keep the filename, drop the file in, done.
Sponsor logos sit on a dark background, so they must be **white / light on transparent**.

**Contact** — both sponsorship buttons open the visitor's mail client addressed to
`aiedc.group@outlook.com` with `nikki.davalsantos@avnet.com` on cc, and a subject line naming which
button they pressed ("sponsorship information packet" vs "organising & city coordination") so the
two enquiry types are easy to tell apart in the inbox. To change either address, edit the two
`mailto:` links in `index.html` — the cc address is url-encoded (`%40` for `@`) and the two
parameters are joined with `&amp;`, which is how an `&` is written inside an HTML attribute.

**Chapters, stats, links** — all in `index.html`. Search for the city name or the number.

## 8. Previewing locally

```bash
cd "path/to/this/folder"
python3 -m http.server 8000
# then open http://localhost:8000
```

---

## Appendix: original one-time setup (already done)

Kept for reference if the project ever has to be rebuilt.

1. Create an empty GitHub repo (`physical-ai-meetup-site`), then from this folder:
   `git init && git add -A && git commit -m "Initial commit" && git remote add origin <repo URL> && git branch -M main && git push -u origin main`
2. In Cloudflare: **Workers & Pages → Create → Import a repository** (Git), choose the repo,
   production branch `main`, leave the build command empty. Cloudflare filled in
   `npx wrangler deploy` as the deploy command.
3. **Domains** tab on the Worker → add `physicalaimeetup.com` (and `www.` if wanted). If the domain's
   nameservers are already on Cloudflare, DNS and SSL are set up automatically.
