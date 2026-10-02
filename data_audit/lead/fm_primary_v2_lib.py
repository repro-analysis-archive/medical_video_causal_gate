"""Source capture + quote verification for the PRIMARY foundation-model candidate survey
(DECISION_003 §2 / DECISION_004 §3), version 2.

All saved copies live under SAVE_DIR (inside the project, never on /media/user/LaCie).  Only TEXT
renderings are kept (HTML -> visible text, PDF -> pdftotext, Markdown/JSON/code -> as served),
each capped at 2 MB.  Raw bytes are not kept; their sha256 is logged in SAVE_DIR/_manifest.jsonl.
No model weights are downloaded: fetch() refuses bodies > 60 MB and is only pointed at
documentation pages, papers, READMEs, licences and API listings; linkcheck() sends HEAD and only
reads a body if it is an HTML/JSON/text landing page.

CLI:
  fm_primary_v2_lib.py fetch NAME URL [NAME URL ...]
  fm_primary_v2_lib.py linkcheck NAME URL [NAME URL ...]
  fm_primary_v2_lib.py grep NAME REGEX [WIDTH]      # search the normalised saved text
"""
import datetime
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import tempfile

import requests
from bs4 import BeautifulSoup

SAVE_DIR = pathlib.Path("/home/user/projects/medical_video_causal_gate/data_audit/lead/fm_sources/primary")
SAVE_DIR.mkdir(parents=True, exist_ok=True)
MANIFEST = SAVE_DIR / "_manifest.jsonl"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) research-audit (read-only documentation)"}
MAX_BYTES = 60_000_000
MAX_TEXT = 2_000_000 - 200  # keep each saved copy < 2 MB
assert not str(SAVE_DIR).startswith("/media/user/LaCie")


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def to_text(raw: bytes, ctype: str, url: str) -> tuple[str, str]:
    if "pdf" in ctype or raw[:5] == b"%PDF-":
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(raw)
            tmp.flush()
            out = subprocess.run(["pdftotext", tmp.name, "-"], capture_output=True).stdout
        return out.decode("utf-8", "replace"), "pdf->pdftotext"
    if "html" in ctype or ("xml" in ctype and "fullTextXML" in url):
        soup = BeautifulSoup(raw, "html.parser")
        for t in soup(["script", "style", "noscript", "svg"]):
            t.decompose()
        return soup.get_text(" "), "html->visible text"
    return raw.decode("utf-8", "replace"), "as served (text/markdown/json/code)"


def _write(name: str, text: str, meta: dict) -> None:
    truncated = False
    enc = text.encode("utf-8")
    if len(enc) > MAX_TEXT:
        text = enc[:MAX_TEXT].decode("utf-8", "ignore")
        truncated = True
    path = SAVE_DIR / f"{name}.txt"
    path.write_text(text, encoding="utf-8")
    meta.update({"name": name, "text_file": str(path), "text_bytes": path.stat().st_size,
                 "text_truncated_to_2MB": truncated, "fetched_utc": now()})
    with open(MANIFEST, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(meta, ensure_ascii=False) + "\n")


def fetch(name: str, url: str, headers=None) -> None:
    h = dict(UA, **(headers or {}))
    r = requests.get(url, headers=h, timeout=90, stream=True, allow_redirects=True)
    clen = int(r.headers.get("content-length") or 0)
    if clen > MAX_BYTES:
        r.close()
        print(f"SKIP {name}: content-length {clen} too large")
        return
    raw = r.raw.read(MAX_BYTES + 1, decode_content=True)
    r.close()
    if len(raw) > MAX_BYTES:
        print(f"SKIP {name}: body too large")
        return
    ctype = r.headers.get("content-type", "")
    text, how = to_text(raw, ctype, url)
    _write(name, text, {"kind": "fetch", "url": url, "final_url": r.url, "status": r.status_code,
                        "content_type": ctype, "raw_bytes": len(raw),
                        "raw_sha256": hashlib.sha256(raw).hexdigest(), "rendering": how})
    print(f"{r.status_code} {name} raw={len(raw)}B text={len(text)}ch {r.url}")


def linkcheck(name: str, url: str) -> None:
    r = requests.head(url, headers=UA, timeout=60, allow_redirects=True)
    ctype = r.headers.get("content-type", "")
    if r.status_code in (403, 404, 405) or any(t in ctype for t in ("html", "json", "text/plain")):
        g = requests.get(url, headers=UA, timeout=60, stream=True, allow_redirects=True)
        if any(t in g.headers.get("content-type", "") for t in ("html", "json", "text/plain")):
            r = g
        else:
            g.close()
    ctype = r.headers.get("content-type", "")
    rec = {"url": url, "final_url": r.url, "status": r.status_code,
           "redirect_chain": [x.headers.get("location") for x in r.history],
           "content_type": ctype, "content_length": r.headers.get("content-length"),
           "content_disposition": r.headers.get("content-disposition"),
           "x_linked_size": r.headers.get("x-linked-size"), "body_read": False}
    if any(t in ctype for t in ("html", "json", "text/plain")):
        body = r.raw.read(2_000_000, decode_content=True)
        rec["body_read"] = True
        if "html" in ctype:
            soup = BeautifulSoup(body, "html.parser")
            rec["html_title"] = soup.title.get_text(" ", strip=True) if soup.title else None
    r.close()
    txt = json.dumps(rec, indent=1, ensure_ascii=False)
    _write(name, txt, {"kind": "linkcheck (HEAD; weights not downloaded)", "url": url, "final_url": r.url,
                       "status": r.status_code, "content_type": ctype,
                       "raw_sha256": hashlib.sha256(txt.encode()).hexdigest(), "rendering": "header record json"})
    print(json.dumps({k: rec.get(k) for k in ("status", "final_url", "content_type", "content_length",
                                               "content_disposition", "x_linked_size", "html_title")},
                     ensure_ascii=False))


def save_text(name: str, text: str, url: str, note: str) -> None:
    """Save a text compiled by this audit from several API responses (e.g. oEmbed metadata)."""
    _write(name, text, {"kind": "compiled", "url": url, "final_url": url, "status": 200,
                        "content_type": "text/plain", "raw_sha256": hashlib.sha256(text.encode()).hexdigest(),
                        "rendering": note})


def manifest() -> dict:
    m = {}
    if MANIFEST.exists():
        for line in MANIFEST.read_text(encoding="utf-8").splitlines():
            e = json.loads(line)
            m[e["name"]] = e  # last capture wins
    return m


_cache: dict = {}


def text_of(name: str) -> str:
    if name not in _cache:
        _cache[name] = norm((SAVE_DIR / f"{name}.txt").read_text(encoding="utf-8"))
    return _cache[name]


def grep(name: str, pat: str, width: int = 160) -> None:
    t = text_of(name)
    n = 0
    for mm in re.finditer(pat, t, flags=re.I):
        s = max(0, mm.start() - width)
        print(f"--[{mm.start()}] ...{t[s:mm.end() + width]}...")
        n += 1
        if n >= 12:
            break
    print(f"({n} shown) len={len(t)}")


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd in ("fetch", "linkcheck"):
        fn = fetch if cmd == "fetch" else linkcheck
        for i in range(0, len(args), 2):
            try:
                fn(args[i], args[i + 1])
            except Exception as e:
                print(f"FAIL {args[i]} {args[i + 1]}: {e!r}")
    elif cmd == "grep":
        grep(args[0], args[1], int(args[2]) if len(args) > 2 else 160)
