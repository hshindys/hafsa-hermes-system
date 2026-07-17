# Egyptian Arabic Voice Training Reference

## Voice clone setup for Hafsa persona
- Primary ref: `/home/hatem/hatem_voice_training/voice2/voice2_ref.wav`
- Chunks: `/home/hatem/hatem_voice_training/chunks_final/`
- Training JSONL: `/home/hatem/hatem_voice_training/train_final.jsonl`
- Preferred TTS: `edge-tts` with `ar-EG-SalmaNeural`
- Banned TTS: Google TTS (`no google tts`)

## Reference selection rule
- Longest/clearest recording wins
- 3+ minutes preferred; 30s minimum useful
- 16kHz mono WAV required for MOSS/Colab
- Keep backup references, do not delete originals

## Egyptian colloquial training text rules
- Use Cairo everyday speech patterns
- Include natural fillers: يعني، ماشي، تمام، حلو
- Mix topics: greetings, tasks, health, Islam, emotions
- Short sentences for 5s chunks
- Avoid MSA; avoid formal phrasing

## Colab notebook artifacts
- `hafsa_voice_clone_training.ipynb` is auto-generated from `train_voice.py`
- Training hyperparams: 5 epochs, lr=1e-5, batch=1, grad_accum=8
- Inference fallback: edge-tts when MOSS fails

## ElevenLabs voice design prompt
- Use 20 Egyptian Arabic lines as training texts
- Voice description: warm Egyptian female, 20s-30s, Cairo dialect, casual
- Settings: stability 0.5, similarity_boost 0.8, style 0.3

## Pitfalls
- Google TTS is banned for this user
- MOSS Arabic is accented; prefer XTTS-v2 for production if available
- Short refs hurt clone quality more than bad texts
- Need quiet room + clear mic for usable ref audio