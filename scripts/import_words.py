#!/usr/bin/env python3
"""把 words 仓库里一篇文章目录（`YYMMDD_<文章标题>/《纽约时报》每日一词：<word>.md` × N）
导入成 Hugo 内容：content/words/<slug>.md × N + content/sources/<source-slug>.md。

用法:
    python3 scripts/import_words.py "<目录>"                 # 默认：每词独立一篇，不建来源页、不加链接
    python3 scripts/import_words.py "<目录>" --source-slug xxx --source-title "..." [--source-note "..."]
                                                           # 可选：另建一个来源页并把词挂上去
    [--force] 覆盖已存在的文件

正文原样搬运（和公众号 gzh 用的是同一份 Markdown），只做三件事：
  1. 去掉空图占位 `![]()`（公众号补图用的，网站不需要）
  2. 等级标签行（`托福` `GRE`）→ 加 class 方便上色，并转成 tags
  3. 从「解析」里抽一句中文释义做 gloss（抽不到就留空，手动补）
"""
import argparse, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TITLE_RE = re.compile(r"^(?:《[^》]+》)?每日一词[:：](.+)\.md$")
GLOSS_RES = [re.compile(r"意思是[“\"]([^”\"]+)[”\"]"), re.compile(r"指[“\"]([^”\"]+)[”\"]")]
LEVEL_RE = re.compile(r"^(?:`[^`]+`[ \t]*)+$", re.M)

def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s

def yaml_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--source-slug")
    ap.add_argument("--source-title")
    ap.add_argument("--source-note", default="《纽约时报》")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    d = a.dir.rstrip("/")
    base = os.path.basename(d)
    m = re.match(r"^(\d{2})(\d{2})(\d{2})_(.+)$", base)
    if not m:
        sys.exit(f"目录名要像 260624_<标题>: {base}")
    date = f"20{m[1]}-{m[2]}-{m[3]}"
    src_title = a.source_title or m[4].strip()
    src_slug = a.source_slug            # 不给就不建来源页、单词页也不挂 source（默认：每词独立一篇）

    files = sorted(f for f in os.listdir(d) if f.endswith(".md"))
    out_words = os.path.join(ROOT, "content", "words")
    out_src = os.path.join(ROOT, "content", "sources", (src_slug or "x") + ".md")
    written = []
    for i, f in enumerate(files):
        tm = TITLE_RE.match(f)
        if not tm:
            print("跳过（文件名不匹配）:", f); continue
        word = tm[1].strip()
        slug = slugify(word)
        body = open(os.path.join(d, f), encoding="utf-8").read()
        body = re.sub(r"^!\[\]\(\)\s*\n", "", body, flags=re.M)
        levels = []
        lm = LEVEL_RE.search(body)
        if lm:
            levels = re.findall(r"`([^`]+)`", lm.group(0))
            body = body.replace(lm.group(0), '<p class="levels">' + " ".join(f"<code>{l}</code>" for l in levels) + "</p>", 1)
        gloss = ""
        for r in GLOSS_RES:
            g = r.search(body)
            if g: gloss = g.group(1); break
        tags = levels + ([src_slug] if src_slug else [])
        fm = [
            "---",
            f"title: {yaml_str(word)}",
            f"date: {date}T09:{i:02d}:00+08:00",
            "tags: [" + ", ".join(yaml_str(t) for t in tags) + "]",
            *([f"source: {yaml_str(src_slug)}"] if src_slug else []),
            f"gloss: {yaml_str(gloss)}",
            f"summary: {yaml_str(gloss)}",
            "---", "",
        ]
        p = os.path.join(out_words, slug + ".md")
        if os.path.exists(p) and not a.force:
            print("已存在，跳过（--force 覆盖）:", p); continue
        open(p, "w", encoding="utf-8").write("\n".join(fm) + body.rstrip() + "\n")
        written.append((word, gloss))
        print(f"  {word:14s} gloss={gloss or '(空，手动补)'}")

    if src_slug and (not os.path.exists(out_src) or a.force):
        open(out_src, "w", encoding="utf-8").write(f'''---
title: {yaml_str(src_title)}
date: {date}
summary: {yaml_str(a.source_note + " · " + date)}
---

{a.source_note}，{date}。本站从这篇文章里收录了 {len(files)} 个词。

> 本站只引用原句、注明出处；原文版权归原发布方。

## 本站收录的词

{{{{< source-words >}}}}
''')
        print("source page:", out_src)
    print(f"done: {len(written)} words" + (f" -> {src_slug}" if src_slug else " (独立页，无来源)"))

if __name__ == "__main__":
    main()
