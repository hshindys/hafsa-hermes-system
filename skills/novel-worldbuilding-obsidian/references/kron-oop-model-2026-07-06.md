# Kron OOP Model — 2026-07-06 session prototype

## What this is
A runnable Python hierarchy built to keep كرون world canon consistent: types → realms → characters → relationships.

## Hierarchy
```
JinnBase
├── BirdJinn → ScholarJinn / RoyalBirdJinn
├── HouriJinn
├── WaterSpirit
├── DragonKind
├── ShortJinn → TripleLimbJinn
├── ShadowJinn
├── RegionalKing
├── WiseElder
└── Human
```

## Blocks
- `JinnBase` — canonical species rules: kind, magic_source, weakness, taboo, description, `can_inhabit(realm)`
- Subclasses add special fields: `wing_color_shape`, `depth_range_m`, `hoard_value`, `oath_owner`, etc.
- `Realm` — name, layer, element, ruling_jinn_kind, danger_scale, locations, laws
- `Character` — name, jinn_type, realm, age, status, traits dict, secrets list
- `Relationship` — type, from_char, to_char, strength, hidden, notes
- `KronWorld` — aggregate and overview printer

## Known Canon Characters instantiated
- BirdJinn: كرون، نبوكت، تارك
- ScholarJinn: تارك
- RoyalBirdJinn: أريوس
- HouriJinn: رتون، نورك
- WaterSpirit: شادن
- DragonKind: ماندو
- ShortJinn: سلمار، مشكال
- TripleLimbJinn: انابا
- ShadowJinn: لسان، حص، اباتى
- RegionalKing: إلياس
- WiseElder: نومن
- Human: صفى

## Pitfalls found this session
- Relationship graph MUST use Character instances, not JinnBase type instances
- Prefer `_protected` attrs in teaching/demo OOP; `__private` breaks subclass access via name mangling
- Keep project files ≤ world.py depth unless user asks for richer structure

## Reuse
When working on كرون consistency, prefer extending this model over ad-hoc markdown edits when relationships or species rules become complex.
