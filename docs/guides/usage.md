# Editing, conversion, and rendering

Start with the [Python quickstart](../../README.md#get-started-with-python). The editing
snippets below share one schematic. Full scripts and outputs are in the
[example gallery](../../examples/README.md); method arguments and behavior are in
the [API reference](../reference/api.md).

## Build and edit

Each region has local coordinates and an origin in schematic-global coordinates.

```python
from mcschemora import Schematic, bed, block, chest, door, item, sign

# Create a Java schematic and get its default region.
scene = Schematic.create(version="1.21.1")
region = scene.region("main")

# Fill a seven-by-seven floor, then place a block with explicit states.
region.select(start=(0, 0, 0), size=(7, 1, 7)).fill(block("stone_bricks"))
region.set((4, 1, 1), block("furnace", facing="west"))
```

```python
# Write blocks in a batch.
region.set_many({
    (4, 1, 2): block("crafting_table"),
    (0, 1, 0): block("oak_log", axis="y"),
})

region.set_many([
    ((6, 1, 0), block("stone")),
    ((6, 1, 0), block("oak_log", axis="y")),
])

region.set_many(((x, 1, 6), block("oak_planks")) for x in range(7))
```

```python
# Place special blocks.
region.place(bed(color="red", head_toward="north"), at=(2, 1, 4))
region.place(door(material="oak", facing="north"), at=(3, 1, 0))
region.place(chest(items={0: item("stone", count=64)}), at=(5, 1, 4))
region.place(sign(["Workshop", "Tools inside"]), at=(0, 1, 3))

# Inspect block properties.
furnace = region.get((4, 1, 1))
print(furnace.id, dict(furnace.properties))
print(scene.registry.describe("furnace"))

# Inspect region properties.
print(region.bounds, region.origin)
print(scene.edition, scene.version, scene.metadata, scene.regions)
```

```python
# Duplicate the selected structure, rotate it, then mirror and move the copy.
area = region.select(start=(0, 0, 0), size=(7, 3, 7))
copy = area.duplicate(offset=(10, 0, 0))
copy.rotate(axis="y", steps=1)
copy.flip(axis="x")
copy.move(offset=(0, 0, 10))

# Copy a fragment into another region, anchored at its local (0, 0, 0).
tower = scene.add_region("tower", origin=(40, 0, 0))
tower.set((0, 0, 0), area.copy())
print(scene.region("tower").get((0, 0, 0)).id)

# The region origin converts local coordinates to world coordinates.
local = (2, 1, 4)
world = tower.to_global(local)
print(world)  # (42, 1, 4)
print(tower.to_local(world))  # (2, 1, 4)
```

```python
# Check game rules, then save a litematic that keeps the named regions.
print(scene.validate())
repairs = scene.repair()
print(repairs.changed, repairs.skipped)
scene.save("workshops.litematic")

# Review the losses from merging regions, then accept them for this schem export.
print(scene.check_export(format="schem", flatten=True))
scene.save("workshops.schem", flatten=True, allow_loss=True)

# Reopen the file and inspect the blocks from disk.
reopened = Schematic.load("workshops.schem")
print(reopened.region().get_all())
```

See [Region](../reference/api.md#region), [Selection](../reference/api.md#selection),
[helpers](../reference/api.md#function-bed), [entities](../reference/api.md#entities),
and [block entities](../reference/api.md#blockentities) for the full signatures.

## Normalize materials

Normalization applies inline rules, optionally extending a bundled profile or
JSON file, to every region in place:

```python
report = scene.normalize(
    keep=["glass", "dirt", "hopper"],
    replace={"spruce_planks": "oak_planks", "birch_log": "oak_log"},
    fallback="iron_block",
)
```

Omit `fallback` to leave unlisted blocks unchanged:

```python
scene.normalize(replace={"red_wool": "white_wool"})
```

The bundled Java `redstone` profile standardizes common building materials,
including planks to oak, wool to white, leaves to oak leaves, and general
building blocks to gray concrete. Its explicit rules are in
[redstone.json](../../data/profiles/java/redstone.json).
Use `keep` for farms that depend on specific materials:

```python
report = scene.normalize(
    "redstone",
    keep=["spruce_log", "spruce_leaves"],
    replace={"red_wool": "blue_wool"},
)
```

For a custom profile, save this as `materials.json`:

```json
{
  "edition": "java",
  "replacements": [
    {
      "from": ["minecraft:granite", "minecraft:diorite"],
      "to": "minecraft:stone"
    },
    {
      "from": ["minecraft:red_stained_glass"],
      "to": "minecraft:glass"
    }
  ]
}
```

```python
report = scene.normalize("materials.json")
print(report["changed"])
print(report["replacements"])
scene.save("normalized.litematic")
```

The report contains `changed` and `replacements` records with `from`, `to`, and
`count`, sorted by source block ID. Only stored non-air cells are replaced;
entities and metadata remain unchanged.

Profiles must match the schematic's edition. IDs are checked against its catalog.
Replacements retain supported properties, discard unsupported properties, and use
target defaults for new properties. Shared values must be valid for the target.
Both blocks must have the same block-entity type; compatible attached data is
preserved. Invalid or incompatible replacements are skipped without report entries.

In a profile, `keep` takes priority over `replacements`, followed by an optional
`fallback`. Inline options override profile rules. Replacement targets remain
canonical, and mappings that would form chains or cycles are skipped. Applying
the same rules again changes nothing. Malformed profiles and edition mismatches
fail before any changes are committed. See
[normalize](../reference/api.md#schematicnormalize) for the full rules.

The profile author decides which materials are interchangeable. Normalization
does not simulate redstone or establish that a farm still works.

Rust callers pass an optional profile and `normalize::Options`:

```rust
let options = mcschemora::normalize::Options {
    keep: vec!["spruce_log".into()],
    replace: [("red_wool".into(), "blue_wool".into())].into(),
    fallback: None,
};
schematic.normalize(None, &options)?;
```

Browser callers pass an optional profile and an options object:

```javascript
schematic.normalize(undefined, { replace: { red_wool: "white_wool" } });
schematic.normalize("redstone", {
  keep: ["spruce_log"],
  replace: { red_wool: "blue_wool" },
});
```

## Material costs

```python
cost = scene.material_cost()
print(cost["items"])
print(cost["raw_materials"])
```

`items` counts placement items and primitive blocks; `raw_materials` expands
those quantities through recipes. Quantities are fractional: five oak planks cost
1.25 oak logs, without rounding crafting batches or charging for surplus.
The schematic is unchanged. Normalize first when comparing standardized builds:

```python
scene.normalize("redstone")
cost = scene.material_cost()
```

The [primitive policy](../../data/cost/java/primitives.json) defines where recipe
expansion stops, including logs, minerals and ingots, natural blocks, drops, and
plants. Blocks or items without an expansion count as one unit of themselves.
Recipe selection is deterministic for a version and does not find the cheapest
acquisition path. The [API reference](../reference/api.md#schematicmaterial_cost)
describes recipe selection and counting rules.

Doors, beds, and tall plants count once per pair; missing partners count as one
item. Double slabs and stacked blocks use their item quantities. Water and lava
count only source blocks (`level=0`). Stored regions contribute independently,
including overlaps. Wall variants use the inventory item. Potted plants require
a flower pot and plant; candle cakes require a cake and candle. Farmland and paths
require dirt, and crops require their planting items. Acquisition steps cover
stripping logs, hardening concrete, drying coral, copper oxidation, carving
pumpkins, and anvil damage.

The estimate excludes inventories, entities, fuel, tool wear, waterlogging,
fluid acquisition, and special or component-dependent recipes. Filled-container
primitives count gross inputs; returned empty containers are not credited.
Missing or malformed recipe data raises an error.

Rust callers use `schematic.material_cost().await?`. Browser callers use
`await schematic.materialCost()` and receive the same report fields. For offline use,
[prepare the required catalogs](../reference/minecraft-data.md#cache-and-offline-use).

## Material values

Apply a fixed unit-value profile to the build's primitive quantities:

```python
value = scene.value_cost("emc")
print(value["total"])
print(value["unpriced"])

server_value = scene.value_cost("essentialsx")
```

`total` is the sum of primitive quantity times unit price. Missing prices
contribute nothing and appear in `unpriced` with their fractional quantities.
A configured zero price is priced. No normalization or editing happens; call
`scene.normalize("redstone")` first when comparing standardized builds.

The bundled `emc` profile adapts ProjectE's values and conversions for vanilla
Java 1.21.1. `essentialsx` uses matching scalar entries from the official default
server sell-price table. Both are fixed across Minecraft versions; recipe
expansion still uses the build's version. EssentialsX's legacy defaults have
limited coverage, including no scalar prices for modern log or wool IDs.
See the [profile sources and coverage](../../data/cost/java/values/SOURCE.md).

Compare builds using the same profile and check unpriced quantities alongside
the total. These scores do not measure construction time or gathering difficulty.
Unknown profiles, invalid prices, and overflowing totals raise an error.

Rust callers use `schematic.value_cost("emc").await?`; browser callers use
`await schematic.valueCost("emc")`. Both return `total` and `unpriced`.

## Inspect contents

Inspection reports resource counts and retained data from loaded schematics:

```python
from mcschemora import inspect_schematics

resources = inspect_schematics(
    [Schematic.load("farm.schem"), Schematic.load("storage.schem")],
    initial_items=[("minecraft:stone", 64)],
)
print(resources["blocks"], resources["items"], resources["entities"])
print(resources["placements"][0]["inventories"])
```

Loading Java files can download catalogs; inspection itself makes no network
requests. Use `Schematic.load(..., max_unpacked_bytes=...)` to limit expanded
binary NBT input. For a single schematic, call `scene.inspect()`.

Each placement reports Minecraft and data versions, dimensions, volume, counts,
inventory paths, embedded IDs, nonempty payload field names, retained data,
entity motion, and the largest item stack. Passengers, equipment, and nested
containers are counted; nested contents are multiplied by the containing stack
count. `initial_items` contributes only to the combined item totals.

Read `complete` and the diagnostics before relying on totals. Callers must apply
their own forbidden IDs, payload restrictions, and stack limits. Counts use
submitted IDs without version conversion. Inspection does not calculate crafting
costs or infer resources created by privileged payloads. See
[inspect_schematics](../reference/api.md#function-inspect_schematics).

## Inspect and convert

Review an export report before changing format or Minecraft version:

```python
loaded = Schematic.load("build-1.20.4.litematic")
report = loaded.check_export(format="litematic", version="1.20.5")
print(report)
loaded.save("build-1.20.5.litematic", version="1.20.5")
```

```python
loaded = Schematic.load("workshops.schem")
report = loaded.check_export(format="litematic")
print(report)
if not report.errors and not report.losses:
    loaded.save("workshops.litematic")
```

Export errors block writing. Reported losses require `allow_loss=True`. Use
`flatten=True` to merge nonoverlapping regions for a single-region format; the
report includes the loss of region boundaries. See
[check_export](../reference/api.md#schematiccheck_export) and
[save](../reference/api.md#schematicsave) for more information.

## Render and crop

Export a textured image or GLB model. Axis ranges use global coordinates and
include both endpoints:

```python
diagnostics = scene.export_png("build.png", size=(800, 600), y=(0, 2))
scene.export_png("layer.png", view="top", grid=True, y=1)
scene.export_glb("build.glb")
print(diagnostics)
```

PNG/GLB rendering downloads visual assets on first use. Read the returned
diagnostics for approximations. Rendering uses a temporary palette and the shared
Java 1.21.6 visual bundle; stored blocks remain unchanged. See
[rendering data and limits](../reference/minecraft-data.md#rendering).

## Sprite diagrams and wiki blueprints

```python
print(scene.export_sprites("sprites.png", view="top", y=1, grid=True))
print(scene.export_blueprint("build.wiki", name="Workshops", y=(0, 2)))
```

Sprite diagrams use bundled Minecraft Wiki icons and need no visual download.
Blueprint export writes layered-blueprint markup. Both return diagnostics for
omitted details. See the [rendered examples](../../examples/README.md#render-and-export-a-blueprint).

Import a wiki blueprint with an explicit Minecraft version:

```python
template = "{{layered blueprint|A=BlockSprite:stone|B=BlockSprite:chest|----Floor|A|----Chest|B}}"
imported = Schematic.from_bytes(
    template.encode(),
    format="blueprint",
    version="1.21.1",
    palette={"B": block("chest", facing="north")},
)
print(imported.import_diagnostics)
```

Map symbols from the input file to explicit blocks when needed. Blueprint imports
infer some defaults because the format has limited detail. Check
`import_diagnostics`; see [from_bytes](../reference/api.md#schematicfrom_bytes).
