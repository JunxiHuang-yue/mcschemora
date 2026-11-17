# Getting started with browser WASM

Use the WASM bindings to build, validate, and convert schematics in a browser.
Catalogs are fetched on demand and kept in memory for each `MinecraftData`
instance. The bindings do not expose the native filesystem cache or PNG/GLB rendering.

## Build

With Rust and npm installed, run from the repository root:

```sh
rustup target add wasm32-unknown-unknown
cargo install wasm-bindgen-cli --version 0.2.129 --locked
npm --prefix bindings/wasm run build
```

The build writes JavaScript, WebAssembly, and TypeScript declarations to
`bindings/wasm/pkg/`.

## Create and export a schematic

Import the generated module from your browser application. Adjust the import
path to match where you serve `bindings/wasm/pkg/`:

```javascript
import init, { MinecraftData } from "./pkg/mcschemora.js";

await init();
const data = new MinecraftData();
try {
  const schematic = await data.create("1.21.1");
  try {
    schematic.setBlock("main", 0, 0, 0, "minecraft:stone_bricks");
    console.log(schematic.getBlock("main", 0, 0, 0));
    console.log(schematic.validate().errors);
    const bytes = await schematic.toBytes("schem", false, false);
    const file = new Blob([bytes], { type: "application/octet-stream" });
    console.log(file.size > 0);
  } finally {
    schematic.free();
  }
} finally {
  data.free();
}
```

```text
minecraft:stone_bricks
[]
true
```

## Import a file

Pass file bytes and a codec name to `fromBytes()`. For ordinary file import,
pass `undefined` as the options argument:

```javascript
const schematic = await data.fromBytes(new Uint8Array(buffer), "litematic", undefined);
try {
  console.log(schematic.version);
} finally {
  schematic.free();
}
```

Use a live `MinecraftData` instance and an `ArrayBuffer` from your application's
file input. Blueprint imports need an explicit version in the options object.
See the [API reference](../reference/api.md#browser-wasm) for methods and arguments,
and the [conversion guide](usage.md#inspect-and-convert) for export reports.
