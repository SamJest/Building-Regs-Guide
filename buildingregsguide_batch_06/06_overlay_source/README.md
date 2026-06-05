# Overlay Source

These files are not intended to be pasted blindly over UKPlanningGuide.

Codex should use them as the new sister-site data layer and adapt naming/imports to the new repo.

Suggested destination in new repo:

- `source/data/building_regs_sources.py`
- `source/data/building_regs_approved_documents.py`
- `source/data/building_regs_routes.py`
- `source/data/building_regs_tools.py`
- `source/data/building_regs_download_assets.py`
- `source/data/building_regs_faqs.py`

After import, Codex should write generators/components that follow the UKPlanningGuide architecture.
