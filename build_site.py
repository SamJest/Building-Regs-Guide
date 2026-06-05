from __future__ import annotations

import html
import json
import math
import os
import runpy
import shutil
from datetime import date
from pathlib import Path
from textwrap import dedent

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
except Exception:  # pragma: no cover - the bundled runtime includes Pillow
    Image = ImageDraw = ImageFilter = ImageFont = None


ROOT = Path(__file__).resolve().parent
PACK = ROOT / "buildingregsguide_batch_06"
OUTPUT = ROOT / "output"
ASSETS = OUTPUT / "assets"
SITE_DOMAIN = os.environ.get("BRG_DOMAIN", "buildingregsguide.co.uk")
BUILD_ENV = os.environ.get("BRG_ENV", "production").strip().lower()
BASE_URL = os.environ.get("BRG_BASE_URL", f"https://{SITE_DOMAIN}").rstrip("/")
SISTER_URL = "https://ukplanningguide.co.uk"
TODAY = date.today().isoformat()
IS_PREVIEW = BUILD_ENV not in {"production", "prod", "live"}

PHASE_1_PATH = PACK / "43_batch_06_content_priority" / "phase_1_launch_page_list.json"
TOOLS_PATH = PACK / "02_data" / "tool_registry.json"
DOWNLOADS_PATH = PACK / "02_data" / "download_assets_registry.json"
SOURCE_SNAPSHOT_PATH = PACK / "44_batch_06_citations_and_sources" / "current_source_snapshot_2026-06-05.json"
ROUTE_DATA_PATH = PACK / "06_overlay_source" / "source" / "data" / "building_regs_routes.py"
SOURCE_DATA_PATH = PACK / "06_overlay_source" / "source" / "data" / "building_regs_sources.py"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def slug_from_path(path: str) -> str:
    clean = path.strip("/")
    return clean.split("/")[-1] if clean else "home"


def escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def long_description(page: dict) -> str:
    title = page.get("title", "Building regulations guide")
    family = page.get("family", "guide")
    if family == "download":
        return (
            f"Printable {title.lower()} for homeowners to record the likely approval route, "
            "inspection evidence, certificates, source checks and building-control questions before work starts."
        )
    if family == "tool":
        return (
            f"Interactive {title.lower()} for England-first home projects, with route prompts, red flags, "
            "official source links, printable results and local-only save options."
        )
    if family in {"approved_document", "approved_document_hub"}:
        return (
            f"Source-linked homeowner guide to {title}, explaining how the Approved Document may affect common "
            "domestic projects, evidence, inspections and version checks in England."
        )
    if family == "project":
        return (
            f"England-first homeowner guide to {title.lower()}, covering likely building-control routes, "
            "drawings, inspections, certificates, evidence and planning handoffs."
        )
    return (
        f"Plain-English guide to {title.lower()} for homeowners, with building-control route prompts, "
        "certificate evidence, official sources and practical next steps."
    )


def load_data() -> dict:
    routes_module = runpy.run_path(str(ROUTE_DATA_PATH))
    sources_module = runpy.run_path(str(SOURCE_DATA_PATH))
    routes = routes_module["BUILDING_REGS_ROUTES"]
    sources = {}
    for source in sources_module["BUILDING_REGS_SOURCES"]:
        sources[source["id"]] = {
            "source_id": source["id"],
            "name": source["title"],
            "url": source["url"],
            "checked_date": source.get("last_verified", "2026-06-04"),
            "key_points_for_site": [source.get("notes", "")],
            "jurisdiction": source.get("jurisdiction", ""),
        }
    for source in read_json(SOURCE_SNAPSHOT_PATH):
        sources[source["source_id"]] = source
    phase_1 = read_json(PHASE_1_PATH)
    tools = read_json(TOOLS_PATH)
    downloads = read_json(DOWNLOADS_PATH)
    by_path = {route["path"]: route for route in routes}
    by_slug = {route["slug"]: route for route in routes}
    tool_by_path = {tool["path"]: tool for tool in tools}
    download_by_path = {download["path"]: download for download in downloads}
    return {
        "phase_1": phase_1,
        "routes": routes,
        "route_by_path": by_path,
        "route_by_slug": by_slug,
        "tools": tools,
        "tool_by_path": tool_by_path,
        "downloads": downloads,
        "download_by_path": download_by_path,
        "sources": sources,
    }


def ensure_clean_output() -> None:
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / "images").mkdir(parents=True, exist_ok=True)
    (ASSETS / "js").mkdir(parents=True, exist_ok=True)


def make_hero_image() -> None:
    if Image is None:
        return
    width, height = 1800, 980
    img = Image.new("RGB", (width, height), "#f5f1e8")
    draw = ImageDraw.Draw(img)
    bands = [
        ("#17324d", 0, 380),
        ("#2f6f73", 300, 610),
        ("#d7a441", 580, 780),
        ("#eef3ef", 740, height),
    ]
    for color, start, end in bands:
        draw.polygon([(0, start), (width, max(0, start - 180)), (width, end), (0, min(height, end + 180))], fill=color)
    for i in range(14):
        x = 120 + i * 125
        y = 260 + int(math.sin(i / 2) * 55)
        draw.rounded_rectangle((x, y, x + 74, y + 420), radius=6, fill="#ffffff")
        draw.rectangle((x + 16, y + 40, x + 58, y + 382), fill="#dce7e0")
        draw.line((x - 24, y + 420, x + 102, y + 420), fill="#14304a", width=8)
    for i in range(7):
        x = 160 + i * 225
        y = 670 + int(math.cos(i) * 16)
        draw.polygon([(x, y), (x + 95, y - 72), (x + 190, y)], fill="#7c4f2a")
        draw.rectangle((x + 24, y, x + 166, y + 118), fill="#f7f4ec")
        draw.rectangle((x + 72, y + 42, x + 118, y + 118), fill="#2f6f73")
    try:
        font = ImageFont.truetype("arial.ttf", 58)
        small = ImageFont.truetype("arial.ttf", 28)
    except Exception:
        font = small = None
    draw.rounded_rectangle((92, 100, 840, 250), radius=14, fill="#f7f4ec")
    draw.text((130, 128), "Building control route map", fill="#17324d", font=font)
    draw.text((134, 205), "Plans, inspections, certificates and evidence", fill="#2d4b53", font=small)
    img = img.filter(ImageFilter.UnsharpMask(radius=1, percent=115, threshold=3))
    img.save(ASSETS / "images" / "building-control-hero.png", optimize=True)


def write_static_assets() -> None:
    make_hero_image()
    (ASSETS / "site.css").write_text(
        dedent(
            """
            :root{--ink:#17202a;--muted:#59636d;--line:#d9dedb;--paper:#fbfaf6;--soft:#eef3ef;--navy:#17324d;--teal:#2f6f73;--green:#4d7d55;--gold:#d7a441;--red:#9b3d36}
            *{box-sizing:border-box}body{margin:0;font-family:Arial,Helvetica,sans-serif;color:var(--ink);background:var(--paper);line-height:1.58}a{color:#195f66;text-underline-offset:3px}a:hover{color:#0d3d42}.site-header{position:sticky;top:0;z-index:3;background:rgba(251,250,246,.96);border-bottom:1px solid var(--line);backdrop-filter:blur(8px)}.nav{display:flex;align-items:center;justify-content:space-between;gap:18px;max-width:1180px;margin:0 auto;padding:14px 20px}.brand{display:flex;align-items:center;gap:10px;font-weight:800;color:var(--navy);text-decoration:none}.brand-mark{display:grid;place-items:center;width:34px;height:34px;border-radius:6px;background:var(--navy);color:#fff}.nav-links{display:flex;gap:14px;flex-wrap:wrap}.nav-links a{font-size:14px;color:var(--ink);text-decoration:none}.nav-links a:hover{text-decoration:underline}.hero{min-height:74vh;background:linear-gradient(90deg,rgba(15,31,45,.82),rgba(15,31,45,.55),rgba(15,31,45,.18)),url('/assets/images/building-control-hero.png') center/cover;display:flex;align-items:end;color:#fff}.hero-inner{width:min(1180px,100%);padding:68px 20px 56px;margin:0 auto}.eyebrow{font-size:13px;text-transform:uppercase;letter-spacing:0;font-weight:700;color:#e9d18f}.hero h1{font-size:clamp(38px,7vw,74px);line-height:1.02;max-width:880px;margin:10px 0 16px}.hero p{font-size:20px;max-width:760px;margin:0 0 26px}.hero-actions{display:flex;gap:12px;flex-wrap:wrap}.button{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:42px;padding:10px 15px;border-radius:7px;border:1px solid var(--navy);background:var(--navy);color:#fff;text-decoration:none;font-weight:700}.button.secondary{background:#fff;color:var(--navy);border-color:#fff}.button.ghost{background:transparent;color:var(--navy);border-color:var(--line)}main{max-width:1180px;margin:0 auto;padding:28px 20px 64px}.band{padding:34px 0;border-bottom:1px solid var(--line)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr));gap:16px}.card{background:#fff;border:1px solid var(--line);border-radius:8px;padding:18px;min-height:100%}.card h3{font-size:19px;margin:0 0 8px}.card p{color:var(--muted);margin:0 0 12px}.split{display:grid;grid-template-columns:minmax(0,1.55fr) minmax(260px,.75fr);gap:24px;align-items:start}.panel{background:#fff;border:1px solid var(--line);border-radius:8px;padding:20px}.warning{border-left:5px solid var(--gold);background:#fff8df;padding:14px 16px;margin:18px 0}.stop{border-left-color:var(--red);background:#fff0ee}.source-panel{background:#edf4f1;border:1px solid #cadbd4;border-radius:8px;padding:18px;margin-top:28px}.source-panel ul{padding-left:20px}.breadcrumbs{font-size:14px;color:var(--muted);margin-bottom:18px}.page-title{font-size:42px;line-height:1.08;margin:0 0 12px;color:var(--navy)}.lede{font-size:19px;color:#31404a;max-width:850px}.section h2{font-size:26px;margin:30px 0 10px;color:#203648}.checklist li{margin-bottom:8px}.tag{display:inline-flex;border:1px solid var(--line);border-radius:999px;padding:4px 10px;background:var(--soft);font-size:13px}.tool-form{display:grid;gap:14px}.field label{display:block;font-weight:700;margin-bottom:5px}.field select,.field input{width:100%;min-height:42px;border:1px solid #bac3c2;border-radius:6px;padding:8px 10px;background:#fff;color:var(--ink)}.result{display:none;margin-top:18px;border:1px solid #b6cbc2;background:#f2f8f5;border-radius:8px;padding:18px}.result.show{display:block}.download-sheet{background:#fff;border:1px solid var(--line);border-radius:8px;padding:22px}.blank-line{border-bottom:1px solid #7d878a;min-height:30px;margin:6px 0 16px}.site-footer{border-top:1px solid var(--line);padding:26px 20px;color:var(--muted);background:#fff}.footer-inner{max-width:1180px;margin:0 auto;display:flex;gap:20px;justify-content:space-between;flex-wrap:wrap}.search-box{display:flex;gap:8px}.search-box input{flex:1;min-height:42px;border:1px solid #bac3c2;border-radius:6px;padding:8px 10px}.local-note{font-size:14px;color:var(--muted)}@media(max-width:760px){.split{grid-template-columns:1fr}.nav{align-items:flex-start;flex-direction:column}.hero{min-height:68vh}.page-title{font-size:34px}.hero p{font-size:18px}.search-box{flex-direction:column}}@media print{.site-header,.site-footer,.hero-actions,.button,.nav-links{display:none!important}body{background:#fff;color:#000}main{max-width:none;padding:0}.panel,.card,.download-sheet,.source-panel{border-color:#777;break-inside:avoid}.page-title{font-size:28px}.band{padding:16px 0}.source-panel{background:#fff}}
            """
        ).strip(),
        encoding="utf-8",
    )
    (ASSETS / "js" / "site.js").write_text(
        dedent(
            """
            const routeAdvice = {
              full_plans: {
                title: "Likely route: full plans or early building control discussion",
                confidence: "Medium",
                points: ["Useful where structure, fire safety, drainage or energy details need checking before work starts.", "Ask what drawings, calculations and specifications the building control body expects."]
              },
              building_notice: {
                title: "Possible route: building notice",
                confidence: "Medium",
                points: ["Often used for smaller domestic work where the details are straightforward.", "You still need inspections and you carry more risk if details are found unsuitable during the build."]
              },
              competent_person: {
                title: "Possible route: registered competent person",
                confidence: "Medium",
                points: ["Some electrical, heating, window and door work can be self-certified by a registered installer.", "Check the installer registration before work starts and keep the certificate."]
              },
              regularisation: {
                title: "Likely route: regularisation or missing-evidence discussion",
                confidence: "Medium",
                points: ["For completed work with missing approval records, gather photos, invoices, drawings and certificates before contacting building control.", "Regularisation is not automatic and may require opening up work."]
              },
              specialist: {
                title: "Stop route: specialist or BSR guidance first",
                confidence: "High",
                points: ["Do not use a homeowner shortcut for higher-risk buildings, flats, major fire-safety work or unclear structural risk.", "Speak to building control, a competent professional or the relevant regulator before relying on general guidance."]
              }
            };

            function chooseRoute(values) {
              if (values.jurisdiction !== "england" || values.higherRisk === "yes") return "specialist";
              if (values.workStatus === "finished" || values.certificateMissing === "yes") return "regularisation";
              if (values.projectType === "electrical" || values.projectType === "heating" || values.projectType === "windows") return "competent_person";
              if (values.structuralChange === "yes" || values.projectType === "loft" || values.projectType === "extension") return "full_plans";
              return "building_notice";
            }

            function renderResult(form) {
              const values = Object.fromEntries(new FormData(form).entries());
              const key = chooseRoute(values);
              const advice = routeAdvice[key];
              const target = form.parentElement.querySelector(".result");
              const date = new Date().toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });
              target.innerHTML = `
                <h3>${advice.title}</h3>
                <p><strong>Confidence:</strong> ${advice.confidence}. This tool gives a planning prompt for your next conversation; it does not grant approval or replace building control.</p>
                <ul>${advice.points.map(point => `<li>${point}</li>`).join("")}</ul>
                <p><strong>Red flags:</strong> higher-risk building, flat conversion, load-bearing changes, fire escape uncertainty, missing certificates, drainage changes or work outside England.</p>
                <p><strong>Next actions:</strong> save this result, check the official source links on this page, and ask your building control body what they need before work starts.</p>
                <p class="local-note">Generated ${date}. Re-check official guidance before relying on this result.</p>
                <button class="button ghost" type="button" onclick="window.print()">Print</button>
                <button class="button ghost" type="button" data-save-result>Save locally</button>
              `;
              target.classList.add("show");
            }

            document.addEventListener("submit", event => {
              const form = event.target.closest("[data-tool-form]");
              if (!form) return;
              event.preventDefault();
              renderResult(form);
            });

            document.addEventListener("click", event => {
              if (!event.target.matches("[data-save-result]")) return;
              const result = event.target.closest(".result");
              const saved = JSON.parse(localStorage.getItem("brg_saved_results") || "[]");
              saved.push({ savedAt: new Date().toISOString(), text: result.innerText.slice(0, 1600) });
              localStorage.setItem("brg_saved_results", JSON.stringify(saved));
              event.target.textContent = "Saved locally";
            });

            document.addEventListener("DOMContentLoaded", () => {
              const mount = document.querySelector("[data-dashboard]");
              if (mount) {
                const saved = JSON.parse(localStorage.getItem("brg_saved_results") || "[]");
                mount.innerHTML = saved.length ? saved.map((item, index) => `<article class="card"><h3>Saved result ${index + 1}</h3><p class="local-note">${new Date(item.savedAt).toLocaleString("en-GB")}</p><p>${item.text.replace(/[<>&]/g, "")}</p></article>`).join("") : `<p>No saved tool results on this device yet.</p>`;
              }
            });
            """
        ).strip(),
        encoding="utf-8",
    )


def nav_html() -> str:
    links = [
        ("/building-regulations/", "Guides"),
        ("/projects/extensions-building-regulations/", "Projects"),
        ("/approved-documents/", "Approved Documents"),
        ("/tools/building-control-route-checker/", "Tools"),
        ("/downloads/extension-building-regulations-checklist/", "Downloads"),
        ("/dashboard/", "Dashboard"),
        ("/search/", "Search"),
    ]
    return "".join(f'<a href="{href}">{label}</a>' for href, label in links)


def base_html(title: str, description: str, path: str, body: str, schema: dict | None = None, noindex: bool = False) -> str:
    canonical = BASE_URL + (path if path.startswith("/") else f"/{path}")
    robots = '<meta name="robots" content="noindex,follow">' if noindex else ""
    schema_html = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>' if schema else ""
    return dedent(
        f"""
        <!doctype html>
        <html lang="en-GB">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>{escape(title)}</title>
          <meta name="description" content="{escape(description)}">
          {robots}
          <link rel="canonical" href="{escape(canonical)}">
          <link rel="stylesheet" href="/assets/site.css">
          {schema_html}
        </head>
        <body>
          <header class="site-header">
            <nav class="nav" aria-label="Main navigation">
              <a class="brand" href="/"><span class="brand-mark">B</span><span>BuildingRegsGuide</span></a>
              <div class="nav-links">{nav_html()}</div>
            </nav>
          </header>
          {body}
          <footer class="site-footer">
            <div class="footer-inner">
              <p>BuildingRegsGuide is an independent, source-linked guide for homeowners. It does not grant building regulations approval.</p>
              <p><a href="/about/">About</a> / <a href="/legal/">Legal and safety</a></p>
              <p><a href="{SISTER_URL}/">UKPlanningGuide</a> covers planning permission and permitted development.</p>
            </div>
          </footer>
          <script src="/assets/js/site.js"></script>
        </body>
        </html>
        """
    ).strip()


def breadcrumbs(path: str, title: str) -> str:
    if path == "/":
        return ""
    parts = [part for part in path.strip("/").split("/") if part]
    crumbs = ['<a href="/">Home</a>']
    if parts and parts[0] != slug_from_path(path):
        crumbs.append(f'<a href="/{parts[0]}/">{parts[0].replace("-", " ").title()}</a>')
    crumbs.append(escape(title))
    return f'<div class="breadcrumbs">{" / ".join(crumbs)}</div>'


def schema_for(page: dict) -> dict:
    kind = "WebPage"
    if page["family"] == "tool":
        kind = "SoftwareApplication"
    elif page["family"] == "download":
        kind = "DigitalDocument"
    elif page["family"] in {"guide", "approval_route", "project", "approved_document"}:
        kind = "Article"
    return {
        "@context": "https://schema.org",
        "@type": kind,
        "name": page["title"],
        "description": page.get("meta_description") or page.get("summary", ""),
        "url": BASE_URL + page["path"],
        "dateModified": TODAY,
        "publisher": {"@type": "Organization", "name": "BuildingRegsGuide"},
    }


def source_panel(source_ids: list[str], sources: dict) -> str:
    items = []
    for source_id in source_ids:
        source = sources.get(source_id)
        if not source:
            continue
        points = source.get("key_points_for_site") or []
        point_html = "".join(f"<li>{escape(point)}</li>" for point in points[:3] if point)
        items.append(
            f"""
            <li>
              <a href="{escape(source['url'])}">{escape(source['name'])}</a>
              <span class="tag">Checked {escape(source.get('checked_date', '2026-06-05'))}</span>
              <ul>{point_html}</ul>
            </li>
            """
        )
    if not items:
        return ""
    return dedent(
        f"""
        <aside class="source-panel" aria-label="Official source and version panel">
          <h2>Source and version panel</h2>
          <p>This page is England-first unless a nation is named. Re-check the linked source before starting work, appointing trades or submitting an application.</p>
          <ul>{''.join(items)}</ul>
        </aside>
        """
    )


def related_links(page: dict, all_pages: list[dict]) -> str:
    candidates = []
    preferred = [
        "/tools/building-control-route-checker/",
        "/tools/full-plans-vs-building-notice-checker/",
        "/building-regulations/completion-certificate/",
        "/downloads/before-you-start-building-regs-checklist/",
        "/building-regulations/planning-permission-vs-building-regulations/",
    ]
    by_path = {item["path"]: item for item in all_pages}
    for path in preferred:
        if path in by_path and path != page["path"]:
            candidates.append(by_path[path])
    for item in all_pages:
        if item["path"] != page["path"] and item["family"] in {"project", "approval_route", "approved_document"} and item not in candidates:
            candidates.append(item)
        if len(candidates) >= 6:
            break
    cards = "".join(
        f'<article class="card"><h3><a href="{item["path"]}">{escape(item["title"])}</a></h3><p>{escape(item.get("summary", item.get("meta_description", "")))}</p></article>'
        for item in candidates[:6]
    )
    return f'<section class="section"><h2>Next useful checks</h2><div class="grid">{cards}</div></section>'


def page_sections(page: dict) -> str:
    title = page["title"]
    family = page["family"]
    is_planning_overlap = "planning" in title.lower()
    planning_handoff = (
        f'<p>For the planning permission side, use <a href="{SISTER_URL}/">UKPlanningGuide</a>. Keep that separate from building regulations approval and completion evidence.</p>'
        if is_planning_overlap or page.get("needs_cross_site_handoff")
        else ""
    )
    higher_risk = "higher-risk" in title.lower() or "fire" in title.lower()
    warning_class = "warning stop" if higher_risk else "warning"
    warning_text = (
        "If the project involves a higher-risk building, flats, major fire-safety work or unclear structural risk, stop and get specialist building-control advice before relying on a general homeowner route."
        if higher_risk
        else "This guide helps you prepare the right questions. It does not grant approval, replace building control or remove the need for competent design and installation."
    )
    doc_version = ""
    if family == "approved_document" or "Document F" in title or "Document L" in title:
        doc_version = "<p>Approved Documents are guidance for ways to comply in England, not the only possible method. Part F and Part L pages are version-aware because 2026 editions may affect future projects while earlier versions can still matter for older work.</p>"
    return dedent(
        f"""
        <section class="section">
          <h2>Short answer</h2>
          <p>{escape(page.get('summary', 'Use this page to understand the building-control route, evidence and certificate questions for the project.'))}</p>
          <div class="{warning_class}">{escape(warning_text)}</div>
          {planning_handoff}
          {doc_version}
        </section>
        <section class="section">
          <h2>What usually triggers extra checks</h2>
          <ul class="checklist">
            <li>Structural changes, new openings, beams, altered load paths or work that changes fire escape routes.</li>
            <li>New or altered drainage, ventilation, insulation, glazing, heating, electrics or controlled services.</li>
            <li>Work already completed without clear records, inspections or certificates.</li>
            <li>Anything outside ordinary domestic England guidance, including Wales, Scotland, Northern Ireland or higher-risk building routes.</li>
          </ul>
        </section>
        <section class="section">
          <h2>Route options to discuss</h2>
          <p>Most homeowners are comparing full plans, a building notice, competent person self-certification, regularisation for historic work, or an early specialist route. The best fit depends on risk, timing, drawings, installer registration and what building control wants to inspect.</p>
        </section>
        <section class="section">
          <h2>Evidence to keep</h2>
          <ul class="checklist">
            <li>Application references, notices, plans, specifications and structural calculations.</li>
            <li>Inspection dates, site photos before work is covered, installer details and product records.</li>
            <li>Completion certificate, competent person certificate, warranties and handover notes.</li>
            <li>A dated note of which official source/version you checked before work started.</li>
          </ul>
        </section>
        <section class="section">
          <h2>Mistakes to avoid</h2>
          <p>Do not assume planning permission, permitted development or a builder's quote answers the building regulations question. Do not cover up work before required inspections. Do not rely on a certificate claim without checking who issues it and how you will receive a copy.</p>
        </section>
        """
    )


def tool_form(tool: dict) -> str:
    return dedent(
        f"""
        <section class="panel" data-tool="{escape(tool['slug'])}">
          <h2>{escape(tool['title'])}</h2>
          <p>{escape(tool['summary'])}</p>
          <form class="tool-form" data-tool-form>
            <div class="field"><label for="projectType">Project type</label><select id="projectType" name="projectType"><option value="extension">Extension</option><option value="loft">Loft conversion</option><option value="garage">Garage conversion</option><option value="structural">Structural alteration</option><option value="windows">Windows or doors</option><option value="electrical">Electrical work</option><option value="heating">Heating or boiler</option><option value="drainage">Drainage or waste</option></select></div>
            <div class="field"><label for="workStatus">Work status</label><select id="workStatus" name="workStatus"><option value="not_started">Not started</option><option value="in_progress">In progress</option><option value="finished">Finished or historic</option></select></div>
            <div class="field"><label for="structuralChange">Structural change?</label><select id="structuralChange" name="structuralChange"><option value="no">No or not sure</option><option value="yes">Yes</option></select></div>
            <div class="field"><label for="certificateMissing">Missing certificate or approval record?</label><select id="certificateMissing" name="certificateMissing"><option value="no">No</option><option value="yes">Yes</option></select></div>
            <div class="field"><label for="higherRisk">Higher-risk building, flat, or major fire-safety signal?</label><select id="higherRisk" name="higherRisk"><option value="no">No</option><option value="yes">Yes or not sure</option></select></div>
            <div class="field"><label for="jurisdiction">Jurisdiction</label><select id="jurisdiction" name="jurisdiction"><option value="england">England</option><option value="wales">Wales</option><option value="scotland">Scotland</option><option value="ni">Northern Ireland</option></select></div>
            <button class="button" type="submit">Check likely route</button>
          </form>
          <div class="result" aria-live="polite"></div>
        </section>
        """
    )


def download_sheet(download: dict) -> str:
    sections = "".join(
        f"""
        <section class="section">
          <h2>{escape(section)}</h2>
          <div class="blank-line"></div>
          <div class="blank-line"></div>
          <div class="blank-line"></div>
        </section>
        """
        for section in download.get("sections", [])
    )
    return dedent(
        f"""
        <article class="download-sheet">
          <p class="tag">Printable HTML-first asset</p>
          <p>{escape(download.get('summary', 'Printable checklist for building regulations evidence.'))}</p>
          <section class="section">
            <h2>Before you use this sheet</h2>
            <p>Use this as a project file prompt, not as proof that the work is compliant. Fill it in before speaking to building control, your designer, your builder or a registered installer so the conversation starts with the evidence that matters.</p>
            <ul class="checklist">
              <li>Write down the project address, proposed work and whether the work has already started.</li>
              <li>Record who is responsible for drawings, calculations, applications, inspections and certificates.</li>
              <li>Keep copies of source checks, installer registrations, inspection dates, photographs and completion paperwork.</li>
              <li>Re-check the official source links if the project scope changes or work starts later than expected.</li>
            </ul>
          </section>
          <p class="warning">Generated {TODAY}. Re-check official guidance and your building control body's requirements before relying on this asset.</p>
          {sections}
          <section class="section">
            <h2>Handover note</h2>
            <p>At the end of the project, store this sheet with completion certificates, competent person certificates, warranties, product information and any building-control correspondence. It may help when selling, remortgaging or explaining historic work later.</p>
          </section>
          <button class="button ghost" type="button" onclick="window.print()">Print checklist</button>
        </article>
        """
    )


def render_standard_page(page: dict, all_pages: list[dict], sources: dict) -> str:
    source_ids = [page.get("primary_source_id", "govuk_building_regs_approval")]
    body = dedent(
        f"""
        <main>
          {breadcrumbs(page['path'], page['title'])}
          <div class="split">
            <article>
              <h1 class="page-title">{escape(page['title'])}</h1>
              <p class="lede">{escape(page.get('meta_description') or page.get('summary', 'Plain-English building regulations guidance for homeowners.'))}</p>
              {page_sections(page)}
            </article>
            <aside class="panel">
              <h2>Use this page to prepare</h2>
              <ul class="checklist">
                <li>Pick a likely building-control route.</li>
                <li>List drawings, calculations and certificates.</li>
                <li>Plan inspections before work is covered.</li>
                <li>Save evidence for sale or remortgage.</li>
              </ul>
              <a class="button" href="/tools/building-control-route-checker/">Open route checker</a>
            </aside>
          </div>
          {related_links(page, all_pages)}
          {source_panel(source_ids, sources)}
        </main>
        """
    )
    return base_html(page["meta_title"], page["meta_description"], page["path"], body, schema_for(page))


def render_tool_page(page: dict, tool: dict, all_pages: list[dict], sources: dict) -> str:
    source_ids = tool.get("official_source_ids") or [page.get("primary_source_id", "govuk_building_regs_approval")]
    body = dedent(
        f"""
        <main>
          {breadcrumbs(page['path'], page['title'])}
          <h1 class="page-title">{escape(page['title'])}</h1>
          <p class="lede">{escape(tool.get('summary', page.get('summary', '')))}</p>
          <div class="warning">This tool does not grant approval. Results are prompts for your next building-control conversation and do not replace competent professional advice.</div>
          <div class="split">
            {tool_form(tool)}
            <aside class="panel">
              <h2>Result includes</h2>
              <ul class="checklist">
                <li>Likely route and confidence level.</li>
                <li>Red flags including higher-risk building signals.</li>
                <li>Official source links and next actions.</li>
                <li>Print and local save options.</li>
              </ul>
            </aside>
          </div>
          {related_links(page, all_pages)}
          {source_panel(source_ids, sources)}
        </main>
        """
    )
    return base_html(page["title"], page.get("summary", ""), page["path"], body, schema_for(page))


def render_download_page(page: dict, download: dict, all_pages: list[dict], sources: dict) -> str:
    source_ids = download.get("source_ids") or [page.get("primary_source_id", "govuk_building_regs_approval")]
    body = dedent(
        f"""
        <main>
          {breadcrumbs(page['path'], page['title'])}
          <h1 class="page-title">{escape(page['title'])}</h1>
          <p class="lede">{escape(download.get('summary', page.get('summary', '')))}</p>
          {download_sheet(download)}
          {related_links(page, all_pages)}
          {source_panel(source_ids, sources)}
        </main>
        """
    )
    return base_html(page["title"], page.get("meta_description") or long_description(page), page["path"], body, schema_for(page))


def render_homepage(all_pages: list[dict], sources: dict) -> str:
    cards = [
        ("/building-regulations/do-i-need-building-regulations-approval/", "Check if approval is likely", "Start with the approval question before quotes or work."),
        ("/building-regulations/full-plans-vs-building-notice/", "Choose an application route", "Compare full plans, building notice and risk."),
        ("/building-regulations/competent-person-schemes/", "Check certificates", "Know when a registered installer can self-certify."),
        ("/tools/building-control-route-checker/", "Use the route checker", "Get a source-linked next-step prompt."),
    ]
    card_html = "".join(f'<article class="card"><h3><a href="{href}">{title}</a></h3><p>{text}</p></article>' for href, title, text in cards)
    project_cards = "".join(
        f'<article class="card"><h3><a href="{page["path"]}">{escape(page["title"])}</a></h3><p>{escape(page.get("summary", ""))}</p></article>'
        for page in all_pages
        if page["family"] == "project"
    )
    body = dedent(
        f"""
        <section class="hero">
          <div class="hero-inner">
            <div class="eyebrow">England-first building regulations guidance</div>
            <h1>BuildingRegsGuide</h1>
            <p>Check likely building-control routes, evidence, inspections and certificates for home projects without mixing them up with planning permission.</p>
            <div class="hero-actions">
              <a class="button secondary" href="/tools/building-control-route-checker/">Start route checker</a>
              <a class="button ghost" href="/building-regulations/planning-permission-vs-building-regulations/">Planning vs building regs</a>
            </div>
          </div>
        </section>
        <main>
          <section class="band"><div class="grid">{card_html}</div></section>
          <section class="band"><h2>Project starting points</h2><div class="grid">{project_cards}</div></section>
          {source_panel(['govuk_building_regs_approval', 'govuk_competent_person_scheme', 'govuk_approved_documents_collection'], sources)}
        </main>
        """
    )
    page = {"title": "Building regulations checker for UK home projects", "path": "/", "summary": "England-first building regulations route checker and homeowner evidence guide.", "family": "homepage"}
    return base_html(page["title"], page["summary"], "/", body, schema_for(page))


def render_index_page(path: str, title: str, description: str, pages: list[dict], family_filter: set[str], sources: dict) -> str:
    selected = [page for page in pages if page["family"] in family_filter]
    card_html = "".join(
        f'<article class="card"><h3><a href="{page["path"]}">{escape(page["title"])}</a></h3><p>{escape(page.get("summary", page.get("meta_description", "")))}</p></article>'
        for page in selected
    )
    body = dedent(
        f"""
        <main>
          {breadcrumbs(path, title)}
          <h1 class="page-title">{escape(title)}</h1>
          <p class="lede">{escape(description)}</p>
          <section class="section">
            <h2>How to use this section</h2>
            <p>Start with the page closest to your project, then use the linked tool or printable checklist to turn the guidance into questions for your building control body, designer, builder or registered installer.</p>
            <p>Every published page keeps planning permission separate from building regulations approval and links back to official sources so you can re-check the current version before relying on it.</p>
            <p>For a cleaner project file, save the likely route, record who is responsible for each certificate, and keep dated evidence before important work is covered up. If the work includes structure, fire safety, drainage, ventilation, electrics, heating or missing historic paperwork, confirm the route before committing money.</p>
          </section>
          <section class="grid">{card_html}</section>
          {source_panel(['govuk_building_regs_approval'], sources)}
        </main>
        """
    )
    page = {"title": title, "path": path, "summary": description, "family": "hub"}
    return base_html(title, description, path, body, schema_for(page))


def render_about(sources: dict) -> str:
    page = {
        "title": "About BuildingRegsGuide",
        "path": "/about/",
        "summary": "About BuildingRegsGuide, an England-first source-linked guide to building regulations routes, inspections, certificates and homeowner evidence.",
        "family": "guide",
    }
    body = dedent(
        f"""
        <main>
          {breadcrumbs('/about/', 'About')}
          <h1 class="page-title">About BuildingRegsGuide</h1>
          <p class="lede">BuildingRegsGuide helps homeowners separate building regulations approval from planning permission, then prepare better questions for building control, designers, builders and registered installers.</p>
          <section class="section">
            <h2>What the site is for</h2>
            <p>The site turns common domestic projects into route prompts, evidence checklists and source-linked next steps. It focuses on England-first building-control decisions, Approved Documents, inspections, competent person certificates and completion records.</p>
            <p>Where planning permission matters, the site keeps that section brief and points to <a href="{SISTER_URL}/">UKPlanningGuide</a> for the planning side. The two topics can overlap, but they are not the same approval track.</p>
          </section>
          <section class="section">
            <h2>What it cannot do</h2>
            <p>BuildingRegsGuide does not grant approval, certify compliance, design structural work, replace a competent professional, replace an installer, or speak for a local authority or registered building control approver.</p>
            <p>If your project involves higher-risk buildings, flats, unclear structure, major fire-safety questions or work outside England, treat the site as a pointer to specialist advice rather than a route answer.</p>
          </section>
          <section class="section">
            <h2>How content is chosen</h2>
            <p>The launch set starts with the routes homeowners most often need before spending money: extensions, lofts, garage conversions, structural alterations, windows, electrics, heating, drainage, completion evidence and regularisation. Candidate SEO pages stay out of the sitemap until they have enough unique guidance and source support.</p>
            <p>The practical aim is not to publish the largest possible site on day one. It is to publish a smaller set of pages that answer a real next question, connect to a tool or checklist, and make the official source trail visible.</p>
          </section>
          <section class="section">
            <h2>Launch status</h2>
            <p>This starter build is prepared for the domain <strong>{escape(SITE_DOMAIN)}</strong>. Until the domain is purchased and connected, use preview builds for testing and keep production DNS changes separate from content checks.</p>
            <p>Before launch, the site should pass the local validators, load cleanly on a preview URL, and show the same source/version warnings that appear in the generated production output. That gives the domain switch a calmer, more reversible path.</p>
          </section>
          {source_panel(['govuk_building_regs_approval', 'govuk_approved_documents_collection'], sources)}
        </main>
        """
    )
    return base_html(page["title"], page["summary"], page["path"], body, schema_for(page))


def render_legal(sources: dict) -> str:
    page = {
        "title": "Legal and safety",
        "path": "/legal/",
        "summary": "Legal, safety and source-use notes for BuildingRegsGuide, including limits of guidance, higher-risk building warnings and local-only dashboard privacy.",
        "family": "guide",
    }
    body = dedent(
        f"""
        <main>
          {breadcrumbs('/legal/', 'Legal and safety')}
          <h1 class="page-title">Legal and safety</h1>
          <p class="lede">Use BuildingRegsGuide as a preparation aid, not as approval, design advice or legal advice.</p>
          <section class="section">
            <h2>No approval or certification</h2>
            <p>The site does not grant building regulations approval, confirm compliance, issue certificates, approve plans, inspect work or replace your building control body. Tool results are route prompts for your next conversation.</p>
          </section>
          <section class="section">
            <h2>Professional and building-control advice</h2>
            <p>Structural alterations, fire safety, drainage, ventilation, energy performance, electrical work, heating work and historic missing certificates may need competent designers, engineers, installers, surveyors or building control input before work starts.</p>
          </section>
          <section class="section">
            <h2>Jurisdiction and source limits</h2>
            <p>Most launch content is England-first. Wales, Scotland and Northern Ireland use different source material, language and approval routes. Re-check the official source links and version dates before relying on any page.</p>
            <p>Approved Documents are practical guidance on ways to meet building regulations in England. They are not the only possible route to compliance, and version timing can matter. If a page mentions Part F, Part L, fire safety or higher-risk buildings, use the source panel as a prompt to verify the current document before acting.</p>
          </section>
          <section class="section">
            <h2>Higher-risk buildings</h2>
            <p>If a project may involve a higher-risk building, a flat/block, major fire-safety implications or work outside an ordinary homeowner route, stop and use specialist or regulator guidance. The site intentionally avoids turning those cases into a simple DIY answer.</p>
          </section>
          <section class="section">
            <h2>Local-only dashboard privacy</h2>
            <p>The starter dashboard stores saved results in your browser localStorage only. There is no account, no server-side project storage and no backend database in this build.</p>
            <p>Do not enter sensitive personal data into saved notes. Treat local saved results as a convenience for your own device, not as a secure project-management system or a formal building-control record.</p>
          </section>
          <section class="section">
            <h2>Advertising, leads and independence</h2>
            <p>This starter build has no paid lead routing, login wall or contractor recommendation engine. If those features are added later, they should be clearly labelled and kept separate from source-backed regulatory guidance.</p>
          </section>
          {source_panel(['govuk_building_regs_approval', 'govuk_bsr_higher_risk_buildings'], sources)}
        </main>
        """
    )
    return base_html(page["title"], page["summary"], page["path"], body, schema_for(page))


def render_not_found(pages: list[dict], sources: dict) -> str:
    suggestions = "".join(
        f'<article class="card"><h3><a href="{page["path"]}">{escape(page["title"])}</a></h3><p>{escape(page.get("summary", ""))}</p></article>'
        for page in pages[:6]
    )
    body = dedent(
        f"""
        <main>
          <h1 class="page-title">Page not found</h1>
          <p class="lede">This page is not in the current BuildingRegsGuide launch set. Try a core route, project guide, tool or search instead.</p>
          <div class="hero-actions">
            <a class="button" href="/search/">Search the site</a>
            <a class="button ghost" href="/tools/building-control-route-checker/">Open route checker</a>
          </div>
          <section class="section">
            <h2>Useful starting points</h2>
            <div class="grid">{suggestions}</div>
          </section>
          {source_panel(['govuk_building_regs_approval'], sources)}
        </main>
        """
    )
    page = {
        "title": "Page not found",
        "path": "/404.html",
        "summary": "BuildingRegsGuide page not found, with links back to search, route checkers, project guides and source-linked building regulations starting points.",
        "family": "utility",
    }
    return base_html(page["title"], page["summary"], "/404.html", body, schema_for(page), noindex=True)


def render_dashboard(sources: dict) -> str:
    body = dedent(
        f"""
        <main>
          {breadcrumbs('/dashboard/', 'Dashboard')}
          <h1 class="page-title">Building regs project dashboard</h1>
          <p class="lede">Saved tool results appear here on this device only. There is no login, no account and no backend storage in this starter build.</p>
          <div class="warning">Privacy note: saved results use your browser localStorage. Clear your browser data to remove them.</div>
          <section class="grid" data-dashboard></section>
          {source_panel(['govuk_building_regs_approval'], sources)}
        </main>
        """
    )
    page = {"title": "Building regs project dashboard", "path": "/dashboard/", "summary": "Local-only project dashboard for saved building regulations tool results.", "family": "dashboard"}
    return base_html(page["title"], page["summary"], page["path"], body, schema_for(page))


def render_search(pages: list[dict], sources: dict) -> str:
    data = json.dumps(
        [{"title": page["title"], "path": page["path"], "summary": page.get("summary", page.get("meta_description", "")), "family": page["family"]} for page in pages],
        ensure_ascii=False,
    )
    body = dedent(
        f"""
        <main>
          {breadcrumbs('/search/', 'Search')}
          <h1 class="page-title">Search BuildingRegsGuide</h1>
          <p class="lede">Search launch pages, tools and printable checklists.</p>
          <div class="search-box"><input id="site-search" type="search" placeholder="Try loft, certificate, drainage or Part L"><button class="button" type="button" id="search-button">Search</button></div>
          <section class="grid" id="search-results"></section>
          <script type="application/json" id="search-data">{data}</script>
          <script>
            const data = JSON.parse(document.getElementById('search-data').textContent);
            const results = document.getElementById('search-results');
            const input = document.getElementById('site-search');
            function runSearch() {{
              const q = input.value.trim().toLowerCase();
              const matches = data.filter(item => !q || (item.title + ' ' + item.summary + ' ' + item.family).toLowerCase().includes(q)).slice(0, 24);
              results.innerHTML = matches.map(item => `<article class="card"><h3><a href="${{item.path}}">${{item.title}}</a></h3><p>${{item.summary}}</p></article>`).join('');
            }}
            document.getElementById('search-button').addEventListener('click', runSearch);
            input.addEventListener('input', runSearch);
            runSearch();
          </script>
          {source_panel(['govuk_building_regs_approval'], sources)}
        </main>
        """
    )
    page = {
        "title": "Search BuildingRegsGuide",
        "path": "/search/",
        "summary": "Search BuildingRegsGuide launch pages, project guides, tools, Approved Document explainers and printable building regulations checklists.",
        "family": "search",
    }
    return base_html(page["title"], page["summary"], page["path"], body, schema_for(page))


def write_page(path: str, content: str) -> None:
    if path == "/":
        target = OUTPUT / "index.html"
    else:
        target = OUTPUT / path.strip("/") / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def enrich_pages(data: dict) -> list[dict]:
    pages = []
    for candidate in data["phase_1"]:
        base = data["route_by_path"].get(candidate["path"], {})
        page = {**candidate, **base}
        page.setdefault("slug", slug_from_path(page["path"]))
        if page.get("family") == "approved_document_hub" and not page.get("meta_title"):
            page["meta_title"] = f"{page['title']} guide"
        page.setdefault("meta_title", page["title"])
        if not page.get("summary") or len(page.get("summary", "")) < 70:
            page["summary"] = long_description(page)
        if not page.get("meta_description") or len(page.get("meta_description", "")) < 70:
            page["meta_description"] = long_description(page)
        page.setdefault("primary_source_id", candidate.get("primary_source_id", "govuk_building_regs_approval"))
        pages.append(page)
    return pages


def build() -> dict:
    data = load_data()
    ensure_clean_output()
    write_static_assets()
    pages = enrich_pages(data)
    published = []

    for page in pages:
        if page["path"] == "/":
            html_text = render_homepage(pages, data["sources"])
        elif page["family"] == "tool":
            html_text = render_tool_page(page, data["tool_by_path"].get(page["path"], {}), pages, data["sources"])
        elif page["family"] == "download":
            html_text = render_download_page(page, data["download_by_path"].get(page["path"], {}), pages, data["sources"])
        else:
            html_text = render_standard_page(page, pages, data["sources"])
        write_page(page["path"], html_text)
        published.append(page)

    extra_pages = [
        ("/projects/", "Building regulations by project", "Project guides for extensions, lofts, garage conversions, outbuildings, structural work, services, drainage and certificate evidence.", {"project"}),
        ("/tools/", "Building regulations tools", "Interactive route, certificate, inspection and Approved Document tools.", {"tool"}),
        ("/downloads/", "Building regulations downloads", "Printable checklists and evidence sheets for homeowner project files.", {"download"}),
        ("/approved-documents/", "Approved Documents for home projects", "Source-linked England Approved Document starting points for common domestic work.", {"approved_document", "approved_document_hub"}),
    ]
    for path, title, description, families in extra_pages:
        write_page(path, render_index_page(path, title, description, pages, families, data["sources"]))
        published.append({"path": path, "title": title, "summary": description, "family": "hub"})
    write_page("/dashboard/", render_dashboard(data["sources"]))
    published.append({"path": "/dashboard/", "title": "Building regs project dashboard", "summary": "Local-only saved tool result dashboard.", "family": "dashboard"})
    write_page("/about/", render_about(data["sources"]))
    published.append({"path": "/about/", "title": "About BuildingRegsGuide", "summary": "About this source-linked building regulations guide.", "family": "guide"})
    write_page("/legal/", render_legal(data["sources"]))
    published.append({"path": "/legal/", "title": "Legal and safety", "summary": "Legal, safety and privacy notes for this building regulations guide.", "family": "guide"})
    write_page("/search/", render_search(published, data["sources"]))
    published.append({"path": "/search/", "title": "Search BuildingRegsGuide", "summary": "Search launch pages, tools and downloads.", "family": "search"})
    (OUTPUT / "404.html").write_text(render_not_found(pages, data["sources"]), encoding="utf-8")

    search_index = [
        {"title": page["title"], "path": page["path"], "summary": page.get("summary", ""), "family": page["family"]}
        for page in published
    ]
    (OUTPUT / "search-index.json").write_text(json.dumps(search_index, indent=2, ensure_ascii=False), encoding="utf-8")
    sitemap_urls = "\n".join(
        f"  <url><loc>{BASE_URL}{page['path']}</loc><lastmod>{TODAY}</lastmod></url>" for page in published
    )
    (OUTPUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap_urls}\n</urlset>\n', encoding="utf-8")
    robots = f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n"
    if IS_PREVIEW:
        robots = "User-agent: *\nDisallow: /\n"
    (OUTPUT / "robots.txt").write_text(robots, encoding="utf-8")
    if not IS_PREVIEW:
        (OUTPUT / "CNAME").write_text(f"{SITE_DOMAIN}\n", encoding="utf-8")
    (OUTPUT / ".nojekyll").write_text("", encoding="utf-8")
    report = {
        "generated_at": TODAY,
        "build_env": BUILD_ENV,
        "base_url": BASE_URL,
        "domain": SITE_DOMAIN,
        "published_count": len(published),
        "phase_1_count": len(pages),
        "extra_navigation_pages": ["/projects/", "/tools/", "/downloads/", "/approved-documents/", "/dashboard/", "/search/"],
        "draft_noindex_count": 0,
        "blocked": [],
        "notes": [
            "Built from the batch 6 phase-1 launch queue.",
            "Tool results are client-side prompts and never claim to grant approval.",
            "Sitemap includes published/indexable pages only.",
            "Dashboard is localStorage only; no backend is implemented.",
        ],
    }
    (OUTPUT / "BUILD_REPORT.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (OUTPUT / "BUILD_REPORT.md").write_text(
        "# BuildingRegsGuide starter build report\n\n"
        f"- Generated: {TODAY}\n"
        f"- Published pages: {len(published)}\n"
        f"- Phase 1 routes: {len(pages)}\n"
        "- Draft/noindex pages: 0\n"
        "- Blocked pages: none in this starter pass\n"
        f"- Build environment: {BUILD_ENV}\n"
        f"- Base URL: {BASE_URL}\n"
        f"- Domain: {SITE_DOMAIN}\n"
        "- Included: generated pages, tools, downloads, sitemap, robots, search index, schema, source panels, print CSS, 404 page, legal page and local-only dashboard.\n",
        encoding="utf-8",
    )
    return report


if __name__ == "__main__":
    result = build()
    print(json.dumps(result, indent=2))
