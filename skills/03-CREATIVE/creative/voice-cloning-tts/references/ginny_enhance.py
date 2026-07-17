#!/usr/bin/env python3
"""Advanced voice enhancement for Ginny — noise reduction + de-esser + EQ chain"""
import sys, os
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt, wiener

def noise_reduce(y, sr, noise_profile=None):
    """Simple noise reduction using Wiener filter"""
    if noise_profile is None:
        noise_samples = int(sr * 0.5)
        noise_profile = y[:noise_samples]
    y_clean = wiener(y, mysize=5)
    return y_clean

def de_ess(y, sr, freq=4000, threshold=-30, ratio=4):
    """De-esser — reduce harsh sibilance"""
    nyq = sr / 2
    bp = butter(2, [(freq-500)/nyq, (freq+500)/nyq], btype="band", output="sos")
    sib = sosfilt(bp, y)
    sib_abs = np.abs(sib)
    thresh = 10**(threshold/20) * np.max(np.abs(y))
    gain = np.ones_like(sib)
    over = sib_abs > thresh
    gain[over] = 1 / (1 + (sib_abs[over]/thresh - 1) * (ratio-1)/ratio)
    return y * gain

def make_room_ir(sr, rt60=0.12, length_ms=60):
    """Generate a room impulse response"""
    n = int(sr * length_ms / 1000)
    t = np.arange(n) / sr
    envelope = np.exp(-t * 6.9 / rt60)
    noise = np.random.randn(n) * 0.15
    ir = envelope * (1 + noise)
    fade = int(sr * 0.005)
    if fade < n:
        ir[:fade] *= np.linspace(0, 1, fade)
    ir = ir / max(np.max(np.abs(ir)), 1e-8)
    return ir

def voice_enhance(ip, op, preset="ginny_final"):
    import soundfile as sf
    d, sr = sf.read(ip, dtype="float32")
    if len(d.shape) > 1: d = d.mean(axis=1)
    nyq = sr / 2

    presets = {
        "ginny_final": {"nr_strength": 0.3, "low_cut": 80, "high_cut": 12000,
                        "warmth": 0.06, "warmth_freq": 250, "presence": 2.5,
                        "presence_freq": 3500, "air": 1.5, "air_freq": 8000,
                        "deess_freq": 4000, "deess_threshold": -35, "deess_ratio": 3,
                        "comp_ratio": 2.0, "comp_threshold": -18,
                        "room_wet": 0.01, "room_rt60": 0.08, "room_ir_ms": 40},
        "ginny_warm": {"nr_strength": 0.2, "low_cut": 60, "high_cut": 14000,
                       "warmth": 0.10, "warmth_freq": 300, "presence": 1.5,
                       "presence_freq": 2500, "air": 0.5, "air_freq": 10000,
                       "deess_freq": 5000, "deess_threshold": -40, "deess_ratio": 2,
                       "comp_ratio": 1.5, "comp_threshold": -15,
                       "room_wet": 0.02, "room_rt60": 0.12, "room_ir_ms": 60},
    }
    p = presets.get(preset, presets["ginny_final"])

    if p["nr_strength"] > 0:
        d = noise_reduce(d, sr) * p["nr_strength"] + d * (1 - p["nr_strength"])
    if p["low_cut"] > 0:
        d = sosfilt(butter(2, p["low_cut"]/nyq, btype="high", output="sos"), d)
    if p["high_cut"] < nyq:
        d = sosfilt(butter(2, p["high_cut"]/nyq, btype="low", output="sos"), d)
    if p["warmth"] > 0:
        d = d + p["warmth"] * sosfilt(butter(2, p["warmth_freq"]/nyq, btype="low", output="sos"), d)
    if p["presence"] > 0:
        bp = butter(2, [2000/nyq, p["presence_freq"]/nyq], btype="band", output="sos")
        d = d + (10**(p["presence"]/20) - 1) * sosfilt(bp, d)
    if p["air"] > 0:
        d = d + (10**(p["air"]/20) - 1) * sosfilt(butter(1, p["air_freq"]/nyq, btype="high", output="sos"), d)
    d = de_ess(d, sr, freq=p["deess_freq"], threshold=p["deess_threshold"], ratio=p["deess_ratio"])
    thresh = 10**(p["comp_threshold"]/20) * np.max(np.abs(d))
    ratio = p["comp_ratio"]
    if thresh > 0:
        over = np.abs(d) > thresh
        d = np.where(over, np.sign(d) * (thresh + (np.abs(d) - thresh) / ratio), d)
    if p["room_wet"] > 0:
        ir = make_room_ir(sr, rt60=p["room_rt60"], length_ms=p["room_ir_ms"])
        wet = fftconvolve(d, ir, mode="same")
        wet = wet / max(np.max(np.abs(wet)), 1e-8)
        d = (1 - p["room_wet"]) * d + p["room_wet"] * wet
    pk = np.max(np.abs(d))
    if pk > 0:
        d = d * (10**(-1/20) / pk)
    d = np.tanh(d * 0.95) / 0.95
    sf.write(op, d, sr)

if __name__ == "__main__":
    ip = sys.argv[1]
    op = sys.argv[2] if len(sys.argv) > 2 else ip.replace(".wav", "_enhanced.wav")
    preset = sys.argv[3] if len(sys.argv) > 3 else "ginny_final"
    voice_enhance(ip, op, preset)
    print(f"Enhanced: {op}")
