"""Detect stale chapter review snapshots; does not prove mathematics."""
import hashlib
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
records = json.loads((root / 'docs/章节复核清单-2026-11-08.json').read_text())
seen = set()
for row in records:
    path = root / row['source']
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == row['source_sha256'], f'{path}: 内容变化，须重新审阅'
    text = raw.decode()
    headings = list(re.finditer(r'^## .+$', text, re.M))
    sections = {m.group()[3:]: text[m.start():headings[i+1].start() if i+1<len(headings) else len(text)] for i,m in enumerate(headings)}
    block = sections[row['chapter']]
    assert hashlib.sha256(block.encode()).hexdigest() == row['chapter_sha256']
    assert re.findall(r'^### (.+)$', block, re.M) == row['subsections']
    key = (row['source'], row['chapter'])
    assert key not in seen
    seen.add(key)
expected = set()
for source in {r['source'] for r in records}:
    expected.update((source, title) for title in re.findall(r'^## (.+)$', (root/source).read_text(), re.M))
assert expected == seen
print(f'{len(seen)} 章快照及小节清单一致；此检查不判断数学命题真假。')
