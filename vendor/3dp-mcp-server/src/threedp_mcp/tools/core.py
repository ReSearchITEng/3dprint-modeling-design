<<<<<<< SEARCH
        try:
            if fmt == "stl":
                from build123d import export_stl

                export_stl(model["shape"], out_path)
            elif fmt == "step":
                from build123d import export_step

                export_step(model["shape"], out_path)
            elif fmt == "3mf":
                from build123d import export_3mf

                export_3mf(model["shape"], out_path)
            else:
                return json.dumps(
                    {"success": False, "error": f"Unsupported format '{fmt}'. Must be stl, step, or 3mf."}
                )
=======
        try:
            if fmt == "stl":
                from build123d import export_stl

                export_stl(model["shape"], out_path)
            elif fmt == "step":
                from build123d import export_step

                export_step(model["shape"], out_path)
            elif fmt == "glb":
                # Export STL first, then convert via trimesh to GLB
                from build123d import export_stl
                import trimesh

                temp_stl = os.path.join(model_dir, f"_temp_{name}.stl")
                export_stl(model["shape"], temp_stl)
                mesh = trimesh.load_mesh(temp_stl)
                mesh.export(out_path)
                if os.path.exists(temp_stl):
                    os.remove(temp_stl)
            elif fmt == "3mf":
                from build123d import export_stl
                import trimesh

                temp_stl = os.path.join(model_dir, f"_temp_{name}.stl")
                export_stl(model["shape"], temp_stl)
                mesh = trimesh.load_mesh(temp_stl)
                mesh.export(out_path)
                if os.path.exists(temp_stl):
                    os.remove(temp_stl)
            else:
                return json.dumps(
                    {"success": False, "error": f"Unsupported format '{fmt}'. Must be stl, step, glb, or 3mf."}
                )
>>>>>>> REPLACE