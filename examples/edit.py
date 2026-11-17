import argparse
from pathlib import Path

from mcschemora import Schematic, block


def main():
    parser = argparse.ArgumentParser(description="Copy, rotate, and restyle the workshop.")
    parser.add_argument("source", type=Path, help="Workshop schematic created by build.py")
    parser.add_argument("--output", type=Path, default=Path("output"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    schematic = Schematic.load(args.source)
    area = schematic.region().select(start=(0, 0, 0), size=(7, 5, 7))
    copy = area.duplicate(offset=(10, 0, 0))
    copy.rotate(steps=1)
    copy.replace("oak_log", block("birch_log", axis="y"))
    print(f"Original bounds: {area.bounds}")
    print(f"Copy bounds: {copy.bounds}")
    print(f"Birch logs: {copy.counts()['minecraft:birch_log[axis=y]']}")
    print(schematic.validate())
    schematic.save(args.output / "workshops.schem")
    diagnostics = schematic.export_png(args.output / "workshops.png", size=(1200, 600), y=(0, 3))
    print("Saved workshops.schem and workshops.png")
    for diagnostic in diagnostics:
        print(diagnostic)


if __name__ == "__main__":
    main()
