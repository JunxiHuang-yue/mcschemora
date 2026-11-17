# Rendering Entities

Minecraft entities require transforms to align and render their models.
`entities.json` is a static catalog for Java 1.21.1 entities with the correct Java
texture bindings and resting poses.

This catalog is adapted from Mojang's Bedrock samples with local corrections for 1.21.1.

Visual renderers use the shared Java 1.21.6 texture bundle for all supported
schematic versions. Source revisions and notices are retained in the `source`
field of `entities.json`.
