#!/usr/bin/env python3
"""Extract an interval from a transcript, optionally rebasing it to zero."""
from __future__ import annotations
import argparse, json
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("transcript")
ap.add_argument("--start", type=float, required=True)
ap.add_argument("--end", type=float, required=True)
ap.add_argument("--rebase", action="store_true")
ap.add_argument("--output", required=True)
args = ap.parse_args()
if args.end <= args.start:
    ap.error("--end must be greater than --start")
doc = json.loads(Path(args.transcript).read_text(encoding="utf-8"))
segments = []
for seg in doc.get("segments", []):
    if float(seg["end"]) <= args.start or float(seg["start"]) >= args.end:
        continue
    seg = json.loads(json.dumps(seg, ensure_ascii=False))
    if args.rebase:
        seg["start"] = round(max(0.0, float(seg["start"]) - args.start), 3)
        seg["end"] = round(max(0.0, float(seg["end"]) - args.start), 3)
        for word in seg.get("words", []):
            word["start"] = round(max(0.0, float(word["start"]) - args.start), 3)
            word["end"] = round(max(0.0, float(word["end"]) - args.start), 3)
    segments.append(seg)
out = {k: v for k, v in doc.items() if k != "segments"}
out["segments"] = segments
out["duration"] = round((args.end - args.start) if args.rebase else args.end, 3)
Path(args.output).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {len(segments)} segments to {args.output}")
