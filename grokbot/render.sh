#!/usr/bin/env bash
# 完整流程：配音 → 混音 → 字幕 → 渲染帧 → 编码两个版本
# 需要：python3 + kokoro-onnx、node + playwright（系统自带 chromium）、ffmpeg(libass)、/opt/fonts 下的 Noto Sans CJK SC
set -euo pipefail
cd "$(dirname "$0")"
ROOT=$(cd .. && pwd)
WORKERS=${WORKERS:-4}
[ "${SKIP_TTS:-0}" = 1 ] || python3 tts.py
python3 make_audio.py
python3 make_subs.py
export PORT=${PORT:-8124}
if ! curl -s -o /dev/null "http://localhost:$PORT/grokbot/scene/index.html"; then
  (cd "$ROOT" && python3 -m http.server "$PORT" --bind 127.0.0.1 >/dev/null 2>&1 &)
  sleep 1
fi
FRAMES=$(python3 -c "import json;print(round(json.load(open('build/timings.json'))['duration']*30))")
rm -rf build/frames && mkdir -p build/frames
CH=$(( (FRAMES + WORKERS - 1) / WORKERS ))
for i in $(seq 0 $((WORKERS - 1))); do
  node capture.mjs build/frames $((i * CH)) $(( (i + 1) * CH )) > build/render-$i.log 2>&1 &
done
wait
N=$(ls build/frames | wc -l); echo "frames: $N / $FRAMES"; [ "$N" = "$FRAMES" ]
mkdir -p "$ROOT/out"
enc() { # $1 字幕文件  $2 输出
  ffmpeg -y -hide_banner -loglevel error -framerate 30 -i build/frames/f%04d.png -i build/mix.wav \
    -vf "ass=build/$1:fontsdir=/opt/fonts,format=yuv420p" \
    -c:v libx264 -preset slow -crf 18 -profile:v high -r 30 -g 60 \
    -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart "$ROOT/out/$2"
  echo "wrote out/$2"
}
enc subs-en.ass grokbot-x.mp4
enc subs-bi.ass grokbot-douyin.mp4
