# 3D Print Modeling & Design Workspace

An AI-driven, parametric 3D-printable CAD design workspace built on **build123d** and **3dp-mcp-server**, optimized for phone-to-CAD workflows and Bambu Lab 3D printers.

## Overview

Describing mechanical components in natural language triggers Jules/Gemini to produce parametric CAD models, run geometric verification, perform printer printability analysis, generate 2D/3D renders, export production files (`STEP`, `STL`, `3MF`, `GLB`), and publish the interactive 3D model to a mobile-friendly WebGL viewer on GitHub Pages.

---

## Directory Structure

```text
├── .gitignore
├── AGENTS.md                  # Generic multi-agent guidelines (Jules, Gemini, Claude)
├── CLAUDE.md                  # Claude specific instructions
├── LICENSE
├── README.md
├── index.html                 # Mobile-friendly Three.js 3D web viewer for GitHub Pages
├── configs/
│   └── printer_profiles.json  # Printer specifications (X1C, P1S, P1P, A1, A1 Mini, X1E, X2D, Generic)
├── models/
│   ├── index.json             # Auto-generated model manifest for the 3D viewer
│   └── mounting_plate/        # Example/infrastructure CAD project
│       ├── model.py           # build123d parametric model script
│       ├── parameters.py      # Named dimensional parameters
│       ├── README.md          # Project documentation
│       ├── output/            # Generated model.step, model.stl, model.3mf, model.glb
│       └── renders/           # Orthographic & isometric PNG renders (iso, front, top, side)
├── scripts/
│   ├── build_model.py         # Autonomous build, validation, render, and export engine
│   └── update_viewer_index.py # Manifest generator for GitHub Pages phone viewer
├── tests/
│   └── test_cad_pipeline.py   # Automated unit and schema test suite
└── vendor/
    └── 3dp-mcp-server/        # Embedded 3dp-mcp-server capability layer
```

---

## 3D Viewer on GitHub Pages Setup

The repository is configured to serve the mobile-friendly WebGL 3D viewer directly from the **root** directory.

### One-Time Manual Setup:
1. Open your repository on GitHub: `https://github.com/ReSearchITEng/3dprint-modeling-design`
2. Go to **Settings** > **Pages**.
3. Under **Build and deployment**:
   - **Source**: Select `Deploy from a branch`.
   - **Branch**: Select `main` (or your default branch) and `/ (root)`.
4. Click **Save**.
5. Your interactive phone CAD viewer will be live at:
   `https://researchiteng.github.io/3dprint-modeling-design/`

---

## Usage & Development Workflow

### 1. Build & Validate a Model
To run geometry validation, printability checks, PNG rendering, and produce `STEP`, `STL`, `3MF`, and `GLB` files for a model:

```bash
python3 scripts/build_model.py <model_name> --printer bambu_x1c
```

### 2. Update Phone Viewer Manifest
To update `models/index.json` so the latest CAD models appear in the GitHub Pages mobile viewer:

```bash
python3 scripts/update_viewer_index.py
```

### 3. Run Automated Tests
```bash
python3 -m unittest discover tests
```

---

## Bambu Lab Printer Profiles

Printers and materials are defined in `configs/printer_profiles.json`. Target printers include:
- **Bambu Lab X1 Carbon / P1S / P1P / A1 / X1E**: 256 x 256 x 256 mm build volume
- **Bambu Lab A1 Mini**: 180 x 180 x 180 mm build volume
- **Bambu Lab X2D**: 300 x 300 x 300 mm build volume
- **Generic FDM**: 220 x 220 x 250 mm build volume

Supported material profiles (PLA, PETG, ABS, ASA, TPU) include default shrinkage compensation factors and clearance recommendations.
