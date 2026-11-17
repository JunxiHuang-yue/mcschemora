# Special block models

`models.json` supplies block geometry that needs overrides in the native renderer.

## Sources

The geometry is adapted from Ewan Howell's
[block-model-renderer assets](https://github.com/ewanhowell5195/block-model-renderer/tree/9ed4d3b0462e3444c16b743dead6042fbf4c6eb6/assets),
commit `9ed4d3b0462e3444c16b743dead6042fbf4c6eb6`.

## Local data

The importer compiles upstream overrides into state rules and model geometry,
using prepared block models and texture coordinates. Its input overrides target
Java 1.21.1. Native rendering uses the shared Java 1.21.6 visual bundle.

## Updating

Check out the pinned upstream revision, then run from the repository root:

```sh
python scripts/import_special_models.py /path/to/block-model-renderer /path/to/prepared/visuals
```

The second argument must contain prepared `models.json`, `textures.json`, and
`blockstates.json`. The script checks the upstream Git revision and writes
`data/block-models/models.json` by default. Review affected block renders after
regeneration.

## Terms

The geometry is covered by the Mozilla Public License 2.0. The complete license
is retained in `data/block-models/LICENSE` in the source tree and
`licenses/block-models/LICENSE` in the Python package.
