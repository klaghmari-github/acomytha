#!/usr/bin/env python3
"""TREE-DIF-005 — Aniss, toboggan, Nino cherche ses mots. N1. Texte seulement."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

N1 = LIMITS["N1"]
SID = "TREE-DIF-005"


def vet(lines: list[str]) -> list[str]:
    out = []
    for raw in lines:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N1:
            raise SystemExit(f"{n}>{N1}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        out.append(f"{role}|{ph}")
    return out


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {
        "expected_answer": ans,
        "accepted_examples": acc,
        "retry_prompt": retry,
    }


def write_tree(
    fil: str,
    title: str,
    chars: str,
    setting: str,
    scripts: dict[str, list[str]],
    sons: dict[str, str],
    extras: dict[str, dict],
) -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"{SID} missing={missing[:8]} extra={sorted(extra_ids)[:8]}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        if kind == "passage_question":
            scale, rate = 1.28, "slow"
        else:
            scale, rate = 1.22, "medium"
        nc = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), scale, rate)
        if cid in extras:
            nc.update(extras[cid])
        by[cid] = nc
    out = dict(src)
    out["fil_rouge"] = fil
    out["title"] = title
    out["characters"] = chars
    out["setting"] = setting
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    n_moment = blob.count("en ce moment")
    if n_moment != 1:
        raise SystemExit(f"{SID}: en ce moment ×{n_moment}")
    if "noé" in blob:
        raise SystemExit(f"{SID}: Noé hors troupe")
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{SID} {c['chunk_id']} fin mécanique: {last}")
    check(SID, out["age_band"], out["chunks"])
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


# T1 colore : matin / sieste / soir
# T2×T3 = 9 aventures au parc (bac, échelle, herbe × ballon, seau, doudou)

TONE = {
    1: {
        "air": "La rosée brille encore sur l'herbe.",
        "sable": "Du sable froid remplit le bac.",
        "metal": "Sous les doigts, le métal pique un peu.",
        "bruit": "Un moineau crie, tout près.",
        "lum": "L'ombre du platane est longue.",
        "quand": "ce matin",
        "fin": "Sur le banc du matin, ça pique encore.",
        "peau": "Les doigts d'Aniss sont un peu rouges.",
    },
    2: {
        "air": "L'air sent la poussière chaude.",
        "sable": "Sous les paumes, le sable brûle un peu.",
        "metal": "Au toucher, le toboggan est tiède.",
        "bruit": "Une cigale frotte, tout loin.",
        "lum": "La lumière pèse, toute blanche.",
        "quand": "après la sieste",
        "fin": "Voilà le banc de la sieste, tout chaud.",
        "peau": "Une goutte coule sur la tempe d'Aniss.",
    },
    3: {
        "air": "La lumière devient orange, tout doux.",
        "sable": "Voilà le sable, déjà refroidi, tout fin.",
        "metal": "Maintenant le toboggan refroidit.",
        "bruit": "Un lampadaire fait un petit tic.",
        "lum": "L'ombre violette touche déjà l'herbe.",
        "quand": "ce soir",
        "fin": "Près du banc du soir, l'air est frais.",
        "peau": "Les genoux d'Aniss ont du sable froid.",
    },
}


def t1_pass(t1: int) -> list[str]:
    t = TONE[t1]
    if t1 == 1:
        return vet(
            [
                f"narrateur|{t['air']}",
                f"narrateur|{t['sable']}",
                f"narrateur|{t['metal']}",
                "enfant-m|Je veux glisser maintenant !",
                "narrateur|Nino pose un pied sur l'échelle.",
                "copain|Le toboggan a.",
                "narrateur|Le mot reste coincé, tout petit.",
                "narrateur|Aniss ouvre la bouche, puis attend.",
                "maman|Tu l'entends, Aniss ?",
                "enfant-m|Oui.",
                "enfant-m|Il cherche.",
                "papa|Le parc est calme, ce matin.",
                f"narrateur|{t['bruit']}",
                "enfant-m|Après, on glisse.",
            ]
        )
    if t1 == 2:
        return vet(
            [
                f"narrateur|{t['lum']}",
                f"narrateur|{t['metal']}",
                f"narrateur|{t['sable']}",
                "enfant-m|Je veux glisser, vite !",
                "narrateur|Nino parle, tout bas, tout lent.",
                "copain|Le bac est.",
                "narrateur|Aniss se tait, les mains au barreau.",
                "maman|Tu l'entends, ce murmure ?",
                "enfant-m|Oui, maman.",
                "enfant-m|C'est Nino.",
                "papa|Le parc dore, après la sieste.",
                f"narrateur|{t['bruit']}",
                "enfant-m|J'attends.",
            ]
        )
    return vet(
        [
            f"narrateur|{t['air']}",
            f"narrateur|{t['bruit']}",
            "narrateur|Le sable colle sur le toboggan.",
            "enfant-m|Je veux glisser avant la nuit !",
            "narrateur|Nino cherche encore un mot.",
            "copain|Je glisse avec.",
            "narrateur|Aniss attend, tout calme.",
            "papa|Le métal refroidit, ce soir.",
            "maman|Tu vois le sable, Aniss ?",
            "enfant-m|Oui.",
            "enfant-m|Sur le toboggan.",
            f"narrateur|{t['lum']}",
            "enfant-m|On glisse après.",
        ]
    )


def t1_q(t1: int) -> list[str]:
    if t1 == 1:
        return vet(["maman|Aniss veut quoi ?"])
    if t1 == 2:
        return vet(["papa|Qui parle doucement ?"])
    return vet(["maman|Où colle le sable ?"])


def t1_c(t1: int) -> list[str]:
    t = TONE[t1]
    if t1 == 1:
        fin = "Le toboggan a du sable."
    elif t1 == 2:
        fin = "Le bac est plein."
    else:
        fin = "Je glisse avec toi."
    return vet(
        [
            "narrateur|Nino reprend, tout doux.",
            f"copain|{fin}",
            "enfant-m|On y va.",
            "papa|Merci, Aniss.",
            "maman|On peut avancer, maintenant.",
            f"narrateur|{t['lum']}",
            "papa|Où va-t-on d'abord ?",
        ]
    )


def t2_tr(t1: int) -> list[str]:
    if t1 == 1:
        lead = "Le matin ouvre trois chemins dans le parc."
        q = "Le bac, l'échelle, ou l'herbe ?"
        who = "papa"
    elif t1 == 2:
        lead = "Après la sieste, trois endroits attendent."
        q = "Le bac, l'échelle, ou l'herbe ?"
        who = "maman"
    else:
        lead = "Le soir laisse trois petits chemins."
        q = "Le bac, l'échelle, ou l'herbe ?"
        who = "papa"
    return vet(
        [
            f"narrateur|{lead}",
            f"{who}|{q}",
            "maman|Tu choisis.",
        ]
    )


def t2_pass(t1: int, t2: int) -> list[str]:
    t = TONE[t1]
    if t2 == 1:
        # bac : on creuse, Nino parle du sable
        if t1 == 1:
            return vet(
                [
                    "narrateur|Aniss court vers le bac, tout léger.",
                    f"narrateur|{t['sable']}",
                    "narrateur|Nino y enfonce une main, puis s'arrête.",
                    "copain|Le sable est.",
                    "narrateur|Le mot tremble au bord des lèvres.",
                    "enfant-m|Je t'écoute.",
                    "maman|Il cherche encore, Aniss.",
                    "papa|Le bac est plein, ce matin.",
                    f"narrateur|{t['lum']}",
                    "copain|Le sable est collant.",
                    "enfant-m|On pourra glisser après.",
                ]
            )
        if t1 == 2:
            return vet(
                [
                    "narrateur|Ils rejoignent le bac, pas à pas.",
                    f"narrateur|{t['sable']}",
                    "narrateur|Nino souffle, une main au-dessus.",
                    "copain|Le château est.",
                    "narrateur|Aniss s'assoit, sans presser.",
                    "papa|Tu attends sa phrase ?",
                    "enfant-m|Oui, papa.",
                    f"narrateur|{t['bruit']}",
                    "copain|Le château est trop sec.",
                    "maman|On peut l'aider, tout doux.",
                    "enfant-m|Puis le toboggan.",
                ]
            )
        return vet(
            [
                "narrateur|Ils s'agenouillent près du bac.",
                f"narrateur|{t['sable']}",
                "narrateur|Nino trace une ligne, puis s'arrête.",
                "copain|La rampe a.",
                "enfant-m|Je reste.",
                "maman|Le soir donne du temps.",
                f"narrateur|{t['bruit']}",
                "copain|La rampe a pris le sable.",
                "papa|On le verra, ensemble.",
                "enfant-m|Ensuite, on glisse.",
                f"narrateur|{t['lum']}",
            ]
        )
    if t2 == 2:
        # échelle
        if t1 == 1:
            return vet(
                [
                    "narrateur|Aniss pose les mains sur l'échelle.",
                    f"narrateur|{t['metal']}",
                    "narrateur|Nino grimpe un barreau, puis s'arrête.",
                    "copain|Le premier est.",
                    "narrateur|Aniss attend, un barreau plus bas.",
                    "papa|Tu le laisses finir ?",
                    "enfant-m|Oui.",
                    f"narrateur|{t['bruit']}",
                    "copain|Le premier est froid.",
                    "maman|On monte, tout doux.",
                    "enfant-m|Le toboggan est tout près.",
                ]
            )
        if t1 == 2:
            return vet(
                [
                    "narrateur|Ils touchent l'échelle, encore chaude.",
                    f"narrateur|{t['metal']}",
                    "narrateur|Nino lève un pied, cherche le mot.",
                    "copain|Je monte le.",
                    "narrateur|Aniss compte dans sa tête, tout bas.",
                    "maman|Il va le trouver.",
                    "enfant-m|J'attends.",
                    f"narrateur|{t['air']}",
                    "copain|Je monte le deuxième.",
                    "papa|On reste derrière lui.",
                    "enfant-m|Après, on glisse.",
                ]
            )
        return vet(
            [
                "narrateur|L'échelle prend la lumière orange.",
                f"narrateur|{t['metal']}",
                "narrateur|Nino s'accroche, puis ouvre la bouche.",
                "copain|Le haut est.",
                "narrateur|Aniss ne dit rien, tout près.",
                "papa|On écoute, ce soir.",
                f"narrateur|{t['bruit']}",
                "copain|Le haut est encore clair.",
                "maman|On y va, barreau après barreau.",
                "enfant-m|Je veux glisser, après.",
                f"narrateur|{t['lum']}",
            ]
        )
    # herbe, bas du toboggan
    if t1 == 1:
        return vet(
            [
                "narrateur|Ils s'assoient dans l'herbe, tout bas.",
                f"narrateur|{t['air']}",
                "narrateur|Le pied du toboggan arrive là.",
                "copain|Je glisse vers.",
                "narrateur|Aniss tient une tige d'herbe, et attend.",
                "maman|Sa phrase va venir.",
                "enfant-m|Je reste ici.",
                f"narrateur|{t['bruit']}",
                "copain|Je glisse vers toi.",
                "papa|Le bas est doux, ce matin.",
                "enfant-m|On glisse, après.",
            ]
        )
    if t1 == 2:
        return vet(
            [
                "narrateur|L'herbe craque un peu, toute sèche.",
                f"narrateur|{t['lum']}",
                "narrateur|Ils attendent au bas du toboggan.",
                "copain|Le bas est.",
                "narrateur|Aniss souffle, les mains dans l'herbe.",
                "papa|Nino cherche, tout doux.",
                "enfant-m|J'écoute.",
                f"narrateur|{t['bruit']}",
                "copain|Le bas est chaud.",
                "maman|On peut s'y asseoir.",
                "enfant-m|Puis on grimpe.",
            ]
        )
    return vet(
        [
            "narrateur|L'herbe du soir est déjà fraîche.",
            f"narrateur|{t['air']}",
            "narrateur|Ils se placent au bas du toboggan.",
            "copain|On se voit dans.",
            "narrateur|Aniss lève les yeux, et attend.",
            "maman|Il finit, Aniss.",
            "enfant-m|Oui.",
            f"narrateur|{t['bruit']}",
            "copain|On se voit dans l'herbe.",
            "papa|Le lampadaire les touche, tout bas.",
            "enfant-m|On glisse vers ici.",
        ]
    )


def t3_tr(t1: int, t2: int) -> list[str]:
    if t2 == 1:
        lead = "Dans le bac, trois objets attendent."
    elif t2 == 2:
        lead = "Près de l'échelle, trois objets attendent."
    else:
        lead = "Dans l'herbe, trois objets attendent."
    if t1 == 3:
        lead = lead.replace("attendent.", "dorment encore.")
    return vet(
        [
            f"narrateur|{lead}",
            "papa|Le ballon rouge, le seau bleu, ou le doudou ?",
            "maman|Tu choisis.",
        ]
    )


def t3_pass(t1: int, t2: int, t3: int) -> list[str]:
    t = TONE[t1]
    # 9 aventures distinctes, T1 colore le toucher / la lumière
    if t2 == 1 and t3 == 1:
        # bac + ballon : on déterre le ballon
        return vet(
            [
                f"narrateur|{t['sable']}",
                "narrateur|Un rond rouge dépasse, à peine.",
                "copain|Le ballon est.",
                "narrateur|Aniss creuse, tout doux, et attend.",
                "papa|Il est sous le sable ?",
                "copain|Le ballon est sous le sable.",
                "enfant-m|Je le sors.",
                "narrateur|Le rouge sort, un peu sablé.",
                f"narrateur|{t['peau']}",
                "maman|Vous l'avez, tous les deux.",
                "narrateur|Ils grimpent, le ballon contre la hanche.",
                "narrateur|Puis ça file, tout court, tout vif.",
            ]
        )
    if t2 == 1 and t3 == 2:
        # bac + seau : vider le sable de la rampe dans le seau
        return vet(
            [
                f"narrateur|{t['air']}",
                "narrateur|Le seau bleu attend près du bac.",
                "copain|Le seau est.",
                "narrateur|Aniss tient l'anse, sans tirer.",
                "maman|Il va le dire.",
                "copain|Le seau est lourd.",
                "enfant-m|On verse, alors.",
                "narrateur|Ils raclent le sable de la rampe.",
                "narrateur|Le bleu se remplit, grain après grain.",
                f"narrateur|{t['metal']}",
                "papa|La rampe redevient lisse.",
                "narrateur|Ça file, tout d'un coup.",
            ]
        )
    if t2 == 1 and t3 == 3:
        # bac + doudou : doudou sablé, Nino ose ensuite
        return vet(
            [
                f"narrateur|{t['lum']}",
                "narrateur|Le doudou dort dans le bac, tout sablé.",
                "copain|Le doudou est.",
                "narrateur|Aniss garde les mains, et attend.",
                "papa|Il le veut, ce doudou ?",
                "copain|Le doudou est tout sablé.",
                "enfant-m|On le tapote.",
                "narrateur|Le sable tombe, un nuage minuscule.",
                "narrateur|Nino le serre contre sa joue.",
                f"narrateur|{t['bruit']}",
                "maman|Il est prêt, maintenant.",
                "narrateur|Ils glissent, le doudou entre eux.",
            ]
        )
    if t2 == 2 and t3 == 1:
        # échelle + ballon : ballon coincé sur un barreau
        return vet(
            [
                f"narrateur|{t['metal']}",
                "narrateur|Le ballon rouge coince un barreau.",
                "copain|Le ballon va.",
                "narrateur|Aniss ouvre les mains, en bas, et attend.",
                "maman|Tu le laisses dire ?",
                "copain|Le ballon va tomber.",
                "enfant-m|Je suis là.",
                "narrateur|Nino pousse, tout doux.",
                "narrateur|Le rouge atterrit dans les mains d'Aniss.",
                f"narrateur|{t['bruit']}",
                "papa|Le chemin est libre.",
                "narrateur|Ils montent, puis ça dévale.",
            ]
        )
    if t2 == 2 and t3 == 2:
        # échelle + seau : racler la rampe depuis le haut
        return vet(
            [
                f"narrateur|{t['lum']}",
                "narrateur|Le seau bleu pend près du haut.",
                "copain|Le seau va.",
                "narrateur|Aniss reste un barreau plus bas.",
                "papa|On l'écoute, d'accord ?",
                "copain|Le seau va nous aider.",
                "enfant-m|Je te le tends.",
                "narrateur|Nino pousse le sable, tout lentement.",
                "narrateur|Les grains tombent dans le bleu.",
                f"narrateur|{t['sable']}",
                "maman|La rampe redevient glissante.",
                "narrateur|Ils dévalent, le seau à la main.",
            ]
        )
    if t2 == 2 and t3 == 3:
        # échelle + doudou : Nino grimpe avec le doudou, mot à mot
        return vet(
            [
                f"narrateur|{t['air']}",
                "narrateur|Le doudou est coincé sur un barreau.",
                "copain|Le doudou va.",
                "narrateur|Aniss ne le prend pas, et attend.",
                "maman|Il cherche encore.",
                "copain|Le doudou va avec moi.",
                "enfant-m|Je te le passe.",
                "narrateur|Nino le glisse sous son bras.",
                "narrateur|Ils montent, barreau après barreau.",
                f"narrateur|{t['metal']}",
                "papa|Vous y êtes, tout en haut.",
                "narrateur|Ils glissent, le doudou au milieu.",
            ]
        )
    if t2 == 3 and t3 == 1:
        # herbe + ballon : marqueur d'arrivée
        return vet(
            [
                f"narrateur|{t['air']}",
                "narrateur|Ils posent le ballon dans l'herbe.",
                "copain|Le ballon reste.",
                "narrateur|Aniss recule d'un pas, et attend.",
                "papa|Il marque l'arrivée ?",
                "copain|Le ballon reste ici.",
                "enfant-m|On glisse vers lui.",
                "narrateur|Ils grimpent, puis se lancent.",
                "narrateur|Le métal chante, tout court.",
                f"narrateur|{t['peau']}",
                "maman|Le rouge les attendait.",
                "enfant-m|Encore une fois !",
            ]
        )
    if t2 == 3 and t3 == 2:
        # herbe + seau : le seau attrape le sable des fesses/genoux
        return vet(
            [
                f"narrateur|{t['sable']}",
                "narrateur|Le seau bleu attend dans l'herbe.",
                "copain|Le seau est.",
                "narrateur|Aniss pose l'anse, sans parler.",
                "maman|On attend le mot.",
                "copain|Le seau est prêt.",
                "enfant-m|On glisse, puis on verse.",
                "narrateur|Ils dévalent, un nuage de grains.",
                "narrateur|Aniss secoue ses genoux au-dessus.",
                f"narrateur|{t['bruit']}",
                "papa|Le bleu a pris le sable.",
                "enfant-m|La rampe est plus lisse !",
            ]
        )
    # herbe + doudou : spectateur dans l'herbe
    return vet(
        [
            f"narrateur|{t['lum']}",
            "narrateur|Ils posent le doudou dans l'herbe.",
            "copain|Le doudou me.",
            "narrateur|Aniss se tait, les yeux sur Nino.",
            "papa|Il n'a pas fini.",
            "copain|Le doudou me regarde.",
            "enfant-m|On glisse vers lui.",
            "narrateur|Ils montent, puis descendent, tout vifs.",
            "narrateur|Le doudou les reçoit, tout mou.",
            f"narrateur|{t['peau']}",
            "maman|Il a vu toute la descente.",
            "enfant-m|On a glissé !",
        ]
    )


FIN_IMG = {
    (1, 1, 1): "Un grain de rosée dort sur le ballon.",
    (1, 1, 2): "Une tache humide reste sous le seau.",
    (1, 1, 3): "Un fil du doudou sent encore le sable.",
    (1, 2, 1): "Un barreau garde la trace du ballon.",
    (1, 2, 2): "Une anse froide reste dans la main.",
    (1, 2, 3): "Sa joue de tissu a pris le froid.",
    (1, 3, 1): "L'herbe mouillée marque le ballon.",
    (1, 3, 2): "Une goutte tremble au bord du seau.",
    (1, 3, 3): "Un genou d'herbe colle au doudou.",
    (2, 1, 1): "Cette poussière chaude reste au rouge.",
    (2, 1, 2): "Ça sonne, tout sec, dans le seau.",
    (2, 1, 3): "Sa joue de tissu est chaude, sablée.",
    (2, 2, 1): "Un croissant de métal tiède marque le ballon.",
    (2, 2, 2): "Ça sent le fer chaud, sur l'anse.",
    (2, 2, 3): "Cette odeur de soleil reste au doudou.",
    (2, 3, 1): "Dans l'herbe sèche, le ballon s'arrête.",
    (2, 3, 2): "Une couronne de grains chauds borde le seau.",
    (2, 3, 3): "De l'herbe sèche colle au ventre du doudou.",
    (3, 1, 1): "Cette dernière lumière reste sur le ballon.",
    (3, 1, 2): "Voilà le seau, presque violet.",
    (3, 1, 3): "Un grain orange dort sur le doudou.",
    (3, 2, 1): "Vers le lampadaire, le ballon roule.",
    (3, 2, 2): "Dans l'ombre, le seau cliquette, tout bas.",
    (3, 2, 3): "Contre l'échelle, le doudou se refroidit.",
    (3, 3, 1): "Dans l'herbe fraîche, le ballon s'endort.",
    (3, 3, 2): "Un peu de sable du soir reste au seau.",
    (3, 3, 3): "Devant le toboggan, le doudou veille encore.",
}


def fin_pass(t1: int, t2: int, t3: int) -> list[str]:
    t = TONE[t1]
    img = FIN_IMG[(t1, t2, t3)]
    if t2 == 1:
        lieu = "Ils quittent le bac, les genoux sablés."
    elif t2 == 2:
        lieu = "Ils descendent de l'échelle, tout calmes."
    else:
        lieu = "Ils restent un moment dans l'herbe."
    if t3 == 1:
        objet = "Aniss tient encore le ballon rouge."
    elif t3 == 2:
        objet = "Nino balance le seau, tout vide."
    else:
        objet = "Le doudou voyage sous le bras de Nino."
    return vet(
        [
            "narrateur|Ils ont glissé, l'un après l'autre.",
            f"narrateur|{lieu}",
            f"narrateur|{objet}",
            "enfant-m|C'était bien.",
            "papa|Le toboggan a chanté, tout court.",
            "maman|On rejoint le banc ?",
            "enfant-m|Oui.",
            f"narrateur|{t['fin']}",
            f"narrateur|{img}",
        ]
    )


def build() -> None:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = vet(
        [
            "narrateur|Au bout du village, le parc s'ouvre.",
            "narrateur|Un platane jette une ombre ronde.",
            "narrateur|Des moineaux picorent près du bac.",
            "narrateur|Le toboggan en métal brille un peu.",
            "narrateur|Du sable fin colle déjà sur la rampe.",
            "narrateur|Ça sent le soleil et la poussière.",
            "papa|Tu vois le toboggan, Aniss ?",
            "enfant-m|Oui, papa.",
            "enfant-m|Il brille.",
            "maman|Le banc est encore un peu froid.",
            "narrateur|En ce moment, Aniss tire sa chaussure.",
            "enfant-m|Je veux glisser !",
            "narrateur|Nino est déjà près de l'échelle.",
            "narrateur|Ses lèvres bougent, tout lentement.",
            "copain|Je veux le.",
            "papa|Nino te parle, Aniss ?",
            "enfant-m|Oui.",
        ]
    )
    sons["CHK_T0000_P0000"] = "enfants_parc"

    s["CHK_T0001_P0000"] = vet(
        [
            "narrateur|Le parc change avec le jour.",
            "papa|Le matin, après la sieste, ou le soir ?",
            "maman|Tu choisis.",
        ]
    )
    extras["CHK_T0001_P0000"] = t3lab("le matin", "après la sieste", "le soir")

    qmap = {
        1: qf(
            "glisser",
            "glisser | le toboggan | toboggan | glisser maintenant | il veut glisser",
            "Aniss veut glisser. Il veut quoi ?",
        ),
        2: qf(
            "Nino",
            "nino | c'est nino | nino parle | lui",
            "Nino parle doucement. Qui parle ?",
        ),
        3: qf(
            "sur le toboggan",
            "toboggan | sur le toboggan | le toboggan | rampe | sur la rampe",
            "Le sable colle sur le toboggan. Où ?",
        ),
    }

    for t1 in (1, 2, 3):
        p1 = f"CHK_T0001_P000{t1}"
        s[p1] = t1_pass(t1)
        sons[p1] = "enfants_parc"
        s[f"{p1}_Q0001"] = t1_q(t1)
        extras[f"{p1}_Q0001"] = qmap[t1]
        s[f"{p1}_C0001"] = t1_c(t1)
        sons[f"{p1}_C0001"] = "enfants_parc"
        s[f"{p1}_T0002_P0000"] = t2_tr(t1)
        extras[f"{p1}_T0002_P0000"] = t3lab("le bac", "l'échelle", "l'herbe")
        for t2 in (1, 2, 3):
            p2 = f"{p1}_T0002_P000{t2}"
            s[p2] = t2_pass(t1, t2)
            sons[p2] = "enfants_parc"
            s[f"{p2}_T0003_P0000"] = t3_tr(t1, t2)
            extras[f"{p2}_T0003_P0000"] = t3lab(
                "le ballon rouge", "le seau bleu", "le doudou"
            )
            for t3 in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{t3}"
                s[p3] = t3_pass(t1, t2, t3)
                sons[p3] = "enfants_parc"
                s[f"{p3}_F0001"] = fin_pass(t1, t2, t3)
                sons[f"{p3}_F0001"] = "enfants_parc"

    title = "Le sable du toboggan et la phrase d'Aniss"
    fil = (
        "Aniss veut glisser. Du sable colle à la rampe. "
        "Nino cherche ses mots. Aniss attend la fin. "
        "Puis ils glissent, avec le ballon, le seau ou le doudou."
    )
    write_tree(
        fil,
        title,
        "Aniss, Nino, papa, maman",
        "le parc du village, toboggan et bac à sable",
        s,
        sons,
        extras,
    )
    relecture(
        SID,
        title,
        "Aniss veut glisser au parc. Sable sur la rampe, Nino cherche ses mots. "
        "T1 colore le jour (matin froid, sieste chaude, soir orange). "
        "T2 bac / échelle / herbe. T3 ballon / seau / doudou : neuf aventures "
        "(déterrer, racler, tapoter, attraper, monter, marquer, verser). "
        "Ils glissent vraiment. Leçon vécue, jamais « laisser le temps » en slogan.",
        "Noé→Aniss, copain Nino (D16). N1 ≤10. T2 labels cuisine/jardin/chambre "
        "→ bac/échelle/herbe (le parc, pas la maison). "
        "Questions de récit, pas le slogan. Un merci de papa après l'attente. "
        "« en ce moment » une fois. Fins sensorielles, pas « l'histoire est finie ». "
        "Chemins relus : matin-bac-ballon ; sieste-échelle-seau ; soir-herbe-doudou ; "
        "et les neuf T2×T3 au matin pour la cohérence des objets.",
    )


if __name__ == "__main__":
    build()
