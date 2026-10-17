#!/bin/bash
# chunks (crf 17 master pieces) -> concat -> re-encode crf 23 (upload copy, < 100 MB for GitHub) + voice track
set -e
cd "$(dirname "$0")"
ls build/chunks/v_*.mp4 | sort | sed "s|^|file '$PWD/|; s|$|'|" > build/list_v.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i build/list_v.txt -c copy build/master_video.mp4
ffmpeg -y -loglevel error -i build/master_video.mp4 -i build/final_audio.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart humanoid_robots.mp4
ls -la humanoid_robots.mp4
