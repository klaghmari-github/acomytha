"""Graphe d'histoire : successeurs explicites + convention d'IDs."""

from __future__ import annotations

import re

from acomytha.models import Chunk

_PART = re.compile(r"^([A-Z]+)(\d+)?$")
# T en tête = branche. T imbriqué = suite du chemin, après Q/C.
_RANK_HEAD = {"T": 0, "P": 1, "O": 2, "Q": 3, "C": 4, "END": 6, "F": 7}
_RANK_NESTED_T = 5


def chunk_sort_key(chunk_id: str) -> tuple:
    body = chunk_id[4:] if chunk_id.startswith("CHK_") else chunk_id
    key: list[tuple[int, int]] = []
    for i, part in enumerate(body.split("_")):
        m = _PART.match(part)
        if not m:
            key.append((50, 0))
            continue
        letters, num = m.group(1), int(m.group(2) or 0)
        if letters == "T" and i > 0:
            rank = _RANK_NESTED_T
        else:
            rank = _RANK_HEAD.get(letters, 40)
        key.append((rank, num))
    return tuple(key)


class StoryGraph:
    """Objet graphe : un chunk courant, des options, une politique nuit."""

    def __init__(self, chunks: list[Chunk]) -> None:
        self.by_id = {c.chunk_id: c for c in chunks}
        self.ids = set(self.by_id)

    @property
    def root(self) -> str:
        if "CHK_T0000_P0000" in self.ids:
            return "CHK_T0000_P0000"
        if self.by_id:
            return min(self.ids, key=chunk_sort_key)
        raise ValueError("histoire sans chunk")

    def is_linear(self) -> bool:
        for cid, chunk in self.by_id.items():
            if self.options(cid):
                return False
            if (chunk.kind or "").startswith("transition"):
                return False
        return True

    def as_client_dict(self, include_text: bool) -> dict:
        nodes = {}
        for cid, chunk in self.by_id.items():
            node = {
                "chunk_id": cid,
                "kind": chunk.kind,
                "wait_ms": chunk.wait_ms or 0,
                "night_policy": chunk.night_policy or "play",
                "default_next": self.successor(cid),
                "options": self.options(cid),
            }
            if include_text:
                node["text"] = chunk.text
            nodes[cid] = node
        return {"root": self.root, "chunks": nodes}

    def options(self, chunk_id: str) -> list[dict]:
        chunk = self.by_id.get(chunk_id)
        if chunk is None:
            return []
        out = []
        for i in (1, 2, 3):
            label = getattr(chunk, f"option_{i}_label") or ""
            nxt = getattr(chunk, f"option_{i}_next") or ""
            if label and nxt:
                out.append({"index": i, "label": label, "next": nxt})
        return out

    def successor(self, chunk_id: str) -> str | None:
        chunk = self.by_id.get(chunk_id)
        if chunk is None:
            return None
        if chunk.kind == "passage_fin":
            return None
        if chunk.default_next and chunk.default_next in self.ids:
            return chunk.default_next
        return self._infer(chunk_id, chunk.kind or "")

    def default_path(self) -> list[str]:
        """Chemin racine → feuille en suivant le défaut (option 1 si choix)."""
        out: list[str] = []
        seen: set[str] = set()
        cid: str | None = self.root
        while cid and cid in self.ids and cid not in seen:
            seen.add(cid)
            out.append(cid)
            chunk = self.by_id[cid]
            if chunk.kind == "passage_fin":
                break
            nxt = self.successor(cid)
            if not nxt:
                opts = self.options(cid)
                nxt = opts[0]["next"] if opts else None
            cid = nxt if nxt in self.ids else None
        return out

    def _infer(self, chunk_id: str, kind: str) -> str | None:
        if kind == "passage_question":
            alt = chunk_id.replace("_Q0001", "_C0001")
            if alt != chunk_id and alt in self.ids:
                return alt
        if self.is_linear():
            ordered = sorted(self.ids, key=chunk_sort_key)
            try:
                i = ordered.index(chunk_id)
            except ValueError:
                return None
            if i + 1 < len(ordered):
                nxt = ordered[i + 1]
                if self.by_id[chunk_id].kind != "passage_fin":
                    return nxt
            return None
        for suffix in ("_Q0001", "_C0001", "_END", "_F0001"):
            cand = f"{chunk_id}{suffix}"
            if cand in self.ids:
                return cand
        if chunk_id.endswith("_C0001"):
            stem = chunk_id[: -len("_C0001")]
            for cand in (f"{stem}_END", f"{stem}_F0001"):
                if cand in self.ids:
                    return cand
            nested_from_stem = [
                i
                for i in self.ids
                if i.startswith(f"{stem}_T") and i.endswith("_P0000")
            ]
            if nested_from_stem:
                return min(nested_from_stem, key=chunk_sort_key)
        nested = [
            i
            for i in self.ids
            if i.startswith(f"{chunk_id}_T") and i.endswith("_P0000")
        ]
        if nested:
            return min(nested, key=chunk_sort_key)
        if chunk_id == "CHK_T0000_P0000" and "CHK_T0001_P0000" in self.ids:
            return "CHK_T0001_P0000"
        t_count = chunk_id.count("_T")
        nested_id = f"{chunk_id}_T{t_count + 1:04d}_P0000"
        if nested_id in self.ids:
            return nested_id
        return None
