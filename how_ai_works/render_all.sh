#!/bin/bash
# 1080p30 并行渲染 8 个分段
cd "$(dirname "$0")"
mkdir -p build/final
render() { s=$1; manim -r 1920,1080 --fps 30 --disable_caching scenes/seg$s.py Seg$s --media_dir build/media_hd > build/final/log_$s.txt 2>&1 && echo "seg$s done $(date +%T)"; }
export -f render
printf "%s\n" 5 3 2 4 6 7 0 1 | xargs -P4 -I{} bash -c 'render {}'
