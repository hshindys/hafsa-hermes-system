---
tags: ["kron"]
tags: ["novel"]
tags: ["worldbuilding"]
tags: ["fiction"]
---
# World of Kron — Knowledge Graph Seed
> Last updated: 2026-07-03 Cairo

## Usage
هذا المجلد يمثّل **الكيانات والعلاقات** specific for رواية كرون، بغض النظر عن Wiki الموجودة في Index.
كل entity يُحفظ في ملف منفصل داخل `Entities/`، والعلاقات في `Relations/`.

## Entity Template
```markdown
# {{Name}}
- type: person / location / artifact / faction / event / magic
- status: canonical / draft / deprecated
- first_appearance: "Chapter 01"
- aliases: []
- relations:
  - relation: "parent-of" | "ally-of" | "rival-of" | "located-in" | "created-by" | "member-of"
    target: "[[Entity Title]]"
    note: ""
```

## Relations Format
```markdown
# relation: {{RelationType}}
source: "[[Entity A]]"
target: "[[Entity B]]"
note: سبب/سياق العلاقة
since: "chapter X"
```

## Examples
نماذج أولية: [[سليم]]، [[سليمة]]، [[صفى]]
