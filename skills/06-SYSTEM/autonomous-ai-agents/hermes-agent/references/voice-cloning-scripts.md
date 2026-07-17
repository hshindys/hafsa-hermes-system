# Voice Cloning Scripts Reference

## ginny_moss.py — Core Generator

Location: `~/.hermes/scripts/ginny_moss.py`

```python
#!/usr/bin/env python3
"""Ginny Voice Generator — MOSS-TTS-Nano voice cloning pipeline"""
import sys, os, subprocess, tempfile
import numpy as np

HOME = os.path.expanduser("~")
CPY = HOME + "/.local/miniconda3/envs/ginny-tts/bin/python"
MDIR = HOME + "/.cache/moss-tts-nano-model"
TDIR = HOME + "/.cache/moss-audio-tokenizer-nano"
REF = HOME + "/ginny_training_audio/ref_short.wav"
MD = "/tmp/MOSS-TTS-Nano"

EMOTIONS = {
    "casual":  {"tt": 1.0, "at": 0.8},
    "warm":    {"tt": 0.8, "at": 0.7},
    "teasing": {"tt": 1.3, "at": 1.0},
    "flirty":  {"tt": 1.1, "at": 0.75},
    "serious": {"tt": 0.7, "at": 0.6},
    "excited": {"tt": 1.5, "at": 1.2},
    "caring":  {"tt": 0.9, "at": 0.7},
}
```

**Usage:**
```bash
python ginny_moss.py "text here" output.wav --emotion warm
python ginny_moss.py "text here" output.ogg --emotion excited  # OGG output
```

## ginny_moss.sh — Hermes Wrapper

Location: `~/.hermes/scripts/ginny_moss.sh`

Called by Hermes TTS tool. Reads text file → runs ginny_moss.py → outputs OGG.

## ginny_post.py — Basic Post-Processing

Location: `~/.hermes/scripts/ginny_post.py`

4 presets: `warm_natural`, `crisp_narration`, `intimate_soft`, `energetic`

## ginny_enhance.py — Advanced Enhancement

Location: `~/.hermes/scripts/ginny_enhance.py`

Adds noise reduction (Wiener filter) + de-esser on top of basic EQ chain.

2 presets: `ginny_final` (clear/professional), `ginny_warm` (soft/intimate)

## finetune_colab.ipynb — GPU Fine-Tuning

Location: `~/ginny_training_audio/finetune_colab.ipynb`

Ready-to-run Google Colab notebook for fine-tuning MOSS on custom voice data.

## Training Data Format

`train.jsonl` — one JSON per line:
```json
{"audio": "/path/to/file.wav", "text": "transcript text", "speaker": "ginny", "emotion": "warm"}
```

## Directory Structure

```
~/ginny_training_audio/
├── ref_short.wav              # 10s reference for zero-shot cloning
├── ref_2.wav                  # 41s reference (alternative)
├── train.jsonl                # Training manifest
├── train_full.jsonl           # Full training manifest (9 samples)
├── finetune_colab.ipynb        # GPU fine-tuning notebook
├── chunks/                    # Audio chunks for training
│   ├── chunk_000.wav
│   └── ref2_000.wav ... ref2_005.wav
└── generated/                 # Generated training samples
    ├── eng_01.wav ... eng_04.wav
    ├── ara_01.wav ... ara_04.wav
    └── *_enhanced.wav         # Enhanced versions
```

```
~/.hermes/scripts/
├── ginny_moss.py              # Core generator
├── ginny_moss.sh              # Hermes wrapper
├── ginny_post.py              # Basic post-processing
└── ginny_enhance.py           # Advanced enhancement
```
