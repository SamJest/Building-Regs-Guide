from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"


class TextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.footer_parts: list[str] = []
        self._skip = False
        self._footer = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style"}:
            self._skip = True
        if tag == "footer":
            self._footer = True

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"}:
            self._skip = False
        if tag == "footer":
            self._footer = False

    def handle_data(self, data: str) -> None:
        if self._skip:
            return
        clean = " ".join(data.split())
        if not clean:
            return
        self.parts.append(clean)
        if self._footer:
            self.footer_parts.append(clean)


def route_for_file(path: Path) -> str:
    if path == OUTPUT / "index.html":
        return "/"
    if path == OUTPUT / "404.html":
        return "/404.html"
    return "/" + path.parent.relative_to(OUTPUT).as_posix().strip("/") + "/"


def visible_text(html: str) -> tuple[str, str]:
    parser = TextParser()
    parser.feed(html)
    return " ".join(parser.parts), " ".join(parser.footer_parts)


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z][A-Za-z'-]+", text))


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []
    html_files = sorted(OUTPUT.rglob("*.html"))
    site_js = (OUTPUT / "assets" / "js" / "site.js").read_text(encoding="utf-8") if (OUTPUT / "assets" / "js" / "site.js").exists() else ""
    if not html_files:
        print("Quality audit failed: run build_site.py first.")
        return 1

    banned_visible_phrases = [
        "Printable HTML-first asset",
        "This guide helps you prepare the right questions",
        "No. It helps you prepare the right questions",
        "Lorem ipsum",
        "TODO",
        "placeholder",
    ]
    repeated_phrases = {
        "This tool does not grant approval": 18,
        "Re-check official guidance": 24,
        "Use this as a project file prompt": 24,
    }
    phrase_counts = {phrase: 0 for phrase in repeated_phrases}

    for file in html_files:
        route = route_for_file(file)
        html = file.read_text(encoding="utf-8")
        text, footer = visible_text(html)
        lower_text = text.lower()

        for phrase in banned_visible_phrases:
            if phrase.lower() in lower_text:
                failures.append(f"{route} contains template-sounding phrase: {phrase}")

        for phrase in phrase_counts:
            if phrase.lower() in lower_text:
                phrase_counts[phrase] += 1

        if "ukplanningguide.co.uk" in footer.lower():
            failures.append(f"{route} has a footer UKPlanningGuide link; cross-site links should stay contextual.")

        if route.startswith("/downloads/") and route != "/downloads/":
            if "Best used:" not in text:
                failures.append(f"{route} download is missing a practical 'Best used' note.")
            if word_count(text) < 650:
                failures.append(f"{route} download is too thin to be useful: {word_count(text)} words.")
            if "Project details" in text and "Evidence checklist" not in text:
                warnings.append(f"{route} may still be relying on fallback worksheet headings.")

        if route.startswith("/tools/") and route != "/tools/":
            if "Why this result:" not in site_js:
                failures.append("Tool result template is missing 'Why this result' in site.js.")
            if "Recommended downloads:" not in site_js or "route decision worksheet" not in site_js:
                failures.append("Tool result template is missing human-readable download labels in site.js.")

        if route in {"/before-you-start/", "/evidence/", "/inspections/", "/compare/", "/questions/"}:
            card_count = html.count('<article class="card">')
            if card_count < 1:
                failures.append(f"{route} hub has no cards.")
            if word_count(text) < 500:
                warnings.append(f"{route} hub may need more editorial copy: {word_count(text)} words.")

        if route not in {"/404.html", "/dashboard/", "/search/"} and word_count(text) < 500:
            warnings.append(f"{route} is short for competitive SEO: {word_count(text)} words.")

    for phrase, count in phrase_counts.items():
        if count > repeated_phrases[phrase]:
            failures.append(f"Phrase appears too often ({count} pages): {phrase}")

    print(f"Quality-audited {len(html_files)} HTML pages.")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    if failures:
        print("Failures:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Quality audit passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
