#!/usr/bin/env python3
"""Bake WAV (Piper si dispo, sinon espeak-ng) depuis les xlsx. Un dossier par arbre."""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
ARBRES = ROOT / "arbres"
AUDIO = ROOT / "audio"
VOICES = ROOT / "outils" / "voices"


def find_engine():
    piper = shutil.which("piper") or str(Path.home() / ".local/bin/piper")
    if piper and not Path(piper).exists():
        piper = None
    model = VOICES / "fr_FR-siwis-medium.onnx"
    if piper and model.exists():
        return "piper", piper, model
    espeak = shutil.which("espeak-ng") or shutil.which("espeak")
    if espeak:
        return "espeak", espeak, None
    return None, None, None


def synth_piper(piper: str, model: Path, text: str, out: Path, length_scale: float):
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        piper,
        "--model",
        str(model),
        "--output_file",
        str(out),
        "--length_scale",
        str(length_scale or 1.2),
        "--sentence_silence",
        "0.35",
    ]
    subprocess.run(cmd, input=text.encode("utf-8"), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def synth_espeak(bin: str, text: str, out: Path, row: dict):
    out.parent.mkdir(parents=True, exist_ok=True)
    wav = out
    speed = max(80, min(160, int(row.get("rate_wpm") or 130)))
    pitch = int(row.get("espeak_pitch") or 50)
    gap = int(row.get("espeak_word_gap") or 10)
    amp = int(row.get("espeak_amp") or 100)
    subprocess.run(
        [
            bin,
            "-v",
            "fr",
            "-s",
            str(speed),
            "-p",
            str(pitch),
            "-g",
            str(gap),
            "-a",
            str(amp),
            "-w",
            str(wav),
            text,
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def load_chunks(xlsx: Path) -> list[dict]:
    wb = load_workbook(xlsx, read_only=True, data_only=True)
    ch = wb["chunks"]
    rows = list(ch.iter_rows(values_only=True))
    headers = [str(h) if h else "" for h in rows[0]]
    out = []
    for r in rows[1:]:
        d = {headers[i]: r[i] if i < len(r) else None for i in range(len(headers))}
        if d.get("chunk_id") and d.get("text"):
            out.append(d)
    wb.close()
    return out


def bake_tree(xlsx: Path, engine, bin_path, model, force=False) -> tuple[int, int]:
    story_id = xlsx.stem
    dest = AUDIO / story_id
    chunks = load_chunks(xlsx)
    ok = skip = 0
    for d in chunks:
        cid = str(d["chunk_id"]).replace("/", "_")
        wav = dest / f"{cid}.wav"
        if wav.exists() and wav.stat().st_size > 44 and not force:
            skip += 1
            continue
        text = str(d["text"]).strip()
        try:
            if engine == "piper":
                ls = float(d.get("length_scale_piper") or 1.2)
                synth_piper(bin_path, model, text, wav, ls)
            else:
                synth_espeak(bin_path, text, wav, d)
            ok += 1
        except Exception as e:
            print(f"FAIL {story_id}/{cid}: {e}", file=sys.stderr)
    return ok, skip


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="tree_id sans .xlsx")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    engine, bin_path, model = find_engine()
    if not engine:
        print("Aucun TTS : installer piper ou espeak-ng", file=sys.stderr)
        sys.exit(1)
    print(f"engine={engine} bin={bin_path} model={model}")
    files = sorted(ARBRES.glob("*.xlsx"))
    if args.only:
        want = set(args.only)
        files = [f for f in files if f.stem in want]
    if args.limit:
        files = files[: args.limit]
    total_ok = total_skip = 0
    for i, f in enumerate(files, 1):
        ok, skip = bake_tree(f, engine, bin_path, model, args.force)
        total_ok += ok
        total_skip += skip
        print(f"[{i}/{len(files)}] {f.stem} +{ok} skip={skip}", flush=True)
    print(f"DONE ok={total_ok} skip={total_skip}")


if __name__ == "__main__":
    main()
