"""Stage the case video files of the 278-case representation set out of the split DS203 archive (orchestration only).

The locked pipeline reads FULL_VIDEOS_DIR/Center<c>/<any>/Center<c>_<op:03d>[_vNN].mp4. DS203 ships them as members of
a split ZIP archive with stored (uncompressed) entries, so staging is a byte copy: no frame is decoded, nothing is
re-encoded, and the copy is checked against the CRC-32 in the archive's central directory.

* Parts: <stem>.z01, <stem>.z02, … and <stem>.zip (the last part, holding the central directory). A member's data
  starts at the global offset CUM[disk] + local-header offset + 30 + name length + local extra length, as in
  data_audit/lead/probe_ds203_containers.py.
* Selection: members named Full_Videos/Center<c>/<dir>/Center<c>_<op:03d>[_vNN].mp4 for the (centre, op) pairs of
  design.representation_cases(); every case must have at least one member. Compressed members stop the run.
* I/O: one reader; members in archive order (sequential over the parts), 64 MiB reads, written to <name>.partial,
  fsynced, CRC-checked, then renamed. staged_manifest.json records each finished member; on resume finished members
  (present with the recorded size) are skipped. staged_plan.json holds the member count and bytes (for --status).
* Errors: an OSError is retried with backoff (5, 30, 120 s); a CRC mismatch is retried once from the start of the
  member; a repeated failure exits non-zero with a STOP message.

    python scripts/stage_ds203_videos.py --zip ARCHIVE.zip --dest STAGED_DIR
"""
import argparse
import json
import os
import re
import struct
import sys
import time
import zlib

CHUNK = 64 << 20
BACKOFF = (5, 30, 120)
MEMBER = re.compile(r"^Full_Videos/Center(\d)/[^/]+/Center(\d)_(\d{3})(?:_v(\d+))?\.mp4$")


class Parts:
    def __init__(self, zip_path):
        stem = zip_path[:-4]
        names, k = [], 1
        while os.path.exists(f"{stem}.z{k:02d}"):
            names.append(f"{stem}.z{k:02d}")
            k += 1
        names.append(zip_path)
        self.paths = names
        self.sizes = [os.path.getsize(p) for p in names]
        self.cum = [0]
        for s in self.sizes:
            self.cum.append(self.cum[-1] + s)
        self._fh = {}

    def _f(self, k):
        if k not in self._fh:
            self._fh[k] = open(self.paths[k], "rb", buffering=0)
        return self._fh[k]

    def read(self, gpos, n):
        out = bytearray()
        while n > 0:
            k = max(i for i in range(len(self.paths)) if self.cum[i] <= gpos)
            off = gpos - self.cum[k]
            m = min(n, self.sizes[k] - off)
            if m <= 0:
                raise OSError(f"read past the end of the archive at {gpos}")
            f = self._f(k)
            f.seek(off)
            b = f.read(m)
            if len(b) != m:
                raise OSError(f"short read in {self.paths[k]} at {off}")
            out += b
            gpos += m
            n -= m
        return bytes(out)

    def close(self):
        for f in self._fh.values():
            f.close()
        self._fh = {}


def central_directory(parts):
    zp = len(parts.paths) - 1
    size = parts.sizes[zp]
    tail = parts.read(parts.cum[zp] + max(0, size - 65558), min(size, 65558))
    i = tail.rfind(b"PK\x06\x07")
    if i >= 0:                                                       # ZIP64 end-of-central-directory locator
        disk_z64, off_z64, _ = struct.unpack("<IQI", tail[i + 4:i + 20])
        z = parts.read(parts.cum[disk_z64] + off_z64, 56)
        assert z[:4] == b"PK\x06\x06", "bad ZIP64 end of central directory"
        (cd_disk,) = struct.unpack("<I", z[20:24])
        (n_ent,) = struct.unpack("<Q", z[32:40])
        cd_size, cd_off = struct.unpack("<QQ", z[40:56])
    else:
        j = tail.rfind(b"PK\x05\x06")
        assert j >= 0, "no end of central directory"
        (cd_disk,) = struct.unpack("<H", tail[j + 6:j + 8])
        (n_ent,) = struct.unpack("<H", tail[j + 10:j + 12])
        cd_size, cd_off = struct.unpack("<II", tail[j + 12:j + 20])
    cd = parts.read(parts.cum[cd_disk] + cd_off, cd_size)
    ents, p = [], 0
    while p < len(cd) and cd[p:p + 4] == b"PK\x01\x02":
        (meth,) = struct.unpack("<H", cd[p + 10:p + 12])
        (crc,) = struct.unpack("<I", cd[p + 16:p + 20])
        csz, usz = struct.unpack("<II", cd[p + 20:p + 28])
        nl, el, cl, disk = struct.unpack("<HHHH", cd[p + 28:p + 36])
        (lho,) = struct.unpack("<I", cd[p + 42:p + 46])
        name = cd[p + 46:p + 46 + nl].decode("utf-8")
        ex = cd[p + 46 + nl:p + 46 + nl + el]
        q = 0
        while q + 4 <= len(ex):
            hid, hl = struct.unpack("<HH", ex[q:q + 4])
            body, r = ex[q + 4:q + 4 + hl], 0
            if hid == 1:
                if usz == 0xFFFFFFFF:
                    (usz,) = struct.unpack("<Q", body[r:r + 8]); r += 8
                if csz == 0xFFFFFFFF:
                    (csz,) = struct.unpack("<Q", body[r:r + 8]); r += 8
                if lho == 0xFFFFFFFF:
                    (lho,) = struct.unpack("<Q", body[r:r + 8]); r += 8
                if disk == 0xFFFF:
                    (disk,) = struct.unpack("<I", body[r:r + 4])
            q += 4 + hl
        ents.append(dict(name=name, method=meth, crc32=crc, csz=csz, usz=usz, disk=disk, lho=lho))
        p += 46 + nl + el + cl
    assert len(ents) == n_ent, (len(ents), n_ent)
    return ents


def wanted_members(ents, cases):
    want = {(int(c), int(cid.split("_")[1])) for cid, c in zip(cases.case_id, cases.center)}
    sel, covered = [], set()
    for e in ents:
        m = MEMBER.match(e["name"])
        if m and m.group(1) == m.group(2) and (int(m.group(1)), int(m.group(3))) in want:
            if e["method"] != 0 or e["csz"] != e["usz"]:
                raise SystemExit(f"STOP: member is compressed, not stored: {e['name']}")
            sel.append(e)
            covered.add((int(m.group(1)), int(m.group(3))))
    missing = sorted(want - covered)
    if missing:
        raise SystemExit(f"STOP: {len(missing)} cases have no member in the archive, e.g. {missing[:3]}")
    return sel


def data_offset(parts, e):
    g = parts.cum[e["disk"]] + e["lho"]
    h = parts.read(g, 30)
    if h[:4] != b"PK\x03\x04":
        raise OSError(f"bad local header for {e['name']}")
    nl, el = struct.unpack("<HH", h[26:30])
    if parts.read(g + 30, nl).decode("utf-8") != e["name"]:
        raise OSError(f"local header name differs for {e['name']}")
    return g + 30 + nl + el


def copy_member(parts, e, dest, log):
    out = os.path.join(dest, e["name"])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = out + ".partial"
    for crc_try in range(2):
        for k in range(len(BACKOFF) + 1):
            try:
                start = data_offset(parts, e)
                crc, done = 0, 0
                with open(tmp, "wb") as o:
                    while done < e["usz"]:
                        b = parts.read(start + done, min(CHUNK, e["usz"] - done))
                        crc = zlib.crc32(b, crc)
                        o.write(b)
                        done += len(b)
                    o.flush()
                    os.fsync(o.fileno())
                break
            except OSError as err:
                parts.close()
                if k == len(BACKOFF):
                    raise SystemExit(f"STOP: repeated I/O failure staging {e['name']}: {err!r}")
                log(f"I/O error staging {e['name']} ({err!r}); retry in {BACKOFF[k]} s")
                time.sleep(BACKOFF[k])
        if crc == e["crc32"]:
            os.replace(tmp, out)
            return
        log(f"CRC-32 mismatch for {e['name']} (attempt {crc_try + 1})")
    os.remove(tmp)
    raise SystemExit(f"STOP: repeated CRC-32 mismatch staging {e['name']}")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", required=True)
    ap.add_argument("--dest", required=True)
    a = ap.parse_args(argv)
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from ss_benchmark import design

    man_p = os.path.join(a.dest, "staged_manifest.json")
    man = json.load(open(man_p)) if os.path.exists(man_p) else {}

    def log(msg):
        print(time.strftime("%Y-%m-%d %H:%M:%S"), msg, flush=True)

    parts = Parts(a.zip)
    sel = wanted_members(central_directory(parts), design.representation_cases())
    sel.sort(key=lambda e: parts.cum[e["disk"]] + e["lho"])
    total = sum(e["usz"] for e in sel)
    os.makedirs(a.dest, exist_ok=True)
    json.dump(dict(members=len(sel), bytes_total=total, archive=os.path.basename(a.zip)),
              open(os.path.join(a.dest, "staged_plan.json"), "w"), indent=1)
    need = sum(e["usz"] for e in sel if e["name"] not in man)
    free = os.statvfs(a.dest).f_bavail * os.statvfs(a.dest).f_frsize
    if free < need + (50 << 30):
        raise SystemExit(f"STOP: free space {free} B < bytes still to stage {need} B + 50 GiB margin")
    log(f"staging {len(sel)} members, {total} B ({len(man)} already staged)")
    t0 = time.time()
    for i, e in enumerate(sel):
        out = os.path.join(a.dest, e["name"])
        if e["name"] in man and os.path.exists(out) and os.path.getsize(out) == e["usz"]:
            continue
        copy_member(parts, e, a.dest, log)
        man[e["name"]] = dict(bytes=e["usz"], crc32=f"{e['crc32']:08x}", disk=e["disk"], local_header_offset=e["lho"])
        tmp = man_p + ".tmp"
        json.dump(man, open(tmp, "w"), indent=1, sort_keys=True)
        os.replace(tmp, man_p)
        log(f"staged {len(man)}/{len(sel)} members ({time.time() - t0:.0f} s)")
    parts.close()
    log("staging complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
