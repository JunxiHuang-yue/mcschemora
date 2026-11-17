# Minecraft Wiki sprites

The bundled sheets support sprite and wiki-style schematic rendering.

## Sources

Sprites come from [Minecraft Wiki](https://minecraft.wiki/).
`sprites.json` retains per-file URLs, hashes, description wikitext, and revision
metadata, plus the imported module snapshots. The importer follows
[SpriteFile](https://minecraft.wiki/w/Module:SpriteFile),
[SpriteGrid](https://minecraft.wiki/w/Module:SpriteGrid), and
[Schematic/data](https://minecraft.wiki/w/Module:Schematic/data).

## Local data

- `blocks.png`: imported `BlockSprite` files and their file redirects.
- `entities.png`: imported `EntitySprite` files and their file redirects.
- `schematic.png`: the wiki schematic sheet with its original layout.
- `sprites.json`: wiki identifiers, pixel rectangles, and source metadata.

## Updating

Run from the repository root:

```sh
uv run --with pillow python scripts/import_wiki_sprites.py
```

The importer reuses its cached source inventory. Add `--refresh` to fetch a new
inventory and module snapshot. `--cache-dir` selects another download cache.
Review the changed sheets and metadata together.

## Terms

Rights remain with the respective authors and rights holders. The project
software license does not relicense these images. Per-file description wikitext
and URLs are retained in `sprites.json` under `files` for the original credits
and license declarations. Python distributions copy `source` and `files` into
`licenses/wiki-sprites/ATTRIBUTION.json`.
