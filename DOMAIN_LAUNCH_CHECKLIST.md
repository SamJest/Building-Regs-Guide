# BuildingRegsGuide Domain Launch Checklist

Use this when `buildingregsguide.co.uk` has been purchased.

## Before DNS

1. Build production output:

```powershell
& 'C:\Users\Jest\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' build_site.py
```

2. Run both gates:

```powershell
& 'C:\Users\Jest\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' validate.py
& 'C:\Users\Jest\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' prelaunch_check.py
```

3. Upload `output/` to a preview/staging host first.

## Preview Build Option

For a preview host before the domain is connected, build with noindex robots and no CNAME:

```powershell
$env:BRG_ENV='preview'
$env:BRG_BASE_URL='https://your-preview-url.example'
& 'C:\Users\Jest\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' build_site.py
```

Then clear those variables before the production build:

```powershell
Remove-Item Env:\BRG_ENV
Remove-Item Env:\BRG_BASE_URL
```

## DNS And Host

- Add `buildingregsguide.co.uk` to the hosting provider.
- Add `www.buildingregsguide.co.uk` if the provider supports it.
- Choose one canonical host and redirect the other.
- Confirm HTTPS certificate issuance before sharing the site.
- Confirm `/sitemap.xml`, `/robots.txt`, `/search-index.json`, `/404.html`, `/legal/` and `/about/` work live.

## After Production

- Submit `https://buildingregsguide.co.uk/sitemap.xml` in Google Search Console.
- Check that production `robots.txt` allows crawling.
- Check Search Console coverage after indexing starts.
- Keep UKPlanningGuide cross-links helpful and limited to planning permission/permitted development topics.
