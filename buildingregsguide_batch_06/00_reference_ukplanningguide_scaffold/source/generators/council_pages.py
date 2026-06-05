from pathlib import Path

from components.editorial_authority import build_editorial_authority_block
from components.landing_cta import build_council_landing_handoff
from components.official_sources import build_official_sources_block
from components.seo import build_council_metadata
from core.paths import OUTPUT_FOLDER, BASE_URL
from core.files import write_file
from core.render import inject_into_base

from data.loaders import load_projects, load_councils, load_rule

from utils.random_tools import page_rng
from components.planning_helpers import first_text, restriction_messages

from utils.council_config import load_scenarios
from components.council_sections import *

from utils.random_tools import get_month_year

def generate_council_pages():

    print("Generating council pages")

    projects = load_projects()
    councils_by_county = load_councils()
    scenarios = load_scenarios()

    councils_folder = OUTPUT_FOLDER / "councils"
    councils_folder.mkdir(parents=True, exist_ok=True)
    priority_project_slugs = [
        "garden-rooms",
        "fences-and-walls",
        "outbuildings",
        "house-extensions",
        "dropped-kerbs",
        "loft-conversions",
    ]

    for county_slug, councils in councils_by_county.items():

        county_name = county_slug.replace("-", " ").title()

        for council in councils:

            town_slug = council["town_slug"]
            town_name = council["town_name"]

            page_rng("council", county_slug, town_slug)

            folder = councils_folder / town_slug
            folder.mkdir(parents=True, exist_ok=True)

            priority_project_checks = []
            restriction_checks = []

            for project in projects:
                if project["slug"] not in priority_project_slugs:
                    continue

                rule = load_rule(project["slug"], county_slug, town_slug)
                summary = first_text(
                    rule.get("permitted_development", ""),
                    f"Start with the local {project['short_name'].lower()} guide for the main planning route and any local restrictions.",
                )
                priority_project_checks.append(
                    {
                        "title": project["short_name"],
                        "href": f"/{project['slug']}/{county_slug}/{town_slug}/",
                        "summary": summary,
                    }
                )

                for label, text in restriction_messages(rule):
                    if (label, text) not in restriction_checks:
                        restriction_checks.append((label, text))

            content = assemble_council_page([
                build_council_hero(town_name, county_name),
                build_council_jurisdiction_notice(town_name, county_slug),
                build_council_jump_links(town_name),
                build_local_decision_summary(town_name, county_name, priority_project_checks, restriction_checks),
                build_council_landing_handoff(
                    town_slug,
                    town_name,
                    priority_project_checks[0]["href"] if priority_project_checks else "",
                    priority_project_checks[0]["title"] if priority_project_checks else "the strongest local project guide",
                ),
                build_editorial_authority_block(
                    f"/councils/{town_slug}/",
                    page_family="council",
                    authority_slug=town_slug,
                    country_slug=council.get("country_slug", ""),
                ),
                build_start_here_section(town_name, county_slug, town_slug, priority_project_checks),
                build_priority_project_checks(priority_project_checks, town_name),
                build_project_navigation(projects, town_name, county_slug, town_slug),
                build_common_planning_topics(projects, scenarios, county_slug, town_slug, town_name),
                build_planning_process_section(town_name),
                build_local_planning_context(town_name, county_name),
                build_planning_examples(town_name),
                build_local_authority_faq(town_name, restriction_checks, priority_project_checks),
                build_council_conversion_hook(town_name, priority_project_checks),
                build_scenario_links(projects, scenarios, county_slug, town_slug, town_name),
                build_nearby_council_links(councils_by_county, county_slug, town_slug),
                build_related_projects(projects),
                build_official_sources_block(
                    page_family="council",
                    authority_slug=town_slug,
                    country_slug=council.get("country_slug", ""),
                ),
                build_trust_section(town_name, county_name),
                f"<div class='last-updated'>Updated {get_month_year()}</div>",
            ])
            title, description = build_council_metadata(
                town_name,
                priority_project_checks,
                restriction_checks,
            )

            html = inject_into_base(
                title=title,
                content=content,
                options={
                    "breadcrumbs": [("Home", "/"), ("Councils", "/councils/"), (town_name, "")],
                    "schema": None,
                    "navigation_links": "",
                    "year": get_month_year().split()[-1],
                },
                canonical_url=f"{BASE_URL}/councils/{town_slug}/",
                meta_description=description,
            )

            write_file(folder, "index.html", html)

    print("Council pages generated successfully")
