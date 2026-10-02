"""Rough embedding-compute estimates per hour of video for the eligible FM candidates (no model run, no video touched).
FLOPs/input: documented where available; transformers 2*P*T; standard CNN backbones: standard GFLOPs (2 x GMACs);
conv video VAEs: c * P * input voxels with c calibrated from VidTok's documented 10.35 TFLOPs for 157M params at
17x256x256 (order-of-magnitude only). Inputs/hour: documented sampling; where only a frame stride is documented, a
25 fps native source is assumed. Sustained throughput = 30% of dense BF16 peak derived from NVIDIA's quoted peaks:
RTX 4500 Ada 634 TFLOPS FP8 (sparse) -> 158.5 dense BF16; RTX PRO 6000 Blackwell WS 4000 TOPS FP4 (sparse) -> 500 dense BF16."""
import csv, json, os
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "out")
GPU = {"RTX 4500 Ada (24 GB)": (0.30 * 158.5e12, 24e9), "RTX PRO 6000 Blackwell WS (96 GB)": (0.30 * 500e12, 96e9)}
C_VAE = 10.35e12 / (157e6 * 17 * 256 * 256)
VOX = lambda t, h, w: t * h * w
M = [  # name, arm, params, flops_per_input, flops_basis, inputs_per_hour, sampling_basis, weights_bytes_bf16
 ("Endo-FM (ViT-B video, 121M)", "primary", 121e6, 2 * 121e6 * 16 * 196, "2PT, 16x196 tokens", 3600 / (16 / 30), "consecutive 16-frame clips at 30 fps"),
 ("EndoViT (ViT-B/16, 85.8M)", "primary", 85.8e6, 2 * 85.8e6 * 197, "2PT, 197 tokens", 3600, "1 fps frames"),
 ("SurgeNetXL CAFormer-S18 (24.3M)", "primary", 24.3e6, 8.2e9, "std CAFormer-S18 ~4.1 GMACs", 3600, "1 fps frames"),
 ("SurgeNetXL DINO ViT-L/14 (~304M)", "primary", 304e6, 2 * 304e6 * 257, "2PT, 257 tokens (224, patch 14)", 3600, "1 fps frames"),
 ("SurgeNet / Public variants (CAFormer-S18)", "primary", 24.3e6, 8.2e9, "std CAFormer-S18", 3600, "1 fps frames"),
 ("SurgVLP / HecVL / PeskaVLP (ResNet-50 visual)", "primary", 25.6e6, 8.2e9, "std ResNet-50 ~4.1 GMACs", 3600, "1 fps frames (uniform in clip)"),
 ("EndoMamba (24.46M)", "primary", 24.46e6, 2 * 24.46e6 * 16 * 196, "2PT, 16x196 tokens", 3600 / (64 / 25), "16 frames, every 4th, 25 fps source"),
 ("LemonFM (ConvNeXt-L, ~198M std)", "primary", 198e6, 68.8e9, "std ConvNeXt-L ~34.4 GMACs", 3600, "1 fps frames"),
 ("EndoSSL ViT-L (~304M std)", "primary", 304e6, 2 * 304e6 * 197, "2PT, 197 tokens", 3600, "1 fps frames"),
 ("SelfSupSurg (ResNet-50)", "primary", 25.6e6, 8.2e9, "std ResNet-50", 18000, "5 fps frames"),
 ("SurgLIME (ViT-B/16 visual)", "primary", 86e6, 2 * 86e6 * 197, "2PT per frame", 3600, "1 fps frames (assumed)"),
 ("PL-Stitch (ViT-B/16)", "primary", 86e6, 2 * 86e6 * 197, "2PT per frame", 3600, "1 fps frames (assumed)"),
 ("Basel V-JEPA ViT-L (~304M std)", "primary", 304e6, 2 * 304e6 * 1568, "2PT, 8x196 tubelet tokens", 3600, "16-frame clip per 1 s"),
 ("Cosmos-H-Surgical v0.3.1 (~15.2B DiT)", "primary", 15.2e9, 2 * 15.2e9 * 24 * 15 * 26, "2PT, latent 24x30x52 / patch 2x2", 3600 / (93 / 16), "93 frames at 16 fps"),
 ("Cosmos-H-Surgical Predict/Transfer 2.5 (2B)", "primary", 2e9, 2 * 2e9 * 24 * 44 * 80, "2PT, latent 24x88x160 / patch 2x2", 3600 / (93 / 16), "93 frames at 16 fps, 1280x704"),
 ("Cosmos-H-Surgical-Simulator (~2B)", "primary", 2e9, 2 * 2e9 * 4 * 18 * 32, "2PT, 512x288, 13 frames", 3600 / 1.3, "13 frames at 10 Hz (assumed)"),
 ("Cosmos-H-Dreams (~2B)", "primary", 2e9, 2 * 2e9 * 3 * 18 * 32, "2PT, 288x512, 12-frame block", 3600 / 1.2, "12 frames at 10 Hz"),
 ("MedSora-B (86.47M)", "primary", 86.47e6, 2 * 86.47e6 * 16 * 8 * 8, "2PT, latent 16x16x16 / patch 2", 3600 / (16 / 25), "16 frames at 25 fps (fps n/s)"),
 ("SG2VID (U-Net ~1.24B, inferred from fp32 file size)", "primary", 1.24e9, 2 * 1.24e9 * 16 * 16 * 16, "2P x latent positions", 3600 / 4, "16 frames at 4 fps"),
 ("KVLR (~12.06B)", "primary", 12.06e9, 2 * 12.06e9 * 5 * 18 * 32, "2PT, 288x512, 17 frames", 3600 / (17 / 30), "17 frames at 30 fps"),
 ("Open-Sora VAE v1.2 (384M whole)", "secondary", 384e6, C_VAE * 384e6 * VOX(17, 256, 256), "calibrated conv-VAE (whole AE)", 3600 / (17 / 24), "17 frames at 24 fps"),
 ("VideoMAE-B (87M)", "secondary", 87e6, 180e9, "documented 180 GFLOPs/view", 3600 / (64 / 25), "16 frames stride 4, 25 fps source"),
 ("VideoMAE-L (305M)", "secondary", 305e6, 597e9, "documented 597 GFLOPs/view", 3600 / (64 / 25), "16 frames stride 4"),
 ("VideoMAE-H (633M)", "secondary", 633e6, 1192e9, "documented 1192 GFLOPs/view", 3600 / (64 / 25), "16 frames stride 4"),
 ("VideoMAE V2-g (1011M)", "secondary", 1011e6, 2.54e12, "documented ~2.54 TFLOPs/view", 3600 / (64 / 25), "16 frames stride 4"),
 ("OmniTokenizer", "secondary", None, 262e9, "documented 262 GFLOPs/video", 3600 / (17 / 25), "17 frames at 25 fps"),
 ("Open-Sora-Plan v1.2 VAE (enc 94M)", "secondary", 94e6, C_VAE * 94e6 * VOX(25, 256, 256), "calibrated conv-VAE (encoder)", 3600 / (25 / 25), "25 frames at 25 fps"),
 ("WF-VAE-L 16ch (enc 84M)", "secondary", 84e6, C_VAE * 84e6 * VOX(33, 256, 256), "calibrated conv-VAE (encoder)", 3600 / (33 / 25), "33 frames at 25 fps"),
 ("CV-VAE (enc 68M)", "secondary", 68e6, C_VAE * 68e6 * VOX(17, 256, 256), "calibrated conv-VAE (encoder)", 3600 / (17 / 25), "17 frames at 25 fps"),
 ("LARP-L (173M)", "secondary", 173e6, 2 * 173e6 * 1024, "2PT, 1024 tokens", 3600 / (16 / 25), "16 frames at 25 fps, 128x128"),
 ("LeanVAE (39.8M)", "secondary", 39.8e6, 0.203e12, "documented 0.203 TFLOPs (input size not given)", 3600 / (17 / 25), "17 frames at 25 fps"),
 ("Reducio-VAE (437M whole)", "secondary", 437e6, C_VAE * 437e6 * VOX(16, 256, 256), "calibrated conv-VAE (whole AE)", 3600 / (16 / 16), "16 frames at 16 fps"),
 ("Open-MAGVIT2 video", "secondary", None, None, "params not documented: not estimable", None, "17 frames at native rate"),
]
HOURS = 145.6
rows = []
for name, arm, P, F, fb, iph, sb in M:
    r = dict(model=name, arm=arm, params=P, flops_per_input=F, flops_basis=fb, inputs_per_video_hour=round(iph) if iph else None, sampling=sb)
    for g, (thr, mem) in GPU.items():
        if F and iph:
            gh = F * iph / thr / 3600; r[f"{g}: GPU-h per video-h"] = round(gh, 4); r[f"{g}: GPU-h for DS203 145.6 h"] = round(gh * HOURS, 2)
        r[f"{g}: bf16 weights fit"] = ("yes" if P * 2 < 0.6 * mem else "NO (needs offload / quantisation)") if P else "n/s"
    rows.append(r)
with open(os.path.join(OUT, "fm_compute_estimate.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); [w.writerow(x) for x in rows]
json.dump(dict(assumptions=__doc__, c_vae=C_VAE, gpus={k: dict(sustained_flops=v[0], memory_bytes=v[1]) for k, v in GPU.items()}, rows=rows), open(os.path.join(OUT, "fm_compute_estimate.json"), "w"), indent=1)
for r in rows: print(f"{r['model'][:46]:46s} {str(r.get('RTX 4500 Ada (24 GB): GPU-h for DS203 145.6 h')):>8s} {str(r.get('RTX PRO 6000 Blackwell WS (96 GB): GPU-h for DS203 145.6 h')):>8s} {r['RTX 4500 Ada (24 GB): bf16 weights fit']}")
