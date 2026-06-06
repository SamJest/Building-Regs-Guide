from __future__ import annotations

import html
import json
import math
import os
import re
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
DOWNLOAD_MARKDOWN_DIR = PACK / "23_batch_04_download_assets" / "full_asset_markdown"

DOWNLOAD_MARKDOWN_MAP = {
    "extension-building-regulations-checklist": "extension-building-control-prep-pack.md",
    "loft-conversion-building-regulations-checklist": "loft-conversion-fire-and-structure-checklist.md",
    "garage-conversion-building-regulations-checklist": "garage-conversion-building-regs-pack.md",
    "building-notice-vs-full-plans-worksheet": "building-control-route-decision-sheet.md",
    "completion-certificate-record-sheet": "completion-certificate-evidence-folder.md",
    "competent-person-certificate-checklist": "competent-person-certificate-tracker.md",
    "inspection-stage-record-sheet": "inspection-stage-checklist.md",
    "structural-calculations-briefing-sheet": "structural-calculation-record-sheet.md",
    "drainage-and-waste-checklist": "drainage-inspection-prep-sheet.md",
    "windows-and-doors-certificate-checklist": "windows-and-doors-certificate-checklist.md",
    "electrical-work-evidence-checklist": "electrician-part-p-certificate-request.md",
    "heating-boiler-certificate-checklist": "gas-boiler-paperwork-request.md",
    "regularisation-evidence-pack": "regularisation-evidence-gatherer.md",
    "approved-document-router-summary": "approved-document-router-printout.md",
    "building-control-phone-call-script": "building-control-contact-log.md",
    "builder-quote-building-regs-questions": "installer-quote-building-regs-questions.md",
    "sale-remortgage-proof-folder": "home-sale-building-regs-document-pack.md",
    "garden-room-building-regs-checklist": "garden-room-building-regs-risk-checklist.md",
    "load-bearing-wall-removal-checklist": "load-bearing-wall-removal-evidence-checklist.md",
    "rooflight-building-regs-checklist": "rooflight-building-regs-checklist.md",
}

PROJECT_PROFILES = {
    "extensions": {
        "answer": "Most extensions need building regulations approval even when the planning route is permitted development. The key early decision is usually full plans versus building notice, with structure, foundations, insulation, drainage and ventilation settled before work is covered.",
        "triggers": ["New foundations or altered ground levels", "Steel beams, roof structure or widened openings", "Drainage runs, public sewer proximity or new bathrooms", "Part L energy details and Part F ventilation strategy"],
        "route": "Use full plans when you want detail checked before work starts, when the builder needs clear specifications, or where structure and energy details are not simple. A building notice may fit smaller straightforward domestic work, but it leaves more detail to be resolved on site.",
        "evidence": ["Approved drawings/specification", "Structural calculations and beam details", "Inspection records for excavations, drains, insulation and completion", "Completion certificate and installer commissioning records"],
    },
    "loft-conversions": {
        "answer": "A loft conversion is normally a building regulations project because it affects structure, stairs, insulation, fire safety, escape routes and ventilation. Treat fire strategy and structural design as early design questions, not end-of-job paperwork.",
        "triggers": ["New floor structure or steel beams", "New stairs and protected escape route questions", "Roof windows, dormers, insulation and ventilation", "Fire doors, smoke alarms and separation from lower floors"],
        "route": "Full plans are usually the safer route because lofts contain several linked design issues. Ask building control what drawings, sections, calculations and fire-safety details they expect before quotes are finalised.",
        "evidence": ["Structural engineer calculations", "Stair and headroom drawings", "Fire safety specification and alarm records", "Insulation/ventilation evidence before plasterboard covers work"],
    },
    "garage-conversions": {
        "answer": "A garage conversion commonly needs building regulations approval because a storage space becomes habitable accommodation. Damp, insulation, ventilation, fire separation, structure and floor build-up are the usual issues.",
        "triggers": ["Raising or insulating the floor", "Replacing the garage door with a wall/window", "Adding heating, electrics, drainage or ventilation", "Changing fire separation to the house or boundary"],
        "route": "Discuss full plans where damp-proofing, wall build-up or structure is unclear. A building notice may only suit very straightforward conversions where the specification is already settled.",
        "evidence": ["Existing garage photos", "Floor, wall and roof insulation details", "Ventilation and heating records", "Completion certificate and electrical certificates"],
    },
    "outbuildings": {
        "answer": "Some small detached outbuildings can be exempt, but size, sleeping use, electrics, drainage, boundary position and fire risk can pull the work back into building regulations territory.",
        "triggers": ["Sleeping accommodation or regular habitable use", "Large floor area or close boundary position", "Electrical supply, heating or drainage", "Combustible construction near boundaries"],
        "route": "Use the route checker before ordering the building. If it includes services or habitable use, get building control input early rather than treating it as a shed.",
        "evidence": ["Supplier specification", "Electrical certificate if installed", "Foundation/base details", "Photos showing distance to boundaries and service routes"],
    },
    "garden-rooms": {
        "answer": "A garden room can look simple but still raise building regulations questions if it is large, serviced, close to boundaries, heated, drained or used like accommodation.",
        "triggers": ["Insulated or heated office use", "Electrical circuit from the house", "Toilet, sink or drainage connections", "Boundary/fire spread concerns"],
        "route": "Confirm whether the building is exempt before purchase. If services or habitable use are included, ask whether building control or registered installers need to be involved.",
        "evidence": ["Supplier drawings and fire classification", "Electrical installation certificate", "Drainage records if connected", "Photos of base, boundaries and service trenches"],
    },
    "structural-alterations": {
        "answer": "Structural alterations usually need building control involvement because they affect how loads move through the building. Do not rely on a builder's verbal assurance for beams, supports or openings.",
        "triggers": ["Removing or altering a load-bearing wall", "Forming a new opening", "Changing roof/floor structure", "Chimney breast or support alterations"],
        "route": "Get structural calculations before work starts and agree inspection stages with building control. Full plans usually gives more certainty for non-trivial structural work.",
        "evidence": ["Structural calculations", "Beam padstone and bearing details", "Photos before boxing-in", "Inspection notes and completion certificate"],
    },
    "removing-load-bearing-wall": {
        "answer": "Removing a load-bearing wall is a building regulations and structural design issue. The approval question is not just whether a beam is present, but whether the load path, bearings, fire protection and installation are suitable.",
        "triggers": ["Wall supports floors, roof or chimney", "Opening is widened or supports are changed", "Steel beam or lintel is installed", "Work is hidden before inspection"],
        "route": "Use a structural engineer and agree building-control inspection points before demolition. Full plans is often the cleaner route for evidence and sale paperwork.",
        "evidence": ["Engineer calculations", "Beam delivery/marking evidence", "Bearing and padstone photos", "Completion certificate"],
    },
    "windows-doors": {
        "answer": "Replacement windows and doors may be covered by a competent person scheme, but you still need evidence. New openings or changed structure can need building control beyond installer self-certification.",
        "triggers": ["Replacement glazing", "Widened openings or new lintels", "Escape window changes", "Thermal performance and safety glazing"],
        "route": "Use a registered installer for covered replacement work, or contact building control where structural openings or unusual changes are involved.",
        "evidence": ["Installer registration details", "Competent person certificate", "Glazing/product specification", "Photos of any structural opening work"],
    },
    "electrical-work": {
        "answer": "Some domestic electrical work is notifiable under Part P. Registered electricians can often self-certify covered work, but homeowners should still check registration and keep certificates.",
        "triggers": ["New circuits", "Consumer unit changes", "Work in bathrooms or special locations", "Electrical work as part of a larger project"],
        "route": "Use a registered electrician where possible. If the installer cannot self-certify notifiable work, ask building control what notification route applies before work starts.",
        "evidence": ["Electrical installation certificate", "Building regulations compliance certificate if applicable", "Installer scheme details", "Circuit schedule and test results"],
    },
    "boiler-heating": {
        "answer": "Boiler, heating and heat-pump work often relies on registered installer certification. The building regulations value is in checking who certifies the work and keeping the handover records.",
        "triggers": ["New or replacement boiler", "Heating system changes", "Heat pump installation", "Flue, ventilation or commissioning requirements"],
        "route": "Use an appropriately registered installer and confirm what certificate or commissioning record will be issued. Building control may be needed if the work is outside self-certification.",
        "evidence": ["Installer registration", "Commissioning certificate", "Benchmark or handover record", "Product manuals and warranty details"],
    },
    "drainage-waste": {
        "answer": "Drainage and waste changes can need early building control input because defects may be hidden below floors, outside trenches or behind finishes.",
        "triggers": ["New bathrooms, kitchens or utility rooms", "Moved soil pipes or waste runs", "Work near public sewers", "New inspection chambers or altered falls"],
        "route": "Ask building control what inspection is needed before trenches or pipework are covered. Public sewer work may also need water company checks.",
        "evidence": ["Drainage layout sketch", "Photos before backfill/cover-up", "Inspection notes", "Product and test records"],
    },
}

APPROVED_DOCUMENT_PROFILES = {
    "approved-document-a-structure": ("Structure", ["Foundations", "Beams and lintels", "Load-bearing walls", "Roof/floor changes"]),
    "approved-document-b-fire-safety": ("Fire safety", ["Escape routes", "Fire doors", "Smoke alarms", "Separation and spread of fire"]),
    "approved-document-f-ventilation": ("Ventilation", ["Bathrooms/kitchens", "New habitable rooms", "Extractor fans", "Background ventilation"]),
    "approved-document-h-drainage-waste": ("Drainage and waste", ["Foul drainage", "Rainwater", "Pipe gradients", "Inspection chambers"]),
    "approved-document-k-falling-collision-impact": ("Protection from falling, collision and impact", ["Stairs", "Guarding", "Glazing safety", "Headroom"]),
    "approved-document-l-conservation-fuel-power": ("Conservation of fuel and power", ["Insulation", "Windows and doors", "Heating efficiency", "Thermal bridging"]),
    "approved-document-p-electrical-safety": ("Electrical safety", ["Notifiable work", "Special locations", "Consumer units", "Certificates"]),
}

SISTER_PROJECT_LINKS = {
    "extensions": {
        "url": f"{SISTER_URL}/",
        "label": "check the planning route first",
        "note": "Extensions often have a separate planning or permitted development question before building control evidence.",
    },
    "loft-conversions": {
        "url": f"{SISTER_URL}/england/projects/dormer-extensions/",
        "label": "planning permission may still matter for dormers",
        "note": "Roof shape, dormers, conservation areas and external changes can make the planning track relevant.",
    },
    "outbuildings": {
        "url": f"{SISTER_URL}/",
        "label": "check permitted development and planning limits",
        "note": "Outbuildings can raise planning issues around size, position, use and protected areas before building regs evidence.",
    },
    "garden-rooms": {
        "url": f"{SISTER_URL}/",
        "label": "check the garden building planning route",
        "note": "A garden room may be simple for building regs but still planning-sensitive if use, size or location changes.",
    },
    "boiler-heating": {
        "url": f"{SISTER_URL}/",
        "label": "check planning-sensitive external equipment",
        "note": "External equipment, flues, heat pumps and protected buildings can need a planning check as well as certification.",
    },
    "windows-doors": {
        "url": f"{SISTER_URL}/",
        "label": "check planning constraints for visible changes",
        "note": "Listed buildings, conservation areas and material external changes can sit on the planning side.",
    },
}

BRIDGE_CARDS = [
    {
        "project": "Extensions",
        "building": "/projects/extensions-building-regulations/",
        "planning": f"{SISTER_URL}/",
        "building_text": "Foundations, structure, insulation, drainage, ventilation, inspections and completion evidence.",
        "planning_text": "Permitted development limits, neighbour-sensitive design, conservation constraints and local planning context.",
    },
    {
        "project": "Loft conversions and dormers",
        "building": "/projects/loft-conversion-building-regulations/",
        "planning": f"{SISTER_URL}/england/projects/dormer-extensions/",
        "building_text": "Stairs, structure, fire safety, insulation, ventilation, smoke alarms and completion paperwork.",
        "planning_text": "Dormers, roof extensions, front roof slopes, conservation areas and external appearance.",
    },
    {
        "project": "Outbuildings and garden rooms",
        "building": "/projects/garden-room-building-regulations/",
        "planning": f"{SISTER_URL}/",
        "building_text": "Exemption checks, electrics, heating, drainage, fire spread and evidence before services are covered.",
        "planning_text": "Size, position, incidental use, sleeping use, boundaries and protected-area planning limits.",
    },
    {
        "project": "Driveways, drainage and access",
        "building": "/projects/drainage-waste-building-regulations/",
        "planning": f"{SISTER_URL}/england/projects/driveways/",
        "building_text": "Drainage layout, waste connections, inspection chambers, soakaways and building-control inspection records.",
        "planning_text": "Permeable surfacing, highway access, dropped kerbs and local planning constraints.",
    },
]

EXPANSION_PAGES = [
    {
        "path": "/planning-and-building-regulations/",
        "title": "Planning and building regulations project map",
        "summary": "A bridge between BuildingRegsGuide and UKPlanningGuide showing which project questions belong to planning and which belong to building control.",
        "family": "guide",
        "primary_source_id": "govuk_building_regs_approval",
        "kind": "bridge",
    },
    {
        "path": "/evidence/building-regulations-documents-to-keep/",
        "title": "Building regulations documents to keep",
        "summary": "Checklist of building regulations paperwork, inspection records, certificates and project evidence to keep for sale, remortgage and future work.",
        "family": "evidence",
        "primary_source_id": "govuk_building_regs_approval",
        "kind": "evidence",
        "documents": ["Application reference or initial notice", "Approved plans or building notice acknowledgement", "Structural calculations and drawings", "Inspection records and dated site photos", "Competent person certificates", "Completion certificate or final acceptance", "Product data, commissioning records and warranties"],
        "download": "/downloads/sale-remortgage-proof-folder/",
    },
    {
        "path": "/evidence/missing-building-regulations-certificate/",
        "title": "Missing building regulations certificate",
        "summary": "What to gather when a completion certificate, competent person certificate or historic building-control evidence is missing.",
        "family": "evidence",
        "primary_source_id": "govuk_how_to_apply",
        "kind": "evidence",
        "documents": ["Project dates and address", "Builder/designer/installer invoices", "Photos showing hidden work if available", "Electrical, heating or glazing certificates", "Planning decision or lawful development certificate if relevant", "Surveyor notes and conveyancing queries", "Building control correspondence"],
        "download": "/downloads/regularisation-evidence-pack/",
    },
    {
        "path": "/compare/full-plans-building-notice-regularisation/",
        "title": "Full plans, building notice or regularisation?",
        "summary": "Compare the three common building-control routes, when each may fit, and what evidence the homeowner should keep.",
        "family": "comparison",
        "primary_source_id": "govuk_how_to_apply",
        "kind": "comparison",
    },
    {
        "path": "/questions/do-i-need-building-regulations-for-loft-conversion/",
        "title": "Do I need building regulations for a loft conversion?",
        "summary": "Answer-first loft conversion building regulations guide covering structure, stairs, fire safety, insulation, ventilation, inspections and planning handoffs.",
        "family": "programmatic_question_page",
        "primary_source_id": "govuk_building_regs_approval",
        "kind": "question",
        "parent": "/projects/loft-conversion-building-regulations/",
        "project_slug": "loft-conversions",
    },
    {
        "path": "/questions/what-documents-do-i-need-for-extension-building-regulations/",
        "title": "What documents do I need for extension building regulations?",
        "summary": "Extension paperwork checklist covering drawings, calculations, inspections, certificates, drainage records and completion evidence.",
        "family": "programmatic_question_page",
        "primary_source_id": "govuk_building_regs_approval",
        "kind": "question",
        "parent": "/projects/extensions-building-regulations/",
        "project_slug": "extensions",
    },
]


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
    if family in {"project", "programmatic_question_page"}:
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
            *{box-sizing:border-box}body{margin:0;font-family:Arial,Helvetica,sans-serif;color:var(--ink);background:var(--paper);line-height:1.58}a{color:#195f66;text-underline-offset:3px}a:hover{color:#0d3d42}.site-header{position:sticky;top:0;z-index:3;background:rgba(251,250,246,.96);border-bottom:1px solid var(--line);backdrop-filter:blur(8px)}.nav{display:flex;align-items:center;justify-content:space-between;gap:18px;max-width:1180px;margin:0 auto;padding:14px 20px}.brand{display:flex;align-items:center;gap:10px;font-weight:800;color:var(--navy);text-decoration:none}.brand-mark{display:grid;place-items:center;width:34px;height:34px;border-radius:6px;background:var(--navy);color:#fff}.nav-links{display:flex;gap:14px;flex-wrap:wrap}.nav-links a{font-size:14px;color:var(--ink);text-decoration:none}.nav-links a:hover{text-decoration:underline}.hero{min-height:74vh;background:linear-gradient(90deg,rgba(15,31,45,.82),rgba(15,31,45,.55),rgba(15,31,45,.18)),url('/assets/images/building-control-hero.png') center/cover;display:flex;align-items:end;color:#fff}.hero-inner{width:min(1180px,100%);padding:68px 20px 56px;margin:0 auto}.eyebrow{font-size:13px;text-transform:uppercase;letter-spacing:0;font-weight:700;color:#e9d18f}.hero h1{font-size:clamp(38px,7vw,74px);line-height:1.02;max-width:880px;margin:10px 0 16px}.hero p{font-size:20px;max-width:760px;margin:0 0 26px}.hero-actions{display:flex;gap:12px;flex-wrap:wrap}.button{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:42px;padding:10px 15px;border-radius:7px;border:1px solid var(--navy);background:var(--navy);color:#fff;text-decoration:none;font-weight:700}.button.secondary{background:#fff;color:var(--navy);border-color:#fff}.button.ghost{background:transparent;color:var(--navy);border-color:var(--line)}main{max-width:1180px;margin:0 auto;padding:28px 20px 64px}.band{padding:34px 0;border-bottom:1px solid var(--line)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr));gap:16px}.card{background:#fff;border:1px solid var(--line);border-radius:8px;padding:18px;min-height:100%}.card h3{font-size:19px;margin:0 0 8px}.card p{color:var(--muted);margin:0 0 12px}.split{display:grid;grid-template-columns:minmax(0,1.55fr) minmax(260px,.75fr);gap:24px;align-items:start}.panel{background:#fff;border:1px solid var(--line);border-radius:8px;padding:20px}.warning{border-left:5px solid var(--gold);background:#fff8df;padding:14px 16px;margin:18px 0}.stop{border-left-color:var(--red);background:#fff0ee}.source-panel{background:#edf4f1;border:1px solid #cadbd4;border-radius:8px;padding:18px;margin-top:28px}.source-panel ul{padding-left:20px}.breadcrumbs{font-size:14px;color:var(--muted);margin-bottom:18px}.page-title{font-size:42px;line-height:1.08;margin:0 0 12px;color:var(--navy)}.lede{font-size:19px;color:#31404a;max-width:850px}.section h2{font-size:26px;margin:30px 0 10px;color:#203648}.checklist li{margin-bottom:8px}.tag{display:inline-flex;border:1px solid var(--line);border-radius:999px;padding:4px 10px;background:var(--soft);font-size:13px}.tool-form{display:grid;gap:14px}.field label{display:block;font-weight:700;margin-bottom:5px}.field select,.field input{width:100%;min-height:42px;border:1px solid #bac3c2;border-radius:6px;padding:8px 10px;background:#fff;color:var(--ink)}.result{display:none;margin-top:18px;border:1px solid #b6cbc2;background:#f2f8f5;border-radius:8px;padding:18px}.result.show{display:block}.download-sheet{background:#fff;border:1px solid var(--line);border-radius:8px;padding:22px}.blank-line{border-bottom:1px solid #7d878a;min-height:30px;margin:6px 0 16px}.site-footer{border-top:1px solid var(--line);padding:26px 20px;color:var(--muted);background:#fff}.footer-inner{max-width:1180px;margin:0 auto;display:flex;gap:20px;justify-content:space-between;flex-wrap:wrap}.search-box{display:flex;gap:8px}.search-box input{flex:1;min-height:42px;border:1px solid #bac3c2;border-radius:6px;padding:8px 10px}.local-note{font-size:14px;color:var(--muted)}.faq-item{border-top:1px solid var(--line);padding:12px 0}.faq-item summary{font-weight:700;cursor:pointer}.table-wrap{overflow-x:auto;margin:16px 0}.evidence-table{width:100%;border-collapse:collapse;background:#fff}.evidence-table th,.evidence-table td{border:1px solid var(--line);padding:8px;text-align:left;vertical-align:top}.evidence-table th{background:var(--soft)}.printable-content h2:first-child{margin-top:18px}.dashboard-actions{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0}.form-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px}.mini-input{width:100%;min-height:40px;border:1px solid #bac3c2;border-radius:6px;padding:8px;background:#fff}.handoff{background:#f4f8f7;border:1px solid #c9deda;border-radius:8px;padding:18px;margin:22px 0}.handoff h2{margin-top:0}.handoff-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}.handoff-card{background:#fff;border:1px solid var(--line);border-radius:8px;padding:14px}.route-table{width:100%;border-collapse:collapse;background:#fff}.route-table th,.route-table td{border:1px solid var(--line);padding:10px;text-align:left;vertical-align:top}.route-table th{background:var(--soft)}.mini-nav{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0}.metric-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px}.metric{background:#fff;border:1px solid var(--line);border-radius:8px;padding:14px}.metric strong{display:block;font-size:24px;color:var(--navy)}@media(max-width:760px){.split{grid-template-columns:1fr}.nav{align-items:flex-start;flex-direction:column}.hero{min-height:68vh}.page-title{font-size:34px}.hero p{font-size:18px}.search-box,.dashboard-actions{flex-direction:column}}@media print{.site-header,.site-footer,.hero-actions,.button,.nav-links{display:none!important}body{background:#fff;color:#000}main{max-width:none;padding:0}.panel,.card,.download-sheet,.source-panel{border-color:#777;break-inside:avoid}.page-title{font-size:28px}.band{padding:16px 0}.source-panel{background:#fff}}
            """
        ).strip(),
        encoding="utf-8",
    )
    (ASSETS / "js" / "site.js").write_text(
        dedent(
            """
            const routeAdvice = {
              full_plans: {
                title: "Likely route: full plans or early building-control discussion",
                confidence: "Medium",
                points: ["Best where structure, fire safety, drainage, ventilation or energy details need checking before work starts.", "Ask what drawings, calculations and specifications the building control body expects."],
                downloads: ["/downloads/building-notice-vs-full-plans-worksheet/", "/downloads/structural-calculations-briefing-sheet/"]
              },
              building_notice: {
                title: "Possible route: building notice",
                confidence: "Medium",
                points: ["Usually only worth considering for straightforward domestic work where the specification is already clear.", "You still need inspections and may carry more risk if details are found unsuitable during the build."],
                downloads: ["/downloads/building-notice-vs-full-plans-worksheet/", "/downloads/inspection-stage-record-sheet/"]
              },
              competent_person: {
                title: "Possible route: registered competent person",
                confidence: "Medium",
                points: ["Some electrical, heating, window and door work can be self-certified by a registered installer.", "Check registration before work starts and keep the certificate because it may matter on sale or remortgage."],
                downloads: ["/downloads/competent-person-certificate-checklist/", "/downloads/sale-remortgage-proof-folder/"]
              },
              regularisation: {
                title: "Likely route: regularisation or missing-evidence discussion",
                confidence: "Medium",
                points: ["For completed work with missing approval records, gather photos, invoices, drawings and certificates before contacting building control.", "Regularisation is not automatic and may require opening up work."],
                downloads: ["/downloads/regularisation-evidence-pack/", "/downloads/completion-certificate-record-sheet/"]
              },
              specialist: {
                title: "Stop route: specialist or BSR guidance first",
                confidence: "High",
                points: ["Do not use a homeowner shortcut for higher-risk buildings, flats, major fire-safety work or unclear structural risk.", "Speak to building control, a competent professional or the relevant regulator before relying on general guidance."],
                downloads: ["/downloads/building-control-phone-call-script/", "/downloads/sale-remortgage-proof-folder/"]
              }
            };

            const toolTweaks = {
              "full-plans-vs-building-notice-checker": values => values.structuralChange === "yes" || ["extension", "loft", "structural", "drainage"].includes(values.projectType) ? "full_plans" : "building_notice",
              "competent-person-scheme-checker": values => ["electrical", "heating", "windows"].includes(values.projectType) && values.workStatus !== "finished" ? "competent_person" : "full_plans",
              "completion-certificate-readiness-checker": values => values.certificateMissing === "yes" || values.workStatus === "finished" ? "regularisation" : "full_plans",
              "approved-document-router": values => values.higherRisk === "yes" ? "specialist" : "full_plans",
              "inspection-stage-checklist-generator": values => values.structuralChange === "yes" || ["extension", "loft", "garage", "drainage"].includes(values.projectType) ? "full_plans" : "building_notice",
              "jurisdiction-route-selector": values => values.jurisdiction !== "england" ? "specialist" : "full_plans"
            };

            const projectDocuments = {
              extension: ["Approved Document A", "Approved Document L", "Approved Document F", "Approved Document H"],
              loft: ["Approved Document A", "Approved Document B", "Approved Document K", "Approved Document L", "Approved Document F"],
              garage: ["Approved Document C", "Approved Document L", "Approved Document F", "Approved Document B"],
              structural: ["Approved Document A", "Approved Document B"],
              windows: ["Approved Document L", "Approved Document K", "Approved Document B"],
              electrical: ["Approved Document P"],
              heating: ["Approved Document L", "Approved Document F"],
              drainage: ["Approved Document H"]
            };

            const officialSources = [
              ["GOV.UK building regulations approval", "https://www.gov.uk/building-regulations-approval"],
              ["GOV.UK how to apply", "https://www.gov.uk/building-regulations-approval/how-to-apply"],
              ["GOV.UK competent person scheme", "https://www.gov.uk/building-regulations-approval/use-a-competent-person-scheme"],
              ["GOV.UK Approved Documents", "https://www.gov.uk/government/collections/approved-documents"]
            ];

            function chooseRoute(values, toolSlug) {
              if (values.jurisdiction !== "england" || values.higherRisk === "yes") return "specialist";
              if (toolTweaks[toolSlug]) return toolTweaks[toolSlug](values);
              if (values.workStatus === "finished" || values.certificateMissing === "yes") return "regularisation";
              if (["electrical", "heating", "windows"].includes(values.projectType)) return "competent_person";
              if (values.structuralChange === "yes" || ["loft", "extension", "garage", "structural", "drainage"].includes(values.projectType)) return "full_plans";
              return "building_notice";
            }

            function renderResult(form) {
              const values = Object.fromEntries(new FormData(form).entries());
              const toolSlug = form.closest("[data-tool]")?.dataset.tool || "building-control-route-checker";
              const key = chooseRoute(values, toolSlug);
              const advice = routeAdvice[key];
              const docs = projectDocuments[values.projectType] || ["Approved Documents collection"];
              const target = form.parentElement.querySelector(".result");
              const date = new Date().toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });
              target.innerHTML = `
                <h3>${advice.title}</h3>
                <p><strong>Confidence:</strong> ${advice.confidence}. This tool does not grant approval or replace building control, a designer, installer, engineer or registered approver.</p>
                <ul>${advice.points.map(point => `<li>${point}</li>`).join("")}</ul>
                <p><strong>Likely documents to check:</strong> ${docs.join(", ")}.</p>
                <p><strong>Red flags:</strong> higher-risk building, flat conversion, load-bearing changes, fire escape uncertainty, missing certificates, drainage changes, public sewer issues or work outside England.</p>
                <p><strong>Next actions:</strong> ask building control what they need before work starts, record who issues each certificate, and save evidence before work is covered up.</p>
                <p><strong>Official sources:</strong> ${officialSources.map(([label, url]) => `<a href="${url}">${label}</a>`).join(" / ")}</p>
                <p><strong>Recommended downloads:</strong> ${advice.downloads.map(path => `<a href="${path}">${path.split("/").filter(Boolean).pop().replaceAll("-", " ")}</a>`).join(" / ")}</p>
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
                const checklist = ["Route chosen", "Building control contacted", "Drawings/spec ready", "Inspection points recorded", "Certificates chased"];
                mount.innerHTML = `
                  <article class="card"><h3>Project evidence tracker</h3><ul>${checklist.map((item, index) => `<li><label><input type="checkbox" data-dashboard-check="${index}"> ${item}</label></li>`).join("")}</ul><button class="button ghost" type="button" onclick="window.print()">Print dashboard</button></article>
                  ${saved.length ? saved.map((item, index) => `<article class="card"><h3>Saved result ${index + 1}</h3><p class="local-note">${new Date(item.savedAt).toLocaleString("en-GB")}</p><p>${item.text.replace(/[<>&]/g, "")}</p></article>`).join("") : `<article class="card"><h3>No saved results yet</h3><p>Run a checker, save the result locally, then use this dashboard as your device-only evidence prompt.</p></article>`}
                `;
                document.querySelectorAll("[data-dashboard-check]").forEach(input => {
                  input.checked = localStorage.getItem(`brg_check_${input.dataset.dashboardCheck}`) === "true";
                  input.addEventListener("change", () => localStorage.setItem(`brg_check_${input.dataset.dashboardCheck}`, input.checked));
                });
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
        ("/planning-and-building-regulations/", "Planning map"),
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
              <p><a href="/planning-and-building-regulations/">Planning and building regs project map</a></p>
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


def faqs_for(page: dict) -> list[tuple[str, str]]:
    family = page.get("family", "")
    title = page.get("title", "this project")
    if family == "project":
        return [
            (f"Does {title.lower()} need building regulations approval?", "Often yes, especially where the work changes structure, fire safety, insulation, ventilation, drainage, electrics or heating. The exact route depends on the specification and building control body."),
            ("Can planning permission and building regulations be separate?", "Yes. Planning permission controls whether development is allowed in planning terms; building regulations deal with safety, energy, ventilation, drainage, structure and completion evidence."),
            ("What should I keep for sale or remortgage?", "Keep the application reference, drawings, inspection notes, photos before work is covered, installer certificates and the completion certificate or equivalent evidence."),
        ]
    if family in {"approval_route", "guide"}:
        return [
            ("Does this page give approval?", "No. It helps you prepare the right questions for building control, a registered approver, designer, installer or other competent professional."),
            ("When should I stop and get specialist advice?", "Stop if the work involves flats, higher-risk buildings, major fire-safety implications, unclear structure, public sewers or work outside England."),
        ]
    if family in {"approved_document", "approved_document_hub"}:
        return [
            ("Are Approved Documents the law?", "They are statutory guidance showing common ways to meet building regulations in England. Other routes may be possible, but you should check the current version and project-specific route."),
            ("Why does version date matter?", "Approved Documents can be amended. Older projects and transitional arrangements can depend on timing, so re-check the official source before work starts."),
        ]
    return []


def schema_for(page: dict) -> dict | list[dict]:
    kind = "WebPage"
    if page["family"] == "tool":
        kind = "SoftwareApplication"
    elif page["family"] == "download":
        kind = "DigitalDocument"
    elif page["family"] in {"guide", "approval_route", "project", "approved_document", "evidence", "comparison", "programmatic_question_page"}:
        kind = "Article"
    main = {
        "@context": "https://schema.org",
        "@type": kind,
        "name": page["title"],
        "description": page.get("meta_description") or page.get("summary", ""),
        "url": BASE_URL + page["path"],
        "dateModified": TODAY,
        "publisher": {"@type": "Organization", "name": "BuildingRegsGuide"},
    }
    breadcrumbs_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": page["title"], "item": BASE_URL + page["path"]},
        ],
    }
    faq_items = faqs_for(page)
    if not faq_items:
        return [main, breadcrumbs_schema]
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": question, "acceptedAnswer": {"@type": "Answer", "text": answer}}
            for question, answer in faq_items
        ],
    }
    return [main, breadcrumbs_schema, faq_schema]


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


def sister_handoff(page: dict) -> str:
    slug = page.get("slug", slug_from_path(page.get("path", "")))
    handoff = SISTER_PROJECT_LINKS.get(slug)
    if not handoff and page.get("needs_cross_site_handoff"):
        handoff = {
            "url": SISTER_URL + "/",
            "label": "check the planning permission side",
            "note": "Use this only for the planning permission, permitted development, prior approval or lawful development question.",
        }
    if not handoff:
        return ""
    return dedent(
        f"""
        <aside class="handoff" aria-label="Planning handoff">
          <h2>Planning side of this project</h2>
          <p>{escape(handoff['note'])}</p>
          <p><a href="{escape(handoff['url'])}">{escape(handoff['label'])}</a> on UKPlanningGuide, then return here for building-control routes, inspections, certificates and evidence.</p>
        </aside>
        """
    )


def related_links(page: dict, all_pages: list[dict]) -> str:
    candidates = []
    preferred = [
        "/tools/building-control-route-checker/",
        "/tools/full-plans-vs-building-notice-checker/",
        "/building-regulations/completion-certificate/",
        "/evidence/building-regulations-documents-to-keep/",
        "/planning-and-building-regulations/",
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


def list_html(items: list[str]) -> str:
    return "".join(f"<li>{escape(item)}</li>" for item in items)


def profile_for(page: dict) -> dict:
    slug = page.get("slug", slug_from_path(page.get("path", "")))
    if slug in PROJECT_PROFILES:
        return PROJECT_PROFILES[slug]
    title = page.get("title", "this project")
    return {
        "answer": page.get("summary", f"Use this page to prepare the building regulations route and evidence questions for {title.lower()}."),
        "triggers": ["Structure, fire safety, drainage, insulation, ventilation or controlled services", "Work already started or completed without clear records", "Missing certificates or unclear handover evidence", "Anything involving flats, higher-risk buildings or work outside England"],
        "route": "Compare full plans, building notice, competent person self-certification, regularisation and specialist advice. The right route depends on risk, timing, drawings, installer registration and what building control wants to inspect.",
        "evidence": ["Application references and notices", "Drawings, specifications and calculations", "Inspection dates and site photos before cover-up", "Completion certificate, competent person certificate and commissioning records"],
    }


def approved_document_section(page: dict) -> str:
    slug = page.get("slug", "")
    topic, checks = APPROVED_DOCUMENT_PROFILES.get(slug, (page["title"], ["Project relevance", "Version date", "Evidence needed", "Inspection timing"]))
    return dedent(
        f"""
        <section class="section">
          <h2>How this Approved Document usually comes up</h2>
          <p>{escape(topic)} guidance can affect design choices, product evidence and inspection conversations. Treat the document as practical guidance for common ways to comply in England, not as a one-line pass/fail answer.</p>
          <ul class="checklist">{list_html(checks)}</ul>
        </section>
        <section class="section">
          <h2>Version and evidence notes</h2>
          <p>Record the version checked, the date checked, and who is responsible for translating the guidance into drawings, specifications, calculations or installer certificates. Part F, Part L and fire-safety topics especially need source/version caution.</p>
        </section>
        """
    )


def faq_section(page: dict) -> str:
    faqs = faqs_for(page)
    if not faqs:
        return ""
    blocks = "".join(
        f"""
        <details class="faq-item">
          <summary>{escape(question)}</summary>
          <p>{escape(answer)}</p>
        </details>
        """
        for question, answer in faqs
    )
    return f'<section class="section faq-list"><h2>Common questions</h2>{blocks}</section>'


def page_sections(page: dict) -> str:
    title = page["title"]
    family = page["family"]
    profile = profile_for(page)
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
    doc_version = approved_document_section(page) if family in {"approved_document", "approved_document_hub"} else ""
    return dedent(
        f"""
        <section class="section">
          <h2>Short answer</h2>
          <p>{escape(profile['answer'])}</p>
          <div class="{warning_class}">{escape(warning_text)}</div>
          {planning_handoff}
          {sister_handoff(page)}
        </section>
        <section class="section">
          <h2>What usually triggers extra checks</h2>
          <ul class="checklist">{list_html(profile['triggers'])}</ul>
        </section>
        <section class="section">
          <h2>Route options to discuss</h2>
          <p>{escape(profile['route'])}</p>
        </section>
        <section class="section">
          <h2>Evidence to keep</h2>
          <ul class="checklist">{list_html(profile['evidence'])}</ul>
        </section>
        {doc_version}
        <section class="section">
          <h2>Mistakes to avoid</h2>
          <p>Do not assume planning permission, permitted development or a builder's quote answers the building regulations question. Do not cover up work before required inspections. Do not rely on a certificate claim without checking who issues it and how you will receive a copy.</p>
        </section>
        {faq_section(page)}
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


def markdown_table(lines: list[str]) -> str:
    rows = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if all(set(cell) <= {"-", ":"} for cell in cells):
            continue
        tag = "th" if not rows else "td"
        rows.append("<tr>" + "".join(f"<{tag}>{escape(cell)}</{tag}>" for cell in cells) + "</tr>")
    if not rows:
        return ""
    return f'<div class="table-wrap"><table class="evidence-table">{"".join(rows)}</table></div>'


def markdown_to_html(markdown: str) -> str:
    markdown = markdown.replace("{ generated_date }", TODAY).replace("{ source_snapshot_id }", "2026-06-05").replace("{ jurisdiction }", "England-first")
    lines = markdown.splitlines()
    if lines and lines[0].strip() == "---":
        try:
            end = lines[1:].index("---") + 1
            lines = lines[end + 1 :]
        except ValueError:
            pass
    html_parts: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    table_lines: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            html_parts.append(f"<p>{escape(' '.join(paragraph))}</p>")
            paragraph.clear()

    def flush_list() -> None:
        if list_items:
            html_parts.append(f'<ul class="checklist">{"".join(f"<li>{escape(item)}</li>" for item in list_items)}</ul>')
            list_items.clear()

    def flush_table() -> None:
        if table_lines:
            html_parts.append(markdown_table(table_lines))
            table_lines.clear()

    for raw in lines:
        line = raw.strip()
        if not line:
            flush_paragraph()
            flush_list()
            flush_table()
            continue
        if line.startswith("|"):
            flush_paragraph()
            flush_list()
            table_lines.append(line)
            continue
        flush_table()
        if line.startswith("# "):
            flush_paragraph()
            flush_list()
            html_parts.append(f"<h2>{escape(line[2:].strip())}</h2>")
        elif line.startswith("## "):
            flush_paragraph()
            flush_list()
            html_parts.append(f"<h2>{escape(line[3:].strip())}</h2>")
        elif line.startswith("### "):
            flush_paragraph()
            flush_list()
            html_parts.append(f"<h3>{escape(line[4:].strip())}</h3>")
        elif line.startswith("- "):
            flush_paragraph()
            list_items.append(line[2:].strip())
        elif re.match(r"^\d+\.\s+", line):
            flush_paragraph()
            list_items.append(re.sub(r"^\d+\.\s+", "", line))
        else:
            paragraph.append(line)
    flush_paragraph()
    flush_list()
    flush_table()
    return "\n".join(html_parts)


def download_markdown_html(download: dict) -> str:
    filename = DOWNLOAD_MARKDOWN_MAP.get(download.get("slug", ""))
    if not filename:
        return ""
    path = DOWNLOAD_MARKDOWN_DIR / filename
    if not path.exists():
        return ""
    return markdown_to_html(path.read_text(encoding="utf-8-sig"))


def download_sheet(download: dict) -> str:
    markdown_html = download_markdown_html(download)
    fallback_sections = "".join(
        f"""
        <section class="section">
          <h2>{escape(section)}</h2>
          <p class="local-note">Use this space to record the project-specific evidence, responsible person, source checked and follow-up action.</p>
          <div class="blank-line"></div>
          <div class="blank-line"></div>
          <div class="blank-line"></div>
        </section>
        """
        for section in download.get("sections", [])
    )
    sections = markdown_html or fallback_sections
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
          <div class="printable-content">{sections}</div>
          <section class="section">
            <h2>Handover note</h2>
            <p>At the end of the project, store this sheet with completion certificates, competent person certificates, warranties, product information and any building-control correspondence. It may help when selling, remortgaging or explaining historic work later.</p>
          </section>
          <button class="button ghost" type="button" onclick="window.print()">Print checklist</button>
        </article>
        """
    )


def render_bridge_page(page: dict, all_pages: list[dict], sources: dict) -> str:
    cards = "".join(
        f"""
        <article class="handoff-card">
          <h3>{escape(card['project'])}</h3>
          <p><strong>Building regs:</strong> {escape(card['building_text'])}</p>
          <p><a href="{escape(card['building'])}">Building-control evidence to keep</a></p>
          <p><strong>Planning:</strong> {escape(card['planning_text'])}</p>
          <p><a href="{escape(card['planning'])}">Check the planning route first</a></p>
        </article>
        """
        for card in BRIDGE_CARDS
    )
    body = dedent(
        f"""
        <main>
          {breadcrumbs(page['path'], page['title'])}
          <h1 class="page-title">{escape(page['title'])}</h1>
          <p class="lede">{escape(page['summary'])}</p>
          <section class="section">
            <h2>Use the two sites together</h2>
            <p>Planning permission asks whether the development is allowed in planning terms. Building regulations ask whether the work is designed, built, inspected and evidenced properly. A project can need one, both or neither, so keep the decisions separate in your project file.</p>
            <div class="metric-grid">
              <div class="metric"><strong>1</strong>Planning route</div>
              <div class="metric"><strong>2</strong>Building-control route</div>
              <div class="metric"><strong>3</strong>Evidence and certificates</div>
            </div>
          </section>
          <section class="section">
            <h2>Project handoff map</h2>
            <div class="handoff-grid">{cards}</div>
          </section>
          <section class="section">
            <h2>Do not mix up these decisions</h2>
            <div class="table-wrap">
              <table class="route-table">
                <tr><th>Question</th><th>Use UKPlanningGuide for</th><th>Use BuildingRegsGuide for</th></tr>
                <tr><td>Can I build it?</td><td>Planning permission, permitted development, prior approval, local planning policy.</td><td>Not the main source, except to understand that building regs may still apply.</td></tr>
                <tr><td>How must it be built?</td><td>Only where design constraints affect planning.</td><td>Approved Documents, full plans, building notice, inspections, competent person schemes.</td></tr>
                <tr><td>What proof should I keep?</td><td>Planning decisions, lawful development certificates and appeal/condition records.</td><td>Drawings, calculations, inspections, completion certificates and installer certificates.</td></tr>
              </table>
            </div>
          </section>
          {related_links(page, all_pages)}
          {source_panel(['govuk_building_regs_approval'], sources)}
        </main>
        """
    )
    return base_html(page["title"], page["summary"], page["path"], body, schema_for(page))


def render_evidence_page(page: dict, all_pages: list[dict], sources: dict) -> str:
    items = "".join(f"<li>{escape(item)}</li>" for item in page.get("documents", []))
    body = dedent(
        f"""
        <main>
          {breadcrumbs(page['path'], page['title'])}
          <h1 class="page-title">{escape(page['title'])}</h1>
          <p class="lede">{escape(page['summary'])}</p>
          <section class="section">
            <h2>Short answer</h2>
            <p>Keep a project file that proves what route was chosen, what was inspected, who certified controlled services, and what evidence was available before work was covered up. Missing records can become a sale, remortgage or future-alteration problem.</p>
          </section>
          <section class="section">
            <h2>Documents and evidence to keep</h2>
            <ul class="checklist">{items}</ul>
          </section>
          <section class="section">
            <h2>When to ask before relying on old paperwork</h2>
            <p>Ask building control, your conveyancer or a competent professional where work is historic, certificates are missing, the work affects structure or fire safety, or the only evidence is a builder's verbal assurance.</p>
          </section>
          <section class="section">
            <h2>Next action</h2>
            <p>Use the printable checklist and local dashboard to keep the evidence trail together.</p>
            <div class="mini-nav">
              <a class="button" href="{escape(page.get('download', '/downloads/'))}">Open related download</a>
              <a class="button ghost" href="/dashboard/">Open local dashboard</a>
              <a class="button ghost" href="/tools/completion-certificate-readiness-checker/">Check completion readiness</a>
            </div>
          </section>
          {related_links(page, all_pages)}
          {source_panel([page.get('primary_source_id', 'govuk_building_regs_approval'), 'govuk_use_competent_person'], sources)}
        </main>
        """
    )
    return base_html(page["title"], page["summary"], page["path"], body, schema_for(page))


def render_comparison_page(page: dict, all_pages: list[dict], sources: dict) -> str:
    body = dedent(
        f"""
        <main>
          {breadcrumbs(page['path'], page['title'])}
          <h1 class="page-title">{escape(page['title'])}</h1>
          <p class="lede">{escape(page['summary'])}</p>
          <section class="section">
            <h2>Plain answer</h2>
            <p>Use full plans when design certainty matters before work starts. A building notice may suit simpler domestic work where details are already settled. Regularisation is for certain completed unauthorised work and can require opening up work; it is not a tidy substitute for applying before work starts.</p>
          </section>
          <section class="section">
            <h2>Route comparison</h2>
            <div class="table-wrap">
              <table class="route-table">
                <tr><th>Route</th><th>Best fit</th><th>Main risk</th><th>Evidence to keep</th></tr>
                <tr><td>Full plans</td><td>Extensions, lofts, structural work, complex drainage, linked fire/energy details.</td><td>More preparation before work starts, but fewer unresolved site surprises.</td><td>Approved plans, calculations, specification, inspection records, completion certificate.</td></tr>
                <tr><td>Building notice</td><td>Clear, straightforward domestic work with competent builders and simple details.</td><td>Problems can surface on site after money is committed.</td><td>Notice acknowledgement, inspection notes, photos, certificates, completion record.</td></tr>
                <tr><td>Regularisation</td><td>Older completed work where approval evidence is missing and the local authority route is available.</td><td>May need opening up; approval is not guaranteed.</td><td>Photos, invoices, drawings, certificates, survey notes, local authority correspondence.</td></tr>
              </table>
            </div>
          </section>
          <section class="section">
            <h2>Common mistakes</h2>
            <ul class="checklist">
              <li>Choosing building notice to avoid preparing structural or energy details.</li>
              <li>Starting work before inspection stages are agreed.</li>
              <li>Assuming planning permission removes the building regulations duty.</li>
              <li>Leaving completion certificate and competent person certificate checks until sale.</li>
            </ul>
          </section>
          <div class="mini-nav">
            <a class="button" href="/tools/full-plans-vs-building-notice-checker/">Use route checker</a>
            <a class="button ghost" href="/downloads/building-notice-vs-full-plans-worksheet/">Print worksheet</a>
          </div>
          {related_links(page, all_pages)}
          {source_panel(['govuk_how_to_apply', 'planning_portal_building_notice'], sources)}
        </main>
        """
    )
    return base_html(page["title"], page["summary"], page["path"], body, schema_for(page))


def render_question_page(page: dict, all_pages: list[dict], sources: dict) -> str:
    project_page = next((item for item in all_pages if item["path"] == page.get("parent")), None)
    profile = profile_for({"slug": page.get("project_slug", ""), "title": page["title"], "summary": page["summary"]})
    parent_link = project_page["path"] if project_page else "/projects/"
    parent_title = project_page["title"] if project_page else "project guide"
    body = dedent(
        f"""
        <main>
          {breadcrumbs(page['path'], page['title'])}
          <h1 class="page-title">{escape(page['title'])}</h1>
          <p class="lede">{escape(page['summary'])}</p>
          <section class="section">
            <h2>Short answer</h2>
            <p>{escape(profile['answer'])}</p>
            {sister_handoff({'slug': page.get('project_slug', ''), 'needs_cross_site_handoff': True})}
          </section>
          <section class="section">
            <h2>What changes the answer</h2>
            <ul class="checklist">{list_html(profile['triggers'])}</ul>
          </section>
          <section class="section">
            <h2>Safer next step</h2>
            <p>{escape(profile['route'])}</p>
            <div class="mini-nav">
              <a class="button" href="{escape(parent_link)}">Open {escape(parent_title)}</a>
              <a class="button ghost" href="/tools/building-control-route-checker/">Use route checker</a>
              <a class="button ghost" href="/evidence/building-regulations-documents-to-keep/">Evidence to keep</a>
            </div>
          </section>
          <section class="section">
            <h2>Evidence checklist</h2>
            <ul class="checklist">{list_html(profile['evidence'])}</ul>
          </section>
          {faq_section({'family': 'project', 'title': page['title']})}
          {related_links(page, all_pages)}
          {source_panel(['govuk_building_regs_approval', 'govuk_how_to_apply'], sources)}
        </main>
        """
    )
    return base_html(page["title"], page["summary"], page["path"], body, schema_for(page))


def render_expansion_page(page: dict, all_pages: list[dict], sources: dict) -> str:
    if page["kind"] == "bridge":
        return render_bridge_page(page, all_pages, sources)
    if page["kind"] == "evidence":
        return render_evidence_page(page, all_pages, sources)
    if page["kind"] == "comparison":
        return render_comparison_page(page, all_pages, sources)
    if page["kind"] == "question":
        return render_question_page(page, all_pages, sources)
    return render_standard_page(page, all_pages, sources)


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
        ("/planning-and-building-regulations/", "Separate planning from building regs", "Use the sister-site map for the planning handoff."),
        ("/evidence/building-regulations-documents-to-keep/", "Keep the right evidence", "Documents and certificates to save before work is hidden."),
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
              <a class="button ghost" href="/planning-and-building-regulations/">Project map</a>
            </div>
          </div>
        </section>
        <main>
          <section class="band">
            <h2>Start with the right question</h2>
            <div class="grid">
              <article class="card"><h3>1. Is this a building regulations issue?</h3><p>Look for structure, fire safety, insulation, ventilation, drainage, electrics, heating or missing certificates. Planning permission is a separate track.</p></article>
              <article class="card"><h3>2. Which route fits?</h3><p>Compare full plans, building notice, competent person self-certification, regularisation or specialist/BSR advice before work starts.</p></article>
              <article class="card"><h3>3. What proof should you keep?</h3><p>Record drawings, calculations, inspection notes, certificates, product records and photos before work is covered up.</p></article>
            </div>
          </section>
          <section class="band"><div class="grid">{card_html}</div></section>
          <section class="band">
            <h2>Use the sister sites together</h2>
            <div class="handoff-grid">
              <article class="handoff-card"><h3>Planning permission</h3><p>Use UKPlanningGuide for permitted development, prior approval, local planning policy and whether the development is allowed.</p><p><a href="{SISTER_URL}/">Open UKPlanningGuide</a></p></article>
              <article class="handoff-card"><h3>Building regulations</h3><p>Use this site for building-control routes, inspections, Approved Documents, certificates and evidence to keep.</p><p><a href="/planning-and-building-regulations/">See the project map</a></p></article>
            </div>
          </section>
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
            <p>The strongest pages in this section are designed to answer one job at a time: choose a route, prepare an inspection, collect documents, or understand where planning permission sits outside building regulations. Use the cards as a sequence rather than a library. A sensible workflow is to read the most relevant guide, run the matching checker, print or save the evidence sheet, and then keep the official source panel with your project notes.</p>
            <p>If a page points to UKPlanningGuide, treat that as a planning handoff only. Come back here for building-control approval, competent person certificates, Approved Document prompts, completion evidence and inspection records. That separation makes the project file easier to explain to builders, designers, surveyors, conveyancers and building control.</p>
            <p>Comparison pages are especially useful before work starts because they expose trade-offs that are easy to miss in quotes: certainty versus speed, self-certification versus direct building-control involvement, and approval routes versus evidence routes. If a comparison still leaves you unsure, treat that uncertainty as a signal to ask building control earlier, not as a reason to choose the quickest route by default.</p>
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
          <p class="lede">Use this as a device-only project file for saved checker results, inspection prompts and certificate follow-up. There is no login, no account and no backend storage in this build.</p>
          <div class="warning">Privacy note: saved results use your browser localStorage. Do not enter sensitive personal data. Clear your browser data to remove saved items.</div>
          <section class="panel">
            <h2>Project note</h2>
            <div class="form-row">
              <input class="mini-input" id="dashboard-project" placeholder="Project, e.g. loft conversion">
              <input class="mini-input" id="dashboard-address" placeholder="Address/reference, optional">
              <input class="mini-input" id="dashboard-contact" placeholder="Building control contact, optional">
            </div>
            <div class="dashboard-actions">
              <button class="button ghost" type="button" onclick="localStorage.setItem('brg_project_note', JSON.stringify({{project:document.getElementById('dashboard-project').value,address:document.getElementById('dashboard-address').value,contact:document.getElementById('dashboard-contact').value}})); location.reload();">Save note locally</button>
              <button class="button ghost" type="button" onclick="window.print()">Print project file</button>
            </div>
          </section>
          <section class="grid" data-dashboard></section>
          {source_panel(['govuk_building_regs_approval'], sources)}
          <script>
            const note = JSON.parse(localStorage.getItem('brg_project_note') || '{{}}');
            if (note.project) document.getElementById('dashboard-project').value = note.project;
            if (note.address) document.getElementById('dashboard-address').value = note.address;
            if (note.contact) document.getElementById('dashboard-contact').value = note.contact;
          </script>
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
    for extra in EXPANSION_PAGES:
        page = {**extra}
        page.setdefault("slug", slug_from_path(page["path"]))
        page.setdefault("meta_title", page["title"])
        page.setdefault("meta_description", page["summary"])
        page.setdefault("primary_source_id", "govuk_building_regs_approval")
        pages.append(page)
    return pages


def mirror_output_to_root() -> None:
    mirror_paths = [
        ".nojekyll",
        "404.html",
        "BUILD_REPORT.json",
        "BUILD_REPORT.md",
        "CNAME",
        "about",
        "approved-documents",
        "assets",
        "building-regulations",
        "compare",
        "dashboard",
        "downloads",
        "evidence",
        "index.html",
        "legal",
        "planning-and-building-regulations",
        "projects",
        "robots.txt",
        "search",
        "search-index.json",
        "sitemap.xml",
        "tools",
        "questions",
    ]
    for relative in mirror_paths:
        source = OUTPUT / relative
        target = ROOT / relative
        if not source.exists():
            continue
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
        if source.is_dir():
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)


def build() -> dict:
    data = load_data()
    ensure_clean_output()
    write_static_assets()
    pages = enrich_pages(data)
    published = []

    for page in pages:
        if page["path"] == "/":
            html_text = render_homepage(pages, data["sources"])
        elif page.get("kind") in {"bridge", "evidence", "comparison", "question"}:
            html_text = render_expansion_page(page, pages, data["sources"])
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
        ("/evidence/", "Building regulations evidence hub", "Documents, certificates and records to keep for building regulations projects, sale and remortgage.", {"evidence"}),
        ("/compare/", "Building regulations comparisons", "Compare building-control routes, certificate responsibilities and common approval misunderstandings.", {"comparison"}),
        ("/questions/", "Building regulations questions", "Focused homeowner answers that link back to fuller project guides, tools, downloads and official sources.", {"programmatic_question_page"}),
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
        "phase_1_count": len(data["phase_1"]),
        "expansion_count": len(EXPANSION_PAGES),
        "extra_navigation_pages": ["/projects/", "/tools/", "/downloads/", "/approved-documents/", "/evidence/", "/compare/", "/questions/", "/dashboard/", "/search/"],
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
        f"- Phase 1 routes: {len(data['phase_1'])}\n"
        f"- Focused expansion pages: {len(EXPANSION_PAGES)}\n"
        "- Draft/noindex pages: 0\n"
        "- Blocked pages: none in this starter pass\n"
        f"- Build environment: {BUILD_ENV}\n"
        f"- Base URL: {BASE_URL}\n"
        f"- Domain: {SITE_DOMAIN}\n"
        "- Included: generated pages, tools, downloads, sitemap, robots, search index, schema, source panels, print CSS, 404 page, legal page and local-only dashboard.\n",
        encoding="utf-8",
    )
    mirror_output_to_root()
    return report


if __name__ == "__main__":
    result = build()
    print(json.dumps(result, indent=2))
