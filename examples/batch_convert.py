import argparse
import json
from pathlib import Path

from mcschemora import Schematic


def main():
    parser = argparse.ArgumentParser(description="Convert a directory and report every outcome.")
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--format", choices=("schem", "litematic", "nbt"), default="litematic")
    parser.add_argument("--version")
    parser.add_argument("--flatten", action="store_true")
    parser.add_argument("--allow-loss", action="store_true")
    args = parser.parse_args()
    if not args.source.is_dir() or args.source.resolve() == args.destination.resolve():
        parser.error("Use an input directory and a separate output directory.")
    sources = sorted(
        path
        for path in args.source.iterdir()
        if path.is_file() and path.suffix in {".schem", ".litematic", ".nbt", ".snbt"}
    )
    if not sources:
        parser.error("No supported input files found.")
    args.destination.mkdir(parents=True, exist_ok=True)
    results = []
    for source in sources:
        result = {"source": source.name}
        try:
            scene = Schematic.load(source, max_unpacked_bytes=64 * 1024 * 1024)
            report = scene.check_export(
                format=args.format, version=args.version, flatten=args.flatten
            )
            result.update(
                import_diagnostics=scene.import_diagnostics,
                errors=report.errors,
                losses=report.losses,
            )
            if report.errors or (report.losses and not args.allow_loss):
                result["status"] = "blocked"
            else:
                destination = args.destination / f"{source.name}.{args.format}"
                scene.save(
                    destination,
                    format=args.format,
                    version=args.version,
                    flatten=args.flatten,
                    allow_loss=args.allow_loss,
                )
                result.update(status="saved", output=destination.name)
        except (OSError, ValueError) as error:
            result.update(status="error", message=str(error))
        results.append(result)
        print(f"{source.name}: {result['status']}")
    (args.destination / "report.json").write_text(json.dumps(results, indent=2) + "\n")
    if any(result["status"] != "saved" for result in results):
        raise SystemExit("Some files were not converted; read report.json.")


if __name__ == "__main__":
    main()
