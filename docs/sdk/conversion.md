---
description: Load and encode Minecraft schematic files, convert formats and versions, preserve regions, and review import diagnostics and export losses.
---

# Conversion

Use `.schem` for WorldEdit builds and `.litematic` when you need named regions.
MCSchemora also reads and writes Java structure files, Bedrock structures, and
Minecraft Wiki blueprints. The [formats table](../reference/formats.md) lists
their limits.

## Load and save

Start with the file from the [developer quickstart](../quickstart/developers.md):

```python
from mcschemora import Schematic

scene = Schematic.load("output/workshop.schem")
print(scene.edition, scene.version, scene.regions)
scene.save("output/workshop.litematic")
```

The file extension selects the format. Loading preserves the file's Minecraft
version; saving without `version=` keeps it. Explicit codec names are available
through `format=`, for example `format="schem2"` for Sponge v2.

## Export reports

```python
report = scene.check_export(format="litematic", version="1.20.4")
print(report)
if not report.errors and not report.losses:
    scene.save("output/workshop-1.20.4.litematic", version="1.20.4")
```

An export report distinguishes errors, which block writing, from losses, which
describe information the target cannot store. Resolve the errors and review each
omission before passing `allow_loss=True`. Version changes can also require
intermediate catalogs; see [offline conversion](minecraft-data.md#conversion-routes).

## Named regions

Save a multi-region build as `.litematic` to keep its regions. For a format with
one region, inspect the flattening report:

```python
report = scene.check_export(format="schem", flatten=True)
print(report)
```

With `flatten=True`, nonoverlapping region bounds are combined into one region.
The report records the loss of region names and boundaries, which also requires
`allow_loss=True` to accept. Resolve overlapping region bounds before flattening.

## Bytes

```python
content = scene.to_bytes(format="schem")
restored = Schematic.from_bytes(content, format="schem")
print(restored.region().bounds)
```

For binary NBT from an untrusted source, set `max_unpacked_bytes` when loading to
cap decompressed input size. See [load](../reference/python.md#schematicload)
and [from_bytes](../reference/python.md#schematicfrom_bytes).

## Import limits

```python
scene = Schematic.load(
    "output/workshop.schem",
    max_unpacked_bytes=64 * 1024 * 1024,
)
for diagnostic in scene.import_diagnostics:
    print(diagnostic)
```

The `max_unpacked_bytes` limit applies to decompressed binary NBT. An application
accepting uploads also needs limits on file size and subsequent memory, CPU,
text, rendering, and output workloads. Blueprint imports require an explicit
version; `version`, `origin`, and symbol-palette overrides apply only to those imports.

## File writes

`save()` encodes the schematic, then replaces the destination through a temporary
file in the same directory. Create the parent directory first. If an ordinary write
is incomplete, the previous destination stays intact. This protection applies to
each schematic save; reports, PNGs, and other batch outputs are written separately.

`check_export` and `to_bytes` leave the scene unchanged. To create an independent
scene at the target version, review the export report, encode, and decode the result.
Read the new scene's import notices. Keep source and destination paths separate when
the original is needed for comparison.

## Retained data

Some imported payloads are retained without support for every edit, so copying
or resizing them can fail. Format conversion can also lose metadata, scheduled
updates, origins, or region boundaries. Keep the export report with the output
file so these omissions remain visible.

Bedrock import and `.mcstructure` output retain supported Bedrock data. General
Bedrock-to-Java block/entity mapping is not implemented, and Java-to-Bedrock export
supports only a limited simple-block subset. Test Create and MineColonies
integrations separately; exporting structure NBT alone does not establish
compatibility with those mods.

## Conversion pipelines

For each input, decode the file and read its import notices before choosing a
target format and version. Check compatibility with `check_export`, resolve
errors, and accept any losses before encoding. Keep the diagnostics with the
output. The target extension selects the codec.

`schem` exports Sponge v3; use explicit `format="schem2"` when the importer needs
Sponge v2. `nbt` means Java structure NBT, not arbitrary NBT documents.
`.schematic` is the legacy MCEdit format and is not an alias for `.schem` here.
See the [format table](../reference/formats.md) before selecting inputs.

The [multi-region conversion example](../examples/litematic-to-schem.md) demonstrates
two explicit losses when flattening the supplied file. The
[NBT example](../examples/litematic-to-nbt.md) shows the separate Java structure route.
For several inputs, [batch conversion](../examples/batch-conversion.md) produces
a report per file and leaves blocked files unsaved.

## Command line

[Download convert.py](../examples/downloads/convert.py) to inspect and convert
a file without writing your own script. Use the workshop from the quickstart:

```sh
uv run --with mcschemora convert.py output/workshop.schem output/workshop.litematic
```

For this build, it prints:

```text
Edition: java; version: 1.21.1
Regions: main
No issues found.
Saved workshop.litematic
```

Add `--version 1.20.4` to target that Java version. Use `--flatten` for multiple
nonoverlapping regions, and add `--allow-loss` only after reviewing the reported
omissions. The converter stops before writing if it finds an error or an
unaccepted loss.

<details markdown="1">
<summary>Read convert.py</summary>

```python
--8<-- "examples/convert.py"
```

</details>

[Download the converted workshop](../assets/examples/workshop.litematic){ .md-button }

## Minecraft import

For WorldEdit, copy the `.schem` file into the WorldEdit configuration's
`schematics` directory. On a Bukkit server this is normally
`plugins/WorldEdit/schematics/`. Load it with `//schem load workshop`, then paste
with `//paste` at the intended location. Pasting changes world blocks; `//undo`
reverses the operation. See
[WorldEdit's clipboard guide](https://worldedit.enginehub.org/en/latest/usage/clipboard/#loading-and-saving)
for configuration paths, formats, and paste options.

For Litematica, save `.litematic` and place it in your Minecraft instance's
`schematics` directory. Open the mod menu with `M`, then choose **Load
Schematics**. Litematica displays a build guide in the world; loading a file does
not place its blocks. See the
[Litematica guide](https://github.com/maruohon/litematica/wiki).

Use a game and importer version compatible with the blocks in your exported
file. Changing a file extension alone does not convert it.
