#!/usr/bin/env python3
"""Render the archived Markdown with tables and preserve TeX for MathJax."""
from pathlib import Path
import html
import re
from zipfile import ZipFile, ZIP_DEFLATED, ZipInfo

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = [
    ("math-study-schedule", "数学系统学习计划", "64 周学习路线、每日安排、配套课程与阶段验收。"),
    ("math-foundations-knowledge", "初高中数学知识点", "代数、函数、几何、公式定理及自测题。"),
    ("advanced-mathematics-knowledge", "大学高等数学", "极限、微积分、多元函数、微分方程与级数。"),
    ("linear-algebra-knowledge", "线性代数", "向量、矩阵、投影、特征值、SVD 与 PCA。"),
    ("probability-statistics-knowledge", "概率论与数理统计", "分布、数字特征、统计推断、回归与贝叶斯。"),
]
PAGES = {slug + ".md": slug + ".html" for slug, _, _ in DOCUMENTS}
MD = MarkdownIt("commonmark", {"html": False}).enable("table")


def render(source):
    # Protect fenced code as well, so example Markdown remains literal text.
    tokens = []

    def protect(match):
        raw = match.group(0)
        marker = f"ARCHIVEMATHTOKEN{len(tokens)}END"
        if raw.startswith("```"):
            tokens.append(raw)
        else:
            tokens.append(html.escape(raw))
        return marker

    pattern = r"```[^\n]*\n[\s\S]*?```|\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)"
    protected = re.sub(pattern, protect, source)
    # Code must reach the parser as code; math must bypass Markdown escaping.
    for i, token in enumerate(tokens):
        if token.startswith("```"):
            protected = protected.replace(f"ARCHIVEMATHTOKEN{i}END", token)
    body = MD.render(protected)
    for i, token in enumerate(tokens):
        if not token.startswith("```"):
            body = body.replace(f"ARCHIVEMATHTOKEN{i}END", token)
    for old, new in PAGES.items():
        body = body.replace(f'href="{old}"', f'href="{new}"')
    return body


def page(title, content, math=False):
    math_scripts = r'''<script>
window.MathJax = {
  tex: {inlineMath: [['\\(', '\\)']], displayMath: [['\\[', '\\]']]},
  options: {skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']}
};
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-chtml.js"></script>''' if math else ""
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}｜数学札记</title>
  <link rel="stylesheet" href="../assets/styles.css">
  <link rel="stylesheet" href="../assets/archive.css">
  {math_scripts}
</head>
<body>
  <header class="site-header"><div class="header-inner"><div class="kicker">Study Archive</div><h1>{html.escape(title)}</h1><p>从初高中基础到大学数学与机器学习的学习资料。</p></div></header>
  <nav class="top-nav"><div class="nav-inner"><a href="../index.html">博客首页</a><a href="index.html">学习资料归档</a><a href="../downloads/math-study-documents.zip" download>下载 Markdown 合集</a></div></nav>
  <main><article class="article archive-article">{content}</article></main>
  <footer class="site-footer">数学札记 · 学习资料归档</footer>
</body>
</html>
'''


def main():
    out = ROOT / "archive"
    out.mkdir(exist_ok=True)
    download = ROOT / "downloads"
    download.mkdir(exist_ok=True)
    cards = []
    with ZipFile(download / "math-study-documents.zip", "w", ZIP_DEFLATED) as bundle:
        def add_file(name, data):
            entry = ZipInfo("math-study-documents/" + name, (2026, 10, 29, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            bundle.writestr(entry, data)

        for slug, title, description in DOCUMENTS:
            source = ROOT / "docs" / (slug + ".md")
            body = '<p><a href="../docs/' + slug + '.md" download>下载此文 Markdown 原稿</a></p>'
            body += render(source.read_text(encoding="utf-8"))
            (out / (slug + ".html")).write_text(page(title, body, math=True), encoding="utf-8")
            add_file(source.name, source.read_bytes())
            cards.append(f'<article class="index-card"><h2><a href="{slug}.html">{title}</a></h2><p>{description}</p></article>')
        readme = "# 数学学习文档合集\n\n" + "\n".join(f"{i}. {title}：{slug}.md" for i, (slug, title, _) in enumerate(DOCUMENTS, 1))
        add_file("README.md", readme + "\n\n部分公式采用 LaTeX，请使用支持数学公式的 Markdown 阅读器。\n")
    intro = '<h1>数学学习资料归档</h1><p>按学习顺序整理的五份资料，包含知识点、公式定理、适用条件和自测题。点击标题在线阅读，也可下载原稿。</p><p>公式由 MathJax 渲染，首次访问需要联网加载；离线时仍保留公式源码。</p>'
    (out / "index.html").write_text(page("学习资料归档", intro + '<div class="archive-grid">' + "".join(cards) + '</div>'), encoding="utf-8")


if __name__ == "__main__":
    main()
