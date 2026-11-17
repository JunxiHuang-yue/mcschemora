# Downloaded catalogs and visual assets

MCSchemora downloads catalog JSON and prepares block visuals for native rendering.
These downloads are separate from the data bundled in the package.

## Sources

| Input | Upstream repository | Revision |
| --- | --- | --- |
| Catalog JSON | [PrismarineJS/minecraft-data](https://github.com/PrismarineJS/minecraft-data/tree/8ffb321c74cffe779acf5c447d08c473c4c291d7) | `8ffb321c74cffe779acf5c447d08c473c4c291d7` |
| Block models and textures | [PrismarineJS/minecraft-assets](https://github.com/PrismarineJS/minecraft-assets/tree/67c9b138b00a6b67c29ba68dae74c41faef4889d) | `67c9b138b00a6b67c29ba68dae74c41faef4889d` |

## Local data

Catalog selection and validation use the requested Java version, starting at
1.13. Selected versions use bundled official snapshots instead of upstream
registry JSON. Rendering uses a shared Java 1.21.6 visual bundle and converts a
temporary block-state palette.

The prepared visual bundle contains:

- `blockstates.json`: map from block IDs to variants and multipart
  conditions. Model references are IDs. Rotations, weights, and UV
  locking remain unchanged.
- `models.json`: map from model IDs to flattened inherited models.
  Child texture and display bindings override parent bindings. Faces reference
  final sprite IDs and carry explicit UVs. Texture objects and face
  `texture_flags` preserve additional source fields such as `force_translucent`.
  Parameterized abstract templates may retain symbolic variables; concrete
  models referenced by blockstates cannot have unbound face textures.
- `textures.json`: map from canonical sprite IDs to `atlas` page index,
  `rect` in pixels, normalized `uv`, decoded `image_hash`, `source` path/blob,
  complete `metadata`, and selected animation `frame`. The generated
  `minecraft:missingno` sprite has null source metadata.
  Atlas rectangles and normalized UVs use a top-left origin. Model face UVs
  retain Minecraft's local 0–16 texture coordinate convention, independently
  of texture pixel dimensions.
- `atlas-<index>.png`: deterministic 1024×1024 RGBA pages with one pixel of
  edge padding. Identical decoded frame pixels and dimensions share a rectangle.
- `manifest.json`: preparation format, bundle identity, repository attribution,
  source versions, input files and hashes, atlas dimensions, abstract unresolved
  variables, and renderer limitations.

## Updating

Catalog and visual source pins are defined in `src/catalog/source.rs` and
`src/catalog/storage/native/visuals.rs`. Update the pins and check affected
catalogs and renders together. Normal use downloads and caches data as needed; the
[cache and offline guide](https://tiltedlabs-ai.github.io/mcschemora/sdk/minecraft-data/#offline-use)
explains preparation and offline use.

## Terms

Upstream notices are recorded in the
[minecraft-data README](https://github.com/PrismarineJS/minecraft-data/blob/8ffb321c74cffe779acf5c447d08c473c4c291d7/README.md)
and the
[minecraft-assets README](https://github.com/PrismarineJS/minecraft-assets/blob/67c9b138b00a6b67c29ba68dae74c41faef4889d/README.md).
Minecraft visual assets remain subject to
[Minecraft's usage guidelines](https://www.minecraft.net/en-us/usage-guidelines).
Entity model sources and local corrections are recorded separately in
`data/entity-models/entities.json` under `source`.
