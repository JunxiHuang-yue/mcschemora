"""Check an installed package and its prepared offline cache.

Run with an isolated interpreter outside the checkout. Optional --visuals also
downloads the shared visual bundle and checks textured rendering offline.
"""

import argparse
from importlib.metadata import version
from importlib.resources import files
from pathlib import Path
from tempfile import TemporaryDirectory

from mcschemora import MinecraftData, Schematic, __version__, block, chest, inspect_schematics, item


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--visuals", action="store_true")
    args = parser.parse_args()
    assert __version__ == version("mcschemora")
    resources = files("mcschemora")
    for name in ("py.typed", "_core.pyi", "licenses/LICENSE", "licenses/NOTICE"):
        assert resources.joinpath(name).is_file(), name

    with TemporaryDirectory(prefix="mcschemora-check-") as temporary:
        directory = Path(temporary)
        cache = directory / "cache"
        try:
            MinecraftData(cache_dir=cache, offline=True).prepare("1.21.1")
        except ValueError as error:
            assert "offline" in str(error).lower(), str(error)
        else:
            raise AssertionError("An empty offline cache must report missing catalogs")

        online = MinecraftData(cache_dir=cache)
        assert online.prepare("1.21.1", target="1.20.4", visuals=args.visuals) == "1.21.1"
        assert online.prepare("1.20.4", target="1.21.1") == "1.20.4"
        offline = MinecraftData(cache_dir=cache, offline=True)
        assert offline.prepare("1.21.1", target="1.20.4", visuals=args.visuals) == "1.21.1"
        schematic = Schematic.create(version="1.21.1", data=offline)
        region = schematic.region()
        region.set((0, 0, 0), block("stone"))
        region.place(chest(items={0: item("diamond", count=3)}), at=(1, 0, 0))

        for format in ("schem", "schem2", "litematic", "nbt", "snbt"):
            path = directory / f"roundtrip.{format}"
            schematic.save(path, format=format)
            restored = Schematic.load(path, format=format, data=offline)
            assert restored.region().get((0, 0, 0)).id == "minecraft:stone", format
            report = inspect_schematics([restored])
            assert report["blocks"]["minecraft:stone"] == 1, (format, report)
            assert report["items"]["minecraft:diamond"] == 3, (format, report)

        assert offline.dataset("1.21.1", "biomes")
        assert offline.dataset("1.21.1", "recipeDefinitions")
        assert offline.dataset("1.21.1", "itemTags")
        converted = Schematic.from_bytes(
            schematic.to_bytes(format="schem", version="1.20.4"), format="schem", data=offline
        )
        assert converted.version == "1.20.4"
        assert inspect_schematics([converted])["items"]["minecraft:diamond"] == 3
        converted = Schematic.from_bytes(
            converted.to_bytes(format="schem", version="1.21.1"), format="schem", data=offline
        )
        assert converted.version == "1.21.1"
        assert inspect_schematics([converted])["items"]["minecraft:diamond"] == 3
        if args.visuals:
            output = directory / "offline.png"
            schematic.export_png(output)
            assert output.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")

        metadata = next(cache.rglob("dataPaths.json"))
        metadata.write_bytes(b"invalid JSON")
        try:
            MinecraftData(cache_dir=cache, offline=True).prepare("1.21.1")
        except ValueError as error:
            assert "offline" in str(error).lower(), str(error)
        else:
            raise AssertionError("An invalid offline cache must report the damaged file")

    print(
        f"Installed mcschemora {__version__}: round trips, inspection, and offline preparation passed."
    )


if __name__ == "__main__":
    main()
