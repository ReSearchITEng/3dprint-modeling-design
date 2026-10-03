import os
import json
import glob

def update_index():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_dir = os.path.join(base_dir, "models")
    index_path = os.path.join(models_dir, "index.json")

    models_list = []

    if os.path.exists(models_dir):
        for item in sorted(os.listdir(models_dir)):
            item_path = os.path.join(models_dir, item)
            if os.path.isdir(item_path):
                glb_file = os.path.join(item_path, "output", "model.glb")
                if os.path.exists(glb_file):
                    rel_glb = f"models/{item}/output/model.glb"

                    models_list.append({
                        "id": item,
                        "name": item.replace("_", " ").title(),
                        "glb_path": rel_glb,
                        "step_path": f"models/{item}/output/model.step",
                        "stl_path": f"models/{item}/output/model.stl",
                        "3mf_path": f"models/{item}/output/model.3mf",
                        "dimensions": [60.0, 40.0, 6.0],
                        "renders": [
                            f"models/{item}/renders/iso.png",
                            f"models/{item}/renders/front.png",
                            f"models/{item}/renders/top.png",
                            f"models/{item}/renders/side.png"
                        ]
                    })

    manifest = {
        "updated_at": "2026-10-03T07:00:00Z",
        "models": models_list
    }

    with open(index_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"Updated {index_path} with {len(models_list)} model(s).")

if __name__ == "__main__":
    update_index()
