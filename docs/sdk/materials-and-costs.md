---
description: Calculate schematic construction materials, expand recipes to raw ingredients, estimate EMC and EssentialsX values, and compare palette variants.
---

# Costs

MCSchemora supports two ways to calculate a build's cost: material costs and valuation.

## Material cost

```python
from mcschemora import Schematic

scene = Schematic.load("output/workshop.schem")
materials = scene.material_cost()
print(materials["items"])
print(materials["raw_materials"])
```

The workshop needs 49 stone bricks, 12 oak logs, 49 oak slabs, one red bed,
one chest, one furnace, and one crafting table. The bed counts once despite
occupying two cells, and the chest's stored 64 stone stay outside this
construction bill.

## Recipe expansion

Material costs use fractional recipes, dividing ingredient quantities by the number of items each recipe produces. For instance, five oak planks require 1.25 oak logs.

Recipe expansion uses the first acyclic path through the recipe catalog to declared primitives. The pinned workshop report uses beetroot for red dye and cobbled deepslate for the furnace.

A block or item with no available recipe counts as a primitive in the final cost list.

```python
import csv
import json
from pathlib import Path

destination = Path("output/materials")
destination.mkdir(parents=True, exist_ok=True)
(destination / "materials.json").write_text(json.dumps(materials, indent=2) + "\n")
with (destination / "materials.csv").open("w", newline="") as output:
    writer = csv.writer(output)
    writer.writerow(("item", "quantity"))
    writer.writerows(sorted(materials["items"].items()))
```

For a complete script that exports both CSV views and valuation reports, use
[export a material list](../examples/material-list.md). The
[raw-ingredient example](../examples/raw-materials.md) explains the same report
from a resource-planning perspective.

## Valuation

Use a valuation profile to estimate a build's value from its raw ingredients.

```python
for profile in ("emc", "essentialsx"):
    value = scene.value_cost(profile)
    print(profile, value["total"], value["unpriced"])
```

We support `emc` and `essentialsx` valuations. See [valuation sources and
derivation](https://github.com/tiltedlabs-ai/mcschemora/blob/main/data/cost/java/values/SOURCE.md) for more details.

For the pinned workshop, EMC totals 1101 and prices every ingredient. EssentialsX
totals 147 but leaves several ingredients unpriced. 