"""Addendum to run_decode_bench.py (synthetic test videos only), run after the main matrix finished:
(1) re-measure the rows that overlapped a ~15 s correctness check of the new 'skip' strategy during the main run
    (C2_1080p25: CPU seek at all rates, CPU keyonly, NVDEC seq at all rates);
(2) 'skip' strategy (forward jump by discarding packets, no seek / flush): single stream and aggregate, CPU and NVDEC;
(3) CPU and NVDEC together: 5 CPU processes x 4 threads plus 4 NVDEC sessions at the same time, seq R=1 and skip.
Output: out/throughput_decode_addendum.json."""
import concurrent.futures as cf, json, os, statistics, subprocess, sys, time
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "..", "out"); BIN, SYN = sys.argv[1], sys.argv[2]
V = json.load(open(os.path.join(OUT, "synthetic_videos.json")))["videos"]
RATES = (0.5, 1, 2, 4)
def run(f, dev, mode, rate, threads):
    r = subprocess.run([BIN, os.path.join(SYN, f + ".mp4"), dev, mode, str(rate), str(threads)], capture_output=True, text=True, check=True)
    d = json.loads(r.stdout); d["file"] = f; return d
def med(f, dev, mode, rate, reps):
    xs = [run(f, dev, mode, rate, 20) for _ in range(reps)]; w = statistics.median(x["wall_s"] for x in xs)
    d = dict(xs[0]); d.update(wall_s=w, x_realtime=round(d["video_s"] / w, 3), reps=[x["wall_s"] for x in xs]); return d
def group(jobs):
    t = time.monotonic()
    with cf.ThreadPoolExecutor(len(jobs)) as ex: res = list(ex.map(lambda j: run(*j), jobs))
    wall = time.monotonic() - t; vs = sum(x["video_s"] for x in res)
    return dict(video_s_total=vs, wall_s=round(wall, 3), x_realtime_aggregate=round(vs / wall, 3), per_stream_wall=[x["wall_s"] for x in res],
                decoded=[x["decoded"] for x in res][:1])
remeasured, single, agg = [], [], []
f = "C2_1080p25"
for rate in RATES: remeasured.append(med(f, "cpu", "seek", rate, 1)); print("remeasure", f, "cpu seek", rate, remeasured[-1]["x_realtime"], flush=True)
remeasured.append(run(f, "cpu", "keyonly", 1, 20)); print("remeasure keyonly", remeasured[-1]["x_realtime"], flush=True)
for rate in RATES: remeasured.append(med(f, "nvdec", "seq", rate, 3)); print("remeasure", f, "nvdec seq", rate, remeasured[-1]["x_realtime"], flush=True)
for f in V:
    for dev in ("cpu", "nvdec"):
        for rate in RATES:
            single.append(med(f, dev, "skip", rate, 3)); print(f, dev, "skip", rate, single[-1]["x_realtime"], single[-1]["decoded"], flush=True)
    for dev, P, thr in (("cpu", 5, 4), ("nvdec", 4, 1)):
        for rate in RATES:
            g = group([(f, dev, "skip", rate, thr)] * P); g.update(file=f, device=dev, streams=P, threads_per_stream=thr, mode="skip", rate=rate); agg.append(g)
            print(f, dev, "AGG skip", rate, g["x_realtime_aggregate"], flush=True)
    for mode, rates in (("seq", (1,)), ("skip", RATES)):
        for rate in rates:
            g = group([(f, "cpu", mode, rate, 4)] * 5 + [(f, "nvdec", mode, rate, 1)] * 4)
            g.update(file=f, device="cpu+nvdec", streams="5 cpu x 4 threads + 4 nvdec", mode=mode, rate=rate); agg.append(g)
            print(f, "cpu+nvdec AGG", mode, rate, g["x_realtime_aggregate"], flush=True)
json.dump(dict(note=__doc__, remeasured_rows=remeasured, single=single, aggregate=agg), open(os.path.join(OUT, "throughput_decode_addendum.json"), "w"), indent=1)
