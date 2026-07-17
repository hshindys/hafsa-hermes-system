# Arabic/Obsidian Novel Vault Migration

## When to use
- Source is an Arabic/Obsidian novel vault with mixed legacy folders and emoji/Chinese artifacts
- User asks to create a clean canonical vault while preserving old content as archive
- Duplicate character/files exist across multiple trees (`01-شخصيات/` at root vs inside atlas folder)
- Sensitive files (API keys, tokens) are incorrectly stored inside the vault

## Canonical novel-vault layout
```
vault-root/
├── 00-عالم-الرواية/
│   ├── 01-شخصيات/
│   ├── 02-أماكن/
│   ├── 03-تواريخ/
│   ├── 04-أنظمة-سحر/
│   ├── 05-ديانات/
│   ├── 06-ثقافات/
│   ├── 07-منظمات/
│   ├── 08-ملاحظات-كتابة/
│   └── 09-خرائط-ومراجع/
├── 01-مسودة/
│   └── part-XX/فصول/
├── 02-حبكة/
│   ├── مشاهد/
│   └── مخططات/
├── 03-أصول/
│   ├── صور/
│   └── خرائط/
├── 04-يوميات-الكتابة/
├── 00-فهرس-الخزنة.md
├── 00-مقدمة.md
├── 00-هيكل-الق story*.md
├── CLAUDE.md
└── أرشيف/
```

## Migration steps for messy Arabic vaults
1. Create destination vault with intended clean structure
2. Copy canonical files from authoritative tree only; skip junk folders (`06-闽`, `.trash`)
3. Deduplicate by filename: if same basename exists in multiple source dirs, keep one canonical copy
4. Rewrite broken wikilinks in bulk; verify zero hits with `grep -rn '\[\[old-prefix/'`
5. Rewrite index/MOC to new canonical paths first
6. Move sensitive files **out of vault entirely**; do not archive inside vault
7. Move old vault to parent `أرشيف-.../` directory, do not delete

## Known failure modes
- `.bak` files missed during cleanup because `find ... -name '*.bak'` was scoped too narrowly
- Index file preserves outdated old-path links even after bulk rewrite of chapter/character files
- Emoji/Chinese folder names require explicit removal via `mv` to archive, not deletion
- Duplicate characters with same basename but different content require human decision; never auto-delete
