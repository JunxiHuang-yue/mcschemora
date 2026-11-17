import argparse
import random
from math import sin
from pathlib import Path

from mcschemora import Schematic, block


def create_pavilion():
    scene = Schematic.create(version="1.21.1")
    region = scene.region()
    rng = random.Random(42)
    palette = {
        name: block(name)
        for name in (
            "stone",
            "andesite",
            "mossy_cobblestone",
            "grass_block",
            "moss_block",
            "stone_bricks",
            "spruce_planks",
            "dark_prismarine",
            "air",
        )
    }
    cells = {}
    surfaces = {}
    for x in range(1, 30):
        for z in range(1, 29):
            outline = ((x - 15) / 15) ** 2 + ((z - 15) / 14) ** 2
            if outline > 1 + 0.06 * sin(x * 1.7 + z):
                continue
            mountain = max(0, 1 - ((x - 23) / 9) ** 2 - ((z - 8) / 9) ** 2)
            height = 2 + int(2 * (1 - min(outline, 1)) + 10 * mountain**1.6)
            if 5 <= x <= 19 and 9 <= z <= 22:
                height = min(height, 5)
            if 20 <= x <= 28 and 14 <= z <= 24:
                height = 2
            surfaces[(x, z)] = height
            for y in range(height + 1):
                name = rng.choice(("stone", "stone", "andesite", "mossy_cobblestone"))
                if y == height:
                    name = "moss_block" if mountain > 0.3 else "grass_block"
                cells[(x, y, z)] = palette[name]
    region.set_many(cells)

    region.select(start=(6, 5, 10), size=(13, 3, 12)).fill(palette["stone_bricks"])
    region.select(start=(7, 7, 11), size=(11, 1, 10)).fill(palette["spruce_planks"])
    for x, z in ((7, 11), (17, 11), (7, 20), (17, 20)):
        region.select(start=(x, 8, z), size=(1, 5, 1)).fill(block("spruce_log", axis="y"))
    for z in (11, 20):
        region.select(start=(7, 12, z), size=(11, 1, 1)).fill(block("spruce_log", axis="x"))
    for x in (7, 17):
        region.select(start=(x, 12, 11), size=(1, 1, 10)).fill(block("spruce_log", axis="z"))

    roof = []
    for x in range(5, 20):
        y = 19 - abs(x - 12)
        material = (
            palette["dark_prismarine"]
            if x == 12
            else block("dark_prismarine_stairs", facing="east" if x < 12 else "west")
        )
        roof.extend(((x, y, z), material) for z in range(9, 23))
    region.set_many(roof)
    region.set((12, 11, 20), block("lantern", hanging=True))

    for z in range(22, 28):
        height = 28 - z
        region.select(start=(11, 0, z), size=(3, height, 1)).fill(palette["stone_bricks"])
        region.select(start=(11, height, z), size=(3, 1, 1)).fill(
            block("stone_brick_stairs", facing="north")
        )
        region.select(start=(11, height + 1, z), size=(3, 6, 1)).fill(palette["air"])
    for x in range(14, 23):
        for z in range(25, 27):
            region.set((x, surfaces[(x, z)], z), palette["stone_bricks"])

    water = block("water", level=0)
    falling_water = block("water", level=8)
    region.select(start=(20, 2, 14), size=(9, 1, 11)).fill(palette["stone_bricks"])
    region.select(start=(21, 3, 15), size=(7, 1, 9)).fill(water)
    for x in range(22, 25):
        for z in range(8, 14):
            region.select(start=(x, 12, z), size=(1, 4, 1)).fill(palette["air"])
            region.set((x, 11, z), palette["stone"])
            region.set((x, 12, z), water)
        region.select(start=(x, 3, 13), size=(1, 9, 1)).fill(palette["stone"])
        region.select(start=(x, 4, 14), size=(1, 9, 1)).fill(falling_water)
    for x in (21, 25):
        region.select(start=(x, 12, 8), size=(1, 1, 6)).fill(palette["mossy_cobblestone"])

    leaves = block("azalea_leaves", persistent=True)
    for x, z, height in ((4, 9, 7), (7, 5, 6), (27, 7, 6)):
        ground = surfaces[(x, z)]
        region.select(start=(x, ground + 1, z), size=(1, height, 1)).fill(
            block("spruce_log", axis="y")
        )
        foliage = []
        for rise in range(3, height + 2):
            radius = max(0, (height + 1 - rise) // 2)
            for dx in range(-radius, radius + 1):
                for dz in range(-radius, radius + 1):
                    if abs(dx) + abs(dz) <= radius + 1 and (dx or dz or rise > height):
                        foliage.append(((x + dx, ground + rise, z + dz), leaves))
        region.set_many(foliage)
    return scene


def main():
    parser = argparse.ArgumentParser(description="Build and render a mountain pavilion.")
    parser.add_argument("--output", type=Path, default=Path("output"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    scene = create_pavilion()
    report = scene.validate()
    print(report)
    if report.errors:
        raise SystemExit("Resolve validation errors before exporting.")
    diagnostics = scene.export_png(args.output / "pavilion.png", size=(1400, 1100))
    print(f"Render diagnostics: {diagnostics}")
    export = scene.check_export(format="schem")
    print(f"Export report: {export}")
    if export.errors or export.losses:
        raise SystemExit("Review export errors and losses before saving.")
    scene.save(args.output / "pavilion.schem")
    print(f"Saved {args.output / 'pavilion.schem'} and {args.output / 'pavilion.png'}")


if __name__ == "__main__":
    main()
