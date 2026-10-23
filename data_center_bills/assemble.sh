#!/bin/bash
# concat the rendered chunks, mux the voice-only master (AAC 192k), faststart
set -e
cd "$(dirname "$0")"
ls build/chunks/en_*.mp4 | sort | sed "s|^|file '$PWD/|; s|$|'|" > build/list_en.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i build/list_en.txt -i build/final_audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart data_center_bills_hq.mp4
ls -la data_center_bills_hq.mp4
