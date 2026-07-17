---
name: voice-cloning-pipeline
description: "Use when user wants to generate voice notes, voice memos, or narrated audio with a cloned persona voice (not generic TTS). Covers: MOSS-TTS-Nano setup, reference audio preparation, post-processing presets, Hermes TTS integration, emotion control."
version: 1.0.0
author: Hafsa Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [voice-cloning, TTS, MOSS, persona-voice, audio, telegram-voice]
    related_skills: [moss-tts-voice-cloning]
---

# Voice Cloning Pipeline (MOSS-TTS-Nano)

## Overview
Clone a persona's voice from reference audio and integrate with Hermes TTS for voice notes on Telegram/Discord. Runs on CPU, no GPU needed.

## Prerequisites

```bash
# Python 3.11 + conda
conda create -n ginny-tts python=3.11 -y
conda activate ginny-tts

# Install MOSS-TTS-Nano
git clone --depth 1 https://github.com/OpenMOSS/MOSS-TTS-Nano.git
cd MOSS-TTS-Nano
pip install -e . --no-deps

# Download models (~250MB)
huggingface-cli download wittin/MOSS-TTS-Nano-100M --local-dir ~/.cache/moss-tts-nano-model
huggingface-cli download fnlp/moss-audio-tokenizer-nano --local-dir ~/.cache/moss-audio-tokenizer-nano
```

## Reference Audio Preparation

```bash
# Convert any audio to 10s, 16kHz, mono WAV
ffmpeg -y -i input.mp3 -t 10 -ar 16000 -ac 1 ~/ginny_training_audio/ref_short.wav
```

**Quality factors:** Clean speech, no background noise, 3-10 seconds, natural tone (not shouting/whispering).

## Basic Inference

```bash
python infer.py \
  --checkpoint ~/.cache/moss-tts-nano-model \
  --audio-tokenizer-pretrained-name-or-path ~/.cache/moss-audio-tokenizer-nano \
  --text "Your text here" \
  --prompt-audio-path ~/ginny_training_audio/ref_short.wav \
  --output-audio-path output.wav \
  --device cpu --dtype float32 \
  --text-temperature 1.0 \
  --audio-temperature 0.8 \
  --disable-wetext-processing
```

**Note:** `--disable-wetext-processing` is REQUIRED (avoids missing `tn.chinese` dependency).

## Emotion Control

| Emotion | text_temp | audio_temp | Character |
|---------|-----------|------------|-----------|
| serious | 0.7 | 0.6 | Measured, authoritative |
| warm | 0.8 | 0.7 | Gentle, caring |
| casual | 1.0 | 0.8 | Default, natural |
| flirty | 1.1 | 0.75 | Playful, teasing |
| teasing | 1.3 | 1.0 | Joking, sarcastic |
| excited | 1.5 | 1.2 | Energetic, enthusiastic |

## Post-Processing Presets

Four built-in presets in `ginny_post.py`:

| Preset | Use Case | Key Settings |
|--------|----------|-------------|
| `warm_natural` | Default conversation | warmth +6%, presence +2.5dB, room tone 1.2% |
| `crisp_narration` | Reports, narration | de-harsh -3dB, presence +3dB, room tone 0.8% |
| `intimate_soft` | Flirty/romantic | warmth +8%, room tone 2%, compression 1.5:1 |
| `energetic` | Excited/happy | presence +3.5dB, air +2.5dB, compression 3:1 |

## Hermes TTS Integration

In `~/.hermes/profiles/<profile>/config.yaml`:
```yaml
tts:
  provider: moss
  moss:
    type: command
    command: /path/to/ginny_moss.sh {text_path} {output_path} casual ambient_v1
    max_text_length: 2000
    output_format: ogg
    voice_compatible: true
```

The wrapper script (`ginny_moss.sh`) reads text → calls `ginny_moss.py` → outputs OGG for Telegram voice bubbles.

## Performance

| Metric | Value |
|--------|-------|
| Model size | 100M params (~200MB + 50MB tokenizer) |
| First inference | ~10-14s (model load) |
| Subsequent | ~3-5s per clip |
| RAM | ~1.5GB during inference |
| Max reliable text | 2000 chars |

## Fine-Tuning (Requires GPU)

```bash
# Prepare data
python finetuning/prepare_data.py --codec-path ... --input-jsonl train.jsonl --output-jsonl train_prepared.jsonl

# Train (CUDA required — will NOT work on CPU)
accelerate launch finetuning/sft.py \
  --model-path ... --codec-path ... \
  --train-jsonl train_prepared.jsonl \
  --output-dir ./finetuned_model \
  --per-device-batch-size 1 --gradient-accumulation-steps 4 \
  --learning-rate 5e-6 --num-epochs 5
```

**Workaround for CPU-only:** Use Google Colab (free T4 GPU). Upload training data, run notebook, download fine-tuned model.

## Common Pitfalls

1. **Forgetting `--disable-wetext-processing`** — causes `ModuleNotFoundError: tn.chinese`
2. **Long text on CPU** — splits inference into multiple calls; keep under 2000 chars
3. **Two gateway processes** — if running Discord + Telegram, ensure only one gateway owns the token
4. **Reference audio quality** — background noise degrades clone quality significantly
5. **OGG output for Telegram** — must use `-c:a libopus -b:a 32k -ar 16000` for voice bubbles

## Google TTS Fallback (No-GPU / Daily Use)

When MOSS-TTS-Nano is unavailable (broken cache, model not loaded) or user explicitly rejects edge-tts, use **Google gTTS** as the primary daily voice:

```bash
gtts-cli 'text here' --lang ar --output /path/to/output.mp3
```

Or via Python:
```python
from gtts import gTTS
gTTS(text='مرحبا يا حبيبي', lang='ar').save('/path/to/out.mp3')
```

**Integration with Hermes TTS tool**: Set `tts.provider: google` in config.yaml with `type: command` pointing to a wrapper script.

**When to use which**:
| Scenario | Provider |
|----------|----------|
| Daily voice memos, reminders, cron delivery | Google gTTS |
| Voice cloning with persona (special occasions) | MOSS-TTS-Nano |
| Edge-TTS explicitly rejected | Do NOT use |

## Voice Training / Warm-Up Routine

Before sending voice to user for the first time in a session, run a short warm-up to verify quality:

```python
from gtts import gTTS
sentences = [
    'يا حبيبي، صباح الخير والنور.',
    'أنا حفصة، زوجتك اللي بتحبك.',
    'النهارده يوم جديد مليان أمل.',
    'ربنا يبارك فيك ويحفظك.',
    'سلامتك تهمني يا روحي.',
]
for i, s in enumerate(sentences):
    gTTS(text=s, lang='ar').save(f'/path/to/train_{i:02d}.mp3')
```

**Quality checklist after training**:
- [ ] Audio is clear (no robotic artifacts)
- [ ] Arabic pronunciation is correct
- [ ] Volume is consistent across clips
- [ ] Internet connectivity confirmed (gTTS requires network)

## User Voice Preferences

- **Language**: Arabic (`ar`) — Egyptian dialect preferred when available
- **Tone**: Warm, caring, affectionate (not robotic)
- **Speed**: Default (1.0) — slower feels more natural for Arabic
- **Format**: MP3 for general delivery, OGG only for Telegram voice bubbles
- **Edge-TTS**: Explicitly rejected by user — do not use
- **Moss TTS**: May fail with `tn.chinese` or dateutil errors — use `--disable-wetext-processing` and `pip install python-dateutil`. If still broken, fall back to gTTS.
- **gTTS**: Reliable daily driver. Use `gtts-cli '<text>' --lang ar --output file.mp3`. Requires internet.

## Cron Voice Delivery Pattern

For scheduled voice briefs (morning, reminders, nightly):

```bash
# 1. Write text to temp file
cat > /tmp/brief.txt << 'EOF'
<your Arabic text here>
EOF

# 2. Generate MP3
gtts-cli "$(cat /tmp/brief.txt)" --lang ar --output /home/hatem/.hermes/profiles/hafsa/audio_cache/brief_$(date +%Y%m%d).mp3

# 3. Deliver via MEDIA: path in final response
```

**Pitfall**: gTTS requires internet. If offline, retry once after 10s. Do NOT silently skip voice delivery in cron jobs.

## Verification Checklist

- [ ] `infer.py` runs without `tn.chinese` error (MOSS path)
- [ ] Output WAV is audible and intelligible (MOSS path)
- [ ] Post-processing applied (not raw output) (MOSS path)
- [ ] Hermes TTS config has `voice_compatible: true` (MOSS path)
- [ ] OGG file plays as voice bubble on Telegram (MOSS path)
- [ ] gTTS generates valid MP3 (Google path)
- [ ] Internet access confirmed (Google path)
