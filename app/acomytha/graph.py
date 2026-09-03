"""Graphe d'histoire : successeurs explicites + convention d'IDs."""

from __future__ import annotations

from acomytha.models import Chunk


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
            return next(iter(self.by_id))
        raise ValueError("histoire sans chunk")

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
        chunk = self.by_id[chunk_id]
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
        return self._infer(chunk_id, chunk.kind)

    def _infer(self, chunk_id: str, kind: str) -> str | None:
        if kind == "passage_question":
            alt = chunk_id.replace("_Q0001", "_C0001")
            if alt != chunk_id and alt in self.ids:
                return alt
        base = chunk_id[: -len("_C0001")] if chunk_id.endswith("_C0001") else chunk_id
        for cand in (
            f"{chunk_id}_Q0001",
            f"{chunk_id}_C0001",
            f"{chunk_id}_END",
            f"{chunk_id}_F0001",
            "CHK_T0001_P0000" if chunk_id == "CHK_T0000_P0000" else "",
            self._next_transition(base),
        ):
            if cand and cand in self.ids:
                return cand
        return None

    def _next_transition(self, chunk_id: str) -> str:
        t_count = chunk_id.count("_T")
        if "_P" not in chunk_id:
            return ""
        return f"{chunk_id}_T{t_count + 1:04d}_P0000"
