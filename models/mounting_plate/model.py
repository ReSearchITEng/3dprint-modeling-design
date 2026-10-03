import build123d as b3d
from parameters import LENGTH, WIDTH, THICKNESS, HOLE_DIAMETER, HOLE_SPACING, CORNER_RADIUS

def build_model():
    """Builds a 60 x 40 x 6 mm mounting plate with two 5mm through holes 40 mm apart."""
    with b3d.BuildPart() as part:
        # Base plate
        b3d.Box(LENGTH, WIDTH, THICKNESS)

        # Rounded vertical corners
        b3d.fillet(part.edges().filter_by(b3d.Axis.Z), radius=CORNER_RADIUS)

        # Through holes centered 40mm apart along X axis
        with b3d.Locations((-HOLE_SPACING / 2.0, 0, 0), (HOLE_SPACING / 2.0, 0, 0)):
            b3d.Cylinder(radius=HOLE_DIAMETER / 2.0, height=THICKNESS * 2.0, mode=b3d.Mode.SUBTRACT)

    return part.part

if __name__ == "__main__":
    shape = build_model()
    print("Mounting plate built successfully!")
    print(f"Bounding box: {shape.bounding_box()}")
