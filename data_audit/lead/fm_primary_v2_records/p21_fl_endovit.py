"""Federated EndoViT (FL-EndoViT; NCT/TU Dresden) (new entry, fork A; no released weights)."""
from ._common import A300, C, NOT_MENTIONED, Q, elig

REC = {
    "name": "FL-EndoViT (Federated EndoViT; NCT/UCC Dresden)",
    "aliases": ["Federated EndoViT"],
    "paper": {"title": "Federated EndoViT: Pretraining Vision Transformers via Federated Learning on Endoscopic Image Collections", "year": 2025,
              "venue": "arXiv 2504.16612v3 (preprint submitted to MIDL)", "arxiv": "2504.16612",
              "quotes": [Q("Comments: Preprint submitted to MIDL", "fedendovit_arxiv_abs"),
                         Q("Translational Surgical Oncology, National Center for Tumor Diseases (NCT), NCT/UCC Dresden, a partnership between DKFZ, Faculty of Medicine and University Hospital Carl Gustav Carus", "fedendovit_arxiv_pdf")]},
    "version": {"value": "no released checkpoint (repo KirchnerMax/FL-EndoViT publishes training code only; no GitHub releases)", "basis": "paper reproducibility statement + README + repo page",
                "quotes": [Q("we make our training code publicly available at https://github.com/KirchnerMax/FL-EndoViT.", "fedendovit_arxiv_pdf"),
                           Q("Releases Packages Contributors", "fedendovit_github_page")]},
    "weights_location": {"url": None, "exists": "NO - README and paper mention only training code; no weights link, no release assets", "access": "n/a",
                         "verification": "GitHub README + repo HTML page, arXiv PDF, 2026-10-02",
                         "quotes": [Q("we make our training code publicly available", "fedendovit_arxiv_pdf")]},
    "licence": {"code": "no licence file/statement found (repo sidebar shows none)", "weights": "n/a", "url": "https://github.com/KirchnerMax/FL-EndoViT", "code_and_weights_differ": "n/a", "quotes": []},
    "domain": {"value": "endoscopic surgery video frames (Endo700k, via simulated federated MAE pretraining)",
               "quotes": [Q("a FL environment is simulated using the Endo700k dataset collection", "fedendovit_arxiv_pdf"), Q("partitioned across nine distinct clients.", "fedendovit_arxiv_pdf")]},
    "pretraining_data_quote": {"summary": "Endo700k (the 9 public datasets of EndoViT, incl. DSAD from Carus Dresden), partitioned into 9 simulated clients",
                               "datasets": ["Endo700k (HeiCo, Cholec80, PSI-AVA, ESAD, LapGyn4, hSDB-instrument, DSAD, GLENDA, SurgicalActions160) - see EndoViT entry"],
                               "quotes": [Q("Pretrained on the large-scale Endo700k dataset, FL-EndoViT is evaluated against a centralized baseline", "fedendovit_arxiv_pdf"),
                                          Q("[Endo700k Dataset Collection](https://github.com/DominikBatic/EndoViT#download-endo700k)", "fedendovit_github_readme")]},
    "appendix300_check": A300(
        "NO", NOT_MENTIONED, False,
        "Pretraining data = Endo700k (closed list of 9 named public datasets; see EndoViT entry). DSAD in Endo700k is from University Hospital Carl "
        "Gustav Carus Dresden (an Appendix300 centre) but is robot-assisted rectal surgery, not appendectomy. Authors are from NCT/UCC Dresden "
        "(partnership incl. Carus), but no in-house data were used.",
        [Q("a FL environment is simulated using the Endo700k dataset collection", "fedendovit_arxiv_pdf")]),
    "input": {"frame_size": "as EndoViT (224x224 MAE ViT-B; not restated in the saved text)", "frame_rate_or_sampling": "Endo700k frames (1 fps, see EndoViT)", "clip_length_frames": "1",
              "notes": "EndoViT ViT backbone with 75% masking", "quotes": [Q("functions as the backbone, utilizing a MAE objective where the model learns to reconstruct the original image from inputs where 75% of the original image is masked out.", "fedendovit_arxiv_pdf")]},
    "embedding_dim": {"value": "768 (EndoViT ViT-B backbone; not restated)", "basis": "backbone = EndoViT", "quotes": []},
    "params": {"value": "not stated in the saved text", "quotes": []},
    "flops_per_input_if_documented": {"value": None, "statement": "not documented (searched 'FLOP')", "quotes": []},
    "eligibility": elig(
        C("FAIL", "Only training code released; no pretrained weights."),
        C("UNKNOWN", "No licence found in repo."),
        C("PASS", "MAE pretraining on endoscopic surgery video frames (Endo700k)."),
        C("PASS", "Endo700k named (documented in EndoViT)."),
        "Dresden-group model, but trained only on public Endo700k."),
}
