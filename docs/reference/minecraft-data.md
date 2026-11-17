# Minecraft catalogs and assets

## Version selection

Pin a Minecraft version for reproducible builds. `latest` resolves to the newest
supported release in the pinned metadata, without a live Mojang release lookup.
Authoring and validation use the selected version's Java catalog. Available catalog versions are listed by
`MinecraftData.versions`; catalog coverage does not mean every operation supports
every version. See [MinecraftData](api.md#minecraftdata) for loading methods.

Creating a provider or importing the Python package does not download Minecraft
data. Catalogs load on first use from pinned sources. Textured rendering also
needs visual assets.

## Cache and offline use

Native Rust and Python use a filesystem cache:

| Platform | Default directory |
| --- | --- |
| Linux | `$XDG_CACHE_HOME/mcschemora` when the variable is an absolute path; otherwise `~/.cache/mcschemora` |
| macOS | `~/Library/Caches/mcschemora` |
| Windows | `%LOCALAPPDATA%/mcschemora` |

Choose a writable cache and prepare the data before going offline:

```python
from mcschemora import MinecraftData, Schematic, block

data = MinecraftData(cache_dir="./minecraft-cache")
data.prepare("1.21.1", visuals=True)

offline = MinecraftData(cache_dir=data.cache_dir, offline=True)
schematic = Schematic.create(version="1.21.1", data=offline)
schematic.region().set((0, 0, 0), block("stone"))
schematic.export_png("offline.png")
```

`prepare()` loads the version's core catalog, biomes, and bundled recipes.
`visuals=True` also prepares the shared rendering catalog and visual assets.
Omit it for authoring, conversion, inspection, and sprite diagrams.

For offline conversion, prepare each source and target route:

```python
data.prepare("1.21.1", target="1.20.4")
```

Conversion can use intermediate catalogs. This call prepares those catalogs and
biomes using the converter's route selection. Preparing only the two endpoints
can leave required data uncached.

The lower-level `load(version)` prepares only the core catalog; optional datasets
can still need a download. `load_visuals(version)` prepares the requested catalog,
shared rendering catalog, and visual assets.

`offline=True` prevents all Minecraft-data downloads. Missing or invalid cached
files raise an error; no different version is substituted. Keep the prepared cache
for later offline use.

Browser WASM fetches catalogs through browser `fetch` and keeps downloaded bytes
in memory for each `MinecraftData` instance. It does not expose the native cache
or PNG/GLB rendering. See the [WASM quickstart](../guides/getting-started-wasm.md).

## Rendering

PNG/GLB rendering uses a shared Java 1.21.6 visual bundle for every schematic
version. It converts a temporary block-state palette with the version-conversion
rules; stored blocks remain unchanged. Inspect visual diagnostics for approximations.

Grass blocks and supported foliage use default colors from the bundle's colormaps.
Native renders do not evaluate per-position biomes. Unsupported tints produce
diagnostics. Sprite diagrams use bundled wiki sheets and need no visual download.

The prepared bundle has a manifest with sources and limitations. See the
[bundle specification](../../src/catalog/storage/native/SOURCE.md).

## Recipe data

Load recipes through the same provider, alongside the matching item catalog:

```python
from mcschemora import MinecraftData

data = MinecraftData()
recipes = data.dataset("1.21.1", "recipes")
items = data.dataset("1.21.1", "items")
```

Recipes come from official Java server JARs and are bundled in a shared,
versioned tracker. Runtime use does not download or execute server JARs.

| Dataset | Contents |
| --- | --- |
| `recipes` | Numeric output item IDs mapped to fixed-input, fixed-output recipes using `inShape`/`ingredients` and `result` |
| `recipeDefinitions` | Original vanilla recipe definitions keyed by recipe ID |
| `itemTags` | Item-tag IDs mapped to resolved numeric item IDs |

Use the same version's `items` dataset to resolve numeric IDs. The recipe index
covers crafting, cooking, stonecutting, smithing, and transmutation. Special and
component-dependent recipes, including brewing, remain in `recipeDefinitions`.

The index enumerates alternatives once per distinct ingredient; repeated uses
share a choice. Original definitions and tags retain the full alternatives,
including mixed-material combinations. Crafting recipes come first; entries are
otherwise ordered by recipe ID. See the
[recipe source record](../../src/catalog/recipes/SOURCE.md) for tracker details
and regeneration commands.

## Asset attribution

The root [LICENSE](../../LICENSE) covers project code. Data and assets retain
their own sources and terms. The [source overview](sources.md) links to upstream
revisions, licenses, local changes, and regeneration instructions. Keep these
records when updating or redistributing assets.
