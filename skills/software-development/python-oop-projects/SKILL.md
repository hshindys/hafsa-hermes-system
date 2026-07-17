---
name: python-oop-projects
description: MUST USE when user asks to learn, teach, or demo object-oriented programming in Python with practical hands-on projects (animals, pets, game entities, simulations). Covers class design, inheritance trees, polymorphism demos, encapsulation patterns, and common Python OOP pitfalls like name mangling with __private attributes in subclasses.
---

# Python OOP Projects

## Trigger
- User says: "نlearn OOP", "n3mel project OOP", "teach me classes", "oop demo", "مشروع كائنات"
- Practical Python OOP teaching with real domain objects (dogs, cats, cars, game units)

## Core Approach
1. Start with one base class + 2-3 subclasses minimum
2. Use a domain the user knows/loves (pets, animals, cars)
3. Demonstrate all 4 OOP pillars in ONE runnable script
4. Encapsulation: use `_single_underscore` for "protected" attrs in Python to avoid name-mangling surprises in inheritance demos
5. Polymorphism: same method name (`bark()`, `move()`, `attack()`) overridden per subclass
6. Always include a `main.py` with a day-in-the-life scenario

## Pitfalls
- **NEVER use `__double_underscore` for internal state in teaching demos.** Python name-mangles `__x` → `_ClassName__x`, which breaks subclass access and confuses learners. Use `_single_underscore` convention instead.
- Avoid abstract ABCs in first demos unless user explicitly asks — keep it concrete and runnable
- Don't create files deeper than 2 levels; `dog.py` + `breeds.py` + `main.py` is enough

## File Structure
```
project/
├── base.py        # Parent class with core methods + _protected attrs
├── subclasses.py  # Child classes with overrides + specializations
├── main.py        # Runnable scenario showing all 4 OOP pillars
└── README.md      # One-page summary of concepts demonstrated
```

## Template
See `templates/oop-pets-template/` for a copy-paste starter.

## Verification
Always run `python3 main.py` and confirm exit code 0 before declaring done. Fix name-mangling errors by converting `__attr` → `_attr` across base and subclass files.

## Extension Ideas
- Add medical/state tracking (vet checks, hunger/energy)
- Add breed-specific behaviors via overrides
- Add a "day simulation" loop in main.py

## Domain Modeling Beyond Pets
OOP demos can extend into non-pet domains that benefit from instance graphs and inheritance:
- Novel/lore worlds: species/types → characters → relationships
- Game entities: races → units → party members → status effects
- Org charts: role types → people → reporting relationships

### Relationship Graph Rule
When modeling relationships between characters/entities, ALWAYS store references to **instances**, not **type/class objects**. Example pitfall:
- ❌ `Relationship("linked", person_a, BirdJinn(), ...)` — will fail when code expects `.name`
- ✅ `Relationship("linked", person_a, bird_character_instance, ...)`

This matters more in prose/novel worlds where relationships are the plot engine.

### File Depth
For world-modeling projects, allow one extra level:
```
project/
├── base.py
├── subclasses.py
├── world.py        # aggregate: realms, characters, relationships
└── main.py
```
