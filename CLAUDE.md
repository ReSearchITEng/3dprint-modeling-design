# CLAUDE.md - Instructions for Claude Code / Claude Desktop

Refer to `AGENTS.md` for overall architecture and multi-agent CAD guidelines.

## Quick Execution Commands
- Build model: `python scripts/build_model.py <model_name>`
- Update phone viewer index: `python scripts/update_viewer_index.py`
- Run test suite: `pytest` or `python -m unittest discover tests`

## Target Printer Defaults
- Default printer: `bambu_x1c` (256x256x256mm, 0.4mm nozzle, 0.2mm layer height)
- Profiles location: `configs/printer_profiles.json`
