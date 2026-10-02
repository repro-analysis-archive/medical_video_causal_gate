"""Save a copy of a source page (HTML / PDF / raw text / JSON API listing) for the
primary foundation-model candidate search (DECISION_003 §2).

Usage: fm_primary_fetch.py NAME URL [NAME URL ...]

For each URL: the raw bytes are saved to SAVE_DIR/NAME.<ext>, a whitespace-preserving
plain-text rendering to SAVE_DIR/NAME.txt (HTML -> visible text, PDF -> pdftotext), and a
manifest entry (url, final url, status, sha256, UTC time) is appended to SAVE_DIR/_manifest.jsonl.
No model weights are downloaded: URLs are pages, papers, READMEs, licences and API listings only.
"""
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

import requests
from bs4 import BeautifulSoup

SAVE_DIR = pathlib.Path("/media/user/LaCie/medvideo_gate/fm_candidates/primary")
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) research-audit (read-only)"}
MAX_BYTES = 60_000_000  # refuse anything large (no weights)


def to_text(raw: bytes, ctype: str, ext: str) -> str:
    if ext == ".pdf":
        tmp = SAVE_DIR / "_tmp.pdf"
        tmp.write_bytes(raw)
        out = subprocess.run(["pdftotext", str(tmp), "-"], capture_output=True).stdout.decode("utf-8", "replace")
        tmp.unlink()
        return out
    if ext in (".html", ".xml"):
        soup = BeautifulSoup(raw, "html.parser")
        for t in soup(["script", "style", "noscript"]):
            t.decompose()
        return soup.get_text(" ")
    return raw.decode("utf-8", "replace")


def fetch(name: str, url: str) -> None:
    r = requests.get(url, headers=UA, timeout=60, stream=True, allow_redirects=True)
    clen = int(r.headers.get("content-length") or 0)
    if clen > MAX_BYTES:
        print(f"SKIP {name}: content-length {clen} too large")
        return
    raw = r.raw.read(MAX_BYTES + 1, decode_content=True)
    if len(raw) > MAX_BYTES:
        print(f"SKIP {name}: body too large")
        return
    ctype = r.headers.get("content-type", "")
    if "pdf" in ctype or raw[:5] == b"%PDF-":
        ext = ".pdf"
    elif "json" in ctype:
        ext = ".json"
    elif "html" in ctype:
        ext = ".html"
    elif "xml" in ctype:
        ext = ".xml"
    else:
        ext = ".raw"
    raw_path = SAVE_DIR / f"{name}{ext}"
    raw_path.write_bytes(raw)
    txt = to_text(raw, ctype, ext)
    (SAVE_DIR / f"{name}.txt").write_text(txt, encoding="utf-8")
    entry = {
        "name": name,
        "url": url,
        "final_url": r.url,
        "status": r.status_code,
        "content_type": ctype,
        "file": raw_path.name,
        "text_file": f"{name}.txt",
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "fetched_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    }
    with open(SAVE_DIR / "_manifest.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")
    print(f"{r.status_code} {name}{ext} {len(raw)}B text={len(txt)}ch {r.url}")


if __name__ == "__main__":
    args = sys.argv[1:]
    assert len(args) % 2 == 0, "pairs of NAME URL"
    for i in range(0, len(args), 2):
        try:
            fetch(args[i], args[i + 1])
        except Exception as e:  # keep going; failure is printed
            print(f"FAIL {args[i]} {args[i+1]}: {e!r}")
