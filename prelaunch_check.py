from __future__ import annotations

import json
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"
BASE_URL = os.environ.get("BRG_BASE_URL", "https://buildingregsguide.co.uk").rstrip("/")


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.assets: list[str] = []
        self.canonical: str | None = None
        self.title = ""
        self.meta_description: str | None = None
        self.schema_blocks: list[str] = []
        self._in_title = False
        self._in_schema = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: value or "" for key, value in attrs}
        if tag == "a" and attr.get("href"):
            self.links.append(attr["href"])
        if tag in {"img", "script"} and attr.get("src"):
            self.assets.append(attr["src"])
        if tag == "link" and attr.get("rel") == "stylesheet" and attr.get("href"):
            self.assets.append(attr["href"])
        if tag == "link" and attr.get("rel") == "canonical":
            self.canonical = attr.get("href")
        if tag == "meta" and attr.get("name") == "description":
            self.meta_description = attr.get("content", "")
        if tag == "title":
            self._in_title = True
        if tag == "script" and attr.get("type") == "application/ld+json":
            self._in_schema = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        if tag == "script":
            self._in_schema = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data
        if self._in_schema:
            self.schema_blocks.append(data)


def route_for_file(path: Path) -> str:
    if path == OUTPUT / "index.html":
        return "/"
    if path == OUTPUT / "404.html":
        return "/404.html"
    return "/" + path.parent.relative_to(OUTPUT).as_posix().strip("/") + "/"


def local_target(value: str) -> Path | None:
    parsed = urlparse(value)
    if parsed.scheme in {"http", "https"}:
        if parsed.netloc not in {"buildingregsguide.co.uk", "www.buildingregsguide.co.uk"}:
            return None
        value = parsed.path or "/"
    if value.startswith("#") or value.startswith("mailto:") or value.startswith("tel:"):
        return None
    if not value.startswith("/"):
        return None
    if value.endswith("/"):
        return OUTPUT / value.strip("/") / "index.html" if value != "/" else OUTPUT / "index.html"
    return OUTPUT / value.strip("/")


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []
    html_files = sorted(OUTPUT.rglob("*.html"))
    titles: dict[str, str] = {}
    descriptions: dict[str, str] = {}

    for file in html_files:
        route = route_for_file(file)
        text = file.read_text(encoding="utf-8")
        parser = PageParser()
        parser.feed(text)

        expected_canonical = f"{BASE_URL}{route}"
        if parser.canonical != expected_canonical:
            failures.append(f"{route} canonical mismatch: expected {expected_canonical}, got {parser.canonical}")
        if not parser.title.strip():
            failures.append(f"{route} missing title")
        if not parser.meta_description or len(parser.meta_description.strip()) < 50:
            failures.append(f"{route} meta description is missing or too short")
        if parser.title in titles:
            warnings.append(f"Duplicate title: {route} and {titles[parser.title]} use {parser.title!r}")
        else:
            titles[parser.title] = route
        if parser.meta_description in descriptions:
            warnings.append(f"Duplicate meta description: {route} and {descriptions[parser.meta_description or '']}")
        elif parser.meta_description:
            descriptions[parser.meta_description] = route

        for block in parser.schema_blocks:
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                failures.append(f"{route} has invalid JSON-LD: {exc}")

        for value in parser.links + parser.assets:
            target = local_target(value)
            if target and not target.exists():
                failures.append(f"{route} references missing local target: {value}")

        visible_words = re.sub(r"<[^>]+>", " ", text)
        word_count = len(re.findall(r"[A-Za-z][A-Za-z'-]+", visible_words))
        if word_count < 450 and route not in {"/dashboard/", "/404.html"}:
            warnings.append(f"{route} is short for launch content: {word_count} words")

    sitemap_path = OUTPUT / "sitemap.xml"
    if not sitemap_path.exists():
        failures.append("Missing sitemap.xml")
    else:
        tree = ElementTree.fromstring(sitemap_path.read_text(encoding="utf-8"))
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        sitemap_routes = {re.sub(f"^{re.escape(BASE_URL)}", "", loc.text or "") for loc in tree.findall(".//sm:loc", ns)}
        page_routes = {route_for_file(file) for file in html_files if route_for_file(file) != "/404.html"}
        if sitemap_routes != page_routes:
            failures.append("Sitemap route set does not exactly match generated HTML routes")

    print(f"Checked {len(html_files)} HTML pages.")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    if failures:
        print("Failures:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Prelaunch check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
