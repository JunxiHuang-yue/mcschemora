---
description: Interpret schematic validation reports and repair supported block connections while preserving unknown context and reviewing changes.
---

# Validation

Validation checks supported Java game rules, including paired blocks and
neighbor-dependent connections. After generating or editing a build, run it
to find structural problems and checks that need more context:

```python
from mcschemora import Schematic

scene = Schematic.load("output/workshop.schem")
report = scene.validate()
print(report)
```

With the workshop from the [developer quickstart](../quickstart/developers.md),
this prints `No issues found.`

## Reports

| Field | Meaning | What to do |
| --- | --- | --- |
| `errors` | A supported rule found a structural problem. | Fix the reported blocks, then validate again. |
| `warnings` | A state may be unstable in the game. | Check whether the behavior is intended. |
| `unknown` | A check needs surroundings or game data that are unavailable. | Inspect the missing context before relying on that check. |
| `ok` | No errors, losses, or unknown results; warnings are allowed. | Read warnings even when this is true. |

The same `Report` type also carries export `losses`; those come from
`check_export`, not game-rule validation.

Validation leaves the schematic unchanged. Test farms and redstone machines in-game;
these checks do not simulate ticks.

## Coverage

There is no tick simulation, farm-output estimate, exploit detection, or general
mod mechanic validation. A supported vanilla rule may require neighbors outside
the schematic, and newer content can have incomplete check coverage. Keep the
Minecraft version, diagnostics, and unresolved context with a delivered build.
For agents, this report is one input to the
[generate-and-review workflow](../quickstart/agents.md), alongside visual review
and a final importer/game check.

## Repairs

The supported repair rules are `redstone`, `stairs`, `fences`, `panes`, and `walls`.
Pass `None` to run them all or an empty list to run none; unknown names fail.
Repair iterates the connection and shape rules until they converge. Invalid bounds,
overlapping regions, or a result that cannot converge can cause the call to fail,
leaving the scene unchanged.

Neighbor checks use global positions and can cross region boundaries. Missing
surroundings remain unknown instead of being assumed to be air. Power, facing,
waterlogging, free entities, and attached data are preserved by repair. An isolated
redstone dot stays a dot.

The [repair reference](../reference/python.md#schematicrepair) lists supported
rules and failure conditions. Use [export checks](conversion.md#export-reports)
separately before changing file format or Minecraft version.

Use repair to recalculate supported neighbor-dependent states:

```python
repairs = scene.repair(rules=["stairs", "fences", "panes", "walls", "redstone"])
print(repairs.changed)
for change in repairs.changes:
    print(change.region, change.position, change.before, change.after)
print(repairs.skipped)
print(scene.validate())
```

Repair updates the schematic in place. The returned `skipped` field explains
properties left unchanged because their surroundings are unknown. Loading a
schematic does not run repair automatically.

## Before export

After a material or geometry edit, read the edit report and validate the build. If
it needs repairs, review the changed states and skipped reasons before validating
again. Then check the destination format and version and save to a new path if
you need the original for comparison.

Check both validation and export reports: repairs can leave export losses, and
lossless exports can contain unstable blocks. `ok=True` allows warnings; if your
application requires none, check `warnings` too.

```python
scene.save("output/repaired.schem")
```
