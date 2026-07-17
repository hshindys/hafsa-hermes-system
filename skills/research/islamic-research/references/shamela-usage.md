# Shamela.ws Usage Notes

## Local copy status
- Path: `/home/hatem/Documents/Hafsa-1+2/📚 Knowledge/المكتبة الشاملة/`
- Status: **often empty** — directories exist but contain no books
- Action: always fall back to web first

## Web search
- URL: `https://shamela.ws/search?q=...`
- Search behavior: keyword OR by default; use `+word` for required, `-word` for excluded, `"phrase"` for exact
- Results: book titles only; need to open book pages to extract content

## Book page
- URL pattern: `https://shamela.ws/book/<ID>`
- If book not available online, search alternative title/author

## Author page
- URL pattern: `https://shamela.ws/author/<ID>`
- Shows all books by that author

## Integration with islamic-research skill
- Use for: classical tafsir, hadith collections, fiqh manuals, seerah books
- Fallback chain: Shamela web → sunnah.com → quran.com → islamweb.net fatwas
