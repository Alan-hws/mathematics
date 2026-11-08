"""Rebase insertions; invalidate earlier reviews whenever source context changes.

Supply the Git revision whose file hashes match the ledger. This deliberately
refuses changed/deleted substantive lines; those require human review, not an
automatic carry-forward of an earlier audit status.
"""
import difflib
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
ledger_path = root / 'docs' / '大学数学逐条核验清单.json'
if len(sys.argv) != 2:
    raise SystemExit('用法：python3 scripts/refresh_university_audit_inventory.py <旧快照的 Git 版本>')
revision = sys.argv[1]
ledger = json.loads(ledger_path.read_text(encoding='utf-8'))


def substantive(text):
    return bool(text and not text.startswith('#') and text not in {r'\[', r'\]', '---'}
                and not re.fullmatch(r'\|?[-:| ]+\|?', text))


all_records = []
new_count = 0
invalidated_count = 0
for name, expected_hash in ledger['source_sha256'].items():
    old = subprocess.check_output(['git', 'show', f'{revision}:docs/{name}'], cwd=root)
    if hashlib.sha256(old).hexdigest() != expected_hash:
        raise SystemExit(f'{name}: 指定 Git 版本与台账快照不一致，拒绝迁移。')
    raw = (root / 'docs' / name).read_bytes()
    context_changed = raw != old
    old_lines = old.decode('utf-8').splitlines()
    new_lines = raw.decode('utf-8').splitlines()
    old_records = {r['snapshot_line']: r for r in ledger['records'] if r['source'] == f'docs/{name}'}
    mapped = {}
    for tag, a, b, c, d in difflib.SequenceMatcher(a=old_lines, b=new_lines, autojunk=False).get_opcodes():
        if tag == 'equal':
            for offset in range(b-a):
                if a+offset+1 in old_records:
                    mapped[c+offset+1] = old_records[a+offset+1].copy()
        elif tag in {'delete', 'replace'} and any(i in old_records for i in range(a+1, b+1)):
            raise SystemExit(f'{name}: 旧行 {a+1}–{b} 包含修改或删除，请人工核验后迁移。')
    subject = next(r['subject'] for r in ledger['records'] if r['source'] == f'docs/{name}')
    section = ''
    for number, line in enumerate(new_lines, 1):
        text = line.strip()
        if text.startswith('#'):
            section = text.lstrip('#').strip()
            continue
        if not substantive(text):
            continue
        record = mapped.get(number)
        if record is None:
            record = {'subject': subject, 'source': f'docs/{name}', 'text': text,
                      'status': '待逐项核验', 'evidence': ''}
            new_count += 1
        elif context_changed:
            record['previous_review'] = {'status': record['status'], 'evidence': record['evidence']}
            record['status'] = '待逐项核验'
            record['evidence'] = ''
            invalidated_count += 1
        record.update(id=f'{name}:{number}', snapshot_line=number, section=section)
        all_records.append(record)
    ledger['source_sha256'][name] = hashlib.sha256(raw).hexdigest()

ledger['records'] = all_records
ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(f'新增 {new_count} 条待核验；因全文上下文变化撤销 {invalidated_count} 条旧状态。旧依据仅作历史记录，不代表当前版本已核验。')
