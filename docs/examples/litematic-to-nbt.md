---
description: Convert a Litematica workshop to Java structure NBT with Python and inspect the metadata loss before accepting the export.
---

# Litematica to structure NBT

Convert the supplied workshop to a Java structure `.nbt` file without opening
Minecraft. Its single region contains a bed and a chest holding 64 stone.
Structure NBT drops the Litematica metadata, so first inspect the loss report,
then decide whether to write the file.

## Check the export

Download [convert.py](downloads/convert.py) and
[workshop.litematic](../assets/examples/workshop.litematic) together, then run:

```sh
uv run --with mcschemora convert.py workshop.litematic output/workshop.nbt
```

The script checks the destination format and stops before writing:

```text
Edition: java; version: 1.21.1
Regions: main
Loss: Destination does not retain schematic metadata
Export blocked; resolve errors or explicitly accept the reported losses.
```

If losing schematic metadata is acceptable, repeat the command with the flag that
accepts the reported loss:

```sh
uv run --with mcschemora convert.py workshop.litematic output/workshop.nbt --allow-loss
```

The exported structure retains the workshop's supported blocks and chest contents.
Compare it with [workshop.nbt](../assets/examples/conversion/workshop.nbt), then
reload and inspect your file before using it in a game or importer:

```python
from mcschemora import Schematic

scene = Schematic.load("output/workshop.nbt")
print(scene.version, scene.inspect()["inventories"])
```

This verifies vanilla Java structure NBT. Compatibility with Create's
schematicannon, modded blocks, or MineColonies formats needs a separate test.
The complete [conversion script](downloads/convert.py) is explained in
[the WorldEdit example](litematic-to-schem.md). See
[files and conversion](../sdk/conversion.md) for supported formats and export
behavior.
