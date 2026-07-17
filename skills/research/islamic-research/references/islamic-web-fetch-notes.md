## Islamic web-fetch notes — 2026-07-08

### Source reliability for hadith verification
- `sunnah.com` returns short search stubs (~434 chars). Do not present these to the user as complete results.
- `al-islam.org` returns truncated pages (~491 chars). Avoid when the user needs a coherent ruling.
- `binbaz.org.sa` often returns ~486 chars; acceptable for a direction, but not enough alone for definitive authentication.
- `islamweb.net` fatwa pages may time out in fetch; generic cached text may be unrelated. Check fatwa ID in URL before trusting content.

### Hard threshold for this class of task
If a fetch returns fewer than ~1000 Arabic characters for a hadith/fiqh source, treat it as incomplete. Do not derive rulings from it; retry with a different source or a more specific ref.

### User preference observed
When the user asks for "نتائج مفهومة", they want:
1. A 4–6 row markdown table with text / حكم / راوي / مصدر
2. Short plain-arabic explanation after the table
3. No long introductions or disclaimers section before the answer
4. Strong direct wording like ✅ صحيح / ❌ لا يصح / ⚠️ ضعيف
