import argparse
import json
from math import ceil, sqrt
from pathlib import Path

from mcschemora import Schematic, block


def create_tower():
    cells = {}
    palette = {
        name: block(name)
        for name in (
            "brown_concrete",
            "brown_terracotta",
            "dark_oak_planks",
            "dark_oak_fence",
            "smooth_stone",
            "stone_bricks",
            "grass_block",
        )
    }
    profile = ((0, 30), (14, 27), (32, 20), (48, 15), (64, 11), (88, 7), (112, 4), (148, 1))

    def width(y):
        for (bottom, wide), (top, narrow) in zip(profile, profile[1:], strict=False):
            if bottom <= y <= top:
                return wide + (narrow - wide) * (y - bottom) / (top - bottom)
        raise ValueError(f"Height outside tower profile: {y}")

    def line(start, end, material, radius=0):
        steps = max(1, ceil(max(abs(b - a) for a, b in zip(start, end, strict=True)) * 2))
        for step in range(steps + 1):
            x, y, z = (round(a + (b - a) * step / steps) for a, b in zip(start, end, strict=True))
            for dx in range(-radius, radius + 1):
                for dz in range(-radius, radius + 1):
                    cells[(x + dx, y + 4, z + dz)] = palette[material]

    for x in range(-43, 44):
        for z in range(-43, 44):
            lawn = abs(x) > 33 and abs(z) > 33
            border = max(abs(x), abs(z)) in (32, 43) or min(abs(x), abs(z)) == 3
            material = "grass_block" if lawn else "stone_bricks" if border else "smooth_stone"
            cells[(x, 0, z)] = palette[material]
    for sx in (-1, 1):
        for sz in (-1, 1):
            for x in range(sx * 30 - 4, sx * 30 + 5):
                for z in range(sz * 30 - 4, sz * 30 + 5):
                    for y in range(1, 4):
                        cells[(x, y, z)] = palette["stone_bricks"]
            for y in range(148):
                line(
                    (sx * width(y), y, sz * width(y)),
                    (sx * width(y + 1), y + 1, sz * width(y + 1)),
                    "brown_concrete",
                    radius=1 if y < 64 else 0,
                )

    for swap in (False, True):
        for side in (-1, 1):
            for x in range(-28, 28):
                y = 10 + 17 * sqrt(1 - (x / 28) ** 2)
                next_y = 10 + 17 * sqrt(1 - ((x + 1) / 28) ** 2)
                start = (side * width(y), y, x) if swap else (x, y, side * width(y))
                end = (
                    (side * width(next_y), next_y, x + 1)
                    if swap
                    else (x + 1, next_y, side * width(next_y))
                )
                line(start, end, "brown_terracotta", radius=1)
            for bottom in range(32, 144, 8):
                top = min(bottom + 8, 148)
                for direction in (-1, 1):
                    start = (direction * width(bottom), bottom, side * width(bottom))
                    end = (-direction * width(top), top, side * width(top))
                    if swap:
                        start, end = (start[2], start[1], start[0]), (end[2], end[1], end[0])
                    line(start, end, "brown_terracotta")
                start = (-width(bottom), bottom, side * width(bottom))
                end = (width(bottom), bottom, side * width(bottom))
                if swap:
                    start, end = (start[2], start[1], start[0]), (end[2], end[1], end[0])
                line(start, end, "brown_concrete")

    for y, outer, inner in ((32, 23, 16), (64, 14, 7), (136, 4, 0)):
        for x in range(-outer, outer + 1):
            for z in range(-outer, outer + 1):
                distance = max(abs(x), abs(z))
                if distance >= inner:
                    for layer in (y - 1, y):
                        cells[(x, layer + 4, z)] = palette["dark_oak_planks"]
                    if distance == outer or (inner and distance == inner):
                        cells[(x, y + 5, z)] = palette["dark_oak_fence"]
    for y in range(149, 169):
        line((0, y, 0), (0, y + 1, 0), "brown_concrete")

    scene = Schematic.create(version="1.21.1")
    scene.region().set_many(cells)
    scene.repair(rules=["fences"])
    return scene


def main():
    parser = argparse.ArgumentParser(
        description="Generate a Minecraft Eiffel Tower interpretation."
    )
    parser.add_argument("--output", type=Path, default=Path("output/eiffel-tower"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    scene = create_tower()
    validation = scene.validate()
    export = scene.check_export(format="schem")
    if validation.errors or export.errors or export.losses:
        raise SystemExit(f"Validation: {validation}\nExport: {export}")
    scene.save(args.output / "eiffel-tower.schem")
    diagnostics = scene.export_png(args.output / "preview.png", size=(1600, 2000))
    report = {
        "inspection": scene.inspect(),
        "validation": {
            "errors": validation.errors,
            "warnings": validation.warnings,
            "unknown": validation.unknown,
        },
        "render_diagnostics": diagnostics,
    }
    (args.output / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Saved tower, preview, and report to {args.output}")


if __name__ == "__main__":
    main()
