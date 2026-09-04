#!/usr/bin/env python3
"""TREE-AUT-026 / TREE-AUT-027 — récit implicite, graphe 86, D16."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import (  # noqa: E402
    BAD_NAMES,
    FORBIDDEN,
    OPENING_BAD,
    ROLES,
    ROOT,
    _listy_run,
    from_script,
    relecture,
    words,
)

LIMITS = {"N1": 10, "N2": 15}


def check_story(sid: str, age: str, chunks: list[dict]) -> None:
    lim = LIMITS[age]
    joined = "\n".join(c["script"] for c in chunks)
    low = joined.lower()
    for bad in FORBIDDEN:
        if bad in low:
            raise SystemExit(f"{sid} interdit: {bad}")
    for name in BAD_NAMES:
        if name in low:
            raise SystemExit(f"{sid} prénom hors troupe: {name}")
    for extra in ("lila", "sami"):
        if re.search(rf"\b{re.escape(extra)}\b", low):
            raise SystemExit(f"{sid} prénom hors troupe: {extra}")
    adults = [ln for ln in joined.splitlines() if ln.startswith("papa|") or ln.startswith("maman|")]
    if not adults:
        raise SystemExit(f"{sid}: aucun papa/maman")
    aj = " ".join(a.split("|", 1)[1] for a in adults).lower()
    if "bravo" not in aj and "merci" not in aj:
        raise SystemExit(f"{sid}: pas de félicitation vécue")
    if not any("?" in a for a in adults):
        raise SystemExit(f"{sid}: aucune question d'adulte")
    if "en ce moment" not in low:
        raise SystemExit(f"{sid}: manque en ce moment")
    first = chunks[0]["script"].splitlines()[0].split("|", 1)[1].lower()
    for bad in OPENING_BAD:
        if bad in first:
            raise SystemExit(f"{sid} ouverture brutale: {first}")
    nwords = sum(words(c["text"]) for c in chunks)
    if nwords < 380:
        raise SystemExit(f"{sid}: trop court ({nwords} mots)")
    listed = _listy_run(joined)
    if listed:
        raise SystemExit(f"{sid}: puces (4 narrations d'affilée commencent par « {listed} »)")
    longp: list[str] = []
    for c in chunks:
        rebuilt, _ = from_script(c["script"].splitlines())
        if rebuilt != c["text"]:
            raise SystemExit(f"{sid} {c['chunk_id']}: text ≠ script")
        if c.get("text_ssml") != c["text"]:
            raise SystemExit(f"{sid} {c['chunk_id']}: ssml ≠ text")
        for ln in c["script"].splitlines():
            if "|" not in ln:
                raise SystemExit(f"{sid} ligne sans | : {ln}")
            role, phrase = ln.split("|", 1)
            if role not in ROLES:
                raise SystemExit(f"{sid} rôle {role}")
            n = words(phrase)
            if n > lim:
                longp.append(f"{c['chunk_id']} {n}>{lim}: {phrase}")
            if n == 0:
                raise SystemExit(f"{sid} phrase vide")
            if not phrase.endswith((".", "?", "!")):
                raise SystemExit(f"{sid} sans ponctuation: {phrase}")
            if phrase.count(".") + phrase.count("?") + phrase.count("!") > 1:
                raise SystemExit(f"{sid} plusieurs phrases: {phrase}")
    if longp:
        raise SystemExit(f"{sid} phrases trop longues:\n" + "\n".join(longp[:40]))
    for c in chunks:
        if c.get("kind") != "passage_fin":
            continue
        last_lines = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        if not last_lines:
            raise SystemExit(f"{sid} {c['chunk_id']}: fin sans narrateur")
        last = last_lines[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{sid} fin mécanique: {last}")
    print(f"OK {sid} {nwords} mots  1re: {chunks[0]['script'].splitlines()[0].split('|',1)[1]}")


def write_story(
    sid: str,
    fil: str,
    title: str,
    chars: str,
    setting: str,
    scripts: dict[str, list[str]],
    sons: dict[str, str],
    qfields: dict[str, dict],
) -> None:
    folder = ROOT / sid
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"{sid} missing={missing[:8]} extra={sorted(extra)[:8]}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        text, script = from_script(scripts[cid])
        nc = deepcopy(c)
        nc["text"] = text
        nc["script"] = script
        nc["text_ssml"] = text
        nc["sons"] = sons.get(cid, c.get("sons") or "") or ""
        kind = c.get("kind") or ""
        if kind in ("passage_question", "transition_question"):
            nc["length_scale_piper"] = 1.28
            nc["rate_label"] = "slow"
        elif src.get("age_band") == "N1":
            nc["length_scale_piper"] = 1.22
            nc["rate_label"] = "slow"
        else:
            nc["length_scale_piper"] = 1.22
            nc["rate_label"] = "medium"
        if cid in qfields:
            nc.update(qfields[cid])
        by[cid] = nc
    out = dict(src)
    out["fil_rouge"] = fil
    out["title"] = title
    out["characters"] = chars
    out["setting"] = setting
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check_story(sid, out["age_band"], out["chunks"])
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


# ---------------------------------------------------------------------------
# TREE-AUT-026  N1  Sarah  AUT.AFF.001  cartable jaune (pas un chant)
# T1 lieux cour / T2 jeu / T3 trésor glissé dans le cartable
# ---------------------------------------------------------------------------

L1_026 = {
    1: {"lab": "le bac à sable", "ici": "au bac à sable", "son": "sable"},
    2: {"lab": "le toboggan", "ici": "au toboggan", "son": "toboggan"},
    3: {"lab": "les balançoires", "ici": "aux balançoires", "son": "balancoire"},
}
L2_026 = {
    1: {"lab": "le ballon", "obj": "le ballon", "un": "le ballon"},
    2: {"lab": "le seau", "obj": "le seau", "un": "le seau"},
    3: {"lab": "le doudou", "obj": "le doudou", "un": "le doudou"},
}
L3_026 = {
    1: {"lab": "la craie", "obj": "la craie", "un": "la craie jaune"},
    2: {"lab": "le caillou", "obj": "le caillou", "un": "le caillou lisse"},
    3: {"lab": "la feuille", "obj": "la feuille", "un": "la feuille verte"},
}

L1_BODY_026 = {
    1: [
        "narrateur|Sarah arrive au bac à sable.",
        "narrateur|Le sable est frais, un peu sombre.",
        "narrateur|Ça fait chh sous les doigts.",
        "narrateur|Le cartable jaune est sur le bois.",
        "papa|Le goûter est encore dedans ?",
        "enfant-f|Oui, papa.",
        "enfant-f|Il fait une petite bosse.",
        "maman|Le bois du bac est tiède.",
        "narrateur|Sarah verse le sable.",
        "narrateur|Un grain reste sous son ongle.",
        "papa|Tes joues sont déjà roses.",
        "enfant-f|Je fais un château.",
        "maman|Tout doux, près du cartable.",
        "narrateur|Le château penche vers le sac.",
        "narrateur|Sarah l'appuie avec la paume.",
    ],
    2: [
        "narrateur|Sarah va vers le toboggan.",
        "narrateur|Le métal est tiède sous la paume.",
        "narrateur|Les marches font toc, toc.",
        "narrateur|Papa pose le cartable en bas.",
        "papa|Je le garde, ici.",
        "enfant-f|Je glisse !",
        "maman|J'attends tout en bas.",
        "narrateur|Sarah glisse.",
        "narrateur|Le plastique fait un petit frou.",
        "enfant-f|Encore une fois.",
        "papa|Une fois, oui.",
        "narrateur|Ses pieds retrouvent l'herbe.",
        "maman|Le cartable est resté près de papa.",
        "enfant-f|Le goûter aussi.",
        "narrateur|Une feuille colle à la rampe.",
    ],
    3: [
        "narrateur|Sarah va vers les balançoires.",
        "narrateur|La chaîne est un peu froide.",
        "narrateur|Le siège est lisse, un peu chaud.",
        "maman|Je pousse tout doux.",
        "enfant-f|Encore un peu ?",
        "maman|Encore.",
        "narrateur|Le cartable jaune est sous le banc.",
        "papa|Le goûter reste à l'ombre.",
        "narrateur|Sarah avance, puis revient.",
        "narrateur|Le vent lui touche le nez.",
        "enfant-f|Je vois le ciel.",
        "papa|Dans la flaque, oui.",
        "maman|Tes mains tiennent la chaîne.",
        "narrateur|Sarah pose un pied au sol.",
        "narrateur|La chaîne fait cling, puis se tait.",
    ],
}

Q_026 = {
    1: [
        "narrateur|Le château penche vers le cartable.",
        "papa|Sarah a mis le goûter où ?",
    ],
    2: [
        "narrateur|Le cartable est resté en bas.",
        "maman|Le goûter de Sarah est où ?",
    ],
    3: [
        "narrateur|Le cartable attend sous le banc.",
        "papa|Sarah a mis le goûter où ?",
    ],
}

C_026 = {
    1: [
        "narrateur|Sarah touche le tissu jaune.",
        "narrateur|Le goûter fait encore une bosse.",
        "enfant-f|Il est dedans.",
        "papa|Oui.",
        "papa|Dans le cartable.",
        "maman|Tu pourras le manger plus tard.",
        "enfant-f|Après le château.",
        "papa|Bravo, Sarah.",
        "narrateur|Un grain reste sur sa joue.",
    ],
    2: [
        "narrateur|Sarah court vers papa.",
        "narrateur|Elle pose la main sur le sac.",
        "enfant-f|Il est là.",
        "maman|Oui.",
        "maman|Le goûter est dans le cartable.",
        "papa|Il a voyagé en bas.",
        "enfant-f|Sans glisser.",
        "maman|Merci, Sarah.",
        "narrateur|La feuille reste sur la rampe.",
    ],
    3: [
        "narrateur|Sarah se penche sous le banc.",
        "narrateur|Le tissu jaune est un peu frais.",
        "enfant-f|Le goûter est là.",
        "papa|Oui.",
        "papa|Dans le cartable.",
        "maman|À l'ombre, tout calme.",
        "enfant-f|Il attend.",
        "papa|Bravo.",
        "narrateur|La chaîne ne fait plus cling.",
    ],
}

L2_BODY_026 = {
    1: [
        "narrateur|Sarah a choisi le ballon.",
        "narrateur|Il est rouge et lisse.",
        "narrateur|Il fait un petit bond.",
        "papa|Tout près de nous, d'accord ?",
        "enfant-f|Il est rouge, papa.",
        "maman|Le cartable reste juste là.",
        "narrateur|Sarah pose le ballon un moment.",
        "enfant-f|Il se repose.",
        "papa|Oui, tout doux.",
        "narrateur|Un brin d'herbe colle au cuir.",
    ],
    2: [
        "narrateur|Sarah a choisi le seau.",
        "narrateur|Le seau jaune a du sable.",
        "narrateur|L'anse est un peu froide.",
        "maman|C'est ton seau, Sarah.",
        "enfant-f|Il est jaune.",
        "enfant-f|Comme le cartable.",
        "papa|Tu verses, tout doux ?",
        "narrateur|Elle verse un peu.",
        "narrateur|Ça fait chh, encore.",
        "maman|Le cartable n'a pas de sable.",
        "narrateur|Sarah pose le seau à côté.",
    ],
    3: [
        "narrateur|Sarah a choisi le doudou.",
        "narrateur|Le doudou gris a une oreille molle.",
        "narrateur|Un peu de vent est dessus.",
        "maman|Il t'attendait, Sarah.",
        "enfant-f|Il est doux.",
        "papa|Il peut s'asseoir sur le sac.",
        "narrateur|Elle le pose sur le cartable.",
        "enfant-f|Il garde le goûter.",
        "maman|Oui.",
        "narrateur|L'oreille du doudou est chaude.",
    ],
}

L2_EXTRA_026 = {
    (1, 1): "Un grain de sable colle au ballon.",
    (1, 2): "Du sable fin brille dans le seau.",
    (1, 3): "L'oreille grise a un peu de sable.",
    (2, 1): "Le ballon est un peu froid, près de la rampe.",
    (2, 2): "Le seau sonne tout doux contre une marche.",
    (2, 3): "Le doudou a vu le toboggan, tout gris.",
    (3, 1): "Un brin d'herbe colle au ballon.",
    (3, 2): "L'anse du seau est froide, près de la chaîne.",
    (3, 3): "Le doudou a senti le vent, tout doux.",
}

L3_FIND_026 = {
    1: [
        "narrateur|Une craie jaune attend dans l'herbe.",
        "narrateur|Elle est un peu cassée.",
        "enfant-f|Une craie !",
        "papa|Elle écrit sur le sol ?",
        "narrateur|Sarah trace un petit trait.",
        "narrateur|Le trait est pâle, tout court.",
        "maman|Tu la gardes ?",
        "enfant-f|Dans le cartable.",
        "narrateur|Elle glisse la craie près du goûter.",
        "papa|Elle ne se perd plus.",
    ],
    2: [
        "narrateur|Un caillou lisse brille un peu.",
        "narrateur|Il est chaud, tout rond.",
        "enfant-f|Il est à moi.",
        "maman|Tu le prends tout doux ?",
        "narrateur|Sarah le serre dans la paume.",
        "narrateur|Il chauffe sa main.",
        "papa|Tu le mets où ?",
        "enfant-f|Dans le cartable.",
        "narrateur|Le caillou tapote le goûter.",
        "maman|Il voyage avec le biscuit.",
    ],
    3: [
        "narrateur|Une feuille verte est tombée.",
        "narrateur|Elle a des nervures, tout net.",
        "enfant-f|Elle est douce.",
        "papa|Comme un petit drapeau.",
        "narrateur|Sarah la souffle une fois.",
        "narrateur|La feuille tremble, puis se pose.",
        "maman|Tu la mets dans le sac ?",
        "enfant-f|Oui.",
        "narrateur|Elle glisse la feuille à plat.",
        "papa|Elle reste belle, là.",
    ],
}

IMG_026 = {
    (1, 1, 1): "Un grain de sable colle à la craie.",
    (1, 1, 2): "Le caillou a un peu de sable.",
    (1, 1, 3): "La feuille a du sable au bord.",
    (1, 2, 1): "La craie sonne contre le seau.",
    (1, 2, 2): "Le caillou roule au fond du seau.",
    (1, 2, 3): "La feuille flotte un peu dans le seau.",
    (1, 3, 1): "La craie est près de l'oreille du doudou.",
    (1, 3, 2): "Le caillou chauffe le doudou, tout doux.",
    (1, 3, 3): "La feuille couvre le doudou, tout léger.",
    (2, 1, 1): "La craie a glissé près du toboggan.",
    (2, 1, 2): "Le caillou est tiède, près de la rampe.",
    (2, 1, 3): "La feuille colle à la rampe.",
    (2, 2, 1): "La craie est dans le seau, en bas.",
    (2, 2, 2): "Le caillou tape le seau, tout doux.",
    (2, 2, 3): "La feuille cache le seau, un peu.",
    (2, 3, 1): "La craie est contre le doudou, en bas.",
    (2, 3, 2): "Le caillou est sur les genoux du doudou.",
    (2, 3, 3): "La feuille couvre le doudou, en bas.",
    (3, 1, 1): "La craie dessine près de la chaîne.",
    (3, 1, 2): "Le caillou brille sous la balançoire.",
    (3, 1, 3): "La feuille vole près de la chaîne.",
    (3, 2, 1): "La craie est dans le seau, sous le banc.",
    (3, 2, 2): "Le caillou attend dans le seau.",
    (3, 2, 3): "La feuille est posée dans le seau.",
    (3, 3, 1): "La craie est dans les bras du doudou.",
    (3, 3, 2): "Le caillou chauffe le doudou, sous le banc.",
    (3, 3, 3): "La feuille est sur le doudou, sous le banc.",
}

FIN_026 = {
    (1, 1, 1): "Le rectangle de soleil a bougé.",
    (1, 1, 2): "Un grain reste sur le bois du bac.",
    (1, 1, 3): "Le château penche encore, tout petit.",
    (1, 2, 1): "L'anse du seau sèche au soleil.",
    (1, 2, 2): "Le sable du seau est tiède.",
    (1, 2, 3): "Une miette de sable brille encore.",
    (1, 3, 1): "L'oreille du doudou a un grain.",
    (1, 3, 2): "Le doudou sent encore le bac.",
    (1, 3, 3): "Le bois du bac est calme.",
    (2, 1, 1): "La rampe du toboggan est tiède.",
    (2, 1, 2): "Une feuille reste collée à la rampe.",
    (2, 1, 3): "Les marches ne font plus toc.",
    (2, 2, 1): "Le seau sonne une dernière fois.",
    (2, 2, 2): "L'herbe au pied du toboggan est chaude.",
    (2, 2, 3): "Une ombre glisse sur la rampe.",
    (2, 3, 1): "Le doudou a vu la rampe, tout gris.",
    (2, 3, 2): "Le plastique du toboggan se tait.",
    (2, 3, 3): "Un brin d'herbe reste au doudou.",
    (3, 1, 1): "La chaîne ne fait plus cling.",
    (3, 1, 2): "La flaque sous la balançoire est calme.",
    (3, 1, 3): "Le vent a quitté la chaîne.",
    (3, 2, 1): "Le seau reste à l'ombre, sous le banc.",
    (3, 2, 2): "Le banc sent encore le bois chaud.",
    (3, 2, 3): "Une ombre de chaîne danse, tout loin.",
    (3, 3, 1): "Le doudou a les joues du vent.",
    (3, 3, 2): "Le siège de la balançoire est vide.",
    (3, 3, 3): "Sous le banc, l'ombre est fraîche.",
}


def build_026() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    qf: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = [
        "narrateur|L'escalier de bois sent encore le froid.",
        "narrateur|Un cartable jaune attend sur la marche.",
        "narrateur|La boucle du cartable brille.",
        "narrateur|Une peau d'orange sent fort.",
        "narrateur|Elle est encore dans la cuisine.",
        "narrateur|Loin, la cloche de l'école tinte.",
        "narrateur|Les crochets du portemanteau sont vides.",
        "narrateur|Une craie blanche a glissé.",
        "narrateur|Elle est sous le banc.",
        "maman|Sarah, tu as vu le soleil ?",
        "enfant-f|Oui, maman.",
        "enfant-f|Il est sur la marche.",
        "papa|La cloche est déjà loin.",
        "narrateur|Sarah pose la main sur le tissu.",
        "narrateur|Le tissu est un peu rêche.",
        "narrateur|En ce moment, elle ouvre la boucle.",
        "narrateur|Ça fait tchac.",
        "enfant-f|Il est vide !",
        "narrateur|Le cartable est trop léger.",
        "papa|Le goûter est encore sur la table.",
        "enfant-f|Je veux l'école !",
        "maman|Le goûter voudra l'école aussi.",
        "narrateur|Sarah court vers la table.",
        "narrateur|Le papier du goûter craque.",
        "narrateur|Elle le glisse dans le cartable.",
        "enfant-f|Il est dedans.",
        "papa|Tu as entendu la boucle ?",
        "enfant-f|Oui, papa.",
        "maman|Bravo.",
        "papa|On peut y aller ?",
        "enfant-f|Oui !",
        "narrateur|Le cartable tape un peu sa hanche.",
    ]
    sons["CHK_T0000_P0000"] = "escalier,sac,cloche"

    s["CHK_T0001_P0000"] = [
        "papa|On joue où, à l'école ?",
        "narrateur|Le bac à sable.",
        "narrateur|Le toboggan.",
        "narrateur|Ou les balançoires.",
    ]
    sons["CHK_T0001_P0000"] = ""

    for i, loc in L1_026.items():
        s[f"CHK_T0001_P000{i}"] = L1_BODY_026[i]
        sons[f"CHK_T0001_P000{i}"] = loc["son"]
        s[f"CHK_T0001_P000{i}_Q0001"] = Q_026[i]
        sons[f"CHK_T0001_P000{i}_Q0001"] = ""
        qf[f"CHK_T0001_P000{i}_Q0001"] = {
            "expected_answer": "sac",
            "accepted_examples": (
                "sac | cartable | le sac | le cartable | dans le sac | "
                "dans le cartable | le goûter"
            ),
            "retry_prompt": "Dans le cartable jaune. Il est où ?",
        }
        s[f"CHK_T0001_P000{i}_C0001"] = C_026[i]
        sons[f"CHK_T0001_P000{i}_C0001"] = ""
        s[f"CHK_T0001_P000{i}_T0002_P0000"] = [
            "maman|Tu prends quel jeu ?",
            "narrateur|Le ballon.",
            "narrateur|Le seau.",
            "narrateur|Ou le doudou.",
        ]
        sons[f"CHK_T0001_P000{i}_T0002_P0000"] = ""

        for j, jeu in L2_026.items():
            cid2 = f"CHK_T0001_P000{i}_T0002_P000{j}"
            extra = L2_EXTRA_026[(i, j)]
            s[cid2] = L2_BODY_026[j] + [
                f"narrateur|{extra}",
                f"narrateur|On est encore {loc['ici']}.",
            ]
            sons[cid2] = ""
            t3 = f"{cid2}_T0003_P0000"
            s[t3] = [
                "papa|Tu as trouvé quoi, dans l'herbe ?",
                "narrateur|La craie.",
                "narrateur|Le caillou.",
                "narrateur|Ou la feuille.",
            ]
            sons[t3] = ""
            qf[t3] = {
                "option_1_label": "la craie",
                "option_2_label": "le caillou",
                "option_3_label": "la feuille",
            }

            for k, tre in L3_026.items():
                cid3 = f"{cid2}_T0003_P000{k}"
                img = IMG_026[(i, j, k)]
                fin = FIN_026[(i, j, k)]
                s[cid3] = L3_FIND_026[k] + [
                    f"narrateur|{jeu['un'][0].upper() + jeu['un'][1:]} reste près d'elle.",
                    f"narrateur|On est encore {loc['ici']}.",
                    f"narrateur|{img}",
                    "maman|Le cartable a le goûter, et ça.",
                    "enfant-f|Il est moins vide.",
                    "papa|Oui.",
                ]
                sons[cid3] = ""
                s[f"{cid3}_F0001"] = [
                    f"narrateur|Sarah est passée par {loc['lab']}.",
                    f"narrateur|Elle a joué avec {jeu['lab']}.",
                    f"narrateur|Elle a gardé {tre['lab']}.",
                    "narrateur|Le goûter est encore dans le cartable.",
                    f"narrateur|{img}",
                    "maman|Tu fermes la boucle ?",
                    "narrateur|Sarah ferme la boucle.",
                    "narrateur|Ça fait tchac.",
                    "papa|Merci, Sarah.",
                    "enfant-f|Le cartable est à moi.",
                    f"narrateur|{fin}",
                ]
                sons[f"{cid3}_F0001"] = ""
    return s, sons, qf


# ---------------------------------------------------------------------------
# TREE-AUT-027  N2  Mila  AUT.AFF.002  manteau bleu, marché, froid, retour
# ---------------------------------------------------------------------------

L1_027 = {
    1: {"lab": "la cuisine", "ici": "dans la cuisine", "son": "orange"},
    2: {"lab": "le jardin", "ici": "dans le jardin", "son": "vent"},
    3: {"lab": "la chambre", "ici": "dans la chambre", "son": "rideau"},
}
L2_027 = {
    1: {"lab": "les cubes", "obj": "les cubes", "un": "un cube"},
    2: {"lab": "le livre", "obj": "le livre", "un": "le livre"},
    3: {"lab": "la dînette", "obj": "la dînette", "un": "une tasse"},
}
L3_027 = {
    1: {"lab": "le matin", "quand": "le matin"},
    2: {"lab": "après la sieste", "quand": "après la sieste"},
    3: {"lab": "le soir", "quand": "le soir"},
}

L1_BODY_027 = {
    1: [
        "narrateur|Mila pousse la porte de la cuisine.",
        "narrateur|Les carreaux sont un peu froids sous les pieds.",
        "narrateur|Ça sent la menthe, tout près de l'évier.",
        "narrateur|Une orange roule, tout doux, vers le panier.",
        "maman|L'orange dans le panier, Mila.",
        "enfant-f|L'orange.",
        "narrateur|Elle la pose.",
        "narrateur|Ça sent le fruit.",
        "papa|La cuisine est tiède, hein ?",
        "enfant-f|Oui.",
        "enfant-f|Mon manteau est chaud, trop chaud.",
        "maman|Tu peux l'ouvrir un peu.",
        "narrateur|Mila ouvre deux boutons ronds.",
        "narrateur|Le col bleu reste sur ses épaules.",
        "papa|On sort après, vers le marché.",
        "enfant-f|Avec le panier.",
        "narrateur|Le panier d'osier pose un cercle d'ombre.",
    ],
    2: [
        "narrateur|Mila va vers le jardin.",
        "narrateur|L'herbe est mouillée, toute brillante.",
        "narrateur|L'air est frais sur le nez.",
        "narrateur|Le manteau bleu sent encore le bois du crochet.",
        "papa|Tu as tes bottes ?",
        "enfant-f|Oui.",
        "enfant-f|Elles font ploc.",
        "maman|La menthe pousse près du muret.",
        "narrateur|Une feuille de menthe tremble.",
        "narrateur|Mila la cueille, tout doux.",
        "papa|Tu la mets dans la poche ?",
        "enfant-f|Oui.",
        "narrateur|La poche du manteau est un peu froide.",
        "narrateur|La menthe sent fort, tout vert.",
        "maman|Sans le manteau, tu aurais froid.",
        "enfant-f|Je l'ai repris.",
        "narrateur|Mila avance dans l'herbe, le panier à la main.",
    ],
    3: [
        "narrateur|Mila va vers la chambre.",
        "narrateur|La couverture est douce, toute pliée.",
        "narrateur|Le rideau jaune bouge un peu.",
        "narrateur|Le manteau bleu frotte la porte.",
        "maman|Ton petit panier jouet est sur le lit.",
        "enfant-f|Je le prends.",
        "enfant-f|Pour le marché.",
        "papa|Il tient dans la poche ?",
        "narrateur|Mila glisse le panier jouet.",
        "narrateur|Puis elle pose le vrai manteau sur le lit.",
        "enfant-f|J'ai trop chaud ici.",
        "maman|La fenêtre est un peu ouverte.",
        "narrateur|L'air froid entre, tout net.",
        "enfant-f|J'ai froid, encore.",
        "papa|Le manteau bleu est sur le lit.",
        "narrateur|Mila revient vers le lit.",
        "narrateur|Elle reprend le manteau.",
        "enfant-f|Il est à moi.",
        "narrateur|Elle glisse un bras, puis l'autre.",
    ],
}

Q_027 = {
    1: [
        "narrateur|Mila a ouvert deux boutons, dans la cuisine.",
        "papa|Elle a repris quoi, pour n'avoir plus froid ?",
    ],
    2: [
        "narrateur|Dans le jardin, Mila n'a pas froid.",
        "maman|Elle a repris quoi, à la porte ?",
    ],
    3: [
        "narrateur|Le manteau était sur le lit.",
        "narrateur|Mila l'a repris.",
        "papa|Elle a repris quoi, pour n'avoir plus froid ?",
    ],
}

C_027 = {
    1: [
        "narrateur|Oui.",
        "narrateur|Elle a repris le manteau bleu.",
        "papa|Merci, Mila.",
        "maman|Les boutons sont encore un peu ouverts.",
        "enfant-f|Pour la cuisine.",
        "papa|On emporte un jeu, dans le panier ?",
        "narrateur|L'orange brille encore, tout près.",
    ],
    2: [
        "narrateur|Oui.",
        "narrateur|Le manteau bleu est sur elle.",
        "maman|Bravo.",
        "maman|Tu n'as plus froid.",
        "enfant-f|La menthe est dans la poche.",
        "papa|On emporte un jeu, pour le marché ?",
        "narrateur|Une goutte brille encore sur l'herbe.",
    ],
    3: [
        "narrateur|Oui.",
        "narrateur|Mila a repris le manteau sur le lit.",
        "papa|Le petit panier est dans la poche.",
        "enfant-f|Pour le marché.",
        "maman|On emporte un jeu aussi ?",
        "narrateur|Le rideau se tait.",
        "narrateur|La chambre redevient calme.",
    ],
}

L2_BODY_027 = {
    1: [
        "narrateur|Mila a choisi les cubes.",
        "narrateur|Ils sont en bois, un peu lourds.",
        "narrateur|Ils cliquent dans la boîte.",
        "papa|On fait un étal, pour le marché ?",
        "enfant-f|Oui.",
        "enfant-f|Un étal de cubes.",
        "maman|Le manteau garde tes bras au chaud.",
        "narrateur|Un cube sent le pin.",
        "narrateur|Mila le serre contre le tissu bleu.",
        "papa|On les emporte dans le panier.",
        "narrateur|La boîte tape doucement sa hanche.",
    ],
    2: [
        "narrateur|Mila a choisi le livre.",
        "narrateur|La couverture montre des oranges.",
        "narrateur|Une page sent encore le papier.",
        "maman|Comme la caisse, dehors.",
        "enfant-f|Oui.",
        "enfant-f|Les vraies oranges.",
        "papa|On le met sous le manteau ?",
        "narrateur|Le livre glisse contre le bleu.",
        "narrateur|Il reste au sec.",
        "maman|On le regardera près des étals.",
        "narrateur|Une page se recourbe, tout doux.",
    ],
    3: [
        "narrateur|Mila a choisi la dînette.",
        "narrateur|Une petite tasse sonne, tout creux.",
        "narrateur|Une cuillère miniature est tiède.",
        "papa|On sert le marché ?",
        "enfant-f|Oui.",
        "enfant-f|Un thé de menthe.",
        "maman|La tasse tient dans la poche.",
        "narrateur|Mila la glisse à côté du bouton.",
        "narrateur|Le manteau bleu la tient.",
        "papa|On y va, alors.",
        "narrateur|La petite assiette reste dans l'autre main.",
    ],
}

L2_EXTRA_027 = {
    (1, 1): "Un cube attrape un reflet d'orange.",
    (1, 2): "Une miette d'orange reste au bord de la page.",
    (1, 3): "La petite casserole est près du vrai bol.",
    (2, 1): "L'herbe tache un cube, tout vert.",
    (2, 2): "Une vraie feuille de menthe sert de marque-page.",
    (2, 3): "Une goutte perle au bord de l'assiette.",
    (3, 1): "Un cube tapote le parquet, tout doux.",
    (3, 2): "Le rideau jaune colore la page.",
    (3, 3): "La petite tasse est près du lit.",
}

MOMENT_027 = {
    1: [
        "narrateur|C'est le matin.",
        "narrateur|La lumière est pâle, tout douce.",
        "narrateur|Un oiseau chante une fois, très loin.",
    ],
    2: [
        "narrateur|C'est après la sieste.",
        "narrateur|Les joues de Mila sont chaudes.",
        "narrateur|La maison est encore calme.",
    ],
    3: [
        "narrateur|C'est le soir.",
        "narrateur|La lampe fait un rond jaune.",
        "narrateur|Les pavés du marché sont déjà bleus.",
    ],
}

L3_MARCHE_027 = {
    1: [
        "papa|Le marché s'ouvre, ce matin.",
        "narrateur|Ils sortent.",
        "narrateur|L'air touche le nez de Mila.",
        "enfant-f|Les oranges brillent.",
        "maman|Tes mains, dans les poches ?",
        "enfant-f|Elles sont au chaud.",
        "narrateur|La bâche rayée claque au-dessus d'eux.",
        "papa|Une orange, pour le panier.",
        "narrateur|Mila la choisit, tout ronde.",
    ],
    2: [
        "papa|Le marché est plus calme, après la sieste.",
        "narrateur|Ils sortent.",
        "narrateur|Le soleil est jaune et doux.",
        "enfant-f|Les pavés sont tièdes.",
        "maman|Le manteau est encore utile.",
        "enfant-f|Oui, un peu.",
        "narrateur|Un store fait une ombre douce.",
        "papa|Une orange, pour le panier.",
        "narrateur|Mila la choisit, un peu chaude.",
    ],
    3: [
        "papa|Le marché se range, ce soir.",
        "narrateur|Ils sortent.",
        "narrateur|La vitre de la maison est bleue.",
        "enfant-f|Je vois les lampes.",
        "maman|Le manteau te tient chaud.",
        "enfant-f|Oui, maman.",
        "narrateur|Une caisse d'oranges reste au stand.",
        "papa|Une orange, pour le panier.",
        "narrateur|Mila la choisit, encore parfumée.",
    ],
}

L3_RETOUR_027 = [
    "papa|C'est l'heure de rentrer.",
    "narrateur|Ils rentrent.",
    "narrateur|Le manteau bleu est un peu lourd.",
    "narrateur|Mila le retire.",
    "narrateur|Elle le raccroche au crochet de bois.",
    "maman|Les boutons sont froids, encore.",
    "enfant-f|Il sèche, là.",
    "papa|Oui.",
    "papa|Le crochet est à ta hauteur.",
]

IMG_027 = {
    (1, 1, 1): "Une miette d'orange sèche sur un cube.",
    (1, 1, 2): "Le cube sent encore la casserole.",
    (1, 1, 3): "L'ombre d'un cube danse sur le carrelage.",
    (1, 2, 1): "Une page sent la menthe, tout doux.",
    (1, 2, 2): "Le livre est tiède, près de la vitre.",
    (1, 2, 3): "La lampe dore le bord d'une page.",
    (1, 3, 1): "Une petite tasse a une goutte de menthe.",
    (1, 3, 2): "La dînette est chaude, comme la cuisine.",
    (1, 3, 3): "La petite cuillère brille sous la lampe.",
    (2, 1, 1): "Un cube a une goutte d'herbe.",
    (2, 1, 2): "Le cube sèche au soleil, tout vert.",
    (2, 1, 3): "Un cube garde une goutte, toute ronde.",
    (2, 2, 1): "Une vraie feuille de menthe marque la page.",
    (2, 2, 2): "Le livre sent l'herbe mouillée.",
    (2, 2, 3): "Un oiseau se tait près du livre.",
    (2, 3, 1): "Une petite assiette a de la rosée.",
    (2, 3, 2): "La dînette est tiède, au soleil.",
    (2, 3, 3): "Loin de la dînette, une goutte tombe.",
    (3, 1, 1): "Un rayon pose sur la tour de cubes.",
    (3, 1, 2): "Un cube est contre l'oreiller, tout calme.",
    (3, 1, 3): "L'ombre des cubes danse sur le mur.",
    (3, 2, 1): "Le rideau jaune colore la page.",
    (3, 2, 2): "Le livre est ouvert sur la couverture.",
    (3, 2, 3): "La page sent le savon, un peu.",
    (3, 3, 1): "Une tasse miniature est près du lit.",
    (3, 3, 2): "La dînette attend au pied du lit.",
    (3, 3, 3): "Une petite assiette reflète la veilleuse.",
}

FIN_027 = {
    (1, 1, 1): "L'orange reste dans le panier, près des cubes.",
    (1, 1, 2): "La casserole fait un tout petit pschitt.",
    (1, 1, 3): "Une miette d'orange reste sur la table.",
    (1, 2, 1): "Un oiseau chante encore, tout loin.",
    (1, 2, 2): "La page se recourbe, près du bol.",
    (1, 2, 3): "La lampe dore le livre fermé.",
    (1, 3, 1): "La petite tasse sèche près de l'évier.",
    (1, 3, 2): "La menthe sent encore, tout bas.",
    (1, 3, 3): "Le bouton du manteau brille, au crochet.",
    (2, 1, 1): "Les bottes sèchent près de la porte.",
    (2, 1, 2): "L'herbe colle encore à un cube.",
    (2, 1, 3): "Une goutte glisse du manteau bleu.",
    (2, 2, 1): "Une feuille de menthe reste dans le livre.",
    (2, 2, 2): "Le jardin est pâle, derrière la vitre.",
    (2, 2, 3): "La flaque ne brille plus, dehors.",
    (2, 3, 1): "La petite assiette a encore de l'herbe.",
    (2, 3, 2): "Les bottes font un dernier ploc.",
    (2, 3, 3): "Le col bleu sèche, au crochet.",
    (3, 1, 1): "Le petit panier repose sur un cube.",
    (3, 1, 2): "L'oreiller sent encore le savon.",
    (3, 1, 3): "Le rideau jaune ne bouge plus.",
    (3, 2, 1): "Le petit panier sèche sur la couverture.",
    (3, 2, 2): "Une page reste ouverte, sur le lit.",
    (3, 2, 3): "La veilleuse dore le livre.",
    (3, 3, 1): "La petite tasse est près du panier jouet.",
    (3, 3, 2): "Le tapis de la chambre est calme.",
    (3, 3, 3): "Le crochet de bois attend déjà demain.",
}


def build_027() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    qf: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = [
        "narrateur|Une bâche rayée claque au-dessus des oranges.",
        "narrateur|Elle est blanche et rouge, tout loin.",
        "narrateur|Une caisse sent encore le soleil.",
        "narrateur|Les pavés brillent encore un peu.",
        "narrateur|Une flaque tient le ciel.",
        "narrateur|Ça sent la menthe, et le pain chaud.",
        "narrateur|Près de la porte, un crochet de bois attend.",
        "narrateur|Un manteau bleu y pend, tout calme.",
        "narrateur|Les boutons sont ronds et froids.",
        "papa|Le panier d'osier est prêt, Mila.",
        "narrateur|Papa pose le panier.",
        "narrateur|Il est encore vide.",
        "maman|Tu as senti la menthe ?",
        "enfant-f|Oui, maman.",
        "enfant-f|Je veux le marché !",
        "narrateur|En ce moment, Mila court vers la porte.",
        "narrateur|Elle n'a pas pris le manteau.",
        "narrateur|Papa ouvre la porte.",
        "narrateur|L'air du marché entre, tout froid.",
        "enfant-f|J'ai froid, papa.",
        "narrateur|Ses épaules montent toutes seules.",
        "maman|Le manteau bleu est encore au crochet.",
        "enfant-f|J'y vais.",
        "narrateur|Mila revient vers le crochet.",
        "narrateur|Elle prend le manteau bleu.",
        "narrateur|Une manche est un peu froide.",
        "papa|Glisse un bras, puis l'autre.",
        "narrateur|Mila glisse un bras.",
        "narrateur|Elle glisse l'autre.",
        "enfant-f|Il est chaud.",
        "maman|Les boutons, Mila ?",
        "narrateur|Elle ferme deux boutons ronds.",
        "papa|Tu as les mains au chaud ?",
        "enfant-f|Dans les poches.",
        "narrateur|Le panier tape contre le manteau.",
    ]
    sons["CHK_T0000_P0000"] = "marche,porte"

    s["CHK_T0001_P0000"] = [
        "papa|On passe où, avant le marché ?",
        "narrateur|La cuisine.",
        "narrateur|Le jardin.",
        "narrateur|Ou la chambre.",
    ]
    sons["CHK_T0001_P0000"] = ""

    for i, loc in L1_027.items():
        s[f"CHK_T0001_P000{i}"] = L1_BODY_027[i]
        sons[f"CHK_T0001_P000{i}"] = loc["son"]
        s[f"CHK_T0001_P000{i}_Q0001"] = Q_027[i]
        sons[f"CHK_T0001_P000{i}_Q0001"] = ""
        qf[f"CHK_T0001_P000{i}_Q0001"] = {
            "expected_answer": "manteau",
            "accepted_examples": "manteau | le manteau | son manteau | le manteau bleu",
            "retry_prompt": "Le manteau bleu. Elle a repris quoi ?",
        }
        s[f"CHK_T0001_P000{i}_C0001"] = C_027[i]
        sons[f"CHK_T0001_P000{i}_C0001"] = ""
        s[f"CHK_T0001_P000{i}_T0002_P0000"] = [
            "maman|Tu emportes quel jeu ?",
            "narrateur|Les cubes.",
            "narrateur|Le livre.",
            "narrateur|Ou la dînette.",
        ]
        sons[f"CHK_T0001_P000{i}_T0002_P0000"] = ""

        for j, jeu in L2_027.items():
            cid2 = f"CHK_T0001_P000{i}_T0002_P000{j}"
            extra = L2_EXTRA_027[(i, j)]
            s[cid2] = L2_BODY_027[j] + [
                f"narrateur|{extra}",
                f"narrateur|On est encore {loc['ici']}.",
            ]
            sons[cid2] = ""
            s[f"{cid2}_T0003_P0000"] = [
                "papa|C'est quel moment, pour le marché ?",
                "narrateur|Le matin.",
                "narrateur|Après la sieste.",
                "narrateur|Ou le soir.",
            ]
            sons[f"{cid2}_T0003_P0000"] = ""

            for k, mom in L3_027.items():
                cid3 = f"{cid2}_T0003_P000{k}"
                img = IMG_027[(i, j, k)]
                fin = FIN_027[(i, j, k)]
                s[cid3] = (
                    MOMENT_027[k]
                    + [
                        f"narrateur|Mila a {jeu['obj']} avec elle.",
                        f"narrateur|Elle est encore {loc['ici']}.",
                    ]
                    + L3_MARCHE_027[k]
                    + [
                        f"narrateur|Elle pose {jeu['un']}, près de la caisse.",
                        "enfant-f|Le marché est à moi.",
                        "papa|Un moment, oui.",
                    ]
                    + L3_RETOUR_027
                    + [
                        f"narrateur|{img}",
                        "papa|Merci, Mila.",
                    ]
                )
                sons[cid3] = {1: "oiseau", 2: "", 3: "lampe"}.get(k, "")
                s[f"{cid3}_F0001"] = [
                    f"narrateur|Mila est passée par {loc['lab']}.",
                    f"narrateur|Elle a emporté {jeu['lab']}.",
                    f"narrateur|C'était {mom['quand']}.",
                    "narrateur|Elle a repris le manteau bleu.",
                    "narrateur|En rentrant, elle l'a raccroché.",
                    f"narrateur|{img}",
                    "maman|Le crochet attend déjà demain.",
                    "enfant-f|Le marché aussi.",
                    f"narrateur|{fin}",
                ]
                sons[f"{cid3}_F0001"] = ""
    return s, sons, qf


def main() -> None:
    s, sons, qf = build_026()
    write_story(
        "TREE-AUT-026",
        (
            "Sarah veut l'école. Le cartable jaune est vide, trop léger. "
            "Le goûter est encore sur la table. Elle le glisse dedans. "
            "À la cour, bac, toboggan ou balançoires, avec un jeu. "
            "Elle trouve une craie, un caillou ou une feuille. "
            "Elle les met dans le cartable. La boucle fait tchac."
        ),
        "Le cartable jaune de Sarah",
        "Sarah, papa, maman",
        "escalier de la maison, puis cour de l'école",
        s,
        sons,
        qf,
    )
    relecture(
        "TREE-AUT-026",
        "Le cartable jaune de Sarah",
        (
            "Sarah veut l'école. Cartable vide, goûter oublié sur la table. "
            "Elle le met. Cour : bac / toboggan / balançoires. "
            "Jeu : ballon / seau / doudou. Trésor : craie / caillou / feuille "
            "glissé dans le cartable. Pas un chant d'objets à ranger."
        ),
        (
            "Lila → Sarah. T3 Tom/Léa/Sami → craie/caillou/feuille (D16, un héros). "
            "N1 ≤ 10. Interdit « ce que l'adulte a dit ». "
            "Question : le goûter est où ? (sac/cartable)."
        ),
    )

    s, sons, qf = build_027()
    write_story(
        "TREE-AUT-027",
        (
            "Mila veut le marché. Elle sort sans le manteau bleu. "
            "L'air est froid. Elle revient le prendre. "
            "Cuisine, jardin ou chambre, avec un jeu. "
            "Matin, sieste ou soir, une orange dans le panier. "
            "Au retour, le manteau retrouve le crochet de bois."
        ),
        "Le manteau bleu de Mila au marché",
        "Mila, papa, maman",
        "maison près du marché, puis le marché",
        s,
        sons,
        qf,
    )
    relecture(
        "TREE-AUT-027",
        "Le manteau bleu de Mila au marché",
        (
            "Mila veut le marché. Sans manteau, froid, elle revient. "
            "Cuisine (boutons ouverts) / jardin (menthe, poche) / chambre "
            "(manteau sur le lit, elle le reprend). "
            "Cubes, livre ou dînette. Matin, sieste ou soir au marché. "
            "Orange. Retour, crochet."
        ),
        (
            "Tom → Mila. N2 < 16. Leçon vécue : froid sans manteau, elle revient. "
            "Question : elle a repris quoi ? (manteau). "
            "Monde ≠ TREE-AUT-016 (flaque, laine, radiateur)."
        ),
    )


if __name__ == "__main__":
    main()
