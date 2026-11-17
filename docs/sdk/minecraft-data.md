---
description: Choose Minecraft catalogs, query block-state schemas and datasets, prepare conversion routes, and manage native and browser data caches.
---

# Minecraft data

MCSchemora checks block IDs and states against a versioned Minecraft catalog.
Pin the version when creating a build; the matching catalog is loaded on demand
and cached for later runs.

## Versions

```python
from mcschemora import MinecraftData, Schematic

data = MinecraftData()
print(data.versions)
scene = Schematic.create(version="1.21.1", data=data)
```

`latest` selects the newest version in the pinned metadata. It does not query Mojang
for a live release. A catalog may include a block that a conversion or renderer does
not support. See the [formats and support table](../reference/formats.md).

Downloads begin when an operation needs data: creating a schematic or loading
a Java file can fetch catalogs, and rendering can fetch visual assets. Importing
the Python package alone does not download anything.

## Cache location

The native Python and Rust bindings use these defaults:

| Platform | Cache directory |
| --- | --- |
| Linux | `$XDG_CACHE_HOME/mcschemora` when the variable is absolute; otherwise `~/.cache/mcschemora` |
| macOS | `~/Library/Caches/mcschemora` |
| Windows | `%LOCALAPPDATA%/mcschemora` |

The directory must be writable. To choose one explicitly, pass
`MinecraftData(cache_dir="./minecraft-cache")` and use that provider when
creating or loading schematics.

## Offline use

Run this while you have network access:

```python
from mcschemora import MinecraftData, Schematic, block

data = MinecraftData(cache_dir="./minecraft-cache")
data.prepare("1.21.1", visuals=True)

offline = MinecraftData(cache_dir=data.cache_dir, offline=True)
scene = Schematic.create(version="1.21.1", data=offline)
scene.region().set((0, 0, 0), block("stone"))
scene.export_png("offline.png")
```

`prepare` loads the core catalog, biomes, and bundled recipes. `visuals=True`
adds the rendering catalog and visual assets. Omit it when you only need
building, inspection, conversion, or sprite diagrams.

Offline mode blocks downloads and raises an error for missing or invalid cached
files, without substituting another version. Copy the prepared directory with
your script when moving it to an offline machine.

## Conversion routes

```python
data.prepare("1.21.1", target="1.20.4")
```

Conversion can use intermediate catalogs. Preparing the route downloads the
catalogs and biomes it needs. Loading only the source and destination catalogs
can leave required data missing.

## Rendering coverage

Native PNG and GLB rendering use a shared Java 1.21.6 bundle for all versions.
MCSchemora converts a temporary palette for the render; stored blocks stay
unchanged. Read the returned diagnostics for approximations. A render from
another Minecraft version can also print a fallback notice.

Grass and supported foliage use default colormap colors. Renders do not
evaluate per-position biomes. Sprite diagrams use bundled wiki sheets and
need no visual download.

## Datasets

```python
blocks = data.dataset("1.21.1", "blocks")
items = data.dataset("1.21.1", "items")
recipes = data.dataset("1.21.1", "recipes")
```

Use the same version's `items` dataset to resolve numeric recipe item IDs.
`recipeDefinitions` contains original recipe definitions; `itemTags` resolves
item tags to numeric IDs. Recipes are bundled from official Java server JARs;
runtime use does not download or execute those JARs.

Browser WASM fetches catalogs through the browser and caches them in memory per
`MinecraftData` instance. It has no native filesystem cache. See the
[browser guide](../languages/wasm.md) and
[MinecraftData reference](../reference/python.md#minecraftdata).

## Block schemas

```python
print(scene.registry.describe("oak_stairs"))
```

The registry belongs to the schematic's selected version. Query it before generating
unfamiliar state combinations or choosing a replacement target. Check the operation's
support for that version as well as the block's presence in the dataset.

## Shared providers

Scenes can share a `MinecraftData` provider to use the same cache location and
offline policy. A second provider without those settings can send operations back
to the default cache or online path. When moving prepared work to an offline
machine, include the cache directory with the scripts.

For a reproducible job, pin the package and Minecraft version, list every input
version and target route, and prepare visual assets separately if rendering is
required. If offline data is missing, prepare it before retrying with the pinned
version.

The WASM binding caches catalogs in memory for each provider instance. It has no
`cache_dir` or native offline provider. See [browser setup](../languages/wasm.md) for
loading data in a web application.