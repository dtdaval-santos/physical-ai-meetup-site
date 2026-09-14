# Deploying to GitHub + Cloudflare Pages

This repo is plain static HTML — **no build step**. Cloudflare serves the files exactly as they are.

---

## Part 1 — Push to GitHub

Run these in **Terminal on your Mac** — this needs your own GitHub credentials, which only exist
on your machine:

```bash
cd "/Users/dominiquedavalsantos/Documents/Claude/Projects/PAI Organiser/Website"

# 1. initialise the repo (skip if it's already a repo — `git status` will tell you)
git init
git add -A
git commit -m "Physical AI Meetup website: sponsor landing page and chapter linktree"

# 2. create an empty repo on github.com (no README, no .gitignore, no licence),
#    then point this folder at it — swap in your username and repo name:
git remote add origin https://github.com/YOUR-USERNAME/physical-ai-meetup-site.git

# 3. push
git branch -M main
git push -u origin main
```

If you have the GitHub CLI installed (`gh`), steps 1 and 2 collapse into one command:

```bash
gh repo create physical-ai-meetup-site --public --source=. --remote=origin --push
```

Check `git log --oneline` first if you want to see what's being pushed.

---

## Part 2 — Connect Cloudflare Pages

In the [Cloudflare dashboard](https://dash.cloudflare.com):

1. **Compute (Workers & Pages)** → **Create** → **Pages** tab → **Connect to Git**
2. Authorise GitHub if prompted, then pick the `physical-ai-meetup-site` repo
3. Build settings — this is the part people get wrong on a no-build site:
   - **Framework preset:** `None`
   - **Build command:** *leave empty*
   - **Build output directory:** `/`  (the repo root — `index.html` lives there)
4. **Save and Deploy**

You'll get a live URL like `physical-ai-meetup-site.pages.dev` within a minute or so.

From then on, **every push to `main` redeploys automatically.**

---

## Part 3 — Point your domain at it

Still in the Pages project: **Custom domains** → **Set up a custom domain** → enter your domain.

- **If the domain's nameservers already point at Cloudflare** (i.e. it shows up under Websites in
  your dashboard) — Cloudflare creates the DNS record and issues the SSL certificate itself. One click.
- **If DNS is still at your registrar** — Cloudflare shows you a CNAME record to add there manually.
  The easier path is usually to add the domain as a site in Cloudflare first and switch the
  nameservers, then come back here.

Add both the apex (`yourdomain.com`) and `www.yourdomain.com` if you want both to work.
SSL takes a few minutes to go from "pending" to active — that's normal.

---

## Everyday workflow after setup

```bash
cd "/Users/dominiquedavalsantos/Documents/Claude/Projects/PAI Organiser/Website"
# ...edit files, drop in real photos...
git add -A
git commit -m "Add real event photos"
git push
```

Cloudflare picks it up and redeploys on its own. Rollbacks live under **Deployments** in the
Pages project — every past deploy stays available.

---

## Things worth knowing

- `_headers` sets caching: assets cache for a year, HTML always revalidates. If you replace an
  image but keep the filename, a browser that already cached it may hold the old one for a while —
  hard-refresh (Cmd+Shift+R) to check, or rename the file to bust the cache.
- The free plan covers unlimited bandwidth and requests for static sites, with a limit on builds
  per month (500 at the time of writing — worth confirming on Cloudflare's current pricing page,
  since these limits change).
- `_archive/` is gitignored, so the old bundled HTML files stay on your Mac and never deploy.
