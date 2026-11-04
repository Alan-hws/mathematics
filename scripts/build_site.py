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

def render_catalog(source, topic_headings=None):
 """Render book/chapter hierarchy from the verified catalog while preserving each line."""
 parts=[]; toc=[]; chapter_open=False; book=''; chapter=0
 destinations={
  '必修第一册':[5,8,5,5,6], '必修第二册':[7,10,7,9,9],
  '选择性必修第一册':[7,7,7], '选择性必修第二册':[8,10],
  '选择性必修第三册':[9,9,9],
  '七年级上册':[2,2,2,4],
  '七年级下册':[4,2,3,2,2,4],
  '八年级上册':[4,4,4,2,2],
  '八年级下册':[2,4,4,3,4],
  '九年级上册':[2,3,4,4,4],
  '九年级下册':[3,4,4,4],
 }
 offsets={'必修第一册':1,'必修第二册':6,'选择性必修第一册':1,'选择性必修第二册':4,'选择性必修第三册':6}
 # Each chapter links to its subject; add a subsection anchor only when a
 # curated, exact topic heading is available. Never guess from keywords.
 anchors={
  '七年级上册': {'1.1':'正负数、有理数与数轴','1.2':'正负数、有理数与数轴','1.3':'有理数的大小比较、加减乘除','1.4':'有理数的大小比较、加减乘除','1.5':'幂运算和科学记数法','2.1':'整式的系数、次数与代数式求值','2.2':'整式与因式分解','3.1':'一元一次方程的概念和等式性质','3.2':'一元一次方程：去括号、去分母与检验','3.3':'一元一次方程：去括号、去分母与检验','3.4':'一元一次方程与不等式','4.1':'立体图形、展开图与截面','4.2':'线段、射线、直线及中点','4.3':'角的比较、角平分线及余补角','4.4':'课题学习：设计长方体包装纸盒'},
  '七年级下册': {'5.1':'直线、角与平行线的判定','5.2':'直线、角与平行线的判定','5.3':'平行线、三角形内角和与外角','5.4':'平移、轴对称与最短路径','6.1':'平方根与算术平方根','6.2':'平方根与算术平方根','6.3':'实数、估算与数轴','7.1':'坐标与函数图像','7.2':'用坐标描述地理位置','8.1':'方程组的代入消元、加减消元与三元消元','8.2':'方程组的代入消元、加减消元与三元消元','8.3':'用方程组处理实际问题','8.4':'方程组的代入消元、加减消元与三元消元','9.1':'不等式解集与一元一次不等式组','9.2':'不等式解集与一元一次不等式组','9.3':'不等式解集与一元一次不等式组','10.1':'统计调查：总体、样本与频数','10.2':'直方图：分组、计数与读图','10.3':'课题学习：收集数据研究节水'},
  '八年级上册': {'11.1':'三角形的中线、高和角平分线','11.2':'平行线、三角形内角和与外角','11.3':'三角形边长与多边形的内外角','12.1':'全等三角形、角平分线与轴对称','12.2':'全等判定：对应与夹角','12.3':'全等三角形、角平分线与轴对称','13.1':'线段垂直平分线的性质与逆命题','13.2':'轴对称作图：先找对应点','13.3':'三角形稳定性与等边三角形','13.4':'平移、轴对称与最短路径','14.1':'整式乘法与分式四则运算','14.2':'整式与因式分解','14.3':'提公因式与公式法分解','15.1':'分式运算与增根','15.2':'整式乘法与分式四则运算','15.3':'分式运算与增根'},
  '八年级下册': {'16.1':'二次根式：定义条件、运算与面积测量','16.2':'二次根式：定义条件、运算与面积测量','16.3':'二次根式：定义条件、运算与面积测量','17.1':'勾股定理及逆定理','17.2':'勾股定理及逆定理','18.1':'平行四边形及特殊四边形的判定','18.2':'特殊平行四边形的性质与判定','19.1':'坐标与函数观念','19.2':'正比例与一次函数：画图、比较和建模','19.3':'正比例与一次函数：画图、比较和建模','20.1':'中位数、众数与随机事件','20.2':'统计：平均数、方差与体质数据','20.3':'统计：平均数、方差与体质数据'},
  '九年级上册': {'21.1':'一元二次方程：配方、因式分解与模型检验','21.2':'直接开平方法与公式法','21.3':'一元二次方程：配方、因式分解与模型检验','22.1':'二次函数的平移与开口','22.2':'二次函数的图像与方程的根','22.3':'反比例与二次函数：变化率和最值','23.1':'旋转与中心对称的坐标','23.2':'旋转与中心对称的坐标','23.3':'课题学习：利用图形变换设计图案','24.1':'圆的性质与切线','24.2':'点和圆的位置关系','24.3':'正多边形的边心距与面积','24.4':'多边形、圆和锐角三角函数','25.1':'中位数、众数与随机事件','25.2':'列表法与树状图：不要遗漏样本点','25.3':'描述统计与初步概率'},
  '九年级下册': {'26.1':'反比例函数','26.2':'函数的表示、坐标平移与实际模型','27.1':'比例线段与相似三角形','27.2':'相似判定与比例应用','27.3':'位似、投影与三视图','28.1':'特殊角的三角函数值','28.2':'解直角三角形：已知一边和一个锐角','29.1':'位似、投影与三视图','29.2':'三视图：对应的长、宽和高','29.3':'课题学习：根据三视图制作立体模型'},
  '必修第一册': {'1.1':'集合与逻辑','1.2':'集合与逻辑','1.3':'集合运算的计数关系与逻辑命题','1.4':'集合与命题：条件与反例','1.5':'集合运算的计数关系与逻辑命题','2.1':'不等式与最值','2.2':'算术—几何平均不等式与最值','2.3':'二次函数、方程和不等式的统一','3.1':'函数的完整框架','3.2':'定义域、奇偶性与单调性','3.3':'幂函数与指数函数的区分','3.4':'函数的完整框架','4.1':'幂、指数、对数','4.2':'指数、对数和函数模型','4.3':'指数、对数和函数模型','4.4':'对数定义域与不等式','4.5':'连续函数零点与二分法','5.1':'弧度与单位圆','5.2':'弧度与单位圆','5.3':'任意角、诱导公式和正切','5.4':'定义、弧度与图像','5.5':'和差、倍角公式与证明思路','5.6':'三角函数图像变换和应用建模','5.7':'三角函数图像变换和应用建模'},
  '必修第二册': {'6.1':'平面与空间向量','6.2':'平面与空间向量','6.3':'平面与空间向量','6.4':'向量的夹角、垂直与投影','7.1':'复数的代数与几何意义','7.2':'复数除法的共轭方法','7.3':'复数的代数与几何意义','8.1':'立体几何初步：体积、平行与垂直','8.2':'立体几何初步：体积、平行与垂直','8.3':'柱、锥、台与球的测量','8.4':'立体几何初步：体积、平行与垂直','8.5':'立体几何初步：体积、平行与垂直','8.6':'立体几何初步：体积、平行与垂直','9.1':'分位数与分层随机抽样','9.2':'随机变量与统计','9.3':'随机变量与统计','10.1':'概率','10.2':'条件概率与独立性的区别','10.3':'概率'},
  '选择性必修第一册': {'1.1':'空间位置关系与非共面基','1.2':'空间位置关系与非共面基','1.3':'空间位置关系与非共面基','1.4':'空间向量与直线、平面的位置关系','2.1':'直线与圆','2.2':'直线与圆的解析几何','2.3':'直线与圆','2.4':'直线与圆的解析几何','2.5':'直线与圆：距离判定和求交','3.1':'椭圆、双曲线与抛物线：定义和参数','3.2':'椭圆、双曲线与抛物线：定义和参数','3.3':'椭圆、双曲线与抛物线：定义和参数'},
  '选择性必修第二册': {'4.1':'数列与求和','4.2':'数列、递推和数学归纳法','4.3':'数列、递推和数学归纳法','4.4':'数列、递推和数学归纳法','5.1':'导数初步','5.2':'导数初步','5.3':'用导数判断单调性和闭区间最值'},
  '选择性必修第三册': {'6.1':'计数原理、排列组合与杨辉三角','6.2':'计数原理、排列组合与杨辉三角','6.3':'二项式定理为什么有组合数','7.1':'全概率、贝叶斯与概率树','7.2':'随机变量与统计','7.3':'随机变量与统计','7.4':'二项分布的期望和方差','7.5':'正态分布与标准化','8.1':'样本相关系数与最小二乘的条件','8.2':'成对数据与一元线性回归','8.3':'列联表与独立性检验入门'},
 }
 specific_anchors={
  '七年级下册': {'6.2':'有理数运算、代数式与立方根','7.1':'象限、坐标轴与平移'},
  '八年级下册': {'20.1':'加权平均数、中位数和众数'},
  '九年级上册': {'24.2':'点和圆、直线和圆的位置关系','24.4':'正多边形的边心距与面积','25.3':'频率估计概率：试验次数与模型'},
  '九年级下册': {'26.1':'反比例与二次函数：变化率和最值','26.2':'反比例与二次函数：变化率和最值','27.1':'相似与位似：对应关系和面积'},
  '必修第一册': {'3.1.1':'定义域、奇偶性与单调性','3.1.2':'函数的完整框架','3.2.1':'定义域、奇偶性与单调性','3.2.2':'定义域、奇偶性与单调性','4.5.1':'连续函数零点与二分法','4.5.2':'连续函数零点与二分法','4.5.3':'指数、对数和函数模型','5.1.2':'弧度与单位圆','5.5.1':'和差、倍角公式与证明思路'},
  '必修第二册': {'6.3.1':'平面向量基本定理与坐标运算','6.3.2':'平面向量基本定理与坐标运算','6.3.3':'平面向量基本定理与坐标运算','6.3.4':'平面向量基本定理与坐标运算','6.3.5':'向量的夹角、垂直与投影','6.4.2':'向量在力和位移中的应用','6.4.3':'三角形面积与余弦定理','7.2.2':'复数除法的共轭方法','8.2':'几何体直观图：斜二测的基本约定','8.3.1':'柱、锥、台与球的测量','8.3.2':'圆柱、圆锥和圆台的侧面积','9.2.1':'样本估计总体与随机模拟','9.2.2':'分位数与分层随机抽样','9.2.3':'样本估计总体与随机模拟','9.2.4':'样本估计总体与随机模拟','10.3.1':'样本估计总体与随机模拟','10.3.2':'样本估计总体与随机模拟'},
  '选择性必修第一册': {'1.1.1':'空间位置关系与非共面基','1.1.2':'空间位置关系与非共面基','1.3.1':'空间位置关系与非共面基','1.3.2':'空间位置关系与非共面基','2.1.2':'直线一般式与平行、垂直','2.3.3':'点到直线的距离：法向投影','2.3.4':'直线一般式与平行、垂直'},
  '选择性必修第二册': {'5.1.1':'从变化率到导数及基本法则','5.1.2':'从变化率到导数及基本法则','5.2.2':'从变化率到导数及基本法则','5.2.3':'从变化率到导数及基本法则'},
  '选择性必修第三册': {'7.1.1':'条件概率与独立性的区别','7.1.2':'全概率、贝叶斯与概率树','7.3.1':'分布列、期望与方差：有限例子','7.3.2':'分布列、期望与方差：有限例子','7.4.1':'二项分布的期望和方差','7.4.2':'超几何分布：不放回抽样','8.1.2':'样本相关系数与最小二乘的条件','8.2.2':'成对数据与一元线性回归'},
 }
 specific_anchors['必修第一册'].update({'2.1':'等式与不等式的性质','4.1.1':'方根与分数指数幂','4.1.2':'指数、对数和函数模型','4.4.1':'指数、对数和函数模型','4.4.2':'指数、对数和函数模型','4.4.3':'指数、对数和函数模型','5.4.3':'任意角、诱导公式和正切'})
 specific_anchors['必修第一册'].update({'3.1.2':'定义域、奇偶性与单调性','3.4':'定义域、奇偶性与单调性','5.4.1':'正弦、余弦函数的图像与性质','5.4.2':'正弦、余弦函数的图像与性质','5.6.1':'三角函数图像变换和应用建模'})
 specific_anchors['选择性必修第三册']['6.3.2']='二项式系数的性质'
 specific_anchors['选择性必修第三册']['7.2']='分布列、期望与方差：有限例子'
 specific_anchors['必修第二册'].update({
  '6.1':'向量的几何运算',
  '6.2.1':'向量的几何运算',
  '6.2.2':'向量的几何运算',
  '6.2.3':'向量的几何运算',
  '6.4.1':'用向量证明三角形中位线定理',
  '8.1':'棱柱、棱锥、棱台与旋转体',
  '8.5':'空间平行、垂直的常用判定与性质',
  '8.5.2':'立体几何初步：体积、平行与垂直',
  '8.5.3':'空间平行、垂直的常用判定与性质',
  '8.6':'空间平行、垂直的常用判定与性质',
  '8.6.2':'立体几何初步：体积、平行与垂直',
  '8.6.3':'空间平行、垂直的常用判定与性质',
  '9.1.1':'样本估计总体与随机模拟',
  '9.1.3':'获取数据与统计调查案例',
  '9.2.3':'估计总体的集中趋势与离散程度',
  '9.2.4':'估计总体的集中趋势与离散程度',
  '9.3':'获取数据与统计调查案例',
  '10.1.1':'有限样本空间与事件运算',
  '10.1.2':'有限样本空间与事件运算',
  '10.1.3':'有限样本空间与事件运算',
  '10.3':'频率与概率的关系',
 })
 specific_anchors['选择性必修第一册'].update({'1.4.2':'空间距离与线面角','2.1.1':'直线的点斜式、两点式与一般式','2.2.1':'直线的点斜式、两点式与一般式','2.2.2':'直线的点斜式、两点式与一般式','2.2.3':'直线的点斜式、两点式与一般式','2.3.1':'直线的点斜式、两点式与一般式','2.5.2':'两圆的位置关系与交点'})
 for line in source.splitlines():
  line=line.strip()
  if not line: continue
  if line.startswith('数据源：'):
   parts.append('<p class="catalog-intro">按教材查找知识点。展开章节查看小节，点击“阅读相关知识”进入讲解。</p>');continue
  if line.startswith('### '):
   if chapter_open: parts.append('</div></details>');chapter_open=False
   book=line[4:];anchor='book-'+str(len(toc)+1);toc.append(('h2',anchor,book))
   parts.append(f'<h2 id="{anchor}" class="catalog-book">{html.escape(book)}</h2>');chapter=0;continue
  if re.match(r'^第[一二三四五六七八九十]+章',line):
   if chapter_open:parts.append('</div></details>')
   chapter+=1
   target=destinations[book][chapter-1]
   parts.append(f'<details class="catalog-chapter"><summary>{html.escape(line)}<span>展开小节</span></summary><div class="catalog-entries"><p class="catalog-action"><a href="foundations-{target}.html">阅读相关知识 →</a></p>')
   chapter_open=True;continue
  if not chapter_open:continue
  entry=line.removeprefix('- ').strip()
  if entry in ('小结','习题课') or entry.startswith(('复习参考题','函数的基本性质习题课','平面向量习题课','向量线性运算习题课')):continue
  m=re.match(r'^(\*?\d+\.\d+(?:\.\d+)?\*?)\s*(.*)',entry)
  if m:
   code,name=m.groups();depth=' catalog-subsection' if code.count('.')==2 else ''
   parent='.'.join(code.strip('*').split('.')[:2])
   wanted=specific_anchors.get(book,{}).get(code.strip('*')) or anchors.get(book,{}).get(parent)
   match=next((anchor for _,anchor,label in (topic_headings or {}).get(target,[]) if wanted and wanted in label),None)
   label=html.escape(name)
   if match:
    label=f'<a href="foundations-{target}.html#{match}">{label}</a>'
   parts.append(f'<div class="catalog-entry{depth}"><span class="catalog-code">{html.escape(code)}</span><span>{label}</span></div>')
  else:
   parts.append(f'<div class="catalog-extra">{html.escape(entry)}</div>')
 if chapter_open:parts.append('</div></details>')
 return ''.join(parts),toc

def collect():
 subjects=[]
 for key,title,slug,nums,desc in SUBJECTS:
  source=('\n\n'.join((ROOT/'docs/foundations'/f'{n}.md').read_text() for n in range(1,17)) if key=='foundations' else (ROOT/'docs'/f'{slug}.md').read_text())
  matches=list(re.finditer(r'^## (.+)$',source,re.M)); topics=[]
  for i,m in enumerate(matches):
   num=int(re.match(r'\d+',m[1])[0])
   if num not in nums: continue
   section=source[m.end():matches[i+1].start() if i+1<len(matches) else len(source)]
   if key=='foundations' and num in (12,13): continue
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
 # Junior-school textbook catalog shares the same chapter navigation.
 junior=(ROOT/'docs/junior-textbook-catalog.md').read_text(encoding='utf-8')
 foundation_headings={int(re.search(r'foundations-(\d+)',t['path']).group(1)):t['headings'] for t in subjects[0]['topics'] if re.search(r'foundations-(\d+)',t['path'])}
 junior_body,junior_headings=render_catalog(junior, foundation_headings)
 subjects[0]['topics'].append(dict(title='初中人教版教材目录',path='topics/junior-textbook-catalog.html',body=junior_body,headings=junior_headings))
 # The high-school textbook catalog is a separate, complete index sourced from the A-edition TOCs.
 catalog=(ROOT/'docs/high-school-textbook-catalog.md').read_text(encoding='utf-8')
 catalog= re.sub(r'^## .+\n', '', catalog, count=1, flags=re.M).strip()
 catalog_body,catalog_headings=render_catalog(catalog, foundation_headings)
 subjects[0]['topics'].append(dict(title='高中人教 A 版教材目录',path='topics/high-school-textbook-catalog.html',body=catalog_body,headings=catalog_headings))
 history=(ROOT/'posts/math-history.html').read_text()
 article=re.search(r'<article(?: [^>]*)?>(.*?)</article>',history,re.S)[1]
 matches=list(re.finditer(r'<h2(?: [^>]*)?>(.*?)</h2>',article,re.S)); topics=[]
 for i,m in enumerate(matches):
  body=article[m.end():matches[i+1].start() if i+1<len(matches) else len(article)]
  body=re.sub(r'<a class="back".*?</a>','',body,flags=re.S)
  body,hs=headings(body.strip())
  topics.append(dict(title=clean(m[1]),path=f'topics/history-{i+1}.html',body=body,headings=hs))
 timeline=(ROOT/'docs/mathematics-history-timeline.md').read_text(encoding='utf-8')
 timeline=timeline.split('\n',1)[1].lstrip()
 timeline_body,timeline_headings=headings(render(timeline))
 topics.insert(0,dict(title='数学发展时间轴',path='topics/history-timeline.html',body=timeline_body,headings=timeline_headings))
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
   source=('<a href="../downloads/math-study-documents.zip" download>下载按主题整理的原稿</a>' if s['key']=='foundations' else f'<a href="../docs/{s["slug"]}.md" download>下载本学科完整笔记</a>' if s['slug'] else ('<a href="../docs/mathematics-history-timeline.md" download>下载时间轴原稿</a>' if t['path']=='topics/history-timeline.html' else '<a href="../posts/math-history.html">阅读数学史原文</a>'))
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
