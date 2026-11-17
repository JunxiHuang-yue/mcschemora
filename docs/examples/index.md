---
title: Minecraft schematic examples
description: Import a real Litematica farm, generate an Eiffel Tower, or use MCSchemora for conversion, material lists, palettes, and rendering.
---

# Examples

Each example includes a runnable Python script and resulting files. You can also
[download all example scripts](downloads/examples.zip).

## Existing builds

[Importing a farm](import-farm.md) uses a downloaded Litematica moss farm by
OpenBagTwo, based on a design by maidofmoss. It includes attribution and a report
of the farm's blocks, inventories, and render diagnostics. The other workflows
use a supplied workshop so you can compare your results with the downloads.

| Example | Outcome |
| --- | --- |
| [Importing a farm](import-farm.md) | Inspect a real farm and render a preview. |
| [Litematica to WorldEdit](litematic-to-schem.md) | Flatten regions and review losses before saving a Sponge schematic. |
| [Litematica to structure NBT](litematic-to-nbt.md) | Export a Java structure and inspect retained contents. |
| [Batch conversion](batch-conversion.md) | Convert a directory with a result recorded for each file. |
| [Rotate a schematic](rotate-schematic.md) | Save rotated positions and directional states. |
| [Layer diagrams](layer-diagrams.md) | Export numbered sprite images with global Y coordinates. |

## Materials

| Example | Outcome |
| --- | --- |
| [Replace blocks](replace-blocks.md) | Change one material throughout a build. |
| [Restyle a workshop](restyle-workshop.md) | Apply a reusable JSON palette profile. |
| [Material lists](material-list.md) | Export construction quantities as CSV and JSON. |
| [Raw ingredients](raw-materials.md) | Expand construction items into crafting ingredients. |
| [Palette costs](compare-palettes.md) | Compare ingredient requirements and priced totals before and after a restyle. |

## Generated builds

The Eiffel Tower follows a building brief through an agent-written Python
generator. Run it to reproduce the tower, read its validation report, or change
the geometry and palette. The other generators build scenes from block placement
and sampled terrain or geometry.

| Example | Outcome |
| --- | --- |
| [Eiffel Tower](eiffel-tower.md) | Reproduce an agent-created tower and inspect its validation report. |
| [Island banner](banner.md) | Build an island around block lettering with structures and animals. |
| [Jade mountain scroll](jade-scroll.md) | Generate seeded mountains with trees, waterfalls, and a pavilion. |
| [Rainbow reef](reef.md) | Sample a gyroid surface and color its outer shell. |
