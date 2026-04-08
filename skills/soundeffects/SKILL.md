---
name: soundeffects
description: "Generate a perfectly timed SFX audio track for an Instagram reel or video. Invoke as /soundeffects:soundeffects with a video file path. Extracts audio, transcribes with Whisper for word-level timestamps, maps ~35-50 contextual sound effects (including 9-10 digital readouts), and outputs a single WAV file ready to drag into Descript. Use when: user says /soundeffects, wants SFX for a reel, needs a sound effects track, or mentions adding sounds to a video."
---

# Sound Effects Track Generator

## Setup (First Time Only)

This skill requires Python dependencies. Run once after installing:

```bash
cd <PLUGIN_DIR>/engine
uv sync
```

Where `<PLUGIN_DIR>` is wherever you cloned/installed this plugin (e.g., `~/.claude/plugins/soundeffects-claude-code/`).

**System requirements:** ffmpeg, Python 3.10+, uv (Python package manager)

## Workflow

1. **Get file path** from user argument (e.g., `/soundeffects:soundeffects /path/to/video.mp4`)
2. **Verify file exists** and get duration: `ffmpeg -i <file> 2>&1 | grep Duration`
3. **Prepare audio for Whisper**:
   - If **video** (`.mp4`, `.mov`, `.mkv`): extract audio: `ffmpeg -i <video> -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/sfx_audio_extract.wav -y`
   - If **audio** (`.wav`, `.mp3`, `.aac`, `.m4a`): convert to 16kHz mono: `ffmpeg -i <audio> -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/sfx_audio_extract.wav -y`
4. **Transcribe with Whisper** (word-level timestamps):
   ```bash
   cd <PLUGIN_DIR>/engine
   uv run python -c "
   import whisper, json
   model = whisper.load_model('base')
   result = model.transcribe('/tmp/sfx_audio_extract.wav', word_timestamps=True, language='en')
   words = []
   for seg in result['segments']:
       for w in seg.get('words', []):
           words.append({'word': w['word'].strip(), 'start': round(w['start'], 3), 'end': round(w['end'], 3)})
   for w in words:
       print(f'{w[\"start\"]:7.3f}s  {w[\"word\"]}')
   "
   ```
   **IMPORTANT**: `<PLUGIN_DIR>` = the root of this plugin. Find it by looking for the `engine/` folder containing `build_sfx_track.py`. Common locations:
   - `~/.claude/plugins/soundeffects-claude-code/`
   - Wherever the user cloned the repo
5. **Map SFX placements** -- analyze transcript, assign ~25-40 contextual SFX + 9-10 digital readouts
6. **Update EVENTS_FINAL** in `<PLUGIN_DIR>/engine/build_sfx_track.py` with the new placements
7. **Build track**:
   ```bash
   cd <PLUGIN_DIR>/engine
   uv run python build_sfx_track.py --output "<video_dir>/<video_name> - SFX Track.wav" --duration-ms <duration>
   ```
8. **Open output folder**: `open <video_directory>` (macOS) or `xdg-open <video_directory>` (Linux)

## SFX Library

All 12 sounds are bundled in the `sfx/` folder of this plugin. Keys in build script:

| Key | File | Use For |
|-----|------|---------|
| digital_readout | textdigitalreadout.wav | FAVORITE -- tech terms, digital actions, stats, reveals. USE 8-10 TIMES per track. **Min 7s gap** between any two digital_readout placements. Space evenly. |
| whoosh | Whoosh 1.wav | Topic transitions, scene changes. **50% gain.** |
| mouse_click | Mouse Click.wav | "Click on", selecting UI, emphasis |
| keyboard | Keyboard-Button-Click-06-c-FesliyanStudios.com_.wav | "Type", "write", "code", entering text |
| impact | Impact 7.wav | Big reveals, dramatic "NOT", punchlines |
| riser | Riser 3.wav | Build-up before reveals, "power", "massive" |
| ding | Correct Ding.wav | Success, "perfect", key points |
| notification | mixkit-bike-notification-bell-590.wav | Tool names, alerts, pings |
| camera_shutter | Camera Shutter 5.wav | Screenshots, showing results |
| digital_shutter | mixkit-camera-digital-shutter-1432.wav | Screen captures, capturing code |
| air_hit | mixkit-air-in-a-hit-2161.wav | Punchy intros, action verbs |
| double_click | mixkit-fast-double-click-on-mouse-275.wav | Section starts, new topics |

## Rules

- **Gain**: Whoosh at 50%, everything else at 20%
- **Max 1 second** per SFX (trim longer)
- **Min 1.5s gap** between any two SFX
- **Min 7s gap** between any two digital_readout placements (never back-to-back). Space them evenly across the track.
- **~35-50 total** per track (contextual SFX + 8-10 digital readouts)
- **Output name**: `[Video Name] - SFX Track.wav`
- **Always open** the output folder after generating
- **Every placement contextually accurate** -- never add for padding
