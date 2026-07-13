# Paypr SEO Foundation — Deploy Guide

The `site/` folder now contains the full SEO foundation **plus** the content layer:

- `index.html` — SEO-optimized homepage (replaces the current bare landing page); links out to all guides
- `nanny-pay-calculator.html` — free interactive calculator tool (link magnet + ranks for "nanny pay calculator")
- `how-much-to-pay-a-nanny.html` — cornerstone article
- `how-to-track-what-you-owe-your-nanny.html` — cornerstone article (maps directly to what the app does)
- `babysitter-hourly-rates.html` — cornerstone article with city-by-city rate table
- `sitemap.xml` — lists every page for Google (already updated with the new pages)
- `robots.txt` — points crawlers to the sitemap

All pages share the app's dark-glass look, carry their own title/meta/OG tags and JSON-LD schema
(`SoftwareApplication`, `WebApplication`, `BlogPosting`, `FAQPage`), and cross-link to each other.

They're built to drop straight into the **`paypr-legal`** repo (the one served at
`jeyfk.github.io/paypr-legal`). They reuse the images already on that site
(`icon.png`, `shots/1-home.png` … `shots/5-history.png`) — no new assets needed.

---

## Before you publish — 2 required edits

1. **App Store link.** Find-and-replace `REPLACE_WITH_APPSTORE_ID` across **all files in this
   folder** (14 spots total) with your real App Store numeric ID. Your link looks like
   `https://apps.apple.com/app/paypr/id6xxxxxxxxx` — the ID is the `id…` part, found in
   App Store Connect or your app's App Store URL. The `apple-itunes-app` meta also uses it
   (shows a native "Open in App Store" banner on iPhone Safari).

2. **Nothing else is required.** The copy, schema, and links are production-ready.

---

## Step 1 — Publish the files

In the `paypr-legal` repo, at the **root** (same folder as the current `index.html`):

1. Replace the old `index.html` with this one.
2. Add `sitemap.xml` and `robots.txt`.
3. Commit and push. GitHub Pages redeploys in ~1 minute.
4. Check it's live: open `https://jeyfk.github.io/paypr-legal/` and
   `https://jeyfk.github.io/paypr-legal/sitemap.xml`.

---

## Step 2 — Google Search Console (the step that makes it findable)

This is what actually gets you into Google. Free.

1. Go to **search.google.com/search-console** → **Add property** → **URL prefix** →
   enter `https://jeyfk.github.io/paypr-legal/`.
2. Verify ownership. Easiest method for GitHub Pages: **HTML file upload** — Google gives
   you a file like `google1a2b3c.html`; drop it in the repo root, push, then click Verify.
   (If you move to a custom domain later, re-verify the domain with the DNS TXT method.)
3. Once verified: **Sitemaps** (left menu) → enter `sitemap.xml` → **Submit**.
4. **URL Inspection** (top bar) → paste the homepage URL → **Request indexing**. This nudges
   Google to crawl now instead of waiting.

You'll start seeing impressions/clicks/queries in a few days to ~2 weeks. That data tells us
which articles to write next.

**Also do:** submit the same sitemap to **Bing Webmaster Tools** (bing.com/webmasters) — 2
minutes, and it feeds ChatGPT/Copilot search too.

---

## Step 3 (recommended) — Custom domain via Google Cloud

`jeyfk.github.io/paypr-legal` ranks and converts worse than a real domain. Since you have a
Google Cloud account:

1. **Cloud Domains** (console.cloud.google.com → Network Services → Cloud Domains) →
   **Register domain**. Search e.g. `paypr.app`, `getpaypr.com`, `paypr.co` (~$12–15/yr).
   `.app` is Google-owned and forces HTTPS — a clean fit.
2. In the `paypr-legal` repo → **Settings → Pages → Custom domain** → enter your domain →
   Save. Add a `CNAME` file (GitHub does this for you) and tick **Enforce HTTPS**.
3. In Cloud Domains DNS, add the records GitHub shows you (four `A` records for the apex, or
   a `CNAME` to `jeyfk.github.io` for a `www` subdomain).
4. **After the domain is live**, find-and-replace `https://jeyfk.github.io/paypr-legal/`
   with your new domain across `index.html`, `sitemap.xml`, and `robots.txt`, then push.
5. Add the new domain as a fresh property in Search Console and re-submit the sitemap.

Do this early — the sooner the SEO equity accrues to a domain you own, the better.

---

## What this gets you

- **Indexable, keyword-targeted homepage** aimed at "nanny pay tracker," "track what you owe
  your nanny," "babysitter/cleaner pay," etc.
- **Rich results eligibility** — the `SoftwareApplication` and `FAQPage` schema can earn you
  an app snippet (price, category) and expandable FAQ in Google.
- **Full crawlability** — sitemap + robots so Google finds every page.
- **A measurement loop** — Search Console shows real queries to build content around.

## Next after this

Content is built. Once it's live and indexed, the growth work is **off-page**: submit the
calculator to tool/directory roundups, answer real questions on Reddit (r/Nanny, r/Parenting)
and Facebook nanny-employer groups linking the relevant guide, and launch on Product Hunt.
Each earns backlinks that push the whole site up. Ask me to draft those when you're ready.
