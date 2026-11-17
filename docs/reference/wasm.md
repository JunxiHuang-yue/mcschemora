# Browser WASM API

Generated from wasm-bindgen declarations by `make docs`.

See the [browser quickstart](../languages/wasm.md) for initialization, file import, and resource cleanup.

The complete declarations, including initialization types, are generated at `bindings/wasm/pkg/mcschemora.d.ts` during the browser build.

```typescript
/**
 * JavaScript MinecraftData: shared Minecraft Java catalogs fetched and cached in memory.
 */
export class MinecraftData {
    free(): void;
    [Symbol.dispose](): void;
    /**
     * Loads a catalog and fulfills with an empty Java Schematic containing a main region.
     */
    create(version: string): Promise<Schematic>;
    /**
     * Loads and caches a JSON dataset: blocks, items, entities, blockCollisionShapes,
     * biomes, recipes, recipeDefinitions, or itemTags. A shared tracker stores official
     * server-JAR recipes with version-specific item IDs. Optional datasets load on demand.
     */
    dataset(version: string, kind: string): Promise<any>;
    /**
     * JavaScript fromBytes: decodes a Uint8Array and fulfills with a Schematic.
     *
     * format selects the codec. options may contain blueprint-only version, origin, and palette;
     * version must be explicit for blueprints.
     */
    fromBytes(bytes: Uint8Array, format: string, options: any): Promise<Schematic>;
    /**
     * Resolves a Java version, loads its catalog, and fulfills with the resolved version.
     */
    load(version: string): Promise<string>;
    /**
     * Creates a catalog provider.
     */
    constructor();
    /**
     * Fetches metadata and fulfills with supported Java version strings.
     */
    versions(): Promise<string[]>;
}

/**
 * JavaScript Schematic: a versioned schematic with named regions.
 */
export class Schematic {
    private constructor();
    free(): void;
    [Symbol.dispose](): void;
    checkExport(format: string, flatten: boolean, version?: string | null): Promise<any>;
    /**
     * JavaScript getBlock: returns a full state string at local integer coordinates.
     *
     * Absent cells read as air; an unknown region throws an Error.
     */
    getBlock(region: string, x: number, y: number, z: number): string;
    /**
     * Returns items and fractional raw_materials. Blocks and items without a recipe
     * expansion count as one primitive unit of themselves.
     * Water and lava count only source blocks (level=0); flowing and falling fluids are excluded.
     * Costs are cached by catalog version. Shaped recipes precede other catalog recipes;
     * the first acyclic expansion to declared primitives wins. Paired structures count once,
     * orphan halves once, and double slabs/stacked items use their item quantities.
     * Regions are summed, including overlaps. Inventories, entities, fuel, tool wear,
     * fluid acquisition, and component-dependent recipes are excluded. No blocks are edited.
     * Filled-container primitives count gross inputs; returned containers are not credited.
     */
    materialCost(): Promise<any>;
    /**
     * Applies inline options and an optional bundled profile name or JSON profile object.
     *
     * Edition must match; block IDs are checked against the schematic's version.
     * Non-air replacements retain supported properties, discard unsupported ones, and use
     * target defaults for new properties. Shared values must be valid. Both blocks require
     * the same block-entity type. Compatible attached data is preserved. Invalid replacements are
     * skipped silently. Options contain keep (block IDs), replace (source-to-target object),
     * and fallback (block ID). Explicit keep wins over replace, then profile rules.
     * Invalid overrides leave their sources unchanged. Override targets remain canonical.
     * A fallback that is itself replaced is skipped. Malformed profiles or options throw an Error.
     */
    normalize(profile?: any | null, options?: any | null): any;
    /**
     * Returns region descriptions with name, schematic-global origin, local start, and size.
     */
    regions(): any;
    repair(rules?: string[] | null): any;
    scheduledTicks(region: string): any;
    /**
     * JavaScript setBlock: validates and writes a state string at local coordinates.
     */
    setBlock(region: string, x: number, y: number, z: number, state: string): void;
    /**
     * JavaScript toBytes: encodes the schematic as a Uint8Array.
     *
     * allow_loss accepts reported omissions; flatten merges regions when required.
     * Blocking errors and unaccepted losses throw an Error.
     */
    toBytes(format: string, allow_loss: boolean, flatten: boolean, version?: string | null): Promise<Uint8Array>;
    toGlobal(region: string, x: number, y: number, z: number): Int32Array;
    toLocal(region: string, x: number, y: number, z: number): Int32Array;
    /**
     * Returns errors, warnings, and unknown arrays without changing the schematic.
     */
    validate(): any;
    /**
     * Values primitive quantities with the bundled emc or essentialsx profile.
     * Returns total and unpriced primitive quantities. Missing prices contribute nothing;
     * zero prices are priced. Uses materialCost without normalizing or editing blocks.
     * Profiles are fixed across versions. Unknown profiles, invalid data, and overflow reject.
     */
    valueCost(profile: string): Promise<any>;
    /**
     * JavaScript importDiagnostics: notices about import assumptions and omissions.
     */
    readonly importDiagnostics: string[];
    /**
     * The schematic Minecraft version string.
     */
    readonly version: string;
}
```
