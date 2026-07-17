# Voice Cloning Pipeline — Technical Details

## Environment Setup (Verified Working)

```bash
# Conda environment at ~/.local/miniconda3/envs/ginny-tts/
# Python 3.11, torch 2.12.0+cpu, transformers 4.57.1

# MOSS-TTS-Nano source at /tmp/MOSS-TTS-Nano/
# Models at ~/.cache/moss-tts-nano-model/ and ~/.cache/moss-audio-tokenizer-nano/
```

## Key Files

| File | Path | Purpose |
|------|------|---------|
| Generator | ~/.hermes/scripts/ginny_moss.py | Core inference script |
| Wrapper | ~/.hermes/scripts/ginny_moss.sh | Hermes TTS wrapper |
| Enhancer | ~/.hermes/scripts/ginny_post.py | Post-processing with 4 presets |
| Inference | /tmp/MOSS-TTS-Nano/infer.py | MOSS official inference |

## User Preferences (Tested)

- **Best preset:** caring (ginny_warm) — warm, natural, good for Arabic
- **Second best:** energetic — good for excited/happy content
- **Default emotion:** casual or serious depending on content
- **Arabic quality:** Good with short sentences (<2000 chars)

## Known Issues

1. **WeTextProcessing fails** — always use `--disable-wetext-processing`
2. **Long text times out** — keep under 2000 chars, split if needed
3. **CPU inference slow** — 10-14s first call, 3-5s subsequent
4. **Wiener filter warnings** — harmless RuntimeWarnings from scipy

## Post-Processing Presets Detail

```python
# ginny_post.py presets
PRESETS = {
    "warm_natural": {"warmth_amt": 0.05, "deharsh_db": -2.0, "presence_db": 2.0, "ambient_wet": 0.012},
    "crisp_narration": {"warmth_amt": 0.03, "deharsh_db": -3.0, "presence_db": 3.0, "ambient_wet": 0.008},
    "intimate_soft": {"warmth_amt": 0.08, "deharsh_db": -1.5, "presence_db": 1.0, "ambient_wet": 0.02},
    "energetic": {"warmth_amt": 0.04, "deharsh_db": -2.5, "presence_db": 3.5, "ambient_wet": 0.015},
}
```

## Hermes TTS Config

```yaml
tts:
  provider: moss
  moss:
    type: command
    command: /home/hatem/.hermes/scripts/ginny_moss.sh {text_path} {output_path} casual ambient_v1
    max_text_length: 2000
    output_format: ogg
    voice_compatible: true
```

## Training Data

- 9 enhanced samples at ~/ginny_training_audio/generated/
- Reference audio: 2 MP3 files (57s + 41s) converted to WAV
- Fine-tuning: requires GPU (CUDA), use Google Colab for free T4
