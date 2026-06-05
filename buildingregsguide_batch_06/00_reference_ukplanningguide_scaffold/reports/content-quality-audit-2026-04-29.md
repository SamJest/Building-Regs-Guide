# Content Quality Audit

Date: 2026-04-29

## Verdict

Do not add another 10,000 pages yet.

The current generated estate is useful and technically substantial, but it is not at the quality level where another large programmatic expansion should be pushed without a cleanup pass first.

## What Looks Strong

- Current generated output: 34,106 `index.html` pages.
- Existing long-tail expansion report shows the previous expansion added 10,131 pages and passed link, sitemap, metadata and content validation.
- Most sampled pages have meaningful local framing, official source links, next-step CTAs and project/rule-specific sections.
- A quick rendered-output scan found very few genuinely short pages:
  - minimum visible text: 416 words
  - 10th percentile: 2,954 words
  - median: 3,293 words
  - 90th percentile: 4,260 words
  - pages under 600 words: 2, both non-core utility/legal pages
- Meta descriptions are mostly unique in the generated output.

## Quality Risks Found

- 32,543 pages contained adjacent duplicated source-footing paragraphs in the editorial authority block.
- Several title families are duplicated or awkward, especially project names reduced to partial words such as:
  - `side in ...: extension local checks`
  - `dropped in ...: kerb local checks`
  - `garage in ...`
- Some generated grammar still reads template-like, for example:
  - `boundary distance rules is the live blocker`
  - `distance from boundary ... looks like the rule`
- The existing project reports already warn that family-repetition is the next quality pass target, especially for older high-scale families.
- The full built-in duplicate/content validation is too slow to complete quickly against 34k pages in this session, which means the audit tooling should be tightened before scaling again.

## Recommendation

Scale only after a content-quality pass, not immediately.

Best next batch:

1. Fix repeated editorial/source copy across generated pages.
2. Fix title generation for `side-extensions`, `dropped-kerbs`, `garage-conversions` and other compound project names.
3. Fix singular/plural grammar in scenario hero copy.
4. Rebuild and rerun metadata/content validation.
5. Add the next long-tail batch in a smaller 2k-3k test slice first, then monitor indexing and CTR before committing to the full extra 10k.

## Change Made During This Audit

- Patched `components/editorial_authority.py` so the source-footing reason no longer falls back to the same source-basis text and renders a duplicate paragraph.
