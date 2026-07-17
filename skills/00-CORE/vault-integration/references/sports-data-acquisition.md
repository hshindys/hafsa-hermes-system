# External Sports Data Acquisition (Egyptian/MENA + Global)

Session-discovered pattern for populating vault-backed sports tracking.

## Observed constraints

- `filgoal.com`, `yallakora.com`, `goal.com/ar`, `365scores.com` commonly return 404/blocked
  pages to non-browser clients.
- Wikipedia remains the most reliable structured source for standings/fixtures whenever it
  has an article for the current season.
- X/Twitter search (`x_search`) may be unavailable due to spending limits.

## Fallback hierarchy (highest → lowest reliability)

1. Wikipedia article for the exact season.
2. Official federation / club site if it serves static season tables.
3. Reputable secondary aggregators mirroring Wikipedia data.
4. **Manual user-supplied results** — always the authoritative source when provided.

## Recommended vault workflow

1. Attempt Wikipedia fetch first.
2. If Wikipedia is unavailable, seed the tracker structure with placeholders and clearly
   label sections as `manual-update`.
3. Accept match results from the user/Cairo-time timestamps as ground truth; use external
   sources only to fill historical context, never to override confirmed local data.
4. Never invent unconfirmed fixtures or assignments.

## Pitfalls

- Do not retry the same blocked source back-to-back; it tightens blocks.
- Google search pages are disallowed by robots.txt; avoid fetching them directly.
- A failed fetch is not evidence “the site is broken”; it is prompt to switch source.
