# Makes the public copies of the two Standfast demo pages for daguanghan.com.
# Run from the site root:  python3 tools/make_standfast_public.py <folder with Standfast_Analysis_Demo.html and Standfast_Feature_Tour.html>
# Display text only: the real place name is withheld, no vendor identifier stays in the source,
# the two pages link to each other under their published names, and a link back to the prototypes page is added.
import re, sys, pathlib
SRC = pathlib.Path(sys.argv[1]); OUT = pathlib.Path("demos/standfast")
def u(t): return "".join("\\u%04x" % ord(c) if ord(c) > 127 else c for c in t)
PAIRS = [
 ("Charnwood Forest, Leicestershire \\u00b7 Demo Line A", "Upland terrain, England \\u00b7 Demo Line A"),
 ("across the north flank of Beacon Hill in Charnwood Forest.", "across the north flank of an upland ridge in England."),
 ("LiDAR terrain of Charnwood Forest.", "LiDAR terrain of an upland site in England."),
 ('<span data-i="crumb.site">Charnwood Forest</span>', '<span data-i="crumb.site">Demo terrain</span>'),
 ("'crumb.site': ['Charnwood Forest', '" + u("查恩伍德森林") + "']", "'crumb.site': ['Demo terrain', '" + u("演示地形") + "']"),
 (u("英国莱斯特郡查恩伍德森林"), u("英格兰丘陵地形")),
 (u("查恩伍德森林比肯山北坡"), u("英格兰一处丘陵的北坡")),
 (u("英国环境署查恩伍德森林 LiDAR"), u("英国环境署 LiDAR")),
 ("http://localhost:11434", "http://localhost:8080"),
 ("Standfast_Feature_Tour.html", "function-tour.html"),
 ("Standfast_Analysis_Demo.html", "analysis-demo.html"),
]
FORBID = [r"Charnwood", r"Leicestershire", r"Beacon Hill", u("查恩伍德"), u("莱斯特"), u("比肯"), r"(?i)anthropic|claude|openai|ollama", r"A\. ?Smith|CEng"]
BADGE = ('<style>#rpBack{position:fixed;left:12px;bottom:12px;z-index:9999;font:600 12px/1.4 -apple-system,Segoe UI,sans-serif;'
         'background:#1d1d1b;color:#fff;border-radius:999px;padding:6px 12px;opacity:.92}#rpBack a{color:#fff}'
         '@media (max-width:760px){#rpBack{position:static;display:block;width:max-content;margin:16px auto}}</style>'
         '<div id="rpBack">Research prototype &middot; demo data &middot; <a href="/demos.html#standfast">Daguang Han: all prototypes</a></div>')
for src, out in (("Standfast_Analysis_Demo.html", "analysis-demo.html"), ("Standfast_Feature_Tour.html", "function-tour.html")):
    s = (SRC / src).read_text(encoding="utf-8")
    for a, b in PAIRS:
        s = s.replace(a, b)
    s = re.sub(r"\banthropic\b", "cloud", s)
    # A visible line on the review panel: the workflow is demonstrated, nobody has reviewed these results.
    key = "'rev.reviewer': ['Reviewer: engineer to be named (demo)', '" + u("审核人：工程师待定（演示）") + "'],"
    assert s.count(key) == 1, out
    s = s.replace(key, key + "   'rev.demo': ['Demo of the review workflow. No engineer has reviewed these results.', '" + u("审核流程演示。这些结果尚未经任何工程师审核。") + "'],")
    box = "font-size:13px;font-weight:600;line-height:1.4;background:rgba(255,149,0,.14);border:1px solid rgba(255,149,0,.55);border-radius:8px;padding:7px 10px"
    if out == "analysis-demo.html":
        ol = '<ol class="steps" id="rev-steps"></ol>'
        assert s.count(ol) == 1
        s = s.replace(ol, '<p data-i="rev.demo" style="margin:0 0 12px;%s"></p>\n        ' % box + ol)
    else:
        chip = "el('span', 'chip', t('pane.rev.reviewer'), body).style.alignSelf = 'flex-start';"
        assert s.count(chip) == 1
        s = s.replace(chip, chip + " el('div', null, t('rev.demo'), body).style.cssText = '%s';" % box)
    head = '<meta name="robots" content="index, follow">\n<link rel="canonical" href="https://daguanghan.com/demos/standfast/%s">' % out
    assert s.count("</title>") == 1 and s.count("</body>") == 1
    s = s.replace("</title>", "</title>\n" + head, 1).replace("</body>", BADGE + "\n</body>", 1)
    for pat in FORBID:
        m = re.search(pat, s)
        assert not m, (out, pat, s[max(0, m.start() - 60):m.end() + 60])
    (OUT / out).write_text(s, encoding="utf-8")
    print("written", OUT / out, len(s))
