# 3DP MCP Server Agent Instructions

This server provides 40 MCP tools for 3D printing CAD workflows using `build123d`.

## Multi-Agent Guidelines (Jules, Gemini, Claude, Cursor, Windsurf)

- **Skills Directory**: Specialized workflow instructions live in `skills/`:
  - `design-model`: Instructions for creating parametric 3D models using build123d.
  - `modify-model`: Instructions for editing existing CAD geometries.
  - `parametric-components`: Guidelines for reusable parameterized mechanical parts.
  - `mechanical-parts`: Guidelines for fasteners, gears, bearings, and enclosures.
  - `print-prep`: Printability validation, overhang checking, orientation, and slicer prep.
  - `publish-model`: Automated publishing to community platforms.

- **Printer Profile Configuration**:
  When using `analyze_printability` or print analysis tools, reference printer constraints (build volume, nozzle size, layer height) defined in the target environment or `configs/printer_profiles.json`.

- **Supported Export Formats**: `stl`, `step`, `glb`, `3mf`.
