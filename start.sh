#!/usr/bin/env bash
# Lance le serveur AcoMytha (parent, enfant, admin, éditeur TTS) — un seul port.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

HOST="${ACOMYTHA_HOST:-127.0.0.1}"
PORT="${ACOMYTHA_PORT:-8787}"

if [[ -x "$ROOT/.venv/bin/python" ]]; then
  PYTHON="$ROOT/.venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON="$(command -v python3)"
else
  echo "Aucun Python : crée .venv à la racine (copie AkoMythaTTS) ou installe python3." >&2
  exit 1
fi

if [[ -f "$ROOT/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$ROOT/.env"
  set +a
fi

export PYTHONPATH="$ROOT/app${PYTHONPATH:+:$PYTHONPATH}"

echo "AcoMytha → http://${HOST}:${PORT}  ($PYTHON)"
exec "$PYTHON" -m uvicorn acomytha.main:create_app --factory --host "$HOST" --port "$PORT"
