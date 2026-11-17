# Data sources and attribution

MCSchemora bundles some data and downloads other data when needed. For download
and cache behavior, see [Minecraft data](minecraft-data.md).

| Data | Delivery | Source record |
| --- | --- | --- |
| Version metadata and Java catalogs | Downloaded from pinned PrismarineJS data; selected registries use bundled snapshots | [Catalogs and visual assets](../../src/catalog/storage/native/SOURCE.md) |
| Official registry snapshots | Bundled for selected versions | [Java snapshots](../../src/catalog/data/SOURCE.md) |
| Vanilla recipes and item tags | Bundled versioned tracker from official Java server JARs | [Recipe tracker](../../src/catalog/recipes/SOURCE.md) |
| Block models and textures for native rendering | Downloaded and prepared from pinned PrismarineJS assets | [Catalogs and visual assets](../../src/catalog/storage/native/SOURCE.md) |
| Special block geometry | Bundled overrides from block-model-renderer | [Block models](../../data/block-models/SOURCE.md) |
| Static entity geometry and texture bindings | Bundled adaptations of Mojang and PrismarineJS data | [Entity models](../../data/entity-models/SOURCE.md) |
| Wiki sprite sheets | Bundled Minecraft Wiki images and metadata | [Wiki sprites](../../data/wiki-sprites/SOURCE.md) |
| Material unit values | Bundled ProjectE EMC and EssentialsX profiles | [Valuation profiles](../../data/cost/java/values/SOURCE.md) |
