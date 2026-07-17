# MOSS-TTS-Nano Import Fix — Session 2026-06-22

## Problem
```
ImportError: cannot import name 'MOSS_TTS_Nano' from 'moss_tts_nano'
```

## Root Cause
The pip package `moss-tts-nano` exposes only config/model classes:
- `MossTTSNanoConfig`
- `MossTTSNanoForCausalLM`
- `MossTTSNanoGenerationOutput`
- etc.

There is NO high-level `MOSS_TTS_Nano` class for inference.

## Fix
Use subprocess to call `infer.py` directly:

```python
cmd = [
    CPY, "/tmp/MOSS-TTS-Nano/infer.py",
    "--checkpoint", MDIR,
    "--audio-tokenizer-pretrained-name-or-path", TDIR,
    "--text", text,
    "--prompt-audio-path", ref,
    "--output-audio-path", out,
    "--device", "cpu",
    "--dtype", "float32",
    "--text-temperature", str(ep["tt"]),
    "--audio-temperature", str(ep["at"]),
    "--disable-wetext-processing"
]
subprocess.run(cmd, capture_output=True, text=True)
```

## Critical Prerequisites
1. `/tmp/MOSS-TTS-Nano/` must exist — clone from GitHub first
2. Models in `~/.cache/moss-tts-nano-model/` and `~/.cache/moss-audio-tokenizer-nano/`
3. Reference audio: `~/ginny_training_audio/ref_short.wav` (10s, 16kHz, mono)
4. `fastmcp` must be installed in the same env (for vault-cortex MCP server)

## Also Discovered
- `--disable-wetext-processing` flag required (avoids `tn.chinese` import error)
- `python-dateutil` must be installed separately
- Fine-tuning requires CUDA GPU — fails on CPU with explicit error
- Zero-shot cloning works well on CPU (~3-5s per clip after model load)
- First clip takes ~5-14s (model load into RAM)
