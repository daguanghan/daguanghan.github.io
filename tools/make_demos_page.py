# Builds demos.html for daguanghan.com (Research prototypes).
# Run from the site root:  python3 tools/make_demos_page.py   -> demos.html
# With --draft it writes a local preview to _drafts/demos_v2/ instead (that folder is not published).
# The laboratory section lives in tools/demos_lab_section.html. Screenshots: images/prototypes/.
import json, re, html, sys
DRAFT = "--draft" in sys.argv
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
NEW_IMG = "_drafts/demos_v2/img/" if DRAFT else IMG
def src(f):
    return (NEW_IMG if f.startswith(("earthstate-twin-syn1-", "earthstate-bridges-", "standfast-app-")) else IMG) + f
PROTOS = [
 dict(id="earthstate-twin", n="01", field="Build, through a conversation", case="First case: ageing steel towers. Bridges in development.", name="EarthState Twin",
      q="Can an asset's model, twin and capacity check be built from its drawings and records, with an engineer signing each step?",
      one="Builds an asset's model, digital twin and capacity check from its drawings and records, through a conversation, for an engineer to sign off.",
      body=["EarthState Twin works through a conversation. From an asset's drawings and records it builds a member-level model and runs its own checks before the model is used: equilibrium under gravity, a stiffness matrix without mechanisms, natural frequencies.",
            "Sensors are registered on the members they sit on, the model is calibrated on one event and validated on another it has not seen, and every member is checked to EN 1993-1-1. Each step goes to an engineer to confirm. Transmission towers were the first case; a bridges pack is in development and is shown below."],
      main=("earthstate-twin-syn1-3d.jpg", "EarthState research prototype in model mode: the 3D twin of a synthetic lattice tower fills the screen, with load and deformation controls and the conversation that built it alongside.", "Model mode: the 3D twin of a synthetic tower, beside the conversation that built it. Development build of 14 November 2026."),
      thumbs=[("earthstate-twin-syn1-records.jpg", "Project files listed and classified by type, with the synthetic sensor records flagged as Demo data.", "1. Project files are read and classified by type. Synthetic records are flagged as Demo data."),
              ("earthstate-twin-syn1-model.jpg", "Run trace of three steps beside the 3D twin: geometry from drawing tables, mechanics model with self-check, 3D view.", "2. Drawing tables become a 3D member model, with geometry and mechanics self-checks."),
              ("earthstate-twin-syn1-sensors.jpg", "Calibration and validation steps in the run trace, beside a chart of prediction against measurement labelled Demo data (synthetic).", "3. Gauges and an anemometer are mapped to members. The twin is calibrated on one synthetic storm and validated on the other."),
              ("earthstate-twin-syn1-signoff.jpg", "Audit column listing each key step with its automatic check and evidence level, above a sign-off block signed by a demonstration checking engineer.", "4. Each key step with its automatic checks and evidence level, then the sign-off. The entry shown is a demonstration.")],
      tags=["Research prototype", "Demo data", "Illustrative", "Engineers decide", "UK patent pending"],
      actions=[("Open the interactive analysis", "demos/structural-twin/analysis-demo.html", True), ("Take the guided tour", "demos/structural-twin/function-tour.html", False)],
      tryline="Both open in the browser. No sign-in, nothing to upload, and no language model is called. In the analysis, drag the wind velocity and turn the 3D model; the tour has ten steps and takes about three minutes. The browser demo is an earlier static version; the screenshots on this page come from the current development build.",
      basis=None, papers=["dxf", "corr"],
      limits="A synthetic lattice tower with synthetic sensor records; it stands for no real structure, line or site. The calibration uses records generated by the same model, so it shows that the workflow recovers a known factor. It is not field validation. Linear elastic analysis; joints, bolts and second-order effects are not modelled. The sign-off in the screenshots is a demonstration entry; engineer review of the test cases is still to be done.",
      extra="bridges",
      demo_url="demos/structural-twin/analysis-demo.html"),
 dict(id="standfast", n="02", field="Assets in service", case="First case: overhead lines. Bridges next.", name="Standfast",
      q="For assets in service, how close is each structure to collapse under a hazard, and what should be strengthened or maintained first?",
      one="Looks after assets in service: hazard scenarios across a network, how close each structure is to collapse, and strengthening and maintenance priorities.",
      body=["Standfast looks after assets in service, on a 3D model of the network. It runs a storm or another hazard scenario across the network and analyses each structure under the load it would see at its own position, so the margin before collapse is known structure by structure.",
            "A collapse sweep finds each structure's limit, strengthening options are compared side by side, and the maintenance priorities and the report go to an engineer to review. Overhead lines were the first case; the same approach is being extended to bridges."],
      main=("standfast-app-line-storm.jpg", "Standfast desktop program: a fictitious overhead line of twenty towers on upland terrain, with a storm scenario bar, wind warnings, the tower list and a start panel.", "First case: a storm scenario crossing a fictitious 400 kV line of twenty towers on upland terrain. Place names removed. Team build of 3 November 2026."),
      thumbs=[("standfast-app-tower-analysis.jpg", "Standfast: one tower analysed under wind, with member utilisation painted on the 3D model and a summary panel.", "1. One tower analysed under the wind it sees at its own position, with the result painted on its members."),
              ("standfast-app-member-table.jpg", "Standfast: a table of every member's check for one tower, governing members first, with a provisional-values flag.", "2. Every member's check in one table, governing members first. Provisional code values are flagged."),
              ("standfast-app-collapse-sweep.jpg", "Standfast: a collapse sweep chart for one tower, with a replay button.", "3. Collapse sweep: the wind is raised, failed members are removed, and the wind at which the tower collapses is found."),
              ("standfast-app-line-screening.jpg", "Standfast: every tower of the line ranked in a table by design check and by margin at the storm peak.", "4. The whole line screened: every tower ranked, with its margin at the storm peak."),
              ("standfast-app-retrofit.jpg", "Standfast: a strengthening plan for one tower listing the parts to add and the members strengthened, before and after.", "5. A strengthening plan for the governing members, re-checked after the change."),
              ("standfast-app-engineer-review.jpg", "Standfast: an engineer review record with seven steps, each pending, and buttons to confirm, modify or query.", "6. Engineer review: each step waits for the reviewing engineer to confirm, modify or query. The record shown is unsigned.")],
      tags=["Research prototype", "Demo data", "Illustrative", "Engineers decide", "UK patent pending"],
      actions=[("Open the interactive analysis", "demos/standfast/analysis-demo.html", True), ("Take the guided tour", "demos/standfast/function-tour.html", False)],
      tryline="Both open in the browser. No sign-in, nothing to upload, and no language model is called. In the analysis, turn the terrain, click a tower, play the storm and replay a collapse; the tour takes about three minutes. The browser demo is an earlier static version; the screenshots on this page come from the desktop program.",
      basis=None, papers=["grid", "risk"],
      limits="A fictitious 400 kV line on real open terrain data (Environment Agency LiDAR, OGL v3); the location is not named. The storm is a synthetic scenario, not a forecast. Some code values are provisional and are flagged on screen. The engineer review in the screenshots is a demonstration record and is unsigned.",
      demo_url="demos/standfast/analysis-demo.html"),
 dict(id="waterstate", n="03", field="The method applied to water", case="Pumping stations", name="WaterState",
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
 dict(id="facilitynexus", n="04", field="The method applied to buildings", case="Buildings and estates in operation", name="FacilityNexus",
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
    return '<a class="%s" href="%s"><img src="%s" alt="%s" loading="lazy"><span class="cap">%s</span></a>' % (cls, src(f), src(f), e(alt), e(cap))
BRIDGES = '''
                <div class="proto-more" id="bridges" style="margin-top:2.2rem;scroll-margin-top:90px">
                    <div class="proto-thumbs">%s%s</div>
                    <div class="card">
                        <p class="kicker">EarthState Twin &middot; Bridges &amp; Roads pack &middot; in development</p>
                        <h3>A highway girder bridge, from drawings to traffic load effects, for the engineer to confirm</h3>
                        <p>EarthState Twin research prototype, Bridges &amp; Roads pack (in development), on a public-domain design example of a two-span precast prestressed girder highway bridge. Values from the published drawings fill the bridge workbook, each with its page reference; the platform builds the grillage and computes EN 1991-2 traffic load effects; the engineer confirms each step before the record can be signed.</p>
                        <div class="tag-row"><span class="tag">Research prototype</span><span class="tag">Demo data</span><span class="tag">Illustrative</span><span class="tag pending">In development</span><span class="tag pat">UK patent pending</span></div>
                        <p class="limits"><strong>Demo data and limits</strong>Drawings: FHWA NHI-04-043 design example (public domain). Every other value is illustrative, and the code values are still to be verified. The demonstration stops at traffic load effects and the engineer&#x27;s sign-off.</p>
                    </div>
                </div>'''
def bridges():
    return BRIDGES % (
        shot("earthstate-bridges-d7-model.jpg", "Bridge workbook run trace beside a grillage plan of six skewed girders and deflection lines under permanent loads and two traffic load models.", "The bridge workbook, filled from the published drawings with a page reference for every value, becomes a grillage of six skewed girders."),
        shot("earthstate-bridges-d7-scene.jpg", "The modelled bridge deck in a 3D motorway scene with a special vehicle in the first span and a deflection colour scale.", "The modelled deck in a motorway scene, with a special vehicle in the first span and the live deflection from the grillage."))
def section(p):
    extra = bridges() if p.get("extra") == "bridges" else ""
    tags = "".join('<span class="tag%s">%s</span>' % (" pat" if t == "UK patent pending" else "", e(t)) for t in p["tags"])
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
                        <p class="proto-case">{case}</p>
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
                </div>{extra}
            </div>
        </section>'''.format(extra=extra, id=p["id"], n=p["n"], field=e(p["field"]), name=e(p["name"]), case=e(p["case"]), q=e(p["q"]), body=body, tags=tags, acts=acts,
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
%s    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="site.css?v=20261126-pat">
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
            <h1 class="page-title">Two platforms with different jobs, tried on four kinds of asset</h1>
            <p class="page-subtitle">EarthState Twin builds an asset's model, twin and capacity check from its drawings and records, through a conversation. Standfast looks after assets in service: hazard scenarios, collapse margins, strengthening and maintenance priorities. Towers and overhead lines came first, and bridges are next. WaterState and FacilityNexus apply the same method to pumping stations and to buildings. In all four, every number comes from a calculation that can be traced to its inputs, and an engineer signs each key step. The AI drafts; engineers decide.</p>
            <div class="proto-nav">%s</div>
        </div>
    </header>

    <main id="software-demos">
        <section class="section compact">
            <div class="container">
                <div class="safe-note">
                    Everything on this page runs on demo data: synthetic structures, generated scenarios or open datasets, labelled as such. Nothing here is a measurement of a real asset or a design check. I lead this work. The prototypes are presented together as <a href="https://earthstate.co.uk/" rel="noopener">EarthState</a>, a series of research prototypes developed by my research team.
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
            <p class="ipline">EarthState Twin and Standfast &middot; Research prototype &middot; Core methods are the subject of UK patent applications filed by Dr Daguang Han &middot; Patent pending &middot; &copy; 2026 Daguang Han</p>
        </div>
    </footer>
</body>
</html>
''' % ('    <base href="/">\n    <meta name="robots" content="noindex">\n' if DRAFT else '', jsonld().replace("\n", "\n    "), nav, "".join(section(p) for p in PROTOS), lab)
OUT = "_drafts/demos_v2/demos_preview.html" if DRAFT else "demos.html"
if DRAFT:
    page = page.replace('href="demos/standfast/', 'href="_drafts/demos_v2/standfast/')
open(OUT, "w", encoding="utf-8").write(page)
print(OUT, "written:", len(page), "bytes")
