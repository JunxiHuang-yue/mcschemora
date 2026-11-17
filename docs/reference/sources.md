# Data sources

MCSchemora ships some datasets with the package and downloads others when an
operation needs them. See [versions and offline use](../sdk/minecraft-data.md)
for download and cache behavior.

The website emblem uses the [Minecraft Wiki crafter inventory icon](https://minecraft.wiki/w/File:Invicon_Crafter.png),
copied unchanged to `docs/assets/crafter.png`. Minecraft artwork belongs to Mojang and Microsoft.

| Data | Delivery | Source record |
| --- | --- | --- |
| Version metadata and Java catalogs | Downloaded from pinned PrismarineJS data; selected registries use bundled snapshots | [Catalogs and visual assets](https://github.com/tiltedlabs-ai/mcschemora/blob/main/src/catalog/storage/native/SOURCE.md) |
| Official registry snapshots | Bundled for selected versions | [Java snapshots](https://github.com/tiltedlabs-ai/mcschemora/blob/main/src/catalog/data/SOURCE.md) |
| Vanilla recipes and item tags | Bundled versioned tracker from official Java server JARs | [Recipe tracker](https://github.com/tiltedlabs-ai/mcschemora/blob/main/src/catalog/recipes/SOURCE.md) |
| Block models and textures for native rendering | Downloaded and prepared from pinned PrismarineJS assets | [Catalogs and visual assets](https://github.com/tiltedlabs-ai/mcschemora/blob/main/src/catalog/storage/native/SOURCE.md) |
| Special block geometry | Bundled overrides from block-model-renderer | [Block models](https://github.com/tiltedlabs-ai/mcschemora/blob/main/data/block-models/SOURCE.md) |
| Static entity geometry and texture bindings | Bundled adaptations of Mojang and PrismarineJS data | [Entity models](https://github.com/tiltedlabs-ai/mcschemora/blob/main/data/entity-models/SOURCE.md) |
| Wiki sprite sheets | Bundled Minecraft Wiki images and metadata | [Wiki sprites](https://github.com/tiltedlabs-ai/mcschemora/blob/main/data/wiki-sprites/SOURCE.md) |
| Material unit values | Bundled ProjectE EMC and EssentialsX profiles | [Valuation profiles](https://github.com/tiltedlabs-ai/mcschemora/blob/main/data/cost/java/values/SOURCE.md) |

The [farm import example](../examples/import-farm.md) uses AChromoss v0.4 by
[OpenBagTwo](https://github.com/OpenBagTwo/Schematics/tree/fd78e34645f7147b7b3a1a5033239f52a4803063),
based on [Chromoss by maidofmoss](https://www.youtube.com/watch?v=eNYZiuVNBe0).
The third-party schematic and its derived previews are licensed under
[AGPL-3.0](../assets/examples/imported-farm/LICENSE.txt).
