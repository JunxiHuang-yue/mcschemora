# Rust

The Rust examples run without Python and need Rust 1.88 or later. This checkout
pins Rust 1.88.0 in `rust-toolchain.toml`.

## Run the example

From the repository root:

```sh
cargo run --example build
```

The [complete example](../examples/downloads/build.rs) loads a catalog, builds a
floor, validates it, and writes a schematic. For a larger generated structure,
see the [Eiffel Tower example](../examples/eiffel-tower.md).

Catalogs download on first use. The cache must be writable; see
[catalogs and offline setup](../sdk/minecraft-data.md#offline-use).

## Dependencies

Add these dependencies to your application's `Cargo.toml`, replacing the path
with the location of this checkout:

```toml
[dependencies]
mcschemora = { path = "/path/to/mcschemora" }
pollster = "0.4"
```

Copy [examples/build.rs](../examples/downloads/build.rs) to your application's `src/main.rs`
and run `cargo run`. The example writes `examples/output/floor.schem` relative to
the working directory.

## Rendering

In the example's async block, after the output directory is created, add:

```rust
let assets = data.geometry_assets(&schematic.version)?;
let prepared = assets.prepare(&schematic, &mcschemora::render::SceneOptions::default())?;
let png = mcschemora::render::png::encode(&prepared, &mcschemora::render::png::Options::default())?;
fs::write(output.join("floor.png"), png)?;
println!("Visual diagnostics: {:?}", prepared.diagnostics);
```

Geometry preparation downloads visual assets on first use. Inspect its diagnostics
for approximations and check the [rendering coverage](../sdk/minecraft-data.md#rendering-coverage).
Build the Rust API reference locally with
`cargo doc -p mcschemora --no-deps --open`.

## Complete example

```rust
--8<-- "examples/build.rs"
```
