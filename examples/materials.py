import argparse
import csv
import json
from pathlib import Path

from mcschemora import Schematic


def main():
    parser = argparse.ArgumentParser(description="Export construction materials and values.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, default=Path("output/materials"))
    args = parser.parse_args()
    scene = Schematic.load(args.source, max_unpacked_bytes=64 * 1024 * 1024)
    materials = scene.material_cost()
    values = {profile: scene.value_cost(profile) for profile in ("emc", "essentialsx")}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "materials.json").write_text(json.dumps(materials, indent=2) + "\n")
    (args.output / "values.json").write_text(json.dumps(values, indent=2) + "\n")
    for field, filename in (("items", "materials.csv"), ("raw_materials", "raw-materials.csv")):
        with (args.output / filename).open("w", newline="") as output:
            writer = csv.writer(output)
            writer.writerow(("item", "quantity"))
            writer.writerows(sorted(materials[field].items()))
    for diagnostic in scene.import_diagnostics:
        print(diagnostic)
    print(f"Construction item types: {len(materials['items'])}")
    for profile, report in values.items():
        print(f"{profile}: {report['total']}; unpriced: {report['unpriced']}")
    print(f"Saved material reports to {args.output}")


if __name__ == "__main__":
    main()
