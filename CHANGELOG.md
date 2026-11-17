# Changelog

## 0.1.0 — release preparation

Initial Python release for Minecraft schematic authoring, editing, conversion,
inspection, and rendering.

- Rust core with a typed Python interface and CPython 3.10+ ABI support.
- Java structure NBT/SNBT, Sponge schematic, Litematic, Bedrock structure, and
  wiki blueprint codecs. Available operations depend on edition and format.
- Region edits, selections, transforms, entity and inventory inspection,
  validation, and material-cost calculation.
- Textured PNG/GLB rendering, sprite diagrams, and wiki blueprint export.
- Pinned upstream catalogs, bundled conversion and recipe data, and explicit
  offline preparation through `MinecraftData.prepare()`.

