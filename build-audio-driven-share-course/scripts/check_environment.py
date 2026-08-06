#!/usr/bin/env python3
"""Report required and optional tools for this Skill."""
from __future__ import annotations
import importlib.util, json, shutil, sys

required = {"python": sys.executable, "ffmpeg": shutil.which("ffmpeg"), "ffprobe": shutil.which("ffprobe")}
optional_modules = {name: bool(importlib.util.find_spec(name)) for name in ("faster_whisper", "whisper", "torch", "transformers")}
report = {
    "required": required,
    "optional_asr_modules": optional_modules,
    "ready_for_audio_inspection": bool(required["ffmpeg"] and required["ffprobe"]),
    "ready_for_local_asr": bool(optional_modules["faster_whisper"] or optional_modules["whisper"]),
}
print(json.dumps(report, ensure_ascii=False, indent=2))
raise SystemExit(0 if report["ready_for_audio_inspection"] else 1)
