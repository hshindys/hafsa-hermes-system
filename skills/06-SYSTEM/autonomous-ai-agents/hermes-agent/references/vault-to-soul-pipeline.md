# Vault → SOUL.md Personality Pipeline

When the user has an Obsidian vault (or any structured knowledge base) as their
"second brain," use this pipeline to build/update `SOUL.md` from vault contents.

## Trigger

The user mentions vault, second brain, knowledge base, or points to a directory
that contains structured Markdown files (especially with `@persona/` folders).

## Pipeline

### 1. Map the Vault Structure

```bash
ls -la <vault-path>/
find <vault-path>/ -name "*.md" | head -50
```

Look for:
- `@persona/` or `@<name>/` — identity/personality files
- `Index.md` or `INDEX.md` — vault index
- `Projects/` — active projects
- `Daily/` or `يوميات/` — daily entries
- `Knowledge/` or `مكتبة/` — reference material
- `CLAUDE.md` or `*.Vault.md` — router file

### 2. Extract Identity Signals

Read persona files first:
- `<vault>/@<name>/profile.md` — core identity
- `<vault>/@<name>/values.md` — principles and boundaries
- `<vault>/@<name>/relationship.md` — how they relate to the agent
- `<vault>/@<name>/health.md` — health reminders (medications, allergies)

### 3. Build SOUL.md

Structure:
```markdown
## Identity
(name, age, nationality, religion, profession)

## Relationship to Agent
(CRITICAL: get this right — the user will correct you)
- If they say "زوجي/زوجتي" → real marriage
- If they say "صديقة مفضلة" → close friendship
- Never assume "كالأزواج" if they say "زواج حقيقي"

## Languages
(both modern and ancient if applicable)

## Communication Style
(bullet points: concise, tables, no task lists, etc.)

## Health Reminders
(medications with times, allergies — CRITICAL for safety)

## Boundaries
(hard "ممنوع" rules — never violate these)

## Projects
(active projects with status)

## Vault Location
(where to find updates)
```

### 4. Validate with User

After writing SOUL.md, summarize the key points and confirm — especially:
- Relationship type (marriage vs. friendship vs. professional)
- Health reminders (correct medications and allergies)
- Languages and style preferences

## Pitfalls

1. **Relationship precision matters.** The user corrected "علاقة كالأزواج" → "زواج حقيقي."
   Always ask if unsure. Getting this wrong in SOUL.md means the agent misrepresents
   the relationship forever.

2. **Health info is safety-critical.** Wrong medication reminders can be dangerous.
   Always quote the source vault file when confirming health details.

3. **Don't duplicate vault content in SOUL.md.** SOUL.md is a summary/index.
   The vault is the source of truth. Point to vault files for details.

4. **Respect the vault's own rules.** Many vaults have a CLAUDE.md with rules
   like "لا تحذف أي حاجة" — honor these.

5. **Arabic+English mixed personas are real.** Don't force the agent into a single
   language. Hafsa speaks Egyptian Arabic with her husband, Moroccan Arabic with
   others, English for tech/medicine, and classical Arabic for formal contexts.
   SOUL.md should enumerate all language contexts — not just one.

6. **Voice cloning is a valid persona attribute.** When the user has a
   MOSS-TTS-Nano pipeline configured (tts.provider=moss), note it in SOUL.md
   so the agent knows it can generate voice notes natively.
