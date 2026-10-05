"""Decode-throughput matrix on the synthetic test videos only (make_synthetic.py): device {cpu, nvdec} x strategy
{seq, seek, hybrid} x grid rate {0.5, 1, 2, 4} fps, plus keyframe-only decode; single stream (CPU 20 threads,
NVDEC 1 session; seq/hybrid 3 repetitions, seek/keyonly 1), then aggregate throughput with parallel streams
(CPU 5 processes x 4 threads; NVDEC 4 sessions) for seq and hybrid. Output: out/throughput_decode.json."""
import concurrent.futures as cf, json, os, statistics, subprocess, sys, time
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "..", "out"); BIN, SYN = sys.argv[1], sys.argv[2]
V = json.load(open(os.path.join(OUT, "synthetic_videos.json")))["videos"]
RATES = (0.5, 1, 2, 4)
def run(f, dev, mode, rate, threads):
    r = subprocess.run([BIN, os.path.join(SYN, f + ".mp4"), dev, mode, str(rate), str(threads)], capture_output=True, text=True, check=True)
    d = json.loads(r.stdout); d["file"] = f; return d
single, agg = [], []
t0 = time.time()
for f in V:
    for dev in ("cpu", "nvdec"):
        for mode in ("seq", "hybrid", "seek"):
            for rate in RATES:
                reps = [run(f, dev, mode, rate, 20) for _ in range(3 if mode != "seek" else 1)]
                w = statistics.median(x["wall_s"] for x in reps); d = dict(reps[0]); d.update(wall_s=w, x_realtime=round(d["video_s"] / w, 3), reps=[x["wall_s"] for x in reps])
                single.append(d); print(f, dev, mode, rate, d["x_realtime"], d["decoded"], d["seeks"], flush=True)
        d = run(f, dev, "keyonly", 1, 20); single.append(d); print(f, dev, "keyonly", d["x_realtime"], flush=True)
    for dev, P, thr in (("cpu", 5, 4), ("nvdec", 4, 1)):
        for mode, rates in (("seq", (1,)), ("hybrid", RATES)):
            for rate in rates:
                t = time.monotonic()
                with cf.ThreadPoolExecutor(P) as ex: res = list(ex.map(lambda _: run(f, dev, mode, rate, thr), range(P)))
                wall = time.monotonic() - t; vs = sum(x["video_s"] for x in res)
                agg.append(dict(file=f, device=dev, streams=P, threads_per_stream=thr, mode=mode, rate=rate, video_s_total=vs, wall_s=round(wall, 3),
                                x_realtime_aggregate=round(vs / wall, 3), per_stream_wall=[x["wall_s"] for x in res], decoded=res[0]["decoded"]))
                print(f, dev, "AGG", P, mode, rate, agg[-1]["x_realtime_aggregate"], flush=True)
json.dump(dict(note=__doc__, binary_source="throughput/decode_bench.c", gpu="NVIDIA RTX 4500 Ada (driver 555.52.04)", cpu_threads=os.cpu_count(),
               ffmpeg_libs="libavformat 58.76.100 / libavcodec 58.134.100 (Ubuntu ffmpeg 4.4.2)", elapsed_s=round(time.time() - t0, 1),
               single=single, aggregate=agg), open(os.path.join(OUT, "throughput_decode.json"), "w"), indent=1)
