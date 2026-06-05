# Robots policy

Recommended initial `/robots.txt`:

```txt
User-agent: *
Disallow: /api/
Disallow: /print/
Disallow: /dashboard/state/
Disallow: /*?print=1
Allow: /
Sitemap: https://buildingregsguide.co.uk/sitemap.xml
```

Do not block `/downloads/` landing pages. Do block raw state, print and internal API routes.
