# -*- coding: utf-8 -*-
import sys, os, subprocess, time, numpy as np, skia
from multiprocessing import Pool
import render, subs
from lib import *
FPS = 30

def work(args):
    k, f0, f1 = args
    T = render.load_scenes(); cues = subs.build_cues(T)
    surf = skia.Surface(W, H); sa = skia.Surface(W, H); sb = skia.Surface(W, H)
    outs = []
    procs = []
    for tag in ("en",):
        fn = f"build/chunks/{tag}_{k:03d}.mp4"
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", fn], stdin=subprocess.PIPE)
        procs.append(p)
    for f in range(f0, f1):
        t = f / FPS
        render.draw_frame(surf.getCanvas(), t, T)
        img = surf.makeImageSnapshot()
        cue = subs.cue_at(cues, t)
        for s_, bil, p in ((sa, False, procs[0]),):
            cv = s_.getCanvas(); cv.drawImage(img, 0, 0); subs.draw_subs(cv, cue, bil)
            p.stdin.write(s_.makeImageSnapshot().toarray(colorType=skia.kBGRA_8888_ColorType).tobytes())
    for p in procs: p.stdin.close(); p.wait()
    return k

if __name__ == "__main__":
    T = render.load_scenes()
    total = int(T.duration * FPS)
    chunk = 450
    jobs = [(i, s, min(total, s + chunk)) for i, s in enumerate(range(0, total, chunk))]
    os.makedirs("build/chunks", exist_ok=True)
    if os.environ.get("ONLY"): jobs = [j for j in jobs if j[0] in {int(x) for x in os.environ["ONLY"].split(",")}]
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        jobs = [(900, 3000, 3030)]
    t0 = time.time()
    with Pool(int(os.environ.get("NPROC", 4))) as pool:
        for k in pool.imap_unordered(work, jobs): print("done", k, round(time.time() - t0), flush=True)
