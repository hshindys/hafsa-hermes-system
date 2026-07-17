---
name: fedora-local-media-toolchain
description: >
  MUST USE when setting up or troubleshooting local-first media/authoring tooling on Fedora 44/Linux.
  Covers: Piper TTS (incl. Arabic model sources), TimesFM, Penpot (Flatpak or Compose),
  Open Montage (Remotion render pipeline), Codebase Memory MCP, local voice alternatives.
  Use for: install/run/troubleshoot these tools, choose local route vs cloud, resolve blocked
  renders, missing Arabic TTS model, or missing Compose files.
metadata:
  openclaw:
    homepage: https://github.com/calesthio/OpenMontage
---

# Fedora 44 Local Media Toolchain

## Why this skill

This class of task keeps recurring in this environment:
- User wants **no seafood rule, nopaid cloud subscriptions, local-first** authoring.
- Fedora 44 is the host OS (Node 22, pnpm, Docker/Flatpak, Python 3.11).
- Open Montage, Piper, TimesFM, Penpot, Codebase Memory MCP show up together.

This skill captures the verified install/runtime patterns for this exact machine.

## Fedora 44 baseline (verified 2026-06-27)

| Component | Verified state | Notes |
|-----------|----------------|-------|
| Node.js | v22.x installed | Corepack missing; use npm-global pnpm |
| pnpm | 10.33.2 via npm-global | `~/.npm-global/bin/pnpm` |
| Docker Compose | v5.2.0 | `docker compose` works; daemon not always running |
| Flatpak | 1.18.0 | install GUI apps (Penpot, etc.) |
| Python | 3.11 (uv) | pip/pipx/venv available |

## Tool routing

| Tool | Fedora path | Quick command |
|------|-------------|---------------|
| Piper TTS | Binary `~/.local/bin/piper`; models `~/piper-models` | `piper -m model.onnx -c model.onnx.json -i in.txt -f out.wav` |
| Piper Arabic model | `rhasspy/piper-voices` on HF has `ar/ar_JO/kareem/medium/...` | Download via `huggingface_hub` or CLI |
| TimesFM | pip in active venv | `python3 -m pip install timesfm` |
| Penpot desktop | Flatpak `com.authormore.penpotdesktop` | `flatpak install -y flathub com.authormore.penpotdesktop` |
| Open Montage | `/home/hatem/OpenMontage` | run `python3 render_demo.py --list` first |
| Codebase Memory MCP | Binary `~/.local/bin/codebase-memory-mcp` | DB in `~/.codebase-memory-mcp/db` |
| World Monitor | PyPI stub package exists at version 2023.9.1; repo is https://github.com/anzechannel/WorldMonitor | verify before relying on functionality |

## Piper TTS — Arabic support

- Repo path on HF: `rhasspy/piper-voices` with `ar/ar_JO/kareem/medium/ar_JO-kareem-medium.onnx` and `.onnx.json`.
- If downloads time out or return incomplete files, check `~/piper-models/.cache/huggingface/download/.../incomplete` and retry with `force_download=True`.
- Fallback if Piper Arabic is blocked: use `node-edge-tts` via npm for Arabic-capable TTS, or use `gTTS` for Arabic strings (note: gTTS is Arabic-capable but requires network).

## Open Montage — run pattern

- This repo is **not** a Node root; it has no package.json at `/home/hatem/OpenMontage`.
- Use the provided Python driver: `python3 render_demo.py --list` to see available demos.
- Render: `python3 render_demo.py code-to-screen` (or `focusflow-pitch`, `world-in-numbers`).
- Render errors often come from `npx remotion` external calls or network blocks (seen Timeout ENETUNREACH). Retry with offline/stable demo props only; do not point at external CDN media.

## Penpot — two supported modes

- **Desktop:** Flatpak `com.authormore.penpotdesktop` is stable on Fedora 44.
- **Self-hosted:** upstream Compose file path changes; if `main/stable/develop` 404s, use official docs, not guessed GitHub raw URLs.

## Cache / skills notes

When the user pastes book chapters, copy them into the vault under `رواية-كرون/01-Projects/07-فصول/` and normalize character names inline there:
- `كرْت` → `كرون`
- `رْت` → `رتوت`

Do NOT overwrite chapter 1 text with chapter 2 text because filenames are inconsistent. Use chapter number and first-line title as truth.

## Preflight-first rule for OpenMontage productions

- Before proposing any production, run `python3 -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu_summary(), indent=2))"` from the OpenMontage working directory.
- Present the capability menu literally: configured/total by capability, then setup offers grouped by env var, then runtime warnings if any.
- When only local assets are available but video/image generation tools are unavailable, explicitly present the fallback options:
  1) still-led treatment with Remotion motion, 2) FFmpeg Ken Burns on stills, 3) collect more local assets.
- Do not silently downgrade an approved motion-led brief to still images or FFmpeg-only without user approval and a logged `render_runtime_selection` decision.

## Python script execution: uv fallback to system Python

When a helper script explicitly requires `uv run python3 ...` but uv install fails with permission denied:
1. Run a preflight check: `python3 -c "import <module>; print('ok')"` to see if the dependency is already installed system-wide.
2. If installed, invoke the script directly with system `python3`: `python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only --timestamps`.
3. Do not block the user-facing task on enforcing uv usage if the system Python already has the required package.

Seen in session: `youtube-transcript-api` was already importable from `/usr` Python in this Fedora 44 environment; uv install failed because `/usr/local/lib/python3.14/site-packages/` is not writable. Direct `python3` execution succeeded without any install.

## Source footage / stock acquisition fallback

- When the user wants real sports/football celebration images for a project:
  1) Use only local/manual placement or user-supplied URLs; do **not** hardcode stock host URLs without verification.
  2) Wikimedia Commons blocks autonomous fetch in this environment; use API/mirror or skip.
  3) Pixabay/Unsplash direct CDN URLs often return small redirect stubs via `mcp_fetch_fetch`; validate with `curl -I` before bulk download.
  4) If no usable image URLs are available, proceed with one verified local asset plus Remotion motion treatment, and ask the user to drop additional real footage/assets into `assets/video/` and `assets/images/`.
- For WC2026-style sports montages, prefer:
  - user-provided footage placed in `assets/video/`
  - stock downloads made with `curl -L` and size validation
  - generated text cards as interstitial scenes when assets are sparse
## Open Montage — Remotion render recipe (still-led success path)

When only 1-2 local images are available and motion generation is unavailable:
- Repeat the verified image across multiple video scenes with different tone grades: `void/steel/neutral/cold`.
- Interleave `kind: "title"` overlay scenes with `variant: "overlay"` in the same timeline.
- Reuse the single crowd/stadium photo with Egyptian flag accents (`#C8102E`, `#D4AF37`) and Arabic title text where desired.
- Generate a complete 21-30s cut with no external CDN assets.

Remotion wiring:
- Do NOT pass `src/wc2026.tsx` directly as entry; Remotion CLI requires a root file with `registerRoot()`.
- Add new project compositions via `Root.tsx`, not standalone scene files.
- Render command: `npx remotion render src/index.tsx <CompositionId> <output.mp4>`.
- `calculateMetadata` export from the scene module is optional; duration can be set directly via `durationInFrames`.

Type-safety pitfall:
- `CinematicRendererProps` accepts `soundtrack/music/captions?: CinematicSoundtrack | undefined`.
- Passing `null` triggers TS2322; use `undefined` or omit the prop.

Post-render verification:
- Always probe the rendered file with `ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,duration -of default=noprint_wrappers=1 <file>`.
- Expected target for full HD social cut: `width=1920 height=1080 r_frame_rate=30/1 duration~30`.

## Open Montage — known gotchas

- `scripts/build.sh` may fail if git submodule `vendored/` directory is empty even after `git submodule update --init --recursive`. MCP tools still function without local CLI build.
- `mcp_fetch_fetch` for GitHub raw `.../main/docker-compose.yaml` often returns HTML 404. Use `github.com/.../raw/...` or docs instead.
- Stock-image URL scraping via generic fetchers frequently returns stubs or redirect pages; verify by file size after download, not by HTTP status alone.
- Image generation depends on provider keys such as `FAL_KEY`, `OPENAI_API_KEY`, `PEXELS_API_KEY`, or `PIXABAY_API_KEY`. If none are configured, do not repeatedly attempt generation; switch to asset-gathering fallback.
- OpenMontage `pipelines/cinematic` is available; `documentary-montage` is more appropriate for real-footage/photo montage when real clips are present. If only stills are available, Remotion motion graphics is preferred over degrading to FFmpeg-only silently.
- Wikimedia Commons robots and pixabay/unsplash fetchers often return redirect stubs via `mcp_fetch_fetch`; use `curl` and verify download sizes before assuming a usable image.
- HuggingFace unauthenticated rate limit can produce 0-byte stubs. Retry later or use `HF_TOKEN`.
- Docker daemon may not be running. Check before Compose workflows.
- Do not use `x_search` when credits/budget is exhausted; fallback to `curl`/`r.jina.ai`.
