# Examples

The [example walkthroughs](https://tiltedlabs-ai.github.io/mcschemora/examples/)
explain how to import a farm, generate a build, or edit an existing schematic.
They include downloadable scripts, prebuilt schematics, and previews or reports
so you can compare your result.

## From a checkout

Run the commands below at the repository root. uv uses the locked development
environment and builds the local package. Start with the workshop generator;
the editing, conversion, and reporting commands use its saved schematic:

```sh
uv run --locked examples/build.py
uv run --locked examples/edit.py output/workshop.schem
uv run --locked examples/render.py output/workshop.schem
uv run --locked examples/convert.py output/workshop.schem output/workshop.litematic
uv run --locked examples/materials.py output/workshop.schem
uv run --locked examples/restyle.py output/workshop.schem examples/workshop_palette.json
uv run --locked examples/rotate.py output/workshop.schem
uv run --locked examples/layers.py output/workshop.schem
uv run --locked examples/eiffel_tower.py
uv run --locked examples/import_farm.py docs/assets/examples/imported-farm/achromoss-v0.4.litematic
```

Generated files go to `output/` by default. For builds and renders, `--output`
chooses another directory; the converter takes an explicit source and destination.
Generated builds use Java 1.21.1, while the imported AChromoss farm retains Java
1.21.4. The farm schematic and preview are AGPL-3.0, with
[source and credits](../docs/assets/examples/imported-farm/SOURCE.md) included.

## Standalone scripts

You can also download a script from its walkthrough and run it in an empty
directory. For example, `uv run --with mcschemora build.py` installs the PyPI
package in a uv-managed environment and runs the workshop generator. First use
downloads the required catalogs; textured rendering also downloads visual assets.

## Rust

For the Rust example, run `cargo run --example build` from a checkout with Rust
1.88 or later. See the [Rust guide](https://tiltedlabs-ai.github.io/mcschemora/languages/rust/).
