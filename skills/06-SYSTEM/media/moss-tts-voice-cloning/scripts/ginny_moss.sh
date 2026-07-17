#!/bin/bash
# Ginny MOSS TTS Wrapper for Hermes
TEXT_PATH="$1"
OUTPUT_PATH="$2"
EMOTION="${3:-casual}"
PRESET="${4:-ambient_v1}"

HOME_DIR="/home/hatem"
CONDA_PYTHON="$HOME_DIR/.local/miniconda3/envs/ginny-tts/bin/python"
SCRIPT="$HOME_DIR/.hermes/scripts/ginny_moss.py"

TEXT=$(cat "$TEXT_PATH")
OUTPUT_OGG="${OUTPUT_PATH%.wav}.ogg"
OUTPUT_OGG="${OUTPUT_OGG%.mp3}.ogg"

"$CONDA_PYTHON" "$SCRIPT" "$TEXT" "$OUTPUT_OGG" --emotion "$EMOTION" --preset "$PRESET" 2>/dev/null

if [ -f "$OUTPUT_OGG" ]; then
    cp "$OUTPUT_OGG" "$OUTPUT_PATH"
fi
