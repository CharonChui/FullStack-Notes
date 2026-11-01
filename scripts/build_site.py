#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把仓库里的 Markdown 笔记渲染成静态站点，输出到 docs/（GitHub Pages 源目录）。

用法：
    python3 scripts/build_site.py

依赖：
    pip3 install --user markdown
"""

import html
import os
import posixpath
import re
import shutil
import urllib.parse
from datetime import date

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs")
ASSETS_SRC = os.path.join(ROOT, "scripts", "site_assets")

GH = "https://github.com/CharonChui/FullStack-Notes/"
SKIP_DIRS = {".git", ".obsidian", ".workbuddy", "node_modules"}

# 域名, 目录, 英文说明, 中文描述, 图标
DOMAINS = [
    ("Android", "移动端", "Mobile", "Android / Kotlin / 音视频 / 端侧 AI", "📱"),
    ("CPP", "C / C++", "Native", "C 语言 / C++ / Qt / Linux 系统编程", "⚙️"),
    ("Golang", "Go", "Backend", "语言基础 / 并发 / Web 开发 / 数据库", "🐹"),
    ("HarmonyOS", "鸿蒙", "HarmonyOS", "ArkTS / 声明式 UI / UIAbility", "🧩"),
    ("Fe", "前端", "Frontend", "HTML/CSS/JS / 框架 / 工程化（规划中）", "🎨"),
    ("Server", "服务端", "Server", "Java / 数据库 / 中间件 / 运维（规划中）", "🗄️"),
]

ANDROID_ORDER = [
    "BasicKnowledge", "AdavancedPart", "SourceAnalysis", "VideoDevelopment",
    "Jetpack", "KotlinCourse", "Dagger2", "ImageLoaderLibrary", "RxJavaPart",
    "JavaKnowledge", "Algorithm", "OperatingSystem", "Architect",
    "Gradle&Maven", "Tools&Library", "AppPublish", "AndroidStudioCourse",
    "Flutter", "MobileAIModel",
]


# ---------------------------------------------------------------- 文件扫描

def natkey(name):
    m = re.match(r"^(\d+)", name)
    return (0, int(m.group(1)), name) if m else (1, 0, name)


def collect():
    """返回 {domain: [ (relpath_from_domain, group) ... ]}，仅排除该域根部的 README（作为域名首页）"""
    data = {}
    for dom, *_ in DOMAINS:
        base = os.path.join(ROOT, dom)
        files = []
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
            for f in filenames:
                if not f.endswith(".md"):
                    continue
                full = os.path.join(dirpath, f)
                rel = os.path.relpath(full, base).replace(os.sep, "/")
                if rel == "README.md":
                    continue  # 域名首页
                group = rel.split("/")[0] if "/" in rel else ""
                files.append((rel, group))
        files.sort(key=lambda x: (x[1] != "", natkey(x[1]), natkey(posixpath.basename(x[0]))))
        data[dom] = files
    return data


def display_title(rel):
    base = posixpath.basename(rel)
    if base == "README.md":
        return posixpath.basename(posixpath.dirname(rel)) or "目录"
    return re.sub(r"\.md$", "", base)


def groups_of(files, domain):
    order = ANDROID_ORDER if domain == "Android" else []
    groups = {}
    for rel, g in files:
        groups.setdefault(g, []).append(rel)
    keys = sorted(groups.keys(), key=lambda k: (k != "", order.index(k) if k in order else 999, natkey(k)))
    return [(k, groups[k]) for k in keys]


# ---------------------------------------------------------------- 路径映射

def out_rel(md_rel):
    """仓库相对 md 路径 -> 站点输出相对路径"""
    d, f = posixpath.split(md_rel)
    if f == "README.md":
        return (d + "/index.html") if d else "index.html"
    return md_rel[:-3] + ".html"


def url_of(site_rel, from_site_rel):
    """从某个输出页面指向另一个输出页面，返回百分号编码后的相对 href"""
    rel = posixpath.relpath(site_rel, posixpath.dirname(from_site_rel) or ".")
    return urllib.parse.quote(rel, safe="/")


def resolve_target(target, src_site_rel):
    """把仓库内的目标路径映射为输出页/资源，失败返回 None"""
    target = target.strip("/")
    if target.startswith("."):
        target = posixpath.normpath(target)
    full = os.path.join(ROOT, target)
    if target.endswith(".md") and os.path.isfile(full):
        return url_of(out_rel(target), src_site_rel)
    if os.path.isdir(full):
        idx = posixpath.join(target, "README.md")
        if os.path.isfile(os.path.join(ROOT, idx)):
            return url_of(out_rel(idx), src_site_rel)
        idx2 = posixpath.join(target, "index.html")
        if os.path.isfile(os.path.join(OUT, idx2)):
            return url_of(idx2, src_site_rel)
        return None
    if os.path.isfile(full) and not target.endswith((".md", ".html")):
        return urllib.parse.quote(target, safe="/")  # 静态资源按原路径直接引用
    return None


def fix_links(text, md_rel, site_rel):
    """重写 md 转 html 后的 href/src"""
    src_dir = posixpath.dirname(md_rel)

    def one(attr, raw):
        href = html.unescape(raw)
        if not href or href.startswith(("#", "mailto:", "javascript:", "data:")):
            return f'{attr}="{raw}"'
        if href.startswith(("http://", "https://", "//")):
            # 兼容各域原有仓库（AndroidNote / GolangStudyNote / …）：路径存在则转为站内链接
            m = re.match(r"https?://github\.com/CharonChui/[^/]+/(?:blob|tree|edit)/[^/]+/(.*)$", href)
            if m:
                frag = ""
                path = m.group(1)
                if "#" in path:
                    path, frag = path.split("#", 1)
                    frag = "#" + frag
                new = resolve_target(urllib.parse.unquote(path), site_rel)
                if new:
                    return f'{attr}="{new}{frag}"'
            return f'{attr}="{raw}" target="_blank" rel="noopener"'
        path, _, frag = href.partition("#")
        if not path:
            return f'{attr}="{raw}"'
        target = posixpath.normpath(posixpath.join(src_dir, urllib.parse.unquote(path)))
        new = resolve_target(target, site_rel)
        if new:
            return f'{attr}="{new}{("#" + frag) if frag else ""}"'
        return f'{attr}="{raw}"'

    return re.sub(r'(href|src)="([^"]*)"', lambda m: one(m.group(1), m.group(2)), text)


# ---------------------------------------------------------------- Markdown 渲染

def render_md(md_path):
    with open(md_path, encoding="utf-8", errors="ignore") as fh:
        text = fh.read()
    md = markdown.Markdown(
        extensions=["extra", "toc", "sane_lists", "admonition"],
        extension_configs={"toc": {"permalink": False, "toc_depth": "2-3"}},
    )
    body = md.convert(text)

    def flat(tokens):
        out = []
        for t in tokens:
            out.append(t)
            out.extend(flat(t.get("children") or []))
        return out

    toc = [t for t in flat(md.toc_tokens) if t["level"] in (2, 3)]
    return body, toc


def plain_title(body, fallback):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
    if m:
        t = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        if t:
            return t
    return fallback


# ---------------------------------------------------------------- 页面骨架

def head(title, root_rel, extra=""):
    return f"""<!DOCTYPE html>
<html lang="zh-CN" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="{root_rel}assets/style.css">
{extra}
</head>"""


def topbar(root_rel, crumbs, home_href):
    return f"""<header class="topbar">
  <div class="topbar-inner">
    <a class="brand" href="{home_href}"><span class="brand-dot"></span>全栈开发知识库</a>
    <nav class="crumbs">{crumbs}</nav>
    <div class="topbar-actions">
      <button class="icon-btn" id="theme-btn" title="切换主题" aria-label="切换主题">◐</button>
    </div>
  </div>
</header>"""


def sidebar(data, counts, current_domain, current_group, root_rel, home_href):
    parts = [f'<aside class="sidebar" id="sidebar"><div class="sb-inner">']
    parts.append(f'<a class="sb-home{" active" if not current_domain else ""}" href="{home_href}">🏠 全站首页</a>')
    for dom, label, _en, _desc, icon in DOMAINS:
        n = counts.get(dom, 0)
        if n == 0:
            continue
        active = " active" if dom == current_domain else ""
        parts.append(f'<div class="sb-domain{active}">')
        parts.append(
            f'<a class="sb-domain-link" href="{root_rel}{urllib.parse.quote(dom)}/index.html">'
            f'<span class="sb-icon">{icon}</span>{dom}<span class="sb-count">{n}</span></a>'
        )
        if dom == current_domain:
            parts.append('<div class="sb-subs">')
            for g, files in groups_of(data[dom], dom):
                if not g:
                    continue
                gname = g
                gurl = f"{root_rel}{urllib.parse.quote(dom)}/{urllib.parse.quote(g)}/index.html"
                if g == current_group:
                    parts.append(f'<div class="sb-group open"><a class="sb-sub active" href="{gurl}">{gname}</a><div class="sb-items">')
                    for rel in files:
                        site = out_rel(f"{dom}/{rel}")
                        curl = url_of_external(site, root_rel)
                        title = display_title(rel)
                        parts.append(f'<a class="sb-item" href="{curl}">{html.escape(title)}</a>')
                    parts.append("</div></div>")
                else:
                    parts.append(f'<a class="sb-sub" href="{gurl}">{gname}<span class="sb-count">{len(files)}</span></a>')
            parts.append("</div>")
        parts.append("</div>")
    parts.append("</div></aside>")
    return "".join(parts)


def url_of_external(site_rel, root_rel):
    """从站点根相对路径生成当前页可用的 href（页面均在根以下一层以内）"""
    return root_rel + urllib.parse.quote(site_rel, safe="/")


# ---------------------------------------------------------------- 各类页面

def article_page(dom, label, md_rel, body, toc, prev_next, data, counts, stats):
    site_rel = out_rel(f"{dom}/{md_rel}")
    depth = site_rel.count("/")
    root_rel = "../" * depth
    home_href = root_rel + "index.html"

    title = plain_title(body, display_title(md_rel))
    group = md_rel.split("/")[0] if "/" in md_rel else ""
    crumbs = []
    crumbs.append(f'<a href="{root_rel}{urllib.parse.quote(dom)}/index.html">{dom}</a>')
    if group:
        crumbs.append(
            f'<a href="{root_rel}{urllib.parse.quote(dom)}/{urllib.parse.quote(group)}/index.html">{group}</a>'
        )
    crumbs.append(f'<span class="crumb-cur">{html.escape(title)}</span>')

    toc_html = ""
    if len(toc) >= 3:
        items = "".join(
            f'<a class="toc-l{t["level"]}" href="#{t["id"]}">{html.escape(t["name"])}</a>' for t in toc
        )
        toc_html = f'<aside class="toc"><div class="toc-title">本页目录</div>{items}</aside>'

    pager = ""
    if prev_next:
        prev_a, next_a = prev_next
        bits = []
        if prev_a:
            bits.append(f'<a class="pager-prev" href="{prev_a[0]}"><span>← 上一篇</span><b>{html.escape(prev_a[1])}</b></a>')
        else:
            bits.append("<span></span>")
        if next_a:
            bits.append(f'<a class="pager-next" href="{next_a[0]}"><span>下一篇 →</span><b>{html.escape(next_a[1])}</b></a>')
        pager = f'<nav class="pager">{"".join(bits)}</nav>'

    return f"""{head(title + " · " + label, root_rel)}
<body class="page-article">
<div class="progress" id="progress"></div>
{topbar(root_rel, "".join(crumbs), home_href)}
<div class="shell">
  {sidebar(data, counts, dom, group, root_rel, home_href)}
  <main class="content">
    <article class="md" id="article">{body}</article>
    {pager}
    <footer class="page-foot">本页由 Markdown 自动渲染 · 共 {stats['total']} 篇笔记</footer>
  </main>
  {toc_html}
</div>
<script src="{root_rel}assets/app.js"></script>
</body>
</html>"""


def group_page(dom, label, icon, group, files, data, counts, stats, group_readme=None):
    site_rel = f"{dom}/{group}/index.html"
    depth = site_rel.count("/")
    root_rel = "../" * depth
    home_href = root_rel + "index.html"

    if group_readme:
        body, toc = render_md(os.path.join(ROOT, dom, group, "README.md"))
        body = fix_links(body, f"{dom}/{group}/README.md", site_rel)
        intro = f'<article class="md">{body}</article>'
        items = ""
    else:
        intro = f'<h1 class="page-title">{html.escape(group or label)}</h1><p class="page-sub">{len(files)} 篇笔记</p>'
        lis = []
        for rel in files:
            title = display_title(rel)
            sub = rel[len(group) + 1:] if group and rel.startswith(group + "/") else rel
            subdir = posixpath.dirname(sub)
            tag = f'<span class="item-tag">{html.escape(subdir)}</span>' if subdir else ""
            lis.append(
                f'<a class="item" href="{url_of(out_rel(f"{dom}/{rel}"), site_rel)}">'
                f'<span class="item-title">{html.escape(title)}</span>{tag}</a>'
            )
        items = f'<div class="item-list">{"".join(lis)}</div>'

    crumbs = f'<a href="{root_rel}{urllib.parse.quote(dom)}/index.html">{dom}</a><span class="crumb-cur">{html.escape(group or label)}</span>'
    return f"""{head((group or label) + " · " + label, root_rel)}
<body class="page-article">
{topbar(root_rel, crumbs, home_href)}
<div class="shell">
  {sidebar(data, counts, dom, group, root_rel, home_href)}
  <main class="content">
    {intro}
    {items}
    <footer class="page-foot">共 {stats['total']} 篇笔记 · 持续更新</footer>
  </main>
</div>
<script src="{root_rel}assets/app.js"></script>
</body>
</html>"""


def domain_page(dom, label, data, counts, stats):
    """域名首屏：由该域的 README.md 渲染"""
    site_rel = f"{dom}/index.html"
    root_rel = "../"
    home_href = root_rel + "index.html"
    md_path = os.path.join(ROOT, dom, "README.md")
    if os.path.isfile(md_path):
        body, toc = render_md(md_path)
        body = fix_links(body, f"{dom}/README.md", site_rel)
        content = f'<article class="md">{body}</article>'
    else:
        content = f'<h1 class="page-title">{html.escape(label)}</h1><p class="page-sub">暂无笔记</p>'

    # 子目录导航
    chips = []
    for g, files in groups_of(data[dom], dom):
        if not g:
            continue
        chips.append(
            f'<a class="chip" href="{urllib.parse.quote(g)}/index.html">'
            f'{html.escape(g)}<b>{len(files)}</b></a>'
        )
    chip_html = (
        f'<div class="chipbar"><span class="chipbar-label">主题目录</span><div class="chips">{"".join(chips)}</div></div>'
        if chips else ""
    )

    crumbs = f'<span class="crumb-cur">{dom}</span>'
    return f"""{head(label, root_rel)}
<body class="page-article">
{topbar(root_rel, crumbs, home_href)}
<div class="shell">
  {sidebar(data, counts, dom, "", root_rel, home_href)}
  <main class="content">
    {chip_html}
    {content}
  </main>
</div>
<script src="{root_rel}assets/app.js"></script>
</body>
</html>"""


def home_page(data, counts, stats):
    cards = []
    for dom, label, en, desc, icon in DOMAINS:
        n = counts.get(dom, 0)
        cards.append(f"""  <a class="card" href="{urllib.parse.quote(dom)}/index.html">
    <div class="card-top"><span class="card-icon">{icon}</span><span class="card-en">{en}</span></div>
    <h3>{label}</h3>
    <p>{desc}</p>
    <div class="card-meta">{str(n) + " 篇笔记" if n else "规划中"}</div>
  </a>""")

    browse = []
    for dom, label, _en, _desc, icon in DOMAINS:
        if counts.get(dom, 0) == 0:
            continue
        rows = []
        for g, files in groups_of(data[dom], dom):
            if not g:
                continue
            rows.append(
                f'<a class="brow" href="{urllib.parse.quote(dom)}/{urllib.parse.quote(g)}/index.html">'
                f'<span class="brow-name">{html.escape(g)}</span>'
                f'<span class="brow-count">{len(files)} 篇</span></a>'
            )
        browse.append(f"""  <section class="browse-sec">
    <h2><span>{icon}</span>{label}<a class="browse-more" href="{urllib.parse.quote(dom)}/index.html">查看该域 →</a></h2>
    <div class="brows">{''.join(rows)}</div>
  </section>""")

    return f"""{head("全栈开发知识库", "")}
<body class="page-home">
{topbar("", '<span class="crumb-cur">首页</span>', "index.html")}
<section class="hero">
  <div class="hero-inner">
    <span class="badge">Full Stack Notes · {stats['year']}</span>
    <h1>全栈开发知识库</h1>
    <p class="hero-sub">移动端 · C/C++ · Go · 鸿蒙 · 前端 · 服务端，{stats['total']} 篇工程实践笔记</p>
    <div class="search">
      <span class="search-icon">⌕</span>
      <input id="q" type="search" placeholder="搜索标题或路径，如 View、协程、Dagger2、排序…" autocomplete="off" spellcheck="false">
      <kbd>⌘K</kbd>
    </div>
    <div class="stats">
      <div><b>{stats['total']}</b><span>篇笔记</span></div>
      <div><b>{stats['domains']}</b><span>个技术域</span></div>
      <div><b>{stats['groups']}</b><span>个主题目录</span></div>
      <div><b>{stats['day']}</b><span>最后构建</span></div>
    </div>
  </div>
</section>
<main class="home">
  <div id="results" class="results" hidden></div>
  <section class="cards">{"".join(cards)}</section>
  <div id="browse">{''.join(browse)}</div>
</main>
<footer class="site-foot">
  <span>© {stats['year']} Charon Chui · Apache-2.0</span>
  <span>由 <code>scripts/build_site.py</code> 自动生成</span>
</footer>
<script src="assets/search-index.js"></script>
<script src="assets/app.js"></script>
</body>
</html>"""


# ---------------------------------------------------------------- 主流程

def main():
    data = collect()
    counts = {d: len(f) for d, f in data.items()}
    total = sum(counts.values())
    groups_total = sum(len([g for g, _ in groups_of(data[d], d) if g]) for d in data)

    stats = {
        "total": total,
        "domains": sum(1 for c in counts.values() if c),
        "groups": groups_total,
        "year": date.today().year,
        "day": date.today().strftime("%Y-%m-%d"),
    }

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)

    # 资源
    for f in ("style.css", "app.js"):
        shutil.copy(os.path.join(ASSETS_SRC, f), os.path.join(OUT, "assets", f))
    open(os.path.join(OUT, ".nojekyll"), "w").close()

    # 全局顺序（用于上一篇/下一篇）
    flat = []
    label_of = {d: l for d, l, *_ in DOMAINS}
    icon_of = {d: i for d, _l, _e, _d, i in DOMAINS}
    for dom, *_ in DOMAINS:
        for rel, _g in data[dom]:
            flat.append((dom, rel))
    pos = {k: i for i, k in enumerate(flat)}

    written = 0
    for dom, rel in flat:
        site_rel = out_rel(f"{dom}/{rel}")
        dst = os.path.join(OUT, site_rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        body, toc = render_md(os.path.join(ROOT, dom, rel))
        body = fix_links(body, f"{dom}/{rel}", site_rel)

        prev_next = [None, None]
        i = pos[(dom, rel)]
        depth = site_rel.count("/")
        root_rel = "../" * depth
        if i > 0:
            pd, pr = flat[i - 1]
            prev_next[0] = (
                root_rel + urllib.parse.quote(out_rel(f"{pd}/{pr}"), safe="/"),
                display_title(pr),
            )
        if i < len(flat) - 1:
            nd, nr = flat[i + 1]
            prev_next[1] = (
                root_rel + urllib.parse.quote(out_rel(f"{nd}/{nr}"), safe="/"),
                display_title(nr),
            )

        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(article_page(dom, label_of[dom], rel, body, toc, prev_next, data, counts, stats))
        written += 1

    # 目录页
    for dom, *_ in DOMAINS:
        os.makedirs(os.path.join(OUT, dom), exist_ok=True)
        with open(os.path.join(OUT, dom, "index.html"), "w", encoding="utf-8") as fh:
            fh.write(domain_page(dom, label_of[dom], data, counts, stats))
        for g, files in groups_of(data[dom], dom):
            if not g:
                continue
            gdir = os.path.join(OUT, dom, g)
            os.makedirs(gdir, exist_ok=True)
            has_readme = os.path.isfile(os.path.join(ROOT, dom, g, "README.md"))
            if has_readme:
                continue  # 该目录已有 README，渲染时已生成 index.html
            with open(os.path.join(gdir, "index.html"), "w", encoding="utf-8") as fh:
                fh.write(group_page(dom, label_of[dom], icon_of[dom], g, files, data, counts, stats))
            written += 1

    # 首页
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(home_page(data, counts, stats))

    # 搜索索引
    idx = []
    for dom, rel in flat:
        idx.append({
            "t": display_title(rel),
            "p": out_rel(f"{dom}/{rel}"),
            "d": label_of[dom],
        })
        idx[-1]["g"] = rel.split("/")[0] if "/" in rel else ""
    import json
    with open(os.path.join(OUT, "assets", "search-index.js"), "w", encoding="utf-8") as fh:
        fh.write("window.SEARCH_INDEX=" + json.dumps(idx, ensure_ascii=False, separators=(",", ":")) + ";")

    print(f"✓ 文章页 {written} 个，笔记 {total} 篇，技术域 {stats['domains']}，主题目录 {groups_total}")
    print(f"✓ 输出目录: {OUT}")


if __name__ == "__main__":
    main()
