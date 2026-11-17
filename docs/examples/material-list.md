---
description: Export the construction material list of a Minecraft workshop to JSON and CSV with a complete Python script and downloadable reports.
---

# Export a material list

Export the workshop's construction items as CSV for a spreadsheet or JSON for
another script. The bill includes 49 stone bricks, 49 oak slabs, 12 oak logs,
one red bed, one chest, one furnace, and one crafting table. Placement quantities
count the two-block bed as a single item and exclude the chest's stored 64 stone.

Download [materials.py](downloads/materials.py) and
[workshop.schem](../assets/examples/workshop.schem) into one directory, then run:

```sh
uv run --with mcschemora materials.py workshop.schem --output output/materials
```

Choose a separate output directory for another build, since rerunning replaces
the reports. The four files provide construction counts, expanded ingredients,
and value estimates:

| File | Contents |
| --- | --- |
| [materials.csv](../assets/examples/materials/materials.csv) | Seven construction item types and their quantities. |
| [raw-materials.csv](../assets/examples/materials/raw-materials.csv) | Fractional ingredients after recipe expansion. |
| [materials.json](../assets/examples/materials/materials.json) | Both views, keyed by canonical item ID. |
| [values.json](../assets/examples/materials/values.json) | EMC and EssentialsX totals, including unpriced materials. |

## Report files

`material_cost()` returns `items` and `raw_materials` dictionaries, which the
script writes with Python's standard `json` and `csv` modules. The example caps
binary NBT decompression at 64 MiB and raises an error if catalogs or recipes
are missing:

```python title="materials.py"
--8<-- "examples/materials.py"
```

Before using the expanded quantities for a gathering plan,
[interpret the raw ingredients](raw-materials.md). The
[materials and costs chapter](../sdk/materials-and-costs.md) explains
construction counts, recipe expansion, and valuation.
