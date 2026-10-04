"""Decision 005: build the named-reference entry (Cosmos tokenizer of K4) with quotes verified against saved copies."""
import json, re, os
H = os.path.dirname(os.path.abspath(__file__)); R = "fm_sources/reference/"; S = "fm_sources/secondary/"; K4 = "../../lit/fulltext/2607.06126.txt"
norm = lambda s: re.sub(r"\s+", " ", s).strip()
def Q(quote, path):
    txt = open(os.path.join(H, path), errors="replace").read(); return dict(quote=quote, copy=path, verified=norm(quote) in norm(txt))
e = dict(
 name="NVIDIA Cosmos tokenizer used by Nakamura, Breuer, Crespin, Dietrich & Imai (2026), arXiv:2607.06126 (K4); named reference representation (Decision 005)",
 version=dict(value="nvidia/Cosmos-1.0-Tokenizer-CV8x8x8 (Cosmos Tokenizer v1.0 continuous video tokenizer; HF repo sha 5110dbb3c94a9eb6648eabbbccc19c76180fe426)",
   basis="K4 names only 'the NVIDIA Cosmos tokenizer (Agarwal et al., 2025)'. The checkpoint is the default of the authors' package gpi_pack (MIT, Copyright 2025 Kentaro Nakamura; repo commit 8836037), whose video module says it implements 'the representation used by the video paper', and whose documentation links 'NVIDIA Cosmos Tokenizer' to this checkpoint. The package also states the paper does not specify resize or frame-sampling policy. Exact version therefore = authors' package default, not a statement in the paper.",
   quotes=[Q("NVIDIA Cosmos tokenizer (Agarwal et al., 2025) and extract their internal representations.", K4),
           Q('DEFAULT_COSMOS_MODEL_ID = "nvidia/Cosmos-1.0-Tokenizer-CV8x8x8"', R + "gpi_pack_video.py.txt"),
           Q("For each segment, the representation used by the video paper is the Cosmos decoder input (``vae.post_quant_conv(latent)``) averaged over its latent-time axis.", R + "gpi_pack_video.py.txt"),
           Q("This section describes how to do so using the `NVIDIA Cosmos Tokenizer <https://huggingface.co/nvidia/Cosmos-1.0-Tokenizer-CV8x8x8>`_.", R + "docs_source__gen_cosmos.rst.txt"),
           Q("The paper reports a `(16, 40, 60)` representation, but does not specify its resize or frame-sampling policy", R + "gpi_pack_readme.md.txt"),
           Q("Copyright (c) 2025 Kentaro Nakamura", R + "gpi_pack_LICENSE.txt")]),
 weights_location=dict(value="https://huggingface.co/nvidia/Cosmos-1.0-Tokenizer-CV8x8x8 (encoder.jit, decoder.jit, autoencoder.jit, vae/diffusion_pytorch_model.safetensors); gated 'auto' - access conditions must be accepted. NOT downloaded; terms NOT accepted.",
   quotes=[Q('"gated":"auto"', R + "hf_cosmos1_cv888_api.json"), Q("The default Cosmos checkpoint requires you to accept its access conditions on Hugging Face.", R + "docs_source__gen_cosmos.rst.txt")]),
 licence=dict(value="NVIDIA Open Model License Agreement (version release date January 6, 2025); card: 'This model is ready for commercial use.'",
   quotes=[Q("NVIDIA Open Model License Agreement", R + "hf_cosmos1_cv888_page.txt"), Q("Version Release Date: January 6, 2025", R + "hf_cosmos1_cv888_page.txt"), Q("This model is ready for commercial use.", R + "hf_cosmos1_cv888_page.txt")]),
 training_data=dict(value="Described, not listed: proprietary video datasets plus publicly available open-domain Internet videos (about 20M hours raw before curation), with content-category percentages; no named datasets; no medical / surgical / endoscopic / laparoscopic term anywhere in the paper (0 matches). The model card states no training data.",
   quotes=[Q("We use both proprietary video datasets and publicly available open-domain Internet videos to train our models.", S + "cosmos_arxiv_2501.03575_fulltext.txt"),
           Q("In total, we accumulate about 20M hours of raw videos with resolutions from 720p to 4k.", S + "cosmos_arxiv_2501.03575_fulltext.txt"),
           Q("We train our tokenizers directly on high-resolution images and long-duration videos without limiting the categories or aspect ratios.", S + "cosmos_arxiv_2501.03575_fulltext.txt"),
           Q("6. Nature dynamics (20%), 7. Dynamic camera movements (8%), 8. Synthetically rendered (4%), and 9. Others (7%).", S + "cosmos_arxiv_2501.03575_fulltext.txt")]),
 ds203_overlap=dict(answer="UNKNOWN", reason="Training sources undisclosed (proprietary + open-domain Internet video), so DS203 / Appendix300 source recordings cannot be excluded. The OPARA release (issued 2026-04-29) post-dates the checkpoint (created 2025-01-07), so the release itself cannot be in it; no medical category is documented."),
 input=dict(value="RGB images/videos; shorter side 256 px to 4K; up to 8 s at 1080p (A100 80 GB bound); checkpoint: 8x temporal, 8x8 spatial compression, 720 short side, 121-frame context. K4 setting: 5-s segments; pooled (16,40,60) consistent with a 320x480 input; package default max_frames=121.",
   quotes=[Q("Minimum: 256px (shorter side). Maximum: Up to 4K", R + "hf_cosmos1_cv888_page.txt"),
           Q("(8x temporal compression, 8x8 spatial compression, 720 short spatial size, 121 frames context)", R + "hf_cosmos1_cv888_page.txt"),
           Q("Our unit of analysis is the video segment, with each segment lasting 5 seconds.", K4),
           Q("which is consistent with a ``(320,480)`` input under 8x8 spatial compression", R + "gpi_pack_video.py.txt")]),
 latent_dimension=dict(value="16 channels per latent voxel; latent grid (1+(T-1)/8) x H/8 x W/8; K4 representation after temporal mean pooling: 16 x 40 x 60 = 38,400 values per 5-s segment",
   quotes=[Q("Continuous-valued feature vectors with a dimensionality of 16", R + "hf_cosmos1_cv888_page.txt"),
           Q("After pooling, the dimensionality of the resulting representa- tions is (16, 40, 60) for video", K4)]),
 params=dict(value="not stated for this checkpoint; the card's runtime table gives 105M and 34.8 ms/frame (A100, encode+decode) for 'Cosmos-Tokenizer-CV' at 4x8x8 and 720x1280 (a different compression ratio; used here only as a proxy)",
   quotes=[Q("averaged encoding and decoding times per image or video frame, measured on a single A100 80GB GPU", R + "hf_cosmos1_cv888_page.txt")]),
)
# Compute per video-hour at the K4 setting (5-s segments, <=121 frames uniformly selected, 320x480, encoder + post_quant_conv only).
FR_H = 720 * 121; PIX = 320 * 480; A100_BF16, ADA, PRO = 312e12, 0.30 * 158.5e12, 0.30 * 500e12  # A100 dense BF16 = NVIDIA spec value (assumed, not from a saved copy)
C_VAE = 10.35e12 / (157e6 * 17 * 256 * 256)  # same calibration as fm_compute_estimate.py (052590c)
rt_encdec = 34.8e-3 * PIX / (720 * 1280) * (A100_BF16 / 158.5e12) * FR_H / 3600  # card runtime, pixel-scaled, A100 -> 4500 Ada by dense-BF16 ratio
fl_whole = C_VAE * 105e6 * 121 * PIX * 720 / ADA / 3600
e["compute"] = dict(
 value=dict(frames_into_tokenizer_per_video_hour=FR_H, input="121 x 320 x 480 per 5-s segment",
   rtx4500ada_gpu_h_per_video_h=dict(runtime_scaled_encode_only=round(rt_encdec / 2, 3), runtime_scaled_encode_decode=round(rt_encdec, 3), flops_calibrated_whole_AE_105M=round(fl_whole, 3)),
   rtx4500ada_gpu_h_DS203_145_6h=dict(low=round(rt_encdec / 2 * 145.6, 1), high=round(fl_whole * 145.6, 1)),
   rtx_pro_6000_gpu_h_per_video_h=dict(low=round(rt_encdec / 2 * ADA / PRO, 3), high=round(fl_whole * ADA / PRO, 3)),
   bf16_weights_fit_24GB="yes (105M proxy)"),
 basis="Order of magnitude only. (i) Card runtime 34.8 ms/frame (A100, encode+decode, 720x1280, 105M 4x8x8 CV proxy) scaled by pixel count to 320x480 and by the dense-BF16 peak ratio A100 312 / RTX 4500 Ada 158.5; encode-only taken as half (assumption). (ii) The 052590c conv-VAE calibration c*P*voxels with P = 105M (whole-AE proxy) at 30% of dense BF16 peak. The representation needs only encode + post_quant_conv (no decode). Frame decoding is dense: <=121 of the 125 (25 fps), 150 (30 fps) or 250 (50 fps) native frames per 5-s segment are selected uniformly, so every native frame must be decoded. Native-resolution input (frame_size=None, the package default) would cost about 13.5x more at 1080p.",
 quotes=[Q("Cosmos-Tokenizer-CV 720x1280 4×8×8 105M 34.8", R + "hf_cosmos1_cv888_page.txt"),
         Q("DEFAULT_MAX_FRAMES = 121", R + "gpi_pack_video.py.txt"),
         Q("Select at most ``max_frames`` indices while retaining both endpoints.", R + "gpi_pack_video.py.txt"),
         Q("latent = get_latent(vae.encode(video)) decoder_input = vae.post_quant_conv(latent)", R + "gpi_pack_video.py.txt")])
allq = [q for f in e.values() if isinstance(f, dict) for q in f.get("quotes", [])]
e["quotes_verified"] = f"{sum(q['verified'] for q in allq)}/{len(allq)}"
json.dump(e, open(os.path.join(H, "out", "cosmos_reference_entry.json"), "w"), indent=1)
print(e["quotes_verified"]); [print("NOT VERIFIED:", q["quote"][:90], q["copy"]) for q in allq if not q["verified"]]
