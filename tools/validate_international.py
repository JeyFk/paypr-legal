#!/usr/bin/env python3
"""Check the published static contract; exits nonzero on any failure."""
import csv
import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote

ROOT=Path(__file__).resolve().parent.parent
DOCS=ROOT/'docs'
BASE='https://usepaypr.com'
errors=[]
def check(condition,message):
    if not condition:errors.append(message)

class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.tags=[];self.ids=set();self.schemas=[];self.script=None;self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs);self.tags.append((tag,a))
        if a.get('id'):self.ids.add(a['id'])
        if tag=='script' and a.get('type')=='application/ld+json':self.script=''
    def handle_data(self,text):
        if self.script is not None:self.script+=text
    def handle_endtag(self,tag):
        if tag=='script' and self.script is not None:
            self.schemas.append(json.loads(self.script));self.script=None
    def select(self,tag,**attrs):
        return [a for t,a in self.tags if t==tag and all(a.get(k)==v for k,v in attrs.items())]

def file_for(path):
    target=DOCS/unquote(path.lstrip('/'))
    if target.is_dir():return target/'index.html'
    if not target.suffix:return target.with_suffix('.html')
    return target

manifest=json.loads((DOCS/'data/localized-pages.json').read_text())
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls=[x.text for x in ET.parse(DOCS/'sitemap.xml').findall('s:url/s:loc',ns)]
check(len(urls)==len(set(urls))==88,'Expected 88 unique sitemap URLs')
check(len(manifest)==34,'Expected 34 localized pages')
cache={};references=0;schemas=0
for url in urls:
    file=file_for(urlparse(url).path)
    check(file.is_file(),'Missing sitemap page: '+url)
    if not file.is_file():continue
    text=file.read_text();p=Page(text);cache[url]=p;schemas+=len(p.schemas)
    check(p.select('link',rel='canonical')==[{'rel':'canonical','href':url}],'Canonical mismatch: '+url)
    check(len(p.select('h1'))==1,'H1 count: '+url)
    check(len(p.select('nav',**{'class':'intl-language'}))==1,'Language navigation: '+url)
    check('noindex' not in text,'Unexpected noindex: '+url)
    check(not re.search(r'\{(?:home|tracking|template|support|privacy|terms|about)\}',text),'Unresolved template: '+url)
    for tag,attrs in p.tags:
        if tag=='img':check('alt' in attrs,'Image without alt: '+url)
        for field in ('href','src'):
            if not attrs.get(field):continue
            dest=urlparse(urljoin(url,attrs[field]))
            if dest.scheme not in ('https','http') or dest.hostname!='usepaypr.com':continue
            references+=1;target=file_for(dest.path)
            check(target.is_file(),'Missing internal reference: '+url+' -> '+attrs[field])
            if dest.fragment and target.is_file() and target.suffix=='.html':
                target_page=Page(target.read_text())
                check(unquote(dest.fragment) in target_page.ids,'Missing fragment: '+url+' -> '+attrs[field])

for item in manifest:
    url=BASE+item['path'];p=cache[url]
    check(p.select('html')[0].get('lang')==item['language'],'HTML language: '+url)
    check(p.select('html')[0].get('dir')==('rtl' if item['language']=='ar' else 'ltr'),'Text direction: '+url)
    alternates=p.select('link',rel='alternate')
    if item['market']=='global':
        check({a['hreflang'] for a in alternates}=={'en','es','fr','de','ar','x-default'},'Incomplete alternates: '+url)
        for a in alternates:
            other=cache.get(a['href']);check(other is not None,'Missing alternate: '+a['href'])
            if other:check(other.select('link',rel='alternate')==alternates,'Nonreciprocal alternate set: '+url)
    else:check(not alternates,'Distinct country guide should not claim translation equivalence: '+url)
    for schema in p.schemas:check(schema['inLanguage']==item['language'],'Schema language: '+url)
    check(not p.select('meta',property='og:image')[0]['content'].endswith('og-image.png'),'English text in social image: '+url)

csv_count=0
for lang in ('es','fr','de','ar'):
    for f in (DOCS/'downloads'/lang).glob('*.csv'):
        rows=list(csv.reader(f.open(encoding='utf-8-sig')));csv_count+=1
        check(len(rows)>0,'Missing CSV headers: '+str(f))
        check(all(len(row)==len(rows[0]) for row in rows),'CSV column mismatch: '+str(f))
        check(len(rows)==(3 if '-example' in f.name else 1),'CSV examples: '+str(f))
    time=list(csv.reader((DOCS/'downloads'/lang/'nanny-timesheet-example.csv').open(encoding='utf-8-sig')))[1:]
    pay=list(csv.reader((DOCS/'downloads'/lang/'nanny-payment-log-example.csv').open(encoding='utf-8-sig')))[1:]
    check(sum(float(r[7]) for r in time)-sum(float(r[2]) for r in pay)==40,'Example reconciliation: '+lang)
check(csv_count==16,'Expected 16 localized CSVs')

redirects=(DOCS/'_redirects').read_text()
for item in manifest:
    path=item['path'];old=path+'index.html' if path.endswith('/') else path+'.html'
    check(f'{old} {path} 301' in redirects,'Missing permanent redirect: '+old)

report={'result':'FAIL' if errors else 'PASS','sitemap_pages':len(urls),'new_pages':len(manifest),'json_ld_blocks':schemas,'internal_references':references,'localized_csvs':csv_count,'errors':errors}
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
