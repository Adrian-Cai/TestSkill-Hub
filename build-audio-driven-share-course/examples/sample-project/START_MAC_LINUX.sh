#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
echo "Preview: http://127.0.0.1:8000/standalone-preview.html"
python3 -m http.server 8000
