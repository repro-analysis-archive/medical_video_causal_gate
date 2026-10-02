"""Helpers for the DECISION_003 sec.2 SECONDARY foundation-model candidate audit.

fetch():   save a source page (raw bytes + text rendering + sidecar meta) under SRC_DIR.
verify():  whitespace-normalized verbatim containment of a quote in the saved text rendering.
assemble(): rebuild the output JSON from per-candidate record files, re-verifying every quote.

No model weights are downloaded: only HTML/markdown/JSON/PDF documentation pages and HF API listings.
"""
import datetime
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
import time

import requests
from bs4 import BeautifulSoup

SRC_DIR = "/media/user/LaCie/medvideo_gate/fm_candidates/secondary"
REC_DIR = os.path.join(SRC_DIR, "records")
OUT_JSON = "/home/user/projects/medical_video_causal_gate/data_audit/lead/out/fm_candidates_secondary.json"
UA = "Mozilla/5.0 (X11; Linux x86_64) research-audit (documentation pages only)"
MAX_BYTES = 60 * 1024 * 1024  # documentation only; refuse anything larger

os.makedirs(SRC_DIR, exist_ok=True)
os.makedirs(REC_DIR, exist_ok=True)


def _now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def html_to_text(raw):
    soup = BeautifulSoup(raw, "html.parser")
    for t in soup(["script", "style", "noscript", "svg"]):
        t.decompose()
    return soup.get_text(" ")


def fetch(url, fname, kind=None, force=False):
    """Save url to SRC_DIR/fname. kind in {html, pdf, text, json}; inferred if None.
    Writes fname (raw), fname.txt (text rendering used for verification), fname.meta.json."""
    path = os.path.join(SRC_DIR, fname)
    meta_path = path + ".meta.json"
    if os.path.exists(meta_path) and not force:
        return json.load(open(meta_path))
    r = requests.get(url, headers={"User-Agent": UA}, timeout=120, stream=True, allow_redirects=True)
    data = b""
    for chunk in r.iter_content(1 << 16):
        data += chunk
        if len(data) > MAX_BYTES:
            r.close()
            raise RuntimeError("refusing >60MB download: " + url)
    ctype = r.headers.get("content-type", "")
    if kind is None:
        if "pdf" in ctype or url.endswith(".pdf"):
            kind = "pdf"
        elif "html" in ctype:
            kind = "html"
        elif "json" in ctype:
            kind = "json"
        else:
            kind = "text"
    with open(path, "wb") as f:
        f.write(data)
    if kind == "pdf":
        subprocess.run(["pdftotext", "-layout", path, path + ".txt"], check=True)
        # also a non-layout rendering (better for running prose)
        subprocess.run(["pdftotext", path, path + ".raw.txt"], check=True)
    elif kind == "html":
        txt = html_to_text(data.decode("utf-8", "replace"))
        open(path + ".txt", "w").write(txt)
    else:
        open(path + ".txt", "w").write(data.decode("utf-8", "replace"))
    meta = {
        "url": url,
        "final_url": r.url,
        "http_status": r.status_code,
        "content_type": ctype,
        "kind": kind,
        "retrieved_utc": _now(),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "file": path,
    }
    json.dump(meta, open(meta_path, "w"), indent=1)
    time.sleep(0.5)
    return meta


def norm(s):
    s = s.replace(" ", " ").replace("­", "")
    # pdftotext hyphenation at line breaks is NOT repaired: quotes must match the saved text.
    return re.sub(r"\s+", " ", s).strip()


def texts_for(fname):
    path = os.path.join(SRC_DIR, fname)
    out = []
    for p in (path + ".txt", path + ".raw.txt"):
        if os.path.exists(p):
            out.append(open(p, encoding="utf-8", errors="replace").read())
    return out


def verify(quote, fname):
    q = norm(quote)
    for t in texts_for(fname):
        if q in norm(t):
            return True
    return False


def find(fname, pattern, width=300, maxn=10, flags=re.I):
    """Print whitespace-normalized context windows for regex pattern in a saved source."""
    ts = texts_for(fname)
    for t in ts[-1:]:  # for PDFs the non-layout rendering; otherwise the single text rendering
        t = norm(t)
        for i, m in enumerate(re.finditer(pattern, t, flags)):
            if i >= maxn:
                break
            a, b = max(0, m.start() - width), min(len(t), m.end() + width)
            print("...", t[a:b], "...\n")


def save_record(rec):
    """Validate every quote in rec, then write record and rebuild OUT_JSON."""
    bad = []
    for q in rec.get("quotes", []):
        ok = verify(q["quote"], q["source_file"])
        q["verified_whitespace_normalized"] = ok
        meta = json.load(open(os.path.join(SRC_DIR, q["source_file"]) + ".meta.json"))
        q["source_url"] = meta["url"]
        q["source_sha256"] = meta["sha256"]
        q["retrieved_utc"] = meta["retrieved_utc"]
        if not ok:
            bad.append(q["quote"][:120])
    if bad:
        print("UNVERIFIED QUOTES:", *bad, sep="\n  ")
        raise SystemExit(1)
    rec["record_written_utc"] = _now()
    json.dump(rec, open(os.path.join(REC_DIR, rec["id"] + ".json"), "w"), indent=1, ensure_ascii=False)
    assemble()
    print("saved", rec["id"], "quotes:", len(rec.get("quotes", [])))


def assemble():
    recs = []
    for p in sorted(glob.glob(os.path.join(REC_DIR, "*.json"))):
        r = json.load(open(p))
        for q in r.get("quotes", []):
            q["verified_whitespace_normalized"] = verify(q["quote"], q["source_file"])
        recs.append(r)
    out = {
        "task": "DECISION_003 sec.2 foundation-model selection rule -- SECONDARY candidates "
                "(generic video generative models / video tokenizers / video VAEs / masked video autoencoders)",
        "rule_source": "/home/user/projects/medical_video_causal_gate/decisions/DECISION_003.md sec.2",
        "rule_criteria": {
            "C1_open_weights": "the weights are publicly downloadable",
            "C2_licence_research_use": "Licence permits research use.",
            "C3_domain_secondary": "a generic video generative model (a generative or tokenizer/autoencoder video "
                                   "model trained on general video)",
            "C4_documented_pretraining_data": "a model card or paper lists the pretraining datasets or sources",
        },
        "judging_conventions": json.load(open(os.path.join(SRC_DIR, "conventions.json")))
        if os.path.exists(os.path.join(SRC_DIR, "conventions.json")) else {},
        "ds203": {
            "name": "Appendix300 (DS203)",
            "doi": "10.25532/OPARA-1173",
            "opara_dc_date_issued": "2026-04-29",
            "opara_metadata_file": "/media/user/LaCie/medvideo_gate/DS203/opara_item.json",
        },
        "source_copies_dir": SRC_DIR,
        "generated_utc": _now(),
        "n_candidates": len(recs),
        "all_quotes_verified": all(q["verified_whitespace_normalized"] for r in recs for q in r.get("quotes", [])),
        "candidates": recs,
    }
    tmp = OUT_JSON + ".tmp"
    json.dump(out, open(tmp, "w"), indent=1, ensure_ascii=False)
    os.replace(tmp, OUT_JSON)


if __name__ == "__main__":
    assemble()
    print("assembled", OUT_JSON)
