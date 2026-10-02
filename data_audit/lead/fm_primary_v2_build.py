"""Build out/fm_candidates_primary.json (DECISION_003 §2 / DECISION_004 §3, PRIMARY domain), version 2.

Records: one module per candidate in fm_primary_v2_records/pNN_*.py, each defining REC (dict).
Every {"quote":..., "file":...} dict anywhere in a record is checked as a whitespace-normalised
substring of the saved text copy fm_sources/primary/<file>.txt; the result, the source URL and the
saved-copy path are written into the quote dict.  The output JSON is rewritten after EACH entry
(incremental).  Run with /home/user/miniconda3/bin/python3.
"""
import copy
import importlib
import json
import os
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import fm_primary_v2_lib as L  # noqa: E402

REC_DIR = HERE / "fm_primary_v2_records"
OUT = HERE / "out" / "fm_candidates_primary.json"
RULE = ("DECISION_003.md §2 (unchanged in DECISION_004.md §3): eligible only if (1) open weights publicly "
        "downloadable, (2) licence permits research use, (3) PRIMARY domain = pretrained on surgical or "
        "endoscopic video (or video frames), (4) documented pretraining data")


CONVENTIONS = {
    "open_weights": "PASS if official weight files are listed publicly (HF API listing or an official public download "
                    "URL resolving to the file, checked by HEAD / API metadata only) without a manual-approval step; "
                    "HF gated='auto' click-through = PASS with a gating flag; manual approval / request form / e-mail = "
                    "UNKNOWN; no official weights or dead link = FAIL. No weights downloaded, no terms accepted.",
    "licence_research_use": "PASS if the quoted licence text covers (non-commercial) research use; FAIL if research use "
                            "is not permitted; UNKNOWN if no licence text is found for the weights/code.",
    "domain_primary": "PASS if the released checkpoint's own (self-/weakly-supervised, contrastive or generative) "
                      "pretraining or domain post-training corpus is surgical or endoscopic video or frames sampled "
                      "from such video (general-domain initialisation allowed and recorded); FAIL if surgical data "
                      "are used only for a task-specific fine-tune/adapter on a generic backbone, or the training "
                      "images are not endoscopic/surgical; UNKNOWN if the documentation does not say whether the "
                      "images are video frames.",
    "documented_pretraining_data": "PASS if the paper / model card names the datasets or named sources of the surgical/"
                                   "endoscopic pretraining or post-training stage that qualifies the model under the domain "
                                   "criterion (named public datasets, named institutions, named web platforms with URL lists "
                                   "or counts); FAIL if described only generically; UNKNOWN if the naming document is not "
                                   "accessible. The documentation level of a general-domain initialisation / base model is "
                                   "recorded in the basis and decides the Appendix300 check, not this criterion.",
    "appendix300_check": "YES if DS203/Appendix300 (doi 10.25532/OPARA-1173, issued 2026-04-29) or its source "
                         "recordings/centres' appendectomy recordings are listed. Lineage = training data of the "
                         "released weights plus the data of their initialisation / base / frozen-backbone weights "
                         "(distillation teachers are recorded in the note but do not decide). NO only if every lineage "
                         "component is a closed list of named datasets / institutions, or in-house data whose documented "
                         "institutions, geography or modality exclude the Appendix300 centres' laparoscopic appendectomy "
                         "recordings, or a closed curated benchmark (ImageNet, Kinetics, SSv2...). UNKNOWN if any "
                         "lineage component is undisclosed, web-scale (e.g. CLIP, DINOv2 LVD-142M, LLM/VLM or Cosmos "
                         "base data) or open-ended web-scraped (YouTube, HowTo100M, WebSurg), so the source recordings "
                         "cannot be excluded. Initialisation that is not documented at all is noted as a caveat.",
}


def atomic_write(path, text):
    tmp = path.with_suffix(path.suffix + f".tmp{os.getpid()}")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def walk_quotes(obj, path=""):
    if isinstance(obj, dict):
        if "quote" in obj and "file" in obj:
            yield path, obj
        for k, v in obj.items():
            yield from walk_quotes(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_quotes(v, f"{path}[{i}]")


def process(rec, man, failures):
    rec = copy.deepcopy(rec)
    used = set(rec.pop("extra_sources", []))
    for path, q in walk_quotes(rec):
        stem = q["file"]
        used.add(stem)
        e = man.get(stem)
        if e is None:
            q["verified_verbatim_ws_normalised"] = False
            failures.append((rec["name"], path, stem, "SOURCE NOT SAVED"))
            continue
        ok = L.norm(q["quote"]) in L.text_of(stem)
        q["verified_verbatim_ws_normalised"] = ok
        q["source_url"] = e["url"]
        q["saved_copy"] = e["text_file"]
        if not ok:
            failures.append((rec["name"], path, stem, q["quote"][:100]))
    rec["sources"] = [
        {"name": s, "url": man[s]["url"], "final_url": man[s].get("final_url"), "http_status": man[s].get("status"),
         "kind": man[s].get("kind"), "saved_copy": man[s]["text_file"], "rendering": man[s].get("rendering"),
         "raw_sha256": man[s].get("raw_sha256"), "fetched_utc": man[s]["fetched_utc"]}
        for s in sorted(used) if s in man]
    for s in sorted(used):
        if s not in man:
            failures.append((rec["name"], "sources", s, "SOURCE NOT SAVED"))
    n_q = sum(1 for _ in walk_quotes(rec))
    n_ok = sum(1 for _, q in walk_quotes(rec) if q.get("verified_verbatim_ws_normalised"))
    rec["quote_verification"] = {"quotes": n_q, "verified": n_ok,
                                 "method": "whitespace-normalised substring of saved text copy"}
    return rec


def main(only=None):
    man = L.manifest()
    mods = sorted(p.stem for p in REC_DIR.glob("p[0-9][0-9]_*.py"))
    failures, out = [], []
    for m in mods:
        if only and m not in only:
            continue
        try:
            mod = importlib.import_module(f"fm_primary_v2_records.{m}")
            rec = mod.REC
        except Exception as e:  # a module being edited must not break the others
            failures.append((m, "import", "", repr(e)[:200]))
            continue
        out.append(process(rec, man, failures))
        doc = {"rule": RULE, "domain": "primary (surgical / endoscopic video)",
               "survey_date": "2026-10-02", "judging_conventions": CONVENTIONS,
               "saved_copies_dir": str(L.SAVE_DIR), "builder": str(pathlib.Path(__file__)),
               "n_candidates": len(out),
               "all_quotes_verified": all(c["quote_verification"]["quotes"] == c["quote_verification"]["verified"]
                                          for c in out),
               "candidates": out}
        if only is None:
            atomic_write(OUT, json.dumps(doc, indent=1, ensure_ascii=False))  # incremental, after each entry
        print(f"[{len(out):2d}] {out[-1]['name'][:70]}: quotes "
              f"{out[-1]['quote_verification']['verified']}/{out[-1]['quote_verification']['quotes']}")
    print(f"{'wrote ' + str(OUT) if only is None else 'dry run'}; candidates={len(out)}; failures={len(failures)}")
    for f in failures:
        print("  FAIL", f)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(set(sys.argv[1:]) or None))
