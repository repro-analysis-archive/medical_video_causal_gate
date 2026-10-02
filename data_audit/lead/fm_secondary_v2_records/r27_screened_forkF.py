import sys; sys.path.insert(0, '/home/user/projects/medical_video_causal_gate/data_audit/lead')
from fm_secondary_v2_lib import save_screened

NOTFOUND = "リクエストされたファイルは存在しません。"
SHA = "\"sha256\": \"38071ab59bd94681c686fa51d75a1968f64e470262043be31f7a094e442fd981\","
items = [
 {
  "name": "TATS 3D VQGAN (songweige/TATS; per-dataset VQGAN checkpoints for UCF-101, Sky-Timelapse, Taichi-HD, MUGEN, AudioSet-Drums)",
  "paper": "Long Video Generation with Time-Agnostic VQGAN and Time-Sensitive Transformer (Ge et al., ECCV 2022, arXiv:2204.03638)",
  "reason_not_added": "no publicly downloadable official weights: the README's Google Drive VQGAN links (checked UCF-101, Sky-Timelapse, Taichi-HD) return HTTP 404 on 2026-10-02 (view page and download endpoint); C1 would FAIL. Code licence MIT. Data would have been closed curated lists (UCF-101, Sky-Timelapse, Taichi-HD, MUGEN, AudioSet-Drums).",
  "checked_utc": "2026-10-02",
  "quotes": [
   {"id": "readme_ucf", "quote": "UCF-101: [official data](https://www.crcv.ucf.edu/data/UCF101.php), [VQGAN](https://drive.google.com/file/d/15Otpyr7v6Wnyw2HfQr_cuaRsBiSMd7Rh/view?usp=sharing)", "source_file": "tats_github_README.md"},
   {"id": "drive_404_ucf", "quote": NOTFOUND, "source_file": "tats_vqgan_ucf101_gdrive_view.txt"},
   {"id": "drive_404_sky", "quote": NOTFOUND, "source_file": "tats_vqgan_sky_gdrive_view.txt"},
   {"id": "drive_404_taichi", "quote": NOTFOUND, "source_file": "tats_vqgan_taichi_gdrive_view.txt"},
   {"id": "head_404_ucf", "quote": "\"http_status\": 404,", "source_file": "tats_vqgan_ucf101_uc_head.json"},
   {"id": "lic", "quote": "TATS is licensed under the MIT license, as found in the LICENSE file.", "source_file": "tats_github_README.md"}
  ]
 },
 {
  "name": "SkyReels-V2 (Skywork/SkyReels-V2-*; checked Skywork/SkyReels-V2-T2V-14B-540P)",
  "reason_not_added": "duplicate VAE: the repo ships Wan2.1_VAE.pth with the same size (507,609,880 bytes) and the same LFS sha256 as Wan-AI/Wan2.1-T2V-1.3B -> byte-identical to the Wan-VAE already recorded as entry 05; no separate tokenizer to audit",
  "checked_utc": "2026-10-02",
  "quotes": [
   {"id": "sky_file", "quote": "\"rfilename\": \"Wan2.1_VAE.pth\",", "source_file": "skyreels_Skywork__SkyReels-V2-T2V-14B-540P_hfapi.json"},
   {"id": "sky_sha", "quote": SHA, "source_file": "skyreels_Skywork__SkyReels-V2-T2V-14B-540P_hfapi.json"},
   {"id": "wan_sha", "quote": SHA, "source_file": "skyreelscmp_Wan-AI__Wan2.1-T2V-1.3B_hfapi.json"}
  ]
 }
]
save_screened(items, "forkF")
