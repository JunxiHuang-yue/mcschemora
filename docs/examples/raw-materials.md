---
description: Calculate logs, stone, and other raw ingredients behind a Minecraft workshop using Python, with explicit recipe choices and fractional quantities.
---

# Raw ingredients

Calculate the logs, stone, and other ingredients needed to craft the workshop's
construction items. The report excludes its chest's stored 64 stone, so it gives
crafting requirements without subtracting stock you already have.

Download [materials.py](downloads/materials.py) and
[workshop.schem](../assets/examples/workshop.schem), then run:

```sh
uv run --with mcschemora materials.py workshop.schem --output output/materials
```

For the supplied Java 1.21.1 workshop, `raw-materials.csv` contains:

| Ingredient | Quantity |
| --- | ---: |
| Beetroot | 3 |
| Cobbled deepslate | 8 |
| Oak logs | 21.875 |
| Stone | 49 |
| White wool | 3 |

Oak logs cover both the placed pillars and crafted wooden items. The fractional
quantity comes from expanding recipes without rounding intermediate crafting
batches. [Download the ingredient CSV](../assets/examples/materials/raw-materials.csv)
or [the JSON report](../assets/examples/materials/materials.json) to inspect the
full result.

## Recipe choices

The selected recipes use beetroot for red dye and cobbled deepslate for the
furnace. Selection prefers shaped recipes, then takes the first supported
acyclic expansion; it does not account for your preferred recipes or the
resources available in your world.

Inventories, entities, fuel, tool wear, and fluid acquisition are excluded.
The 64 stone in the chest therefore do not reduce the requirements. Calculating
remaining stock needs an explicit inventory and crafting policy in your application.

The [complete exporter](material-list.md#report-files) writes both item and
ingredient views. See [recipe expansion](../sdk/materials-and-costs.md#recipe-expansion)
for fractional quantities and how ingredients with no available recipe are counted.
