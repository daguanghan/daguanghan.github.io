#!/usr/bin/env python3
"""One-off site consolidation (November 2026).

- experience.html  <- membership, talks, awards, teaching (each becomes a section; old files become redirects)
- publications.html gains a #patents section from patents.html (patents.html becomes a redirect)
- one eight-item nav on every top-level page and on tools/network.template.html
- sitemap.xml and llms.txt follow the new page list
papers/ is not touched.
"""
import re
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
NAV = [("index.html", "Home"), ("research.html", "Research"), ("ai-advisory.html", "AI &amp; Advisory"),
       ("projects.html", "Projects"), ("impact.html", "Impact"), ("publications.html", "Publications"),
       ("experience.html", "Experience"), ("demos.html", "Lab &amp; Demos")]
MERGED = [("membership", "membership", "Professional service"), ("talks", "talks", "Talks"),
          ("awards", "awards", "Recognition"), ("teaching", "teaching", "Teaching")]
DROP_FOOTERS = {"talks", "awards", "teaching"}   # policy footers that no longer apply


def read(name):
    return (SITE / name).read_text(encoding="utf-8")


def parts(html):
    head = html[:html.index('<header class="page-header">')]
    hdr = re.search(r'<header class="page-header">\s*<div class="container">(.*?)</div>\s*</header>', html, re.S).group(1)
    main = re.search(r"<main>(.*?)</main>", html, re.S).group(1)
    foot = re.search(r'<footer class="footer">\s*<div class="container">(.*?)</div>\s*</footer>', html, re.S)
    return head, hdr, main, foot.group(1) if foot else ""


def section_header(hdr, kicker, anchor):
    eyebrow = re.search(r'<p class="eyebrow">(.*?)</p>', hdr, re.S).group(1)
    title = re.search(r'<h1 class="page-title">(.*?)</h1>', hdr, re.S).group(1)
    sub = re.search(r'<p class="page-subtitle">(.*?)</p>', hdr, re.S)
    rest = hdr[hdr.index("</p>", hdr.index('page-subtitle')) + 4:] if sub else ""
    return (f'        <section class="section merged-head" id="{anchor}">\n            <div class="container">\n'
            f'                <div class="section-header"><div><p class="kicker">{kicker}</p>'
            f'<h2 class="section-title">{title}</h2>'
            + (f'<p class="section-subtitle">{sub.group(1)}</p>' if sub else "")
            + f'</div></div>{rest.strip()}\n            </div>\n        </section>\n')


def footer_note(foot):
    if not foot.strip():
        return ""
    h = re.search(r"<h2>(.*?)</h2>", foot, re.S).group(1)
    p = re.search(r"<p>(.*?)</p>", foot, re.S).group(1)
    return (f'        <section class="section compact">\n            <div class="container">\n'
            f'                <div class="safe-note"><strong>{h}.</strong> {p.strip()}</div>\n            </div>\n        </section>\n')


def nav_html(active):
    items = "\n".join(f'                <li><a href="{h}"{" class=\"active\"" if h == active else ""}>{t}</a></li>' for h, t in NAV)
    return f'<ul class="nav-links">\n{items}\n            </ul>'


def set_nav(html, active):
    return re.sub(r'<ul class="nav-links">.*?</ul>', lambda m: nav_html(active), html, count=1, flags=re.S)


def redirect(target, label):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Moved to {label} | Daguang Han</title>
    <link rel="canonical" href="https://daguanghan.com/{target}">
    <meta http-equiv="refresh" content="0; url={target}">
    <meta name="robots" content="noindex, follow">
    <style>body{{background:#000;color:#fff;font-family:Inter,-apple-system,sans-serif;padding:2rem}}a{{color:#9aa7ff}}</style>
</head>
<body>
    <p>This page is now part of <a href="{target}">{label}</a>.</p>
</body>
</html>
"""


def main():
    # 1. experience.html
    head0, _, _, _ = parts(read("membership.html"))
    head = re.sub(r'<meta name="description" content="[^"]*">',
                  '<meta name="description" content="Professional service, invited talks, awards and teaching of Dr.-Ing. Daguang Han.">', head0)
    head = re.sub(r"<title>.*?</title>", "<title>Experience | Daguang Han</title>", head)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="https://daguanghan.com/experience.html">', head)
    body = ['    <header class="page-header">\n        <div class="container">\n'
            '            <p class="eyebrow">Experience</p>\n'
            '            <h1 class="page-title">Professional service, talks, recognition and teaching</h1>\n'
            '            <p class="page-subtitle">Memberships and editorial roles, invited talks, awards, and teaching and supervision. '
            'The institutions I work with are mapped on the <a href="network.html">collaboration page</a>.</p>\n'
            '            <div class="action-row">'
            + "".join(f'<a class="btn secondary" href="#{a}">{k}</a>' for _, a, k in MERGED)
            + '<a class="btn secondary" href="network.html">Where I work with colleagues</a></div>\n'
            '        </div>\n    </header>\n\n    <main>\n']
    for name, anchor, kicker in MERGED:
        _, hdr, main_, foot = parts(read(f"{name}.html"))
        body.append(section_header(hdr, kicker, anchor))
        body.append(main_.strip("\n") + "\n")
        if name not in DROP_FOOTERS:
            body.append(footer_note(foot))
    body.append("    </main>\n</body>\n</html>\n")
    (SITE / "experience.html").write_text(set_nav(head + "".join(body), "experience.html"), encoding="utf-8")

    # 2. patents into publications
    pub = read("publications.html")
    if 'id="patents"' not in pub:
        _, hdr, main_, foot = parts(read("patents.html"))
        block = section_header(hdr, "Patents", "patents") + main_.strip("\n") + "\n" + footer_note(foot)
        pub = pub.replace("    </main>", block + "    </main>", 1)
    (SITE / "publications.html").write_text(pub, encoding="utf-8")

    # 3. redirects
    for name, anchor, kicker in MERGED:
        (SITE / f"{name}.html").write_text(redirect(f"experience.html#{anchor}", "Experience"), encoding="utf-8")
    (SITE / "patents.html").write_text(redirect("publications.html#patents", "Publications"), encoding="utf-8")

    # 4. nav everywhere
    redirected = {f"{n}.html" for n, _, _ in MERGED} | {"patents.html"}
    for f in sorted(SITE.glob("*.html")):
        if f.name in redirected:
            continue
        s = f.read_text(encoding="utf-8")
        if '<ul class="nav-links">' in s:
            f.write_text(set_nav(s, f.name), encoding="utf-8")
    t = SITE / "tools/network.template.html"
    t.write_text(set_nav(t.read_text(encoding="utf-8"), ""), encoding="utf-8")

    # 5. sitemap
    sm = read("sitemap.xml")
    for name in [n for n, _, _ in MERGED] + ["patents"]:
        sm = re.sub(rf"\s*<url>\s*<loc>https://daguanghan.com/{name}\.html</loc>.*?</url>", "", sm, flags=re.S)
    for page in ["experience.html", "ai-advisory.html", "network.html"]:
        if f"/{page}<" not in sm:
            sm = sm.replace('  <url><loc>https://daguanghan.com/demos.html',
                            f'  <url><loc>https://daguanghan.com/{page}</loc><lastmod>2026-11-02</lastmod><priority>0.8</priority></url>\n  <url><loc>https://daguanghan.com/demos.html', 1)
    (SITE / "sitemap.xml").write_text(sm, encoding="utf-8")


if __name__ == "__main__":
    main()
