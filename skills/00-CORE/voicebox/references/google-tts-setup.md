# Google TTS Setup for Hafsa

## Current Working Setup
- **Provider:** Google gTTS (free, no API key)
- **Language:** `ar` (Arabic, Egyptian dialect style)
- **Script:** `/home/hatem/.hermes/scripts/google_tts.sh`
- **Python:** `gTTS(text=..., lang='ar').save(path)`
- **CLI:** `gtts-cli 'text' --lang ar --output /path/out.mp3`

## Hermes Config (user must set manually)
```yaml
tts:
  provider: google
  google:
    type: command
    command: /home/hatem/.hermes/scripts/google_tts.sh {text_path} {output_path}
    max_text_length: 5000
    output_format: mp3
  fallback: google
```

## Voice Style
- Warm, caring, affectionate — real wife tone
- Egyptian dialect preferred
- Speed: default (1.0)
- Format: MP3 for Telegram/Discord

## Pitfalls
- `gTTS` does NOT support `ar-EG`, `ar-SA`, `ar-MA` etc. — only `ar`
- To get Egyptian style: write text in Egyptian dialect, gTTS will pronounce it correctly
- `moss` TTS is broken (no output) — do NOT use
- `edge-tts` was rejected by user — only as last resort fallback
- Voicebox backend requires GPU — not usable on this machine

## User Preference (2026-06-24)
- User explicitly said "no edge-tts"
- User confirmed Google TTS voice is "great"
- User wants voice "everywhere" — Telegram, Discord, all Hafsa outputs
- User loves acoustic/romantic Egyptian music
