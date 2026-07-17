---
name: meal-planning-cuisine
description: MUST USE when building a recipe collection, planning meals, setting up food-related cron reminders, or when user asks about cooking or eating healthy global cuisine. Covers vault-based recipe storage, dietary restriction safety, meal reminder cron setup, and world cuisine organization.
triggers:
  - "وصفات"
  - "أكل صحي"
  - "تذكير وجبة"
  - "world cuisine"
  - "meal planning"
  - "recipes"
  - "طبخ"
---

# Meal Planning and World Cuisine

## When to use
- User wants to build a recipe collection in vault
- Setting up meal reminder cron jobs
- Planning healthy meals for specific conditions (diabetes, hypertension)
- Organizing recipes by world cuisine
- User asks about cooking or healthy eating

## Architecture

### Vault Structure
```
🍽️ World Cuisine/
├── 00-Index.md              # Master index with allergy warnings
├── Top 10 Global Healthy.md # Quick reference
├── 🇮🇹 Italian.md            # 5 recipes per cuisine
├── 🇯🇵 Japanese.md
├── 🇲🇦 Moroccan.md
├── 🇪🇬 Egyptian.md
├── 🇲🇽 Mexican.md
├── 🇮🇳 Indian.md
├── 🇹🇭 Thai.md
├── 🇬🇷 Greek.md
├── 🇰🇷 Korean.md
├── 🇹🇷 Turkish.md
├── 🇨🇳 Chinese.md
├── 🇱🇧 Lebanese.md
├── 🇪🇸 Spanish.md
├── 🇫🇷 French.md
└── 🇻🇳 Vietnamese.md
```

### Recipe Template
```markdown
## [Name] ([Arabic Name])
- **السعرات:** ~XXX
- **الوقت:** XX دقيقة
- **مناسب لل:** [condition]

### المقادير:
| الكمية | المكون |
|--------|--------|

### طريقة:
1. ...

⚠️ ممنوع لحاتم: [substitution note]
```

## Dietary Restriction Safety

### Allergy Check Protocol
1. Before adding ANY recipe, check SOUL.md and user profile for allergies
2. Never include recipes containing the user's allergens
3. Always include substitution notes for borderline ingredients
4. Add explicit warning at top of each cuisine file

### Common Substitutions
| Restriction | Substitute |
|-------------|-----------|
| All seafood | Chicken, tofu, beef |
| Fish sauce | Soy sauce |
| Fish-based dashi | Vegetable dashi |

## Meal Reminder Cron Pattern

### Setup
```
schedule: "0 12,18 * * *"
prompt: Pick recipe from vault, respect allergies, format concisely
```

### Output Format
```
🍽️ الوصفة: [Name] - [Cuisine]
الوقت: X دقيقة | السعرات: X

المقادير: ...
الطريقة: ...
مناسب لـ: [condition]
```

## World Cuisine Quick Reference

### Healthiest Cuisines
1. Greek (Mediterranean diet)
2. Japanese (low fat, clean protein)
3. Italian (olive oil, vegetables)
4. Moroccan (spices, lentils)
5. Indian (turmeric, legumes)

### Top 10 Healthy Recipes
| # | Recipe | Cuisine | Cal | Good For |
|---|--------|---------|-----|----------|
| 1 | Palak Dal | Indian | 200 | Anemia, Heart |
| 2 | Lemon Chicken Soup | Greek | 200 | Immunity |
| 3 | Tabbouleh | Lebanese | 150 | Digestion |
| 4 | Zucchini Noodles | Italian | 180 | Low-carb |
| 5 | Miso Soup | Japanese | 120 | Digestion |
| 6 | Black Bean Tacos | Mexican | 250 | Diabetes |
| 7 | Spring Rolls | Vietnamese | 120 | Low-calorie |
| 8 | Chana Masala | Indian | 220 | Heart |
| 9 | Tom Yum Soup | Thai | 150 | Immunity |
| 10 | Bibimbap | Korean | 350 | Balanced |

## Pitfalls
1. Forgetting allergy check before suggesting recipes
2. Inconsistent recipe format across cuisines
3. No substitution notes for restricted ingredients
4. Meal reminder too verbose - keep concise
5. Not rotating cuisines in suggestions

## See Also
- `vault-integration` skill - for vault structure setup
- `references/full-cuisine-list.md` - complete 15-cuisine recipe index
