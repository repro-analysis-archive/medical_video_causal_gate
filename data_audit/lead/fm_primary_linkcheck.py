"""Check that a weights link resolves WITHOUT downloading the weights.

Usage: fm_primary_linkcheck.py NAME URL [NAME URL ...]

Sends a HEAD request (GET only for HTML/JSON/text landing pages), records status / final URL / redirect chain / content-type /
content-length / content-disposition, and closes the connection.  The body is read (max 2 MB)
only if it is an HTML/JSON/text page (a landing or preview page, never a binary).  The header
record is saved as SAVE_DIR/NAME.json (+ .txt for quote checks) and logged in _manifest.jsonl.
"""
import datetime
import hashlib
import json
import pathlib
import sys

import requests
from bs4 import BeautifulSoup

SAVE_DIR = pathlib.Path("/media/user/LaCie/medvideo_gate/fm_candidates/primary")
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) research-audit (read-only)"}


def check(name, url):
    # HEAD first: never transfers a body.  Only if the target is an HTML/JSON/text page
    # (landing/preview page) is a GET issued to read its title.
    r = requests.head(url, headers=UA, timeout=60, allow_redirects=True)
    ctype = r.headers.get("content-type", "")
    if r.status_code in (403, 404, 405) or any(t in ctype for t in ("html", "json", "text/plain")):
        g = requests.get(url, headers=UA, timeout=60, stream=True, allow_redirects=True)
        if any(t in g.headers.get("content-type", "") for t in ("html", "json", "text/plain")):
            r = g
        else:
            g.close()
    ctype = r.headers.get("content-type", "")
    rec = {
        "url": url,
        "final_url": r.url,
        "status": r.status_code,
        "redirect_chain": [h.headers.get("location") for h in r.history],
        "content_type": ctype,
        "content_length": r.headers.get("content-length"),
        "content_disposition": r.headers.get("content-disposition"),
        "x_linked_size": r.headers.get("x-linked-size"),
        "x_linked_etag": r.headers.get("x-linked-etag"),
        "body_read": False,
    }
    if any(t in ctype for t in ("html", "json", "text/plain")):
        body = r.raw.read(2_000_000, decode_content=True)
        rec["body_read"] = True
        if "html" in ctype:
            soup = BeautifulSoup(body, "html.parser")
            rec["html_title"] = soup.title.get_text(" ", strip=True) if soup.title else None
    r.close()
    raw = json.dumps(rec, indent=1, ensure_ascii=False).encode()
    (SAVE_DIR / f"{name}.json").write_bytes(raw)
    (SAVE_DIR / f"{name}.txt").write_text(raw.decode(), encoding="utf-8")
    entry = {
        "name": name, "url": url, "final_url": r.url, "status": r.status_code, "content_type": ctype,
        "file": f"{name}.json", "text_file": f"{name}.txt", "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "fetched_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "kind": "linkcheck (headers only, weights not downloaded)",
    }
    with open(SAVE_DIR / "_manifest.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")
    print(json.dumps({k: rec[k] for k in ("status", "final_url", "content_type", "content_length", "content_disposition", "x_linked_size")} | {"title": rec.get("html_title")}, ensure_ascii=False))


if __name__ == "__main__":
    a = sys.argv[1:]
    for i in range(0, len(a), 2):
        try:
            check(a[i], a[i + 1])
        except Exception as e:
            print(f"FAIL {a[i]}: {e!r}")
