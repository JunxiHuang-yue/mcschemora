# Official Java catalog snapshots

Bundled snapshots contain registry data from exact versions of the official
Minecraft Java server runtime.

## Sources

The generator reads Mojang's version manifest and downloads each selected
version's server JAR and official mappings when available. It verifies download
SHA1 hashes. Snapshot JSON records the version, data version, and source hashes;
the recipe tracker also records the matching runtime provenance.

## Local data

Blocks, items, and entity IDs come from the official data generator's `--reports`
output. Every block state is checked against its reported global state ID using
sorted property names and the runtime's ordered property values. Default states
are explicitly marked by the runtime.

Living-entity classification uses each static `EntityType` entry's actual generic
entity class and `LivingEntity.isAssignableFrom`. Official mappings resolve
reflection names where available; unobfuscated runtimes use their original class
names. Java 1.14.2 predates official server mappings, so its known runtime names
are `fm` for the registry, `aim` for entity types, and `air` for living entities.

Biome names come from vanilla biome resources where available. Java 1.19.1 uses
the server data generator's worldgen biome output; Java 1.14.2 uses its biome
registry report.

### Recipes

Recipes are stored separately from the registry snapshots in
[the recipe tracker](https://github.com/tiltedlabs-ai/mcschemora/blob/main/src/catalog/recipes/SOURCE.md).
All supported versions use official server-JAR recipe data, including versions
whose block registries come from minecraft-data. Full snapshot generation refreshes the matching tracker entries
using the newly generated item IDs to validate recipe names.

## Updating

Run these commands from the repository root:

```sh
uv run --locked scripts/generate_snapshots.py
uv run --locked scripts/generate_snapshots.py --check
```

The generator rebuilds every bundled registry snapshot and its entries in the
shared recipe tracker. Pass version arguments to select snapshots or generate a
new version. New versions also need
an entry in `src/catalog/snapshots.rs` to ship in the library.

To update official recipes for every supported version:

```sh
uv run --locked scripts/import_recipes.py
uv run --locked scripts/import_recipes.py --check
```

Full generation requires a JDK capable of running the requested Minecraft
versions; JDK 25 runs all currently bundled versions. `--java` and `--javac`
select executables. The small `scripts/SnapshotRuntime.java` helper reads entity
class metadata after the official data generator runs. Reports and JVM output
are saved under the cache's `reports/<version>` directory. Recipe-only import
reads JAR resources without executing Java.

## Terms

The data comes from Mojang's Minecraft Java runtimes. The project software
license does not relicense Minecraft content. See
[Minecraft's EULA](https://www.minecraft.net/en-us/eula) and
[usage guidelines](https://www.minecraft.net/en-us/usage-guidelines).
