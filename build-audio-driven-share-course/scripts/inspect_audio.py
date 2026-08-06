#!/usr/bin/env python3
"""Inspect an audio file without trusting its extension.

Requires ffprobe and ffmpeg on PATH. Outputs a JSON report describing the
container, codec, presentation duration, decoded duration, and timestamp gaps.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def parse_clock(value: str) -> float:
    h, m, s = value.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--output")
    args = ap.parse_args()

    audio = Path(args.audio)
    if not audio.is_file():
        print(f"Audio not found: {audio}", file=sys.stderr)
        return 2
    for binary in ("ffprobe", "ffmpeg"):
        if shutil.which(binary) is None:
            print(f"Required binary not found: {binary}", file=sys.stderr)
            return 2

    meta_proc = run([
        "ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(audio)
    ])
    if meta_proc.returncode:
        print(meta_proc.stderr, file=sys.stderr)
        return meta_proc.returncode
    meta = json.loads(meta_proc.stdout)
    audio_streams = [s for s in meta.get("streams", []) if s.get("codec_type") == "audio"]
    stream = audio_streams[0] if audio_streams else {}
    container_duration = float(meta.get("format", {}).get("duration") or stream.get("duration") or 0)

    frame_proc = run([
        "ffprobe", "-v", "error", "-select_streams", "a:0",
        "-show_entries", "frame=pts_time,best_effort_timestamp_time,pkt_duration_time,nb_samples",
        "-of", "json", str(audio)
    ])
    frames = []
    if frame_proc.returncode == 0:
        frames = json.loads(frame_proc.stdout).get("frames", [])

    def frame_time(frame: dict) -> float | None:
        for key in ("pts_time", "best_effort_timestamp_time"):
            value = frame.get(key)
            if value not in (None, "N/A"):
                return float(value)
        return None

    times = [frame_time(f) for f in frames]
    times = [t for t in times if t is not None]
    first_pts = times[0] if times else None
    timestamp_jumps = []
    for left, right in zip(times, times[1:]):
        delta = right - left
        if delta > 0.25:
            timestamp_jumps.append({"from": round(left, 6), "to": round(right, 6), "gap": round(delta, 6)})

    decode_proc = run(["ffmpeg", "-hide_banner", "-i", str(audio), "-map", "0:a:0", "-f", "null", "-"])
    clocks = re.findall(r"time=(\d{2}:\d{2}:\d{2}(?:\.\d+)?)", decode_proc.stderr)
    decoded_duration = parse_clock(clocks[-1]) if clocks else 0.0

    report = {
        "path": str(audio.resolve()),
        "filename": audio.name,
        "extension": audio.suffix.lower(),
        "format_name": meta.get("format", {}).get("format_name"),
        "format_long_name": meta.get("format", {}).get("format_long_name"),
        "codec_name": stream.get("codec_name"),
        "codec_long_name": stream.get("codec_long_name"),
        "sample_rate": int(stream.get("sample_rate") or 0),
        "channels": stream.get("channels"),
        "container_duration": round(container_duration, 6),
        "decoded_duration": round(decoded_duration, 6),
        "duration_difference": round(container_duration - decoded_duration, 6),
        "first_audio_timestamp": round(first_pts, 6) if first_pts is not None else None,
        "timestamp_jumps": timestamp_jumps[:100],
        "warnings": [],
    }
    if audio.suffix.lower() == ".mp3" and stream.get("codec_name") != "mp3":
        report["warnings"].append("File extension is .mp3 but the actual audio codec is not MP3.")
    if container_duration - decoded_duration > 0.5:
        report["warnings"].append("Presentation duration is longer than decoded audio; inspect timestamp gaps or edit lists.")
    if first_pts is not None and first_pts > 0.25:
        report["warnings"].append("The first audio frame starts after time zero.")

    payload = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
