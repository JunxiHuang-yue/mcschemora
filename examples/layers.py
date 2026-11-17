import argparse
import json
from pathlib import Path

from mcschemora import Schematic


def main():
    parser = argparse.ArgumentParser(description="Export every global Y layer as a sprite diagram.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, default=Path("output/layers"))
    args = parser.parse_args()
    scene = Schematic.load(args.source, max_unpacked_bytes=64 * 1024 * 1024)
    ranges = []
    for name in scene.regions:
        region = scene.region(name)
        bounds = region.bounds
        if bounds is not None:
            start = region.to_global(bounds.start)[1]
            ranges.append((start, start + bounds.size[1]))
    if not ranges:
        parser.error("The schematic has no bounded regions.")
    args.output.mkdir(parents=True, exist_ok=True)
    layers = []
    for index, y in enumerate(
        range(min(start for start, _ in ranges), max(end for _, end in ranges))
    ):
        filename = f"layer-{index:03d}-y{y}.png"
        diagnostics = scene.export_sprites(args.output / filename, y=y, grid=True)
        layers.append({"y": y, "file": filename, "diagnostics": diagnostics})
    (args.output / "layers.json").write_text(json.dumps(layers, indent=2) + "\n")
    print(f"Saved {len(layers)} layer diagrams and layers.json to {args.output}")


if __name__ == "__main__":
    main()
