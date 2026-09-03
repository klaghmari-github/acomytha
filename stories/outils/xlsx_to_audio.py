#!/usr/bin/env python3
"""Bake audio depuis les xlsx.

Piper sort du 22050 Hz (souvent muet sur téléphone / Windows / navigateur).
On réécrit en WAV PCM 44100 Hz 16-bit + MP3 64 kbit/s, niveau normalisé.
"""
from __future__ import annotations

import argparse
import shutil
import struct
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np
from openpyxl import load_workbook
from scipy.signal import resample_poly

ROOT = Path(__file__).resolve().parents[1]
ARBRES = ROOT / "arbres"
AUDIO = ROOT / "audio"
VOICES = ROOT / "outils" / "voices"
TARGET_SR = 44100
PEAK_TARGET = 0.89  # ~ -1 dBFS
MIN_PEAK = 500  # en dessous = considéré muet


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


def read_pcm16(path: Path) -> tuple[np.ndarray, int]:
    with wave.open(str(path), "rb") as w:
        sr = w.getframerate()
        nch = w.getnchannels()
        sw = w.getsampwidth()
        n = w.getnframes()
        raw = w.readframes(n)
    if sw != 2:
        raise ValueError(f"{path}: sampwidth {sw}, attendu 16-bit")
    samples = np.frombuffer(raw, dtype="<i2").astype(np.float32)
    if nch > 1:
        samples = samples.reshape(-1, nch).mean(axis=1)
    return samples, sr


def write_wav44100(path: Path, samples: np.ndarray):
    path.parent.mkdir(parents=True, exist_ok=True)
    clipped = np.clip(samples, -32768, 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(TARGET_SR)
        w.writeframes(clipped.tobytes())


def write_mp3(path: Path, samples: np.ndarray):
    import lameenc

    enc = lameenc.Encoder()
    enc.set_bit_rate(64)
    enc.set_in_sample_rate(TARGET_SR)
    enc.set_channels(1)
    enc.set_quality(2)
    pcm = np.clip(samples, -32768, 32767).astype("<i2").tobytes()
    mp3 = enc.encode(pcm) + enc.flush()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(mp3)


def finalize(samples: np.ndarray, sr: int) -> tuple[np.ndarray, dict]:
    if sr != TARGET_SR:
        # 22050 → 44100 = *2 exact
        g = np.gcd(sr, TARGET_SR)
        samples = resample_poly(samples, TARGET_SR // g, sr // g)
    peak = float(np.max(np.abs(samples))) if len(samples) else 0.0
    if peak < MIN_PEAK:
        raise ValueError(f"signal trop faible peak={peak}")
    samples = samples * (PEAK_TARGET * 32767.0 / peak)
    rms = float(np.sqrt(np.mean(samples**2)))
    return samples, {
        "peak": int(np.max(np.abs(samples))),
        "rms": round(rms, 1),
        "dur": round(len(samples) / TARGET_SR, 2),
        "src_peak": int(peak),
    }


def stats_file(path: Path) -> dict:
    samples, sr = read_pcm16(path)
    peak = int(np.max(np.abs(samples))) if len(samples) else 0
    rms = float(np.sqrt(np.mean(samples**2))) if len(samples) else 0
    return {
        "sr": sr,
        "peak": peak,
        "rms": round(rms, 1),
        "dur": round(len(samples) / sr, 2),
        "ok": sr == TARGET_SR and peak >= MIN_PEAK,
    }


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
    subprocess.run(
        cmd,
        input=text.encode("utf-8"),
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def synth_espeak(bin: str, text: str, out: Path, row: dict):
    out.parent.mkdir(parents=True, exist_ok=True)
    speed = max(80, min(160, int(row.get("rate_wpm") or 130)))
    pitch = int(row.get("espeak_pitch") or 50)
    gap = int(row.get("espeak_word_gap") or 10)
    amp = int(row.get("espeak_amp") or 100)
    subprocess.run(
        [
            bin, "-v", "fr", "-s", str(speed), "-p", str(pitch),
            "-g", str(gap), "-a", str(amp), "-w", str(out), text,
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


def emit_playable(src_wav: Path, dest_wav: Path, dest_mp3: Path) -> dict:
    samples, sr = read_pcm16(src_wav)
    samples, info = finalize(samples, sr)
    write_wav44100(dest_wav, samples)
    write_mp3(dest_mp3, samples)
    check = stats_file(dest_wav)
    if not check["ok"]:
        raise RuntimeError(f"post-verif fail {dest_wav} {check}")
    if dest_mp3.stat().st_size < 400:
        raise RuntimeError(f"mp3 trop petit {dest_mp3}")
    info.update(check)
    return info


def bake_tree(xlsx: Path, engine, bin_path, model, force=False) -> tuple[int, int, int]:
    story_id = xlsx.stem
    dest = AUDIO / story_id
    chunks = load_chunks(xlsx)
    ok = skip = fail = 0
    for d in chunks:
        cid = str(d["chunk_id"]).replace("/", "_")
        wav = dest / f"{cid}.wav"
        mp3 = dest / f"{cid}.mp3"
        if wav.exists() and mp3.exists() and not force:
            try:
                if stats_file(wav)["ok"]:
                    skip += 1
                    continue
            except Exception:
                pass
        text = str(d["text"]).strip()
        try:
            with tempfile.TemporaryDirectory() as td:
                raw = Path(td) / "raw.wav"
                if engine == "piper":
                    ls = float(d.get("length_scale_piper") or 1.2)
                    synth_piper(bin_path, model, text, raw, ls)
                else:
                    synth_espeak(bin_path, text, raw, d)
                emit_playable(raw, wav, mp3)
            ok += 1
        except Exception as e:
            fail += 1
            print(f"FAIL {story_id}/{cid}: {e}", file=sys.stderr)
    return ok, skip, fail


def fix_existing(force=False) -> tuple[int, int]:
    """Réécrit les WAV 22050 déjà là en 44100+MP3, sans Piper."""
    ok = fail = 0
    for wav in sorted(AUDIO.rglob("*.wav")):
        if wav.with_suffix(".mp3").exists() and not force:
            try:
                if stats_file(wav)["ok"]:
                    continue
            except Exception:
                pass
        tmp = wav.with_suffix(".wav.tmp")
        try:
            info = emit_playable(wav, tmp, wav.with_suffix(".mp3"))
            tmp.replace(wav)
            ok += 1
            print(f"FIX {wav.parent.name}/{wav.name} sr44100 peak={info['peak']} dur={info['dur']}")
        except Exception as e:
            if tmp.exists():
                tmp.unlink()
            fail += 1
            print(f"FAIL fix {wav}: {e}", file=sys.stderr)
    return ok, fail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="tree_id sans .xlsx")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--fix-existing", action="store_true", help="réécrire 22050→44100+mp3")
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()

    if args.fix_existing:
        ok, fail = fix_existing(args.force)
        print(f"FIX DONE ok={ok} fail={fail}")
        if args.verify or True:
            bad = 0
            n = 0
            for wav in AUDIO.rglob("*.wav"):
                n += 1
                s = stats_file(wav)
                mp3 = wav.with_suffix(".mp3")
                if not s["ok"] or not mp3.exists():
                    bad += 1
                    print("BAD", wav, s, "mp3", mp3.exists())
            print(f"VERIFY n={n} bad={bad}")
        sys.exit(1 if fail else 0)

    engine, bin_path, model = find_engine()
    if not engine:
        print("Aucun TTS : installer piper ou espeak-ng", file=sys.stderr)
        sys.exit(1)
    print(f"engine={engine} bin={bin_path} model={model} out=wav44100+mp3")
    files = sorted(ARBRES.glob("*.xlsx"))
    if args.only:
        want = set(args.only)
        files = [f for f in files if f.stem in want]
    if args.limit:
        files = files[: args.limit]
    total_ok = total_skip = total_fail = 0
    for i, f in enumerate(files, 1):
        ok, skip, fail = bake_tree(f, engine, bin_path, model, args.force)
        total_ok += ok
        total_skip += skip
        total_fail += fail
        print(f"[{i}/{len(files)}] {f.stem} +{ok} skip={skip} fail={fail}", flush=True)
    print(f"DONE ok={total_ok} skip={total_skip} fail={total_fail}")
    sys.exit(1 if total_fail else 0)


if __name__ == "__main__":
    main()
