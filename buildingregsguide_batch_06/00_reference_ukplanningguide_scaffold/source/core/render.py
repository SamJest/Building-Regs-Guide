import re
from datetime import datetime
from html import escape

from components.page_authority import build_authority_schema_bundle, build_page_trust_strip
from components.seo import refine_metadata, render_schema_markup
from components.shared_components import render_tool_ui_templates
from components.upgrade_components import build_sticky_action_bar
from core.paths import TEMPLATES_FOLDER
from utils.copy_tone import polish_html_copy


def _normalize_href(href: str) -> str:
    clean = str(href or "").strip()
    if not clean or clean.startswith(("http://", "https://", "#", "/")):
        return clean
    return "/" + clean.lstrip("/")


def _render_breadcrumbs(breadcrumbs) -> str:
    if not breadcrumbs:
        return ""

    if isinstance(breadcrumbs, str):
        return breadcrumbs

    parts = []
    for label, href in breadcrumbs:
        text = escape(str(label))
        if href:
            parts.append(f'<a href="{escape(_normalize_href(href), quote=True)}">{text}</a>')
        else:
            parts.append(f"<span>{text}</span>")

    if not parts:
        return ""

    return '<nav class="breadcrumbs" aria-label="Breadcrumbs">' + "".join(parts) + "</nav>"


def _is_inner_page(canonical_url: str) -> bool:
    clean = str(canonical_url or "").strip().rstrip("/")
    if not clean:
        return False
    return clean != "https://ukplanningguide.co.uk"


def _render_trust_strip(year) -> str:
    month_year = datetime.now().strftime("%B %Y")
    return (
        '<div class="page-trust-strip" data-nosnippet>'
        '<div class="page-trust-strip-heading">'
        "<strong>Editorially checked</strong>"
        "<span>Visible ownership, review date and source footing for this page.</span>"
        "</div>"
        '<div class="page-trust-strip-items">'
        f"<span><strong>Last reviewed</strong>{month_year}</span>"
        "<span><strong>Source footing</strong>National planning guidance, local context and page-specific tripwires.</span>"
        "<span><strong>Verify before spending</strong>Use a formal check when the proposal is close to a limit or affected by special controls.</span>"
        "</div>"
        "</div>"
    )


def _render_social_meta(title: str, meta_description: str, canonical_url: str) -> str:
    if not title and not meta_description and not canonical_url:
        return ""

    og_type = "website" if not _is_inner_page(canonical_url) else "article"
    tags = [
        ('property', 'og:site_name', "UK Planning Guide"),
        ('property', 'og:title', title),
        ('property', 'og:description', meta_description),
        ('property', 'og:url', canonical_url),
        ('property', 'og:type', og_type),
        ('name', 'twitter:card', "summary"),
        ('name', 'twitter:title', title),
        ('name', 'twitter:description', meta_description),
    ]

    lines = []
    for attr_name, attr_value, content in tags:
        if not content:
            continue
        lines.append(
            f'<meta {attr_name}="{escape(str(attr_value), quote=True)}" content="{escape(str(content), quote=True)}">'
        )

    return "\n".join(lines)


def inject_into_base(
    title,
    content,
    options=None,
    canonical_url="",
    meta_description="",
):
    template = (TEMPLATES_FOLDER / "base.html").read_text(encoding="utf-8")
    options = options or {}
    title, meta_description = refine_metadata(title or "", meta_description or "", canonical_url or "")
    content = content or ""
    if _is_inner_page(canonical_url):
        content = (build_page_trust_strip(canonical_url) or _render_trust_strip(options.get("year"))) + content
    breadcrumbs = options.get("breadcrumbs")
    extra_schema = (
        options.get("schema")
        or options.get("structuredData")
        or options.get("structured_data")
    )
    authority_schema = build_authority_schema_bundle(canonical_url or "", title or "", meta_description or "")
    if extra_schema:
        if isinstance(extra_schema, list):
            extra_schema = authority_schema + extra_schema
        else:
            extra_schema = authority_schema + [extra_schema]
    else:
        extra_schema = authority_schema
    schema = render_schema_markup(
        title or "",
        canonical_url or "",
        meta_description or "",
        breadcrumbs=breadcrumbs,
        extra_schema=extra_schema,
    )

    replacements = {
        "title": escape(title or ""),
        "meta_description": escape(meta_description or ""),
        "social_meta_tags": _render_social_meta(title or "", meta_description or "", canonical_url or ""),
        "meta_robots_tag": (
            f'<meta name="robots" content="{escape(str(options.get("meta_robots") or ""), quote=True)}">'
            if options.get("meta_robots")
            else ""
        ),
        "canonical": escape(canonical_url or "", quote=True),
        "schema": schema,
        "breadcrumbs": _render_breadcrumbs(breadcrumbs),
        "navigation_links": options.get("navigation_links", "") or "",
        "content": (content or "") + (build_sticky_action_bar() if _is_inner_page(canonical_url) else ""),
        "year": str(options.get("year") or datetime.now().year),
        "tool_ui_components": render_tool_ui_templates(),
    }

    html = template
    for key, value in replacements.items():
        html = html.replace(f"{{{{{key}}}}}", value)

    return polish_html_copy(re.sub(r"\{\{.*?\}\}", "", html))
