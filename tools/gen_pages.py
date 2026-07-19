#!/usr/bin/env python3
"""
gen_pages.py — Generate Paypr's Phase-3 location rate pages from BLS data.

Reads docs/data/babysitter-rates.json (produced by bls_rates.py) and emits:
  * 15 featured static metro pages  ->  docs/babysitter-rates-<city>.html
  * one searchable lookup page       ->  docs/babysitter-rates-by-city.html
    (client-side search over ALL 384 metros, by city / state / area code)
Then patches docs/sitemap.xml with the new URLs (idempotent).

Every page matches the existing BlogPosting layout (babysitter-hourly-rates.html),
cites BLS, and labels the figure as childcare-worker *wage* data — not the higher
informal date-night sitter rate (SEO_PLAN.md guardrail: cite, never conflate).

Usage:  python3 gen_pages.py
"""
from __future__ import annotations

import datetime as _dt
import json
import re
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
DATA = DOCS / "data" / "babysitter-rates.json"
BASE = "https://usepaypr.com"
APP = "https://apps.apple.com/app/paypr/id6778970494"
TODAY = _dt.date.today().isoformat()

# BLS gives one figure (childcare wage). We show two columns:
#   Nanny (regular)      = the BLS local childcare median as-is.
#   Babysitter (occasional) = that wage x an on-demand premium, disclosed below.
# ~1.6x reflects national UrbanSitter/Sittercity sitter rates (~$26) vs the BLS
# childcare wage (~$15). Tune here; it is labelled as an estimate on-page.
SITTER_PREMIUM = 1.6

# Curated top metros by search demand (full slugs as they appear in the JSON).
FEATURED = [
    "new-york-newark-jersey-city-ny-nj",
    "los-angeles-long-beach-anaheim-ca",
    "chicago-naperville-elgin-il-in",
    "houston-pasadena-the-woodlands-tx",
    "dallas-fort-worth-arlington-tx",
    "phoenix-mesa-chandler-az",
    "atlanta-sandy-springs-roswell-ga",
    "boston-cambridge-newton-ma-nh",
    "san-francisco-oakland-fremont-ca",
    "seattle-tacoma-bellevue-wa",
    "washington-arlington-alexandria-dc-va-md-wv",
    "miami-fort-lauderdale-west-palm-beach-fl",
    "denver-aurora-centennial-co",
    "austin-round-rock-san-marcos-tx",
    "columbus-oh",
]

# Shared CSS, lifted verbatim from babysitter-hourly-rates.html so every page
# is visually identical to the rest of the site.
CSS = """<style>
  :root{--bg:#0B0D12;--card:rgba(255,255,255,.05);--stroke:rgba(255,255,255,.10);--ink:#F5F7FA;--muted:#9AA3B2;--accent:#4A90E2;--accent-2:#5FA8FF}
  *{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:#c9d1dc;line-height:1.7;-webkit-font-smoothing:antialiased}
  a{color:var(--accent-2);text-decoration:none}a:hover{text-decoration:underline}
  .bg-glow{position:fixed;inset:0;z-index:-1;background:radial-gradient(55% 40% at 50% -10%,rgba(74,144,226,.22),transparent 70%),var(--bg)}
  .wrap{max-width:1080px;margin:0 auto;padding:0 24px}
  .article{max-width:720px;margin:0 auto;padding:0 24px}
  nav{display:flex;align-items:center;justify-content:space-between;padding:20px 0}
  .brand{display:flex;align-items:center;gap:12px;font-weight:700;font-size:20px;color:var(--ink)}
  .brand img{width:34px;height:34px;border-radius:9px}
  .btn{display:inline-block;background:var(--accent);color:#fff;font-weight:600;padding:12px 22px;border-radius:12px}
  .btn:hover{background:var(--accent-2);text-decoration:none}
  .crumb{color:var(--muted);font-size:14px;margin:26px 0 10px}
  h1{color:var(--ink);font-size:clamp(30px,5vw,44px);font-weight:800;letter-spacing:-.02em;line-height:1.12;margin-bottom:14px}
  .meta{color:var(--muted);font-size:14px;margin-bottom:8px}
  h2{color:var(--ink);font-size:24px;font-weight:800;margin:36px 0 12px;letter-spacing:-.01em}
  p{margin-bottom:16px}
  ul,ol{margin:0 0 16px 22px}li{margin-bottom:8px}
  table{width:100%;border-collapse:collapse;margin:18px 0;font-size:15px}
  th,td{text-align:left;padding:11px 12px;border-bottom:1px solid var(--stroke)}
  th{color:var(--muted);font-weight:600}
  .tip{background:var(--card);border:1px solid var(--stroke);border-left:3px solid var(--accent);border-radius:12px;padding:16px 20px;margin:20px 0}
  .cta{background:linear-gradient(180deg,rgba(74,144,226,.16),transparent);border:1px solid var(--stroke);border-radius:20px;padding:32px 24px;text-align:center;margin:36px 0}
  .cta h2{margin-top:0}
  footer{border-top:1px solid var(--stroke);padding:28px 0;color:var(--muted);font-size:14px;display:flex;gap:16px;flex-wrap:wrap;justify-content:space-between;margin-top:20px}
  footer a{color:var(--muted)}
  .note{color:var(--muted);font-size:13px}
  .big{font-size:34px;font-weight:800;color:var(--ink);letter-spacing:-.02em}
  input[type=search]{width:100%;padding:14px 16px;font-size:16px;border-radius:12px;border:1px solid var(--stroke);background:var(--card);color:var(--ink)}
  input[type=search]::placeholder{color:var(--muted)}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;margin:18px 0}
  .grid a{display:block;padding:12px 14px;border:1px solid var(--stroke);border-radius:12px;background:var(--card)}
  .res td:first-child{color:var(--ink)}
  .res th{background:rgba(255,255,255,.07)}
  .res td{background:rgba(255,255,255,.035);border-bottom:1px solid var(--stroke)}
  .res tr:nth-child(even) td{background:rgba(255,255,255,.075)}
</style>"""

NAV = f"""<nav class="wrap">
  <a class="brand" href="index.html"><img src="icon.png" alt="Paypr icon"> Paypr</a>
  <a class="btn" href="{APP}">Get the app</a>
</nav>"""

FOOTER = """<footer class="wrap">
  <div>© 2026 QAtion · Paypr</div>
  <div><a href="index.html">Home</a> · <a href="privacy.html">Privacy</a> · <a href="terms.html">Terms</a></div>
</footer>
  <!-- Cloudflare Web Analytics --><script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token": "0a79256628664b25bdf9093c0c977cf2"}'></script><!-- End Cloudflare Web Analytics -->"""


def short_name(v: dict) -> str:
    city = v["area_title"].split(",")[0].split("-")[0].strip()
    st = v.get("state") or v["area_title"].split(",")[-1].strip().split("-")[0]
    return f"{city}, {st}"


def short_slug(v: dict) -> str:
    return re.sub(r"[^a-z0-9]+", "-", short_name(v).lower()).strip("-")


def usd(x) -> str:
    return f"${x:,.2f}" if isinstance(x, (int, float)) else "—"


def sitter(med) -> float | None:
    # On-demand estimate: apply the premium, round to the nearest $0.50 so it
    # reads as an estimate, not spurious precision.
    if not isinstance(med, (int, float)):
        return None
    return round(med * SITTER_PREMIUM * 2) / 2


def head(title: str, desc: str, canon: str, jsonld: dict) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<link rel="icon" type="image/png" href="icon.png">
<link rel="apple-touch-icon" href="icon.png">
<meta name="theme-color" content="#0B0D12">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{BASE}/icon.png">
<meta name="twitter:card" content="summary_large_image">

<script type="application/ld+json">
{json.dumps(jsonld, indent=2)}
</script>

{CSS}
</head>
<body>
<div class="bg-glow"></div>
{NAV}
"""


def metro_page(slug: str, v: dict, meta: dict) -> tuple[str, str]:
    name = short_name(v)
    fname = f"babysitter-rates-{short_slug(v)}.html"
    canon = f"{BASE}/{fname}"
    year = meta["reference_year"]
    h = v["hourly"]
    title = f"Babysitter & Childcare Rates in {name} ({year}) | Paypr"
    desc = (
        f"What childcare workers earn per hour in {name}: BLS {year} median {usd(h['median'])}, "
        f"typical range {usd(h['p25'])}–{usd(h['p75'])}. How to set a fair local sitter rate."
    )
    jsonld = {
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": f"Babysitter & childcare rates in {name} ({year})",
        "description": desc,
        "datePublished": TODAY, "dateModified": TODAY,
        "author": {"@type": "Organization", "name": "Paypr"},
        "publisher": {"@type": "Organization", "name": "Paypr",
                      "logo": {"@type": "ImageObject", "url": f"{BASE}/icon.png"}},
        "mainEntityOfPage": canon, "image": f"{BASE}/icon.png",
    }

    body = f"""<article class="article">
  <div class="crumb"><a href="index.html">Paypr</a> · <a href="babysitter-rates-by-city.html">Rates by city</a> · {name}</div>
  <h1>Babysitter &amp; childcare rates in {name}</h1>
  <p class="meta">Updated {TODAY} · BLS {year} data</p>

  <p>In the {v['area_title']} area, childcare workers earn a median of
  <strong>{usd(h['median'])} per hour</strong>, with most paid between
  {usd(h['p25'])} and {usd(h['p75'])}. Use this as the local anchor for what a
  regular sitter or nanny is worth, then adjust for the factors below.</p>

  <p class="big">{usd(h['median'])}<span style="font-size:16px;color:var(--muted);font-weight:600"> /hr median</span></p>

  <h2>Hourly rate spread in {name}</h2>
  <table>
    <tr><th>Level</th><th>Hourly</th></tr>
    <tr><td>Entry (10th percentile)</td><td>{usd(h['p10'])}</td></tr>
    <tr><td>Lower typical (25th)</td><td>{usd(h['p25'])}</td></tr>
    <tr><td><strong>Median (50th)</strong></td><td><strong>{usd(h['median'])}</strong></td></tr>
    <tr><td>Upper typical (75th)</td><td>{usd(h['p75'])}</td></tr>
    <tr><td>Experienced (90th)</td><td>{usd(h['p90'])}</td></tr>
    <tr><td>Average (mean)</td><td>{usd(h['mean'])}</td></tr>
  </table>

  <div class="tip">These are <strong>childcare-worker wage</strong> figures — what
  employed and regular sitters earn locally. Occasional, on-demand
  <a href="babysitter-hourly-rates.html">date-night babysitting</a> usually pays
  more per hour because it's short-notice and flexible. Treat this as the floor,
  not the ceiling.</div>

  <h2>What raises the rate in {name}</h2>
  <ul>
    <li><strong>More kids:</strong> add about $2–$5/hour per additional child.</li>
    <li><strong>Infants &amp; multiples:</strong> pay more than one school-age child.</li>
    <li><strong>Overnights, holidays &amp; late nights:</strong> expect a premium.</li>
    <li><strong>Extras:</strong> cooking, driving, bath-and-bed nudge it up.</li>
  </ul>

  <div class="tip">Know the hours but not the total? The free
  <a href="nanny-pay-calculator.html">pay calculator</a> turns any rate into a
  weekly, monthly and yearly figure.</div>

  <div class="cta">
    <h2>Track every sitter in one place</h2>
    <p>Different sitters, different rates, different nights — Paypr keeps a running
    balance for each one, so you always know what you owe before you pay.</p>
    <a class="btn" href="{APP}">Download Paypr on the App Store</a>
  </div>

  <p class="note">Source: U.S. Bureau of Labor Statistics, Occupational Employment
  &amp; Wage Statistics (OEWS), {year} — Childcare Workers (SOC 39-9011),
  {v['area_title']} metropolitan area. Public-domain data; presentation by Paypr.
  Local pay varies by neighborhood, experience and demand. General information only.</p>

  <p style="margin-top:24px"><strong>Related:</strong><br>
  <a href="babysitter-rates-by-city.html">Find another city</a> ·
  <a href="babysitter-hourly-rates.html">National babysitter rates</a> ·
  <a href="how-much-to-pay-a-nanny.html">How much to pay a nanny</a> ·
  <a href="nanny-pay-calculator.html">Pay calculator</a></p>
</article>

{FOOTER}
</body>
</html>
"""
    return fname, head(title, desc, canon, jsonld) + body


def lookup_page(metros: dict, meta: dict, featured_files: dict) -> tuple[str, str]:
    fname = "babysitter-rates-by-city.html"
    canon = f"{BASE}/{fname}"
    year = meta["reference_year"]
    title = f"Babysitter & Childcare Rates by City ({year}) — Look Up Any US Metro | Paypr"
    desc = (
        f"Search {meta['metro_count']} US metro areas for local childcare hourly "
        f"rates (BLS {year}). Find your city by name, state or area code."
    )
    jsonld = {
        "@context": "https://schema.org", "@type": "CollectionPage",
        "headline": f"Babysitter & childcare rates by city ({year})",
        "description": desc, "url": canon,
        "publisher": {"@type": "Organization", "name": "Paypr",
                      "logo": {"@type": "ImageObject", "url": f"{BASE}/icon.png"}},
    }

    # Featured city rows — one per city, Nanny (BLS) + Babysitter (estimate).
    rows = "\n".join(
        f'      <tr><td><a href="{featured_files[s]}">{short_name(metros[s])}</a></td>'
        f'<td>{usd(metros[s]["hourly"]["median"])}/hr</td>'
        f'<td>{usd(sitter(metros[s]["hourly"]["median"]))}/hr</td></tr>'
        for s in FEATURED if s in metros
    )
    # href map so search results deep-link to featured pages where they exist.
    href_map = {s: featured_files[s] for s in FEATURED if s in metros}

    body = f"""<article class="article">
  <div class="crumb"><a href="index.html">Paypr</a> · Rates by city</div>
  <h1>Babysitter &amp; childcare rates by city</h1>
  <p class="meta">Updated {TODAY} · {meta['metro_count']} US metros · BLS {year} data</p>

  <p>Search any US metro area for local hourly rates — by city, state or BLS area
  code. The <strong>Nanny</strong> figure is the median wage for childcare workers
  (SOC 39-9011) from the U.S. Bureau of Labor Statistics, a good anchor for regular,
  ongoing care. The <strong>Babysitter</strong> figure estimates occasional,
  on-demand pay at about {int(round((SITTER_PREMIUM - 1) * 100))}% above that local
  wage (see method below). Featured cities have full guides:</p>

  <table class="res">
    <tr><th>City</th><th>Nanny <span class="note">(regular)</span></th><th>Babysitter <span class="note">(occasional)</span></th></tr>
{rows}
  </table>

  <h2>Look up your city</h2>
  <input id="q" type="search" placeholder="Type a city, state or area code — e.g. Portland, OR or 38900" autocomplete="off" aria-label="Search metro areas">
  <p class="note" id="count"></p>
  <table class="res">
    <tr><th>City</th><th>Nanny <span class="note">(regular)</span></th><th>Babysitter <span class="note">(occasional)</span></th></tr>
    <tbody id="res"></tbody>
  </table>

  <div class="cta">
    <h2>Track every sitter in one place</h2>
    <p>Paypr keeps a running balance for each sitter, so you always know what you
    owe before you pay.</p>
    <a class="btn" href="{APP}">Download Paypr on the App Store</a>
  </div>

  <p class="note"><strong>Method &amp; sources.</strong> Nanny figures are median
  hourly wages for Childcare Workers (SOC 39-9011) by metro area, from the U.S.
  Bureau of Labor Statistics, OEWS {year} (public-domain data). Babysitter figures
  are a Paypr estimate — the same local wage multiplied by {SITTER_PREMIUM}× to
  reflect the on-demand premium occasional sitters command (national UrbanSitter /
  Sittercity rates run roughly that much above the childcare wage), rounded to the
  nearest $0.50. Estimates only; local pay varies by experience, hours and demand.</p>

  <p style="margin-top:24px"><strong>Related:</strong><br>
  <a href="babysitter-hourly-rates.html">National babysitter rates</a> ·
  <a href="how-much-to-pay-a-nanny.html">How much to pay a nanny</a> ·
  <a href="nanny-pay-calculator.html">Pay calculator</a></p>
</article>

{FOOTER}
<script>
const HREF = {json.dumps(href_map)};
let ROWS = [];
fetch('data/babysitter-rates.json').then(r=>r.json()).then(d=>{{
  ROWS = Object.entries(d.metros).map(([slug,v])=>({{
    slug, title:v.area_title, code:v.area_code||'', med:v.hourly.median,
    p25:v.hourly.p25, p75:v.hourly.p75,
    hay:(v.area_title+' '+(v.state||'')+' '+(v.area_code||'')).toLowerCase()
  }}));
  render('');
}});
const PREMIUM = {SITTER_PREMIUM};
function money(x){{return (x||x===0)?'$'+Number(x).toFixed(2):'—';}}
function sitter(m){{return (m||m===0)?'$'+(Math.round(m*PREMIUM*2)/2).toFixed(2):'—';}}
function render(q){{
  q=q.trim().toLowerCase();
  let list = q ? ROWS.filter(r=>r.hay.includes(q)) : ROWS;
  list = list.slice().sort((a,b)=>a.title.localeCompare(b.title)).slice(0,60);
  const res=document.getElementById('res'), cnt=document.getElementById('count');
  res.innerHTML = list.map(r=>{{
    const label = HREF[r.slug] ? `<a href="${{HREF[r.slug]}}">${{r.title}}</a>` : r.title;
    return `<tr><td>${{label}}</td><td>${{money(r.med)}}/hr</td>`+
           `<td>${{sitter(r.med)}}/hr</td></tr>`;
  }}).join('') || '<tr><td colspan="3">No metro matches that. Try a bigger nearby city.</td></tr>';
  cnt.textContent = q ? `${{list.length}} match${{list.length===1?'':'es'}} shown` : 'Start typing to filter all metros.';
}}
document.getElementById('q').addEventListener('input',e=>render(e.target.value));
</script>
</body>
</html>
"""
    return fname, head(title, desc, canon, jsonld) + body


def patch_sitemap(files: list[str]) -> int:
    sm = DOCS / "sitemap.xml"
    xml = sm.read_text()
    added = 0
    for f in files:
        loc = f"{BASE}/{f}"
        if loc in xml:
            continue
        entry = (f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n"
                 f"    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n")
        xml = xml.replace("</urlset>", entry + "</urlset>")
        added += 1
    sm.write_text(xml)
    return added


def main() -> None:
    data = json.loads(DATA.read_text())
    metros, meta = data["metros"], data["meta"]

    featured_files = {s: f"babysitter-rates-{short_slug(metros[s])}.html"
                      for s in FEATURED if s in metros}
    missing = [s for s in FEATURED if s not in metros]
    if missing:
        print("WARN missing featured slugs:", missing)

    written = []
    for slug in FEATURED:
        if slug not in metros:
            continue
        fname, html = metro_page(slug, metros[slug], meta)
        (DOCS / fname).write_text(html)
        written.append(fname)

    lf, lhtml = lookup_page(metros, meta, featured_files)
    (DOCS / lf).write_text(lhtml)
    written.append(lf)

    added = patch_sitemap(written)
    print(f"Wrote {len(written)} pages ({len(featured_files)} metros + lookup).")
    print(f"sitemap.xml: +{added} new URLs.")


if __name__ == "__main__":
    main()
