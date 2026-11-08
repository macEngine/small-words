# 外刊小词 small-words

从公开演讲里学单词。每个词一页：释义、原句出处、官方视频时间戳。

- 站点：https://macengine.github.io/small-words/
- 生成器：[Hugo](https://gohugo.io/)，自写主题（`layouts/` + `assets/`，纯 CSS，样式参考 [笨狗又一窝](https://whusnoopy.github.io/blog/)）
- 部署：push 到 `main` → GitHub Actions 构建 → GitHub Pages

## 目录

```
content/words/<word>.md          # 每词一页
content/sources/<source>.md      # 每个来源（文章/演讲）一页，自动列出收录的词
scripts/import_words.py          # 从 words 仓库的文章目录批量导入
layouts/                         # 模板（两栏 + 侧栏归档/演讲/标签）
assets/css/main.css  assets/js/site.js
layouts/shortcodes/speech-words.html
layouts/shortcodes/todo.html
```

## 导入一篇文章的词

words 仓库里每篇文章是一个目录 `YYMMDD_<标题>/`，里面每词一个 `每日一词：<word>.md`（和公众号 gzh 用同一份 Markdown）：

```bash
python3 scripts/import_words.py "/path/to/260624_How the Iran Deal ..."        # 默认每词独立一篇
```

脚本只去掉公众号补图占位 `![]()`，把等级标签转成 tags，并从「解析」里抽一句中文释义作 gloss（抽不到就手动补）。

## 本地预览

```bash
git clone git@github.com:macEngine/small-words.git
cd small-words
hugo server
```

## 版权

本站只引用演讲原句、链接官方视频，不托管视频或整篇文稿。视频与文稿版权归原发布方。
