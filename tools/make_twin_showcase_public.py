#!/usr/bin/env python3
"""Public copies of the two TwinLLM showcase pages for demos/structural-twin/.

The originals stay untouched. Public-face rules: no line or cable vocabulary (EN 50341-1, conductors, earth wires,
insulators), the monitoring events are synthetic (never "observed" / 实测), no API cost figures, a research-prototype
label, and the verification count carries the note that engineer review is still in progress.
Chinese strings appear both raw and \\u-escaped in the pages, so every Chinese replacement is applied in both forms.
Usage: python3 tools/make_twin_showcase_public.py <showcase source dir>
"""
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
OUT = SITE / "demos" / "structural-twin"
PAGES = {"TwinLLM_function_animation.html": "function-tour.html", "TwinLLM_analysis_demo.html": "analysis-demo.html"}

# (old, new); English strings are plain, Chinese strings are also applied in their \u-escaped form
SUBS = [
    ("three crossarm levels and an earth-wire peak", "three arm levels and a peak"),
    ('"include_conductors": true', '"include_attachments": true'),
    ("Conductor and earth-wire loads included", "Attachment-point loads included"),
    ("Leg utilisation at observed events below 0.6", "Leg utilisation at synthetic events below 0.6"),
    ("Wind loads (EN 1991-1-4, EN 1993-3-1, EN 50341-1)", "Wind loads (EN 1991-1-4, EN 1993-3-1)"),
    (', "EN 50341-1"]', "]"),
    ('"EN 50341-1", "Project value', '"Project value'),
    ('"th_cost": "费用", ', ""),
    ("th_cost: 'Cost', ", ""),
    ("Weight incl. conductors and insulators", "Weight incl. attached equipment"),
    ("observed events E1, E2", "synthetic events E1, E2"),
    ("Acceptance cases against hand calculations and analytical solutions",
     "Acceptance cases against hand calculations and analytical solutions (independent engineer review still in progress)"),
    ("verification cases passed (S3, S4, S8)", "verification cases passed (S3, S4, S8); engineer review in progress"),
    ("验证用例通过（S3、S4、S8）", "验证用例通过（S3、S4、S8），工程师复核进行中"),
    ("总重（含导线与绝缘子）", "总重（含附属设备）"),
    ("模型 / 实测 斜率比", "模型 / 合成数据 斜率比"),
    ("实测事件 E1、E2", "合成事件 E1、E2"),
    ("S4 风荷载（EN 1991-1-4、EN 1993-3-1、EN 50341-1）", "S4 风荷载（EN 1991-1-4、EN 1993-3-1）"),
    ("在平台上用 Claude API 实测", "在平台上用 Claude API 测试"),
    ("对照手算和解析解的验收用例", "对照手算和解析解的验收用例（工程师独立复核仍在进行）"),
    # API cost column: header, cell and the figures themselves
    ("<th class=\"n\">' + esc(T('th_cost')) + '</th>", ""),
    ("<td class=\"n\">US$ ' + r.usd + '</td>", ""),
]
# the EN 50341-1 entry of the code register (an object inside a JSON list)
CODE_ENTRY = re.compile(r',?\s*\{"code": "EN 50341-1", "used_for": "Wind on conductors and earth wires", "parameters": \{[^{}]*\}, "status": "[^"]*"\}')
CSS_CHIP = re.compile(r"(?<![A-Za-z0-9+/])chip(?![A-Za-z0-9+/=])")   # CSS class name; trips the public-face word filter
USD = re.compile(r',\s*"usd":\s*"[0-9.]+"')
BADGE = ('<style>#rpBadge{position:fixed;right:12px;bottom:12px;z-index:9999;font:600 12px/1.4 -apple-system,Segoe UI,sans-serif;'
         'background:#1d1d1b;color:#fff;border-radius:999px;padding:6px 12px;opacity:.9}'
         '@media (max-width:760px){#rpBadge{position:static;display:block;width:max-content;margin:16px auto}}</style>'
         '<div id="rpBadge">Research prototype &middot; synthetic demo data</div>')
HEAD = ('<meta name="robots" content="noindex, follow">\n<link rel="canonical" href="https://daguanghan.com/demos.html#software-demos">\n')
BANNED = re.compile(r"EN 50341|conductor|earth[- ]?wire|insulator|observed event|US\$|\"usd\"|导线|地线|绝缘子|实测|费用|输电|电网|\bkV\b", re.I)


def esc(s):
    return "".join(c if ord(c) < 128 else "\\u%04x" % ord(c) for c in s)


def readable(html):
    html = re.sub(r"[A-Za-z0-9+/=]{200,}", "", html)
    return re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), html)


def main(src):
    OUT.mkdir(parents=True, exist_ok=True)
    for name, out in PAGES.items():
        s = (Path(src) / name).read_text(encoding="utf-8")
        s, n_code = CODE_ENTRY.subn("", s)
        s, n_usd = USD.subn("", s)
        s = CSS_CHIP.sub("tagv", s)
        hits = {}
        for old, new in SUBS:
            for o, n in {(old, new), (esc(old), esc(new))}:
                c = s.count(o)
                if c:
                    s = s.replace(o, n)
                    hits[old[:40]] = hits.get(old[:40], 0) + c
        s = s.replace("<head>", "<head>\n" + HEAD, 1).replace("</body>", BADGE + "\n</body>", 1)
        left = sorted(set(m.group(0) for m in BANNED.finditer(readable(s))))
        (OUT / out).write_text(s, encoding="utf-8")
        print(f"{out}: code entries removed {n_code}, usd figures removed {n_usd}, replacements {sum(hits.values())}; remaining banned terms: {left or 'none'}")


if __name__ == "__main__":
    main(sys.argv[1])
