#!/usr/bin/env python3
"""
SFX Timeline Builder
Generates a single SFX WAV track from timestamped events.
Designed to be used with Claude Code's /soundeffects skill.

Usage:
  uv run python build_sfx_track.py --output "My Video - SFX Track.wav" --duration-ms 95000
"""

import argparse
import os
from pathlib import Path
from pydub import AudioSegment


# --- SFX Library Mapping ---
# Resolve sfx/ folder relative to this script (works from any working directory)
SFX_DIR = Path(__file__).resolve().parent.parent / "sfx"

SFX_LIBRARY = {
    "mouse_click":      SFX_DIR / "Mouse Click.wav",
    "double_click":     SFX_DIR / "mixkit-fast-double-click-on-mouse-275.wav",
    "keyboard":         SFX_DIR / "Keyboard-Button-Click-06-c-FesliyanStudios.com_.wav",
    "whoosh":           SFX_DIR / "Whoosh 1.wav",
    "air_hit":          SFX_DIR / "mixkit-air-in-a-hit-2161.wav",
    "ding":             SFX_DIR / "Correct Ding.wav",
    "notification":     SFX_DIR / "mixkit-bike-notification-bell-590.wav",
    "camera_shutter":   SFX_DIR / "Camera Shutter 5.wav",
    "digital_shutter":  SFX_DIR / "mixkit-camera-digital-shutter-1432.wav",
    "riser":            SFX_DIR / "Riser 3.wav",
    "impact":           SFX_DIR / "Impact 7.wav",
    "digital_readout":  SFX_DIR / "textdigitalreadout.wav",
}

# Gain levels (linear -> dB)
# 20% = 20 * log10(0.2) = -13.98 dB
# 50% = 20 * log10(0.5) = -6.02 dB
GAIN_20_PERCENT_DB = -13.98
GAIN_50_PERCENT_DB = -6.02

# Whoosh at 50%, everything else at 20%
LOUD_SFX = {"whoosh"}


def load_sfx(name: str) -> AudioSegment:
    """Load an SFX file, normalize to correct gain, trim to max 1 second."""
    path = SFX_LIBRARY[name]
    if not path.exists():
        raise FileNotFoundError(f"SFX file not found: {path}")
    sfx = AudioSegment.from_file(str(path))

    # Trim to max 1 second
    if len(sfx) > 1000:
        sfx = sfx[:1000]

    # Step 1: Normalize to 0 dBFS (bring peak to maximum)
    peak_normalize = -sfx.max_dBFS
    sfx = sfx.apply_gain(peak_normalize)

    # Step 2: Whoosh at 50%, everything else at 20%
    if name in LOUD_SFX:
        sfx = sfx.apply_gain(GAIN_50_PERCENT_DB)
    else:
        sfx = sfx.apply_gain(GAIN_20_PERCENT_DB)

    return sfx


def build_track(events: list[dict], total_duration_ms: int, output_path: str):
    """
    Build a single SFX track from a list of events.

    events: [{"sfx": "whoosh", "at_ms": 1200}, ...]
    total_duration_ms: total duration matching the video
    output_path: where to save the WAV
    """
    # Create silent canvas at 48kHz stereo (matches typical video audio)
    track = AudioSegment.silent(duration=total_duration_ms, frame_rate=48000)

    for i, evt in enumerate(events):
        sfx_name = evt["sfx"]
        position = evt["at_ms"]

        try:
            sfx = load_sfx(sfx_name)
            track = track.overlay(sfx, position=position)
            print(f"  [{i+1:2d}] {position/1000:6.2f}s  {sfx_name:<20s}  ({len(sfx)}ms)")
        except Exception as e:
            print(f"  [{i+1:2d}] ERROR: {sfx_name} at {position}ms -- {e}")

    # Export
    track.export(output_path, format="wav")
    file_size = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\nExported: {output_path} ({total_duration_ms/1000:.1f}s, {file_size:.1f}MB)")


# --- SFX Event Placements ---
# Claude Code's /soundeffects skill will overwrite this list each time.
# This is just an example placement for reference.

EVENTS_FINAL = [
    # Example: Replace this with your actual timestamped events.
    # Claude Code will analyze your transcript and fill this in.
    {"sfx": "air_hit",         "at_ms": 0},
    {"sfx": "digital_readout", "at_ms": 5000},
    {"sfx": "whoosh",          "at_ms": 10000},
    {"sfx": "impact",          "at_ms": 15000},
]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build SFX track for a video")
    parser.add_argument("--output", default="sfx_track.wav", help="Output WAV path")
    parser.add_argument("--duration-ms", type=int, default=60000, help="Video duration in ms")
    args = parser.parse_args()

    print(f"Building SFX track ({args.duration_ms/1000:.1f}s, {len(EVENTS_FINAL)} events)...\n")
    build_track(EVENTS_FINAL, args.duration_ms, args.output)
    print("\nDone! Drag this file into Descript as an upper audio layer.")
