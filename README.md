# MCSchemora

<p align="center">
  <img src="docs/assets/banner.png" alt="Banner built and rendered with MCSchemora">
</p>

Author, edit, convert, and render Minecraft schematics in Rust with Python and WASM bindings.
Supports `.schem`, `.litematic`, `.nbt`, `.snbt`, `.mcstructure`, and wiki blueprints.

[Reproduce the banner build](examples/README.md#build-the-banner).

## Capabilities

- Build with version-checked block states, bulk edits, and named regions.
- Filter selections; copy, move, rotate, and mirror builds.
- Check Java game rules and inspect conversion losses before exporting.
- Render textured PNGs, GLB models, sprite diagrams, and layered wiki blueprints.

## Showcase

Shan Shui style world [code](examples/jade_scroll.py)
<p align="center">
  <img src="docs/assets/jade-scroll.png" alt="Shan Shui style world">
</p>


Gyroid reefs [code](examples/reef.py)
<p align="center">
  <img src="docs/assets/reef.png" alt="Gyroid reefs">
</p>


## Get started

### Python

The `0.1.0` release is being prepared. After publication, install with CPython 3.10+:

```sh
python -m pip install mcschemora
```

Matching wheels include the compiled extension. For development, install
[uv](https://docs.astral.sh/uv/) and [Rust](https://rustup.rs/), then run from the checkout:

```sh
uv sync --locked
uv run --locked python examples/build.py
uv run --locked python examples/render.py
```

Catalogs download on first use; textured rendering also downloads visual assets.
See [data preparation and offline use](docs/reference/minecraft-data.md#cache-and-offline-use).

Example schematic output:

<p align="center">
  <img src="docs/assets/workshop.png" alt="Workshop example output">
</p>

Example sprite output:

<p align="center">
  <img src="docs/assets/workshop-layer.png" alt="Sprite example output">
</p>

### Rust

With a stable Rust toolchain, run from this checkout:

```sh
cargo run --example build
```

## Documentation

- [Quickstarts: Python](bindings/python/README.md) · [Rust](docs/guides/getting-started-rust.md) · [Browser WASM](bindings/wasm/README.md).
- [Usage guide](docs/guides/usage.md) · [Examples and output gallery](examples/README.md).
- [API reference](docs/reference/api.md) · [Catalogs and assets](docs/reference/minecraft-data.md).
- [Documentation index and maintenance](docs/index.md).
- [Contributing](CONTRIBUTING.md) · [Release preparation](docs/guides/releases.md) · [Changelog](CHANGELOG.md).

## License

Project code is [MIT licensed](LICENSE). Bundled and downloaded assets have
[their own attribution and terms](docs/reference/minecraft-data.md#asset-attribution).
