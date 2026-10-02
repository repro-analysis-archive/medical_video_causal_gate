"""Semantic Scholar client for the gate's S2 arms (investigator instruction 2026-10-02):
- API key read at call time from ~/.config/s2/key, sent only as the x-api-key header; never printed, logged or stored.
- At most 1 request per second (>= 1.05 s between request starts).
- On HTTP 429 or 5xx: retry after 2, 4, 8, 16, 32 s; if the 6th attempt fails, raise S2Stop (stop and report).
- Every string that reaches a log passes through scrub(), which removes the key if it ever appears."""
import json, os, time, urllib.error, urllib.request
KEY_PATH = os.path.expanduser("~/.config/s2/key"); BACKOFF = (2, 4, 8, 16, 32); MIN_GAP = 1.05
_last = [0.0]
class S2Stop(RuntimeError): pass
def _key():
    with open(KEY_PATH) as f: return f.read().strip()
def scrub(s):
    s = str(s); k = _key(); return s.replace(k, "[REDACTED]") if k else s
def get(url, log=print):
    for attempt in range(len(BACKOFF) + 1):
        wait = _last[0] + MIN_GAP - time.time()
        if wait > 0: time.sleep(wait)
        _last[0] = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "gate-audit/1.0", "x-api-key": _key()})
            with urllib.request.urlopen(req, timeout=90) as r: return json.load(r)
        except urllib.error.HTTPError as e:
            code = e.code
            if code == 429 or 500 <= code < 600:
                if attempt < len(BACKOFF): log(scrub(f"HTTP {code}; retry in {BACKOFF[attempt]} s")); time.sleep(BACKOFF[attempt]); continue
                raise S2Stop(scrub(f"HTTP {code} after {len(BACKOFF)} retries: {url}"))
            return {"error": code}
        except Exception as e:                                                       # noqa: BLE001  (network error: same schedule)
            if attempt < len(BACKOFF): log(scrub(f"ERR {type(e).__name__}; retry in {BACKOFF[attempt]} s")); time.sleep(BACKOFF[attempt]); continue
            raise S2Stop(scrub(f"{type(e).__name__} after {len(BACKOFF)} retries: {url}"))
def status_only(url):
    """Single request; returns the HTTP status code only (key verification)."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "gate-audit/1.0", "x-api-key": _key()})
        with urllib.request.urlopen(req, timeout=60) as r: return r.status
    except urllib.error.HTTPError as e: return e.code
