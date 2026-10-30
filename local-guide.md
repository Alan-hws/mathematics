# 数学札记

这是一个独立的本地静态数学博客，不依赖构建工具和第三方框架。

## 查看

直接用浏览器打开 `index.html`。

## 目录结构

```text
mathematics/
  index.html                 # 博客首页
  README.md                  # 说明
  assets/styles.css          # 公共样式
  posts/
    limits.html              # 极限
    derivatives.html         # 导数与中值定理
    linear-algebra.html      # 向量空间与矩阵
    probability.html         # 贝叶斯公式
    math-history.html        # 数学史
```

## 新增文章

复制 `posts/` 中任意文章作为模板，修改标题、分类、正文和导航链接，然后在首页 `index.html` 的“文章”区域增加一张卡片。

每篇文章建议保持以下结构：

1. 直觉或问题背景
2. 定义与公式
3. 定理与条件
4. 例子或推导
5. 数学史
6. 记忆卡片

## 学科目录改版

首页使用左侧学科与主题目录。主题页位于 `topics/`，公式定理速查位于 `reference.html`。

更新 `docs/` 原稿后，先安装 `scripts/requirements.txt` 中的依赖，再运行 `python3 scripts/build_site.py` 重新生成完整站点。生成的 HTML 可直接静态托管；在线公式渲染需要加载 MathJax。原文章路径仍然可访问。
