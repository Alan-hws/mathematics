#!/usr/bin/env python3
"""Build the subject/topic navigation from the original study documents."""
from pathlib import Path
import re
import html
import os
from build_archive import ROOT, render, main as build_archive

SUBJECTS = [
 ('foundations','初高中数学基础','math-foundations-knowledge',range(2,14),'代数、函数、几何与大学数学的先修知识'),
 ('calculus','高等数学','advanced-mathematics-knowledge',range(2,16),'从极限与变化率，到积分、微分方程和级数'),
 ('linear','线性代数','linear-algebra-knowledge',range(2,15),'用向量、矩阵和空间理解线性关系'),
 ('probability','概率统计','probability-statistics-knowledge',range(2,18),'从随机现象到基于数据的估计与推断'),
]

def clean(s):
 return re.sub(r'【.*?】','',re.sub(r'^\d+(?:\.\d+)*[.、]?\s*','',s)).strip()

def headings(body):
 result=[]
 def add(m):
  tag,text=m.groups(); anchor=f'section-{len(result)+1}'
  label=html.unescape(re.sub('<[^>]+>','',text))
  result.append((tag,anchor,label))
  return f'<{tag} id="{anchor}">{text}</{tag}>'
 return re.sub(r'<(h[23])(?: [^>]*)?>(.*?)</\1>',add,body,flags=re.S),result

def collect():
 subjects=[]
 for key,title,slug,nums,desc in SUBJECTS:
  source=(ROOT/'docs'/f'{slug}.md').read_text()
  matches=list(re.finditer(r'^## (.+)$',source,re.M)); topics=[]
  for i,m in enumerate(matches):
   num=int(re.match(r'\d+',m[1])[0])
   if num not in nums: continue
   section=source[m.end():matches[i+1].start() if i+1<len(matches) else len(source)]
   if key=='foundations' and num in (11,12,13): continue
   body=render(section)
   for slug_name in ['math-study-schedule','math-foundations-knowledge','advanced-mathematics-knowledge','linear-algebra-knowledge','probability-statistics-knowledge']:
    body=body.replace(f'href="{slug_name}.html"', f'href="../archive/{slug_name}.html"')
   body,hs=headings(body.strip())
   topics.append(dict(title=clean(m[1]),path=f'topics/{key}-{num}.html',body=body,headings=hs))
  # Foundations already has a carefully curated formula/theorem handbook.
  if key=='foundations':
   start=source.index('## 15. '); end=source.index('## 16. ')
   formulas,hs=headings(render(source[start:end]))
   topics.append(dict(title='公式与定理速查',path='topics/foundations-formulas.html',body=formulas,headings=hs))
  subjects.append(dict(key=key,title=title,desc=desc,topics=topics,slug=slug))
 history=(ROOT/'posts/math-history.html').read_text()
 article=re.search(r'<article(?: [^>]*)?>(.*?)</article>',history,re.S)[1]
 matches=list(re.finditer(r'<h2(?: [^>]*)?>(.*?)</h2>',article,re.S)); topics=[]
 for i,m in enumerate(matches):
  body=article[m.end():matches[i+1].start() if i+1<len(matches) else len(article)]
  body=re.sub(r'<a class="back".*?</a>','',body,flags=re.S)
  body,hs=headings(body.strip())
  topics.append(dict(title=clean(m[1]),path=f'topics/history-{i+1}.html',body=body,headings=hs))
 subjects.append(dict(key='history',title='数学史',desc='从问题的起源理解概念与方法的发展',topics=topics,slug=None))
 return subjects

MATH=r'''<script>window.MathJax={tex:{inlineMath:[['\\(','\\)']],displayMath:[['\\[','\\]']]},options:{skipHtmlTags:['script','noscript','style','textarea','pre','code']}};</script><script defer src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-chtml.js"></script>'''

def layout(path,title,body,subjects,current=None,toc=None,breadcrumb='学习导航'):
 def url(p): return os.path.relpath(p,Path(path).parent).replace(os.sep,'/')
 nav=[]
 for s in subjects:
  active=any(t['path']==path for t in s['topics'])
  items=''.join(f'<a class="topic-link{" active" if t["path"]==path else ""}" {"aria-current=\"page\"" if t["path"]==path else ""} href="{url(t["path"])}">{html.escape(t["title"])}</a>' for t in s['topics'])
  nav.append(f'<details class="subject" {"open" if active else ""}><summary>{s["title"]}</summary><div class="topic-list">{items}</div></details>')
 toc_html=''.join(f'<a class="toc-{tag}" href="#{anchor}">{html.escape(label)}</a>' for tag,anchor,label in (toc or []))
 return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}｜数学札记</title><link rel="stylesheet" href="{url('assets/notebook.css')}">{MATH}<script defer src="{url('assets/notebook.js')}"></script></head><body>
 <a class="skip" href="#content">跳到正文</a><header class="mobile-bar"><a href="{url('index.html')}">数学札记</a><button id="menu-toggle" aria-expanded="false" aria-controls="sidebar">打开目录</button></header>
 <aside id="sidebar" class="sidebar"><a class="brand" href="{url('index.html')}"><span class="brand-mark">∑</span><span>数学札记<small>MATHEMATICS NOTES</small></span></a><p class="sidebar-caption">循着问题，理解数学。</p><label class="search-label" for="topic-search">查找主题</label><input id="topic-search" type="search" placeholder="搜索主题名称…" autocomplete="off"><nav aria-label="学科目录">{''.join(nav)}</nav><p id="search-empty" hidden>没有匹配的主题</p><nav class="utilities" aria-label="辅助入口"><a href="{url('reference.html')}">公式与定理速查</a><a href="{url('archive/math-study-schedule.html')}">学习计划</a><a href="{url('downloads/math-study-documents.zip')}" download>下载文档合集 ↗</a></nav></aside>
 <div class="workspace"><div class="breadcrumb">数学札记 <span>/</span> {html.escape(breadcrumb)}</div><div class="reading-layout"><main id="content" class="content"><article>{body}</article><footer>数学札记 · 理解概念，也记住结论成立的条件。</footer></main><aside class="toc" aria-label="本文目录"><div class="toc-label">本文目录</div>{toc_html or '<a href="#content">阅读正文</a>'}</aside></div></div></body></html>'''

def write(path,text):
 p=ROOT/path; p.parent.mkdir(parents=True,exist_ok=True); p.write_text("\n".join(line.rstrip() for line in text.splitlines()) + "\n")

def main():
 build_archive()
 subjects=collect()
 for s in subjects:
  for i,t in enumerate(s['topics']):
   links=[]
   if i: links.append(f'<a href="{Path(s["topics"][i-1]["path"]).name}">← {s["topics"][i-1]["title"]}</a>')
   if i+1<len(s['topics']): links.append(f'<a href="{Path(s["topics"][i+1]["path"]).name}">{s["topics"][i+1]["title"]} →</a>')
   source=f'<a href="../docs/{s["slug"]}.md" download>下载本学科完整笔记</a>' if s['slug'] else '<a href="../posts/math-history.html">阅读数学史原文</a>'
   body=f'<div class="eyebrow">{s["title"]}</div><h1>{t["title"]}</h1><p class="page-note">{source}</p>'+t['body']+'<nav class="page-turn" aria-label="相邻主题">'+''.join(links)+'</nav>'
   write(t['path'],layout(t['path'],t['title'],body,subjects,t,t['headings'],s['title']+' / '+t['title']))
 # Reading-first home with subject rows instead of duplicate archive/article grids.
 rows=[]
 for i,s in enumerate(subjects,1):
  examples=''.join(f'<a href="{t["path"]}">{t["title"]}</a>' for t in s['topics'][:3])
  rows.append(f'<section class="subject-row" id="{s["key"]}"><span class="row-number">0{i}</span><div><h2><a href="{s["topics"][0]["path"]}">{s["title"]}</a></h2><p>{s["desc"]}</p><div class="sample-topics">{examples}</div></div><span class="topic-count">{len(s["topics"])} 个主题</span></section>')
 body='<div class="eyebrow">学习导航</div><h1>把知识连成一条线。</h1><p class="lead">从基础到大学数学，按学科与主题逐步学习。定义、公式、定理与例子放在一起，方便理解，也方便回看。</p><div class="reading-note"><strong>从哪里开始？</strong><p>已完成初高中基础，可以从高等数学的“函数、数列与极限”开始；线性代数可并行学习，概率统计在掌握基础积分后推进。</p><a href="archive/math-study-schedule.html">查看完整学习计划 →</a></div><div class="subject-directory">'+''.join(rows)+'</div><section id="roadmap"><h2>阅读与复习</h2><p>左侧选择主题，右侧跳转本文小节。需要快速找结论时，使用<a href="reference.html">公式与定理速查</a>；完整原稿和练习仍保留在<a href="archive/index.html">文档归档</a>中。</p><p><a href="learning-roadmap.html">教材与课程路线 →</a></p></section>'
 home_toc=[('h2',s['key'],s['title']) for s in subjects]+[('h2','roadmap','阅读与复习')]
 write('index.html',layout('index.html','学习导航',body,subjects,toc=home_toc))
 # One index of named formula/theorem headings; links lead to the full context.
 chunks=[]; refs=[]
 for s in subjects[:-1]:
  items=[]
  for t in s['topics']:
   matches=[(a,label) for _,a,label in t['headings'] if re.search('公式|定理|法则|判别|判定|恒等|求导|积分表|等价条件|期望|协方差',label)]
   if matches:
    items.extend(f'<li><a href="{t["path"]}#{a}">{html.escape(clean(label))}</a><span>{t["title"]}</span></li>' for a,label in matches)
   elif s['key']!='foundations':
    items.append(f'<li><a href="{t["path"]}">{t["title"]}</a><span>定义、公式与适用条件</span></li>')
  chunks.append(f'<section id="{s["key"]}"><h2>{s["title"]}</h2><ul class="reference-list">'+''.join(items)+'</ul></section>')
  refs.append(('h2',s['key'],s['title']))
 body='<div class="eyebrow">复习工具</div><h1>公式与定理速查</h1><p class="lead">按学科查找结论。每个入口回到对应主题，连同定义、使用条件与解释一起阅读。</p>'+''.join(chunks)
 write('reference.html',layout('reference.html','公式与定理速查',body,subjects,toc=refs,breadcrumb='公式与定理速查'))
 # All existing URLs continue to work, now within the same notebook shell.
 paths=list((ROOT/'archive').glob('*.html'))+list((ROOT/'posts').glob('*.html'))+[ROOT/'learning-roadmap.html']
 for p in paths:
  raw=p.read_text(); match=re.search(r'<main[^>]*>(.*?)</main>',raw,re.S)
  if not match: continue
  body=match[1]
  body=re.sub(r'<footer.*?</footer>','',body,flags=re.S)
  body=re.sub(r'</?article\b[^>]*>','',body)
  body=re.sub(r'<a class="back".*?</a>','',body,flags=re.S)
  body,hs=headings(body.strip())
  title=html.unescape(re.search(r'<title>(.*?)</title>',raw,re.S)[1].split('｜')[0])
  path=p.relative_to(ROOT).as_posix()
  write(path,layout(path,title,body,subjects,toc=hs,breadcrumb=title))
 print('Built',sum(len(s['topics']) for s in subjects),'topic pages and shared navigation.')

if __name__=='__main__': main()
