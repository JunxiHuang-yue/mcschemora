# Formats

MCSchemora creates new builds against Java catalogs. It also imports Bedrock
structures, retaining data for export back to `.mcstructure`. Operation support
depends on the edition, catalog, and destination format.

## File formats

| File | Codec | Read/write | Named regions | Use and limits |
| --- | --- | --- | --- | --- |
| `.schem` | `schem` | Both | One | Sponge v3, used by WorldEdit. Multiple regions require flattening and acceptance of boundary loss. |
| `.schem` | `schem2` | Both | One | Sponge v2. Choose this codec explicitly; the extension alone selects v3 for export. |
| `.litematic` | `litematic` | Both | Multiple | Keeps region names and boundaries, including retained scheduled ticks when representable. |
| `.nbt` | `nbt` | Both | One | Java structure NBT. Placement origin and schematic metadata can be lost. |
| `.snbt` | `snbt` | Both | One | Text form of Java structure NBT, with the same structure limits. |
| `.mcstructure` | `mcstructure` | Both | One | Bedrock structure. General Java-to-Bedrock mapping is unavailable; only supported simple Java blocks can be exported. |
| `.wiki` | `blueprint` | Both | Sprite layers | Minecraft Wiki markup. Import needs an explicit Java version and can infer defaults; export omits full block states and other schematic data. |

Java file import supports 1.13 and later. Some files can be retained without an
available authoring catalog; operations that need that catalog can then fail.
Inspect `import_diagnostics` after loading.

Conversion support depends on the content of the build as well as the format.
Run `check_export` for your build and target to find blocking errors and losses
that need explicit acceptance. See [conversion](../sdk/conversion.md).

## Editions

Java catalogs support authoring, validation, inspection, material estimates,
and version conversion within the implemented data rules. Use a pinned version
and read conversion reports for blocks, entities, or item data that cannot be
represented at the destination.

Imported Bedrock secondary layers and palette data can be retained for
`.mcstructure` output, but a structure with retained secondary layers cannot
be resized. Bedrock-to-Java state and entity mapping is not implemented, so
`.mcstructure` support does not provide general conversion between editions.

## Language bindings

| Capability | Python | Rust | Browser WASM |
| --- | --- | --- | --- |
| Author, edit, and validate Java blocks | Yes | Yes | Yes |
| Import/export and conversion reports | Yes | Yes | Yes |
| Inspect blocks and estimate materials | Yes | Yes | Yes |
| Inventory and entity inspection helpers | Yes | Yes | No |
| Native PNG, GLB, and sprite rendering | Yes | Yes | No |
| Filesystem cache and offline provider | Yes | Yes | No; catalogs are fetched and cached in memory |

Rendering uses Java 1.21.6 visual assets, including for builds from other
versions. Check [rendering coverage](../sdk/minecraft-data.md#rendering-coverage)
for approximation and biome limits.

Use the [Python](python.md), [browser WASM](wasm.md), and
[Rust](../languages/rust.md) documentation for the methods each binding exposes.
