# Minecraft builds, made with code

Build, edit, convert, and render Minecraft schematics with **MCSchemora**.
Use Python for scripts and agent workflows, Rust for native applications,
or WASM for browser tools.

![Floating island scene built and rendered with MCSchemora](assets/banner.png)

[Get started with Python](guides/getting-started-python.md){ .md-button .md-button--primary }
[Explore the API](reference/api.md){ .md-button }

## From a script to a schematic

Install the Python package:

```sh
python -m pip install mcschemora
```

Create a floor, check the build, and save it:

```python
from mcschemora import Schematic, block

scene = Schematic.create(version="1.21.1")
scene.region().select(start=(0, 0, 0), size=(7, 1, 7)).fill(block("stone_bricks"))
print(scene.validate())
scene.save("floor.schem")
```

Catalogs download on first use. Textured PNG and GLB rendering also download visual
assets. See [cache preparation and offline use](reference/minecraft-data.md#cache-and-offline-use).

## Build, transform, and inspect

- **Author builds:** version-checked block states, bulk edits, and named regions.
- **Edit structures:** filter selections, copy, rotate, mirror, and swap materials.
- **Check your work:** validate game rules, inspect inventories, and estimate material costs.
- **Share results:** save schematics, render textured PNGs, export GLB models, and create layer diagrams.

Read and write `.schem`, `.litematic`, `.nbt`, `.snbt`, `.mcstructure`, and
Minecraft Wiki blueprints. Available operations depend on the edition and format.
Browser WASM supports authoring, conversion, validation, and material estimates;
PNG and GLB rendering are available in Python and Rust.

Follow the [usage guide](guides/usage.md) for complete workflows, or start with
the [Rust](guides/getting-started-rust.md) and
[browser WASM](guides/getting-started-wasm.md) quickstarts.

## See what's possible

### Jade mountain scroll

Floating islands, waterfalls, and a pavilion inspired by shan shui landscapes.

![Jade mountain scroll with floating islands, waterfalls, and a pavilion](assets/jade-scroll.png)

[Read the script](https://github.com/tiltedlabs-ai/mcschemora/blob/main/examples/jade_scroll.py)
or [run the example](https://github.com/tiltedlabs-ai/mcschemora/blob/main/examples/README.md#build-the-jade-mountain-scroll).

### Rainbow reef

Procedural gyroid geometry with a rainbow palette on a dark plinth.

![Procedural rainbow gyroid reef on a dark plinth](assets/reef.png)

[Read the script](https://github.com/tiltedlabs-ai/mcschemora/blob/main/examples/reef.py)
or [run the example](https://github.com/tiltedlabs-ai/mcschemora/blob/main/examples/README.md#build-the-gyroid-rainbow-reef).

Browse [all runnable examples](https://github.com/tiltedlabs-ai/mcschemora/blob/main/examples/README.md),
including the banner scene and a small workshop.

## Project and data

Project code is [MIT licensed](https://github.com/tiltedlabs-ai/mcschemora/blob/main/LICENSE).
Bundled and downloaded assets have [their own sources and terms](reference/sources.md).
See [catalogs and assets](reference/minecraft-data.md) for supported data and rendering limits.

MCSchemora is an independent project and is not affiliated with Mojang, Microsoft, or PrismarineJS.
