"""Check audit ledger source fingerprints and proof evidence integrity."""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parents[1]
ledger = json.loads((root / 'docs' / '大学数学逐条核验清单.json').read_text(encoding='utf-8'))
source_lines = {}
for name, expected in ledger['source_sha256'].items():
    raw = (root / 'docs' / name).read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != expected:
        raise SystemExit(f'{name}: 原文已改变；逐条对照并更新快照后再使用旧行号。')
    source_lines[name] = raw.decode('utf-8').splitlines()

seen = set()
for record in ledger['records']:
    name = Path(record['source']).name
    number = record['snapshot_line']
    if record['id'] in seen:
        raise SystemExit(f"重复条目：{record['id']}")
    seen.add(record['id'])
    if name not in source_lines or source_lines[name][number-1].strip() != record['text']:
        raise SystemExit(f"条目与原文不符：{record['id']}")
    if record['status'] not in {'待逐项核验', '已核验', '不适用'}:
        raise SystemExit(f"未知状态：{record['id']}")
    if record['status'] in {'已核验', '不适用'} and not record['evidence']:
        raise SystemExit(f"已处理条目缺少证据或说明：{record['id']}")

expected_ids = set()
for name, lines in source_lines.items():
    for number, line in enumerate(lines, 1):
        text = line.strip()
        if text.startswith('#') or not text or text in {r'\[', r'\]', '---'} or re.fullmatch(r'\|?[-:| ]+\|?', text):
            continue
        expected_ids.add(f'{name}:{number}')
if seen != expected_ids:
    raise SystemExit(f'清单覆盖不完整：缺少 {len(expected_ids-seen)} 条，多出 {len(seen-expected_ids)} 条。')

counts = Counter(row['status'] for row in ledger['records'])
print(f"核对 {len(seen)} 条原文记录：已核验 {counts['已核验']}，不适用 {counts['不适用']}，待逐项核验 {counts['待逐项核验']}。")
print('记录包含说明和证明；记录条数不等于独立公式数量。')
