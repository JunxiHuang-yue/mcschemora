# MCSchemora for Python

Rust-based programmatic tools for editing, converting, and rendering Minecraft schematics.

## Install

```sh
python -m pip install mcschemora
```

## Install from source

With [uv](https://docs.astral.sh/uv/) and [Rust](https://rustup.rs/), run from the
repository root:

```sh
uv sync --locked
uv run --locked python examples/build.py
```

After changing Rust code, run `make rebuild` to refresh the native extension.

## Build release files

From the repository root:

```sh
make build
make check-dist
```

This builds a source archive and a wheel from that archive. Install the wheel
from `dist/` in a separate environment to check the released package.
See the [release guide](https://github.com/tiltedlabs-ai/mcschemora/blob/master/docs/guides/releases.md).

## Usage

```python
from mcschemora import Schematic, block

schematic = Schematic.create(version="1.21.1")
floor = schematic.region().select(start=(0, 0, 0), size=(7, 1, 7))
floor.fill(block("stone_bricks"))
print(schematic.validate())
schematic.save("floor.schem")
```

## Inspect submissions

```python
from mcschemora import Schematic, inspect_schematics

resources = inspect_schematics(
    [Schematic.load("farm.schem"), Schematic.load("storage.schem")],
    initial_items=[("minecraft:stone", 64)],
)
print(resources["blocks"], resources["items"], resources["entities"])
print(resources["placements"][0]["inventories"])
```

Inspection takes loaded schematics. Loading Java files can download catalogs;
inspection itself does not make network requests. Resource counting and aggregation
run in Rust. Use `Schematic.load(..., max_unpacked_bytes=...)` to limit expanded
binary NBT input. Inspection does not impose a submission admission policy.

Each placement reports Minecraft and data versions, dimensions, volume, block/item/entity
counts, inventory paths, embedded identifiers, nonempty payload field names,
retained data, entity motion, and the largest item stack.
Passengers, equipment, and nested containers are counted; nested contents are
multiplied by their containing stack count. `initial_items` contributes only to
the combined item totals.

These are inspection facts, not an admission policy. Callers must apply their own
forbidden IDs, payload restrictions, and stack limits. Read the report's
`complete` flag and diagnostics before relying on its totals. Counts use the
submitted IDs without version conversion; inspection does not calculate crafting
costs or infer resources created by privileged payloads.

## Downloads and offline use

Catalogs and textured rendering assets download from pinned upstream revisions
and are cached locally. Importing the package does not download Minecraft data.
A fresh installation needs a connection before Java schematic work.

```python
from mcschemora import MinecraftData, Schematic

data = MinecraftData(cache_dir="./minecraft-cache")
data.prepare("1.21.1", visuals=True)

offline = MinecraftData(cache_dir=data.cache_dir, offline=True)
schematic = Schematic.create(version="1.21.1", data=offline)
```

Omit `visuals=True` for authoring, inspection, conversion, and sprite diagrams.
For offline conversion, prepare the whole route with
`data.prepare("1.21.1", target="1.20.4")`. This also fetches intermediate catalogs.

## Documentation

- [Usage guide](https://github.com/tiltedlabs-ai/mcschemora/blob/master/docs/guides/usage.md) · [Examples and outputs](https://github.com/tiltedlabs-ai/mcschemora/blob/master/examples/README.md).
- [API reference](https://github.com/tiltedlabs-ai/mcschemora/blob/master/docs/reference/api.md#python) · [Catalogs and offline preparation](https://github.com/tiltedlabs-ai/mcschemora/blob/master/docs/reference/minecraft-data.md).

## Licensing

Project code is MIT licensed. Bundled geometry and sprites have separate terms;
each installed package includes notices and attribution under `mcschemora/licenses/`.
MCSchemora is an independent project and is not affiliated with Mojang or Microsoft.
