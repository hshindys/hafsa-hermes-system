# WC2026 Live Source Behavior Notes

Observed during an unattended daily results update on 2026-07-11.

## Goal.com
- Homepage simplifies better than article pages.
- Strong for narrative round summaries; weak as a direct fixture/combinations source when article pages time out.

## 365scores.com
- HTML simplification frequently fails in fetch mode.
- A failed fetch from 365scores should not block updates; move to Wikipedia immediately.

## Wikipedia 2026 FIFA World Cup / Knockout stage
- Reliable structural source for confirmed combinations and round-of-32 matchups.
- Use `knockout_stage` page plus the main tournament page for dates and match numbers.
- Prefer Wikipedia fixture/combination tables when live sources are degraded.

## General
- Multi-source cross-check is good, but delayed/timed-out live fetches degrade quickly.
- When all live sources underperform, Wikipedia alone is sufficient for structure; fall back to user-supplied local Egypt results for MOTM and scores.
