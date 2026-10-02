import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_lib import save_record
C = "svd_xt_README.md"; L = "svd_xt_LICENSE.md"; V = "svd_xt_vae_config.json"; P = "svd_arxiv_2311.15127.pdf"
rec = {
 "id": "02_stable_video_diffusion",
 "name": "Stable Video Diffusion (SVD img2vid 14-frame, SVD-XT img2vid-xt 25-frame) and its VAE (AutoencoderKLTemporalDecoder)",
 "paper": {"title": "Stable Video Diffusion: Scaling Latent Video Diffusion Models to Large Datasets", "year": 2023, "arxiv": "2311.15127"},
 "weights": {
   "urls": ["https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt", "https://huggingface.co/stabilityai/stable-video-diffusion-img2vid"],
   "hf_api_evidence": ["svd_stable-video-diffusion-img2vid-xt_hfapi_blobs.json", "svd_stable-video-diffusion-img2vid_hfapi_blobs.json"],
   "files_listed_xt": {"vae/diffusion_pytorch_model.safetensors": 391017740, "unet/diffusion_pytorch_model.fp16.safetensors": 3049435868, "svd_xt.safetensors": 9559625980},
   "gated": False, "private": False,
   "note": "HF API gated=False on 2026-10-02 (raw README/LICENSE readable without login). Not downloaded."
 },
 "licence": {
   "id": "Stability AI Community License Agreement (HF license_name: stable-video-diffusion-community; LICENSE.md 'Last Updated: July 5, 2024')",
   "url": "https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt/blob/main/LICENSE.md",
   "commercial": "free commercial use only below USD 1M annual revenue, with registration", "non_commercial_only": False,
   "restrictions": "Stability AI Acceptable Use Policy (https://stability.ai/use-policy); revocable",
   "gating": "none at HF level (gated=False); licence text says acceptance by clicking or by use",
   "quote_ids": ["lic_research", "lic_grant", "lic_aup"]
 },
 "architecture": {
   "type": "latent video diffusion UNet (SD 2.1 initialised, temporal layers) + KL image autoencoder with temporally fine-tuned decoder",
   "params": "not stated in card/paper text searched; unet fp16 file 3.05 GB (~1.5B params, inferred); VAE fp32 file 391 MB (~98M params incl. temporal decoder, inferred)",
   "representation": "VAE encoder latents: 4-channel, 1/8 spatial (f8), computed frame-wise (encoder is an image encoder; only the decoder is temporal); alternatively UNet intermediate features",
   "input_resolution": "576x1024 (generation resolution)",
   "frames_per_clip": "14 (SVD) / 25 (SVD-XT)",
   "temporal_compression": "none (1x; frame-wise f8 autoencoder)",
   "spatial_compression": "8x8",
   "quote_ids": ["arch_frames", "arch_decoder", "arch_vae_class", "arch_vae_latent", "arch_sd21"]
 },
 "pretraining_data": {
   "summary": "Image stage: Stable Diffusion 2.1 initialisation. Video stage: in-house Large Video Dataset (LVD), 580M clips / 212 years, curated to LVD-F; high-res finetune on ~1M-sample 'high-quality video dataset'. Sources of LVD not named.",
   "form": "described only (LVD is internal; no source list)",
   "quote_ids": ["data_collect", "data_lvd", "data_hq", "data_appendix"]
 },
 "medical_video_in_data": {"answer": "NOT MENTIONED", "basis": "Search of saved paper PDF text and model card for medical|surgical|endoscop|laparoscop|clinic|hospital: only hit is the reference title 'U-Net: ... Biomedical Image Segmentation'."},
 "appendix300_possible": {"answer": "UNKNOWN", "basis_class": "undisclosed", "basis": "LVD sources undisclosed ('We collect an initial dataset of long videos'). Context: paper 2023-11-25, weights 2023-11-20, before the OPARA issue 2026-04-29.", "quote_ids": ["data_collect"]},
 "eligibility": {
   "C1_open_weights": {"status": "PASS", "basis": "HF API lists vae/unet safetensors, gated=False"},
   "C2_licence_research_use": {"status": "PASS", "basis": "Community License section 2 grants Research & Non-Commercial use; AUP applies"},
   "C3_domain_secondary": {"status": "PASS", "basis": "generative video (image-to-video latent diffusion) model on general video; note the VAE encoder itself is frame-wise (image) -- the video-specific part is the UNet/temporal decoder"},
   "C4_documented_pretraining_data": {"status": "FAIL", "basis": "video data = internal LVD described by size/curation only; no datasets or named sources"},
   "eligible": "NO (fails C4)"
 },
 "quotes": [
  {"id": "lic_research", "quote": "You can use this model for non-commercial or research purposes under this [license](https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt/blob/main/LICENSE.md).", "source_file": C},
  {"id": "lic_grant", "quote": "Stability AI grants You a non-exclusive, worldwide, non-transferable, non-sublicensable, revocable and royalty-free limited license under Stability AI’s intellectual property or other rights owned by Stability AI embodied in the Stability AI Materials to use, reproduce, distribute, and create Derivative Works of, and make modifications to, the Stability AI Materials for any Research or Non-Commercial Purpose.", "source_file": L},
  {"id": "lic_aup", "quote": "The model should not be used in any way that violates Stability AI's [Acceptable Use Policy](https://stability.ai/use-policy).", "source_file": C},
  {"id": "arch_frames", "quote": "This model was trained to generate 25 frames at resolution 576x1024 given a context frame of the same size, finetuned from [SVD Image-to-Video [14 frames]](https://huggingface.co/stabilityai/stable-video-diffusion-img2vid).", "source_file": C},
  {"id": "arch_decoder", "quote": "We also finetune the widely used [f8-decoder](https://huggingface.co/docs/diffusers/api/models/autoencoderkl#loading-from-the-original-format) for temporal consistency.", "source_file": C},
  {"id": "arch_vae_class", "quote": "\"_class_name\": \"AutoencoderKLTemporalDecoder\",", "source_file": V},
  {"id": "arch_vae_latent", "quote": "\"latent_channels\": 4,", "source_file": V},
  {"id": "arch_sd21", "quote": "we ground our initial model on a pretrained image diffusion model - namely Stable Diffusion 2.1 [71] - to equip it with a strong visual representation.", "source_file": P},
  {"id": "data_collect", "quote": "We collect an initial dataset of long videos which forms the base data for our video pretraining stage.", "source_file": P},
  {"id": "data_lvd", "quote": "The resulting initial dataset, which we dub Large Video Dataset (LVD), consists of 580M annotated video clip pairs, forming 212 years of content.", "source_file": P},
  {"id": "data_hq", "quote": "We finetune the base text-to-video model on a high-quality video dataset of ∼ 1M samples.", "source_file": P},
  {"id": "data_appendix", "quote": "All considered potential data sources were included for final training, with none held out as the proposed data filtering methods described in the SVD paper handle the quality control/filtering of the dataset.", "source_file": C}
 ]
}
save_record(rec)
