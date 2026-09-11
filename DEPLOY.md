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

---

## Activating testimonials

`docs/index.html` ships a **"Why people use Paypr"** section (id `#why`) sitting just above
pricing. It is deliberately **not** testimonials: three scenario cards in the reader's own voice,
with no names, faces, star ratings or user counts. Nothing in it is attributed to a customer, so
it is safe to run with zero reviews on the storefront.

Directly beneath it, inside one HTML comment, is the **real** testimonial block — markup, styling
hooks and `Review` JSON-LD, every quote a `[BRACKETED]` placeholder. It renders nothing until you
delete the comment wrapper.

**Do not fill it with invented quotes.** Fabricated consumer testimonials are actionable under the
FTC's rule on fake reviews (16 CFR Part 465), and it contradicts the standing guardrail in
`paypr/SEO_PLAN.md:172` — *"only with real, permissioned quotes — never fabricated."*

To activate, in order:

1. **Accumulate real App Store reviews.** As of 2026-07-14 the US storefront showed **0 public
   ratings** (`paypr/ACQUISITION.md:82`). The in-app prompt already works (`ReviewManager`); the
   bottleneck is installs. Optional squeeze: point the Settings "Rate" button at the write-review
   deep link — `https://apps.apple.com/app/paypr/id6778970494?action=write-review` — which opens
   the composer directly and yields *written* reviews rather than a bare star tap.
2. **Get permission** before quoting anyone by name, even publicly. A reply to their review asking
   to feature it is enough; keep the reply as your record.
3. **Quote verbatim.** Trimming with an ellipsis is fine. Rewording, fixing their grammar,
   compositing two reviewers into one, or upgrading a 4-star to 5 is not.
4. **Fill every placeholder** — quote, real first name, real city, and a star count matching what
   they actually left. Set `datePublished` in the JSON-LD to the real review date.
5. **Delete the comment wrapper** (the opening marker and the `END INERT TESTIMONIAL BLOCK` line).
   Keep or delete `#why` — the two sections are independent and read fine together.
6. **`aggregateRating` stays locked** until the App Store shows real public ratings, and must then
   mirror the store's real count and average. It lives on the `SoftwareApplication` block in the
   `<head>`, not in the testimonial block. This is the one rating Google *will* treat as
   third-party and eligible for a star rich result — self-hosted `Review` markup is ignored for
   that purpose (`paypr/SEO_PLAN.md:174`), so the JSON-LD in the block is provenance, not ranking.

---

## Bot traffic tracking (DataFast AI crawl)

Two separate DataFast integrations run on this site. They do not overlap:

| | What it sees | Where it lives |
|---|---|---|
| Browser script | Humans. Pageviews, referrers, conversions. | `<head>` of every page in `docs/` |
| `@datafast/ai-crawl` | Bots. ClaudeBot, GPTBot, ChatGPT-User, PerplexityBot, Googlebot… | `functions/_middleware.ts` |

AI crawlers request raw HTML and never execute JavaScript, so the browser script cannot see them —
that is the whole reason the second integration exists. It is **server-side**, which is why this
site moved off GitHub Pages: Pages serves static files and runs no code, so `@datafast/ai-crawl`
could not run there at all.

### Hosting: Cloudflare Pages

Build settings for the Pages project (nothing to build — the site is static HTML):

| Setting | Value |
|---|---|
| Production branch | `master` |
| Build command | *(empty)* |
| Build output directory | `docs` |
| Root directory | *(repo root)* |

Cloudflare installs `package.json` dependencies automatically and compiles `functions/_middleware.ts`,
so `git push origin master` still deploys, exactly like before.

`docs/_routes.json` controls which requests invoke the Function. Images are excluded so Cloudflare
does not bill a Function invocation for every PNG. **Do not exclude `/robots.txt`, `/llms.txt` or
`/sitemap.xml`** — crawlers usually fetch those first, and seeing those hits is how you know bots are
finding the site's AI/SEO instructions at all.

### One-time setup (manual, in the Cloudflare dashboard)

1. **Pages → Create → Connect to Git** → pick `JeyFk/paypr-legal`, apply the build settings above.
2. Let the first deploy finish, then check the `*.pages.dev` URL it hands you.
3. **Move DNS to Cloudflare**: add `usepaypr.com` as a zone, then change the nameservers at the
   registrar. This is the cutover — until it happens, the live site is still GitHub Pages.
4. **Pages → Custom domains** → add `usepaypr.com` and `www.usepaypr.com`.
5. Confirm the switch: `curl -sI https://usepaypr.com/ | grep -i server` should stop saying
   `GitHub.com`.

The old GitHub Pages deployment can stay enabled as a fallback during the move; `docs/CNAME` is
kept for that reason and is harmless on Cloudflare.

### Verifying it works

Bot traffic only appears when a **real** crawler hits the site, so an empty card right after
deploying is normal, not a failure. To force a check without waiting:

```bash
curl -sI https://usepaypr.com/nanny-tax-calculator.html \
  -A "Mozilla/5.0 (compatible; ClaudeBot/1.0; +claudebot@anthropic.com)"
```

Then open the **Bot traffic** card in the DataFast dashboard. Note it defaults to showing
IP-verified crawlers only — a spoofed user agent from your laptop will fail IP verification, so
turn that filter off to see the test hit.

Watch for crawlers repeatedly requesting paths that **404**. That is a content signal: bots expect a
page there. Those show up in the same card.

### Optional: request authentication

Off by default, and fine to leave off. To enable: create a `dfbot_…` token in the Bot traffic card
settings, add it as an **encrypted** environment variable named `DATAFAST_BOT_TOKEN` on the Pages
project, deploy, *then* turn on "Reject unauthenticated requests" in that order. The middleware
already reads the variable. Never commit the token — it does not belong in this repo.

### Cost

100,000 accepted bot requests per account per billing cycle, then $9/month per extra 1M. Allowance
counting starts **15 September 2026**. Hitting the cap pauses bot ingestion only; normal web
analytics keeps working. To cut usage, disable whole companies or individual agents under Crawler
ingestion in the Bot traffic card — requests from disabled agents are dropped before storage and do
not count.
