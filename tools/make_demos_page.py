# Builds demos.html for daguanghan.com (Research prototypes).
# Run from the site root:  python3 tools/make_demos_page.py
# The laboratory section lives in tools/demos_lab_section.html. Screenshots: images/prototypes/.
import json, re, html
BASE = "https://daguanghan.com/"
P = {
 "dxf":  ("End-to-End Automated Wind-Induced Stress Simulation of Lattice Transmission Towers in Complex Terrain via Physics-Conserving PINN Wind-Field Reconstruction and Graph-Theory-Based DXF Parsing", "Applied Sciences, 2026", "10.3390/app16178582", "papers/end-to-end-automated-wind-induced-stress-simulation-of-lattice-transm.html"),
 "corr": ("Integrated Multi-Mode Image-Based Corrosion Assessment and Probabilistic Reliability Framework for Steel Tower Structures Under Uncertainty", "Buildings, 2026", "10.3390/buildings16112250", "papers/integrated-multi-mode-image-based-corrosion-assessment-and-probabilist.html"),
 "risk": ("Risk-Based Safety Assessment of Aging Lattice Steel Space-Truss Structures Under Extreme Winds: A Multi-Scale Wind and Multi-Degradation Coupling Framework with Application to Transmission Towers", "Applied Sciences, 2026", "10.3390/app16136788", "papers/risk-based-safety-assessment-of-aging-lattice-steel-space-truss-struct.html"),
 "grid": ("An Auditable Gridded Wind–DEM-to-FE Workflow with Source Time, Spatial Contract, Texture Axis, and Solver Balance Gates: A Transmission Tower Case Study", "Applied Sciences, 2026", "10.3390/app16199420", None),
 "om":   ("Multi-domain data integration and management for enhancing service-oriented digital twin for infrastructure operation and maintenance", "Developments in the Built Environment, 2024", "10.1016/j.dibe.2024.100475", "papers/multi-domain-data-integration-and-management-for-enhancing-service-ori.html"),
 "hitl": ("Human-in-the-Loop Semantic Rule Base Generation and Dynamic Updating for Automated BIM Compliance Checking: A Knowledge Graph Approach", "Buildings, 2026", "10.3390/buildings16040719", "papers/human-in-the-loop-semantic-rule-base-generation-and-dynamic-updating-f.html"),
 "ahu":  ("A Digital Twin predictive maintenance framework of air handling units based on automatic fault detection and diagnostics", "Energy and Buildings, 2022", "10.1016/j.enbuild.2022.111988", "papers/a-digital-twin-predictive-maintenance-framework-of-air-handling-units.html"),
}
IMG = "images/prototypes/"
PROTOS = [
 dict(id="earthstate-twin", n="01", field="Ageing steel towers", name="EarthState Twin",
      q="How much can one ageing lattice tower still carry?",
      one="One tower in depth: a member-level model built from the drawings, with every member checked to EN 1993-1-1.",
      body=["The prototype reads the node and member tables of a drawing set, builds a member-level frame model and runs its own checks before the model is used: equilibrium under gravity, a stiffness matrix without mechanisms, natural frequencies.",
            "Sensors are registered on the members they sit on. The model is calibrated on one wind event and validated on another it has not seen. Every member is then checked to EN 1993-1-1, and the critical wind speeds and warning levels go to an engineer to confirm."],
      main=("earthstate-twin-3d.jpg", "Interactive 3D twin of a synthetic 48 m lattice tower, coloured by member utilisation, with a wind velocity slider, governing leg utilisation and warning level.", "Interactive 3D twin: move the wind velocity and every member is rechecked. Version of 2 November 2026."),
      thumbs=[("earthstate-twin-model.jpg", "Model built from drawing tables: elevation of the tower, model facts, member groups and sections.", "Model from drawing tables, with its self-checks."),
              ("earthstate-twin-sensors.jpg", "Wind and strain records over one event, beside a list of data quality checks.", "Sensor records on the model, with quality checks kept as an audit record.")],
      tags=["Demo data", "Engineers decide", "Patent pending"],
      actions=[("Open the interactive analysis", "demos/structural-twin/analysis-demo.html", True), ("Take the guided tour", "demos/structural-twin/function-tour.html", False)],
      tryline="Both open in the browser. No sign-in, nothing to upload, and no language model is called. In the analysis, drag the wind velocity and turn the 3D model; the tour has ten steps and takes about three minutes.",
      basis=None, papers=["dxf", "corr"],
      limits="A synthetic 48 m tower with synthetic sensor records. Linear elastic analysis; joints, bolts and second-order effects are not modelled. The automated test cases pass; engineer review of those cases is still to be done.",
      demo_url="demos/structural-twin/analysis-demo.html"),
 dict(id="standfast", n="02", field="Overhead lines in storms", name="Standfast",
      q="When a storm crosses a line, which towers should be looked at first?",
      one="A whole line under a storm: each tower analysed under the wind at its own position, and ranked by the margin that remains.",
      body=["Standfast places a whole line on terrain, moves a storm across it and analyses each tower under the wind it would see at its own position. Towers are ranked by the margin that remains.",
            "A collapse sweep shows what follows if one tower fails. Strengthening options are compared side by side, and the report is drafted for an engineer to review."],
      main=("standfast-line-storm.jpg", "Standfast: a line of twenty towers on terrain during a storm scenario, with the tower list, wind warnings and a guided tour panel.", "A storm scenario crossing a 400 kV demo line of twenty towers. Terrain from open data; place labels removed."),
      thumbs=[], tags=["Demo data", "Engineers decide"],
      actions=[], pending="Browser demo in preparation",
      tryline="A browser demo that runs on built-in commands, with no sign-in, is being prepared and will open from this page.",
      basis=None, papers=["grid", "risk"],
      limits="A synthetic line on open terrain data. The storm is a scenario, not a forecast, and the utilisation values are illustrative.",
      demo_url=None),
 dict(id="waterstate", n="03", field="Water pumping stations", name="WaterState",
      q="What maintenance does each failure mode of a pumping station need, and what should be done in the 72 hours before heavy rain?",
      one="Reliability-centred maintenance for a pumping station: failure modes taken through to tasks, and spill risk ranked 72 hours ahead.",
      body=["WaterState applies reliability-centred maintenance to a pumping station. Each failure mode is listed with its effect and scored (FMECA), then taken through the RCM decision questions to a maintenance task, and the path taken is shown.",
            "The AI drafts the reasoning from the work-order history. An engineer accepts or edits each answer, and the sign-off is recorded. A second view combines the rainfall forecast with wet-well level, pump current and vibration to rank the risk of a spill over the next 72 hours."],
      main=("waterstate-risk-72h.jpg", "WaterState: spill probability for three scenarios over the next 72 hours, a planned job before the rain peak, and a 3D pumping station with sensors placed on the model.", "Risk 72 hours ahead, with level, flow, current and vibration sensors placed on the 3D station. Version of 11 November 2026."),
      thumbs=[("waterstate-rcm-programme.jpg", "WaterState: a preventive maintenance programme of seven tasks and the RCM decision tree for a standby pump that fails to start.", "Maintenance programme and the RCM decision tree for one failure mode.")],
      tags=["Demo data", "Engineers decide"],
      actions=[], pending="Browser demo in preparation",
      tryline="A browser demo on one synthetic station is being prepared and will open from this page.",
      basis="This prototype has not been reported in a paper yet. FMECA and the RCM decision logic are established reliability practice. The operations twin and the engineer's sign-off follow two of my papers:",
      papers=["om", "hitl"],
      limits="One synthetic wastewater pumping station. Every value on screen is illustrative; none is a measurement. The prototype has not been run on an operator's own stations.",
      demo_url=None),
 dict(id="facilitynexus", n="04", field="Buildings and estates in operation", name="FacilityNexus",
      q="Can one twin hold the events, the equipment health and the operating knowledge of a building, so that every answer comes with its source?",
      one="A building in operation: events, equipment health and the operations knowledge base on one 3D model.",
      body=["FacilityNexus puts events, work orders, equipment health, energy and the operations knowledge base on one 3D model of the building. Each sensor point sits on the room or the unit it measures, so a complaint about a warm office can be traced to the supply branch behind it.",
            "The assistant answers only from platform data and the operator's own procedures. Conclusions on safety and cost go to a person for review."],
      main=("facilitynexus-space-comfort.jpg", "FacilityNexus: temperature by zone for one floor, complaints with likely causes, a 3D building model with equipment markers, and an assistant panel.", "Space and comfort for one floor, beside the 3D model. Building model from an open dataset (BSI, 2020, CC BY 4.0), converted and simplified."),
      thumbs=[], tags=["Demo data", "Engineers decide"],
      actions=[], pending="Browser demo in preparation",
      tryline="A browser demo with no sign-in is being prepared and will open from this page.",
      basis=None, papers=["ahu", "om"],
      limits="The building model comes from an open dataset; the sensor values, events and work orders are illustrative.",
      demo_url=None),
]
e = html.escape
def paper_li(k):
    t, src, doi, page = P[k]
    title = '<a href="%s">%s</a>' % (page, e(t)) if page else e(t)
    return '<li>%s<span class="src">%s &middot; <a href="https://doi.org/%s" rel="noopener">doi:%s</a></span></li>' % (title, e(src), doi, doi)
def shot(f, alt, cap, cls="proto-shot"):
    return '<a class="%s" href="%s%s"><img src="%s%s" alt="%s" loading="lazy"><span class="cap">%s</span></a>' % (cls, IMG, f, IMG, f, e(alt), e(cap))
def section(p):
    tags = "".join('<span class="tag">%s</span>' % e(t) for t in p["tags"])
    if p.get("pending"): tags += '<span class="tag pending">%s</span>' % e(p["pending"])
    acts = "".join('<a class="btn %s" href="%s">%s</a>' % ("primary" if prim else "secondary", u, e(l)) for l, u, prim in p["actions"])
    acts = '<div class="action-row">%s</div>' % acts if acts else ""
    body = "".join("<p%s>%s</p>" % (' style="margin-top:.7rem"' if i else "", e(b)) for i, b in enumerate(p["body"]))
    thumbs = ""
    if p["thumbs"]:
        thumbs = '<div class="proto-thumbs%s">%s</div>' % (" one" if len(p["thumbs"]) == 1 else "", "".join(shot(*t) for t in p["thumbs"]))
    else:
        thumbs = '<div class="card"><p class="kicker">Try it</p><p>%s</p></div>' % e(p["tryline"])
    tryline = '<p class="small-print">%s</p>' % e(p["tryline"]) if p["thumbs"] else ""
    basis = '<p style="font-size:.9rem;margin-bottom:.8rem">%s</p>' % e(p["basis"]) if p["basis"] else ""
    return '''
        <section class="proto" id="{id}">
            <div class="container">
                <div class="proto-top">
                    {main}
                    <div class="proto-text">
                        <p class="kicker">Prototype {n} &middot; {field}</p>
                        <h2 class="proto-name">{name}</h2>
                        <p class="proto-q">{q}</p>
                        {body}
                        <div class="tag-row">{tags}</div>
                        {acts}
                        {tryline}
                    </div>
                </div>
                <div class="proto-more">
                    {thumbs}
                    <div class="card">
                        <p class="kicker">Published basis</p>
                        {basis}<ul class="paper-list">{papers}</ul>
                        <p class="limits"><strong>Demo data and limits</strong>{limits}</p>
                    </div>
                </div>
            </div>
        </section>'''.format(id=p["id"], n=p["n"], field=e(p["field"]), name=e(p["name"]), q=e(p["q"]), body=body, tags=tags, acts=acts,
                             tryline=tryline, thumbs=thumbs, basis=basis, papers="".join(paper_li(k) for k in p["papers"]),
                             limits=e(p["limits"]), main=shot(*p["main"]))
def jsonld():
    g = [{"@type": "CollectionPage", "@id": BASE + "demos.html#page", "url": BASE + "demos.html", "name": "Research prototypes",
          "description": "Four research prototypes by Dr.-Ing. Daguang Han for the assessment and maintenance of ageing infrastructure, with screenshots, working demonstrations and the papers they are based on.",
          "inLanguage": "en-GB", "author": {"@id": BASE + "#person"}, "about": {"@id": BASE + "#person"},
          "hasPart": [{"@id": BASE + "demos.html#" + p["id"]} for p in PROTOS]}]
    for p in PROTOS:
        d = {"@type": "SoftwareApplication", "@id": BASE + "demos.html#" + p["id"], "name": p["name"],
             "url": BASE + "demos.html#" + p["id"], "description": p["one"],
             "applicationCategory": "Engineering research prototype", "operatingSystem": "Web browser",
             "creativeWorkStatus": "Research prototype", "creator": {"@id": BASE + "#person"}, "author": {"@id": BASE + "#person"},
             "image": BASE + IMG + p["main"][0],
             "citation": [dict({"@type": "ScholarlyArticle", "name": P[k][0], "sameAs": "https://doi.org/" + P[k][2]},
                               **({"url": BASE + P[k][3]} if P[k][3] else {})) for k in p["papers"]]}
        if p["demo_url"]:
            d["subjectOf"] = {"@type": "WebPage", "name": p["name"] + " interactive analysis", "url": BASE + p["demo_url"], "isAccessibleForFree": True}
        g.append(d)
    return json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False, indent=2)

lab = open("tools/demos_lab_section.html", encoding="utf-8").read().strip()
nav = "".join('<a href="#%s">%s</a>' % (p["id"], e(p["name"])) for p in PROTOS) + '<a href="#lab">Laboratory and testbeds</a>'
page = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Four research prototypes by Dr.-Ing. Daguang Han for ageing infrastructure: EarthState Twin, Standfast, WaterState and FacilityNexus, with screenshots, working demonstrations on demo data and the papers they are based on.">
    <title>Research Prototypes and Demos | Daguang Han</title>
    <link rel="canonical" href="https://daguanghan.com/demos.html">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="site.css?v=20261111-proto">
    <script type="application/ld+json">
%s
    </script>
</head>
<body>
    <nav class="site-nav">
        <div class="nav-inner">
            <a href="index.html" class="brand"><span class="brand-mark">DH</span><span>Daguang Han</span></a>
            <ul class="nav-links">
                <li><a href="index.html">Home</a></li>
                <li><a href="research.html">Research</a></li>
                <li><a href="ai-advisory.html">AI &amp; Advisory</a></li>
                <li><a href="projects.html">Projects</a></li>
                <li><a href="impact.html">Impact</a></li>
                <li><a href="publications.html">Publications</a></li>
                <li><a href="experience.html">Experience</a></li>
                <li><a href="demos.html" class="active">Lab &amp; Demos</a></li>
            </ul>
        </div>
    </nav>

    <header class="page-header">
        <div class="container">
            <p class="eyebrow">Research prototypes</p>
            <h1 class="page-title">One method, tried on four kinds of asset</h1>
            <p class="page-subtitle">Each prototype asks the same two questions of a different asset: how much margin is left, and what should be fixed first. The model is built from drawings or a scan, every number comes from a calculation that can be traced to its inputs, and an engineer signs each key step. The AI drafts; engineers decide.</p>
            <div class="proto-nav">%s</div>
        </div>
    </header>

    <main id="software-demos">
        <section class="section compact">
            <div class="container">
                <div class="safe-note">
                    Everything on this page runs on demo data: synthetic structures, generated scenarios or open datasets, labelled as such. Nothing here is a measurement of a real asset or a design check. These are research prototypes that I lead; they are also offered through my independent practice, <a href="https://earthstate.co.uk/" rel="noopener">EarthState</a>.
                </div>
            </div>
        </section>
%s

        %s
    </main>

    <footer class="footer">
        <div class="container">
            <h2>Demos Policy</h2>
            <p>Public demos show methods on demo data only. Restricted data, partner identities and internal platform screens are excluded. The demos on this page need no sign-in, take no uploads and call no language model.</p>
        </div>
    </footer>
</body>
</html>
''' % (jsonld().replace("\n", "\n    "), nav, "".join(section(p) for p in PROTOS), lab)
open("demos.html", "w", encoding="utf-8").write(page)
print("demos.html written:", len(page), "bytes")
