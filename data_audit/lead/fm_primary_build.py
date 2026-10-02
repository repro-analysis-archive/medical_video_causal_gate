"""Build fm_candidates_primary.json (DECISION_003 §2, PRIMARY domain: surgical/endoscopic video FMs).

Records live in fm_primary_records.py (appended one candidate at a time).  Every quote is
checked verbatim against the saved copy of its source (SAVE_DIR/<file>.txt) after whitespace
normalisation (runs of whitespace -> one space).  A record whose quote fails is still written
but flagged; the run prints all failures.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from fm_primary_records import RECORDS  # noqa: E402

SAVE_DIR = pathlib.Path("/media/user/LaCie/medvideo_gate/fm_candidates/primary")
OUT = pathlib.Path(__file__).parent / "out" / "fm_candidates_primary.json"
RULE = "/home/user/projects/medical_video_causal_gate/decisions/DECISION_003.md §2"


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


_cache = {}


def text_of(stem: str) -> str:
    if stem not in _cache:
        _cache[stem] = norm((SAVE_DIR / f"{stem}.txt").read_text(encoding="utf-8"))
    return _cache[stem]


def manifest():
    m = {}
    for line in (SAVE_DIR / "_manifest.jsonl").read_text().splitlines():
        e = json.loads(line)
        m[e["name"]] = e  # last fetch wins
    return m


def walk_quotes(obj, path=""):
    """Yield (path, quote-dict) for every {'quote':..., 'file':...} dict in a record."""
    if isinstance(obj, dict):
        if "quote" in obj and "file" in obj:
            yield path, obj
        for k, v in obj.items():
            yield from walk_quotes(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_quotes(v, f"{path}[{i}]")


def main():
    man = manifest()
    failures = []
    out = []
    for rec in RECORDS:
        rec = json.loads(json.dumps(rec))  # deep copy
        used = set()
        for path, q in walk_quotes(rec):
            stem = q["file"]
            used.add(stem)
            ok = norm(q["quote"]) in text_of(stem)
            q["verified_verbatim_ws_normalised"] = ok
            e = man.get(stem, {})
            q["source_url"] = e.get("url")
            q["saved_copy"] = str(SAVE_DIR / e.get("file", stem))
            if not ok:
                failures.append((rec["name"], path, stem, q["quote"][:90]))
        for stem in rec.get("extra_sources", []):
            used.add(stem)
        rec.pop("extra_sources", None)
        rec["sources"] = [
            {
                "url": man[s]["url"],
                "final_url": man[s]["final_url"],
                "http_status": man[s]["status"],
                "saved_copy": str(SAVE_DIR / man[s]["file"]),
                "text_copy": str(SAVE_DIR / man[s]["text_file"]),
                "sha256": man[s]["sha256"],
                "fetched_utc": man[s]["fetched_utc"],
            }
            for s in sorted(used)
            if s in man
        ]
        missing = sorted(s for s in used if s not in man)
        if missing:
            failures.append((rec["name"], "sources", ",".join(missing), "NOT IN MANIFEST"))
        out.append(rec)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {OUT} with {len(out)} candidates; quote/source failures: {len(failures)}")
    for f in failures:
        print("  FAIL", f)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
