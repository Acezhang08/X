# -*- coding: utf-8 -*-
"""Voice-only master: two-pass loudnorm to -14 LUFS, true peak <= -1 dBTP, 48 kHz. No music."""
import subprocess, json, re
def run(cmd): return subprocess.run(cmd, capture_output=True, text=True)
TARGET = "I=-14:TP=-1.5:LRA=11"
# voice is peaky (crest ~20 dB): a gentle compressor + limiter first, otherwise the -1 dBTP ceiling caps loudness near -15.3 LUFS
PRE = "highpass=f=70,acompressor=threshold=-30dB:ratio=5:attack=5:release=80:makeup=8dB,alimiter=limit=0.7:attack=2:release=30:level=disabled"
run(["ffmpeg", "-y", "-i", "build/voice.wav", "-af", PRE, "build/voice_c.wav"])
r = run(["ffmpeg", "-y", "-i", "build/voice_c.wav", "-af", f"loudnorm={TARGET}:print_format=json", "-f", "null", "-"])
j = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S).group(0)); print(j)
ln = f"loudnorm={TARGET}:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true"
r = run(["ffmpeg", "-y", "-i", "build/voice_c.wav", "-af", ln, "-ar", "48000", "build/final_audio.wav"])
r = run(["ffmpeg", "-i", "build/final_audio.wav", "-af", "ebur128=peak=true", "-f", "null", "-"])
print("LUFS", re.findall(r"I:\s+(-?\d+\.\d) LUFS", r.stderr)[-1:], "TP", re.findall(r"Peak:\s+(-?\d+\.\d) dBFS", r.stderr)[-1:])
