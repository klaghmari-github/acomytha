#!/usr/bin/env python3
"""Validateur déterministe Sentier — CHILD_AUDIO, graphe, contrat pédagogique."""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LECONS_PATH = ROOT / "referentiel" / "lecons.json"
ATOM = ROOT / "atomiques"
RAMI = ROOT / "ramifiees"
REPORT = ROOT / "rapports"

BLOCKING_PATTERNS = [
    (r"\bdeux papas\b", "GARDEN", "configuration familiale hors jardin"),
    (r"\bdeux mamans\b", "GARDEN", "configuration familiale hors jardin"),
    (r"\bpapa et papa\b", "GARDEN", "configuration familiale hors jardin"),
    (r"\bmaman et maman\b", "GARDEN", "configuration familiale hors jardin"),
    (r"\blgbt\b", "GARDEN", "discours hors jardin"),
    (r"\btransgenre\b", "GARDEN", "discours hors jardin"),
    (r"\bpri[eè]re\b", "GARDEN", "religion"),
    (r"\b[eé]glise\b", "GARDEN", "religion"),
    (r"\bmosqu[eé]e\b", "GARDEN", "religion"),
    (r"\bsynagogue\b", "GARDEN", "religion"),
    (r"\bguerre\b", "SAFE", "guerre"),
    (r"\bsoldats?\b", "SAFE", "guerre"),
    (r"\bbombe\b", "SAFE", "guerre"),
    (r"\bfusil\b", "SAFE", "arme"),
    (r"\barme\b", "SAFE", "arme"),
    (r"\btuerie\b", "SAFE", "violence"),
    (r"\btuer\b", "SAFE", "violence"),
    (r"\bcrime\b", "SAFE", "crime"),
    (r"\bhyperactif\b", "RESPECT", "diagnostic nommé"),
    (r"\bautiste\b", "RESPECT", "diagnostic nommé"),
    (r"\btdah\b", "RESPECT", "diagnostic nommé"),
    (r"ne t['']aimera plus", "SAFE", "menace affective"),
    (r"on ne t['']aime plus", "SAFE", "menace affective"),
    (r"\bil est m[eé]chant\b", "NEU", "étiquette identitaire"),
    (r"\belle est m[eé]chante\b", "NEU", "étiquette identitaire"),
    (r"\bil est bizarre\b", "NEU", "étiquette identitaire"),
    (r"\bil est nul\b", "NEU", "étiquette identitaire"),
    (r"\btu es nul\b", "NEU", "humiliation"),
    (r"\bregarde (l['']image|l[''][eé]cran|le dessin)\b", "NAR", "dépendance visuelle"),
]

CRITICAL_IMITABLE = [
    (r"courir (sur|dans) (la )?(chauss[eé]e|route)", "course sur chaussée"),
    (r"traverser (au rouge|tout seul|sans adulte)", "traversée imitable"),
    (r"avancer au rouge", "option dangereuse"),
    (r"dans la prise", "geste électrique"),
    (r"sauter (du|de la|par le) balcon", "hauteur"),
    (r"ouvrir la porti[eè]re", "transport"),
    (r"comment frapper", "bagarre"),
    (r"rendre un coup", "bagarre"),
]

FRANCHISE = [
    r"\bmickey\b", r"\bpikachu\b", r"\belsa\b", r"\bdisney\b", r"\bmario\b",
    r"\bspiderman\b", r"\bspider-man\b", r"\breine des neiges\b", r"\bpaw patrol\b",
    r"\bpat[' ]?patrouille\b", r"\bpeppa\b", r"\bbarbie\b",
]


def norm(s: str) -> str:
    return (s or "").lower().replace("’", "'")


def load_lessons() -> dict:
    data = json.loads(LECONS_PATH.read_text(encoding="utf-8"))
    return {l["lesson_id"]: l for l in data["lessons"]}


def collect_child_text(node: dict) -> str:
    parts = [
        node.get("text") or "",
        node.get("prompt") or "",
        node.get("retry_prompt") or "",
        node.get("positive_feedback") or "",
        node.get("wrong_feedback") or "",
    ]
    for opt in node.get("options") or []:
        parts.append(opt.get("label") or "")
    return " ".join(parts)


def walk_graph(nodes: dict, root: str):
    if root not in nodes:
        return [], set(), [f"root {root} absent"]
    seen = set()
    q = deque([root])
    order = []
    errors = []
    while q:
        nid = q.popleft()
        if nid in seen:
            continue
        seen.add(nid)
        order.append(nid)
        n = nodes.get(nid)
        if not n:
            errors.append(f"nœud manquant {nid}")
            continue
        nxt = []
        if n.get("next"):
            nxt.append(n["next"])
        if n.get("default_next"):
            nxt.append(n["default_next"])
        for opt in n.get("options") or []:
            nxt.append(opt.get("next"))
        for x in nxt:
            if not x:
                errors.append(f"{nid}: next vide")
                continue
            if x not in nodes:
                errors.append(f"{nid}: next {x} inexistant")
            else:
                q.append(x)
    orphans = set(nodes) - seen
    return order, orphans, errors


def enumerate_paths(nodes: dict, root: str, cap: int = 400):
    paths = []

    def rec(nid, acc, depth):
        if len(paths) >= cap:
            return
        if depth > 40:
            return
        n = nodes.get(nid)
        if not n:
            return
        acc2 = acc + [nid]
        if n.get("type") == "ending":
            paths.append(acc2)
            return
        nxt = []
        for opt in n.get("options") or []:
            if opt.get("next"):
                nxt.append(opt["next"])
        if n.get("next"):
            nxt.append(n["next"])
        if n.get("default_next") and n["default_next"] not in nxt:
            nxt.append(n["default_next"])
        if not nxt:
            paths.append(acc2)
            return
        for x in nxt:
            if x in acc2:
                continue
            rec(x, acc2, depth + 1)

    rec(root, [], 0)
    return paths


def choice_depth_stats(nodes: dict, root: str):
    """Nombre de nœuds choice_story sur le plus long chemin, et fan-out min."""
    max_choices = 0
    fanouts = []

    def rec(nid, nchoices, seen):
        nonlocal max_choices
        n = nodes.get(nid)
        if not n or nid in seen:
            return
        seen = seen | {nid}
        if n.get("type") == "choice_story":
            nchoices += 1
            opts = n.get("options") or []
            fanouts.append(len(opts))
            max_choices = max(max_choices, nchoices)
            for opt in opts:
                rec(opt.get("next"), nchoices, seen)
            if n.get("default_next"):
                rec(n["default_next"], nchoices, seen)
            return
        if n.get("type") == "ending":
            max_choices = max(max_choices, nchoices)
            return
        for x in filter(None, [n.get("next"), n.get("default_next")]):
            rec(x, nchoices, seen)

    rec(root, 0, set())
    return max_choices, (min(fanouts) if fanouts else 0), (max(fanouts) if fanouts else 0), len(fanouts)


def validate_story(path: Path, lessons: dict) -> dict:
    findings = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return {
            "file": str(path.relative_to(ROOT)),
            "tree_id": None,
            "decision": "REJECTED",
            "blocking": 1,
            "major": 0,
            "findings": [{"severity": "BLOCKING", "rule": "JSON", "msg": str(e)}],
        }

    def add(sev, rule, msg, node=None):
        findings.append({"severity": sev, "rule": rule, "msg": msg, "node": node})

    for field in [
        "tree_id", "kind", "language", "age_band", "title", "lesson_id",
        "domain", "subdomain", "framing", "family_model", "nodes", "root_id",
    ]:
        if field not in data:
            add("BLOCKING", "SCHEMA", f"champ manquant {field}")

    if data.get("language") != "fr":
        add("BLOCKING", "SCHEMA", "language doit être fr")
    if data.get("family_model") != "father_mother_children":
        add("BLOCKING", "GARDEN", "family_model doit être father_mother_children")
    if data.get("age_band") not in ("N1", "N2", "N3"):
        add("BLOCKING", "SCHEMA", f"age_band invalide {data.get('age_band')}")

    lesson_id = data.get("lesson_id")
    lesson = lessons.get(lesson_id)
    if not lesson:
        add("BLOCKING", "PED-001", f"leçon inconnue {lesson_id}")

    nodes = data.get("nodes") or {}
    if not isinstance(nodes, dict) or not nodes:
        add("BLOCKING", "GRAPH", "nodes vide")
        return pack(path, data, findings)

    root = data.get("root_id")
    order, orphans, gerr = walk_graph(nodes, root)
    for e in gerr:
        add("BLOCKING", "GRAPH-001", e)
    for o in orphans:
        add("BLOCKING", "GRAPH-001", f"nœud orphelin {o}")

    endings = [n for n, v in nodes.items() if v.get("type") == "ending"]
    if not endings:
        add("BLOCKING", "GRAPH-001", "aucune feuille ending")

    kinds = {v.get("type") for v in nodes.values()}
    if data.get("kind") == "atomic":
        if "choice_story" in kinds:
            add("BLOCKING", "ATOMIC", "une histoire atomique ne doit pas avoir de choice_story")
        paths = enumerate_paths(nodes, root)
        if len(paths) != 1:
            add("MAJOR", "ATOMIC", f"attendu 1 chemin, obtenu {len(paths)}")
    elif data.get("kind") == "ramifiee":
        max_c, min_fan, max_fan, nchoices = choice_depth_stats(nodes, root)
        if max_c < 3:
            add("BLOCKING", "RAMI", f"profondeur de choix {max_c} < 3")
        if max_c > 3:
            add("BLOCKING", "RAMI", f"profondeur de choix {max_c} > 3 (plafond)")
        if min_fan < 3:
            add("BLOCKING", "RAMI", f"fan-out min {min_fan} < 3")
        if max_fan > 3 and data.get("age_band") == "N1":
            add("MAJOR", "N1", "N1 : 2 choix max, ici fan-out > 3")
        paths = enumerate_paths(nodes, root)
        if len(paths) < 27:
            add("MAJOR", "RAMI", f"chemins {len(paths)} < 27 (3×3×3)")
    else:
        add("BLOCKING", "SCHEMA", f"kind inconnu {data.get('kind')}")
        paths = enumerate_paths(nodes, root)

    # questions
    qnodes = [v for v in nodes.values() if v.get("type") in ("question_lesson", "question_comprehension", "choice_story")]
    if data.get("kind") == "atomic" and not any(v.get("type") == "question_lesson" for v in nodes.values()):
        add("MAJOR", "PED-010", "pas de question_lesson (mobilisation manquante)")

    for v in qnodes:
        if v.get("type") == "choice_story":
            opts = v.get("options") or []
            if len(opts) < 2:
                add("BLOCKING", "INT", f"{v.get('id')}: choice sans options", v.get("id"))
            if not v.get("default_next"):
                add("MAJOR", "INT-004", f"{v.get('id')}: default_next manquant", v.get("id"))
            continue
        if not v.get("expected_intents"):
            add("MAJOR", "INT-002", f"{v.get('id')}: expected_intents manquant", v.get("id"))
        if not v.get("wrong_feedback"):
            add("MAJOR", "POS-005", f"{v.get('id')}: wrong_feedback manquant", v.get("id"))
        if not v.get("default_next"):
            add("MAJOR", "INT-004", f"{v.get('id')}: default_next manquant (silence)", v.get("id"))
        # answers 1-3 words in examples
        for ex in v.get("accepted_examples") or []:
            wc = len(ex.split())
            if wc > 5:
                add("MINOR", "INT-001", f"exemple trop long ({wc} mots): {ex}", v.get("id"))

    # lexique + framing
    framing = data.get("framing") or (lesson or {}).get("framing")
    all_text = " ".join(collect_child_text(v) for v in nodes.values())
    nall = norm(all_text)

    for pat, layer, why in BLOCKING_PATTERNS:
        if re.search(pat, nall, re.I):
            add("BLOCKING", f"NEU-{layer}", f"{why} : /{pat}/")

    for pat in FRANCHISE:
        if re.search(pat, nall, re.I):
            add("BLOCKING", "NAR-005", f"franchise possible : /{pat}/")

    if framing == "positive_only_critical" or (lesson or {}).get("framing") == "positive_only_critical":
        for pat, why in CRITICAL_IMITABLE:
            if re.search(pat, nall, re.I):
                add("BLOCKING", "SAFE-002", f"geste imitable ({why}) : /{pat}/")

    if lesson:
        for forb in lesson.get("forbidden_in_audio") or []:
            if forb and len(forb) > 3 and norm(forb) in nall:
                add("BLOCKING", "PED-002", f"forbidden_in_audio présent : {forb}")

        # COVER: required messages on every path (approx: in concatenated path text)
        req = lesson.get("required_messages") or []
        for path_ids in paths[:200]:
            ptxt = norm(" ".join(collect_child_text(nodes[i]) for i in path_ids if i in nodes))
            missing = []
            for m in req:
                tokens = [t for t in re.split(r"[;/]", m) if t.strip()]
                ok = False
                for t in tokens:
                    t = t.strip().lower()
                    if len(t) < 3:
                        continue
                    # flexible: all significant words
                    words = [w for w in re.findall(r"[a-zàâäéèêëïîôùûüçœ-]{3,}", t) if w not in ("une", "des", "les", "est", "avec", "pour", "dans")]
                    if words and all(w in ptxt for w in words[:2]):
                        ok = True
                        break
                    if t in ptxt:
                        ok = True
                        break
                if tokens and not ok:
                    missing.append(m)
            if missing:
                add("MAJOR", "COVER", f"chemin {path_ids[0]}→{path_ids[-1]} messages manquants: {missing}")
                break  # un rapport par arbre suffit à signaler

        # papa/maman presence for family stories: soft
        if "papa" not in nall and "maman" not in nall and data.get("domain") in ("FAM", "SEC", "SAN", "AUT"):
            add("MAJOR", "GARDEN", "ni papa ni maman nommés")

    # N1 phrase length on audio nodes
    if data.get("age_band") == "N1":
        for v in nodes.values():
            if v.get("type") in ("audio", "feedback", "ending", "transition"):
                for sent in re.split(r"[.!?]+", v.get("text") or ""):
                    sent = sent.strip()
                    if not sent:
                        continue
                    wc = len(sent.split())
                    if wc > 14:
                        add("MINOR", "N1", f"phrase longue ({wc} mots): {sent[:80]}", v.get("id"))

    # auto status: generator must not self-approve as PACKAGE; we may set APPROVED_TEXT
    blocking = sum(1 for f in findings if f["severity"] == "BLOCKING")
    major = sum(1 for f in findings if f["severity"] == "MAJOR")
    if blocking:
        decision = "REJECTED"
    elif major:
        decision = "REVISION_REQUIRED"
    else:
        decision = "APPROVED_TEXT"

    # persist status into file if changed
    val = data.get("validation") or {}
    val["status"] = decision
    val["blocking_findings"] = blocking
    val["major_findings"] = major
    val["paths_tested"] = len(paths) if "paths" in dir() else None
    data["validation"] = val
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return pack(path, data, findings, decision, blocking, major, len(paths))


def pack(path, data, findings, decision=None, blocking=None, major=None, npaths=None):
    if decision is None:
        blocking = sum(1 for f in findings if f["severity"] == "BLOCKING")
        major = sum(1 for f in findings if f["severity"] == "MAJOR")
        decision = "REJECTED" if blocking else ("REVISION_REQUIRED" if major else "APPROVED_TEXT")
    return {
        "file": str(path.relative_to(ROOT)),
        "tree_id": data.get("tree_id"),
        "kind": data.get("kind"),
        "lesson_id": data.get("lesson_id"),
        "age_band": data.get("age_band"),
        "decision": decision,
        "blocking": blocking or 0,
        "major": major or 0,
        "minor": sum(1 for f in findings if f["severity"] == "MINOR"),
        "paths": npaths,
        "findings": findings[:40],
    }


def main():
    lessons = load_lessons()
    files = sorted(ATOM.rglob("*.json")) + sorted(RAMI.rglob("*.json"))
    results = []
    for f in files:
        results.append(validate_story(f, lessons))
    REPORT.mkdir(exist_ok=True)
    summary = {
        "total": len(results),
        "approved_text": sum(1 for r in results if r["decision"] == "APPROVED_TEXT"),
        "revision": sum(1 for r in results if r["decision"] == "REVISION_REQUIRED"),
        "rejected": sum(1 for r in results if r["decision"] == "REJECTED"),
        "atomic": sum(1 for r in results if r.get("kind") == "atomic"),
        "ramifiee": sum(1 for r in results if r.get("kind") == "ramifiee"),
        "results": results,
    }
    out = REPORT / "validation.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = [f"# Rapport validation\n", f"- total: {summary['total']}",
          f"- APPROVED_TEXT: {summary['approved_text']}",
          f"- REVISION_REQUIRED: {summary['revision']}",
          f"- REJECTED: {summary['rejected']}\n"]
    for r in results:
        if r["decision"] != "APPROVED_TEXT":
            md.append(f"## {r['tree_id']} — {r['decision']}")
            md.append(f"`{r['file']}` bloquants={r['blocking']} majeurs={r['major']}")
            for fnd in r["findings"]:
                if fnd["severity"] in ("BLOCKING", "MAJOR"):
                    md.append(f"- **{fnd['severity']}** `{fnd['rule']}` {fnd['msg']}")
            md.append("")
    (REPORT / "validation.md").write_text("\n".join(md), encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("total", "approved_text", "revision", "rejected", "atomic", "ramifiee")}, ensure_ascii=False))
    return 0 if summary["rejected"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
