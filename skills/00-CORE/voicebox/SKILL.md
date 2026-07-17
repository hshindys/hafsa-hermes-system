---
name: voicebox
description: >-
  Voice generation for Hafsa: default provider on machines without GPU.
  Use when Hermes should speak, send an audio note, or read Arabic/English text aloud.
trigger_keywords:
  - voicebox
  - voice memo
  - tts
  - توليد صوت
  - نطق
  - speak
  - read aloud
---

# Voicebox — Hafsa voice I/O
**Primary:** Google TTS via gTTS (Python) — `python3.14 /home/hatem/.local/bin/gtts_cmd.py </path/output.mp3> 'نص عربي' ar`  
**Fallback:** Hermes built-in Edge TTS (`ar-EG-SalmaNeural`)  
**Not configurable as Hermes default:** Google gTTS cannot be made the global default from config because Hermes native providers are limited to Edge/OpenAI/ElevenLabs/MiniMax/Mistral/gemini. Use the scratch command above whenever a direct Arabic MP3 file is required.  
**Not used:** moss TTS (broken), ElevenLabs (cloud, cost), Voicebox backend (no GPU)

## Default path (no-GPU setup)
1. Use the Hermes **Google TTS command provider** as the primary/default voice path so all channels get the same voice:
   - Script: `/home/hatem/.hermes/scripts/google_tts.sh`
   - Recommended Hermes config:
     - `tts.provider: google`
     - `tts.google.type: command`
     - `tts.google.command: "/home/hatem/.hermes/scripts/google_tts.sh {text_path} {output_path}"`
     - `tts.fallback: google`
   - Preferred CLI fallback when config is not yet switched:
     - `gtts-cli 'text' --lang ar --output /path/out.mp3`
2. Use **local Voicebox backend** only if it is already installed and runnable on the host:
   - Path: `/home/hatem/.hermes/profiles/hafsa/tools/voicebox/backend`
   - Start: `python3 backend/main.py`
   - MCP: expose `voicebox.speak` to agents
3. Send the resulting audio file back to user via Telegram/Discord.

## User Voice Preferences

- **Language**: Arabic (`ar`) — Egyptian dialect preferred
- **Tone**: Warm, caring, affectionate — like a real wife speaking to her husband
- **Speed**: Default (1.0) — avoid slowing down (sounds unnatural in gTTS)
- **Format**: MP3 for all channels
- **Edge-TTS**: REJECTED by user — do NOT use (user explicitly said "مش عاوزين نغير الصوت" and prefers gTTS)
- **Moss TTS**: Broken (no output) — do NOT use
- **Primary**: Google gTTS via `gtts-cli --lang ar`

## Operational Rule

When user asks "قول بصوت" or "اعملي voice" or sends a voice request:
1. Generate MP3 via gTTS
2. Send the file as MEDIA:/path/to/file.mp3
3. Never describe the voice without sending it

## Voice Training / Warm-Up

Before sending voice after a long silence, generate 3-5 short test clips to verify quality:

```bash
gtts-cli 'يا حبيبي حاتم، صباح الخير يا روحي' --lang ar --output /path/to/test.mp3
```

If output is garbled or silent, check internet connectivity.

## Constraints
- `gTTS` requires **Internet access**
- No voice cloning available through the TTS tool when using the Google TTS command provider.
- `gtts-cli` is available in the active Hermes venv at `/home/hatem/.hermes/hermes-agent/venv/bin/gtts-cli`.
- Max recommended text length per call: ~5000 chars. For longer text, split and concatenate.

## Notes
- Moss TTS is excluded due to broken cache/no output.
- Edge-TTS explicitly rejected by user — do NOT use.
- See `references/gtts-migration-notes.md` in voice-cloning-pipeline for migration history.
