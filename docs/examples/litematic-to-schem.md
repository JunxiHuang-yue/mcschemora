---
description: Convert a two-region Litematica workshop into a WorldEdit Sponge schematic with Python, reviewing flattening losses before export.
---

# Litematica to WorldEdit

Convert two workshops in a Java 1.21.1 Litematica file to one WorldEdit `.schem`.
The input has `main` at the origin and `annex` offset by ten blocks. Flattening
keeps their relative placement while discarding the region boundaries; the
script asks you to accept that loss before saving.

## Check the export

Download [convert.py](downloads/convert.py) and
[workshop-regions.litematic](../assets/examples/workshop-regions.litematic)
into the same directory. With [uv installed](https://docs.astral.sh/uv/getting-started/installation/), run:

```sh
uv run --with mcschemora convert.py workshop-regions.litematic output/workshops.schem --flatten
```

The check reports two losses and stops before writing:

```text
Edition: java; version: 1.21.1
Regions: annex, main
Loss: Destination stores one region; region names and boundaries will be lost
Loss: main: omitted structure cells become explicit air in schem
Export blocked; resolve errors or explicitly accept the reported losses.
```

To accept the loss of region boundaries and the conversion of omitted cells to
explicit air, rerun with the loss flag:

```sh
uv run --with mcschemora convert.py workshop-regions.litematic output/workshops.schem --flatten --allow-loss
```

The command saves `output/workshops.schem`; compare it with the
[verified output](../assets/examples/conversion/workshops.schem). If region
bounds overlap, resolve that error first. `--allow-loss` only accepts losses.

Put the result in WorldEdit's configured schematics directory, load it with
`//schem load workshops`, and paste at the intended location. See
[Minecraft import instructions](../sdk/conversion.md#minecraft-import) for paths
and importer compatibility.

## Export checks

The script calls `check_export(format="schem", flatten=True)` before saving.
Errors block writing, and losses require explicit acceptance. The output
extension selects Sponge v3; legacy MCEdit `.schematic` conversion is unsupported.

```python title="convert.py"
--8<-- "examples/convert.py"
```

Use [files and conversion](../sdk/conversion.md) for version changes, retained
payloads, and codec choices. To convert a directory with a report for each input,
continue with [batch conversion](batch-conversion.md).
