# 数学札记

静态数学博客，入口为 `index.html`。

## 学习资料归档

- `docs/`：五份 Markdown 原稿，后续内容更新在这里进行。
- `archive/index.html`：资料目录；同目录的 HTML 为在线阅读版本。
- `downloads/math-study-documents.zip`：五份原稿和阅读说明的合集。
- `scripts/build_archive.py`：生成页面及压缩包，保留原有博客文章。

更新 Markdown 后重新生成：

```sh
python3 -m pip install -r scripts/requirements.txt
python3 scripts/build_archive.py
```

生成结果直接纳入仓库，不依赖 GitHub Pages 构建时安装 Python 包。阅读页使用固定版本 MathJax 3.2.2 CDN 渲染 LaTeX；离线时公式源码仍可阅读。

本地预览：

```sh
python3 -m http.server 8000
```

访问 `http://localhost:8000/`。所有站内路径均为相对路径，兼容 GitHub Pages 的 `/mathematics/` 子路径。
