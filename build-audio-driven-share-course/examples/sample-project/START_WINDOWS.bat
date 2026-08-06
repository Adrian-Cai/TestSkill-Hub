@echo off
cd /d %~dp0
echo Preview: http://127.0.0.1:8000/standalone-preview.html
echo OBS: http://127.0.0.1:8000/standalone-preview.html?record=1^&autoplay=1^&delay=3
start http://127.0.0.1:8000/standalone-preview.html
python -m http.server 8000
