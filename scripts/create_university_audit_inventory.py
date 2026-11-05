"""Freeze a line-by-line audit inventory without claiming automatic proof.

The ledger includes every substantive line, including explanations and proof
lines, so formulae in prose are not silently omitted. A line may contain more
than one mathematical claim: each claim must be checked before marking it done.
Run only when starting a fresh inventory; never overwrite human audit results.
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'docs' / '大学数学逐条核验清单.json'
FILES = {
    '高等数学': 'advanced-mathematics-knowledge.md',
    '线性代数': 'linear-algebra-knowledge.md',
    '概率统计': 'probability-statistics-knowledge.md',
}

if OUTPUT.exists():
    raise SystemExit('清单已存在，拒绝覆盖人工核验结果。')

records = []
snapshots = {}
for subject, name in FILES.items():
    path = ROOT / 'docs' / name
    raw = path.read_bytes()
    snapshots[name] = hashlib.sha256(raw).hexdigest()
    section = ''
    before_solutions = False
    for line_number, line in enumerate(raw.decode('utf-8').splitlines(), 1):
        text = line.strip()
        if text.startswith('#'):
            section = text.lstrip('#').strip()
            before_solutions = section in {'16. 练习与参考答案', '19. 练习与参考答案'}
            continue
        if not text or text in {r'\[', r'\]', '---'} or re.fullmatch(r'\|?[-:| ]+\|?', text):
            continue
        # Each numbered question is recorded only if its derivation and
        # independent numerical/symbolic check already exist in the document.
        if text == '逐题推导与检验：':
            before_solutions = False
        question = re.match(r'^(\d+)\.\s', text)
        verified = bool(before_solutions and question and (
            (subject == '线性代数' and section == '16. 练习与参考答案' and int(question[1]) <= 4)
            or (subject == '概率统计' and section == '19. 练习与参考答案' and int(question[1]) <= 6)
        ))
        nonclaim = text.startswith('![') or text in {r'\begin{aligned}', r'\end{aligned}'}
        records.append({
            'id': f'{name}:{line_number}',
            'subject': subject,
            'source': f'docs/{name}',
            'snapshot_line': line_number,
            'section': section,
            'text': text,
            'status': '不适用' if nonclaim else ('已核验' if verified else '待逐项核验'),
            'evidence': '图片或公式排版标记，不是数学断言。' if nonclaim else ('原文“逐题推导与检验”；scripts/check_university_audit.py' if verified else ''),
        })

ledger = {
    'description': '工作区三个大学数学文档的冻结清单，按非空原文行登记；一行可能含多个断言，必须全部核验后才能标记完成。说明文字和既有证明也收录，不代表每行都是未证明公式。',
    'scope_note': '这是创建时的工作区快照，不是自动识别出的全部独立公式；之后原文行号可能变化，应以内容和文件哈希复核。',
    'source_sha256': snapshots,
    'records': records,
}
OUTPUT.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
done = sum(item['status'] == '已核验' for item in records)
print(f'已冻结 {len(records)} 条原文记录，其中 {done} 条编号习题已有单独证明和复算。')
