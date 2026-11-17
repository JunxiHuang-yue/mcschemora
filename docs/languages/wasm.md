# Browser WASM

The WASM bindings let a browser application build, validate, and convert schematics.
Each `MinecraftData` instance fetches catalogs on demand and keeps them in memory.
The native filesystem cache and PNG/GLB rendering are unavailable in the browser.

## Build

With Rust and npm installed, run from the repository root:

```sh
rustup target add wasm32-unknown-unknown
cargo install wasm-bindgen-cli --version 0.2.129 --locked
npm --prefix bindings/wasm run build
```

The build writes JavaScript, WebAssembly, and TypeScript declarations to
`bindings/wasm/pkg/`.

## Create a schematic

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

## File import

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

Here the `ArrayBuffer` comes from your application's file input, and the
`MinecraftData` instance must stay live while loading. For blueprint imports,
provide an explicit version in the options object. The
[API reference](../reference/wasm.md) lists methods and arguments, and the
[conversion guide](../sdk/conversion.md#export-reports) explains export reports.
