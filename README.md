# 数学札记

静态数学博客，入口为 `index.html`。左侧按学科与知识主题展开，中间为正文，右侧为本文目录；手机端通过“打开目录”浏览。

## 学科与主题

- 初高中数学基础、高等数学、线性代数、概率统计、数学史。
- `topics/`：按原文档章节生成的主题页，保留定义、公式、定理与例子之间的联系。
- `reference.html`：公式与定理速查，链接到结论所在主题及小节。
- 目录支持主题名称搜索，当前主题自动展开并高亮。
- `assets/notebook.css`、`assets/notebook.js`：统一阅读布局与导航交互。

## 学习资料归档

- `docs/`：五份 Markdown 原稿，后续内容更新在这里进行。
- `archive/index.html`：资料目录；同目录的 HTML 为在线阅读版本。
- `downloads/math-study-documents.zip`：五份原稿和阅读说明的合集。
- `scripts/build_archive.py`：生成页面及压缩包，保留原有博客文章。

更新 Markdown 后重新生成：

```sh
python3 -m pip install -r scripts/requirements.txt
python3 scripts/build_site.py
```

`build_site.py` 先运行原稿归档生成器，再生成主题页、首页与速查页，并给既有文章加上统一目录。仅更新归档时也可单独运行 `build_archive.py`，但发布前应运行完整站点生成器。

生成结果直接纳入仓库，不依赖 GitHub Pages 构建时安装 Python 包。阅读页使用固定版本 MathJax 3.2.2 CDN 渲染 LaTeX；离线时公式源码仍可阅读。现有文章与归档 URL 保持可访问。

本地预览：

```sh
python3 -m http.server 8000
```

访问 `http://localhost:8000/`。所有站内路径均为相对路径，兼容 GitHub Pages 的 `/mathematics/` 子路径。
