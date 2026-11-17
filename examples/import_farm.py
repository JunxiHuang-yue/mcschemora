import argparse
import json
from pathlib import Path

from mcschemora import Schematic


def main():
    parser = argparse.ArgumentParser(description="Inspect and render a downloaded Litematica farm.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, default=Path("output/imported-farm"))
    args = parser.parse_args()
    scene = Schematic.load(args.source, max_unpacked_bytes=64 * 1024 * 1024)
    inspection = scene.inspect()
    validation = scene.validate()
    args.output.mkdir(parents=True, exist_ok=True)
    diagnostics = scene.export_png(args.output / "preview.png", size=(1400, 1200))
    report = {
        "inspection": inspection,
        "import_diagnostics": scene.import_diagnostics,
        "validation": {
            "errors": validation.errors,
            "warnings": validation.warnings,
            "unknown": validation.unknown,
        },
        "render_diagnostics": diagnostics,
    }
    (args.output / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Loaded Java {scene.version}: {inspection['regions']}")
    print(f"Validation: {validation}")
    print(f"Render diagnostics: {diagnostics}")
    print(f"Saved preview and report to {args.output}")


if __name__ == "__main__":
    main()
