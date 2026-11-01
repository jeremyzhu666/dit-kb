#!/usr/bin/env python3
"""Render DIT知识库 Markdown files into dit-kb-site/public as static HTML.

风格参考 Freefly Knowledge Base（GitBook 系）：
浅色主题 / 左侧文档树 / 内容区居中 / 页脚带更新时间与上一篇·下一篇导航。
"""
import datetime
from pathlib import Path
from urllib.parse import quote
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent / "DIT知识库"
OUT = ROOT / "public"
OUT.mkdir(exist_ok=True)

md = MarkdownIt("commonmark", {"html": True}).enable("table")

TODAY = "2026-11-01"

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · DIT 知识库</title>
<style>
:root {{
  --sidebar-w: 280px;
  --accent: #1f6feb;
  --accent-soft: #eaf2fe;
  --ink: #24292f;
  --muted: #6e7781;
  --line: #e6e8eb;
  --bg: #ffffff;
  --sidebar-bg: #fafbfc;
  --hint-bg: #f6f8fa;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; background: var(--bg); color: var(--ink); line-height: 1.75; font-size: 15px; }}
a {{ color: var(--accent); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}

/* 顶栏 */
.topbar {{ position: sticky; top: 0; z-index: 20; display: flex; align-items: center; gap: 10px; height: 52px; padding: 0 20px; background: rgba(255,255,255,.92); backdrop-filter: blur(8px); border-bottom: 1px solid var(--line); }}
.topbar .logo {{ width: 24px; height: 24px; border-radius: 6px; background: var(--accent); color: #fff; font-size: 13px; font-weight: 700; display: flex; align-items: center; justify-content: center; }}
.topbar .site {{ font-weight: 600; font-size: 15px; }}
.topbar .tag {{ font-size: 12px; color: var(--muted); }}
.topbar .crumb {{ margin-left: auto; font-size: 13px; color: var(--muted); }}

.layout {{ display: flex; min-height: calc(100vh - 52px); }}

/* 侧边栏（GitBook 文档树） */
.sidebar {{ width: var(--sidebar-w); flex-shrink: 0; background: var(--sidebar-bg); border-right: 1px solid var(--line); padding: 18px 14px 60px; position: sticky; top: 52px; height: calc(100vh - 52px); overflow-y: auto; }}
.sidebar .search {{ width: 100%; padding: 7px 12px; font-size: 13px; border: 1px solid var(--line); border-radius: 8px; background: #fff; outline: none; margin-bottom: 14px; }}
.sidebar .search:focus {{ border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-soft); }}
.sidebar .group {{ font-size: 11px; font-weight: 600; color: var(--muted); letter-spacing: .06em; text-transform: uppercase; margin: 18px 8px 4px; }}
.sidebar a.navlink {{ display: block; color: #3b4048; font-size: 13.5px; padding: 5px 10px; border-radius: 6px; }}
.sidebar a.navlink:hover {{ background: #eef1f4; text-decoration: none; }}
.sidebar a.navlink.active {{ background: var(--accent-soft); color: var(--accent); font-weight: 600; }}
.sidebar a.navlink.hidden, .sidebar .group.hidden {{ display: none; }}

/* 内容区 */
.content {{ flex: 1; min-width: 0; padding: 40px 48px 80px; }}
.content .inner {{ max-width: 780px; margin: 0 auto; }}
.content h1 {{ font-size: 30px; font-weight: 700; margin-bottom: 20px; letter-spacing: -.01em; }}
.content h2 {{ font-size: 21px; font-weight: 650; margin: 36px 0 12px; padding-top: 8px; }}
.content h3 {{ font-size: 16.5px; font-weight: 650; margin: 24px 0 8px; }}
.content p {{ margin: 10px 0; }}
.content blockquote {{ border: 1px solid var(--line); border-left: 3px solid var(--accent); background: var(--hint-bg); padding: 12px 16px; margin: 14px 0; border-radius: 0 8px 8px 0; color: #3b4048; font-size: 14px; }}
.content blockquote p {{ margin: 4px 0; }}
.content table {{ border-collapse: collapse; width: 100%; margin: 16px 0; font-size: 14px; display: block; overflow-x: auto; }}
.content thead, .content tbody {{ display: table; width: 100%; }}
.content th, .content td {{ border: 1px solid var(--line); padding: 8px 12px; text-align: left; }}
.content th {{ background: var(--hint-bg); font-weight: 600; }}
.content ul, .content ol {{ margin: 10px 0 10px 24px; }}
.content li {{ margin: 4px 0; }}
.content code {{ background: var(--hint-bg); border: 1px solid var(--line); padding: 1px 6px; border-radius: 5px; font-size: 13px; }}
.content pre {{ background: var(--hint-bg); border: 1px solid var(--line); padding: 14px 16px; border-radius: 8px; overflow-x: auto; margin: 14px 0; }}
.content pre code {{ background: none; border: none; padding: 0; }}
.content hr {{ border: none; border-top: 1px solid var(--line); margin: 28px 0; }}
.content strong {{ font-weight: 650; }}

/* 页脚：更新时间 + 上/下一篇 */
.foot {{ max-width: 780px; margin: 48px auto 0; }}
.updated {{ font-size: 13px; color: var(--muted); padding-top: 16px; border-top: 1px solid var(--line); }}
.pager {{ display: flex; justify-content: space-between; gap: 14px; margin-top: 20px; }}
.pager a {{ flex: 1; max-width: 48%; border: 1px solid var(--line); border-radius: 10px; padding: 12px 16px; font-size: 13.5px; color: var(--ink); background: #fff; }}
.pager a:hover {{ border-color: var(--accent); text-decoration: none; box-shadow: 0 1px 4px rgba(31,111,235,.12); }}
.pager a .dir {{ display: block; font-size: 12px; color: var(--muted); margin-bottom: 2px; }}
.pager a.next {{ text-align: right; margin-left: auto; }}

@media (max-width: 820px) {{
  .layout {{ flex-direction: column; }}
  .sidebar {{ width: 100%; height: auto; position: static; border-right: none; border-bottom: 1px solid var(--line); }}
  .content {{ padding: 26px 20px 60px; }}
  .topbar .crumb {{ display: none; }}
}}
</style>
</head>
<body>
<header class="topbar">
  <span class="logo">D</span>
  <span class="site">DIT 知识库</span>
  <span class="tag">短片 / 广告 / MV · 实战教学版</span>
  <span class="crumb">{crumb}</span>
</header>
<div class="layout">
<nav class="sidebar">
<input class="search" type="search" placeholder="搜索文档…" oninput="filterNav(this.value)">
{nav}
</nav>
<main class="content"><div class="inner">
{body}
<div class="foot">
  <div class="updated">最后更新：{updated}</div>
  <div class="pager">{prev}{next}</div>
</div>
</div></main>
</div>
<script>
function filterNav(q) {{
  q = q.trim().toLowerCase();
  document.querySelectorAll('.sidebar a.navlink').forEach(a => {{
    a.classList.toggle('hidden', q && !a.textContent.toLowerCase().includes(q));
  }});
  document.querySelectorAll('.sidebar .group').forEach(g => {{
    let el = g.nextElementSibling, any = false;
    while (el && !el.classList.contains('group')) {{
      if (el.classList.contains('navlink') && !el.classList.contains('hidden')) any = true;
      el = el.nextElementSibling;
    }}
    g.classList.toggle('hidden', !any);
  }});
}}
</script>
</body>
</html>
"""


def slug(rel: Path) -> str:
    """URL path without extension, preserving Chinese; dirs kept."""
    return str(rel.with_suffix(""))


# collect docs grouped by top-level dir, sorted
groups: dict[str, list[Path]] = {}
for f in sorted(SRC.rglob("*.md")):
    rel = f.relative_to(SRC)
    if rel.name == "README.md" and len(rel.parts) == 1:
        continue
    groups.setdefault(rel.parts[0] if len(rel.parts) > 1 else "", []).append(f)

nav_items = []   # (group, title, href, key)
for g in sorted(groups):
    for f in groups[g]:
        rel = f.relative_to(SRC)
        key = slug(rel)
        nav_items.append((rel.parts[0] if len(rel.parts) > 1 else "", f.stem, quote(key) + ".html", key))

# 扁平页序：首页在最前，用于上一篇/下一篇
flat = [("首页", "index.html", "")] + [(t, h, k) for _, t, h, k in nav_items]


def render_nav(active: str) -> str:
    html = []
    cur = None
    for g, title, href, key in nav_items:
        if g != cur:
            html.append(f'<div class="group">{g or "综合"}</div>')
            cur = g
        cls = ' class="navlink active"' if key == active else ' class="navlink"'
        html.append(f'<a href="{href}"{cls}>{title}</a>')
    return "\n".join(html)


def render_pager(idx: int) -> tuple[str, str]:
    prev_html = next_html = ""
    if idx > 0:
        t, h, _ = flat[idx - 1]
        prev_html = f'<a class="prev" href="{h}"><span class="dir">← 上一篇</span>{t}</a>'
    if idx < len(flat) - 1:
        t, h, _ = flat[idx + 1]
        next_html = f'<a class="next" href="{h}"><span class="dir">下一篇 →</span>{t}</a>'
    return prev_html, next_html


def write_page(title: str, active_key: str, body: str, out_file: Path, flat_idx: int):
    prev_html, next_html = render_pager(flat_idx)
    crumb = f"DIT 知识库 / {title}" if title != "首页" else "DIT 知识库"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(
        TEMPLATE.format(title=title, crumb=crumb, nav=render_nav(active_key),
                        body=body, updated=TODAY, prev=prev_html, next=next_html),
        encoding="utf-8")


# home page
home_body = md.render((SRC / "README.md").read_text(encoding="utf-8"))
write_page("首页", "", home_body, OUT / "index.html", 0)

for i, (g, title, href, key) in enumerate(nav_items, start=1):
    f = next(x for x in groups[g] if slug(x.relative_to(SRC)) == key)
    body = md.render(f.read_text(encoding="utf-8"))
    write_page(title, key, body, OUT / (key + ".html"), i)

print(f"built {len(nav_items) + 1} pages -> {OUT}")
