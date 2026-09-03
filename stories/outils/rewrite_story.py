#!/usr/bin/env python3
"""F-NAR-008 — dump / merge agents / apply (l'xlsx source reste intact jusqu'à apply)."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
ARBRES = ROOT / "arbres"
REWRITES = ROOT / "rewrites"

CHUNK_FIELDS = (
    "chunk_id",
    "kind",
    "text",
    "script",
    "sons",
    "length_scale_piper",
    "rate_label",
    "pause_after_ms",
)


def dump_story(story_id: str) -> Path:
    src = ARBRES / f"{story_id}.xlsx"
    if not src.exists():
        raise SystemExit(f"absent: {src}")
    wb = load_workbook(src, read_only=True, data_only=True)
    meta = {}
    if "meta" in wb.sheetnames:
        for row in wb["meta"].iter_rows(values_only=True):
            if row and row[0] not in (None, "clé"):
                meta[str(row[0])] = "" if row[1] is None else str(row[1])
    rows = list(wb["chunks"].iter_rows(values_only=True))
    headers = [str(h) if h else "" for h in rows[0]]
    chunks = []
    for r in rows[1:]:
        d = {headers[i]: r[i] if i < len(r) else None for i in range(len(headers))}
        if not d.get("chunk_id"):
            continue
        chunks.append({k: d.get(k) for k in CHUNK_FIELDS if k in d})
    wb.close()
    out_dir = REWRITES / story_id
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "story_id": story_id,
        "fil_rouge": "",
        "title": meta.get("title", ""),
        "lesson_id": meta.get("lesson_id", ""),
        "age_band": meta.get("age_band", ""),
        "kind": meta.get("kind", ""),
        "characters": meta.get("characters", ""),
        "setting": meta.get("setting", ""),
        "chunks": chunks,
    }
    path = out_dir / "source.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def _score(agent: dict) -> int:
    """Plus le fil rouge et les textes sont longs (sans être vides), mieux c'est."""
    s = len(agent.get("fil_rouge") or "")
    for c in agent.get("chunks") or []:
        s += min(len(str(c.get("text") or "")), 400)
        s += 20 if c.get("script") else 0
    return s


def merge_story(story_id: str) -> Path:
    folder = REWRITES / story_id
    source = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    agents = []
    for p in sorted(folder.glob("agent_*.json")):
        agents.append(json.loads(p.read_text(encoding="utf-8")))
    if not agents:
        raise SystemExit(f"aucun agent_*.json dans {folder}")
    agents.sort(key=_score, reverse=True)
    best = agents[0]
    by_id = {c["chunk_id"]: c for c in source["chunks"]}
    for ag in reversed(agents):
        for c in ag.get("chunks") or []:
            cid = c.get("chunk_id")
            if cid in by_id:
                for k in CHUNK_FIELDS:
                    if c.get(k) not in (None, ""):
                        by_id[cid][k] = c[k]
    merged = dict(source)
    merged["fil_rouge"] = best.get("fil_rouge") or source.get("fil_rouge")
    merged["title"] = best.get("title") or source.get("title")
    merged["merged_from"] = [p.name for p in sorted(folder.glob("agent_*.json"))]
    merged["chunks"] = [by_id[c["chunk_id"]] for c in source["chunks"]]
    out = folder / "merged.json"
    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def apply_story(story_id: str) -> Path:
    folder = REWRITES / story_id
    merged_path = folder / "merged.json"
    if not merged_path.exists():
        merge_story(story_id)
    merged = json.loads(merged_path.read_text(encoding="utf-8"))
    src = ARBRES / f"{story_id}.xlsx"
    backup = folder / "original.xlsx"
    if not backup.exists():
        shutil.copy2(src, backup)
    wb = load_workbook(src)
    if "meta" in wb.sheetnames and merged.get("title"):
        ms = wb["meta"]
        for row in ms.iter_rows(min_col=1, max_col=2):
            if row[0].value == "title":
                row[1].value = merged["title"]
            if row[0].value == "fil_rouge":
                row[1].value = merged.get("fil_rouge") or ""
        keys = {str(c.value) for c in ms["A"] if c.value}
        if "fil_rouge" not in keys:
            ms.append(["fil_rouge", merged.get("fil_rouge") or ""])
    ws = wb["chunks"]
    headers = [c.value for c in ws[1]]
    for name in ("script", "sons", "length_scale_piper", "rate_label"):
        if name not in headers:
            ws.cell(1, len(headers) + 1, name)
            headers.append(name)
    idx = {name: i + 1 for i, name in enumerate(headers)}
    by_id = {c["chunk_id"]: c for c in merged["chunks"]}
    for r in range(2, ws.max_row + 1):
        cid = ws.cell(r, idx["chunk_id"]).value
        if cid not in by_id:
            continue
        c = by_id[cid]
        for k in ("text", "script", "sons", "length_scale_piper", "rate_label"):
            if k in idx and c.get(k) is not None:
                ws.cell(r, idx[k], c[k])
    if "journal" in wb.sheetnames:
        wb["journal"].append(["F-NAR-008 récit captivant, fusion agents"])
    wb.save(src)
    wb.close()
    return src


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["dump", "merge", "apply"])
    ap.add_argument("story_id")
    args = ap.parse_args()
    if args.cmd == "dump":
        print(dump_story(args.story_id))
    elif args.cmd == "merge":
        print(merge_story(args.story_id))
    else:
        print(apply_story(args.story_id))


if __name__ == "__main__":
    main()
