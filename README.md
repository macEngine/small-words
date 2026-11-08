# 小词 small-words

从公开演讲里学单词。每个词一页：释义、原句出处、官方视频时间戳。

- 站点：https://macengine.github.io/small-words/
- 生成器：[Hugo](https://gohugo.io/) + [PaperMod](https://github.com/adityatelange/hugo-PaperMod) 主题
- 部署：push 到 `main` → GitHub Actions 构建 → GitHub Pages

## 目录

```
content/words/<word>.md          # 每词一页
content/speeches/<speech>.md     # 每篇演讲一页，自动列出收录的词
layouts/shortcodes/speech-words.html
layouts/shortcodes/todo.html
```

## 本地预览

```bash
git clone --recurse-submodules git@github.com:macEngine/small-words.git
cd small-words
hugo server
```

## 版权

本站只引用演讲原句、链接官方视频，不托管视频或整篇文稿。视频与文稿版权归原发布方。
