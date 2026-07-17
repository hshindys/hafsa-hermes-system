---
name: world-recipes-vault
description: >
  MUST USE when building a vault-based recipe knowledge base from world cuisines.
  Covers: creating structured recipe files with health-conscious filtering,
  allergy-aware recipe selection, ingredient lists with measurements, and
  multi-cuisine organization. Use when user mentions: recipes, world cuisine,
  healthy cooking, meal planning, recipe vault, وصفات, أكل صحي, مطابخ عالمية.
---

# World Recipes Vault — Healthy Multi-Cuisine Recipe Knowledge Base

Build and maintain a vault-based recipe knowledge base with health-conscious filtering, allergy awareness, and multi-cuisine organization.

## When to use

- User wants to collect healthy recipes from different cuisines
- Building a recipe knowledge base in the vault
- Setting up meal reminders with recipe suggestions
- Creating a structured recipe index with health filters
- User mentions "وصفات", "أكل صحي", "world recipes", "meal planning"

## Architecture

```
Vault/
├── 🍳 Food/
│   ├── World Healthy Recipes.md      # Main recipe file
│   ├── Meal Plan Weekly.md           # Weekly meal plans
│   └── Shopping List.md              # Aggregated shopping lists
├── 📌 Index.md                        # Updated with recipe section
└── CLAUDE.md                          # Router updated
```

## Recipe File Template

```markdown
---
title: <Recipe Name>
category: 🍳 <Cuisine> Healthy Recipes
cuisine: <Italian/Japanese/Moroccan/etc>
calories: ~XXX
suitable_for: [diabetes, hypertension, heart, vegetarian]
allergen_warning: [nuts, dairy, gluten, etc]
updated: YYYY-MM-DD
status: active
---

# <Cuisine> <Dish Name>

## المكونات
| الكمية | المكون |
|--------|--------|
| 1 كوب | ... |

## الطريقة
1. Step 1
2. Step 2

## 💡 ملاحظات صحية
- مناسب لـ: <condition>
- بديل صحي: <tip>
```

## Health-Conscious Recipe Selection

### Criteria for "Healthy" Recipes

| Criteria | ✅ Good | ❌ Avoid |
|----------|---------|----------|
| Cooking method | Grilled, steamed, baked | Deep-fried |
| Oil | Olive oil, sesame | Butter, lard |
| Salt | Low/no added salt | Heavy salting |
| Sugar | Natural sweeteners | Refined sugar |
| Carbs | Whole grains, brown rice | White flour, white rice |
| Protein | Chicken, fish*, legumes | Processed meats |

*Fish/seafood: ONLY if no allergy. Always check user profile first.

### Cuisine-Specific Healthy Picks

| Cuisine | Healthy Dishes | Dishes to Avoid |
|---------|---------------|-----------------|
| Italian | Grilled vegetable parmigiana, minestrone | Creamy pasta, deep-dish pizza |
| Japanese | Salmon teriyaki, miso soup | Tempura, tonkatsu |
| Moroccan/Arab | Tagine (vegetable), fattoush, hummus | Heavy lamb, fried pastries |
| Mexican | Black bean tacos, grilled chicken fajitas | Nachos, cheese-heavy quesadillas |
| Indian | Palak dal, tandoori chicken | Heavy cream curries |
| Thai | Tom yum soup, veggie pad thai | Deep-fried rolls, heavy coconut milk |
| Greek | Greek salad, grilled halloumi, lemon soup | Heavy moussaka, fried calamari |
| Egyptian | Molokhia (low oil), okra with lamb | Heavy taameya with excess oil |
| Korean | Kimchi stew, bibimbap (brown rice) | Fried chicken, heavy BBQ |

## Allergy-Aware Filtering

### CRITICAL: Check Before Every Recipe

1. **Read user profile** — SOUL.md / memory for allergies
2. **Flag allergens** in recipe metadata
3. **Never suggest** recipes containing user allergens
4. **Provide substitutions** when possible

### Common Allergens in Recipes

| Allergen | Cuisines to Watch | Substitution |
|----------|-------------------|--------------|
| Seafood | Japanese, Thai, Mediterranean | Chicken, tofu |
| Nuts | Indian, Thai, Moroccan | Seeds (sunflower) |
| Dairy | Italian, Greek, Indian | Nutritional yeast, coconut milk |
| Gluten | Italian (pasta), Mexican (tortillas) | Rice noodles, corn tortillas |
| Eggs | Many baked goods | Flax egg, mashed banana |

## Meal Reminder Integration

When creating a daily meal reminder cron:

```
1. Read recipe vault file
2. Select recipe that matches:
   - No allergens from user profile
   - Suitable for user's health conditions
   - Not repeated recently
3. Format: Brief recipe card with ingredients + steps
4. Tone: Warm, encouraging, spousal
```

## Pitfalls

### 1. Forgetting allergy check
**WRONG:** Suggesting shrimp pad thai when user has seafood allergy
**RIGHT:** Always cross-reference user allergies before any recipe
**Rule:** Store allergies in SOUL.md, check before EVERY food response

### 2. Unrealistic recipes
**WRONG:** Hard-to-find ingredients or 3-hour prep for busy users
**RIGHT:** Simple (under 45 min), accessible ingredients
**Rule:** Target 30-minute meals with <10 ingredients

### 3. No variety
**WRONG:** Same cuisine repeatedly
**RIGHT:** Rotate through cuisines across the week
**Rule:** Track last suggested cuisine in memory

### 4. Missing measurements
**WRONG:** "Add some oil, cook until done"
**RIGHT:** "2 tablespoons olive oil, 7 minutes"
**Rule:** Always include quantities

### 5. No health context
**WRONG:** Just listing recipes without health notes
**RIGHT:** Note: "مناسب للسكري — مؤشر جلايكيمي منخفض"
**Rule:** Add "مناسب لـ:" tag to every recipe

## See Also

- `references/recipe-template.md` — Blank template for new recipes
- `references/cuisine-guide.md` — Quick reference for healthy picks per cuisine
- `vault-integration` — How to structure vault files
- `health-reminder-cron` — For meal reminder cron integration
