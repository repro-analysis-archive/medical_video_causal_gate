| model | arm | 0.5 fps | 1 fps | 2 fps | 4 fps | documented sampling |
|---|---|---|---|---|---|---|
| Endo-FM (ViT-B video, 121M) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 4.5 h (model) |
| EndoViT (ViT-B/16, 85.8M) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.2 h (I/O) |
| SurgeNetXL CAFormer-S18 (24.3M) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.2 h (I/O) |
| SurgeNetXL DINO ViT-L/14 (~304M) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.2 h (I/O) |
| SurgeNet / Public variants (CAFormer-S18) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.2 h (I/O) |
| SurgVLP / HecVL / PeskaVLP (ResNet-50 visual) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.2 h (I/O) |
| EndoMamba (24.46M) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.3 h (decode ~ I/O) |
| LemonFM (ConvNeXt-L, ~198M std) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.2 h (I/O) |
| EndoSSL ViT-L (~304M std) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.2 h (I/O) |
| SelfSupSurg (ResNet-50) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.3 h (decode ~ I/O) |
| SurgLIME (ViT-B/16 visual) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.2 h (I/O) |
| PL-Stitch (ViT-B/16) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.2 h (I/O) |
| Basel V-JEPA ViT-L (~304M std) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.3 h (decode ~ I/O) |
| Cosmos-H-Surgical v0.3.1 (~15.2B DiT) | primary | 4.8 h (model) | 9.7 h (model) | 19.4 h (model) | 38.7 h (model) | 154.7 h (model) |
| Cosmos-H-Surgical Predict/Transfer 2.5 (2B) | primary | 5.7 h (model) | 11.5 h (model) | 23.0 h (model) | 46.0 h (model) | 183.7 h (model) |
| Cosmos-H-Surgical-Simulator (~2B) | primary | 3.1 h (decode) | 3.2 h (I/O) | 4.5 h (model) | 9.0 h (model) | 22.4 h (model) |
| Cosmos-H-Dreams (~2B) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.6 h (model) | 7.3 h (model) | 18.2 h (model) |
| MedSora-B (86.47M) | primary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.3 h (decode ~ I/O) |
| SG2VID (U-Net ~1.24B, inferred from fp32 file size) | primary | 3.1 h (decode) | 3.2 h (I/O) | 4.0 h (model) | 8.0 h (model) | 8.0 h (model) |
| KVLR (~12.06B) | primary | 6.5 h (model) | 12.9 h (model) | 25.8 h (model) | 51.7 h (model) | 387.6 h (model) |
| Open-Sora VAE v1.2 (384M whole) | secondary | 3.1 h (decode) | 4.7 h (model) | 9.4 h (model) | 18.8 h (model) | 113.0 h (model) |
| VideoMAE-B (87M) | secondary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.3 h (decode ~ I/O) |
| VideoMAE-L (305M) | secondary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.3 h (decode ~ I/O) |
| VideoMAE-H (633M) | secondary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.3 h (decode ~ I/O) |
| VideoMAE V2-g (1011M) | secondary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.3 h (decode ~ I/O) |
| OmniTokenizer | secondary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.3 h (decode ~ I/O) |
| Open-Sora-Plan v1.2 VAE (enc 94M) | secondary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 4.6 h (model) | 28.8 h (model) |
| WF-VAE-L 16ch (enc 84M) | secondary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 4.1 h (model) | 25.7 h (model) |
| CV-VAE (enc 68M) | secondary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.3 h (model ~ decode) | 20.8 h (model) |
| LARP-L (173M) | secondary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.3 h (decode ~ I/O) |
| LeanVAE (39.8M) | secondary | 3.1 h (decode) | 3.2 h (I/O) | 3.2 h (I/O ~ decode) | 3.2 h (decode ~ I/O) | 3.3 h (decode ~ I/O) |
| Reducio-VAE (437M whole) | secondary | 3.1 h (decode) | 5.4 h (model) | 10.7 h (model) | 21.4 h (model) | 85.7 h (model) |
| Open-MAGVIT2 video | secondary | 3.1 h (decode (model n/e)) | 3.2 h (I/O (model n/e)) | 3.2 h (I/O ~ decode (model n/e)) | 3.2 h (decode ~ I/O (model n/e)) | 3.2 h (I/O (model n/e)) |
| Cosmos tokenizer CV8x8x8 (Decision 005 reference) | reference | 3.1 h (decode) | 3.2 h (I/O ~ model) | 6.0 h (model) | 12.1 h (model) | 73.1 h (model) |
