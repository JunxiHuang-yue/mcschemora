import argparse
import json
from pathlib import Path

from mcschemora import Schematic


def main():
    parser = argparse.ArgumentParser(
        description="Apply a material profile and compare build costs."
    )
    parser.add_argument("source", type=Path)
    parser.add_argument("profile", type=Path)
    parser.add_argument("--output", type=Path, default=Path("output/restyled"))
    args = parser.parse_args()
    if args.source.resolve().parent == args.output.resolve():
        parser.error("Choose an output directory separate from the input file.")
    scene = Schematic.load(args.source, max_unpacked_bytes=64 * 1024 * 1024)
    before = {
        "materials": scene.material_cost(),
        "values": {profile: scene.value_cost(profile) for profile in ("emc", "essentialsx")},
    }
    args.output.mkdir(parents=True, exist_ok=True)
    before_diagnostics = scene.export_png(args.output / "before.png", size=(800, 600), y=(0, 3))
    changes = scene.normalize(args.profile)
    validation = scene.validate()
    print(validation)
    if validation.errors:
        raise SystemExit("Resolve validation errors before saving the restyled build.")
    after = {
        "materials": scene.material_cost(),
        "values": {profile: scene.value_cost(profile) for profile in ("emc", "essentialsx")},
    }
    scene.save(args.output / "restyled.litematic")
    after_diagnostics = scene.export_png(args.output / "after.png", size=(800, 600), y=(0, 3))
    report = {
        "before": before,
        "after": after,
        "changes": changes,
        "import_diagnostics": scene.import_diagnostics,
        "render_diagnostics": {"before": before_diagnostics, "after": after_diagnostics},
    }
    (args.output / "comparison.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"Replaced {changes['changed']} blocks")
    for profile in ("emc", "essentialsx"):
        previous = before["values"][profile]
        current = after["values"][profile]
        print(f"{profile}: {previous['total']} -> {current['total']}")
        print(f"Unpriced before: {previous['unpriced']}; after: {current['unpriced']}")
    print(f"Render diagnostics: {report['render_diagnostics']}")
    print(f"Saved build, previews, and comparison to {args.output}")


if __name__ == "__main__":
    main()
