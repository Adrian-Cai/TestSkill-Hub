#!/usr/bin/env python3
"""Piecewise-linearly remap transcript and timeline timestamps from verified anchors."""
from __future__ import annotations

import argparse
import bisect
import json
import sys
from copy import deepcopy
from pathlib import Path


def load(path: str | None):
    if not path:
        return None
    return json.loads(Path(path).read_text(encoding="utf-8"))


def build_mapper(anchor_doc: dict):
    anchors = sorted(anchor_doc.get("anchors", []), key=lambda x: float(x["source"]))
    if len(anchors) < 2:
        raise ValueError("At least two anchors are required")
    xs = [float(a["source"]) for a in anchors]
    ys = [float(a["target"]) for a in anchors]
    if any(b <= a for a, b in zip(xs, xs[1:])):
        raise ValueError("Source anchors must be strictly increasing")
    if any(b <= a for a, b in zip(ys, ys[1:])):
        raise ValueError("Target anchors must be strictly increasing")

    def map_time(value: float) -> float:
        x = float(value)
        if x <= xs[0]:
            i = 0
        elif x >= xs[-1]:
            i = len(xs) - 2
        else:
            i = bisect.bisect_right(xs, x) - 1
        ratio = (x - xs[i]) / (xs[i + 1] - xs[i])
        return ys[i] + ratio * (ys[i + 1] - ys[i])

    return map_time, anchors


def retime_transcript(doc: dict, mapper) -> dict:
    out = deepcopy(doc)
    for seg in out.get("segments", []):
        seg["start"] = round(mapper(seg["start"]), 3)
        seg["end"] = round(mapper(seg["end"]), 3)
        for word in seg.get("words", []):
            word["start"] = round(mapper(word["start"]), 3)
            word["end"] = round(mapper(word["end"]), 3)
    if out.get("segments"):
        out["duration"] = round(out["segments"][-1]["end"], 3)
    return out


def retime_timeline(doc: dict, mapper) -> dict:
    out = deepcopy(doc)
    for scene in out.get("scenes", []):
        scene["start"] = round(mapper(scene["start"]), 3)
        scene["end"] = round(mapper(scene["end"]), 3)
        if "detailAt" in scene:
            scene["detailAt"] = round(mapper(scene["detailAt"]), 3)
        for cue in scene.get("cues", []):
            cue["at"] = round(mapper(cue["at"]), 3)
    if out.get("scenes"):
        out["duration"] = round(out["scenes"][-1]["end"], 3)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-transcript")
    ap.add_argument("--input-timeline")
    ap.add_argument("--anchors", required=True)
    ap.add_argument("--output-dir", required=True)
    args = ap.parse_args()
    if not args.input_transcript and not args.input_timeline:
        ap.error("Provide at least one input JSON")

    mapper, anchors = build_mapper(load(args.anchors))
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    report = {"anchors": anchors, "outputs": []}

    if args.input_transcript:
        result = retime_transcript(load(args.input_transcript), mapper)
        path = out_dir / "transcript.raw.json"
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        report["outputs"].append(str(path))
    if args.input_timeline:
        result = retime_timeline(load(args.input_timeline), mapper)
        path = out_dir / "timeline.json"
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        report["outputs"].append(str(path))

    (out_dir / "retime-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"retime_json: {exc}", file=sys.stderr)
        raise SystemExit(2)
