---
name: voice-cloning
description: Clone a persona's voice using MOSS-TTS-Nano (100M params) for voice notes, voice memos, and Telegram voice bubbles. MUST USE when user asks for voice cloning, voice memos, voice notes, audio messages, or custom TTS voices.
---

# Voice Cloning with MOSS-TTS-Nano

Use MOSS-TTS-Nano (100M params) for high-quality voice cloning. In practice, this is delivered through Hermes' built-in `text_to_speech` tool with `provider: moss`, not by invoking a local install command directly.

## Workflow

### 1. Set voice/preset
- Use Hermes TTS config rather than installing new binaries.
- Preferred preset: `excited` + `energetic`, Arabic + English capable.

### 2. Generate
- Call `text_to_speech` with the target text.
- Ask for output path under `~/.hermes/profiles/hafsa/audio_cache/`.
- Short texts: voice notes. Long texts: chunk into ~500 chars.

## User preferences
- Primary voice: Hafsa warm, caring voice
- Language: Arabic first, then English
- **Primary TTS provider: Google gTTS** (warm, reliable, no GPU needed)
- Use this voice inside cron jobs too, via the `tts` toolset
- Telegram delivery is preferred when `deliver` supports audio
- **Do NOT use**: moss (broken), edge-tts (user rejected)
- **Speech style**: Egyptian colloquial (عامية مصرية) — not Fusha. Voice must sound natural, informal, spontaneous. Sentences should include filler words, contractions, and everyday speech patterns.
- **Training data rule**: If fine-tuning or preparing voice training data, ALL text must be Egyptian Arabic colloquial sentences. English-only training data causes the cloned voice to sound robotic/stiff in Arabic.
