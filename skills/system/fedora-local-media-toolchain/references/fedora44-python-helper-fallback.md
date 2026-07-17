# Fedora 44 — Python media helper fallback pattern

## Observed
- Host: Fedora 44/Linux, Hermes profile `hafsa`
- Skill: `youtube-content` helper script `/home/hatem/.hermes/profiles/hafsa/skills/06-SYSTEM/media/youtube-content/scripts/fetch_transcript.py`
- Failure: `uv pip install youtube-transcript-api` → permission denied creating `/usr/local/lib/python3.14/site-packages/`
- Resolution: `python3 -c "import youtube_transcript_api"` succeeded because python3 resolved site-packages under `/usr`, writeable by root already containing the package. Direct `python3 <script> ...` worked without any install.

## Rule
If a helper script requires uv but uv install/dir creation is blocked by permissions, do a system Python import check before reattempting install via alternate paths. If system Python already has the dependency, run the script with `python3` directly.

## Checks to run before declaring "missing"
1. `which python3 && python3 --version`
2. `python3 -c "import <module>"` / `python3 -c "import <module>; print(module.__file__)"`
3. Only if those fail, attempt `pipx run`, `uv run --system`, or install into a Hermes/writable venv.

## Why this matters in this skill family
Media-related helpers (`youtube-transcript-api`, `yt-dlp`, `ffmpeg`, `spleeter`, etc.) often already ship in `/usr` site-packages or `/usr/bin` on Fedora. Enforcing `uv run python3 <script>` without a fallback makes otherwise-working sessions fail for permission quirks unrelated to the task.
