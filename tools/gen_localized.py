#!/usr/bin/env python3
"""Build the four language experiences. Standard library only; output is committed.

Run from any directory. Existing English content is only decorated with language
links and alternate metadata; the historical redirects and sitemap dates survive.
"""
from __future__ import annotations
import csv
import html
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / 'docs'
BASE = 'https://usepaypr.com'
APP = 'https://apps.apple.com/app/id6778970494'
DATE = '2026-09-30'
LANGUAGES = ('es', 'fr', 'de', 'ar')
SLUGS = {'home':'', 'support':'support', 'privacy':'privacy', 'terms':'terms',
         'about':'about', 'guides':'guides', 'tracking':'how-to-track-what-you-owe-your-nanny',
         'template':'nanny-timesheet-template'}
NAMES = {'en':'English','es':'Español','fr':'Français','de':'Deutsch','ar':'العربية'}
EN_UI = {'languages':'Language','home_suffix':' — home'}
ESC = html.escape

def read_locale(lang):
    return json.loads((ROOT / 'tools/i18n' / f'{lang}.json').read_text())

def route(lang, key):
    prefix = '' if lang == 'en' else '/' + lang
    return prefix + '/' + SLUGS[key]

def alternates(key):
    return '\n'.join(f'<link rel="alternate" hreflang="{lang}" href="{BASE}{route(lang, key)}">'
                     for lang in ('en', *LANGUAGES)) + f'\n<link rel="alternate" hreflang="x-default" href="{BASE}{route("en", key)}">'

def language_nav(lang, key, ui):
    links = []
    for target, name in NAMES.items():
        path = route(target, key) if key else route(target, 'home')
        label = name if key else name + ui['home_suffix']
        current = ' aria-current="page"' if target == lang and key else ''
        links.append(f'<a href="{path}" lang="{target}" hreflang="{target}" dir="auto"{current}>{ESC(label)}</a>')
    return '<!-- intl-language --><nav class="intl-language" aria-label="'+ESC(ui['languages'])+'"><span>'+ESC(ui['languages'])+'</span>'+''.join(links)+'</nav><!-- /intl-language -->'

def decorate_english(source, path):
    """Idempotent public hook for the existing English city-page generator."""
    key = next((k for k in SLUGS if route('en', k) == path), None)
    source = re.sub(r'<!-- intl-head -->.*?<!-- /intl-head -->\s*', '', source, flags=re.S)
    source = re.sub(r'<!-- intl-language -->.*?<!-- /intl-language -->', '', source, flags=re.S)
    head = '<!-- intl-head -->\n<link rel="stylesheet" href="/sage/international.css?v=20260929">\n'
    if key:
        head += alternates(key) + '\n'
    head += '<!-- /intl-head -->\n'
    source = source.replace('</head>', head + '</head>', 1)
    source = source.replace('</header>', '</header>' + language_nav('en', key, EN_UI), 1)
    if '/sage/conversions.js' not in source:
        source = source.replace('</head>', '<script src="/sage/conversions.js" defer></script>\n</head>', 1)
    return source

def paragraph(text):
    return '<p>' + ESC(text) + '</p>'

def sections(items, lang):
    result = ''
    for heading, body in items:
        for key in SLUGS:
            body = body.replace('{'+key+'}', route(lang, key))
        result += '<section><h2>'+ESC(heading)+'</h2>'+body+'</section>\n'
    return result

def card(lang, key, data):
    p = data['pages'][key]
    return f'<a class="intl-card" href="{route(lang,key)}"><h2>{ESC(p["title"])}</h2><p>{ESC(p["description"])}</p><span aria-hidden="true">↗</span></a>'

def shell(lang, key, data, title, description, body, path=None, market='global'):
    ui = data['ui']; path = path or route(lang, key)
    home = route(lang, 'home')
    schema = {'@context':'https://schema.org','@type':'WebPage','name':title,
              'description':description,'url':BASE+path,'inLanguage':lang if market=='global' else 'es-'+market,
              'publisher':{'@type':'Organization','name':'QAtion','url':BASE+'/'}}
    if key == 'home':
        schema = {'@context':'https://schema.org','@type':'SoftwareApplication','name':'Paypr',
                  'description':description,'url':BASE+path,'operatingSystem':'iOS 17.0 or later',
                  'applicationCategory':'ProductivityApplication','inLanguage':lang,'downloadUrl':APP,
                  'author':{'@type':'Organization','name':'QAtion'}}
    navlinks = f'<a href="{home}#how">{ESC(ui["how"])}</a><a href="{home}#pricing">{ESC(ui["pricing"])}</a><a href="{route(lang,"guides")}">{ESC(ui["guides"])}</a>'
    footlinks = ''.join(f'<a href="{route(lang,k)}">{ESC(ui[k])}</a>' for k in ('about','support','privacy','terms'))
    language = lang if market == 'global' else 'es-'+market
    return f'''<!doctype html>
<html lang="{language}" dir="{data['direction']}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{ESC(title)} | Paypr</title><meta name="description" content="{ESC(description)}">
<link rel="canonical" href="{BASE}{path}">
{alternates(key) if key else ''}
<meta name="theme-color" content="#faf9f3"><meta name="apple-itunes-app" content="app-id=6778970494">
<link rel="icon" type="image/png" sizes="192x192" href="/favicon.png?v=circle-20260928"><link rel="apple-touch-icon" href="/icon.png?v=mascot-20260915">
<meta property="og:type" content="website"><meta property="og:site_name" content="Paypr"><meta property="og:title" content="{ESC(title)}"><meta property="og:description" content="{ESC(description)}"><meta property="og:url" content="{BASE}{path}"><meta property="og:image" content="{BASE}/icon.png"><meta property="og:image:alt" content="Paypr">
<meta name="twitter:card" content="summary"><meta name="twitter:title" content="{ESC(title)}"><meta name="twitter:description" content="{ESC(description)}"><meta name="twitter:image" content="{BASE}/icon.png">
<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')}</script>
<link rel="stylesheet" href="/sage/sage-nav.css?v=sage-20260915"><link rel="stylesheet" href="/sage/international.css?v=20260929">
<script src="/sage/navigation.js?v=sage-20260915" defer></script><script src="/sage/conversions.js" defer></script>
<script defer data-website-id="dfid_hJ2Kroo4GcBHH6S3fdlZU" data-domain="usepaypr.com" src="https://datafa.st/js/script.js"></script>
</head><body class="intl-page"><a class="sage-skip" href="#main">{ESC(ui['skip'])}</a>
<header class="sage-header"><a class="sage-brand" href="{home}" aria-label="Paypr — {ESC(ui['home'])}" dir="ltr">paypr<span>.</span></a><nav class="sage-nav" aria-label="{ESC(ui['navigation'])}">{navlinks}</nav><a class="sage-download" href="{APP}">{ESC(ui['download'])} <span aria-hidden="true">↗</span></a><details class="sage-menu"><summary>{ESC(ui['menu'])}<span aria-hidden="true">＋</span></summary><nav aria-label="{ESC(ui['navigation'])}">{navlinks}<a href="{APP}">{ESC(ui['download'])}</a></nav></details></header>
{language_nav(lang,key,ui)}
<main id="main">{body}</main>
<footer class="intl-footer"><a class="intl-wordmark" href="{home}" dir="ltr">paypr.</a><span>© 2026 QAtion · Paypr</span><nav aria-label="{ESC(ui['navigation'])}">{footlinks}</nav></footer>
<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token":"0a79256628664b25bdf9093c0c977cf2"}}'></script>
</body></html>\n'''

def homepage(lang, data):
    h=data['home']; ui=data['ui']
    features=''.join(f'<article><span class="intl-number">0{i}</span><h3>{ESC(t)}</h3>{paragraph(p)}</article>' for i,(t,p) in enumerate(h['features'],1))
    faq=''.join(f'<details><summary>{ESC(q)}</summary>{paragraph(a)}</details>' for q,a in h['faq'])
    return f'''<section class="intl-hero intl-wrap"><div><p class="intl-eyebrow">{ESC(h['eyebrow'])}</p><h1>{ESC(h['title'])}</h1><p class="intl-lead">{ESC(h['lead'])}</p><a class="intl-button" href="{APP}">{ESC(ui['download'])} <span aria-hidden="true">↗</span></a><p class="intl-note">{ESC(h['free'])}</p></div><div class="intl-phone"><img src="/sage/i18n/{lang}/home.png" width="1320" height="2868" alt="{ESC(ui['shot_alt'])}" fetchpriority="high"></div></section>
<section class="intl-wrap intl-section" id="how"><p class="intl-eyebrow">01 / {ESC(ui['how'])}</p><h2>{ESC(h['eyebrow'])}</h2><div class="intl-steps">{features}</div></section>
<section class="intl-band"><div class="intl-wrap"><h2>{ESC(h['contractor_title'])}</h2>{paragraph(h['contractor'])}</div></section>
<section class="intl-wrap intl-section" id="pricing"><p class="intl-eyebrow">02 / {ESC(ui['pricing'])}</p><h2>{ESC(ui['pricing'])}</h2><div class="intl-prices"><article><h3>{ESC(ui['free'])}</h3>{paragraph(h['free'])}</article><article><h3>{ESC(ui['pro'])}</h3>{paragraph(h['pro'])}</article></div>{paragraph(h['pricing_note'])}<p class="intl-note">{ESC(h['privacy'])}</p></section>
<section class="intl-wrap intl-section"><p class="intl-eyebrow">03 / {ESC(ui['support'])}</p><h2>{ESC(ui['support'])}</h2><div class="intl-faq">{faq}</div></section>
<section class="intl-wrap intl-section"><h2>{ESC(ui['guides'])}</h2><div class="intl-cards">{card(lang,'tracking',data)}{card(lang,'template',data)}</div><a href="{route(lang,'guides')}">{ESC(ui['guides'])} <span aria-hidden="true">↗</span></a></section>'''

def downloads(lang, data):
    ui=data['ui']
    files=[('nanny-timesheet.csv','blank_time'),('nanny-timesheet-example.csv','example_time'),('nanny-payment-log.csv','blank_pay'),('nanny-payment-log-example.csv','example_pay')]
    return '<section class="intl-downloads"><h2>'+ESC(ui['downloads'])+'</h2><ul>'+''.join(f'<li><a href="/downloads/{lang}/{file}" download>{ESC(ui[label])} (CSV)</a></li>' for file,label in files)+'</ul><p class="intl-note">'+ESC(ui['print'])+' · ⌘P / Ctrl+P</p></section>'

def article(lang, key, data, page):
    ui=data['ui']
    body=f'<article class="intl-article"><p class="intl-eyebrow"><a href="{route(lang,"home")}">Paypr</a> / {ESC(ui["guides"] if key in ("tracking","template",None) else ui[key])}</p><h1>{ESC(page["title"])}</h1><p class="intl-lead">{ESC(page["description"])}</p><p class="intl-note">{ESC(ui["legal_date"] if key in ("privacy","terms") else ui["updated"])}</p>'
    if key=='template': body+=downloads(lang,data)
    body+=sections(page['sections'],lang)
    if key not in ('privacy','terms'):
        other='tracking' if key=='template' else 'template'
        body+=f'<aside class="intl-related"><h2>{ESC(ui["related"])}</h2><a href="{route(lang,other)}">{ESC(data["pages"][other]["title"])}</a><p><a class="intl-button" href="{APP}">{ESC(ui["download"])}</a></p></aside>'
    return body+'</article>'

def write_page(path, source):
    target=DOCS/(path.lstrip('/')+'index.html' if path.endswith('/') else path.lstrip('/')+'.html')
    target.parent.mkdir(parents=True,exist_ok=True); target.write_text(source)

def write_csv(lang,data):
    dest=DOCS/'downloads'/lang; dest.mkdir(parents=True,exist_ok=True)
    c=data['csv']; person=c['person']; currency=c['currency']
    rows=[['2026-09-15',person,'16:00','18:30','0','2.5','20','50',currency,c['note']],['2026-09-17',person,'16:00','19:00','0','3','20','60',currency,c['note']]]
    payments=[['2026-09-18',person,'40',currency,c['method'],'01'],['2026-09-21',person,'30',currency,c['method'],'02']]
    for name,header,body in [('nanny-timesheet',c['time'],rows),('nanny-payment-log',c['payment'],payments)]:
        for example in (False,True):
            with (dest/(name+('-example' if example else '')+'.csv')).open('w',encoding='utf-8-sig',newline='') as stream:
                writer=csv.writer(stream);writer.writerow(header)
                if example:writer.writerows(body)

def main():
    locales={lang:read_locale(lang) for lang in LANGUAGES}
    markets=json.loads((ROOT/'tools/i18n/markets.json').read_text())
    manifest=[]
    for lang,data in locales.items():
        for key in SLUGS:
            if key=='home':
                title=data['home']['title'];desc=data['home']['description'];body=homepage(lang,data)
            elif key=='guides':
                title=data['ui']['guides'];desc=data['ui']['guide_intro']
                body=f'<section class="intl-article"><h1>{ESC(title)}</h1><p class="intl-lead">{ESC(desc)}</p><div class="intl-cards">'+card(lang,'tracking',data)+card(lang,'template',data)+'</div>'
                if lang=='es':
                    body+='<h2>España y México</h2><div class="intl-cards">'+''.join(f'<a class="intl-card" href="{p["path"]}"><h3>{ESC(p["title"])}</h3>{paragraph(p["description"])}</a>' for p in markets)+'</div>'
                body+='</section>'
            else:
                page=data['pages'][key];title=page['title'];desc=page['description'];body=article(lang,key,data,page)
            path=route(lang,key)
            write_page(path,shell(lang,key,data,title,desc,body))
            manifest.append({'path':path,'language':lang,'market':'global','page':key,'title':title,'lastmod':DATE})
        write_csv(lang,data)
    for page in markets:
        write_page(page['path'],shell('es',None,locales['es'],page['title'],page['description'],article('es',None,locales['es'],page),path=page['path'],market=page['market']))
        manifest.append({k:page[k] for k in ('path','language','market','title')}|{'page':'country-guide','lastmod':DATE})
    for file in DOCS.glob('*.html'):
        if file.name.startswith('google'):continue
        path='/' if file.stem=='index' else '/'+file.stem
        file.write_text(decorate_english(file.read_text(),path))
    ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns)
    tree=ET.parse(DOCS/'sitemap.xml');root=tree.getroot()
    old={n.find('{'+ns+'}loc').text:n for n in root}
    for page in manifest:
        url=BASE+page['path']
        if url not in old:
            node=ET.SubElement(root,'{'+ns+'}url');ET.SubElement(node,'{'+ns+'}loc').text=url
            ET.SubElement(node,'{'+ns+'}lastmod').text=DATE
    ET.indent(tree,space='  ');tree.write(DOCS/'sitemap.xml',encoding='utf-8',xml_declaration=True)
    redirects=DOCS/'_redirects';text=redirects.read_text()
    text=re.sub(r'\n# BEGIN INTERNATIONAL.*?# END INTERNATIONAL\n?','',text,flags=re.S)
    lines=['','\n# BEGIN INTERNATIONAL']
    for page in manifest:
        p=page['path']
        if p.endswith('/'):
            lines.extend([f'{p[:-1]} {p} 301',f'{p}index.html {p} 301'])
        else:lines.append(f'{p}.html {p} 301')
    redirects.write_text(text.rstrip()+'\n'+'\n'.join(lines)+'\n# END INTERNATIONAL\n')
    (DOCS/'data/localized-pages.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(f'Generated {len(manifest)} pages, {len(LANGUAGES)*4} CSVs; sitemap: {len(root)} URLs.')

if __name__=='__main__':main()
