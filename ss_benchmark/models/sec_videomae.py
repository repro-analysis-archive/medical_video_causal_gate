"""VideoMAE adapter (clip-level, secondary arm; K400 / SSv2 / UCF101 self-supervised checkpoints).

* Architecture: transformers VideoMAEModel with the released checkpoint's config.json (saved copies:
  fm_sources/secondary/videomae_videomae-{base,base-ssv2,base-short,large}_config.json); random initialisation at
  code lock. Clip length 16 ("num_frames": 16), input 224 × 224 ("image_size": 224), tubelet 2.
* Representation: mean of the last hidden states over all tokens (768-d base, 1024-d large); the released
  pre-training checkpoints have use_mean_pooling = false and no fc_norm, so no head is applied.
* Normalisation: the checkpoint's preprocessor_config.json image_mean / image_std when weights are loaded from a
  local checkpoint directory (§14 step 4); otherwise ImageNet mean / std (the VideoMAE code base's
  IMAGENET_DEFAULT_MEAN / STD).
"""
import json
import os

import torch

_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_SRC = os.path.join(_REPO, "data_audit", "lead", "fm_sources", "secondary")
VARIANTS = {"base": "videomae_videomae-base_config.json", "base-ssv2": "videomae_videomae-base-ssv2_config.json",
            "base-short": "videomae_videomae-base-short_config.json", "large": "videomae_videomae-large_config.json"}

SPEC = dict(name="VideoMAE", arm="secondary", kind="clip", input_size=(224, 224), clip_length=16,
            representation="mean of last_hidden_state over tokens", normalisation="checkpoint preprocessor_config "
            "(fallback ImageNet mean/std)", variants=VARIANTS,
            sources=[dict(quote="\"num_frames\": 16,",
                          copy="data_audit/lead/fm_sources/secondary/videomae_videomae-base_config.json", level=3),
                     dict(quote="\"image_size\": 224,",
                          copy="data_audit/lead/fm_sources/secondary/videomae_videomae-base_config.json", level=3)],
            third_party=None)


def build(weights=None, device="cpu", dtype=torch.float32, variant="base"):
    from transformers import VideoMAEConfig, VideoMAEModel
    if weights is None:
        model = VideoMAEModel(VideoMAEConfig.from_json_file(os.path.join(_SRC, VARIANTS[variant])))
        mean, std = [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]
    else:
        model = VideoMAEModel.from_pretrained(weights, local_files_only=True)
        pp = os.path.join(weights, "preprocessor_config.json")
        cfg = json.load(open(pp)) if os.path.exists(pp) else {}
        mean = cfg.get("image_mean", [0.485, 0.456, 0.406])
        std = cfg.get("image_std", [0.229, 0.224, 0.225])
    model.ss_norm = (torch.tensor(mean).view(1, 1, 3, 1, 1), torch.tensor(std).view(1, 1, 3, 1, 1))
    return model.to(device=device, dtype=dtype).eval()


def encode(model, x):
    p = next(model.parameters())
    mean, std = (t.to(x.device) for t in model.ss_norm)
    out = model(pixel_values=((x / 255.0 - mean) / std).to(p.dtype))
    return out.last_hidden_state.mean(1)
