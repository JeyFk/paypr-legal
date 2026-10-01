# International website maintenance

The website adds Spanish (`/es/`), French (`/fr/`), German (`/de/`), and Arabic (`/ar/`). Each has a home page, support, privacy, terms, about, guides index, hours/payment guide, and downloadable timesheet guide. Two separate Spanish country guides cover Spain and Mexico. Arabic uses RTL layout. Original English URLs and redirects stay in place.

Edit copy in `tools/i18n/*.json`, layout in `tools/gen_localized.py`, styles in `docs/sage/international.css`, and analytics in `docs/sage/conversions.js`. Run:

```sh
python3 tools/gen_localized.py
python3 tools/validate_international.py
node --test tools/test_international.cjs
```

Commit the generated HTML, sitemap, redirects, manifest, and CSVs with the source changes. Generation is repeatable. Run the existing English generator only when intentionally updating its city content; it calls the shared language-decoration helper. Do not replace reviewed English pages with old generator output merely to regenerate translations.

Each equivalent page has a self-canonical and reciprocal `en`, `es`, `fr`, `de`, `ar`, `x-default` alternates. Country articles are independent resources, not translations of one another. A link to a language homepage is labelled as such when no equivalent translation exists. Do not add `es-419` to Google hreflang or equate Spanish with a country. Add country variants only when the actual page content warrants them.

The four core paths use existing English slugs for stable page mapping. Visible copy and metadata are localized. New country guides use Spanish slugs. Language choice never triggers an automatic IP/browser-language redirect.

Prices are shown by the App Store. Example earnings in guides and screenshots are illustrative, not suggested wages. Work records are separate from payment-date receipts. CSV downloads are templates with headers/examples, not formula-driven accounting or app imports.

Publish website URLs before releasing an app build or App Store metadata pointing to them. Keep the Mexico guide's release-availability note until the version with MXN is publicly available. Legal text translates the existing policy; separately review policy coverage when data processing changes.

Cloudflare Workers Builds serves `docs/` from `master`; `DEPLOY.md` includes older historical deployment instructions. Verify explicit 301s, query preservation, canonical 200s, true 404s, downloads, and Google verification after deployment. No production configuration change is needed.
