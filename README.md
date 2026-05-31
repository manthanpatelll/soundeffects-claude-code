# 🔊 /soundeffects — Claude Code Plugin

**By Manthan Patel (@LeadGenMan)**

🔗 [LinkedIn](https://www.linkedin.com/in/leadgenmanthan/) • 📸 [Instagram](https://www.instagram.com/leadgenman/) • 🎥 [YouTube](https://www.youtube.com/@LeadGenMan) • 🎵 [TikTok](https://www.tiktok.com/@leadgenmanthan) • 🎓 [Skool Community](https://www.skool.com/ai-inner-circle/about) • 🎬 [TiltIt](https://tiltit.video) • ✏️ [PenAnywhere](https://apps.apple.com/us/app/penanywhere/id6760774183) • 🗣️ [Impromptly AI](https://impromptly.ai/)

* * *

Generate perfectly timed SFX audio tracks for your videos. Give it a video file, and it transcribes your speech with Whisper, maps contextual sound effects to key moments, and outputs a single WAV track you can drag into Descript, Premiere, or any editor.

> Want the full video pipeline? Six more skills (rough cut, captions, YouTube descriptions, Instagram captions, reel overlays, content series) live in **[leadgenman-video-skills](https://github.com/manthanpatelll/leadgenman-video-skills)**.

## What it does

1. Extracts audio from your video
2. Transcribes with OpenAI Whisper (word-level timestamps)
3. Claude analyzes the transcript and maps ~35-50 sound effects to contextual moments
4. Builds a single WAV track aligned to your video timeline

## Included SFX (12 sounds)

| Sound | Use Case |
|-------|----------|
| `digital_readout` | Tech terms, stats, reveals (use 8-10x per track) |
| `whoosh` | Topic transitions, scene changes |
| `impact` | Big reveals, dramatic moments |
| `riser` | Build-up before reveals |
| `ding` | Success, key points |
| `air_hit` | Punchy intros, action verbs |
| `keyboard` | Typing, writing, code |
| `mouse_click` | Clicking, selecting, emphasis |
| `double_click` | Section starts, new topics |
| `notification` | Alerts, tool names, pings |
| `camera_shutter` | Screenshots, showing results |
| `digital_shutter` | Screen captures, code snapshots |

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- ffmpeg

## Install

```bash
# Clone the repo
git clone https://github.com/manthanpatelll/soundeffects-claude-code.git

# Install Python dependencies
cd soundeffects-claude-code/engine
uv sync

# Install the plugin in Claude Code
claude plugin install /path/to/soundeffects-claude-code
```

Or add it directly from GitHub in Claude Code:

```
/plugin install github:manthanpatelll/soundeffects-claude-code
```

## Usage

In Claude Code:

```
/soundeffects:soundeffects /path/to/your/video.mp4
```

That's it. Claude handles the rest -- transcription, SFX mapping, track generation, and opens the output folder when done.

## Output

A single WAV file named `[Your Video] - SFX Track.wav` in the same directory as your video. Drag it into your editor as an upper audio layer.

## License

MIT
