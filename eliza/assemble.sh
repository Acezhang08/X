#!/bin/bash
set -e
cd "$(dirname "$0")"
ls build/chunks/v_*.mp4 | sort | sed "s|^|file '$PWD/|; s|$|'|" > build/list_v.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i build/list_v.txt -i build/final_audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart eliza_history_of_ai.mp4
ls -la eliza_history_of_ai.mp4
