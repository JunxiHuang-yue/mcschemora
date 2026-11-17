---
description: Inspect Minecraft block palettes, replace materials while retaining compatible states, and build reusable normalization profiles.
---

# Palettes

A build's palette is the set of complete block states it uses, such as
`minecraft:oak_log[axis=y]`. You can count those states to inspect a build, choose
an authoring palette in Python, or apply a normalization profile to change its
materials. Wiki imports and render exports have separate mappings for symbols
and sprites.

## Count block states

Load the [workshop](../quickstart/developers.md) and count its non-air states:

```python
from collections import Counter
from mcschemora import Schematic

scene = Schematic.load("output/workshop.schem")
states = Counter()
for name in scene.regions:
    region = scene.region(name)
    bounds = region.bounds
    if bounds is not None:
        states.update(region.select(start=bounds.start, size=bounds.size).counts())
for state, count in states.most_common():
    print(state, count)
```

Counts use full state strings, so differently oriented stairs have distinct entries.
To group them by block ID, use `state.split("[", 1)[0]`. Each region contributes
its stored cells, including any that overlap another region at the same world
position. These counts describe the palette; edits happen through selections or
normalization, without a separate palette handle.

## Authoring palettes

```python
from mcschemora import block

palette = {
    "wall": block("stone_bricks"),
    "pillar": block("oak_log", axis="y"),
    "roof": block("oak_slab", type="bottom"),
}
region = scene.region()
region.select(start=(0, 0, 0), size=(7, 1, 7)).fill(palette["wall"])
```

An authoring palette is a collection of immutable `Block` values that you can reuse
across placements. Changing its dictionary affects future writes; existing cells
keep their states. Every write is checked against the destination schematic's catalog.

## Material replacement

For a whole-build material change, normalize by identifier:

```python
changes = scene.normalize(
    keep=["chest", "furnace"],
    replace={"oak_log": "birch_log", "stone_bricks": "deepslate_bricks"},
)
print(changes["changed"])
print(changes["replacements"])
```

Normalization changes matching IDs across all regions while retaining compatible
properties such as log axis, stair facing, and slab type. It removes properties the
target does not support and uses defaults for new ones; values of shared properties
must remain valid. Attached data also needs a compatible block-entity type, so a
chest-to-stone replacement is skipped and the chest keeps its inventory.

`Selection.replace(identifier, block(...))` instead writes the exact target block
description to matching selected cells. Use it when deliberately setting the
target state. To alter a property without changing material, filter a selection
and call `patch(...)`. See [selections and transformations](editing.md).

## Profiles

Save a profile with explicit edition, preserved IDs, replacement groups, and an
optional fallback. This is the profile used by the
[workshop restyling example](../examples/restyle-workshop.md):

```json title="workshop_palette.json"
--8<-- "examples/workshop_palette.json"
```

```python
changes = scene.normalize("workshop_palette.json")
```

Python accepts a profile file path or the bundled name `redstone`. Rust accepts a
parsed `normalize::Profile`; browser WASM accepts a profile object or the bundled
name. For inline Python rules, pass the `keep`, `replace`, and `fallback` keyword
arguments. The profile argument does not accept Python dictionaries.

| Field | Meaning |
| --- | --- |
| `edition` | Must match the schematic's edition. |
| `keep` | IDs that stay unchanged across all states and attached data. |
| `replacements` | Groups with `from` ID lists and a `to` ID. |
| `fallback` | Optional material for other eligible, unpreserved blocks. Omit it to retain unlisted materials. |

Profiles reject unknown fields and malformed input, and block names must exist in
the schematic's version. A valid profile can still contain a replacement that is
incompatible with the content of a particular build.

## Rule precedence

Explicit `keep` takes priority over replacements. Inline replacements override
profile replacement/keep rules; an explicit fallback overrides the profile fallback.
Replacement chains such as A→B→C are not followed. Incompatible or chained mappings
can be skipped.

```python
changes = scene.normalize(
    "redstone",
    keep=["oak_log", "oak_slab"],
    replace={"stone_bricks": "deepslate_bricks"},
)
```

The redstone profile preserves listed mechanisms and related materials, maps material
families to representative blocks, and replaces other eligible blocks with gray
concrete. Review decorative changes before saving and test mechanisms in-game after
simplification. Read the [bundled
profile](https://github.com/tiltedlabs-ai/mcschemora/blob/main/data/profiles/java/redstone.json)
when adapting it to a particular build.

## Compare variants

The report gives the changed-block count and sorted records of each source ID,
target ID, and quantity. It can skip incompatible replacements without reporting a
reason, so compare palette counts before and after to find unchanged blocks.
Malformed profiles raise an error.

Normalization edits the scene in place. For independent alternatives, reload the
original or clone through `to_bytes(format="litematic")` and `from_bytes(...)`,
checking the source's export report before accepting any losses. Assigning
`variant = scene` only creates another reference to the same object.

To compare costs, calculate a report before and after applying the profile, using
the same version, recipe policy, and valuation profile. Check unpriced materials
alongside the totals. See
[materials and costs](materials-and-costs.md#valuation) and the
[complete comparison example](../examples/compare-palettes.md).

## Visual mappings

For Wiki imports, `palette={"A": block("stone")}` resolves symbols into blocks.
For sprite/blueprint exports, `sprites={"minecraft:stone": "BlockSprite:stone"}`
chooses visual identifiers. Sprite overrides do not edit the schematic or affect
cost calculations. See [rendering and blueprints](rendering.md).

The [normalize reference](../reference/python.md#schematicnormalize) documents
the callable interface; [replace](../reference/python.md#selectionreplace)
and [patch](../reference/python.md#selectionpatch) cover selection edits.
