# AGENTS.md - Guidelines for AI CAD Agents (Jules, Gemini, Claude, etc.)

This repository is an AI-driven, parametric 3D-printable CAD design environment built on **build123d** and **3dp-mcp-server**.

## Core Philosophy

1. **Parametric Source of Truth**: All CAD models must be defined as parametric Python code (`build123d`) in their dedicated directory under `models/<model_name>/`.
2. **Clean Project Structure**:
   ```
   models/
     <model_name>/
       parameters.py   # Parameter definitions (named variables, tolerances, dimensions)
       model.py        # build123d modeling function returning Part/Assembly
       README.md       # Description, parameter table, assembly instructions
       renders/        # High quality PNG renders (iso, front, top, side)
       output/         # STEP, STL, 3MF, and GLB files
   ```
3. **Agent Iteration Loop**:
   - Step 1: Parse requirements and set parameters in `parameters.py`.
   - Step 2: Implement model in `model.py` using `build123d`.
   - Step 3: Verify geometry validity and check bounding box dimensions.
   - Step 4: Run printability analysis against target printer profile in `configs/printer_profiles.json` (overhangs, wall thickness, build volume).
   - Step 5: Render orthographic & isometric PNG views to verify visual appearance.
   - Step 6: Export CAD deliverables (`.step`, `.stl`, `.3mf`, `.glb`).
   - Step 7: Update `models/index.json` or run `python scripts/update_viewer_index.py` so the phone viewer updates automatically.

4. **Printer Profile Awareness**:
   - Target printer settings are specified in `configs/printer_profiles.json`. Default targets are Bambu printers (X1C, P1S, P1P, A1, A1 Mini, X1E, X2D).
   - Ensure component dimensions fit within the target printer's `build_volume_mm`.
   - Use recommended tolerances (`recommended_tolerance_mm`) for mechanical interlock fits (snap-fits, dovetails, clearance holes).

5. **Multi-Agent Compatibility**:
   - Follow standard Python code practices.
   - Do not rely exclusively on proprietary vendor features; ensure python scripts can be executed directly via standard CLI (`python scripts/build_model.py <model_name>`).
