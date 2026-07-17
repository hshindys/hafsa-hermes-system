# Place Deep Profile — Pattern for Kron

## When to use
- Created beside the character deep-profile template because places share the same lifecycle.
- Use `enrich.py place --note <path> --template references/place_deep_profile_template.md --vault-root "/home/hatem/Documents/رواية-كرون"`.

## Canonical folders
- Original/active notes: `/home/hatem/Documents/رواية-كرون/02-Knowledge/الأماكن/`
- Suggestions: `/home/hatem/Documents/رواية-كرون/02-Knowledge/اقتراحات-التعميق/`
- Image prompts: `/home/hatem/Documents/رواية-كرون/02-Knowledge/برومبتات-صور-مقترحة/`

## Required sections
1. الهوية المكانية
2. الجغرافيا والتضاريس
3. الحواس — repeatable sensory anchors
4. البنية الاجتماعية والسياسية
5. التاريخ والأساطير
6. الدور في الحبكة
7. تفاصيل للاستخدام في المشاهد
8. ملاحظات للـ AI

## Hard rules
- Do not invent geo facts that contradict existing maps or vault lore.
- Sensory details must be stable across scenes.
- Output Arabic literary only; English only in image prompts.
- Do not overwrite original note; write `-مقترح-تعميق.md` for merge review.

## Common pitfalls
- Repeating the same description order each appearance → vary order, reuse anchors.
- Forbidden: cinematic stage directions inside place note.
- Merge workflow: never auto-apply; user reviews `-مقترح-تعميق.md` then runs `enrich.py merge`.
