# Nous daily cost report — session reference

Generated from a cron cost-report task on 2026-07-16. Store durable query patterns here rather than rediscovering them.

## Sources consulted

### 1. Nous billing state
File: `/home/hatem/.hermes/hermes-agent/hermes_cli/nous_billing.py`
Call: `get_billing_state()`
Return shape:
- `monthlyCap.limitUsd`
- `monthlyCap.spentThisMonthUsd`
- `balanceUsd`
- `org.role`
Example output:
```json
{
  "balanceUsd":"0",
  "monthlyCap":{"limitUsd":"1000","spentThisMonthUsd":"0","isDefaultCeiling":true},
  "autoReload":null
}
```

### 2. Local state.db aggregation
Schema table: `sessions`
Columns used:
- `started_at REAL` — unix epoch seconds, Cairo-local compare required
- `model TEXT`
- `api_call_count INTEGER`
- `estimated_cost_usd REAL`
- `actual_cost_usd REAL`

Cairo-day window query pattern:
```python
from datetime import datetime, time
from zoneinfo import ZoneInfo
cairo = ZoneInfo('Africa/Cairo')
today = datetime.now(cairo).date()
start_ts = datetime.combine(today, time.min, tzinfo=cairo).timestamp()
rows = con.execute('SELECT ... FROM sessions WHERE started_at >= ?', (start_ts,)).fetchall()
daily_est = sum(r['estimated_cost_usd'] or 0 for r in rows)
daily_actual = sum((r['actual_cost_usd'] or 0) for r in rows)
```

Observed on 2026-07-16:
- 42 sessions started today.
- Model in use: `stepfun/step-3.7-flash:free`.
- `estimated_cost_usd` was `0.0` across all rows.
- `actual_cost_usd` was `None` for most rows.

## Known pitfalls
- `fetch_account_usage(None)` does not auto-resolve the active Hermes provider when provider is unset; explicit provider or Nous billing path is safer for Nous accounts.
- OpenRouter credits endpoint is not used here because this profile’s provider is Nous, not OpenRouter.
- Session `started_at` is epoch seconds, not ISO8601.
