from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class Check:
    path: str
    contains: str | None = None
    content_type: str | None = None


CHECKS = [
    Check("/", "BuildingRegsGuide", "text/html"),
    Check("/sitemap.xml", "<urlset", "xml"),
    Check("/robots.txt", "Sitemap:", "text/plain"),
    Check("/assets/site.css", ".hero", "text/css"),
    Check("/assets/js/site.js", "routeAdvice", "javascript"),
    Check("/building-regulations/", "Building regulations", "text/html"),
    Check("/tools/building-control-route-checker/", "data-tool-form", "text/html"),
    Check("/downloads/extension-building-regulations-checklist/", "Evidence checklist", "text/html"),
    Check("/legal/", "Legal and safety", "text/html"),
    Check("/404.html", "Page not found", "text/html"),
]


def fetch(url: str) -> tuple[int, str, str]:
    request = Request(url, headers={"User-Agent": "BuildingRegsGuide-live-check/1.0"})
    with urlopen(request, timeout=20) as response:
        body = response.read().decode("utf-8", errors="replace")
        return response.status, response.headers.get("Content-Type", ""), body


def main() -> int:
    parser = argparse.ArgumentParser(description="Check the live BuildingRegsGuide deployment.")
    parser.add_argument("--base-url", default="https://buildingregsguide.co.uk", help="Production or preview base URL.")
    parser.add_argument("--retries", type=int, default=1, help="Attempts per URL before failing.")
    parser.add_argument("--delay", type=int, default=10, help="Seconds to wait between retry attempts.")
    args = parser.parse_args()
    base_url = args.base_url.rstrip("/")
    failures: list[str] = []

    for check in CHECKS:
        url = f"{base_url}{check.path}"
        last_failure = ""
        for attempt in range(1, args.retries + 1):
            try:
                status, content_type, body = fetch(url)
            except HTTPError as exc:
                last_failure = f"{check.path} returned HTTP {exc.code}"
            except URLError as exc:
                last_failure = f"{check.path} could not be reached: {exc.reason}"
            else:
                page_failures: list[str] = []
                if status != 200:
                    page_failures.append(f"{check.path} returned HTTP {status}")
                if check.content_type and check.content_type not in content_type:
                    page_failures.append(f"{check.path} content type {content_type!r} does not include {check.content_type!r}")
                if check.contains and check.contains not in body:
                    page_failures.append(f"{check.path} does not contain expected marker {check.contains!r}")
                if not page_failures:
                    last_failure = ""
                    break
                last_failure = "; ".join(page_failures)
            if attempt < args.retries:
                time.sleep(args.delay)
        if last_failure:
            failures.append(last_failure)

    if failures:
        print("Live check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Live check passed for {base_url}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
