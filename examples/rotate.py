import argparse
from pathlib import Path

from mcschemora import Schematic


def main():
    parser = argparse.ArgumentParser(
        description="Rotate a single-region build and save its blocks."
    )
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, default=Path("output/rotated"))
    args = parser.parse_args()
    scene = Schematic.load(args.source, max_unpacked_bytes=64 * 1024 * 1024)
    if len(scene.regions) != 1:
        parser.error("This example rotates one region; select a single-region input.")
    if args.source.resolve() == (args.output / "rotated.litematic").resolve():
        parser.error("The output must differ from the input.")
    region = scene.region(scene.regions[0])
    bounds = region.bounds
    if bounds is None:
        parser.error("The input region is empty.")
    area = region.select(start=bounds.start, size=bounds.size)
    area.rotate(steps=1)
    report = scene.validate()
    print(report)
    if report.errors:
        raise SystemExit("Resolve validation errors before saving the rotated build.")
    args.output.mkdir(parents=True, exist_ok=True)
    scene.save(args.output / "rotated.litematic")
    diagnostics = scene.export_png(args.output / "rotated.png", size=(800, 600), y=(0, 3))
    print(f"Saved rotated blocks to {args.output}")
    for diagnostic in diagnostics:
        print(diagnostic)


if __name__ == "__main__":
    main()
