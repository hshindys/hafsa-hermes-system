# MOSS-TTS-Nano Fine-Tuning

## Status: Requires GPU (CUDA)

Fine-tuning MOSS-TTS-Nano requires an NVIDIA GPU. Will fail on CPU-only systems:

```
OSError: MOSS-TTS-Nano finetuning requires CUDA, but Accelerate resolved device=cpu.
```

## What Works on CPU

1. **Zero-shot voice cloning** — reference audio → inference → output (good quality)
2. **Data preparation** — `finetuning/prepare_data.py` runs on CPU
3. **Post-processing** — EQ chain dramatically improves quality
4. **Emotion tuning** — temperature parameters change delivery style

## What Requires GPU

- Supervised fine-tuning via `finetuning/run_train.sh`
- Training via `finetuning/sft.py`

## Training Data Preparation (CPU)

```bash
# Prepare data (works on CPU)
python finetuning/prepare_data.py \
  --codec-path ~/.cache/moss-audio-tokenizer-nano \
  --device cpu \
  --input-jsonl ~/ginny_training_audio/train.jsonl \
  --output-jsonl ~/ginny_training_audio/train_prepared.jsonl \
  --batch-size 4
```

## Training Manifest Format

```jsonl
{"audio": "/path/to/chunk_000.wav", "text": "Hello world", "speaker": "ginny"}
{"audio": "/path/to/chunk_001.wav", "text": "مرحبا بالعالم", "speaker": "ginny"}
```

## If You Have a GPU

1. Prepare data on CPU first (or on the GPU machine)
2. Run training:
```bash
bash finetuning/run_train.sh
# Or manually with accelerate launch
```

## Key Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| learning-rate | 1e-5 | Lower for small datasets |
| num-epochs | 3-5 | More epochs with small data risks overfitting |
| per-device-batch-size | 1 | Must be 1 on CPU |
| gradient-accumulation-steps | 4-8 | Compensate for small batch |
| max-length | 512-1024 | Shorter for voice cloning |
| channelwise-loss-weight | 1,16 or 1,32 | Audio codec layers weighting |

## Recommendation

For most users, zero-shot cloning + post-processing is sufficient. Only pursue fine-tuning if:
- You have 30+ minutes of clean reference audio
- You have access to a GPU
- Zero-shot quality is not acceptable
