from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile

root = Path(__file__).resolve().parent.parent

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.duplicate_ids = set()
        self.catalog_entry = None
        self.catalog_numbered = 0
        self.catalog_linked = 0
        self.catalog_missing = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            if a['id'] in self.ids:
                self.duplicate_ids.add(a['id'])
            self.ids.add(a['id'])
        if tag == 'a' and a.get('href'):
            self.links.append(a['href'])
        if tag == 'div' and 'catalog-entry' in a.get('class', '').split():
            self.catalog_entry = {'numbered': False, 'linked': False, 'text': ''}
        if self.catalog_entry is not None:
            if tag == 'span' and 'catalog-code' in a.get('class', '').split():
                self.catalog_entry['numbered'] = True
            if tag == 'a' and a.get('href', '').startswith('foundations-') and '#section-' in a['href']:
                self.catalog_entry['linked'] = True
    def handle_data(self, data):
        if self.catalog_entry is not None:
            self.catalog_entry['text'] += data
    def handle_endtag(self, tag):
        if tag == 'div' and self.catalog_entry is not None:
            entry = self.catalog_entry
            if entry['numbered']:
                self.catalog_numbered += 1
                self.catalog_linked += int(entry['linked'])
                if not entry['linked']:
                    self.catalog_missing.append(entry['text'].strip())
            self.catalog_entry = None

pages = {}
for path in root.rglob('*.html'):
    if '.git' in path.parts:
        continue
    parser = Links()
    parser.feed(path.read_text(encoding='utf-8'))
    pages[path.resolve()] = parser
missing = []
for path, parser in pages.items():
    for duplicate_id in parser.duplicate_ids:
        missing.append((path.relative_to(root), duplicate_id, 'duplicate id'))
    for entry in parser.catalog_missing:
        missing.append((path.relative_to(root), entry, 'numbered catalog entry lacks section link'))
    for href in parser.links:
        url = urlsplit(href)
        if url.scheme or url.netloc:
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        if target.is_dir():
            target /= 'index.html'
        if not target.exists():
            missing.append((path.relative_to(root), href, 'missing file'))
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            missing.append((path.relative_to(root), href, 'missing fragment'))
for path in [root / 'topics' / f'foundations-{n}.html' for n in range(2, 11)] + [root / 'archive' / 'math-foundations-knowledge.html']:
    source = path.read_text(encoding='utf-8')
    if 'tex-chtml.js' not in source or source.count('\\(') != source.count('\\)') or source.count('\\[') != source.count('\\]'):
        missing.append((path.relative_to(root), '', 'MathJax script or TeX delimiter check failed'))
with ZipFile(root / 'downloads' / 'math-study-documents.zip') as bundle:
    for n in range(1, 17):
        source = root / 'docs' / 'foundations' / f'{n}.md'
        name = f'math-study-documents/foundations/{n}.md'
        if name not in bundle.namelist() or bundle.read(name) != source.read_bytes():
            missing.append((Path('downloads/math-study-documents.zip'), name, 'source does not match archive'))
for path, href, reason in missing:
    print(f'{path}: {href}: {reason}')
for path, parser in pages.items():
    if parser.catalog_numbered:
        print(f'{path.relative_to(root)}: {parser.catalog_linked}/{parser.catalog_numbered} numbered entries link to a section')
print(f'Checked {len(pages)} HTML files; {len(missing)} static validation issues')
raise SystemExit(bool(missing))
