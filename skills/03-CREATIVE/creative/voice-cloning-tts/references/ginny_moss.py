#!/usr/bin/env python3
"""Ginny Voice Generator — MOSS-TTS-Nano voice cloning pipeline"""
import sys, os, subprocess, time, tempfile, shutil
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
}

def generate(text, out=None, emo="casual", ref=None):
    if out is None: out = "/tmp/gm.wav"
    if ref is None: ref = REF
    ep = EMOTIONS.get(emo, EMOTIONS["casual"])
    cmd = [CPY, MD+"/infer.py",
           "--checkpoint", MDIR,
           "--audio-tokenizer-pretrained-name-or-path", TDIR,
           "--text", text,
           "--prompt-audio-path", ref,
           "--output-audio-path", out,
           "--device", "cpu",
           "--dtype", "float32",
           "--text-temperature", str(ep["tt"]),
           "--audio-temperature", str(ep["at"]),
           "--disable-wetext-processing"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr)
        sys.exit(1)
    return out

def generate_ogg(text, out=None, emo="casual", ref=None):
    if out is None: out = "/tmp/gm.ogg"
    raw = tempfile.mktemp(suffix=".wav")
    try:
        generate(text, raw, emo, ref)
        r = subprocess.run(["ffmpeg","-y","-i",raw,"-c:a","libopus",
                           "-b:a","32k","-ar","16000",out],
                          capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stderr, file=sys.stderr)
            sys.exit(1)
        return out
    finally:
        if os.path.exists(raw): os.remove(raw)

if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else "Hello"
    o = sys.argv[2] if len(sys.argv) > 2 else "/tmp/gm.wav"
    e = "casual"
    if "--emotion" in sys.argv:
        i = sys.argv.index("--emotion")
        if i+1 < len(sys.argv): e = sys.argv[i+1]
    if o.endswith(".ogg"):
        generate_ogg(t, o, e)
    else:
        generate(t, o, e)
    print(f"Generated: {o}")
