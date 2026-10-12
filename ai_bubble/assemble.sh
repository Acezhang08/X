#!/bin/bash
set -e
cd "$(dirname "$0")"
for tag in en bi; do
  ls build/chunks/${tag}_*.mp4 | sort | sed "s|^|file '$PWD/|; s|$|'|" > build/list_${tag}.txt
done
ffmpeg -y -loglevel error -f concat -safe 0 -i build/list_en.txt -i build/final_audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart youtube_ai_bubble.mp4
ffmpeg -y -loglevel error -f concat -safe 0 -i build/list_bi.txt -i build/final_audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart douyin_ai_bubble.mp4
ls -la *.mp4
