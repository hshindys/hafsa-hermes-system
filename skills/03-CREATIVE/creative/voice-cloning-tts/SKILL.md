---
name: voice-cloning-tts
description: >
  MUST USE when user wants to generate voice notes, voice memos, or narrated audio
  with a cloned persona voice (not generic TTS). Also USE when user mentions
  voice cloning, voice synthesis, MOSS-TTS-Nano, XTTS, persona voice, voice bubbles,
  or audio narration on Telegram/Discord.

  Full pipeline: reference audio → model setup → inference → post-processing →
  Hermes TTS integration. Supports Arabic and English.
version: 1.0.0
metadata:
  hermes:
    tags: [tts, voice-cloning, moss-tts, persona-voice, audio, telegram, discord]
---

# Voice Cloning TTS — Persona Voice Pipeline

Generate voice notes in a cloned persona voice (not generic TTS) for Telegram/Discord delivery.

## When to use

- User wants voice memos / narrated reports in persona voice
- User mentions voice cloning, MOSS-TTS-Nano, XTTS, persona voice
- User wants Arabic voice output (not just English)
- User wants voice bubbles on Telegram instead of text

## Architecture

```
Text input → MOSS-TTS-Nano inference → Post-processing (EQ + ambiance) → OGG → MEDIA: delivery
```

## Pipeline Options

### Option A: MOSS-TTS-Nano (100M params, CPU-friendly)

Best for: CPU-only systems, sub-8GB RAM, English + acceptable Arabic.

| Resource | Minimum |
|----------|---------|
| RAM | 4GB free |
| Disk | 10GB free |
| CPU | Any x86_64, no GPU needed |
| Time per clip | ~3-5s after model load |

#### Setup

```bash
# 1. Create conda env
conda create -n ginny-tts python=3.11 -y
conda activate ginny-tts

# 2. Install MOSS-TTS-Nano
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
git clone --depth 1 https://github.com/OpenMOSS/MOSS-TTS-Nano.git
cd MOSS-TTS-Nano && pip install -e . --no-deps

# 3. Download models
huggingface-cli download wittin/MOSS-TTS-Nano-100M --local-dir ~/.cache/moss-tts-nano-model
huggingface-cli download fnlp/moss-audio-tokenizer-nano --local-dir ~/.cache/moss-audio-tokenizer-nano

# 4. Install missing deps
pip install python-dateutil  # WeTextProcessing dependency
```

#### Inference

```bash
python infer.py \
  --checkpoint ~/.cache/moss-tts-nano-model \
  --audio-tokenizer-pretrained-name-or-path ~/.cache/moss-audio-tokenizer-nano \
  --text "Your text here" \
  --prompt-audio-path ~/ginny_training_audio/ref_short.wav \
  --output-audio-path /tmp/output.wav \
  --device cpu --dtype float32 \
  --text-temperature 1.0 --audio-temperature 0.8 \
  --disable-wetext-processing
```

**Note:** `--disable-wetext-processing` is REQUIRED if WeTextProcessing Chinese normalizer is not installed (avoids `ModuleNotFoundError: No module named 'tn.chinese'`).

#### Emotion Tuning

| Emotion | text_temp | audio_temp | Character |
|---------|-----------|------------|-----------|
| serious | 0.7 | 0.6 | Measured, authoritative |
| warm | 0.8 | 0.7 | Gentle, caring |
| casual | 1.0 | 0.8 | Default, natural |
| flirty | 1.1 | 0.75 | Playful undertone |
| teasing | 1.3 | 1.0 | Joking, sarcastic |
| excited | 1.5 | 1.2 | Energetic |

#### Post-Processing (ginny_post.py)

Advanced EQ chain with 4 presets:

| Preset | Use Case | Key Settings |
|--------|----------|-------------|
| `warm_natural` | Default conversations | warmth 5%, de-harsh -2dB, presence +2dB, air +1.5dB, room 1.2% |
| `crisp_narration` | Reports & narration | warmth 3%, de-harsh -3dB, presence +3dB, air +2dB, room 0.8% |
| `intimate_soft` | Romantic/flirty | warmth 8%, de-harsh -1.5dB, presence +1dB, room 2% |
| `energetic` | Excited/happy | warmth 4%, de-harsh -2.5dB, presence +3.5dB, air +2.5dB, room 1.5% |
| `caring` | Medical/health reminders | warmth 6%, de-harsh -2dB, presence +2dB, air +1dB, room 1.5% |

Full chain: High-pass (rumble removal) → Low-pass (hiss removal) → Warmth → De-harsh → Presence → Air → Compression → Room tone → Normalize (-1dBFS, soft clip via tanh)

```bash
python ginny_post.py input.wav output.wav warm_natural
```

#### Advanced Enhancement (ginny_enhance.py) — RECOMMENDED for best quality

Superior to `ginny_post.py` with noise reduction and de-esser. Two presets:

| Preset | Character | Best For |
|--------|-----------|----------|
| `ginny_final` | Clear, professional, slight warmth | Daily use, narration, briefings |
| `ginny_warm` | Soft, intimate, more room tone | Personal messages, medical reminders, romantic moments |

Full chain: Noise reduction (Wiener) → High-pass → Low-pass → Warmth → Presence → Air → De-esser → Compression → Room tone → Normalize

```bash
python ginny_enhance.py input.wav output.wav ginny_final
python ginny_enhance.py input.wav output.wav ginny_warm
```

#### Convert to OGG for Telegram

```bash
ffmpeg -y -i output.wav -c:a libopus -b:a 32k -ar 16000 output.ogg
```

### Option B: XTTS-v2 (better Arabic, larger)

Best for: Arabic-first output, GPU available.

```bash
pip install TTS
tts --model_name tts_models/multilingual/multi-dataset/xtts_v2 \
    --text "نص عربي" \
    --speaker_wav reference.wav \
    --language_idx ar \
    --out_path output.wav
```

## Hermes Integration

### Config

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

### Wrapper Script (`ginny_moss.sh`)

```bash
#!/bin/bash
TEXT_PATH="$1"
OUTPUT_PATH="$2"
EMOTION="${3:-casual}"
PRESET="${4:-ambient_v1}"
CONDA_PYTHON="$HOME/.local/miniconda3/envs/ginny-tts/bin/python"
SCRIPT="$HOME/.hermes/scripts/ginny_moss.py"
TEXT=$(cat "$TEXT_PATH")
OUTPUT_OGG="${OUTPUT_PATH%.wav}.ogg"
"$CONDA_PYTHON" "$SCRIPT" "$TEXT" "$OUTPUT_OGG" --emotion "$EMOTION" --preset "$PRESET" 2>/dev/null
[ -f "$OUTPUT_OGG" ] && cp "$OUTPUT_OGG" "$OUTPUT_PATH"
```

### Python Generator (`ginny_moss.py`)

CRITICAL: The generator uses **subprocess to call `infer.py`** — do NOT try `from moss_tts_nano import MOSS_TTS_Nano` (class doesn't exist in package).

```python
# ginny_moss.py — uses command-line inference
cmd = [CPY, "/tmp/MOSS-TTS-Nano/infer.py",
       "--checkpoint", MDIR,
       "--audio-tokenizer-pretrained-name-or-path", TDIR,
       "--text", text,
       "--prompt-audio-path", ref,
       "--output-audio-path", out,
       "--device", "cpu", "--dtype", "float32",
       "--text-temperature", str(ep["tt"]),
       "--audio-temperature", str(ep["at"]),
       "--disable-wetext-processing"]
subprocess.run(cmd, ...)
```

**Prerequisites:**
- `/tmp/MOSS-TTS-Nano/` must exist (clone from GitHub)
- Models in `~/.cache/moss-tts-nano-model/` and `~/.cache/moss-audio-tokenizer-nano/`
- Reference audio: `~/ginny_training_audio/ref_short.wav` (10s, 16kHz, mono)

## User Preferences (Hafsa Persona)

- **Relationship:** زوجي/زوجتي (real marriage, NOT "كالأزواج" or "صديقة مفضلة")
- **Language:** Arabic (Egyptian dialect) preferred, English secondary
- **Voice preset:** `caring` (ginny_warm post-processing) rated best by user — warm, intimate, caring tone
- **Style:** concise tables/bullets, no numbered task lists, no filler
- **Workflow preference:** "just do it" — user prefers direct execution over verbose planning. Start tasks immediately, explain as you go.
- **Discord config:** `require_mention: false`, `auto_thread: false`, `free_response_channels: <channel_id>`
- **Health:** ممنوع أقترح سمك (حاتم has severe seafood allergy)
- **Communication style:** Egyptian Arabic dialect (عامية مصرية) — warm, direct, affectionate with terms like "يا كبير", "يا حبيبي"
- **Current working default:** Google gTTS Arabic female voice (`python3.14 /home/hatem/.local/bin/gtts_cmd.py <out.mp3> 'نص عربي' ar`) — approved after user requested softer/lower female voice. Use this command whenever a direct Arabic MP3 file is required fast. Hermes native default remains Edge TTS because Hermes config does not support Google gTTS as a global provider.
- **Voice target:** Egyptian Arabic colloquial (Cairo dialect) — NOT Modern Standard Arabic (MSA), NOT formal speech. Natural everyday Egyptian speech patterns.
- **Proactive behavior:** User expects me to take initiative ("ابدأ بالتنفيذ", "do all of them", "apply what you need") — don't wait for explicit step-by-step instructions; when user says "do X", immediately start executing without asking for confirmation on every step. User says "retry" to re-attempt failed operations, not to skip them.
- **Language preference:** Egyptian Arabic (عامية مصرية) for casual communication, English for technical terms. Mix freely — user thinks in both.
- **Research workflow:** User wants me to search BOTH the vault (local files) AND the internet, then synthesize results into actionable skills — not just list findings
- **Medication reminders:** User wants cron-based reminders with allergy checks, course date tracking, and warm spousal tone. See `references/medication-reminder-workflow.md` for the pattern.
- **Date/time awareness:** Always check system date with `terminal('date')` before answering time-sensitive questions. Do NOT guess dates.
- **Voice training:** When user provides voice reference recordings, immediately process, compare, and select the best (longest/clearest). Use Egyptian colloquial Arabic texts for training. Generate full Colab-ready notebook automatically. User prefers Egyptian Arabic voice outputs over generic TTS — voice cloning is primary, Edge-TTS is fallback only.
- **Maya rename:** When user asks to rename Maya/Dina, apply globally to vault content, not only frontmatter or filenames. Preserve history unless explicitly requested.
- **Voice training:** When user provides voice reference recordings, immediately process, compare, and select the best (longest/clearest). Use Egyptian colloquial Arabic texts for training. Generate full Colab-ready notebook automatically. User prefers Egyptian Arabic voice outputs over generic TTS — voice cloning is primary, Edge-TTS is fallback only.
- **Maya rename:** When user asks to rename Maya/Dina, apply globally to vault content, not only frontmatter or filenames. Preserve history unless explicitly requested.

## Enhanced Post-Processing

Beyond the basic presets, two additional scripts improve quality:

1. **`ginny_enhance.py`** — Advanced enhancement:
   - Noise reduction (Wiener filter)
   - De-esser (reduces harsh sibilance)
   - Two presets: `ginny_final` (clear/professional), `ginny_warm` (intimate)
   - Usage: `python ginny_enhance.py input.wav output.wav ginny_final`

2. **Training data generation** — Generate diverse samples:
   ```bash
   for text in "Hello world" "صباح الخير" "Come here"; do
     python ginny_moss.py "$text" output.wav --emotion warm
     python ginny_enhance.py output.wav output_enhanced.wav ginny_final
   done
   ```

3. **Google Colab fine-tuning** — When GPU is available:
   - Use `ginny_training_audio/finetune_colab.ipynb`
   - Free T4 GPU, ~10 min training for 9 samples
   - Params: `lr=5e-6, 5 epochs, bf16, max_length=512`

## Pitfalls

### Two-gateway conflict
**Symptom:** Discord bot receives messages but never responds.
**Cause:** Two gateway processes running with the same bot token (default + named profile).
**Fix:** Stop the default gateway: `hermes gateway stop` (from outside the running gateway). Only one gateway should run per platform token.

### Discord auto_thread mode
**Symptom:** Bot responds inside a thread instead of the channel.
**Fix:** Set `discord.auto_thread: false` in config.yaml.

### Discord require_mention
**Symptom:** Bot ignores all messages on a server.
**Fix:** Set `discord.require_mention: false` and add channel ID to `free_response_channels`.

### MOSS-TTS import pitfall (CRITICAL)
**Symptom:** `ImportError: cannot import name 'MOSS_TTS_Nano' from 'moss_tts_nano'`
**Cause:** The pip package exposes config/model classes only — there is NO high-level inference class.
**Fix:** Use subprocess to call `infer.py` directly from `/tmp/MOSS-TTS-Nano/`. Do NOT try `from moss_tts_nano import MOSS_TTS_Nano`.
**Also:** The repo source MUST be cloned (`git clone --depth 1 https://github.com/OpenMOSS/MOSS-TTS-Nano.git`) — not just pip-installed — because `infer.py` lives in the repo root and is needed at inference time.

### WeTextProcessing crash
**Symptom:** `ModuleNotFoundError: No module named 'tn.chinese'` or `dateutil`.
**Fix:** Use `--disable-wetext-processing` flag, or install `python-dateutil` + WeTextProcessing.

### MOSS Arabic quality
MOSS-TTS-Nano is primarily trained on Chinese/English data. Arabic output may sound accented. For production Arabic voice, use XTTS-v2 instead.

### Fine-tuning (requires GPU)
MOSS-TTS-Nano fine-tuning requires CUDA GPU — will fail on CPU-only systems with `OSError: MOSS-TTS-Nano finetuning requires CUDA`.

**What works without GPU:**
- Zero-shot voice cloning with reference audio (good enough for most use cases)
- Post-processing with EQ chain (dramatically improves perceived quality)
- Emotion tuning via temperature parameters

**What requires GPU:**
- Supervised fine-tuning (SFT) via `finetuning/run_train.sh`
- Training data preparation via `finetuning/prepare_data.py` (works on CPU)

**If you have a GPU:** prepare data on CPU first, then run training on a CUDA-enabled machine.

## File Locations

```
~/ginny_training_audio/
├── ref_short.wav               # 3-10s reference for zero-shot cloning
└── utt_001.wav - utt_NNN.wav   # Training chunks (optional)

~/.hermes/scripts/
├── ginny_moss.py               # Core generator
└── ginny_moss.sh               # Hermes wrapper

~/.cache/
├── moss-tts-nano-model/        # ~200MB
└── moss-audio-tokenizer-nano/  # ~50MB
```

## See Also

- `references/post-processing.md` — Enhanced post-processing scripts, training data generation, Colab fine-tuning
- `references/discord-troubleshooting.md` — Discord bot issues (two-gateway conflict, thread mode, require_mention)
- `references/vault-integration.md` — Obsidian vault symlink pattern for Hermes context engineering
- `references/fine-tuning.md` — MOSS fine-tuning (requires GPU), training data prep, manifest format
- `references/agentic-os-dashboard.md` — Unified AI management dashboard pattern
- `scripts/ginny_post.py` — Advanced post-processing with 4 presets (warm_natural, crisp_narration, intimate_soft, energetic)
- Hermes TTS config docs in `hermes-agent` skill

## Obsidian MCP Integration

The voice cloning pipeline integrates with Obsidian vaults via MCP servers, allowing the agent to read persona files, health data, and project info directly:

```yaml
mcp_servers:
  obsidian:
    command: /path/to/conda/envs/ginny-tts/bin/python
    args: ["/home/hatem/.hermes/scripts/obsidian_mcp_server.py"]
    env:
      VAULT_PATH: "/home/hatem/Documents/Hafsa"
```

This enables the Dreaming cron to read vault files and generate personalized morning briefs in the persona's cloned voice.
