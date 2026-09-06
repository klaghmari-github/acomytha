"""python -m akomythatts convert|web."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from .app import TtsApp
from .web import create_app


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = argparse.ArgumentParser(prog="akomythatts")
    sub = parser.add_subparsers(dest="cmd", required=True)
    convert = sub.add_parser("convert", help="Convertit les Excel de stories/arbres en JSON TTS")
    convert.add_argument("--source", type=Path, default=None)
    convert.add_argument("--output", type=Path, default=None)
    sub.add_parser("web", help="Lance le studio web")
    args = parser.parse_args()
    if args.cmd == "web":
        create_app().run()
        return
    tts = TtsApp.assemble()
    report = tts.convert_excel(args.source, args.output)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
