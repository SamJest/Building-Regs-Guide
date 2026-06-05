from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"
BASE_URL = os.environ.get("BRG_BASE_URL", "https://buildingregsguide.co.uk").rstrip("/")


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def html_files() -> list[Path]:
    return sorted(OUTPUT.rglob("*.html"))


def route_from_file(path: Path) -> str:
    if path == OUTPUT / "index.html":
        return "/"
    if path == OUTPUT / "404.html":
        return "/404.html"
    return "/" + path.parent.relative_to(OUTPUT).as_posix().strip("/") + "/"


def validate() -> list[str]:
    failures: list[str] = []
    files = html_files()
    if not files:
        fail("No generated HTML files found. Run build_site.py first.", failures)
        return failures

    for file in files:
        text = file.read_text(encoding="utf-8")
        route = route_from_file(file)
        if "source-panel" not in text:
            fail(f"{route} is missing a source/version panel.", failures)
        if "grant approval" in text.lower() and "does not grant approval" not in text.lower():
            fail(f"{route} may imply approval without the required disclaimer.", failures)
        if '<script type="application/ld+json">' not in text:
            fail(f"{route} is missing JSON-LD schema.", failures)
        if route.startswith("/tools/") and route != "/tools/":
            for required in ["data-tool-form", "does not grant approval", "Higher-risk"]:
                if required not in text:
                    fail(f"{route} tool page is missing required marker: {required}", failures)
        if route.startswith("/downloads/") and route != "/downloads/":
            if "Generated" not in text or "Re-check official guidance" not in text:
                fail(f"{route} download page is missing generated/re-check warning.", failures)

    css = (OUTPUT / "assets" / "site.css").read_text(encoding="utf-8") if (OUTPUT / "assets" / "site.css").exists() else ""
    if "@media print" not in css:
        fail("Print CSS is missing.", failures)

    search_path = OUTPUT / "search-index.json"
    if not search_path.exists():
        fail("search-index.json is missing.", failures)
    else:
        index = json.loads(search_path.read_text(encoding="utf-8"))
        if len(index) < 70:
            fail("Search index has fewer than the phase-1 route count.", failures)

    sitemap_path = OUTPUT / "sitemap.xml"
    if not sitemap_path.exists():
        fail("sitemap.xml is missing.", failures)
    else:
        sitemap = sitemap_path.read_text(encoding="utf-8")
        tree = ElementTree.fromstring(sitemap)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        sitemap_routes = {re.sub(f"^{re.escape(BASE_URL)}", "", loc.text or "") for loc in tree.findall(".//sm:loc", ns)}
        generated_routes = {route_from_file(file) for file in files if route_from_file(file) != "/404.html"}
        missing = generated_routes - sitemap_routes
        extra = sitemap_routes - generated_routes
        if missing:
            fail(f"Sitemap missing generated routes: {sorted(missing)[:8]}", failures)
        if extra:
            fail(f"Sitemap has routes without generated pages: {sorted(extra)[:8]}", failures)
        for file in files:
            text = file.read_text(encoding="utf-8")
            if 'name="robots" content="noindex' in text and route_from_file(file) in sitemap_routes:
                fail(f"Noindex route appears in sitemap: {route_from_file(file)}", failures)

    dashboard = OUTPUT / "dashboard" / "index.html"
    if not dashboard.exists() or "localStorage" not in dashboard.read_text(encoding="utf-8"):
        fail("Dashboard page is missing the localStorage-only privacy marker.", failures)

    return failures


if __name__ == "__main__":
    problems = validate()
    if problems:
        print("Validation failed:")
        for problem in problems:
            print(f"- {problem}")
        sys.exit(1)
    print("Validation passed.")
