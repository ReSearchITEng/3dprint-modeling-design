import unittest
import os
import sys
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)

from scripts.build_model import build_and_export_model

class TestCadPipeline(unittest.TestCase):

    def test_mounting_plate_build(self):
        result = build_and_export_model("mounting_plate", printer_profile="bambu_x1c")

        self.assertEqual(result["model_name"], "mounting_plate")
        self.assertAlmostEqual(result["dimensions"][0], 60.0, delta=0.1)
        self.assertAlmostEqual(result["dimensions"][1], 40.0, delta=0.1)
        self.assertAlmostEqual(result["dimensions"][2], 6.0, delta=0.1)

        # Check export files exist and are non-empty
        for key in ["step", "stl", "3mf", "glb"]:
            path = result[key]
            self.assertTrue(os.path.exists(path), f"Missing export file: {path}")
            self.assertGreater(os.path.getsize(path), 0, f"Empty export file: {path}")

        # Check renders exist
        renders_dir = os.path.join(base_dir, "models", "mounting_plate", "renders")
        for view in ["iso.png", "front.png", "top.png", "side.png"]:
            render_path = os.path.join(renders_dir, view)
            self.assertTrue(os.path.exists(render_path), f"Missing render: {render_path}")

    def test_printer_profiles(self):
        config_path = os.path.join(base_dir, "configs", "printer_profiles.json")
        self.assertTrue(os.path.exists(config_path))
        with open(config_path, "r") as f:
            data = json.load(f)

        printers = data.get("printers", {})
        self.assertIn("bambu_x1c", printers)
        self.assertIn("bambu_x2d", printers)
        self.assertIn("generic_fdm", printers)

if __name__ == "__main__":
    unittest.main()
