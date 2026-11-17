# MCSchemora

Build, edit, convert, and render Minecraft schematics. MCSchemora has a Rust core,
Python bindings, and browser WASM bindings.

<p align="center">
  <img src="https://raw.githubusercontent.com/tiltedlabs-ai/mcschemora/main/docs/assets/banner.png" alt="Island banner built and rendered with MCSchemora">
</p>

Author, edit, convert, and render Minecraft schematics in Rust with Python and WASM bindings.
Supports `.schem`, `.litematic`, `.nbt`, `.snbt`, `.mcstructure`, and wiki blueprints.

[Reproduce the banner build](https://github.com/tiltedlabs-ai/mcschemora/blob/main/examples/README.md#build-the-banner).

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
[cache preparation and offline use](https://tiltedlabs-ai.github.io/mcschemora/reference/minecraft-data/#cache-and-offline-use).
To run from a checkout, follow the
[example setup](https://github.com/tiltedlabs-ai/mcschemora/blob/main/examples/README.md)
or [contributor setup](https://github.com/tiltedlabs-ai/mcschemora/blob/main/CONTRIBUTING.md).

## Showcase

Shan shui mountain scroll:
[source code](https://github.com/tiltedlabs-ai/mcschemora/blob/main/examples/jade_scroll.py)

<p align="center">
  <img src="https://raw.githubusercontent.com/tiltedlabs-ai/mcschemora/main/docs/assets/jade-scroll.png" alt="Jade mountain scroll with floating islands, waterfalls, and a pavilion">
</p>

Gyroid rainbow reef:
[source code](https://github.com/tiltedlabs-ai/mcschemora/blob/main/examples/reef.py)

<p align="center">
  <img src="https://raw.githubusercontent.com/tiltedlabs-ai/mcschemora/main/docs/assets/reef.png" alt="Procedural rainbow gyroid reef on a dark plinth">
</p>

## Documentation

- [Usage guide](https://tiltedlabs-ai.github.io/mcschemora/guides/usage/)
  and [runnable examples](https://github.com/tiltedlabs-ai/mcschemora/blob/main/examples/README.md).
- [Rust quickstart](https://tiltedlabs-ai.github.io/mcschemora/guides/getting-started-rust/)
  and [browser WASM quickstart](https://tiltedlabs-ai.github.io/mcschemora/guides/getting-started-wasm/).
- [API reference](https://tiltedlabs-ai.github.io/mcschemora/reference/api/)
  and [catalogs and assets](https://tiltedlabs-ai.github.io/mcschemora/reference/minecraft-data/).
- [Documentation index](https://tiltedlabs-ai.github.io/mcschemora/),
  [contributing](https://github.com/tiltedlabs-ai/mcschemora/blob/main/CONTRIBUTING.md),
  and [changelog](https://github.com/tiltedlabs-ai/mcschemora/blob/main/CHANGELOG.md).

## License

Project code is [MIT licensed](https://github.com/tiltedlabs-ai/mcschemora/blob/main/LICENSE).
Bundled and downloaded data and assets have
[their own sources and terms](https://tiltedlabs-ai.github.io/mcschemora/reference/sources/).

MCSchemora is an independent project and is not affiliated with Mojang, Microsoft, or PrismarineJS.
