#!/usr/bin/env python3
"""Veille de gestion_projet/feedback_chatgpt/ (F-NAR-017).

scan   — fichiers nouveaux / changés (JSON), exit 0 même si vide
claim  — marque un fichier « processing » (échec si déjà done pour ce hash)
done   — marque « done »
watch  — poll ; une ligne ACTION_REQUIRED par nouveau hash, puis continue
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FEED = ROOT / "gestion_projet" / "feedback_chatgpt"
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


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def list_candidates() -> list[Path]:
    if not FEED.is_dir():
        return []
    out = []
    for p in sorted(FEED.iterdir()):
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
    LEDGER.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def with_lock():
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    fh = LOCK.open("a+")
    fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
    return fh


def pending() -> list[dict]:
    ledger = load_ledger().get("files") or {}
    rows = []
    for p in list_candidates():
        digest = sha256(p)
        rec = ledger.get(p.name) or {}
        if rec.get("sha256") == digest and rec.get("status") in ("done", "processing"):
            continue
        rows.append(
            {
                "name": p.name,
                "path": str(p.relative_to(ROOT)),
                "sha256": digest,
                "bytes": p.stat().st_size,
                "prev_status": rec.get("status"),
            }
        )
    return rows


def cmd_scan(_args: argparse.Namespace) -> int:
    rows = pending()
    json.dump({"files": rows}, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


def cmd_claim(args: argparse.Namespace) -> int:
    name = Path(args.path).name
    target = FEED / name
    if not target.is_file():
        print(f"absent: {target}", file=sys.stderr)
        return 1
    digest = sha256(target)
    fh = with_lock()
    try:
        data = load_ledger()
        files = data.setdefault("files", {})
        rec = files.get(name) or {}
        if rec.get("sha256") == digest and rec.get("status") == "done":
            print(json.dumps({"ok": False, "reason": "already-done", "name": name}))
            return 2
        if rec.get("sha256") == digest and rec.get("status") == "processing":
            print(json.dumps({"ok": False, "reason": "already-processing", "name": name}))
            return 3
        files[name] = {
            "sha256": digest,
            "status": "processing",
            "note": rec.get("note") or "",
        }
        save_ledger(data)
        print(json.dumps({"ok": True, "name": name, "sha256": digest, "path": str(target.relative_to(ROOT))}))
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


def cmd_watch(args: argparse.Namespace) -> int:
    announced: set[str] = set()
    interval = max(5, int(args.interval))
    while True:
        try:
            for row in pending():
                key = row["sha256"]
                if key in announced:
                    continue
                announced.add(key)
                print(f"ACTION_REQUIRED: nouveau feedback {row['path']} sha256={key[:12]}", flush=True)
            # hashes now done drop from pending; allow re-announce if file changes later
            live = {r["sha256"] for r in pending()}
            announced &= live
        except Exception as exc:
            print(f"FAILED: watch {exc}", flush=True)
            return 1
        time.sleep(interval)


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
    p_watch.add_argument("--interval", type=int, default=30)
    args = ap.parse_args()
    fn = {"scan": cmd_scan, "claim": cmd_claim, "done": cmd_done, "watch": cmd_watch}[args.cmd]
    raise SystemExit(fn(args))


if __name__ == "__main__":
    main()
