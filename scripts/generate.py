#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Moire 静态生成器（classic 密集日志主题）

读取 src/memos/**/*.md，生成 build/index.html。
- 日期从文件名 YYYYMMDDHHMMSS 前缀解析，其次 frontmatter 的 created，再次文件 mtime
- 正文按 markdown 渲染（## 标题、列表、引用、代码块等）
- 行内 #tag 渲染为标签胶囊
- 相对图片复制到 build/assets 并改写路径（http/绝对路径原样保留）
- 不移动任何 md 文件

用法: python scripts/generate.py
"""

import os
import re
import shutil
import datetime

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMOS_DIR = os.path.join(ROOT, "src", "memos")
BUILD_DIR = os.path.join(ROOT, "build")
ASSETS_DIR = os.path.join(BUILD_DIR, "assets")

MD_EXTENSIONS = ["extra", "sane_lists", "tables"]


def load_config():
    """从 moire.config.ts 抽取字符串字段（保持单一信息源，不重复维护）。"""
    path = os.path.join(ROOT, "moire.config.ts")
    text = ""
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            text = f.read()

    def get(key):
        m = re.search(r'%s\s*:\s*"([^"]*)"' % re.escape(key), text)
        return m.group(1) if m else ""

    return {
        "title": get("title") or "Moire",
        "author": get("author") or "",
        "description": get("description") or "",
    }


def strip_frontmatter(raw):
    m = re.match(r"^---\s*\n.*?\n---\s*\n?", raw, re.S)
    if m:
        return raw[m.end():]
    return raw


def parse_date(slug, path):
    m = re.match(r"(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})", slug)
    if m:
        y, mo, d, h, mi, s = (int(x) for x in m.groups())
        try:
            return datetime.datetime(y, mo, d, h, mi, s)
        except ValueError:
            pass
    return datetime.datetime.fromtimestamp(os.path.getmtime(path))


def collect_memos():
    memos = []
    if not os.path.isdir(MEMOS_DIR):
        return memos

    for md_path in sorted(
        p for p in _iter_files(MEMOS_DIR) if p.lower().endswith(".md")
    ):
        rel = os.path.relpath(md_path, MEMOS_DIR)
        slug = os.path.splitext(os.path.basename(md_path))[0]
        with open(md_path, encoding="utf-8") as f:
            raw = f.read()
        raw = strip_frontmatter(raw)
        memos.append(
            {
                "slug": slug,
                "rel_dir": os.path.dirname(rel),
                "date": parse_date(slug, md_path),
                "raw": raw,
            }
        )

    memos.sort(key=lambda m: m["date"], reverse=True)
    return memos


def _iter_files(base):
    for root, _dirs, files in os.walk(base):
        for name in files:
            yield os.path.join(root, name)


IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def process_images(raw, rel_dir):
    """复制相对图片到 build/assets，并把路径改写为发布路径。"""
    def repl(m):
        alt, src = m.group(1), m.group(2).strip()
        if src.startswith(("http://", "https://", "//", "/", "data:")):
            return m.group(0)
        src_path = os.path.normpath(os.path.join(MEMOS_DIR, rel_dir, src))
        if not os.path.isfile(src_path):
            return m.group(0)
        out_rel = os.path.join("assets", rel_dir, os.path.basename(src))
        dest = os.path.join(BUILD_DIR, out_rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy(src_path, dest)
        return "![%s](%s)" % (alt, out_rel.replace(os.sep, "/"))

    return IMG_RE.sub(repl, raw)


TAG_RE = re.compile(r"(?<![#\w])#([^\s#.,!?;:()\[\]\"']+)")


def render_body_with_dir(raw, rel_dir):
    raw = process_images(raw, rel_dir)
    body = TAG_RE.sub(
        lambda m: '<span class="tag" data-tag="%s">#%s</span>' % (m.group(1), m.group(1)),
        raw,
    )
    return markdown.markdown(body, extensions=MD_EXTENSIONS)


CSS = """
:root {
  --bg: #ffffff;
  --fg: #1d1d1f;
  --muted: #9a9a9a;
  --line: #ececec;
  --accent: #3a6ea5;
  --tag-bg: #f1f3f5;
  --tag-fg: #4a5568;
}
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--fg);
  font-family: "SimSun", "宋体", "Songti SC", "STSong", "KaiTi", "楷体", serif;
  font-size: 13.5px;
  line-height: 1.45;
}
.wrap { max-width: 760px; margin: 0 auto; padding: 16px 16px 40px; }
.site-head { border-bottom: 1px solid var(--line); padding-bottom: 8px; margin-bottom: 4px; }
.site-head h1 { font-size: 17px; font-weight: 700; margin: 0 0 2px; letter-spacing: .2px; }
.site-head .desc { color: var(--muted); font-size: 12px; }
.memo {
  display: flex;
  gap: 10px;
  padding: 6px 0;
  border-bottom: 1px dashed var(--line);
}
.memo .date {
  flex: 0 0 74px;
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
  font-size: 11.5px;
  color: var(--muted);
  padding-top: 2px;
  white-space: nowrap;
}
.memo .body { flex: 1 1 auto; min-width: 0; }
.memo .body > :first-child { margin-top: 0; }
.memo .body > :last-child { margin-bottom: 0; }
.memo h1, .memo h2, .memo h3 { line-height: 1.3; margin: 8px 0 4px; }
.memo h1 { font-size: 15px; }
.memo h2 { font-size: 14px; }
.memo h3 { font-size: 13.5px; }
.memo p { margin: 4px 0; }
.memo ul, .memo ol { margin: 4px 0; padding-left: 20px; }
.memo li { margin: 1px 0; }
.memo blockquote {
  margin: 4px 0; padding: 1px 10px;
  border-left: 3px solid var(--line); color: #555; font-style: italic;
}
.memo code {
  font-family: "SFMono-Regular", Consolas, Menlo, monospace;
  font-size: 12px; background: #f5f5f7; padding: 1px 4px; border-radius: 4px;
}
.memo pre {
  background: #f5f5f7; padding: 8px; border-radius: 6px;
  overflow-x: auto; font-size: 12px; line-height: 1.45;
}
.memo pre code { background: none; padding: 0; }
.memo a { color: var(--accent); text-decoration: none; }
.memo a:hover { text-decoration: underline; }
.memo img { max-width: 100%; border-radius: 6px; margin: 4px 0; }
.memo table { border-collapse: collapse; margin: 5px 0; font-size: 12.5px; }
.memo th, .memo td { border: 1px solid var(--line); padding: 3px 7px; text-align: left; }
.tag {
  display: inline-block; font-size: 11.5px; line-height: 1;
  background: var(--tag-bg); color: var(--tag-fg);
  padding: 2px 6px; border-radius: 999px; margin: 0 2px;
}
.site-foot { margin-top: 28px; padding-top: 14px; border-top: 1px solid var(--line);
  color: var(--muted); font-size: 12px; text-align: center; }
@media (max-width: 520px) {
  .memo { flex-direction: column; gap: 1px; }
  .memo .date { padding-top: 0; }
}
"""


def build_html(config, memos):
    items = []
    for m in memos:
        date_str = m["date"].strftime("%Y.%m.%d")
        body = render_body_with_dir(m["raw"], m["rel_dir"])
        items.append(
            '<article class="memo">'
            '<div class="date">%s</div>'
            '<div class="body">%s</div>'
            "</article>" % (date_str, body)
        )

    desc = config["description"]
    desc_html = '<div class="desc">%s</div>' % desc if desc else ""

    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<style>%(css)s</style>
</head>
<body>
<div class="wrap">
  %(items)s
</div>
</body>
</html>
""" % {
        "title": config["title"],
        "desc": desc,
        "css": CSS,
        "desc_html": desc_html,
        "items": "\n".join(items),
    }


def main():
    config = load_config()
    memos = collect_memos()

    if os.path.isdir(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    os.makedirs(ASSETS_DIR, exist_ok=True)

    html = build_html(config, memos)
    out = os.path.join(BUILD_DIR, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)

    print("Generated %s memos -> %s" % (len(memos), out))


if __name__ == "__main__":
    main()
