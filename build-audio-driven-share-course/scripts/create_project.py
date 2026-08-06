#!/usr/bin/env python3
"""Create a self-contained OBS-ready HTML project with embedded audio."""
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import shutil
from pathlib import Path


def audio_mime(path: Path) -> str:
    suffix = path.suffix.lower()
    return {
        ".m4a": "audio/mp4", ".mp4": "audio/mp4", ".aac": "audio/aac",
        ".mp3": "audio/mpeg", ".wav": "audio/wav", ".ogg": "audio/ogg",
    }.get(suffix, mimetypes.guess_type(path.name)[0] or "audio/mp4")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", required=True)
    ap.add_argument("--timeline", required=True)
    ap.add_argument("--transcript", required=True)
    ap.add_argument("--project-name", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    script_dir = Path(__file__).resolve().parent
    root = script_dir.parent
    template = (root / "templates" / "standalone-preview.template.html").read_text(encoding="utf-8")
    audio = Path(args.audio)
    timeline_path = Path(args.timeline)
    transcript_path = Path(args.transcript)
    for path in (audio, timeline_path, transcript_path):
        if not path.is_file():
            raise FileNotFoundError(path)

    timeline = json.loads(timeline_path.read_text(encoding="utf-8"))
    transcript = json.loads(transcript_path.read_text(encoding="utf-8"))
    encoded = base64.b64encode(audio.read_bytes()).decode("ascii")
    data_uri = f"data:{audio_mime(audio)};base64,{encoded}"
    html = template.replace("__PROJECT_NAME__", args.project_name)
    html = html.replace("__AUDIO_DATA_URI__", data_uri)
    html = html.replace("__TIMELINE_JSON__", json.dumps(timeline, ensure_ascii=False, separators=(",", ":")))

    out = Path(args.output)
    if out.exists():
        shutil.rmtree(out)
    (out / "audio").mkdir(parents=True)
    (out / "standalone-preview.html").write_text(html, encoding="utf-8")
    shutil.copy2(audio, out / "audio" / audio.name)
    (out / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "transcript.raw.json").write_text(json.dumps(transcript, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "START_WINDOWS.bat").write_text(
        '@echo off\ncd /d %~dp0\necho Preview: http://127.0.0.1:8000/standalone-preview.html\necho OBS: http://127.0.0.1:8000/standalone-preview.html?record=1^&autoplay=1^&delay=3\nstart http://127.0.0.1:8000/standalone-preview.html\npython -m http.server 8000\n',
        encoding="utf-8"
    )
    (out / "START_MAC_LINUX.sh").write_text(
        '#!/usr/bin/env bash\nset -e\ncd "$(dirname "$0")"\necho "Preview: http://127.0.0.1:8000/standalone-preview.html"\npython3 -m http.server 8000\n',
        encoding="utf-8"
    )
    (out / "START_MAC_LINUX.sh").chmod(0o755)
    (out / "README.md").write_text(f"""# {args.project_name}

## 启动

Windows 双击 `START_WINDOWS.bat`，或运行：

```bash
python -m http.server 8000
```

普通预览：

```text
http://127.0.0.1:8000/standalone-preview.html
```

OBS：

```text
http://127.0.0.1:8000/standalone-preview.html?record=1&autoplay=1&delay=3
```

OBS 浏览器来源尺寸：1920×1080。
""", encoding="utf-8")
    print(out.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
