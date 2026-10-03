import os
import sys
import json
import argparse
import build123d as b3d
import trimesh

# Add vendor directory to sys.path so threedp_mcp can be imported if needed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "vendor", "3dp-mcp-server", "src"))

def load_printer_profile(profile_name="bambu_x1c"):
    config_path = os.path.join(os.path.dirname(__file__), "..", "configs", "printer_profiles.json")
    if not os.path.exists(config_path):
        return None
    with open(config_path, "r") as f:
        data = json.load(f)
    return data.get("printers", {}).get(profile_name, data.get("printers", {}).get("bambu_x1c"))

def build_and_export_model(model_name, printer_profile="bambu_x1c"):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_dir = os.path.join(base_dir, "models", model_name)
    model_py = os.path.join(model_dir, "model.py")

    if not os.path.exists(model_py):
        raise FileNotFoundError(f"Model file not found at {model_py}")

    # Dynamically import or execute model.py
    sys.path.insert(0, model_dir)
    import importlib.util
    spec = importlib.util.spec_from_file_location("model_module", model_py)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    if hasattr(mod, "build_model"):
        shape = mod.build_model()
    elif hasattr(mod, "result"):
        shape = mod.result
    else:
        raise AttributeError("model.py must define 'build_model()' function or 'result' variable.")

    # Paths
    output_dir = os.path.join(model_dir, "output")
    renders_dir = os.path.join(model_dir, "renders")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(renders_dir, exist_ok=True)

    # 1. Verification & Dimensions
    bbox = shape.bounding_box()
    size = [bbox.max.X - bbox.min.X, bbox.max.Y - bbox.min.Y, bbox.max.Z - bbox.min.Z]
    volume = shape.volume if hasattr(shape, "volume") else 0.0

    print(f"[{model_name}] Bounding Box Size: {size[0]:.2f} x {size[1]:.2f} x {size[2]:.2f} mm")
    print(f"[{model_name}] Volume: {volume:.2f} mm^3")

    # 2. Printability Check against profile
    profile = load_printer_profile(printer_profile)
    if profile:
        build_vol = profile["build_volume_mm"]
        fits = size[0] <= build_vol[0] and size[1] <= build_vol[1] and size[2] <= build_vol[2]
        print(f"[{model_name}] Fits in target printer ({profile['name']}): {fits}")
        if not fits:
            print(f"WARNING: Model exceeds build volume {build_vol} mm!")

    # 3. Export STEP & STL
    step_path = os.path.join(output_dir, "model.step")
    stl_path = os.path.join(output_dir, "model.stl")
    three_mf_path = os.path.join(output_dir, "model.3mf")
    glb_path = os.path.join(output_dir, "model.glb")

    b3d.export_step(shape, step_path)
    b3d.export_stl(shape, stl_path)

    # Convert STL to 3MF & GLB via Trimesh
    mesh = trimesh.load_mesh(stl_path)
    try:
        mesh.export(three_mf_path)
        print(f"[{model_name}] Exported 3MF to {three_mf_path}")
    except Exception as e:
        print(f"[{model_name}] Could not export 3MF: {e}")

    mesh.export(glb_path)
    print(f"[{model_name}] Exported STEP, STL, GLB to {output_dir}")

    # 4. Render PNG views (ISO, Front, Top, Side)
    try:
        import matplotlib.pyplot as plt

        verts = mesh.vertices
        faces = mesh.faces

        # ISO View
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_trisurf(verts[:, 0], verts[:, 1], verts[:, 2], triangles=faces, cmap='viridis', alpha=0.8)
        ax.set_title(f"{model_name} - ISO View")
        plt.savefig(os.path.join(renders_dir, "iso.png"), bbox_inches='tight')
        plt.close()

        # Front View
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.plot(verts[:, 0], verts[:, 2], 'k.', markersize=0.5)
        ax.set_aspect('equal')
        ax.set_title(f"{model_name} - Front View")
        plt.savefig(os.path.join(renders_dir, "front.png"), bbox_inches='tight')
        plt.close()

        # Top View
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.plot(verts[:, 0], verts[:, 1], 'k.', markersize=0.5)
        ax.set_aspect('equal')
        ax.set_title(f"{model_name} - Top View")
        plt.savefig(os.path.join(renders_dir, "top.png"), bbox_inches='tight')
        plt.close()

        # Side View
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.plot(verts[:, 1], verts[:, 2], 'k.', markersize=0.5)
        ax.set_aspect('equal')
        ax.set_title(f"{model_name} - Side View")
        plt.savefig(os.path.join(renders_dir, "side.png"), bbox_inches='tight')
        plt.close()

        print(f"[{model_name}] Renders saved to {renders_dir}")
    except Exception as e:
        print(f"[{model_name}] Note: Render generation had warning/fallback: {e}")

    return {
        "model_name": model_name,
        "dimensions": size,
        "volume": volume,
        "step": step_path,
        "stl": stl_path,
        "3mf": three_mf_path,
        "glb": glb_path
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build and validate CAD model")
    parser.add_argument("model_name", help="Name of model directory in models/")
    parser.add_argument("--printer", default="bambu_x1c", help="Printer profile to validate against")
    args = parser.parse_args()

    build_and_export_model(args.model_name, args.printer)
