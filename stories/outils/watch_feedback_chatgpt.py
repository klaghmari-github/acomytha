#!/usr/bin/env python3
"""Veille de gestion_projet/feedback_chatgpt/ (F-NAR-017).

Surveille le worktree ET le clone SSD (là où les fichiers sont déposés).
watch utilise inotify Linux (réveil immédiat), sinon poll 2 s.

scan / claim / done / watch
"""

from __future__ import annotations

import argparse
import ctypes
import fcntl
import hashlib
import json
import os
import select
import shutil
import struct
import sys
import time
from pathlib import Path

LIBC = ctypes.CDLL("libc.so.6", use_errno=True)
LIBC.inotify_init.restype = ctypes.c_int
LIBC.inotify_add_watch.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_uint32]
LIBC.inotify_add_watch.restype = ctypes.c_int

ROOT = Path(__file__).resolve().parents[2]
FEED = ROOT / "gestion_projet" / "feedback_chatgpt"
SSD_FEED = Path("/media/laghmari/ssd-data/dev/akomytha/gestion_projet/feedback_chatgpt")
LEDGER = FEED / "processed.json"
LOCK = FEED / "processed.json.lock"

IGNORE_NAMES = {
    "processed.json",
    "processed.json.lock",
    "NOTES.md",
    "AGENT.md",
    "README.md",
}
IGNORE_SUFFIXES = {".py", ".pyc", ".swp", ".tmp"}
OK_SUFFIXES = {".txt", ".md", ".html", ".pdf"}

IN_CLOSE_WRITE = 0x00000008
IN_MOVED_TO = 0x00000080
IN_CREATE = 0x00000100
IN_MASK = IN_CLOSE_WRITE | IN_MOVED_TO | IN_CREATE
EVENT_HDR = struct.Struct("iIII")


def watch_dirs() -> list[Path]:
    dirs = [FEED]
    try:
        if SSD_FEED.is_dir() and SSD_FEED.resolve() != FEED.resolve():
            dirs.append(SSD_FEED)
    except OSError:
        pass
    return dirs


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def list_candidates(folder: Path) -> list[Path]:
    if not folder.is_dir():
        return []
    out = []
    for p in sorted(folder.iterdir()):
        if not p.is_file():
            continue
        if p.name.startswith("."):
            continue
        if p.name in IGNORE_NAMES:
            continue
        if p.suffix.lower() in IGNORE_SUFFIXES:
            continue
        if p.suffix.lower() not in OK_SUFFIXES:
            continue
        out.append(p)
    return out


def load_ledger() -> dict:
    if not LEDGER.exists():
        return {"files": {}}
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def save_ledger(data: dict) -> None:
    FEED.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def with_lock():
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    fh = LOCK.open("a+")
    fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
    return fh


def pending() -> list[dict]:
    ledger = load_ledger().get("files") or {}
    best: dict[str, dict] = {}
    for folder in watch_dirs():
        for p in list_candidates(folder):
            digest = sha256(p)
            rec = ledger.get(p.name) or {}
            if rec.get("sha256") == digest and rec.get("status") in ("done", "processing"):
                continue
            row = {
                "name": p.name,
                "path": str(p),
                "sha256": digest,
                "bytes": p.stat().st_size,
                "mtime": p.stat().st_mtime,
                "prev_status": rec.get("status"),
            }
            prev = best.get(p.name)
            if prev is None or row["mtime"] >= prev["mtime"]:
                best[p.name] = row
    rows = list(best.values())
    rows.sort(key=lambda r: r["name"])
    return rows


def sync_into_worktree(src: Path) -> Path:
    """Copie vers le worktree pour versionner / traiter."""
    dest = FEED / src.name
    if src.resolve() == dest.resolve():
        return dest
    FEED.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    return dest


def cmd_scan(_args: argparse.Namespace) -> int:
    rows = pending()
    json.dump({"files": rows, "dirs": [str(d) for d in watch_dirs()]}, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


def cmd_claim(args: argparse.Namespace) -> int:
    src = Path(args.path)
    if not src.is_file():
        # nom seul dans le dossier feedback
        for folder in watch_dirs():
            cand = folder / src.name
            if cand.is_file():
                src = cand
                break
    if not src.is_file():
        print(f"absent: {args.path}", file=sys.stderr)
        return 1
    dest = sync_into_worktree(src)
    digest = sha256(dest)
    fh = with_lock()
    try:
        data = load_ledger()
        files = data.setdefault("files", {})
        rec = files.get(dest.name) or {}
        if rec.get("sha256") == digest and rec.get("status") == "done":
            print(json.dumps({"ok": False, "reason": "already-done", "name": dest.name}))
            return 2
        if rec.get("sha256") == digest and rec.get("status") == "processing":
            print(json.dumps({"ok": False, "reason": "already-processing", "name": dest.name}))
            return 3
        files[dest.name] = {
            "sha256": digest,
            "status": "processing",
            "note": rec.get("note") or "",
        }
        save_ledger(data)
        rel = str(dest.relative_to(ROOT)) if dest.is_relative_to(ROOT) else str(dest)
        print(json.dumps({"ok": True, "name": dest.name, "sha256": digest, "path": rel}))
        return 0
    finally:
        fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
        fh.close()


def cmd_done(args: argparse.Namespace) -> int:
    name = Path(args.path).name
    target = FEED / name
    digest = sha256(target) if target.is_file() else ""
    fh = with_lock()
    try:
        data = load_ledger()
        files = data.setdefault("files", {})
        rec = files.get(name) or {}
        files[name] = {
            "sha256": digest or rec.get("sha256") or "",
            "status": "done",
            "note": args.note or rec.get("note") or "",
        }
        save_ledger(data)
        print(json.dumps({"ok": True, "name": name, "status": "done"}))
        return 0
    finally:
        fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
        fh.close()


def _announce_pending(announced: set[str]) -> set[str]:
    live = set()
    for row in pending():
        key = row["sha256"]
        live.add(key)
        if key in announced:
            continue
        announced.add(key)
        print(
            f"ACTION_REQUIRED: nouveau feedback {row['path']} sha256={key[:12]}",
            flush=True,
        )
    return announced & live


def watch_inotify(interval: int) -> int:
    fd = LIBC.inotify_init()
    if fd < 0:
        raise OSError("inotify_init")
    os.set_blocking(fd, False)
    for d in watch_dirs():
        wd = LIBC.inotify_add_watch(fd, str(d).encode(), IN_MASK)
        if wd < 0:
            raise OSError(f"inotify_add_watch {d}")
    announced: set[str] = set()
    announced = _announce_pending(announced)
    buf = b""
    while True:
        ready, _, _ = select.select([fd], [], [], max(1, interval))
        if ready:
            try:
                buf += os.read(fd, 65536)
            except BlockingIOError:
                pass
            while len(buf) >= EVENT_HDR.size:
                _wd, _mask, _cookie, nlen = EVENT_HDR.unpack_from(buf)
                total = EVENT_HDR.size + nlen
                if len(buf) < total:
                    break
                raw_name = buf[EVENT_HDR.size : total].split(b"\x00", 1)[0]
                buf = buf[total:]
                name = raw_name.decode("utf-8", "replace")
                if not name or name in IGNORE_NAMES:
                    continue
                time.sleep(0.2)
                announced = _announce_pending(announced)
        else:
            announced = _announce_pending(announced)


def watch_poll(interval: int) -> int:
    announced: set[str] = set()
    while True:
        announced = _announce_pending(announced)
        time.sleep(max(2, interval))


def cmd_watch(args: argparse.Namespace) -> int:
    interval = max(2, int(args.interval))
    print(
        "WATCHING " + " ".join(str(d) for d in watch_dirs()),
        file=sys.stderr,
        flush=True,
    )
    try:
        try:
            return watch_inotify(interval)
        except OSError:
            return watch_poll(interval)
    except Exception as exc:
        print(f"FAILED: watch {exc}", flush=True)
        return 1


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("scan")
    p_claim = sub.add_parser("claim")
    p_claim.add_argument("path")
    p_done = sub.add_parser("done")
    p_done.add_argument("path")
    p_done.add_argument("--note", default="")
    p_watch = sub.add_parser("watch")
    p_watch.add_argument("--interval", type=int, default=2)
    args = ap.parse_args()
    fn = {"scan": cmd_scan, "claim": cmd_claim, "done": cmd_done, "watch": cmd_watch}[args.cmd]
    raise SystemExit(fn(args))


if __name__ == "__main__":
    main()
