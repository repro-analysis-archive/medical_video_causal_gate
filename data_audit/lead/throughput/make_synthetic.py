"""Generate synthetic H.264 test videos matching each DS203 centre format (codec, resolution, frame rate, median
bitrate, median keyframe interval from out/DS203_codec_facts.json). Source = ffmpeg testsrc2 + temporal noise only:
no DS203 byte or frame is used. Files go to the session scratchpad (not committed); commands, sha256 and ffprobe facts
are recorded in out/synthetic_videos.json."""
import hashlib, json, os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "..", "out"); SYN = sys.argv[1]
DUR = 60
# name: (centre format it stands for, width, height, fps, Mbps (median of that format), GOP frames (median of that format))
F = {"C1_1080p30": ("Center 1, 1920x1080 ~30 fps", 1920, 1080, 30, 6.2, 135),
     "C2_1080p25": ("Center 2, 1920x1080 25 fps (74/82 files)", 1920, 1080, 25, 16.0, 60),
     "C2_2160p25": ("Center 2, 3840x2160 25 fps (8/82 files)", 3840, 2160, 25, 73.1, 30),
     "C3_2160p25": ("Center 3, 3840x2160 25 fps (41/42 files)", 3840, 2160, 25, 75.0, 36),
     "C4_1080p50": ("Center 4, 1920x1080 50 fps", 1920, 1080, 50, 7.8, 96),
     "C5_1080p50": ("Center 5, 1920x1080 50 fps", 1920, 1080, 50, 8.5, 214)}
rec = {}
for name, (desc, w, h, fps, mbps, gop) in F.items():
    path = os.path.join(SYN, name + ".mp4"); b = f"{mbps}M"
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", f"testsrc2=size={w}x{h}:rate={fps}:duration={DUR}",
           "-vf", "noise=alls=14:allf=t+u", "-c:v", "libx264", "-preset", "veryfast", "-profile:v", "high", "-pix_fmt", "yuv420p",
           "-b:v", b, "-maxrate", f"{mbps * 1.5:.1f}M", "-bufsize", f"{mbps * 2:.1f}M", "-g", str(gop), "-keyint_min", str(gop), "-sc_threshold", "0",
           "-bf", "3", "-refs", "5", "-movflags", "+faststart", path]
    if not os.path.exists(path): subprocess.run(cmd, check=True)
    pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                    "stream=codec_name,profile,level,width,height,r_frame_rate,pix_fmt,has_b_frames,refs,bit_rate,nb_frames",
                                    "-of", "json", path], capture_output=True, text=True, check=True).stdout)["streams"][0]
    kf = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "packet=flags", "-of", "csv=p=0", path],
                        capture_output=True, text=True, check=True).stdout.split()
    n_key = sum("K" in x for x in kf)
    rec[name] = dict(stands_for=desc, target=dict(width=w, height=h, fps=fps, mbps=mbps, gop_frames=gop), command=" ".join(cmd),
                     bytes=os.path.getsize(path), sha256=hashlib.sha256(open(path, "rb").read()).hexdigest(),
                     achieved_mbps=round(os.path.getsize(path) * 8 / DUR / 1e6, 2), packets=len(kf), keyframes=n_key,
                     achieved_gop_frames=round(len(kf) / n_key, 1), ffprobe=pr)
    print(name, rec[name]["achieved_mbps"], "Mbps (target", mbps, ") gop", rec[name]["achieved_gop_frames"], pr["profile"], pr["level"], "B", pr["has_b_frames"])
json.dump(dict(note=__doc__, duration_s=DUR, videos=rec), open(os.path.join(OUT, "synthetic_videos.json"), "w"), indent=1)
