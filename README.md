# BuildingRegsGuide Starter

Static-first starter site for `buildingregsguide.co.uk`, built as a sister site to `ukplanningguide.co.uk`.

The extracted `buildingregsguide_batch_06/` folder is the source handoff pack. The working starter build is generated from the phase-1 launch queue in that pack.

## Build

Use the bundled Codex Python runtime on this machine:

```powershell
& 'C:\Users\Jest\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' build_site.py
```

This produces production output for `https://buildingregsguide.co.uk`, including `CNAME`.

## Preview Build

Before the domain is connected, build a no-crawl preview with:

```powershell
$env:BRG_ENV='preview'
$env:BRG_BASE_URL='https://your-preview-url.example'
& 'C:\Users\Jest\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' build_site.py
```

Preview mode writes `robots.txt` with `Disallow: /` and does not write `CNAME`.

Clear the environment variables before a production build:

```powershell
Remove-Item Env:\BRG_ENV
Remove-Item Env:\BRG_BASE_URL
```

## Validate

```powershell
& 'C:\Users\Jest\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' validate.py
& 'C:\Users\Jest\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' prelaunch_check.py
```

## GitHub Pages Deployment

The repository includes `.github/workflows/pages.yml`. It builds the static site, runs both validation gates, uploads `output/` as the GitHub Pages artifact root, deploys it, then checks the live production URLs.

In GitHub repository settings, set **Pages -> Build and deployment -> Source** to **GitHub Actions**. That makes `https://buildingregsguide.co.uk/` serve the generated site root instead of the repository README.

The generated site is also mirrored at the repository root as a GitHub Pages branch-source fallback. This prevents GitHub Pages from rendering `README.md` if the repository is temporarily set to branch deployment.

After deployment, run:

```powershell
python live_check.py --base-url https://buildingregsguide.co.uk
```

## Output

Generated static files are written to `output/`.

Included in this starter pass:

- Phase-1 launch pages, tools and printable downloads
- Source/version panels
- Client-side route checker logic
- Local-only dashboard using browser localStorage
- Search page and `search-index.json`
- `sitemap.xml`, `robots.txt`, `CNAME` and `.nojekyll`
- `/about/`, `/legal/` and `404.html`
- Build report at `output/BUILD_REPORT.md`

Domain launch steps are in `DOMAIN_LAUNCH_CHECKLIST.md`.
