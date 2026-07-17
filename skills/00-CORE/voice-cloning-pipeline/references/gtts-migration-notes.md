# gTTS Migration Notes

## Timeline
- **2026-06-24**: User explicitly rejected edge-tts ("no edgs-tss"). Moss TTS broken (no output). Google gTTS adopted as primary.
- Config: `tts.provider: google`, `tts.google.type: command`, wrapper at `/home/hatem/.hermes/scripts/google_tts.sh`

## What was tried and failed
| Provider | Status | Reason |
|----------|--------|--------|
| moss | ❌ Broken | "TTS provider 'moss' produced no output" — persistent |
| edge-tts | ❌ Rejected | User explicitly said "no edgs-tss" |
| Google gTTS | ✅ Working | Requires internet, but generates valid MP3 |

## Voice training technique
Run 5-10 short Arabic sentences through gTTS before first delivery each session to verify quality. Store in `audio_cache/train_*.mp3`.

## User voice preferences
- Arabic (`ar`) — Egyptian dialect
- Warm, caring, affectionate tone
- MP3 format for all channels
- Max 5000 chars per gTTS call
