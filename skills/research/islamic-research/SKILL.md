---
name: islamic-research
description: >-
  MUST USE when researching Islamic topics: Quran, Hadith, Fiqh, Aqidah,
  Seerah, Islamic history, theology, jurisprudence, or Arabic Islamic texts.
  Covers authentic sources, scholarly consensus, and methodological rules.
tags:
  - islamic
  - quran
  - hadith
  - fiqh
  - seerah
  - theology
  - arabic
---

# Islamic Research

Systematic research workflow for Islamic studies using authentic sources and scholarly methodology.

## When to use
- Quranic exegesis (Tafsir), verse context, abrogation
- Hadith studies: isnad, matn, authenticity grading
- Fiqh questions: rulings, madhabs, comparative jurisprudence
- Aqidah: theology, creed, sects
- Seerah: biography of the Prophet ﷺ, companions, early Islam
- Islamic history: caliphates, empires, scholars, movements
- Arabic Islamic terminology and semantics

## Source hierarchy (most to least authoritative)
1. **Primary texts:** Quran (Arabic), authentic Hadith collections
   - Sahihayn: Bukhari, Muslim
   - Sunan: Abu Dawud, Tirmidhi, Nasa'i, Ibn Majah
   - Musnad: Ahmad ibn Hanbal
2. **Classical scholarly consensus (Ijma)**
3. **Major classical tafsir** (Ibn Kathir, Al-Tabari, Al-Qurtubi, Al-Razi)
4. **Major fiqh references** (Al-Mughni, Fath al-Qadir, Minhaj al-Talibin)
5. **Reliable Islamic encyclopedias** (Encyclopaedia of Islam, Brill)
6. **Trusted academic institutions:**
   - Islamweb.net, IslamOnline.net
   - Al-Azhar publications
   - Saudi Digital Library (for Hanbali/Shafi'i references)
   - ISNA, IIIT, Yaqeen Institute
   - Sunnah.com (hadith lookup)
7. **Peer-reviewed journals:** Journal of Islamic Studies, Arabica
8. **Wikipedia for orientation only** — verify with primary sources

## Methodology
### Quran/Hadith research
1. Identify exact Arabic text before translation
2. Check hadith grading: sahih, hasan, da'if, mawdu'
3. Trace isnad chain weakness/strength
4. Note abrogating (naskh) vs abrogated (mansukh) verses
5. Cross-reference tafsir from at least 2 classical sources

### Fiqh research
1. Identify relevant madhab (Hanafi, Maliki, Shafi'i, Hanbali)
2. Present all madhab positions on disputed issues
3. Prefer stronger dalil (Quran > Sunnah > Ijma > Qiyas)
4. Note contemporary ijtihad where applicable

### Seerah/history
1. Distinguish between sahih and weak narrations in seerah
2. Prioritize Ibn Ishaq/Ibn Hisham, Al-Tabari, Ibn Kathir
3. Note Orientalist vs Muslim scholarly perspectives separately
4. Verify dates with multiple historical sources

## Output rules
- Always cite source: Quran (Surah:Ayah), Hadith (book/number), or scholar
- Distinguish between authentic (صحيح) and weak (ضعيف) narrations
- Present minority opinions fairly
- Add disclaimer: "هذا بحثي مبدئي — للمزيد راجع أهل العلم"
- Arabic preferred; English only on new lines for source refs
- No speculative theological claims without scholarly backing

## Common pitfalls to avoid
- Presenting weak hadith as authentic
- Ignoring scholarly consensus (ijma) on settled issues
- Mixing Orientalist conclusions with traditional methodology
- Oversimplifying madhab differences
- Claiming definitive ruling on disputed issues (khilaf)
- Fabricating or paraphrasing hadith text incorrectly

## Vault placement
Save final research notes to: `/home/hatem/Documents/Hafsa/Religion/`
File naming: `topic-name.md` with frontmatter `tags: [religion, islam, theology]`

## Session-proven source URLs (priority order)
1. **Hadith lookup:** https://sunnah.com — search by keyword, returns grades + Arabic text
2. **Shamela library:** https://shamela.ws — search classical Islamic books; local Shamela directory may be empty, always try web first: `/home/hatem/Documents/Hafsa-1+2/📚 Knowledge/المكتبة الشاملة/`
3. **Quran + tafsir:** https://quran.com — text may require start_index pagination
4. **Fiqh fatwas:** https://islamweb.net/fatawa — verify specific fatwa IDs; generic pages may return unrelated cached text
5. **Alternative:** https://binbaz.org.sa, https://dar-alifta.org

## Output formatting (user preference)
- Use Markdown tables for comparisons (madhabs, scholars, sources)
- Separate sections: Quran → Hadith → Scholarly opinions → Conclusion
- Cite as: `Quran 2:163`, `Sunan Abi Dawud 1496`, `Tirmidhi 3478`
- Always include a **"الراجح"** (preponderant view) summary table
- Add disclaimer: "هذا بحث مبدئي — راجع أهل Science للمزيد"
- Arabic first; English only for source references on new lines
- Always distinguish بين صحيح وضعيف

## Duplicate-skill note
This skill overlaps with `historical-research` on Islamic-history questions. Use this skill when the core topic is Quran/Hadith/Fiqh/Aqidah/Seerah; use `historical-research` for broader Islamic-history narratives, empires, or historiography questions that do not require hadith grading.

## Pitfalls discovered
- sunnah.com search returns paginated results; fetch truncates at 10000 chars — use specific hadith refs when known
- islamweb.net fatwa pages may return unrelated cached text; verify the URL contains the correct fatwa ID
- shamela.ws local directory is often empty — rely on web version
- quran.com uses JS rendering; fetch may return generic content — prefer known Arabic text
- Some sites block automated fetches; retry with alternative source rather than same URL
- Muslim / Abu Dawud / Ibn Majah / Tirmidhi / Nasa'i sites often return truncated body text through plain fetch. When fetch returns fewer than ~1000 Arabic chars or the response is a stub/incomplete page, treat that source as incomplete and do not base rulings on it. Prefer known canonical refs from established Islamic databases or cross-check with another source.
- When the user asks for "نتائج مفهومة", they want unambiguous tables/short rulings in dialect or simple Arabic, not long introductions. Start with a short table, then add the details.
