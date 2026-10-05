"""Sequential read throughput of the DS203 full-video archive parts on LaCie (bytes only: dd with O_DIRECT to
/dev/null, so neither the page cache nor any decoder is involved; nothing is extracted or decoded).
Points: 2 GiB at the start, middle and end of each of the six parts, plus one 16 GiB sustained read."""
import json, os, re, subprocess, time
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "..", "out")
A = "/media/user/LaCie/medvideo_gate/DS203/archive/"
PARTS = [f"Appendix300_Full_Videos.z0{i}" for i in range(1, 6)] + ["Appendix300_Full_Videos.zip"]
BS = 64 * 2**20
def dd(path, skip_blocks, count):
    t = time.monotonic()
    r = subprocess.run(["dd", f"if={path}", "of=/dev/null", f"bs={BS}", f"skip={skip_blocks}", f"count={count}", "iflag=direct"], capture_output=True, text=True)
    wall = time.monotonic() - t; m = re.search(r"^(\d+) bytes", r.stderr, re.M); n = int(m.group(1)) if m else 0
    return dict(file=os.path.basename(path), offset_bytes=skip_blocks * BS, bytes=n, wall_s=round(wall, 3), MBps=round(n / wall / 1e6, 1), dd_tail=r.stderr.strip().splitlines()[-1])
rows = []
for p in PARTS:
    size = os.path.getsize(A + p); nblk = size // BS; cnt = 32  # 2 GiB
    for frac in (0.0, 0.5, 0.97):
        s = min(int(nblk * frac), max(nblk - cnt, 0)); r = dd(A + p, s, cnt); r["position"] = frac; rows.append(r); print(r)
sus = dd(A + "Appendix300_Full_Videos.z03", (268435456000 // BS) // 4, 256); sus["position"] = "sustained 16 GiB from 25% of z03"; print(sus)
pts = [r["MBps"] for r in rows]
res = dict(note=__doc__, device="LaCie d2 Professional, USB, rotational (lsblk ROTA=1, TRAN=usb)", points=rows, sustained=sus,
           MBps=dict(min=min(pts), median=sorted(pts)[len(pts) // 2], max=max(pts), sustained=sus["MBps"]))
json.dump(res, open(os.path.join(OUT, "lacie_read_throughput.json"), "w"), indent=1); print(res["MBps"])
