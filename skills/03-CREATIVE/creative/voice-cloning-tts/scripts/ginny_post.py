#!/usr/bin/env python3
"""Advanced post-processing for Ginny voice — EQ chain + room tone"""
import sys, os
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt

def make_room_ir(sr, rt60=0.12, length_ms=60):
    n = int(sr * length_ms / 1000)
    t = np.arange(n) / sr
    envelope = np.exp(-t * 6.9 / rt60)
    noise = np.random.randn(n) * 0.15
    ir = envelope * (1 + noise)
    fade_samples = int(sr * 0.005)
    if fade_samples < n:
        ir[:fade_samples] *= np.linspace(0, 1, fade_samples)
    ir = ir / max(np.max(np.abs(ir)), 1e-8)
    return ir

def post_process(ip, op, preset="warm_natural"):
    import soundfile as sf
    d, sr = sf.read(ip, dtype="float32")
    if len(d.shape) > 1: d = d.mean(axis=1)
    nyq = sr / 2

    presets = {
        "warm_natural": {"warmth_amt":0.05,"warmth_freq":250,"deharsh_db":-2.0,"deharsh_freq":4000,"presence_db":2.0,"presence_freq":3000,"air_db":1.5,"air_freq":8000,"low_cut":80,"high_cut":12000,"ambient":True,"ambient_wet":0.012,"ambient_rt60":0.10,"ambient_ir_ms":50,"compression_ratio":2.0,"compression_threshold":-18},
        "crisp_narration": {"warmth_amt":0.03,"warmth_freq":200,"deharsh_db":-3.0,"deharsh_freq":3500,"presence_db":3.0,"presence_freq":4000,"air_db":2.0,"air_freq":7000,"low_cut":100,"high_cut":10000,"ambient":True,"ambient_wet":0.008,"ambient_rt60":0.08,"ambient_ir_ms":40,"compression_ratio":2.5,"compression_threshold":-20},
        "intimate_soft": {"warmth_amt":0.08,"warmth_freq":300,"deharsh_db":-1.5,"deharsh_freq":5000,"presence_db":1.0,"presence_freq":2500,"air_db":0.5,"air_freq":10000,"low_cut":60,"high_cut":14000,"ambient":True,"ambient_wet":0.02,"ambient_rt60":0.15,"ambient_ir_ms":80,"compression_ratio":1.5,"compression_threshold":-15},
        "energetic": {"warmth_amt":0.04,"warmth_freq":200,"deharsh_db":-2.5,"deharsh_freq":3000,"presence_db":3.5,"presence_freq":5000,"air_db":2.5,"air_freq":6000,"low_cut":80,"high_cut":12000,"ambient":True,"ambient_wet":0.015,"ambient_rt60":0.12,"ambient_ir_ms":60,"compression_ratio":3.0,"compression_threshold":-22},
    }
    p = presets.get(preset, presets["warm_natural"])

    if p["low_cut"] > 0:
        d = sosfilt(butter(2, p["low_cut"]/nyq, btype="high", output="sos"), d)
    if p["high_cut"] < nyq:
        d = sosfilt(butter(2, p["high_cut"]/nyq, btype="low", output="sos"), d)
    if p["warmth_amt"] > 0:
        d = d + p["warmth_amt"] * sosfilt(butter(2, p["warmth_freq"]/nyq, btype="low", output="sos"), d)
    if p["deharsh_db"] < 0:
        hp = butter(1, p["deharsh_freq"]/nyq, btype="high", output="sos")
        lp = butter(1, p["deharsh_freq"]/nyq, btype="low", output="sos")
        d = sosfilt(lp, d) + (10**(p["deharsh_db"]/20)) * sosfilt(hp, d)
    if p["presence_db"] > 0:
        bp = butter(2, [2000/nyq, p["presence_freq"]/nyq], btype="band", output="sos")
        d = d + (10**(p["presence_db"]/20) - 1) * sosfilt(bp, d)
    if p["air_db"] > 0:
        d = d + (10**(p["air_db"]/20) - 1) * sosfilt(butter(1, p["air_freq"]/nyq, btype="high", output="sos"), d)

    thresh = 10**(p["compression_threshold"]/20)
    ratio = p["compression_ratio"]
    d = np.where(np.abs(d) > thresh, np.sign(d) * (thresh + (np.abs(d) - thresh) / ratio), d)

    if p.get("ambient"):
        ir = make_room_ir(sr, rt60=p.get("ambient_rt60",0.12), length_ms=p.get("ambient_ir_ms",60))
        wet = fftconvolve(d, ir, mode="same")
        wet = wet / max(np.max(np.abs(wet)), 1e-8)
        d = (1 - p["ambient_wet"]) * d + p["ambient_wet"] * wet

    pk = np.max(np.abs(d))
    if pk > 0: d = d * (10**(-1/20) / pk)
    d = np.tanh(d * 0.95) / 0.95

    import soundfile as sf
    sf.write(op, d, sr)
    return True

if __name__ == "__main__":
    ip = sys.argv[1]
    op = sys.argv[2] if len(sys.argv) > 2 else ip.replace(".wav", "_processed.wav")
    preset = sys.argv[3] if len(sys.argv) > 3 else "warm_natural"
    post_process(ip, op, preset)
    print(f"Processed: {op} ({preset})")
