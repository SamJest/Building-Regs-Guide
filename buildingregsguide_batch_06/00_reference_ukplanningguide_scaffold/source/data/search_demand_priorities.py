from __future__ import annotations


HMO_ARTICLE_4_PRIORITY_ROUTES = {
    ("staffordshire", "tamworth"): {
        "query": "tamworth hmo planning permitted development article 4",
        "local_search_slug": "hmo-article-4-tamworth",
        "impressions": 14515,
        "position": 4.09,
    },
    ("staffordshire", "stafford"): {
        "query": "stafford hmo article 4 direction staffordshire 2024 2025",
        "local_search_slug": "hmo-article-4-stafford",
        "impressions": 1487,
        "position": 9.67,
    },
    ("buckinghamshire", "milton-keynes"): {
        "query": "milton keynes article 4 direction hmo areas not covered",
        "local_search_slug": "hmo-article-4-milton-keynes",
        "impressions": 512,
        "position": 11.27,
    },
    ("northamptonshire", "west-northamptonshire"): {
        "query": "northampton hmo article 4 west northamptonshire council",
        "local_search_slug": "hmo-article-4-west-northamptonshire",
        "impressions": 454,
        "position": 9.30,
    },
    ("leicestershire", "charnwood"): {
        "query": "article 4 hmo charnwood loughborough blaby oadby wigston",
        "local_search_slug": "hmo-article-4-charnwood",
        "impressions": 381,
        "position": 10.08,
    },
    ("leicestershire", "blaby"): {
        "query": "article 4 hmo blaby",
        "local_search_slug": "hmo-article-4-blaby",
    },
    ("leicestershire", "harborough"): {
        "query": "article 4 hmo harborough",
        "local_search_slug": "hmo-article-4-harborough",
    },
    ("leicestershire", "oadby-and-wigston"): {
        "query": "article 4 hmo oadby and wigston",
        "local_search_slug": "hmo-article-4-oadby-and-wigston",
    },
    ("warwickshire", "nuneaton-and-bedworth"): {
        "query": "article 4 hmo nuneaton bedworth stratford daventry 2024 2025",
        "local_search_slug": "hmo-article-4-nuneaton-bedworth-warwickshire",
        "impressions": 314,
        "position": 8.35,
    },
}


DATA_LED_LOCAL_SEARCH_SLUGS = tuple(
    sorted(
        {
            route["local_search_slug"]
            for route in HMO_ARTICLE_4_PRIORITY_ROUTES.values()
            if route.get("local_search_slug")
        }
        | {
            "hmo-article-4-leicestershire",
            "hmo-article-4-milton-keynes",
            "hmo-article-4-west-northamptonshire",
            "hmo-article-4-nuneaton-bedworth-warwickshire",
            "planning-permission-newham",
            "westminster-conservation-areas",
            "planning-permission-eastleigh",
            "outbuildings-glasgow-city",
        }
    )
)


CTR_RESCUE_LOCAL_SEARCH_SLUGS = tuple(
    sorted(
        {
            "hmo-article-4-tamworth",
            "hmo-article-4-stafford",
            "hmo-article-4-milton-keynes",
            "hmo-article-4-west-northamptonshire",
            "hmo-article-4-charnwood",
            "hmo-article-4-leicestershire",
            "hmo-article-4-nuneaton-bedworth-warwickshire",
            "outbuildings-glasgow-city",
            "westminster-conservation-areas",
            "planning-permission-newham",
        }
    )
)


LOW_CTR_PAGE_TARGETS = (
    "/conservation-areas/glasgow-city/",
    "/councils/sheffield/",
    "/local-search/outbuildings-glasgow-city/",
    "/councils/aberdeen-city/",
    "/outbuildings/scotland/east-lothian/",
    "/local-search/westminster-conservation-areas/",
    "/councils/croydon/",
    "/conservation-areas/portsmouth/",
    "/driveways/greater-london/barking-and-dagenham/",
    "/outbuildings/greater-london/brent/article-4/",
    "/planning-permission/carmarthenshire/",
)


def hmo_article_4_priority_for(county_slug: str, town_slug: str) -> dict:
    return HMO_ARTICLE_4_PRIORITY_ROUTES.get((county_slug, town_slug), {})
