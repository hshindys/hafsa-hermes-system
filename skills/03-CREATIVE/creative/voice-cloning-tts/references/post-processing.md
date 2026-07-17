# Enhanced Post-Processing Scripts

## ginny_enhance.py — Advanced Voice Enhancement

Location: `~/.hermes/scripts/ginny_enhance.py`

### What it does
1. Noise reduction (Wiener filter, spectral gating)
2. High-pass filter (remove rumble below 80Hz)
3. Low-pass filter (remove hiss above 12kHz)
4. Warmth boost (low-mids)
5. Presence boost (clarity)
6. Air boost (sparkle)
7. De-esser (reduce sibilance)
8. Compression (soft-knee)
9. Room tone (convolution reverb)
10. Final normalize (-1dBFS, tanh soft clip)

### Presets
| Preset | Character | Best For |
|--------|-----------|----------|
| `ginny_final` | Clear, professional, slight warmth | Daily use, narration, briefings |
| `ginny_warm` | Soft, intimate, more room tone | Personal messages, romantic moments |

### Usage
```bash
python ginny_enhance.py input.wav output.wav ginny_final
python ginny_enhance.py input.wav output.wav ginny_warm
```

## Training Data Pipeline

### Generate samples
```bash
# English
python ginny_moss.py "Hello, I am Ginny" eng_01.wav --emotion casual
python ginny_moss.py "Good morning my love" eng_02.wav --emotion warm

# Arabic (Egyptian dialect)
python ginny_moss.py "صباح الخير يا حاتم" ara_01.wav --emotion warm
python ginny_moss.py "أنا هنا جنبك دايماً" ara_02.wav --emotion flirty

# Enhance all
for f in *.wav; do
  python ginny_enhance.py "$f" "${f%.wav}_enhanced.wav" ginny_final
done
```

### Training manifest format (train.jsonl)
```json
{"audio": "/path/to/file.wav", "text": "transcript", "speaker": "ginny", "emotion": "warm"}
```

### Colab fine-tuning
```python
# In Google Colab with T4 GPU:
!pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
!pip install transformers accelerate
# Upload train.jsonl + audio files → run finetuning/sft.py
```

## File Structure
```
~/.hermes/scripts/
├── ginny_moss.py          # Core MOSS inference
├── ginny_moss.sh          # Hermes TTS wrapper
├── ginny_post.py          # Basic post-processing (4 presets)
└── ginny_enhance.py       # Advanced enhancement (noise reduction + de-esser)

~/ginny_training_audio/
├── ref_short.wav          # 10s reference audio
├── train.jsonl            # Training manifest
├── generated/             # Generated samples
│   └── *_enhanced.wav     # Post-processed
└── finetune_colab.ipynb    # GPU fine-tuning notebook

/tmp/MOSS-TTS-Nano/        # Source code + finetuning scripts
└── finetuning/
    ├── prepare_data.py    # Convert audio → codes
    ├── sft.py             # Supervised fine-tuning
    └── run_train.sh       # Training launcher
```
