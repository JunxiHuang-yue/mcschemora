# MCSchemora

Build, edit, convert, and render Minecraft schematics. MCSchemora has a Rust core,
Python bindings, and browser WASM bindings.

<p align="center">
  <img src="https://raw.githubusercontent.com/tiltedlabs-ai/mcschemora/master/docs/assets/banner.png" alt="Island banner built and rendered with MCSchemora">
</p>

Author, edit, convert, and render Minecraft schematics in Rust with Python and WASM bindings.
Supports `.schem`, `.litematic`, `.nbt`, `.snbt`, `.mcstructure`, and wiki blueprints.

[Reproduce the banner build](https://github.com/tiltedlabs-ai/mcschemora/blob/master/examples/README.md#build-the-banner).

## Capabilities

- Build with version-checked block states, bulk edits, and named regions.
- Filter selections; copy, move, rotate, mirror, and normalize builds.
- Check Java game rules and review conversion errors and losses before export.
- Inspect blocks, inventories, and entities; estimate material costs and values.
- Export textured PNGs, GLB models, sprite diagrams, and layered wiki blueprints.

Read and write `.schem`, `.litematic`, `.nbt`, `.snbt`, `.mcstructure`, and
Minecraft Wiki blueprints. Available operations depend on the edition and format.
Browser WASM supports authoring, validation, inspection of blocks, conversion,
and material estimates; it does not expose PNG/GLB rendering.

## Get started with Python

```sh
python -m pip install mcschemora
```

Create a floor, check it, and save it as a Sponge schematic:

```python
from mcschemora import Schematic, block

schematic = Schematic.create(version="1.21.1")
floor = schematic.region().select(start=(0, 0, 0), size=(7, 1, 7))
floor.fill(block("stone_bricks"))
print(schematic.validate())
schematic.save("floor.schem")
```

Catalogs download on first use; textured rendering also downloads visual assets. See
[cache preparation and offline use](https://github.com/tiltedlabs-ai/mcschemora/blob/master/docs/reference/minecraft-data.md#cache-and-offline-use).
To run from a checkout, follow the
[example setup](https://github.com/tiltedlabs-ai/mcschemora/blob/master/examples/README.md)
or [contributor setup](https://github.com/tiltedlabs-ai/mcschemora/blob/master/CONTRIBUTING.md).

## Showcase

Shan shui mountain scroll:
[source code](https://github.com/tiltedlabs-ai/mcschemora/blob/master/examples/jade_scroll.py)

<p align="center">
  <img src="https://raw.githubusercontent.com/tiltedlabs-ai/mcschemora/master/docs/assets/jade-scroll.png" alt="Jade mountain scroll with floating islands, waterfalls, and a pavilion">
</p>

Gyroid rainbow reef:
[source code](https://github.com/tiltedlabs-ai/mcschemora/blob/master/examples/reef.py)

<p align="center">
  <img src="https://raw.githubusercontent.com/tiltedlabs-ai/mcschemora/master/docs/assets/reef.png" alt="Procedural rainbow gyroid reef on a dark plinth">
</p>

## Documentation

- [Usage guide](https://github.com/tiltedlabs-ai/mcschemora/blob/master/docs/guides/usage.md)
  and [runnable examples](https://github.com/tiltedlabs-ai/mcschemora/blob/master/examples/README.md).
- [Rust quickstart](https://github.com/tiltedlabs-ai/mcschemora/blob/master/docs/guides/getting-started-rust.md)
  and [browser WASM quickstart](https://github.com/tiltedlabs-ai/mcschemora/blob/master/docs/guides/getting-started-wasm.md).
- [API reference](https://github.com/tiltedlabs-ai/mcschemora/blob/master/docs/reference/api.md)
  and [catalogs and assets](https://github.com/tiltedlabs-ai/mcschemora/blob/master/docs/reference/minecraft-data.md).
- [Documentation index](https://github.com/tiltedlabs-ai/mcschemora/blob/master/docs/index.md),
  [contributing](https://github.com/tiltedlabs-ai/mcschemora/blob/master/CONTRIBUTING.md),
  and [changelog](https://github.com/tiltedlabs-ai/mcschemora/blob/master/CHANGELOG.md).

## License

Project code is [MIT licensed](https://github.com/tiltedlabs-ai/mcschemora/blob/master/LICENSE).
Bundled and downloaded data and assets have
[their own sources and terms](https://github.com/tiltedlabs-ai/mcschemora/blob/master/docs/reference/sources.md).

MCSchemora is an independent project and is not affiliated with Mojang, Microsoft, or PrismarineJS.
