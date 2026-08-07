---
name: jellyfin
description: "Control the local Jellyfin server (HSHINDY) from Hermes — search, browse, play."
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Jellyfin (local server control)

Control the local Jellyfin server (HSHINDY) from Hermes. The server runs at
`http://localhost:8096` and is already wired up with an API key stored in the
Hermes config (NOT in the synced vault).

## Credentials
- Config file: `~/.hermes/config/jellyfin.json` (Windows: `AppData\Local\hermes\config/jellyfin.json`)
- Shape: `{"base_url": "http://localhost:8096", "api_key": "...", "user": "hshindy"}`
- Auth header: `X-Emby-Token: <api_key>`

## CLI tool
Path: `AppData\Local\hermes/skills/productivity/jellyfin/jellyfin_cli.py`
```powershell
python <path>/jellyfin_cli.py libraries
python <path>/jellyfin_cli.py search "Al-Baqara" --limit 5
python <path>/jellyfin_cli.py search "قرآن" --type Audio
python <path>/jellyfin_cli.py recent --limit 10
python <path>/jellyfin_cli.py item <ID>
python <path>/jellyfin_cli.py play <ID>      # returns stream + web URLs
```

## What you can do (verified 2026-08-07)
- List libraries: Movies, TV-Show, Quran (music), Playlists — 472 items.
- Search by title in any language (Arabic/English/French) — Jellyfin indexes
  multilingual metadata. NOTE: `SearchTerm` matches item NAMES, not generic
  words; e.g. search "Al-Baqara" finds the Surah, but "قرآن" returns nothing
  (no item is literally named that). For browsing, list the library by ParentId.
- Get item details / overview.
- Return a direct stream/play URL for the user to open.
- Trigger a library scan: POST `/Library/Refresh` (admin).

## Pitfalls
- The API key MUST stay out of the OneDrive/Drive-synced vault (leak risk).
- Localhost only — works while the Jellyfin Windows service is running.
- For Arabic audio libraries, prefer browsing by ParentId over SearchTerm.
