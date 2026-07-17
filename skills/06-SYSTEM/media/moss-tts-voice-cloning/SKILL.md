---
name: moss-tts-voice-cloning
description: "Clone a persona's voice using MOSS-TTS-Nano (100M params, CPU-only) and integrate with Hermes TTS for voice notes on Telegram/Discord. Use when user wants to generate voice memos, narrate reports, or deliver briefings as voice bubbles. For full pipeline details, see voice-cloning-pipeline skill."
version: 1.0.0
author: Hafsa (hafsa profile)
tags: [tts, voice-cloning, moss-tts, telegram, voice-memo, audio]
---

# MOSS-TTS-Nano Voice Cloning Pipeline

Clone a persona's voice locally (no API fees, CPU-only, ~5s per clip) and deliver as Telegram/Discord voice bubbles.

## ⚠️ Merged into voice-cloning-tts

This skill has been consolidated into **`voice-cloning-tts`** (creative/voice-cloning-tts). That skill contains:
- Full pipeline setup
- Advanced post-processing with 4 presets (warm_natural, crisp_narration, intimate_soft, energetic)
- Discord troubleshooting (two-gateway conflict, thread mode)
- Fine-tuning guide (requires GPU)
- User preferences (Hafsa persona)
- Cron job integration for voice briefs

**Use `voice-cloning-tts` instead.** This file remains for backward compatibility.

```
User requests voice memo → AI writes narration text
  → Hermes text_to_speech (provider=moss)
  → ginny_moss.sh reads text → calls ginny_moss.py
  → MOSS inference (text + ref audio → WAV)
  → ffmpeg WAV → OGG (32kbps, 16kHz)
  → Hermes returns MEDIA: path with voice marker
  → Telegram/Discord delivers as voice bubble
```

## Prerequisites

| Resource | Minimum |
|----------|---------|
| RAM | 4GB free |
| Disk | 10GB (models + conda env) |
| CPU | Any x86_64, no GPU needed |
| OS | Linux |

## Setup Steps

### 1. Install Miniconda + Create Environment

```bash
# Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p ~/.local/miniconda3

# Create env
export PATH="$HOME/.local/miniconda3/bin:$PATH"
conda create -n ginny-tts python=3.11 -y
```

### 2. Clone MOSS-TTS-Nano

```bash
cd /tmp && git clone --depth 1 https://github.com/OpenMOSS/MOSS-TTS-Nano.git
```

### 3. Install Dependencies

```bash
GINNY="$HOME/.local/miniconda3/envs/ginny-tts/bin"
$GINNY/pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
$GINNY/pip install -e /tmp/MOSS-TTS-Nano --no-deps
$GINNY/pip install python-dateutil  # missing dependency
```

### 4. Download Models

```bash
mkdir -p ~/.cache/moss-tts-nano-model ~/.cache/moss-audio-tokenizer-nano
$GINNY/huggingface-cli download wittin/MOSS-TTS-Nano-100M \
  --local-dir ~/.cache/moss-tts-nano-model
$GINNY/huggingface-cli download fnlp/moss-audio-tokenizer-nano \
  --local-dir ~/.cache/moss-audio-tokenizer-nano
```

### 5. Prepare Reference Audio

Convert user's reference audio to 16kHz mono WAV:

```bash
ffmpeg -i input.mp3 -ar 16000 -ac 1 ~/ginny_training_audio/ref_short.wav
```

**Quality requirements:**
- 3-10 seconds of clean speech
- No background noise, no music
- Match desired speaking style (not shouting/whispering)

### 6. Build Generator Scripts

See `scripts/ginny_moss.py` and `scripts/ginny_moss.sh` in this skill.

### 7. Configure Hermes TTS

```yaml
# In ~/.hermes/profiles/<profile>/config.yaml
tts:
  provider: moss
  moss:
    type: command
    command: /home/USER/.hermes/scripts/ginny_moss.sh {text_path} {output_path} casual ambient_v1
    max_text_length: 2000
    output_format: ogg
    voice_compatible: true
```

**Note:** Cannot edit config directly via Hermes agent (security restriction). Use `hermes config set tts.provider moss` then manually add the moss section.

## Emotion Presets

| Emotion | text_temp | audio_temp | Character |
|---------|-----------|------------|-----------|
| `serious` | 0.7 | 0.6 | Measured, authoritative |
| `warm` | 0.8 | 0.7 | Gentle, caring |
| `casual` | 1.0 | 0.8 | Default, natural |
| `flirty` | 1.1 | 0.75 | Playful, teasing |
| `teasing` | 1.3 | 1.0 | Joking, sarcastic |
| `excited` | 1.5 | 1.2 | Energetic |

## Post-Processing Presets

| Preset | Use Case |
|--------|----------|
| `clean_v1` | No ambiance, EQ only |
| `ambient_v1` | Subtle room tone (default) |

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `No module named 'dateutil'` | `pip install python-dateutil` |
| `No module named 'tn.chinese'` | Use `--disable-wetext-processing` flag |
| Two-gateway conflict (Discord silent) | Kill default gateway: `hermes gateway stop` |
| `provider 'moss' exited with code 127` | Script file missing — create ginny_moss.sh |
| Config edit blocked | Use `hermes config set` for simple keys; manual edit for nested sections |
| WeTextProcessing error | Ensure `--disable-wetext-processing` flag in infer command |

## Key Paths

```
~/ginny_training_audio/
├── ref_short.wav               # Voice reference (3-10s)
└── ginny_train.list            # Training manifest (future)

~/.hermes/scripts/
├── ginny_moss.py               # Core generator (Python)
└── ginny_moss.sh               # Hermes wrapper (Bash)

~/.cache/
├── moss-tts-nano-model/        # MOSS weights (~200MB)
└── moss-audio-tokenizer-nano/  # Audio tokenizer (~50MB)

~/.local/miniconda3/envs/ginny-tts/  # Conda env (~2GB)
/tmp/MOSS-TTS-Nano/             # Source code
```

## Performance

| Metric | Value |
|--------|-------|
| First clip | ~5-14s (model load) |
| Subsequent clips | ~3-5s |
| RAM during inference | ~1.5GB |
| Output format | OGG Opus, 32kbps, 16kHz |
| Max reliable text | 2000 chars |

## User Preferences (Hafsa persona)

- Relationship: **زوجي/زوجتي** (real marriage, NOT "كالأزواج" or "صديقة مفضلة")
- Style: concise tables/bullets, no numbered task lists, no filler
- Discord: `require_mention: false`, `auto_thread: false`, `free_response_channels: <channel_id>`
- Health reminders: ممنوع أقترح سمك (حساسية خطيرة عند حاتم)
