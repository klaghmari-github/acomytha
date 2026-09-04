#!/usr/bin/env python3
"""F-NAR-008/009 — ATOM-DIF.BES.001-06..08 et 002-01..05."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIMITS = {"N1": 10, "N2": 15, "N3": 16}
ROLES = {"narrateur", "papa", "maman", "enfant-m", "enfant-f", "copain", "copine"}
FORBIDDEN = (
    "on va apprendre",
    "voici le geste",
    "papa sourit",
    "maman sourit",
    "papa est là",
    "maman est là",
    "il était une fois",
    "ceci est l'histoire",
    "aujourd'hui,",
    "aujourd'hui ",
    "tu as fait du bon travail",
    "tu as mis ce que l'adulte a dit",
    "un chuchotement serre",
    "une étape après l'autre",
    "l'histoire est finie. l'histoire est finie",
)
BAD_NAMES = (
    "adèle", "adele", "estelle", "anaïs", "anais", "corentin",
    "hugo", "kenzo", "dounia", "ninon", "octave", "kilian", "maël", "mael",
    "lucas", "céline", "celine", "constentin",
)
BAD_NAMES_WORDS = (
    "tom", "ava", "lila", "côme", "come", "léa", "lea", "lina", "iris", "luca",
)
NEED_001 = ("répéter", "observer d'abord")
NEED_002 = ("proposer", "accepter plusieurs réponses")


def words(s: str) -> int:
    return len(s.replace("'", " ").replace("’", " ").replace("-", " ").split())


def from_script(lines: list[str]) -> tuple[str, str]:
    phrases, out = [], []
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        role, phrase = raw.split("|", 1)
        phrase = phrase.strip()
        out.append(f"{role}|{phrase}")
        phrases.append(phrase)
    return " ".join(phrases), "\n".join(out)


def piper_scale(lines: list[str], kind: str) -> float:
    if kind == "passage_question":
        return 1.28
    first = lines[0].split("|", 1)[0]
    if first.startswith("enfant") or first in ("copain", "copine"):
        return 1.28
    if first in ("papa", "maman"):
        return 1.18
    return 1.22


def make_chunk(src: dict, lines: list[str], sons, extra: dict | None = None) -> dict:
    text, script = from_script(lines)
    nc = dict(src)
    nc["text"] = text
    nc["script"] = script
    nc["text_ssml"] = text
    nc["sons"] = sons if sons is not None else (src.get("sons") or "")
    if nc["sons"] is None:
        nc["sons"] = ""
    nc["length_scale_piper"] = piper_scale(lines, src.get("kind") or "")
    age = extra.get("age") if extra else None
    kind = src.get("kind") or ""
    if kind == "passage_question" or age == "N1":
        nc["rate_label"] = "slow"
    else:
        nc["rate_label"] = "medium"
    if extra:
        for k, v in extra.items():
            if k != "age":
                nc[k] = v
    return nc


def check(sid: str, age: str, chunks: list[dict], need: tuple[str, ...]) -> None:
    lim = LIMITS[age]
    joined = "\n".join(c["script"] for c in chunks)
    low = joined.lower()
    for bad in FORBIDDEN:
        if bad in low:
            raise SystemExit(f"{sid} interdit: {bad}")
    for name in BAD_NAMES:
        if name in low:
            raise SystemExit(f"{sid} prénom hors troupe: {name}")
    for name in BAD_NAMES_WORDS:
        if re.search(rf"\b{re.escape(name)}\b", low):
            raise SystemExit(f"{sid} prénom hors troupe: {name}")
    adults = [ln for ln in joined.splitlines() if ln.startswith("papa|") or ln.startswith("maman|")]
    if not adults:
        raise SystemExit(f"{sid}: aucun papa/maman")
    if not any("?" in a for a in adults):
        raise SystemExit(f"{sid}: aucune question d'adulte")
    aj = " ".join(a.split("|", 1)[1] for a in adults).lower()
    if "bravo" not in aj and "merci" not in aj:
        raise SystemExit(f"{sid}: pas de félicitation de scène")
    if "en ce moment" not in low:
        raise SystemExit(f"{sid}: manque en ce moment")
    if "l'histoire est finie." not in low:
        raise SystemExit(f"{sid}: manque fin")
    all_text = " ".join(c["text"] for c in chunks).lower()
    for m in need:
        if m.lower() not in all_text:
            raise SystemExit(f"{sid}: message manquant: {m}")
    first = chunks[0]["script"].splitlines()[0].split("|", 1)[1].lower()
    for bad in ("joue au salon", "est dans l'entrée", "c'est le matin"):
        if bad in first:
            raise SystemExit(f"{sid} ouverture brutale: {first}")
    nwords = sum(words(c["text"]) for c in chunks)
    if nwords < 400:
        raise SystemExit(f"{sid}: trop court ({nwords} mots)")
    for c in chunks:
        rebuilt, _ = from_script(c["script"].splitlines())
        if rebuilt != c["text"]:
            raise SystemExit(f"{sid} {c['chunk_id']}: text ≠ script")
        for ln in c["script"].splitlines():
            if "|" not in ln:
                raise SystemExit(f"{sid} ligne sans | : {ln}")
            role, phrase = ln.split("|", 1)
            if role not in ROLES:
                raise SystemExit(f"{sid} rôle {role}")
            n = words(phrase)
            if n > lim:
                raise SystemExit(f"{sid} {c['chunk_id']} {n}>{lim}: {phrase}")
            if n == 0:
                raise SystemExit(f"{sid} phrase vide")
            if not phrase.endswith((".", "?", "!")):
                raise SystemExit(f"{sid} sans ponctuation: {phrase}")
            if phrase.count(".") + phrase.count("?") + phrase.count("!") > 1:
                raise SystemExit(f"{sid} plusieurs phrases: {phrase}")
    print(f"OK {sid} {nwords} mots  1re: {chunks[0]['script'].splitlines()[0].split('|',1)[1]}")


def write_story(
    sid: str,
    fil: str,
    title: str,
    chars: str,
    setting: str,
    scripts: dict,
    sons: dict,
    extras: dict | None = None,
    relecture: str = "",
) -> None:
    folder = ROOT / sid
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"{sid} chunks missing={missing} extra={extra_ids}")
    extras = extras or {}
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        extra = dict(extras.get(cid) or {})
        extra["age"] = src.get("age_band")
        by[cid] = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), extra)
    out = dict(src)
    out["fil_rouge"] = fil
    out["title"] = title
    out["characters"] = chars
    out["setting"] = setting
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    lesson = out.get("lesson_id") or ""
    need = NEED_001 if lesson.endswith("001") else NEED_002
    check(sid, out["age_band"], out["chunks"], need)
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"# {sid} — {title}\n\n"
        f"Relu : ouverture, désir, imprévu, question, résolution, fin. "
        f"`chunk_id` / `kind` inchangés.\n\n"
        f"## Vécu\n{relecture}\n\n"
        f"## Non vérifié\nAudio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )


Q001 = {
    "expected_answer": "répéter",
    "accepted_examples": "répéter | observer d'abord | observer | attendre",
    "retry_prompt": "On peut répéter. On peut observer d'abord. Que fait-on ?",
}
Q002_PROP = {
    "expected_answer": "proposer",
    "accepted_examples": "proposer | inviter | accepter | d'accord",
    "retry_prompt": "On peut proposer. On peut accepter. Que fait-on ?",
}
Q002_ACC = {
    "expected_answer": "accepter",
    "accepted_examples": "accepter | proposer | un non | regarder",
}


# ---------------------------------------------------------------------------
# 001-06 N1 Raphaël, Aniss — train sous la table
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.BES.001-06",
    "Raphaël veut que son train de bois passe sous la table jusqu'à la chaise. Aniss reste près du buffet. Raphaël répète : un wagon, puis on attend. Aniss observe d'abord, puis pose le wagon rouge. Le train arrive.",
    "Le train sous la table",
    "Raphaël, Aniss, papa, maman",
    "cuisine, matin, nappe à carreaux",
    {
        "CHK_T0000_P0000": [
            "narrateur|La confiture d'abricot brille dans le pot.",
            "narrateur|Elle est orange et un peu épaisse.",
            "narrateur|Le pain grillé sent encore le four.",
            "narrateur|Une miette colle à la nappe.",
            "narrateur|La nappe a des carreaux rouges.",
            "narrateur|Papa essuie la cuillère de bois.",
            "papa|Raphaël, tu veux de la confiture ?",
            "enfant-m|Oui, papa.",
            "enfant-m|Un peu, s'il te plaît.",
            "narrateur|Maman ouvre le tiroir du bas.",
            "narrateur|Dedans, le train de bois attend.",
            "narrateur|Les wagons sont lisses et froids.",
            "maman|Tu as vu le train, Raphaël ?",
            "enfant-m|Oui.",
            "enfant-m|Il va sous la table.",
            "maman|Jusqu'à la chaise ?",
            "enfant-m|Oui.",
            "enfant-m|Le wagon rouge aussi.",
            "narrateur|En ce moment, Raphaël s'assoit.",
            "narrateur|Le carrelage est un peu froid.",
            "narrateur|Il pose un wagon brun.",
            "narrateur|Ça fait un petit clic.",
            "papa|Tu as entendu le clic ?",
            "enfant-m|Oui, papa.",
            "narrateur|Maman ouvre la porte.",
            "narrateur|Aniss arrive tout doux.",
            "narrateur|Il reste près du buffet.",
            "narrateur|Ses mains touchent le bois.",
            "narrateur|Il a besoin de calme.",
            "enfant-m|Aniss.",
            "enfant-m|Tu viens ?",
            "narrateur|Aniss ne vient pas encore.",
            "enfant-m|Le wagon rouge est pour lui.",
            "narrateur|Raphaël regarde papa.",
            "papa|On peut répéter, tout doux.",
            "maman|On peut observer d'abord.",
            "enfant-m|D'accord.",
            "narrateur|Le wagon rouge attend par terre.",
            "narrateur|Il est lisse et froid.",
            "papa|Tu parles tout bas, d'accord ?",
            "enfant-m|D'accord, papa.",
            "narrateur|Une miette est sur le wagon.",
            "papa|Tu as vu la miette ?",
            "enfant-m|Oui.",
            "narrateur|Raphaël souffle.",
            "narrateur|La miette part.",
            "maman|Le train peut avancer un peu.",
            "narrateur|Raphaël pousse le wagon brun.",
            "narrateur|Aniss regarde, près du buffet.",
            "narrateur|Ses pieds restent au même endroit.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Aniss a besoin de calme.",
            "narrateur|Que peut-on faire ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Raphaël va près du buffet.",
            "narrateur|Il parle tout bas.",
            "enfant-m|Un wagon.",
            "enfant-m|Puis on attend.",
            "narrateur|C'est répéter, tout doux.",
            "narrateur|Aniss écoute.",
            "narrateur|Il va observer d'abord.",
            "narrateur|Ses mains restent sur le bois.",
            "narrateur|Raphaël pose un wagon bleu.",
            "narrateur|Il attend.",
            "papa|Tu as répété, Raphaël ?",
            "enfant-m|Oui, papa.",
            "maman|Aniss peut regarder.",
            "narrateur|Aniss avance un pied.",
            "narrateur|Puis il s'arrête.",
            "narrateur|Il observe d'abord.",
            "papa|C'est bien.",
            "narrateur|Le train a trois wagons.",
            "enfant-m|Il manque le rouge.",
            "maman|Il attend encore un peu.",
            "narrateur|Raphaël pousse le train.",
            "narrateur|Il passe près du buffet.",
            "narrateur|Aniss suit des yeux.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Plus tard, Aniss tend la main.",
            "narrateur|Il prend le wagon rouge.",
            "narrateur|Il le pose, tout doux.",
            "narrateur|Ça fait clic.",
            "enfant-m|Merci, Aniss.",
            "papa|Tu as laissé le temps.",
            "maman|Bravo, Raphaël.",
            "narrateur|Le train passe sous la table.",
            "narrateur|Il va vers la chaise.",
            "enfant-m|Il arrive, papa ?",
            "papa|Bientôt.",
            "narrateur|Un pied de chaise est proche.",
            "narrateur|Le train le touche.",
            "enfant-m|Il est arrivé.",
            "maman|Oui.",
            "maman|Jusqu'à la chaise.",
            "narrateur|Raphaël souffle comme un sifflet.",
            "narrateur|Aniss souffle un tout petit peu.",
            "papa|Tu as fini ton train ?",
            "enfant-m|Oui, papa.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le wagon rouge brille encore.",
            "enfant-m|On a attendu.",
            "enfant-m|Aniss a regardé d'abord.",
            "maman|Puis le train a avancé.",
            "papa|Oui.",
            "narrateur|La confiture sent encore bon.",
            "narrateur|Une miette reste sur la nappe.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "cuisine,bois",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "bois",
        "CHK_T0000_P0000_END": "bois",
        "CHK_T0000_P0000_END_F0001": "",
    },
    extras={"CHK_T0000_P0000_Q0001": Q001},
    relecture=(
        "Cuisine, confiture d'abricot, nappe à carreaux. Raphaël veut le train "
        "sous la table jusqu'à la chaise. Aniss reste au buffet. Une miette sur "
        "le wagon. Raphaël répète, Aniss observe d'abord, pose le rouge. Le train arrive."
    ),
)


# ---------------------------------------------------------------------------
# 001-07 N2 Victorina, Chouchou — magasin en carton
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.BES.001-07",
    "Victorina veut la poire de bois du magasin en carton. Elle reste près de l'escalier. Chouchou répète : un fruit, on dit le nom. Elle observe d'abord, puis montre la poire. La clochette ferme le magasin.",
    "La poire du magasin",
    "Victorina, Chouchou, papa, maman",
    "véranda, draps au soleil",
    {
        "CHK_T0000_P0000": [
            "narrateur|Des draps blancs sèchent sur la véranda.",
            "narrateur|Le soleil passe à travers le linge.",
            "narrateur|Ça fait des taches chaudes au sol.",
            "narrateur|Une pince à linge claque, tout doux.",
            "narrateur|Ça sent le savon, tout près.",
            "narrateur|Un carton ouvert sert de magasin.",
            "narrateur|Dessus, des fruits de bois.",
            "narrateur|Une pomme.",
            "narrateur|Une banane.",
            "narrateur|Une poire claire.",
            "narrateur|Une clochette attend dans une chaussette.",
            "papa|Tu as senti le drap, Victorina ?",
            "enfant-f|Oui, papa.",
            "enfant-f|Il est encore un peu humide.",
            "maman|On parle tout doux, d'accord ?",
            "enfant-f|D'accord.",
            "narrateur|En ce moment, Chouchou pose la pomme.",
            "narrateur|Le bois est lisse et tiède.",
            "copain|Le magasin est ouvert.",
            "copain|Un fruit.",
            "copain|On dit le nom.",
            "narrateur|Victorina reste près de l'escalier.",
            "narrateur|Le bois de l'escalier est frais.",
            "narrateur|Elle a besoin de calme.",
            "enfant-f|La poire est pour moi.",
            "narrateur|Ses mains restent sur la rampe.",
            "copain|Victorina.",
            "copain|Tu viens ?",
            "narrateur|Victorina ne vient pas encore.",
            "papa|On peut répéter la règle.",
            "maman|On peut observer d'abord.",
            "copain|D'accord.",
            "narrateur|Chouchou va près de l'escalier.",
            "narrateur|Il parle tout bas.",
            "narrateur|La clochette bouge dans la chaussette.",
            "papa|Tu as entendu la clochette ?",
            "enfant-f|Un tout petit peu.",
            "maman|Elle est dans la chaussette.",
            "maman|Elle sonne moins fort.",
            "narrateur|Victorina regarde la poire.",
            "narrateur|La poire a une petite feuille peinte.",
            "enfant-f|Elle est claire.",
            "papa|Oui.",
            "papa|Elle attend.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Victorina a besoin de calme.",
            "narrateur|Que peut-on faire ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Chouchou répète, tout bas.",
            "copain|Un fruit.",
            "copain|On dit le nom.",
            "narrateur|Victorina écoute.",
            "narrateur|Elle va observer d'abord.",
            "narrateur|Elle regarde la pomme.",
            "copain|Pomme.",
            "narrateur|Il la pose sur le carton.",
            "narrateur|Ça fait un petit toc.",
            "maman|Observer d'abord, c'est possible.",
            "narrateur|Victorina avance un pied.",
            "narrateur|Puis elle s'arrête.",
            "papa|Tu vois la poire, Victorina ?",
            "enfant-f|Oui.",
            "enfant-f|La petite feuille.",
            "narrateur|Chouchou montre la banane.",
            "copain|Banane.",
            "narrateur|Victorina suit des yeux.",
            "narrateur|Elle ne prend pas encore.",
            "maman|Tu as répété, Chouchou ?",
            "copain|Oui.",
            "papa|Victorina peut regarder.",
            "narrateur|Un coin de drap claque un peu.",
            "narrateur|Le soleil a bougé.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Plus tard, Victorina tend la main.",
            "narrateur|Elle prend la poire de bois.",
            "narrateur|Elle la montre, tout doux.",
            "enfant-f|Poire.",
            "copain|Oui.",
            "narrateur|Elle pose la poire sur le carton.",
            "papa|Tu as observé d'abord.",
            "maman|Bravo, Chouchou.",
            "maman|Tu as répété tout bas.",
            "narrateur|Chouchou sort la clochette.",
            "narrateur|Il la secoue une fois.",
            "narrateur|Ça fait un son mou.",
            "enfant-f|Le magasin ferme ?",
            "copain|Oui.",
            "copain|La poire reste.",
            "papa|Tu as fini ta poire ?",
            "enfant-f|Oui, papa.",
            "narrateur|Les draps bougent encore.",
            "narrateur|Ça sent toujours le savon.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|La poire claire brille sur le carton.",
            "enfant-f|J'ai regardé d'abord.",
            "copain|J'ai répété.",
            "maman|Puis la poire est arrivée.",
            "papa|Oui.",
            "narrateur|La clochette dort dans la chaussette.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "draps,bois",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "bois",
        "CHK_T0000_P0000_END": "clochette",
        "CHK_T0000_P0000_END_F0001": "",
    },
    extras={"CHK_T0000_P0000_Q0001": dict(Q001, retry_prompt="On répète la règle. Victorina peut quoi d'abord ?")},
    relecture=(
        "Véranda, draps au soleil, magasin en carton. Victorina veut la poire de bois. "
        "Elle reste à l'escalier. Chouchou répète. La clochette est dans une chaussette. "
        "Elle observe d'abord, puis montre la poire. Le magasin ferme."
    ),
)


# ---------------------------------------------------------------------------
# 001-08 N3 Sarah, Victorino — bateau dans la bassine
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.BES.001-08",
    "Sarah veut que le bateau de bois traverse la bassine. Victorino reste près de la porte du cabanon. Elle répète : on pousse, puis on attend. Il observe d'abord. Sur la serviette, même jeu. Le bateau touche l'autre bord.",
    "Le bateau dans la bassine",
    "Sarah, Victorino, papa, maman",
    "jardin, cabanon, fin d'après-midi",
    {
        "CHK_T0000_P0000": [
            "narrateur|La mousse du robinet sent le bois mouillé.",
            "narrateur|Une goutte tombe dans la bassine.",
            "narrateur|Elle fait un petit rond.",
            "narrateur|Le soleil est bas, tout orange.",
            "narrateur|Le cabanon a une porte peinte en vert.",
            "narrateur|La peinture s'écaille un peu.",
            "narrateur|Un bateau de bois flotte, tout léger.",
            "narrateur|Sa voile est un carré de tissu.",
            "maman|Tu as vu le rond, Sarah ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Il grandit, puis il part.",
            "papa|L'eau est tiède, ce soir.",
            "enfant-f|Je veux qu'il traverse.",
            "enfant-f|Jusqu'à l'autre bord.",
            "maman|Avec la voile ?",
            "enfant-f|Oui.",
            "narrateur|En ce moment, Sarah touche le bateau.",
            "narrateur|Le bois est lisse et humide.",
            "narrateur|Victorino reste près de la porte.",
            "narrateur|Il tient le bord du cabanon.",
            "narrateur|Il a besoin de calme.",
            "enfant-f|Victorino.",
            "enfant-f|Tu pousses avec moi ?",
            "narrateur|Victorino ne vient pas encore.",
            "papa|On peut répéter, tout doux.",
            "maman|On peut observer d'abord.",
            "enfant-f|D'accord.",
            "narrateur|Une feuille tombe dans l'eau.",
            "narrateur|Elle devient une petite île.",
            "papa|Tu as vu la feuille, Sarah ?",
            "enfant-f|Oui.",
            "enfant-f|Le bateau peut tourner autour.",
            "maman|Oui.",
            "maman|Sans presser.",
            "narrateur|Sarah pose un doigt sur l'eau.",
            "narrateur|L'eau est tiède, comme papa a dit.",
            "narrateur|Victorino regarde depuis la porte.",
            "narrateur|Ses pieds restent sur la pierre.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Victorino a besoin de calme.",
            "narrateur|Que peut-on faire ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Sarah va près de la porte.",
            "narrateur|Elle répète, tout bas.",
            "enfant-f|On pousse.",
            "enfant-f|Puis on attend.",
            "narrateur|Victorino écoute.",
            "narrateur|Il va observer d'abord.",
            "narrateur|Sarah pousse le bateau un peu.",
            "narrateur|Elle attend.",
            "narrateur|Le bateau tourne autour de la feuille.",
            "papa|Tu as vu le tour, Victorino ?",
            "copain|Oui.",
            "maman|Observer d'abord, c'est possible.",
            "narrateur|Victorino avance un pas.",
            "narrateur|Puis il s'arrête.",
            "narrateur|Il observe d'abord.",
            "enfant-f|La voile est mouillée, en bas.",
            "papa|Oui.",
            "papa|Elle tient encore.",
            "narrateur|Sarah pousse encore un peu.",
            "narrateur|Le bateau n'est pas à l'autre bord.",
            "maman|Tu as répété, Sarah ?",
            "enfant-f|Oui, maman.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Plus tard, maman pose une serviette.",
            "narrateur|La serviette est chaude de soleil.",
            "narrateur|C'est un quai, tout doux.",
            "papa|Même jeu, autre lieu.",
            "enfant-f|On pousse.",
            "enfant-f|Puis on attend.",
            "narrateur|Victorino s'assoit au bord.",
            "narrateur|Il observe d'abord.",
            "narrateur|Puis il pose un doigt.",
            "narrateur|Le bateau avance encore.",
            "narrateur|Il touche l'autre bord.",
            "enfant-f|Il est arrivé.",
            "copain|Moi aussi, j'ai poussé.",
            "maman|Tu as laissé le temps, Sarah.",
            "papa|Bravo.",
            "papa|La voile a tenu.",
            "narrateur|Une goutte reste sur le bois.",
            "enfant-f|On souffle ?",
            "papa|Oui.",
            "narrateur|Ils soufflent sur la voile.",
            "narrateur|Le tissu tremble un peu.",
            "maman|Tu as fini la traversée ?",
            "enfant-f|Oui, maman.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le bateau repose contre le bord.",
            "enfant-f|On a répété.",
            "enfant-f|Victorino a observé d'abord.",
            "maman|Puis il a touché l'eau.",
            "papa|Oui.",
            "narrateur|La feuille flotte encore, toute seule.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "eau,bois",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "eau",
        "CHK_T0000_P0000_END": "eau,tissu",
        "CHK_T0000_P0000_END_F0001": "",
    },
    extras={"CHK_T0000_P0000_Q0001": dict(Q001, retry_prompt="On répète la règle. Victorino peut quoi d'abord ?")},
    relecture=(
        "Jardin, mousse du robinet, bassine, bateau de bois. Sarah veut la traversée. "
        "Victorino reste à la porte du cabanon. Une feuille devient une île. "
        "Elle répète, il observe d'abord. Serviette-quai. Le bateau touche l'autre bord."
    ),
)


# ---------------------------------------------------------------------------
# 002-01 N1 Nino, Victorina — cheval et pont
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.BES.002-01",
    "Nino veut que le cheval de bois traverse un pont en carton. Il propose. Victorina dit non, puis je regarde, puis plus tard. Nino accepte. Le pont se plie, il l'aplatit. Le cheval passe. Un mouton s'approche.",
    "Le cheval et le pont",
    "Nino, Victorina, papa, maman",
    "cuisine après gâteaux, carton de céréales",
    {
        "CHK_T0000_P0000": [
            "narrateur|De la farine blanche dort sur les manches de papa.",
            "narrateur|La plaque de gâteaux refroidit.",
            "narrateur|Ça sent le beurre encore chaud.",
            "narrateur|Une miette sucrée colle au bois.",
            "narrateur|Un carton de céréales est à plat.",
            "narrateur|Des lettres bleues restent dessus.",
            "narrateur|Nino l'a plié en pont.",
            "narrateur|Un cheval de bois attend.",
            "narrateur|Sa crinière est peinte en brun.",
            "narrateur|Un mouton de bois aussi.",
            "maman|Tu as vu la farine, Nino ?",
            "enfant-m|Oui, maman.",
            "enfant-m|Sur les manches.",
            "papa|Les gâteaux attendent un peu.",
            "papa|On reste par terre.",
            "enfant-m|Le cheval va sur le pont.",
            "maman|Jusqu'à l'autre côté ?",
            "enfant-m|Oui.",
            "enfant-m|Le mouton après.",
            "narrateur|En ce moment, Nino pose le pont.",
            "narrateur|Le carton est un peu rêche.",
            "narrateur|Il appuie les deux bords.",
            "narrateur|Maman ouvre la porte.",
            "narrateur|Victorina arrive.",
            "narrateur|Elle a des chaussettes jaunes.",
            "enfant-m|Tu viens ?",
            "copine|Non.",
            "narrateur|Nino regarde papa.",
            "papa|On peut proposer.",
            "maman|On peut accepter plusieurs réponses.",
            "papa|Oui.",
            "papa|Non.",
            "papa|Regarder.",
            "papa|Plus tard.",
            "enfant-m|D'accord.",
            "narrateur|Nino pousse le cheval.",
            "narrateur|Les sabots glissent un peu.",
            "narrateur|Le pont se plie au milieu.",
            "enfant-m|Oh.",
            "papa|Tu as vu le pli, Nino ?",
            "enfant-m|Oui.",
            "narrateur|Nino aplatit le carton.",
            "narrateur|Il passe la main dessus.",
            "narrateur|Le pont redevient droit.",
            "maman|Tu proposes encore, tout doux ?",
            "enfant-m|Plus tard, tu viens ?",
            "copine|Je regarde.",
            "papa|Regarder, c'est une réponse.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Nino invite Victorina.",
            "narrateur|Que fait-on ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Nino a su proposer.",
            "narrateur|Il accepte plusieurs réponses.",
            "enfant-m|D'accord.",
            "narrateur|Victorina s'assoit près du buffet.",
            "narrateur|Elle regarde le cheval.",
            "narrateur|Nino pousse encore.",
            "narrateur|Les sabots tapent le carton.",
            "papa|Tu as entendu les sabots ?",
            "enfant-m|Oui, papa.",
            "enfant-m|Tu veux le mouton ?",
            "copine|Plus tard.",
            "enfant-m|D'accord.",
            "maman|Plusieurs réponses sont possibles.",
            "narrateur|Le cheval avance au milieu.",
            "narrateur|Le pont tient.",
            "papa|Tu as aplati le pli.",
            "enfant-m|Oui.",
            "narrateur|Une miette tombe près du pont.",
            "narrateur|Nino la pousse du doigt.",
            "narrateur|Victorina avance un peu.",
            "narrateur|Elle reste à regarder.",
            "maman|C'est bien.",
            "maman|Le beurre sent encore.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Plus tard, Victorina tend la main.",
            "narrateur|Elle pose le mouton près du pont.",
            "enfant-m|Merci.",
            "papa|Tu as accepté, Nino ?",
            "enfant-m|Oui, papa.",
            "maman|Bravo.",
            "narrateur|Le cheval finit le pont.",
            "narrateur|Il arrive de l'autre côté.",
            "enfant-m|Il est passé.",
            "copine|Le mouton aussi, après.",
            "papa|Clip, clop.",
            "enfant-m|Clip, clop.",
            "maman|Les gâteaux sont tièdes, maintenant.",
            "papa|On range le pont ?",
            "enfant-m|Oui.",
            "narrateur|Nino plie le carton.",
            "narrateur|Les lettres bleues se plient aussi.",
            "narrateur|Victorina pose le cheval.",
            "narrateur|Le mouton reste près d'elle.",
            "papa|Tu as fini le pont ?",
            "enfant-m|Oui, papa.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le cheval repose près du mouton.",
            "enfant-m|J'ai proposé.",
            "enfant-m|J'ai accepté.",
            "maman|Plusieurs réponses sont possibles.",
            "papa|Oui.",
            "narrateur|La farine dort encore sur les manches.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "cuisine,carton",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "bois",
        "CHK_T0000_P0000_END": "bois",
        "CHK_T0000_P0000_END_F0001": "",
    },
    extras={"CHK_T0000_P0000_Q0001": Q002_PROP},
    relecture=(
        "Cuisine, farine sur les manches, gâteaux. Nino veut le cheval sur le pont en carton. "
        "Victorina dit non, puis je regarde, puis plus tard. Le pont se plie. "
        "Nino accepte. Le cheval passe. Le mouton s'approche."
    ),
)


# ---------------------------------------------------------------------------
# 002-02 N2 Mila, Aniss — cerf-volant de papier
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.BES.002-02",
    "Mila veut que son cerf-volant de papier se lève au-dessus de la lavande. Elle propose. Aniss dit je regarde, puis plus tard, puis non pour la ficelle. Mila accepte. Une abeille passe. L'ombre du cerf-volant glisse sur les fleurs.",
    "Le cerf-volant de papier",
    "Mila, Aniss, papa, maman",
    "terrasse, lavande, après la sieste",
    {
        "CHK_T0000_P0000": [
            "narrateur|La pierre de la terrasse est encore chaude.",
            "narrateur|La lavande sent fort, tout près.",
            "narrateur|Des tiges violettes bougent un peu.",
            "narrateur|Des cigales chantent dans l'olivier.",
            "narrateur|Un cerf-volant de papier attend sur la chaise.",
            "narrateur|Il est bleu, avec une queue blanche.",
            "narrateur|La ficelle est enroulée, un peu rêche.",
            "maman|Je pose le chapeau sur le banc.",
            "papa|Je remplis le verre d'eau.",
            "maman|Tu entends les cigales, Mila ?",
            "enfant-f|Oui, maman.",
            "papa|La pierre est chaude, hein ?",
            "enfant-f|Oui, papa.",
            "enfant-f|Je veux qu'il se lève.",
            "enfant-f|Au-dessus de la lavande.",
            "maman|Un tout petit vent suffit.",
            "narrateur|En ce moment, Mila prend le papier.",
            "narrateur|Il est léger et un peu froissé.",
        ],
        "CHK_T0000_P0000_X": [
            "narrateur|Aniss est sur la marche.",
            "narrateur|Ses pieds restent à l'ombre.",
            "narrateur|Mila tient la ficelle.",
            "enfant-f|Tu viens ?",
            "copain|Je regarde.",
            "narrateur|Mila accepte.",
            "maman|On peut proposer.",
            "maman|On peut accepter plusieurs réponses.",
            "papa|Oui.",
            "papa|Non.",
            "papa|Regarder.",
            "papa|Plus tard.",
            "enfant-f|D'accord.",
            "narrateur|Mila lève le papier.",
            "narrateur|Le vent le fait trembler.",
            "narrateur|Aniss reste sur la marche.",
            "narrateur|Il regarde la queue blanche.",
            "enfant-f|Plus tard ?",
            "copain|Plus tard.",
            "enfant-f|D'accord.",
            "papa|Tu as accepté, Mila ?",
            "enfant-f|Oui, papa.",
            "maman|Regarder, c'est une réponse.",
            "narrateur|Une abeille passe sur la lavande.",
            "narrateur|Elle fait un petit bruit.",
            "maman|Tu l'entends, Mila ?",
            "enfant-f|Oui.",
            "papa|On attend qu'elle parte.",
            "narrateur|Mila tient le papier bas.",
            "narrateur|L'abeille s'en va.",
            "enfant-f|Tu veux la ficelle ?",
            "copain|Non.",
            "enfant-f|D'accord.",
            "papa|Plusieurs réponses sont possibles.",
            "narrateur|Le cerf-volant tremble encore.",
            "narrateur|Aniss avance un pied.",
            "narrateur|Puis il le retire.",
        ],
        "CHK_T0000_P0000_X_Q0001": [
            "narrateur|Mila invite Aniss.",
            "narrateur|Que fait-elle ?",
        ],
        "CHK_T0000_P0000_X_C0001": [
            "narrateur|Mila a su proposer.",
            "narrateur|Elle a su accepter plusieurs réponses.",
            "papa|Aniss a dit regarder, puis plus tard.",
            "maman|Oui.",
            "maman|Tout ça va.",
            "enfant-f|J'ai dit d'accord.",
            "papa|Bravo.",
            "papa|Tu as tenu la ficelle.",
            "narrateur|Le papier se lève un peu.",
            "narrateur|L'ombre passe sur la lavande.",
            "enfant-f|Tu vois l'ombre, Aniss ?",
            "copain|Je regarde.",
            "maman|C'est une réponse.",
            "narrateur|Mila recule d'un pas.",
            "narrateur|La queue blanche danse.",
            "narrateur|Une tige de lavande se plie.",
            "papa|Le vent est juste assez.",
        ],
        "CHK_T0000_P0000_X_END": [
            "maman|On repose le papier ?",
            "enfant-f|Encore un peu.",
            "narrateur|L'ombre glisse sur deux tiges.",
            "narrateur|Aniss suit des yeux.",
            "papa|Tu as fini de jouer, Mila ?",
            "enfant-f|Oui, papa.",
            "narrateur|Mila pose le cerf-volant.",
            "narrateur|Il retrouve la chaise.",
            "narrateur|Aniss secoue un pied.",
            "narrateur|Un peu de poussière tombe.",
            "maman|Merci, Aniss.",
            "maman|Tu as regardé.",
            "papa|La lavande sent encore.",
            "enfant-f|L'ombre était jolie.",
            "papa|Oui.",
        ],
        "CHK_T0000_P0000_X_END_F0001": [
            "narrateur|Le cerf-volant bleu dort sur la chaise.",
            "enfant-f|J'ai proposé.",
            "enfant-f|J'ai accepté.",
            "maman|Plusieurs réponses sont possibles.",
            "papa|Oui.",
            "narrateur|Les cigales chantent encore.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "terrasse,cigales",
        "CHK_T0000_P0000_X": "vent,papier",
        "CHK_T0000_P0000_X_Q0001": "",
        "CHK_T0000_P0000_X_C0001": "vent",
        "CHK_T0000_P0000_X_END": "",
        "CHK_T0000_P0000_X_END_F0001": "",
    },
    extras={
        "CHK_T0000_P0000_X_Q0001": dict(
            Q002_ACC,
            retry_prompt="Elle propose. Aniss peut regarder. Que fait Mila ?",
        )
    },
    relecture=(
        "Terrasse chaude, lavande, cigales. Mila veut lever le cerf-volant de papier. "
        "Aniss dit je regarde, plus tard, non pour la ficelle. Une abeille passe. "
        "Mila accepte. L'ombre glisse sur les fleurs. Le papier retrouve la chaise."
    ),
)


# ---------------------------------------------------------------------------
# 002-03 N3 Amir, Sarah — raisins du gâteau puis balcon
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.BES.002-03",
    "Amir veut poser des raisins en rond sur le gâteau. Il propose. Sarah dit non, puis je regarde, puis plus tard. Un raisin roule. Au balcon, il propose l'arrosoir. Sarah pose un raisin. Le rond est fini.",
    "Les raisins du gâteau",
    "Amir, Sarah, papa, maman",
    "cuisine puis balcon",
    {
        "CHK_T0000_P0000": [
            "narrateur|La vanille chaude sort du four, toute douce.",
            "narrateur|Un petit gâteau refroidit sur la grille.",
            "narrateur|La grille fait un tout petit tic.",
            "narrateur|Il a des trous, tout légers.",
            "narrateur|Un bol de raisins secs attend.",
            "narrateur|Les raisins sont sombres et un peu collants.",
            "narrateur|Une cuillère de bois repose à côté.",
            "maman|Tu as senti la vanille, Amir ?",
            "enfant-m|Oui, maman.",
            "enfant-m|C'est sucré.",
            "papa|Les raisins sont prêts.",
            "papa|Le gâteau aussi.",
            "maman|On décore un peu, d'accord ?",
            "enfant-m|D'accord.",
            "enfant-m|Un rond de raisins.",
            "narrateur|En ce moment, Amir tient un raisin.",
            "narrateur|Il est collant, entre deux doigts.",
            "narrateur|Maman ouvre la porte.",
            "narrateur|Sarah arrive.",
            "narrateur|Elle a une barrette bleue.",
            "enfant-m|Tu viens ?",
            "copine|Non.",
            "narrateur|Amir regarde papa.",
            "papa|On peut proposer.",
            "maman|On peut accepter plusieurs réponses.",
            "papa|Oui.",
            "papa|Non.",
            "papa|Regarder.",
            "papa|Plus tard.",
            "enfant-m|D'accord.",
            "narrateur|Amir pose un raisin.",
            "narrateur|Un autre raisin roule sous le bol.",
            "enfant-m|Il est parti.",
            "papa|Tu as vu le raisin, Amir ?",
            "enfant-m|Oui.",
            "narrateur|Amir penche le bol.",
            "narrateur|Le raisin revient, tout collant.",
            "maman|Tu proposes encore, tout doux ?",
            "enfant-m|Tu as vu le gâteau, Sarah ?",
            "copine|Je regarde.",
            "papa|Regarder, c'est une réponse.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Amir invite Sarah.",
            "narrateur|Que fait-on ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Amir a su proposer.",
            "narrateur|Il accepte plusieurs réponses.",
            "enfant-m|D'accord.",
            "narrateur|Sarah s'assoit près du buffet.",
            "narrateur|Elle regarde le rond.",
            "narrateur|Le rond a trois raisins.",
            "maman|Il en manque, hein ?",
            "enfant-m|Oui.",
            "enfant-m|Tu veux un raisin ?",
            "copine|Plus tard.",
            "enfant-m|D'accord.",
            "papa|Plusieurs réponses sont possibles.",
            "narrateur|Plus tard, au balcon, l'air est frais.",
            "narrateur|Une jardinière sent la terre.",
            "narrateur|Un arrosoir rouge s'appuie au rebord.",
            "narrateur|Amir se souvient.",
            "enfant-m|Tu veux l'arrosoir ?",
            "copine|Je regarde.",
            "maman|On accepte plusieurs réponses.",
            "narrateur|Amir soulève l'arrosoir.",
            "narrateur|Une goutte tombe sur la pierre.",
            "papa|C'est bien.",
            "enfant-m|Plus tard, tu viens ?",
            "copine|Plus tard.",
            "enfant-m|D'accord.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Ils rentrent près du gâteau.",
            "narrateur|La vanille est plus douce, maintenant.",
            "narrateur|Sarah hoche la tête.",
            "narrateur|Elle pose un raisin.",
            "narrateur|Le raisin colle un peu.",
            "narrateur|Puis elle s'arrête.",
            "narrateur|Amir accepte.",
            "maman|Tu as su proposer.",
            "papa|Tu as su accepter.",
            "maman|Bravo, Amir.",
            "narrateur|Amir pose le dernier raisin.",
            "narrateur|Le rond est fini.",
            "narrateur|Il brille un peu, au milieu.",
            "enfant-m|Il est rond, papa.",
            "papa|Oui.",
            "papa|Tout autour.",
            "maman|On range le bol ?",
            "enfant-m|Oui.",
            "narrateur|Sarah range un raisin tombé.",
            "papa|Tu as fini le rond, Amir ?",
            "enfant-m|Oui, papa.",
            "narrateur|La vanille sent encore, tout doux.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le gâteau a son rond de raisins.",
            "enfant-m|J'ai proposé.",
            "enfant-m|J'ai accepté.",
            "maman|Plusieurs réponses sont possibles.",
            "papa|Oui.",
            "narrateur|L'arrosoir rouge s'appuie encore au rebord.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "four,cuisine",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "balcon",
        "CHK_T0000_P0000_END": "cuisine",
        "CHK_T0000_P0000_END_F0001": "",
    },
    extras={"CHK_T0000_P0000_Q0001": Q002_PROP},
    relecture=(
        "Vanille, petit gâteau, raisins. Amir veut un rond. Sarah dit non, je regarde, plus tard. "
        "Un raisin roule sous le bol. Au balcon, l'arrosoir. Elle pose un raisin. Le rond est fini."
    ),
)


# ---------------------------------------------------------------------------
# 002-04 N2 Nina, Victorino — collier de maman
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.BES.002-04",
    "Nina veut enfiler un collier de perles de bois pour maman. Elle propose. Victorino regarde, dit plus tard, dit non pour une perle. Une perle se cache dans la dentelle. Nina accepte. Maman met le collier. Il tape tout doux.",
    "Le collier de maman",
    "Nina, Victorino, papa, maman",
    "salon, boîte à couture, rideau de dentelle",
    {
        "CHK_T0000_P0000": [
            "narrateur|La boîte à couture sent la cire.",
            "narrateur|Le couvercle est lisse, un peu chaud.",
            "narrateur|Une pelote de laine dort dans un coin.",
            "narrateur|La laine est grise, un peu rêche.",
            "narrateur|Dedans, des perles de bois dorment.",
            "narrateur|Brunes.",
            "narrateur|Beiges.",
            "narrateur|Une rouge, toute ronde.",
            "narrateur|Le rideau de dentelle fait des trous de lumière.",
            "narrateur|Un carré de soleil touche le fil.",
            "papa|Tu as senti la cire, Nina ?",
            "enfant-f|Oui, papa.",
            "enfant-f|Ça sent le bois aussi.",
            "maman|On reste au sec, d'accord ?",
            "enfant-f|D'accord, maman.",
            "enfant-f|Je fais un collier.",
            "enfant-f|Pour toi.",
            "maman|Pour moi ?",
            "enfant-f|Oui.",
            "narrateur|En ce moment, Nina prend un fil.",
            "narrateur|Le fil est un peu raide.",
            "narrateur|Victorino est près de la fenêtre.",
            "narrateur|Il tient un pli du rideau.",
            "enfant-f|Tu viens ?",
            "copain|Je regarde.",
            "narrateur|Nina accepte.",
            "maman|On peut proposer.",
            "maman|On peut accepter plusieurs réponses.",
            "papa|Oui.",
            "papa|Non.",
            "papa|Regarder.",
            "papa|Plus tard.",
            "narrateur|Nina enfile une perle brune.",
            "narrateur|Ça fait un petit glissement.",
            "narrateur|Le fil tremble un peu.",
            "enfant-f|Plus tard ?",
            "copain|Plus tard.",
            "enfant-f|D'accord.",
            "papa|Tu as accepté, Nina ?",
            "enfant-f|Oui, papa.",
            "maman|Regarder, c'est une réponse.",
            "narrateur|La perle rouge roule.",
            "narrateur|Elle se cache dans la dentelle.",
            "papa|Tu as vu le trou de lumière ?",
            "enfant-f|La perle est dedans.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Nina invite Victorino.",
            "narrateur|Que fait-elle ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Nina a su proposer.",
            "narrateur|Elle a su accepter plusieurs réponses.",
            "papa|Victorino a dit regarder, puis plus tard.",
            "maman|Oui.",
            "maman|Tout ça va.",
            "enfant-f|J'ai dit d'accord.",
            "narrateur|Nina cherche dans la dentelle.",
            "narrateur|Le fil du rideau chatouille un peu.",
            "narrateur|Ses doigts trouvent la perle rouge.",
            "enfant-f|Te voilà.",
            "papa|Bravo.",
            "papa|Tu as retrouvé la perle.",
            "enfant-f|Tu veux la rouge ?",
            "copain|Non.",
            "enfant-f|D'accord.",
            "maman|Plusieurs réponses sont possibles.",
            "narrateur|Nina enfile la rouge.",
            "narrateur|Le collier s'allonge.",
            "narrateur|Les perles tapent l'une contre l'autre.",
            "narrateur|Victorino s'assoit sur ses talons.",
            "narrateur|Il regarde encore.",
            "maman|Tu as proposé tout doux ?",
            "enfant-f|Oui, maman.",
        ],
        "CHK_T0000_P0000_END": [
            "maman|On noue le fil ?",
            "enfant-f|Oui.",
            "narrateur|Papa tient le nœud.",
            "narrateur|Nina tire, tout doux.",
            "narrateur|Le collier est fermé.",
            "papa|Tu as fini le collier, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Maman baisse un peu la tête.",
            "narrateur|Nina passe le collier.",
            "narrateur|Les perles tapent, tout doux.",
            "narrateur|La perle rouge se met au milieu.",
            "maman|Il est beau.",
            "maman|Merci, Nina.",
            "enfant-f|Victorino a regardé.",
            "papa|Oui.",
            "papa|C'est une réponse.",
            "narrateur|La lumière perce encore la dentelle.",
            "narrateur|La perle rouge brille au milieu.",
            "narrateur|Maman touche le bois, tout doux.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le collier repose sur maman.",
            "enfant-f|J'ai proposé.",
            "enfant-f|J'ai accepté.",
            "maman|Plusieurs réponses sont possibles.",
            "papa|Oui.",
            "narrateur|La boîte à couture sent encore la cire.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "boite,perles",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "perles",
        "CHK_T0000_P0000_END": "perles",
        "CHK_T0000_P0000_END_F0001": "",
    },
    extras={
        "CHK_T0000_P0000_Q0001": dict(
            Q002_ACC,
            retry_prompt="Elle propose. Victorino peut regarder. Que fait Nina ?",
        )
    },
    relecture=(
        "Boîte à couture, cire, dentelle. Nina veut un collier pour maman. "
        "Victorino regarde, dit plus tard, dit non pour la perle rouge. "
        "La perle se cache. Nina accepte. Maman met le collier."
    ),
)


# ---------------------------------------------------------------------------
# 002-05 N2 Chouchou, Mila — garage en carton
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.BES.002-05",
    "Chouchou veut que la voiture rouge rentre dans un garage en carton. Il propose. Mila dit non, puis je regarde, puis plus tard. Le rabat est dur, il le plie deux fois. Chouchou accepte. La voiture fait toc. Le rabat se ferme.",
    "Le garage en carton",
    "Chouchou, Mila, papa, maman",
    "couloir, carton, vent dans la cheminée",
    {
        "CHK_T0000_P0000": [
            "narrateur|Le vent chante dans la cheminée.",
            "narrateur|Ça fait un son long, tout bas.",
            "narrateur|Un carton ouvert attend dans le couloir.",
            "narrateur|Il sent encore le crayon.",
            "narrateur|Un trait bleu reste sur un bord.",
            "narrateur|Une voiture rouge de bois est par terre.",
            "narrateur|Ses roues sont noires et lisses.",
            "narrateur|Un phare est peint en jaune.",
            "maman|Tu entends le vent, Chouchou ?",
            "enfant-m|Oui, maman.",
            "papa|J'ai plié un rabat, tout à l'heure.",
            "papa|Ça peut être une porte.",
            "maman|On reste au couloir, d'accord ?",
            "enfant-m|D'accord.",
            "enfant-m|La voiture rentre dedans.",
            "narrateur|En ce moment, Chouchou tire le carton.",
            "narrateur|Le carton racle un peu le sol.",
            "narrateur|Une poussière s'envole, toute légère.",
            "narrateur|Maman ouvre la porte.",
            "narrateur|Mila arrive.",
            "narrateur|Elle a des chaussettes à rayures.",
            "enfant-m|Tu viens ?",
            "copine|Non.",
            "narrateur|Chouchou regarde papa.",
            "papa|On peut proposer.",
            "maman|On peut accepter plusieurs réponses.",
            "papa|Oui.",
            "papa|Non.",
            "papa|Regarder.",
            "papa|Plus tard.",
            "enfant-m|D'accord.",
            "narrateur|Chouchou pousse le rabat.",
            "narrateur|Le rabat est dur.",
            "papa|Le rabat est dur, hein ?",
            "enfant-m|Oui.",
            "narrateur|Il le plie une fois.",
            "narrateur|Le carton craque, tout doux.",
            "narrateur|Puis une autre fois.",
            "narrateur|Le rabat s'ouvre mieux.",
            "enfant-m|Plus tard, tu viens ?",
            "copine|Je regarde.",
            "maman|Regarder, c'est une réponse.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Chouchou invite Mila.",
            "narrateur|Que fait-on ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Chouchou a su proposer.",
            "narrateur|Il accepte plusieurs réponses.",
            "enfant-m|D'accord.",
            "narrateur|Mila s'assoit près du mur.",
            "narrateur|Elle regarde la voiture.",
            "narrateur|Chouchou pousse la voiture.",
            "narrateur|Les roues font un petit bruit.",
            "narrateur|Le phare jaune avance.",
            "papa|Tu as entendu les roues ?",
            "enfant-m|Oui, papa.",
            "enfant-m|Tu veux pousser ?",
            "copine|Plus tard.",
            "enfant-m|D'accord.",
            "maman|Plusieurs réponses sont possibles.",
            "narrateur|La voiture s'arrête devant le rabat.",
            "narrateur|Le phare jaune touche le carton.",
            "narrateur|Elle n'est pas encore dedans.",
            "papa|Tu as plié le rabat.",
            "enfant-m|Deux fois.",
            "narrateur|Mila avance un peu.",
            "narrateur|Elle reste à regarder.",
            "maman|C'est bien.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Chouchou pousse encore.",
            "narrateur|La voiture rentre.",
            "narrateur|Les roues passent le rabat.",
            "narrateur|Ça fait toc.",
            "enfant-m|Elle est dedans.",
            "papa|Tu as accepté, Chouchou ?",
            "enfant-m|Oui, papa.",
            "maman|Bravo.",
            "narrateur|Il ferme le rabat.",
            "narrateur|Le carton redevient calme.",
            "narrateur|On n'entend plus les roues.",
            "copine|J'ai regardé.",
            "papa|Oui.",
            "papa|Regarder, c'est une réponse.",
            "maman|On range la voiture ?",
            "enfant-m|Elle dort déjà.",
            "papa|Tu as fini le garage ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le vent chante encore, tout loin.",
            "narrateur|Les rayures de Mila brillent.",
            "narrateur|Le trait bleu du carton reste.",
            "narrateur|La poussière est retombée.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|La voiture rouge dort dans le carton.",
            "narrateur|Le phare jaune ne se voit plus.",
            "enfant-m|J'ai proposé.",
            "enfant-m|J'ai accepté.",
            "maman|Plusieurs réponses sont possibles.",
            "papa|Oui.",
            "narrateur|Le vent finit sa chanson.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "vent,carton",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "roues",
        "CHK_T0000_P0000_END": "carton",
        "CHK_T0000_P0000_END_F0001": "",
    },
    extras={"CHK_T0000_P0000_Q0001": Q002_PROP},
    relecture=(
        "Vent dans la cheminée, carton du couloir, voiture rouge. Chouchou veut le garage. "
        "Mila dit non, je regarde, plus tard. Le rabat est dur, il le plie deux fois. "
        "Il accepte. Toc. Le rabat se ferme."
    ),
)


print("done")
