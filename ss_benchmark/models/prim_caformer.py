"""SurgeNetCholec / SurgeNetRARP adapter: CAFormer-S18 (frame-level, primary arm).

* Architecture: CAFormer-S18 ("a standard named architecture", §4.1.4 rule 3) via timm 1.0.15 `caformer_s18`
  (num_classes=0). SurgeNet's own metaformer.py (saved copy fm_sources/primary/surgenet_metaformer_py.txt) is the
  original MetaFormer implementation of the same network; checkpoints in that naming are mapped with timm's
  metaformer checkpoint_filter_fn when weights are loaded (§14 step 4; not exercised at code lock).
* Representation: pooled, normalised stage-4 features (forward_head(pre_logits=True) = norm(mean over H, W)), 512-d;
  the same tensor as `self.norm(x.mean([1, 2]))` in SurgeNet's metaformer.py.
* Input size 224 × 224 (CAFormer-S18 / ImageNet-1k initialisation resolution; timm pretrained_cfg input_size). The
  SurgeNet papers state 224×399 for downstream fine-tuning only; the protocol's square standardized frame is resized
  to the model input size (§3.1 step 2).
* Normalisation: ImageNet mean / std (timm pretrained_cfg of caformer_s18; SurgeNet initialises from ImageNet-1k
  weights). No level-1–3 SurgeNet source states a different normalisation.
"""
import torch

_MEAN = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1)
_STD = torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1)

_SOURCES = [
    dict(quote="We initiate pretraining from ImageNet-initialized weights as recommended by Ramesh et al. (2023)",
         copy="data_audit/lead/fm_sources/primary/surgenetxl_arxiv_pdf.txt", level=1),
    dict(quote="\"ImageNet1k\": \"https://huggingface.co/sail/dl/resolve/main/caformer/caformer_s18.pth\"",
         copy="data_audit/lead/fm_sources/primary/surgenet_github_readme.txt", level=2),
    dict(quote="self.norm(x.mean([1, 2])),", copy="data_audit/lead/fm_sources/primary/surgenet_metaformer_py.txt",
         level=2),
]


def _spec(name):
    return dict(name=name, arm="primary", kind="frame", input_size=(224, 224), clip_length=None,
                representation="CAFormer-S18 pooled normalised stage-4 features (512)",
                normalisation="ImageNet mean/std on [0,1] pixels", sources=_SOURCES, third_party=None)


SPECS = {"SurgeNetCholec": _spec("SurgeNetCholec (CAFormer-S18)"), "SurgeNetRARP": _spec("SurgeNetRARP (CAFormer-S18)")}
SPEC = SPECS["SurgeNetCholec"]


def build(weights=None, device="cpu", dtype=torch.float32):
    import timm
    model = timm.create_model("caformer_s18", pretrained=False, num_classes=0)
    if weights is not None:
        from timm.models.metaformer import checkpoint_filter_fn
        sd = torch.load(weights, map_location="cpu", weights_only=False)
        for key in ("teacher", "student", "state_dict", "model"):
            if isinstance(sd, dict) and key in sd and isinstance(sd[key], dict):
                sd = sd[key]
                break
        sd = {k.replace("module.", "").replace("backbone.", ""): v for k, v in sd.items()}
        sd = checkpoint_filter_fn(sd, model)
        missing, unexpected = model.load_state_dict(sd, strict=False)
        missing = [k for k in missing if not k.startswith("head.fc")]
        unexpected = [k for k in unexpected if not k.startswith(("head", "dino_head"))]
        if missing or unexpected:
            raise RuntimeError(f"checkpoint mismatch: missing {missing[:5]}, unexpected {unexpected[:5]}")
    return model.to(device=device, dtype=dtype).eval()


def encode(model, x):
    p = next(model.parameters())
    x = ((x / 255.0 - _MEAN.to(x.device)) / _STD.to(x.device)).to(p.dtype)
    return model.forward_head(model.forward_features(x), pre_logits=True)
