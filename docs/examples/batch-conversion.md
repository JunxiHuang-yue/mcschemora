---
description: Convert a directory of Minecraft schematics with Python while retaining per-file diagnostics, blocking unaccepted losses, and avoiding filename collisions.
---

# Batch conversion

Convert a folder of schematics into Litematica files, keeping a JSON result for
each input. The script continues after a failed or blocked conversion, but exits
with a failure status if any input could not be saved. Inspect the report even
when some outputs were saved.

Download [batch_convert.py](downloads/batch_convert.py) and
[conversion-inputs.zip](../assets/examples/conversion-inputs.zip). Extract the
archive into an `incoming` directory; it contains `workshop.schem` and the
two-region `workshop-regions.litematic`. Choose a separate output directory:

```sh
uv run --with mcschemora batch_convert.py incoming output/converted
```

Both supplied inputs convert successfully:

```text
workshop-regions.litematic: saved
workshop.schem: saved
```

The output contains `workshop-regions.litematic.litematic`,
`workshop.schem.litematic`, and `report.json`. Appending the new suffix to each
full filename keeps outputs separate when input stems match across formats.
[Download the successful sample report](../assets/examples/conversion/batch-report.json)
to compare the results.

## Blocked exports

Converting the same inputs to WorldEdit requires flattening:

```sh
uv run --with mcschemora batch_convert.py incoming output/worldedit --format schem --flatten
```

The multi-region input has flattening losses, so its result is `blocked`.
Review `report.json` before rerunning with `--allow-loss`; that flag never
permits an export error. Use `--version` to choose a supported target Java
version, allowing for any intermediate catalogs that preparation needs.

## Error handling

The script reads immediate directory children ending in `.schem`, `.litematic`,
`.nbt`, or `.snbt`. It caps binary NBT decompression at 64 MiB per input and
records failures in the report. Legacy `.schematic` and MineColonies `.blueprint`
files are unsupported inputs.

Rerunning replaces existing outputs. Each schematic save is atomic, but an
interrupted batch can leave some converted files without a final report. Keep
that possibility in mind when using the script in an automated pipeline:

```python title="batch_convert.py"
--8<-- "examples/batch_convert.py"
```

See [files and conversion](../sdk/conversion.md#conversion-pipelines) for
supported formats and handling retained imported data.
