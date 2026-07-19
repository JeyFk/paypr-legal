#!/usr/bin/env python3
"""
gen_icons.py — Generate the website's card icons in the app-icon style.

Emerald gradient tile (sampled from icon.png: #14BC7B -> #085C3B), cream glyph
(#FDFBF5) with a green accent (#10A86B). Each icon is a self-contained SVG that
replaces a flat emoji in guides.html / index.html.

Run:  python3 gen_icons.py   ->  writes docs/icons/<name>.svg
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "docs" / "icons"
CREAM = "#FDFBF5"
FOLD = "#DFE9E1"
ACCENT = "#10A86B"
MUTE = "#BFDBCB"
DARK = "#0D925D"

HEAD = ('<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}">\n'
        '  <defs><linearGradient id="tile" x1="0" y1="0" x2="1" y2="1">\n'
        '    <stop offset="0" stop-color="#14BC7B"/><stop offset="1" stop-color="#085C3B"/>\n'
        '  </linearGradient></defs>\n'
        '  <rect width="48" height="48" rx="11" fill="url(#tile)"/>\n')
TAIL = "</svg>\n"

# name -> (aria label, glyph markup)
ICONS = {
"pay": ("Pay", f'''
  <path d="M16 12 h11 l7 7 v15 a2 2 0 0 1-2 2 H16 a2 2 0 0 1-2-2 V14 a2 2 0 0 1 2-2 Z" fill="{CREAM}"/>
  <path d="M27 12 v5 a2 2 0 0 0 2 2 h5 Z" fill="{FOLD}"/>
  <rect x="18.5" y="21.5" width="11" height="1.8" rx="0.9" fill="{MUTE}"/>
  <rect x="18.5" y="24.8" width="7" height="1.8" rx="0.9" fill="{MUTE}"/>
  <text x="24" y="34" text-anchor="middle" font-family="-apple-system,Helvetica,Arial,sans-serif" font-size="9.5" font-weight="800" fill="{ACCENT}">$312</text>'''),

"location": ("Location", f'''
  <path d="M24 11.5 c-5.2 0-9.3 4.1-9.3 9.3 0 6.8 9.3 15.7 9.3 15.7 s9.3-8.9 9.3-15.7 c0-5.2-4.1-9.3-9.3-9.3 Z" fill="{CREAM}"/>
  <circle cx="24" cy="20.8" r="3.5" fill="{DARK}"/>'''),

"city": ("City", f'''
  <rect x="13" y="23" width="7" height="13" rx="1" fill="{CREAM}"/>
  <rect x="20.5" y="15" width="7" height="21" rx="1" fill="{CREAM}"/>
  <rect x="28" y="19" width="7" height="17" rx="1" fill="{CREAM}"/>
  <g fill="{ACCENT}"><rect x="22.5" y="18" width="1.6" height="1.6"/><rect x="24.9" y="18" width="1.6" height="1.6"/><rect x="22.5" y="21.5" width="1.6" height="1.6"/><rect x="24.9" y="21.5" width="1.6" height="1.6"/></g>'''),

"cleaning": ("Cleaning", f'''
  <rect x="19" y="19" width="12" height="16" rx="2.5" fill="{CREAM}"/>
  <rect x="22" y="14.5" width="5" height="4.5" fill="{CREAM}"/>
  <path d="M22 14.5 h-4.5 v3 h4.5 Z" fill="{CREAM}"/>
  <rect x="21.5" y="24" width="7" height="7" rx="1.2" fill="{ACCENT}"/>
  <g fill="{MUTE}"><circle cx="14.5" cy="11.5" r="1"/><circle cx="13" cy="14.5" r="1"/><circle cx="14.5" cy="17.5" r="1"/></g>'''),

"books": ("Books", f'''
  <path d="M24 17.2 c-2.6-1.7-6-1.7-8.4-0.8 v13.8 c2.4-0.9 5.8-0.9 8.4 0.8 c2.6-1.7 6-1.7 8.4-0.8 V16.4 c-2.4-0.9-5.8-0.9-8.4 0.8 Z" fill="{CREAM}"/>
  <line x1="24" y1="17.2" x2="24" y2="31" stroke="{ACCENT}" stroke-width="1.5"/>'''),

"tax": ("Tax", f'''
  <path d="M16 12 h16 v20 l-2.7 1.8 -2.6-1.8 -2.7 1.8 -2.7-1.8 -2.6 1.8 L16 32 Z" fill="{CREAM}"/>
  <rect x="19" y="16" width="10" height="1.8" rx="0.9" fill="{MUTE}"/>
  <text x="24" y="29" text-anchor="middle" font-family="-apple-system,Helvetica,Arial,sans-serif" font-size="11" font-weight="800" fill="{ACCENT}">%</text>'''),

"ledger": ("Ledger", f'''
  <rect x="15" y="13" width="18" height="22" rx="2.5" fill="{CREAM}"/>
  <path d="M15 15.5 a2.5 2.5 0 0 1 2.5-2.5 H20 v22 h-2.5 A2.5 2.5 0 0 1 15 32.5 Z" fill="{ACCENT}"/>
  <g fill="{MUTE}"><rect x="22.5" y="19" width="7.5" height="1.7" rx="0.85"/><rect x="22.5" y="23" width="7.5" height="1.7" rx="0.85"/><rect x="22.5" y="27" width="5.5" height="1.7" rx="0.85"/></g>'''),

"calculator": ("Calculator", f'''
  <rect x="15" y="12" width="18" height="24" rx="3" fill="{CREAM}"/>
  <rect x="18" y="15" width="12" height="5" rx="1.2" fill="{ACCENT}"/>
  <g fill="{DARK}">
    <rect x="18.5" y="23" width="3" height="3" rx="0.8"/><rect x="22.5" y="23" width="3" height="3" rx="0.8"/><rect x="26.5" y="23" width="3" height="3" rx="0.8"/>
    <rect x="18.5" y="27.5" width="3" height="3" rx="0.8"/><rect x="22.5" y="27.5" width="3" height="3" rx="0.8"/><rect x="26.5" y="27.5" width="3" height="3" rx="0.8"/>
  </g>'''),

"bottle": ("Bottle", f'''
  <rect x="21.7" y="11.5" width="4.6" height="3" rx="1.5" fill="{CREAM}"/>
  <rect x="20.3" y="14.5" width="7.4" height="2.6" rx="1" fill="{CREAM}"/>
  <rect x="19.7" y="17.1" width="8.6" height="17.4" rx="3" fill="{CREAM}"/>
  <g stroke="{ACCENT}" stroke-width="1.3" stroke-linecap="round"><line x1="21.5" y1="22" x2="24.5" y2="22"/><line x1="21.5" y1="25" x2="24.5" y2="25"/><line x1="21.5" y1="28" x2="24.5" y2="28"/></g>'''),

"chart": ("Chart", f'''
  <rect x="14" y="26" width="5.5" height="9" rx="1" fill="{CREAM}"/>
  <rect x="21.2" y="20" width="5.5" height="15" rx="1" fill="{CREAM}"/>
  <rect x="28.5" y="14.5" width="5.5" height="20.5" rx="1" fill="{ACCENT}"/>'''),

"timer": ("Timer", f'''
  <rect x="21.3" y="10.3" width="5.4" height="3.2" rx="1.2" fill="{CREAM}"/>
  <circle cx="24" cy="25" r="9.6" fill="{CREAM}"/>
  <line x1="24" y1="25" x2="24" y2="19.2" stroke="{ACCENT}" stroke-width="1.9" stroke-linecap="round"/>
  <line x1="24" y1="25" x2="28" y2="26.6" stroke="{DARK}" stroke-width="1.7" stroke-linecap="round"/>
  <circle cx="24" cy="25" r="1.5" fill="{DARK}"/>'''),

"money": ("Money", f'''
  <rect x="15.5" y="21" width="17" height="8.5" fill="{CREAM}"/>
  <ellipse cx="24" cy="29.5" rx="8.5" ry="3.1" fill="{CREAM}"/>
  <ellipse cx="24" cy="21" rx="8.5" ry="3.1" fill="#FFFFFF"/>
  <line x1="15.5" y1="25.2" x2="32.5" y2="25.2" stroke="{MUTE}" stroke-width="1"/>
  <text x="24" y="23.2" text-anchor="middle" font-family="-apple-system,Helvetica,Arial,sans-serif" font-size="7.5" font-weight="800" fill="{ACCENT}">$</text>'''),

"check": ("Check", f'''
  <circle cx="24" cy="24" r="11" fill="{CREAM}"/>
  <path d="M18.5 24.3 l3.6 3.6 l7.2-7.6" fill="none" stroke="{ACCENT}" stroke-width="2.7" stroke-linecap="round" stroke-linejoin="round"/>'''),

"document": ("Document", f'''
  <path d="M17 12 h9 l6 6 v16 a2 2 0 0 1-2 2 H17 a2 2 0 0 1-2-2 V14 a2 2 0 0 1 2-2 Z" fill="{CREAM}"/>
  <path d="M26 12 v4 a2 2 0 0 0 2 2 h4 Z" fill="{FOLD}"/>
  <g fill="{MUTE}"><rect x="19.5" y="22" width="9" height="1.7" rx="0.85"/><rect x="19.5" y="26" width="9" height="1.7" rx="0.85"/><rect x="19.5" y="30" width="6.5" height="1.7" rx="0.85"/></g>'''),

"lock": ("Lock", f'''
  <rect x="16" y="22" width="16" height="13" rx="2.6" fill="{CREAM}"/>
  <path d="M19.2 22 v-3.2 a4.8 4.8 0 0 1 9.6 0 V22" fill="none" stroke="{CREAM}" stroke-width="2.4"/>
  <circle cx="24" cy="27.3" r="2" fill="{ACCENT}"/>
  <rect x="23.2" y="28.4" width="1.6" height="3.4" rx="0.8" fill="{ACCENT}"/>'''),
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (label, glyph) in ICONS.items():
        svg = HEAD.format(label=label) + glyph.strip("\n") + "\n" + TAIL
        (OUT / f"{name}.svg").write_text(svg)
    print(f"Wrote {len(ICONS)} icons to {OUT}")


if __name__ == "__main__":
    main()
