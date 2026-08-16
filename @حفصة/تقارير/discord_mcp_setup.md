# Discord MCP — جاهز للتشغيل (cappyeo/discord-mcp v2.4.0)
# ثبّت عبر: npm install -g discord-mcp
# 19 أداة: send/edit/delete message, reactions, history, search, attachments, DM, friends, presence.

## كيفية التشغيل
يحتاج Discord user token (أو bot token). للتشغيل كـ MCP server محلي:

```bash
# متغير البيئة المطلوب
export DISCORD_TOKEN="<your-discord-token>"

# تشغيل الـ MCP server (stdio)
npx discord-mcp

# أو تسجيله في إعداد Hermes MCP
```

## ربطه بهيرمس
أضفه كـ MCP server في config Hermes (config.yaml → mcp.servers) مع أمر:
`npx discord-mcp` ومتغير `DISCORD_TOKEN`.

⚠️ ملاحظة: الأدوات المعروضة للتوجيه (send/edit/delete/reactions) — مش قراءة خوادم الإدارة.
الـ token محتاج يُحفظ في Hermes .env (مش في الشات). لا تلصق التوكن هنا.

## الحالة
- [x] مثبّت (npm global) ✓
- [ ] ينتظر Discord token من المستخدم لتفعيله فعلياً
