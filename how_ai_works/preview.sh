#!/bin/bash
# 用法: preview.sh video.mp4 out_prefix t1 t2 ...  -> 拼成一张联系表
v=$1; p=$2; shift 2
rm -f preview/${p}_*.png
for t in "$@"; do ffmpeg -v error -y -ss $t -i $v -frames:v 1 preview/${p}_$t.png; done
ffmpeg -v error -y $(for t in "$@"; do echo -n "-i preview/${p}_$t.png "; done) -filter_complex "$(n=$#; i=0; for t in "$@"; do echo -n "[$i:v]scale=640:-1[s$i];"; i=$((i+1)); done; i=0; for t in "$@"; do echo -n "[s$i]"; i=$((i+1)); done; echo -n "xstack=inputs=$#:layout=$(python3 -c "
n=$#;cols=2
print('|'.join(f'{(i%cols)*640}_{(i//cols)*360}' for i in range(n)))")")" preview/${p}_sheet.png
