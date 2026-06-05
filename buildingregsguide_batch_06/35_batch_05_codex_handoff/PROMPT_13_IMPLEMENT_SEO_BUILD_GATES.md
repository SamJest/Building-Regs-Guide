# Prompt 13: implement SEO build gates

Wire the validation scripts into the build process.

Requirements:

- Validate route path/title/source fields.
- Validate visible official source blocks.
- Catch risky certainty phrases.
- Check Part L/F/HRB source warnings.
- Smoke-test JSON-LD.
- Output validation reports.
- Mark candidate pages noindex when they fail non-critical gates.
- Fail build for core pages with critical errors.
