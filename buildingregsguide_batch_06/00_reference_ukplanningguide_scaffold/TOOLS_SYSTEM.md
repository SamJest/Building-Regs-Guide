# Tools System

Interactive tools are generated as static pages with inline JavaScript.

Key files:

- `source/data/tools_data.py`
- `source/data/custom_tool_configs.py`
- `source/generators/planning_tools.py`
- `source/components/tool_pages.py`
- `source/components/structured_tool_ui.py`
- individual tool components such as planning decision, rejection risk and permitted development calculator files
- `source/scripts/tool_smoke_test.js`
- `source/scripts/tool_mobile_audit.js`

## Tool Pattern

1. Registry defines title, slug, summary, metadata and related routes.
2. Generator creates `/tools/{slug}/`.
3. Component renders a static shell plus inline script.
4. Tool result links point to relevant guide pages.
5. Sitewide JS enhances result capture, printing and return-visit behaviour.
6. Validation checks tool pages have root markers and inline scripts.

## Sister Site Tool Ideas

For BuildingRegsGuide:

- Building control route checker.
- Building notice vs full plans checker.
- Competent person scheme checker.
- Completion certificate readiness checker.
- Project inspection checklist generator.
- Approved Document topic router.
- Extension building regulations prep pack.

Reuse the static interactive pattern, but rewrite the decision logic.
