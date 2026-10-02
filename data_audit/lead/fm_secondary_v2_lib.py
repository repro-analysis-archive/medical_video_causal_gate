"""Helpers for the DECISION_003 sec.2 / DECISION_004 sec.3 SECONDARY foundation-model candidate survey, revision 2.

All source copies are saved under SRC_DIR on /home (never on /media/user/LaCie):
  SRC_DIR/<fname>            plain-text rendering (HTML -> BeautifulSoup get_text(" "); PDF -> pdftotext, non-layout;
                             markdown / JSON / plain text saved as served).  Each copy must be < 2 MB.
  SRC_DIR/<fname>.layout.txt PDF only: pdftotext -layout rendering (a second rendering used for verification).
  SRC_DIR/_meta/<fname>.json sidecar: url, final url, status, content type, raw sha256/bytes, text sha256, UTC time.
Raw PDF/HTML bytes are NOT kept (only hashed); PDFs pass through the session scratchpad and are deleted.
No model weights are downloaded: only documentation pages, papers, READMEs, configs, licences and HF API listings.

Quote verification: a quote passes if norm(quote) is a substring of norm(saved copy), where norm() maps NBSP to space,
drops soft hyphens and collapses whitespace runs (PDF line-break hyphenation is not repaired).
"""
import datetime
import glob
import hashlib
import json
import os
import re
import subprocess
import tempfile
import time

import requests
from bs4 import BeautifulSoup

LEAD = "/home/user/projects/medical_video_causal_gate/data_audit/lead"
SRC_DIR = os.path.join(LEAD, "fm_sources", "secondary")
META_DIR = os.path.join(SRC_DIR, "_meta")
REC_DIR = os.path.join(LEAD, "fm_secondary_v2_records", "json")
CONV_V1 = os.path.join(LEAD, "fm_secondary_v2_records", "conventions_v1.json")
CONV_V2 = os.path.join(LEAD, "fm_secondary_v2_records", "conventions_v2.json")
PREV_OUT = os.path.join(LEAD, "fm_secondary_v2_records", "previous_output_v1.json")
OUT_JSON = os.path.join(LEAD, "out", "fm_candidates_secondary.json")
SCRATCH = "/tmp/claude-1000/-home-user/8e61e1d1-14de-446a-a848-8bd699ca6e04/scratchpad"
UA = "Mozilla/5.0 (X11; Linux x86_64) research-audit (documentation pages only)"
MAX_RAW = 40 * 1024 * 1024      # refuse anything larger (no weights)
MAX_COPY = 2 * 1024 * 1024 - 1  # each saved copy must be < 2 MB

assert "LaCie" not in SRC_DIR and "/media/" not in SRC_DIR
os.makedirs(META_DIR, exist_ok=True)
os.makedirs(REC_DIR, exist_ok=True)

MED_TERMS = r"medical|surgical|surgery|endoscop|laparoscop|clinical|health|hospital"
A300_TERMS = r"appendix ?300|DS203|OPARA|appendectom|appendic"


def _now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def html_to_text(raw):
    soup = BeautifulSoup(raw, "html.parser")
    for t in soup(["script", "style", "noscript", "svg"]):
        t.decompose()
    return soup.get_text(" ")


def copy_path(fname):
    return os.path.join(SRC_DIR, fname)


def meta(fname):
    return json.load(open(os.path.join(META_DIR, fname + ".json")))


def fetch(url, fname, kind=None, force=False, json_pretty=False):
    """Fetch url; save a text rendering to SRC_DIR/fname. kind in {html, pdf, text, json}; inferred if None."""
    assert "/" not in fname
    mp = os.path.join(META_DIR, fname + ".json")
    if os.path.exists(mp) and not force:
        return json.load(open(mp))
    r = requests.get(url, headers={"User-Agent": UA}, timeout=120, stream=True, allow_redirects=True)
    data = b""
    for chunk in r.iter_content(1 << 16):
        data += chunk
        if len(data) > MAX_RAW:
            r.close()
            raise RuntimeError("refusing >40MB download: " + url)
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
    texts = {}
    if kind == "pdf":
        fd, tmp = tempfile.mkstemp(suffix=".pdf", dir=SCRATCH)
        os.write(fd, data)
        os.close(fd)
        texts[fname] = subprocess.run(["pdftotext", tmp, "-"], capture_output=True, check=True).stdout.decode("utf-8", "replace")
        texts[fname + ".layout.txt"] = subprocess.run(["pdftotext", "-layout", tmp, "-"], capture_output=True, check=True).stdout.decode("utf-8", "replace")
        os.unlink(tmp)
    elif kind == "html":
        texts[fname] = html_to_text(data.decode("utf-8", "replace"))
    elif kind == "json" and json_pretty:
        texts[fname] = json.dumps(json.loads(data), indent=1, ensure_ascii=False)
    else:
        texts[fname] = data.decode("utf-8", "replace")
    out_meta = {
        "url": url, "final_url": r.url, "http_status": r.status_code, "content_type": ctype, "kind": kind,
        "retrieved_utc": _now(), "raw_bytes": len(data), "raw_sha256": hashlib.sha256(data).hexdigest(),
        "copies": {},
    }
    for fn, t in texts.items():
        b = t.encode("utf-8")
        if len(b) > MAX_COPY:
            raise RuntimeError(f"text rendering {fn} is {len(b)} bytes (>= 2 MB); not saved")
        open(copy_path(fn), "wb").write(b)
        out_meta["copies"][fn] = {"path": copy_path(fn), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
    json.dump(out_meta, open(mp, "w"), indent=1)
    time.sleep(0.3)
    return out_meta


def hf_api(repo, prefix):
    """Save the HF API model listing (metadata only; ?blobs=true gives file sizes). Returns parsed JSON."""
    fname = f"{prefix}_{repo.replace('/', '__')}_hfapi.json"
    m = fetch(f"https://huggingface.co/api/models/{repo}?blobs=true", fname, kind="json", json_pretty=True)
    return fname, json.load(open(copy_path(fname))), m


def head_check(url, fname):
    """For weights hosted outside HF: HTTP HEAD only (no body is transferred). Saves status + headers as a text copy."""
    assert "/" not in fname
    mp = os.path.join(META_DIR, fname + ".json")
    if os.path.exists(mp):
        return json.load(open(copy_path(fname)))
    r = requests.head(url, headers={"User-Agent": UA}, timeout=60, allow_redirects=True)
    rec = {"head_request_url": url, "final_url": r.url, "http_status": r.status_code,
           "headers": {k: v for k, v in r.headers.items()},
           "redirect_chain": [h.url for h in r.history], "retrieved_utc": _now(),
           "note": "HTTP HEAD only; no file body was downloaded"}
    t = json.dumps(rec, indent=1)
    open(copy_path(fname), "w").write(t)
    b = t.encode()
    json.dump({"url": url, "final_url": r.url, "http_status": r.status_code, "content_type": "HEAD response",
               "kind": "head", "retrieved_utc": rec["retrieved_utc"], "raw_bytes": 0,
               "raw_sha256": hashlib.sha256(b).hexdigest(),
               "copies": {fname: {"path": copy_path(fname), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}}},
              open(mp, "w"), indent=1)
    return rec


def norm(s):
    s = s.replace(" ", " ").replace("­", "")
    return re.sub(r"\s+", " ", s).strip()


def renderings(fname):
    out = []
    for fn in (fname, fname + ".layout.txt"):
        p = copy_path(fn)
        if os.path.exists(p):
            out.append((p, open(p, encoding="utf-8", errors="replace").read()))
    return out


def verify(quote, fname):
    """Return the saved-copy path in which norm(quote) is found, or None."""
    q = norm(quote)
    for p, t in renderings(fname):
        if q in norm(t):
            return p
    return None


def find(fname, pattern, width=250, maxn=8, flags=re.I):
    """Print whitespace-normalized context windows for a regex in a saved copy (exploration helper)."""
    p, t = renderings(fname)[0]
    t = norm(t)
    n = 0
    for m in re.finditer(pattern, t, flags):
        if n >= maxn:
            break
        a, b = max(0, m.start() - width), min(len(t), m.end() + width)
        print("...", t[a:b], "...\n")
        n += 1
    if n == 0:
        print("[no hit]", pattern, "in", fname)


def term_search(fnames, pattern, width=90, maxn=6):
    """Automated term search across saved copies; returns {file: [snippets]} (empty list = no hit)."""
    res = {}
    for fn in fnames:
        p, t = renderings(fn)[0]
        t = norm(t)
        hits = []
        for m in re.finditer(pattern, t, re.I):
            a, b = max(0, m.start() - width), min(len(t), m.end() + width)
            hits.append(t[a:b])
            if len(hits) >= maxn:
                break
        res[copy_path(fn)] = hits
    return res


def _resolve(obj, qmap):
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            if k == "quote_ids":
                missing = [i for i in v if i not in qmap]
                if missing:
                    raise SystemExit(f"unknown quote ids {missing}")
                obj["quotes"] = [{"id": i, "quote": qmap[i]["quote"], "source_url": qmap[i]["source_url"],
                                  "copy_path": qmap[i]["copy_path"]} for i in v]
            elif k != "quotes":
                _resolve(v, qmap)
    elif isinstance(obj, list):
        for v in obj:
            _resolve(v, qmap)


REQUIRED = ["id", "name", "version", "weights_location", "licence", "domain", "pretraining_data_quote",
            "appendix300_check", "input", "embedding_dim", "params", "flops_per_input_if_documented", "eligibility",
            "quotes"]
INPUT_KEYS = ["frame_size", "frame_rate_or_sampling", "clip_length_frames", "temporal_compression", "spatial_compression"]


def save_record(rec, prev_quotes=None):
    """Verify every quote against its saved copy, resolve quote_ids, write record JSON, re-assemble OUT_JSON.
    prev_quotes: optional {quote_id: v1 quote dict} to record the v1 source sha256 for comparison."""
    for k in REQUIRED:
        assert k in rec, f"missing field {k}"
    for k in INPUT_KEYS:
        assert k in rec["input"], f"missing input.{k}"
    bad = []
    qmap = {}
    for q in rec["quotes"]:
        assert q["id"] not in qmap, "duplicate quote id " + q["id"]
        m = meta(q["source_file"])
        p = verify(q["quote"], q["source_file"])
        q["verified_whitespace_normalized"] = p is not None
        q["copy_path"] = p or copy_path(q["source_file"])
        q["source_url"] = m["url"]
        q["final_url"] = m["final_url"]
        q["raw_sha256"] = m["raw_sha256"]
        q["copy_sha256"] = m["copies"][os.path.basename(q["copy_path"])]["sha256"]
        q["retrieved_utc"] = m["retrieved_utc"]
        if prev_quotes and q["id"] in prev_quotes:
            pq = prev_quotes[q["id"]]
            q["v1_source_sha256"] = pq.get("source_sha256")
            q["raw_sha256_equals_v1"] = pq.get("source_sha256") == m["raw_sha256"]
        if p is None:
            bad.append(f"{q['id']}: {q['quote'][:140]}")
        qmap[q["id"]] = q
    if bad:
        print("UNVERIFIED QUOTES:", *bad, sep="\n  ")
        raise SystemExit(1)
    _resolve({k: v for k, v in rec.items() if k != "quotes"}, qmap)
    rec["all_quotes_verified"] = True
    rec["record_written_utc"] = _now()
    json.dump(rec, open(os.path.join(REC_DIR, rec["id"] + ".json"), "w"), indent=1, ensure_ascii=False)
    assemble()
    print("saved", rec["id"], "quotes:", len(rec["quotes"]), "eligible:", rec["eligibility"].get("eligible"))


def save_screened(items, tag):
    """Screened-but-not-added candidates (e.g. no official weights, image-only tokenizer). Every quote is verified."""
    bad = []
    for it in items:
        for k in ("name", "reason_not_added", "quotes"):
            assert k in it, f"screened item missing {k}"
        for q in it["quotes"]:
            m = meta(q["source_file"])
            p = verify(q["quote"], q["source_file"])
            q["verified_whitespace_normalized"] = p is not None
            q["copy_path"] = p or copy_path(q["source_file"])
            q["source_url"] = m["url"]
            q["raw_sha256"] = m["raw_sha256"]
            q["retrieved_utc"] = m["retrieved_utc"]
            if p is None:
                bad.append(f"{it['name']}: {q['quote'][:140]}")
    if bad:
        print("UNVERIFIED QUOTES:", *bad, sep="\n  ")
        raise SystemExit(1)
    json.dump(items, open(os.path.join(LEAD, "fm_secondary_v2_records", f"screened_not_added_{tag}.json"), "w"),
              indent=1, ensure_ascii=False)
    assemble()
    print("saved screened", tag, len(items))


def prev_candidate(cid):
    d = json.load(open(PREV_OUT))
    for c in d["candidates"]:
        if c["id"] == cid:
            return c
    raise KeyError(cid)


def assemble():
    recs = []
    for p in sorted(glob.glob(os.path.join(REC_DIR, "*.json"))):
        r = json.load(open(p))
        for q in r.get("quotes", []):
            q["verified_whitespace_normalized"] = verify(q["quote"], q["source_file"]) is not None
        r["revision_status"] = r.get("revision_status", "revision 2 record (all quotes re-verified against /home copies)")
        recs.append(r)
    prev = json.load(open(PREV_OUT))
    done = {r["id"] for r in recs}
    pending = []
    for c in prev["candidates"]:  # keep every v1 entry in the merged file until its revision-2 record exists
        if c["id"] not in done:
            c = dict(c)
            c["revision_status"] = ("v1 entry carried over unchanged; NOT yet re-verified in revision 2 "
                                    "(its source copies are on LaCie, not accessed)")
            pending.append(c)
    recs = sorted(recs + pending, key=lambda r: r["id"])
    conv = json.load(open(CONV_V2)) if os.path.exists(CONV_V2) else {"judging_conventions": json.load(open(CONV_V1))}
    out = {
        "task": prev["task"],
        "rule_source": prev["rule_source"],
        "rule_source_repeat": "/home/user/projects/medical_video_causal_gate/decisions/DECISION_004.md sec.3 (identical rule)",
        "rule_criteria": prev["rule_criteria"],
        "judging_conventions": conv["judging_conventions"],
        "judging_conventions_note": conv.get("judging_conventions_note", ""),
        "judging_conventions_clarifications_v2": conv.get("judging_conventions_clarifications_v2", {}),
        "structured_field_conventions": conv.get("structured_field_conventions", {}),
        "revision_log": conv.get("revision_log", []),
        "ds203": prev["ds203"],
        "source_copies_dir": SRC_DIR,
        "source_copies_note": "Revision 2 re-fetched every source into this /home directory as plain-text renderings "
                              "(< 2 MB each; sidecar metadata in _meta/). The v1 copies on "
                              "/media/user/LaCie/medvideo_gate/fm_candidates/secondary were NOT read or touched.",
        "previous_version": {"file": PREV_OUT, "generated_utc": prev["generated_utc"], "n_candidates": prev["n_candidates"]},
        "generated_utc": _now(),
        "n_candidates": len(recs),
        "eligible_candidates": [r["id"] for r in recs if str(r["eligibility"].get("eligible", "")).startswith("YES")],
        "n_pending_v1_entries": len(pending),
        "all_quotes_verified": (not pending) and all(q["verified_whitespace_normalized"] for r in recs for q in r.get("quotes", [])),
        "candidates": recs,
    }
    screened = []
    for p in sorted(glob.glob(os.path.join(LEAD, "fm_secondary_v2_records", "screened_not_added*.json"))):
        screened.extend(json.load(open(p)))
    out["screened_not_added"] = screened
    tmp = OUT_JSON + f".tmp{os.getpid()}"
    json.dump(out, open(tmp, "w"), indent=1, ensure_ascii=False)
    os.replace(tmp, OUT_JSON)


if __name__ == "__main__":
    assemble()
    print("assembled", OUT_JSON)
