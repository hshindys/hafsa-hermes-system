# Data Verification from Authoritative Sources

## Lesson Learned (2026-06-25)
When updating structured data (scores, standings, match results), ALWAYS verify against the authoritative source before writing. In the World Cup 2026 case:
- FIFA's official site was JS-rendered and couldn't be scraped
- Wikipedia (via browser console) had accurate, up-to-date group standings
- I initially wrote wrong scores (7 errors out of 14 matches) by relying on incomplete data
- A subagent confirmed the correct scores from Wikipedia group pages

## Verification Protocol
1. **Identify the authoritative source** (Wikipedia for general knowledge, official APIs for live data)
2. **Fetch from that source** — don't rely on memory or assumptions
3. **Cross-check** — if possible, verify against a second source
4. **Write only confirmed data** — if unsure, say "pending" or "⏳"
5. **Report discrepancies** — if your initial data was wrong, flag it

## Source Reliability Hierarchy
| Source Type | Reliability | Examples |
|-------------|-------------|----------|
| Official API | ⭐⭐⭐⭐⭐ | FIFA API, GitHub API |
| Wikipedia (verified) | ⭐⭐⭐⭐ | Match results, standings |
| News sites | ⭐⭐⭐ | ESPN, BBC Sport |
| AI-generated/LLM memory | ⭐ | Your own output (verify before reuse!) |
