# -*- coding: utf-8 -*-
import sys, os, subprocess, time, skia
from multiprocessing import Pool
import render, subs
from lib import *
FPS = 30

def work(args):
    k, f0, f1 = args
    T = render.load_scenes(); cues = subs.build_cues(T)
    surf = skia.Surface(W, H); sa = skia.Surface(W, H)
    fn = f"build/chunks/v_{k:03d}.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", fn], stdin=subprocess.PIPE)
    for f in range(f0, f1):
        t = f / FPS
        render.draw_frame(surf.getCanvas(), t, T)
        img = surf.makeImageSnapshot()
        cv = sa.getCanvas(); cv.drawImage(img, 0, 0); subs.draw_subs(cv, subs.cue_at(cues, t))
        p.stdin.write(sa.makeImageSnapshot().toarray(colorType=skia.kBGRA_8888_ColorType).tobytes())
    p.stdin.close(); p.wait()
    return k

if __name__ == "__main__":
    T = render.load_scenes()
    total = int(T.duration * FPS); chunk = 450
    jobs = [(i, s, min(total, s + chunk)) for i, s in enumerate(range(0, total, chunk))]
    os.makedirs("build/chunks", exist_ok=True)
    if os.environ.get("ONLY"): jobs = [j for j in jobs if j[0] in {int(x) for x in os.environ["ONLY"].split(",")}]
    t0 = time.time()
    with Pool(int(os.environ.get("NPROC", 4))) as pool:
        for k in pool.imap_unordered(work, jobs): print("done", k, round(time.time() - t0), flush=True)
