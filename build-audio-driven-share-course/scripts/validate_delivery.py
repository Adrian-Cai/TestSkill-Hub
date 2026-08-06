#!/usr/bin/env python3
"""Validate an audio-driven course project before delivery."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    args = ap.parse_args()
    root = Path(args.project)
    errors: list[str] = []
    warnings: list[str] = []

    html_path = root / "standalone-preview.html"
    timeline_candidates = [root / "timeline.json"] + sorted(root.glob("timeline(*).json"))
    transcript_candidates = [root / "transcript.raw.json"] + sorted(root.glob("transcript.raw(*).json"))
    timeline_path = next((p for p in timeline_candidates if p.is_file()), None)
    transcript_path = next((p for p in transcript_candidates if p.is_file()), None)

    for name in ("START_WINDOWS.bat", "START_MAC_LINUX.sh", "README.md"):
        if not (root / name).is_file():
            errors.append(f"Missing {name}")
    if not html_path.is_file():
        errors.append("Missing standalone-preview.html")
    if timeline_path is None:
        errors.append("Missing timeline JSON")
    if transcript_path is None:
        errors.append("Missing transcript JSON")

    timeline = None
    if timeline_path:
        try:
            timeline = json.loads(timeline_path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"Invalid timeline JSON: {exc}")
    if transcript_path:
        try:
            json.loads(transcript_path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"Invalid transcript JSON: {exc}")

    if timeline:
        obsolete_root_fields = [name for name in ("title",) if name in timeline]
        if obsolete_root_fields:
            errors.append("Obsolete timeline fields must be removed: " + ", ".join(obsolete_root_fields))
        duration = float(timeline.get("duration", 0))
        if duration <= 0:
            errors.append("Timeline duration must be positive")
        previous_end = -1.0
        ids = set()
        for scene in timeline.get("scenes", []):
            sid = str(scene.get("id", ""))
            obsolete_scene_fields = [name for name in ("title", "eyebrow", "summary") if name in scene]
            if obsolete_scene_fields:
                errors.append(
                    f"Scene {sid} contains obsolete display fields: " + ", ".join(obsolete_scene_fields)
                )
            if sid in ids:
                errors.append(f"Duplicate scene id: {sid}")
            ids.add(sid)
            start, end = float(scene.get("start", -1)), float(scene.get("end", -1))
            if start < previous_end - 0.001:
                errors.append(f"Scene {sid} overlaps previous scene")
            if end <= start:
                errors.append(f"Scene {sid} has invalid interval")
            if end > duration + 0.01:
                errors.append(f"Scene {sid} ends after timeline duration")
            for cue in scene.get("cues", []):
                at = float(cue.get("at", -1))
                if at < start - 0.001 or at > end + 0.001:
                    errors.append(f"Cue {cue.get('target')} is outside scene {sid}")
            previous_end = end

    if html_path.is_file():
        html = html_path.read_text(encoding="utf-8", errors="replace")
        for token in ("record", "autoplay", "delay", "guide"):
            if token not in html:
                errors.append(f"HTML does not support parameter: {token}")
        if "1920" not in html or "1080" not in html:
            errors.append("HTML does not declare a 1920×1080 canvas")
        if "data:audio/" not in html:
            errors.append("Audio is not embedded as a data URI")
        if 'data-recording-content-only="true"' not in html:
            warnings.append("Recording stage is not marked content-only; verify that preview chrome is outside the 1920x1080 stage")
        if "scene?.title" in html or "TIMELINE.title" in html:
            errors.append("HTML still falls back to a timeline or scene title when no cue is active")
        chrome_classes = ("progress", "header", "chapter-rail", "chapter-indicator", "cue-note", "clockTop")
        found_chrome = [name for name in chrome_classes if re.search(rf'class=["\'][^"\']*\b{re.escape(name)}\b', html)]
        if found_chrome:
            warnings.append(
                "Possible recording chrome found; remove unless explicitly requested: "
                + ", ".join(found_chrome)
            )
        external = re.findall(r'(?:src|href)=["\'](https?://[^"\']+)', html)
        if external:
            warnings.append(f"External dependencies found: {external[:5]}")
        if "catch(err)" not in html and "audio.addEventListener('error'" not in html:
            warnings.append("No visible playback error handling detected")

    result = {"project": str(root.resolve()), "errors": errors, "warnings": warnings, "valid": not errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
