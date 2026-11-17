# Entity models

`entities.json` contains static geometry, texture bindings, and resting poses
adapted for Java 1.21.1 entities.

## Sources

The `source` field in `entities.json` retains the full source metadata and notices.

| Input | Upstream repository | Revision |
| --- | --- | --- |
| Bedrock geometry, release `1.21.0.3` | [Mojang/bedrock-samples](https://github.com/Mojang/bedrock-samples/tree/c989e80c35508d658eb4a11932a04382feee4217) | `c989e80c35508d658eb4a11932a04382feee4217` |
| Additional geometry, `viewer/lib/entity/entities.json` | [PrismarineJS/prismarine-viewer](https://github.com/PrismarineJS/prismarine-viewer/tree/d78e38c4f12bf6f5eda94de1dea413a61c9eb728) | `d78e38c4f12bf6f5eda94de1dea413a61c9eb728` |
| Java 1.21.1 texture bindings | [PrismarineJS/minecraft-assets](https://github.com/PrismarineJS/minecraft-assets/tree/67c9b138b00a6b67c29ba68dae74c41faef4889d) | `67c9b138b00a6b67c29ba68dae74c41faef4889d` |

The recorded Bedrock source SHA256 is
`34d8e06047a073b64ad2abfe149017287cab124dbb86509ecc030701f6197a33`.

## Local data

Local corrections align static poses, geometry, UV coordinates, and Java texture
bindings. The corrections are listed in `source.prismarine.corrections`.
The native renderer uses the shared Java 1.21.6 texture bundle for schematic
versions that it can convert to the rendering version.

## Terms

All licensing and usage are subject to Mojang's Minecraft asset notice and PrismarineJS's MIT License.
