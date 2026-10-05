"""VideoMAE adapter (clip-level, secondary arm; self-supervised K400 / SSv2 / UCF101 pre-training checkpoints).

* Architecture: transformers 4.46.3 VideoMAEModel (encoder only) with the configuration of the checkpoint's size:
  ViT-B = fm_sources/secondary/videomae_videomae-base_config.json, ViT-L = videomae_videomae-large_config.json
  (level 3; "num_frames": 16, "image_size": 224, "tubelet_size": 2, "patch_size": 16, "use_mean_pooling": false).
  The SSv2 / short configs are the same ViT-B configuration. Random initialisation at code lock.
* Checkpoints covered (ViT-B and ViT-L: the sizes whose compute the eligibility facts quote, paper Table 7):
  HF format (MCG-NJU): videomae-base (K400, 1600 ep), videomae-base-short (K400, 800 ep), videomae-base-ssv2 (SSv2,
  2400 ep), videomae-large (K400, 1600 ep); original-repository format (MODEL_ZOO.md, pre-training checkpoints):
  K400 ViT-B 800 / 1600 ep, K400 ViT-L 1600 ep, SSv2 ViT-B 800 / 2400 ep, UCF101 ViT-B 3200 ep. Original-format
  state dicts are mapped to transformers names with the encoder rules of transformers'
  models/videomae/convert_videomae_to_pytorch.py (rename_key / convert_state_dict; decoder, mask token and
  encoder_to_decoder keys dropped). ViT-S / ViT-H checkpoints are not covered (no saved configuration).
* Input: clip of L = 16 grid frames ("num_frames": 16), 224 × 224 ("image_size": 224), layout (B, T, 3, H, W).
* Normalisation: x / 255, then mean / std = the checkpoint's preprocessor_config.json (HF format) when present;
  otherwise ImageNet mean (0.485, 0.456, 0.406) / std (0.229, 0.224, 0.225) (the VideoMAE code base's
  IMAGENET_DEFAULT_MEAN / STD; random init and original-format checkpoints).
* Representation: VideoMAEModel(...).last_hidden_state = the output of the final encoder layer after the final
  LayerNorm (videomae.layernorm, present because use_mean_pooling = false), averaged over all tokens: 8 temporal
  (16 frames / tubelet 2) × 14 × 14 spatial = 1,568 patch tokens; VideoMAE has no CLS token. 768 (ViT-B) or 1,024
  (ViT-L) values. No head, no fc_norm.
* Inference: eval() (dropout / drop-path inactive; dropout probabilities are 0 in the configs); no token masking
  (bool_masked_pos is not passed).
"""
import json
import os

import torch

_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_SRC = os.path.join(_REPO, "data_audit", "lead", "fm_sources", "secondary")
CONFIGS = {"base": "videomae_videomae-base_config.json", "large": "videomae_videomae-large_config.json"}
CHECKPOINTS = {
    # key: (size, format, identifier)
    "hf-base-k400-1600": ("base", "hf", "MCG-NJU/videomae-base"),
    "hf-base-k400-800": ("base", "hf", "MCG-NJU/videomae-base-short"),
    "hf-base-ssv2-2400": ("base", "hf", "MCG-NJU/videomae-base-ssv2"),
    "hf-large-k400-1600": ("large", "hf", "MCG-NJU/videomae-large"),
    "orig-base-k400-800": ("base", "original", "MODEL_ZOO K400 ViT-B 800 ep pre-training checkpoint"),
    "orig-base-k400-1600": ("base", "original", "MODEL_ZOO K400 ViT-B 1600 ep pre-training checkpoint"),
    "orig-large-k400-1600": ("large", "original", "MODEL_ZOO K400 ViT-L 1600 ep pre-training checkpoint"),
    "orig-base-ssv2-800": ("base", "original", "MODEL_ZOO SSv2 ViT-B 800 ep pre-training checkpoint"),
    "orig-base-ssv2-2400": ("base", "original", "MODEL_ZOO SSv2 ViT-B 2400 ep pre-training checkpoint"),
    "orig-base-ucf101-3200": ("base", "original", "MODEL_ZOO UCF101 ViT-B 3200 ep pre-training checkpoint"),
}
VARIANTS = {"base": "base", "base-ssv2": "base", "base-short": "base", "large": "large"}
IMAGENET = ([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])

SPEC = dict(name="VideoMAE", arm="secondary", kind="clip", input_size=(224, 224), clip_length=16,
            representation="last_hidden_state (final encoder layer after videomae.layernorm) averaged over all "
                           "1568 patch tokens (8 x 14 x 14; no CLS token); 768 (ViT-B) / 1024 (ViT-L)",
            normalisation="x/255, checkpoint preprocessor_config mean/std (HF format) else ImageNet mean/std",
            checkpoints=CHECKPOINTS,
            sources=[dict(quote="\"num_frames\": 16,",
                          copy="data_audit/lead/fm_sources/secondary/videomae_videomae-base_config.json", level=3),
                     dict(quote="\"image_size\": 224,",
                          copy="data_audit/lead/fm_sources/secondary/videomae_videomae-base_config.json", level=3),
                     dict(quote="\"use_mean_pooling\": false",
                          copy="data_audit/lead/fm_sources/secondary/videomae_videomae-base_config.json", level=3),
                     dict(quote="VideoMAE ViT-B 7 16 180×5×3 87 81.5 95.1",
                          copy="data_audit/lead/fm_sources/secondary/videomae_arxiv_2203.12602v3.txt", level=1)],
            third_party=None)


def _rename_key(name):
    """Encoder part of transformers' convert_videomae_to_pytorch.rename_key (Apache-2.0)."""
    if "encoder." in name:
        name = name.replace("encoder.", "")
    if "cls_token" in name:
        name = name.replace("cls_token", "videomae.embeddings.cls_token")
    if "pos_embed" in name and "decoder" not in name:
        name = name.replace("pos_embed", "videomae.embeddings.position_embeddings")
    if "patch_embed.proj" in name:
        name = name.replace("patch_embed.proj", "videomae.embeddings.patch_embeddings.projection")
    if "patch_embed.norm" in name:
        name = name.replace("patch_embed.norm", "videomae.embeddings.norm")
    if "blocks" in name:
        name = name.replace("blocks", "videomae.encoder.layer")
    if "attn.proj" in name:
        name = name.replace("attn.proj", "attention.output.dense")
    if "attn" in name and "bias" not in name:
        name = name.replace("attn", "attention.self")
    if "attn" in name:
        name = name.replace("attn", "attention.attention")
    if "norm1" in name:
        name = name.replace("norm1", "layernorm_before")
    if "norm2" in name:
        name = name.replace("norm2", "layernorm_after")
    if "mlp.fc1" in name:
        name = name.replace("mlp.fc1", "intermediate.dense")
    if "mlp.fc2" in name:
        name = name.replace("mlp.fc2", "output.dense")
    if "norm.weight" in name and "fc" not in name:
        name = name.replace("norm.weight", "videomae.layernorm.weight")
    if "norm.bias" in name and "fc" not in name:
        name = name.replace("norm.bias", "videomae.layernorm.bias")
    return name


def convert_original(sd, hidden_size):
    """Original-repository pre-training state dict -> VideoMAEModel state dict (encoder only)."""
    for key in ("model", "module", "state_dict"):
        if key in sd and isinstance(sd[key], dict):
            sd = sd[key]
    out = {}
    for key, val in sd.items():
        if key.startswith(("decoder", "encoder_to_decoder", "mask_token")):
            continue
        k = key[len("encoder."):] if key.startswith("encoder.") else key
        if "qkv" in k:
            layer = int(k.split(".")[1])
            p = f"encoder.layer.{layer}.attention.attention."
            if "weight" in k:
                out[p + "query.weight"] = val[:hidden_size]
                out[p + "key.weight"] = val[hidden_size:2 * hidden_size]
                out[p + "value.weight"] = val[-hidden_size:]
            continue
        k = _rename_key(k)
        out[k[len("videomae."):] if k.startswith("videomae.") else k] = val
    return out


def build(weights=None, device="cpu", dtype=torch.float32, variant="base", checkpoint=None):
    """weights=None: random init of the size of ``checkpoint`` (CHECKPOINTS key) or ``variant``; weights=path:
    an HF directory (format "hf") or an original-repository .pth (format "original")."""
    from transformers import VideoMAEConfig, VideoMAEModel
    size, fmt = (CHECKPOINTS[checkpoint][:2] if checkpoint else (VARIANTS[variant], "hf"))
    config = VideoMAEConfig.from_json_file(os.path.join(_SRC, CONFIGS[size]))
    mean, std = IMAGENET
    if weights is None:
        model = VideoMAEModel(config)
    elif fmt == "hf":
        model = VideoMAEModel.from_pretrained(weights, local_files_only=True)
        pp = os.path.join(weights, "preprocessor_config.json")
        cfg = json.load(open(pp)) if os.path.exists(pp) else {}
        mean, std = cfg.get("image_mean", mean), cfg.get("image_std", std)
    else:
        model = VideoMAEModel(config)
        sd = convert_original(torch.load(weights, map_location="cpu", weights_only=False), config.hidden_size)
        missing, unexpected = model.load_state_dict(sd, strict=False)
        if missing or unexpected:
            raise RuntimeError(f"checkpoint mismatch: missing {missing[:5]}, unexpected {unexpected[:5]}")
    model.ss_norm = (torch.tensor(mean).view(1, 1, 3, 1, 1), torch.tensor(std).view(1, 1, 3, 1, 1))
    return model.to(device=device, dtype=dtype).eval()


def encode(model, x):
    p = next(model.parameters())
    mean, std = (t.to(x.device) for t in model.ss_norm)
    out = model(pixel_values=((x / 255.0 - mean) / std).to(p.dtype))
    return out.last_hidden_state.mean(1)
