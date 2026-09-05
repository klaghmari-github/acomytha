#!/usr/bin/env python3
"""TREE-DIF-058 — Les clochettes de Chouchou, au-dessus de la porte (N3, DIF.COR.001)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-058"
N3 = 16
TITLE = "Les clochettes de Chouchou, au-dessus de la porte"
FIL = (
    "Le soir, dans la chambre. Une barre jaune du réverbère traverse le plancher. "
    "Chouchou veut accrocher trois clochettes, pour que la porte sonne quand Nino entre. "
    "Nino est plus grand. Ils emportent les clochettes, le ruban rouge et l'anneau de bois. "
    "Au crochet de la porte, au pied du lit, au loquet de la fenêtre : "
    "trois hauteurs, neuf façons. La porte sonne pour eux."
)
CHARS = "Chouchou, Nino, papa, maman"
SETTING = "chambre le soir : porte, lit, fenêtre"


def L(*rows: str) -> list[str]:
    out: list[str] = []
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N3:
            raise SystemExit(f"{n}>{N3}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        out.append(f"{role}|{ph}")
    return out


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {"expected_answer": ans, "accepted_examples": acc, "retry_prompt": retry}


def write_tree(scripts: dict[str, list[str]], extras: dict[str, dict], sons: dict[str, str]) -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"{SID} missing={missing[:8]} extra={sorted(extra_ids)[:8]}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        if kind in ("passage_question", "transition_question"):
            scale, rate = 1.28, "slow"
        else:
            scale, rate = 1.22, "medium"
        nc = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), scale, rate)
        if cid in extras:
            nc.update(extras[cid])
        by[cid] = nc
    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    labels = " ".join(
        f"{c.get('option_1_label') or ''} {c.get('option_2_label') or ''} {c.get('option_3_label') or ''}"
        for c in out["chunks"]
    ).lower()
    whole = blob + "\n" + labels
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "tailles différentes",
        "plus petit ou plus grand",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "capitaine",
        "plic",
        "volet jaune",
        "pommier",
        "bac à sable",
        "toboggan",
        "balançoire",
        "sami",
        "léa",
        "lea ",
        "tom ",
        "drap à pois",
        "cabane",
        "cacao",
        "étoile",
        "loup de carton",
        "camp",
        "doudou",
        "ballon",
        "seau",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "chouchou" not in blob:
        raise SystemExit(f"{SID}: Chouchou absente")
    if "nino" not in blob:
        raise SystemExit(f"{SID}: Nino absent")
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [x for x in c["script"].splitlines() if x.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{SID} {c['chunk_id']} fin mécanique: {last}")
    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


OBJ = {
    1: {
        "lab": "les clochettes",
        "cap": "Les clochettes",
        "t1q": "contre le ventre",
        "t1acc": "ventre | le ventre | contre le ventre | son ventre",
        "t1retry": "Les clochettes sont contre le ventre.",
    },
    2: {
        "lab": "le ruban rouge",
        "cap": "Le ruban",
        "t1q": "autour du poignet",
        "t1acc": "poignet | le poignet | autour du poignet | son poignet",
        "t1retry": "Le ruban est autour du poignet.",
    },
    3: {
        "lab": "l'anneau de bois",
        "cap": "L'anneau",
        "t1q": "sous le bras",
        "t1acc": "bras | le bras | sous le bras | son bras",
        "t1retry": "L'anneau est sous le bras.",
    },
}

T3_LABS = {
    1: ("les bras de Nino", "le tabouret à deux", "la poignée plus bas"),
    2: ("le pied du lit", "deux fils", "s'asseoir ensemble"),
    3: ("le loquet du bas", "tenir le cadre", "un ruban plus long"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Chouchou serre la soucoupe, encore tiède.",
            "enfant-f|Ça sent le métal, tout près.",
            "maman|Garde-la contre ton ventre, tout droit.",
            "narrateur|Les clochettes glissent, puis tiennent.",
            "papa|Le ruban, ensuite, autour du poignet.",
            "narrateur|Nino prend l'anneau de bois.",
            "narrateur|Le métal tinte à chaque pas, vers la porte.",
            "enfant-f|Nino, tu viens près du seuil ?",
            "copain|J'arrive, Chouchou.",
            "papa|Les clochettes d'abord, vous les avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Chouchou enroule le ruban rouge, encore parfumé.",
            "enfant-f|Il sent la lavande, sur ma peau.",
            "papa|Glisse-le autour du poignet, tout droit.",
            "narrateur|Le satin froisse, puis se tait.",
            "maman|Les clochettes, ensuite, contre le ventre.",
            "narrateur|Nino prend l'anneau de bois.",
            "narrateur|Le ruban tire un peu, vers la porte.",
            "enfant-f|Nino va tout voir.",
            "narrateur|Ses épaules passent déjà sous l'abat-jour.",
            "copain|Me voilà, Chouchou.",
            "enfant-f|On les accroche, tous les deux ?",
            "maman|Le ruban d'abord, il est prêt.",
        )
    return L(
        "narrateur|Chouchou soulève l'anneau de bois, un peu rêche.",
        "enfant-f|Il est tiède, comme le plancher.",
        "maman|Serre-le sous ton bras, tout droit.",
        "narrateur|Le bois fait un petit toc, contre le pull.",
        "papa|Les clochettes et le ruban, avec vous.",
        "narrateur|Elle les pose près de la chemise pliée.",
        "narrateur|Rien ne reste dans la soucoupe.",
        "enfant-f|Nino, vite !",
        "narrateur|Une ombre trop longue passe au seuil.",
        "copain|J'arrive près des clochettes.",
        "enfant-f|Je te garde l'anneau.",
        "papa|L'anneau d'abord, il est prêt.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Le ventre porte la soucoupe, tout contre le pull.",
            "copain|Elles sont trop froides !",
            "enfant-f|C'est pour notre porte.",
            "narrateur|Nino a les genoux plus hauts que Chouchou.",
            "narrateur|Ses pieds touchent déjà le bas du chambranle.",
            "maman|Regarde ses genoux, près du bois.",
            "papa|On reste dans la chambre ?",
            "enfant-f|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "narrateur|Le poignet veille près du ruban.",
            "copain|Je vois le rouge !",
            "enfant-f|Ne le noue pas encore.",
            "narrateur|Nino se baisse, trop long, trop vite.",
            "narrateur|Une mèche saute sous l'abat-jour.",
            "papa|Ça sent déjà la lavande, sur le satin.",
            "maman|Vos mains, au-dessus de la soucoupe ?",
            "copain|Oui, maman.",
        )
    return L(
        "narrateur|L'anneau de bois cache encore le coude.",
        "copain|Ça sent le tiède.",
        "enfant-f|Le coin de départ est là.",
        "narrateur|Le pull de Nino s'arrête trop haut.",
        "narrateur|Les manches laissent ses poignets libres.",
        "maman|La chambre est tiède, autour.",
        "papa|On y va, tous les quatre ?",
        "enfant-f|Oui.",
    )


def t2_question(t1: int) -> list[str]:
    head = {
        1: "Les clochettes tapent le ventre, tout bas.",
        2: "Le ruban frotte le poignet, un peu lisse.",
        3: "L'anneau tape le coude, tout doux.",
    }[t1]
    return L(
        f"narrateur|{head}",
        "narrateur|Au crochet de la porte, c'est trop haut.",
        "narrateur|Tout bas, le pied du lit attend déjà.",
        "narrateur|Près du loquet, la fenêtre clignote, au milieu.",
        "papa|Vous les accrochez où, pour Nino ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|Chouchou lève la soucoupe, trop bas pour le crochet.",
            2: "narrateur|Chouchou lève le ruban, trop court pour le crochet.",
            3: "narrateur|Chouchou lève l'anneau, trop bas pour le crochet.",
        }[t1]
        mishap = {
            1: "narrateur|Une clochette tinte, puis retombe dans la paume.",
            2: "narrateur|Le satin glisse, sans accrocher le métal.",
            3: "narrateur|Le bois tape le chambranle, trop bas.",
        }[t1]
        return L(
            lead,
            "narrateur|Le crochet brille, trop loin pour Chouchou.",
            "copain|Moi je l'atteins, Chouchou !",
            "narrateur|Nino se hausse, le front contre le bois.",
            mishap,
            {
                1: "enfant-f|Les clochettes n'attendaient pas ça.",
                2: "enfant-f|Le ruban n'attendait pas ça.",
                3: "enfant-f|L'anneau n'attendait pas ça.",
            }[t1],
            "maman|Ses bras vont jusqu'au crochet.",
            "papa|Toi tu vois la poignée, lui le haut.",
            "copain|Ça va sonner trop tôt, sur mon front.",
            "papa|Vous les mettez à quelle hauteur ?",
        )
    if t2 == 2:
        lead = {
            1: "narrateur|Chouchou pose la soucoupe au pied du lit.",
            2: "narrateur|Chouchou noue le ruban au pied du lit.",
            3: "narrateur|Chouchou glisse l'anneau au pied du lit.",
        }[t1]
        mishap = {
            1: "narrateur|Les clochettes s'emmêlent dans la couverture.",
            2: "narrateur|Le satin se coince sous le matelas.",
            3: "narrateur|L'anneau roule, puis bute contre un pied.",
        }[t1]
        return L(
            lead,
            "enfant-f|Ici, c'est à ma hauteur, Nino.",
            "copain|Je m'assois, trop large !",
            "narrateur|Sa hanche heurte déjà le métal, ding.",
            mishap,
            "narrateur|Un peu de laine lève, puis retombe.",
            "maman|Ses genoux arrivent déjà au bois.",
            "papa|Toi tu noues, lui il cogne.",
            "enfant-f|On peut sonner avec lui ?",
            "papa|Comment sonner sans cogner ?",
        )
    lead = {
        1: "narrateur|Chouchou porte la soucoupe vers le carreau.",
        2: "narrateur|Chouchou tend le ruban vers le loquet.",
        3: "narrateur|Chouchou pousse l'anneau vers le rebord.",
    }[t1]
    mishap = {
        1: "narrateur|Le vent fait tinter, sans que Nino entre.",
        2: "narrateur|Le satin claque, trop loin de ses doigts.",
        3: "narrateur|L'anneau n'atteint pas encore le loquet.",
    }[t1]
    return L(
        lead,
        "enfant-f|Ici, ça respire, Nino.",
        "copain|Je touche le loquet, tout haut !",
        "narrateur|Le nœud reste trop loin pour Chouchou.",
        mishap,
        {
            1: "narrateur|Les clochettes attendent au rebord, un peu seules.",
            2: "narrateur|Le ruban attend au rebord, un peu seul.",
            3: "narrateur|L'anneau attend au rebord, un peu seul.",
        }[t1],
        "maman|Ses coudes vont jusqu'au cadre.",
        "papa|Toi tu vois le bas, lui le vent.",
        "copain|On noue comment, alors ?",
        "papa|Le nœud, vous le faites où ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Le crochet attend encore, trop haut.",
            "papa|Les bras, le tabouret, ou la poignée ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Le pied du lit attend encore, trop bas.",
            "maman|Le pied, deux fils, ou s'asseoir ensemble ?",
        )
    return L(
        "narrateur|Le loquet attend encore, trop loin.",
        "papa|Le loquet du bas, le cadre, ou un ruban plus long ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        use = {
            1: "narrateur|Chouchou tend la soucoupe, bras tout courts.",
            2: "narrateur|Chouchou tend le ruban, bras tout courts.",
            3: "narrateur|Chouchou pousse l'anneau, tout près.",
        }[t1]
        return L(
            "enfant-f|Tu noues, toi, tu vois le crochet.",
            "narrateur|Nino passe le ruban, assez haut.",
            "copain|Ça tient, tout doux.",
            use,
            "narrateur|Chouchou lève la paume, pour tester.",
            "enfant-f|Ça sonne au-dessus de moi !",
            "papa|Tes doigts allaient assez loin.",
            "narrateur|Les clochettes pendent, à leur hauteur.",
            "copain|Écoute, Chouchou.",
            "enfant-f|Elles sont à nous.",
        )
    if t2 == 1 and t3 == 2:
        wait = {
            1: "narrateur|La soucoupe attend au bord, pleine d'ombre.",
            2: "narrateur|Le ruban attend au bord, un peu lisse.",
            3: "narrateur|L'anneau attend au bord, un peu chaud.",
        }[t1]
        return L(
            "enfant-f|Je monte, tout doux.",
            "papa|Tiens le bois, Chouchou.",
            "narrateur|Chouchou se hausse, le nez au crochet.",
            "copain|Moi je noue, tout près.",
            "narrateur|Nino tient le tabouret, au-dessus.",
            "narrateur|Le nœud glisse, puis serre.",
            "copain|Tu vois, maintenant.",
            "maman|Vous le partagez.",
            wait,
        )
    if t2 == 1 and t3 == 3:
        catch = {
            1: "narrateur|Les clochettes glissent vers la poignée, ding.",
            2: "narrateur|Le ruban glisse vers la poignée, tout doux.",
            3: "narrateur|L'anneau glisse vers la poignée, toc.",
        }[t1]
        return L(
            "enfant-f|On les met plus bas, à la poignée.",
            "copain|Moi aussi, je baisse.",
            "narrateur|Nino incline le front, pour passer.",
            "narrateur|Chouchou noue autour du métal, assez petite.",
            catch,
            "papa|La poignée est venue vers vous.",
            "copain|On l'ouvre, ça sonne.",
            "enfant-f|Ça tinte encore.",
            "maman|Vos cheveux sentent le métal tiède.",
        )
    if t2 == 2 and t3 == 1:
        carry = {
            1: "narrateur|Nino pose la soucoupe au pied du bois.",
            2: "narrateur|Nino pose le ruban au pied du bois.",
            3: "narrateur|Nino pose l'anneau au pied du bois.",
        }[t1]
        return L(
            "enfant-f|Je noue au pied, tout bas.",
            "copain|Je te tends les affaires.",
            "narrateur|Chouchou s'agenouille, assez petite.",
            "narrateur|Le bois du lit s'ouvre, un peu.",
            "enfant-f|Je le tiens !",
            carry,
            "papa|Tes hanches étaient à la bonne hauteur.",
            "copain|Passe-le, un peu.",
            "enfant-f|Il sent encore la lavande.",
        )
    if t2 == 2 and t3 == 2:
        reach = {
            1: "narrateur|Chouchou tend les clochettes, bras tout courts.",
            2: "narrateur|Chouchou tend le ruban, bras tout courts.",
            3: "narrateur|Chouchou pousse l'anneau, tout près.",
        }[t1]
        return L(
            "enfant-f|On met deux fils, ici.",
            "copain|Un haut pour moi, un bas pour toi.",
            reach,
            "narrateur|Deux rubans font deux hauteurs, tout doux.",
            "narrateur|Nino passe dessous, Chouchou noue devant.",
            "copain|Je l'entends !",
            "maman|Vos fils ont trouvé le chemin.",
            "enfant-f|Ça sent le satin.",
            "papa|Le lit a deux voix, maintenant.",
        )
    if t2 == 2 and t3 == 3:
        nest = {
            1: "narrateur|Les clochettes deviennent un nid, contre le bois.",
            2: "narrateur|Le ruban devient un nid, contre le bois.",
            3: "narrateur|L'anneau devient un nid, contre le bois.",
        }[t1]
        return L(
            "enfant-f|Assieds-toi, Nino, tout doux.",
            "copain|Je me baisse, à ta hauteur.",
            "narrateur|Les genoux de Nino rejoignent les siens.",
            "narrateur|Chouchou noue, Nino tient le satin.",
            nest,
            "copain|On se parle tout près.",
            "enfant-f|Oui.",
            "maman|Vous y arrivez, tous les deux.",
            "narrateur|Deux voix tiennent le même tintement.",
        )
    if t2 == 3 and t3 == 1:
        hold = {
            1: "narrateur|Chouchou garde la soucoupe au bas du cadre.",
            2: "narrateur|Chouchou garde le ruban au bas du cadre.",
            3: "narrateur|Chouchou garde l'anneau au bas du cadre.",
        }[t1]
        return L(
            "copain|Je me hausse encore.",
            hold,
            "narrateur|Les doigts de Chouchou touchent le loquet du bas.",
            "enfant-f|Il bouge !",
            "narrateur|Le nœud penche, puis s'accroche.",
            "copain|Je tiens le haut.",
            "papa|Tes doigts allaient assez près.",
            "maman|Nino tenait bien le cadre.",
            "enfant-f|Elles sont à nous.",
        )
    if t2 == 3 and t3 == 2:
        up = {
            1: "narrateur|Chouchou pose la soucoupe contre le bois.",
            2: "narrateur|Chouchou pose le ruban contre le bois.",
            3: "narrateur|Chouchou pousse l'anneau, tout près.",
        }[t1]
        return L(
            "enfant-f|Tu tiens le cadre, Nino ?",
            "copain|Oui, tout ferme.",
            up,
            "narrateur|Papa veille près de la vitre, tout calme.",
            "narrateur|Chouchou et Nino se haussent ensemble.",
            "enfant-f|Je vois le nœud !",
            "copain|Je le sens.",
            "maman|Vous avez noué ensemble.",
            "papa|Le cadre est resté doux.",
        )
    two = {
        1: "narrateur|Nino tend la soucoupe, bras tout longs.",
        2: "narrateur|Nino tend le ruban, bras tout longs.",
        3: "narrateur|Nino pousse l'anneau, tout près.",
    }[t1]
    return L(
        "enfant-f|Un ruban plus long, Nino.",
        "copain|Je tends, d'ici.",
        two,
        "narrateur|Nino fait glisser le satin, tout doux.",
        "narrateur|Le rebord prend Chouchou, puis lui.",
        "enfant-f|Je le tiens !",
        "papa|Chacun a noué sa part.",
        "copain|Il sent le soir.",
        "maman|Vos bras n'avaient pas la même longueur.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        keep = {
            1: "narrateur|Les clochettes pendent encore au-dessus du seuil.",
            2: "narrateur|Le ruban rouge pèse encore au-dessus du seuil.",
            3: "narrateur|L'anneau de bois veille encore au-dessus du seuil.",
        }[t1]
        return L(
            "narrateur|Au crochet, la porte sent le bois chaud.",
            "copain|Tu as tendu, moi j'ai noué.",
            "enfant-f|Tes bras l'ont fait pendre.",
            "papa|Vous l'avez, enfin.",
            "maman|La chemise pliée dort sur la chaise, au calme.",
            keep,
            "enfant-f|On reste un peu, Nino.",
            "narrateur|Un tintement s'endort sur le plancher.",
            "narrateur|La barre jaune redevient douce, autour.",
        )
    if t2 == 1 and t3 == 2:
        keep = {
            1: f"narrateur|{o['cap']} restent dans la paume de Chouchou.",
            2: f"narrateur|{o['cap']} reste dans la paume de Chouchou.",
            3: f"narrateur|{o['cap']} reste dans la paume de Chouchou.",
        }[t1]
        return L(
            "narrateur|Sur le tabouret, deux têtes se calment.",
            "enfant-f|Nino, tu l'as vue glisser.",
            "copain|Oui, tout près de tes mains.",
            "papa|Toi haute, lui qui noue, ça tenait.",
            "maman|Vos voix sont devenues toutes petites.",
            keep,
            "copain|Je reste encore un peu.",
            "narrateur|Une poussière reste collée aux cheveux.",
            "narrateur|Le tapis sent encore le soir.",
        )
    if t2 == 1 and t3 == 3:
        keep = {
            1: "narrateur|Les clochettes retombent, tout léger.",
            2: "narrateur|Le ruban rouge retombe, tout léger.",
            3: "narrateur|L'anneau de bois retombe, tout léger.",
        }[t1]
        return L(
            "narrateur|La poignée redescend, tout doux.",
            "copain|Ça sonne dès qu'on tourne.",
            "enfant-f|On a baissé, tous les deux.",
            "maman|Elles n'étaient plus trop hautes.",
            "papa|Le métal froisse encore, dans l'air.",
            keep,
            "enfant-f|On souffle dessus, tout calme.",
            "narrateur|Un tintement veille près des oreillers.",
            "narrateur|Le réverbère se tait, contre le carreau.",
        )
    if t2 == 2 and t3 == 1:
        keep = {
            1: "narrateur|Les clochettes gardent un brin de laine.",
            2: "narrateur|Le ruban rouge garde un brin de laine.",
            3: "narrateur|L'anneau de bois garde un brin de laine.",
        }[t1]
        return L(
            "narrateur|Au pied du lit, ça sent le bois.",
            "copain|Mes mains savaient le chemin.",
            "enfant-f|Moi, je nouais trop bas.",
            "papa|Vous avez suivi ce qui était à vous.",
            "maman|Un brin de laine reste au pull.",
            keep,
            "enfant-f|Elles sont pour demain, les clochettes.",
            "copain|Elles sont un peu chaudes encore.",
            "narrateur|L'ombre du lit s'allonge, puis s'arrête.",
        )
    if t2 == 2 and t3 == 2:
        keep = {
            1: f"narrateur|{o['cap']} gardent un brin de laine.",
            2: f"narrateur|{o['cap']} garde un brin de laine.",
            3: f"narrateur|{o['cap']} garde un brin de laine.",
        }[t1]
        return L(
            "narrateur|Les deux fils restent, comme deux voix.",
            "enfant-f|J'ai noué d'en bas.",
            "copain|Tes bras étaient assez courts.",
            "maman|Le satin sent fort, sur vos mains.",
            "papa|Frottez-les sur le tapis, tout doux.",
            keep,
            "copain|Je le tiens, Chouchou.",
            "narrateur|Un pied de bois grince, puis se tait.",
            "narrateur|Le rouge sèche près de la fenêtre.",
        )
    if t2 == 2 and t3 == 3:
        keep = {
            1: "narrateur|Les clochettes marquent encore le bois.",
            2: "narrateur|Le ruban rouge marque encore le bois.",
            3: "narrateur|L'anneau de bois marque encore le pied.",
        }[t1]
        return L(
            "narrateur|Une voix basse, une voix plus haute, puis plus.",
            "enfant-f|Nino s'est assis à ma hauteur.",
            "copain|On a noué tout près.",
            "papa|Le lit vous a laissé la place.",
            "maman|Le secret tient encore, tout chaud.",
            keep,
            "enfant-f|Écoute-les, Nino, elles brillent.",
            "copain|Je les entends, d'ici.",
            "narrateur|Le métal reste au chaud, sur le drap.",
        )
    if t2 == 3 and t3 == 1:
        keep = {
            1: "narrateur|Les clochettes pèsent encore sur le loquet.",
            2: "narrateur|Le ruban rouge veille encore au loquet.",
            3: "narrateur|L'anneau de bois veille encore au loquet.",
        }[t1]
        return L(
            "narrateur|Les talons de Nino sont encore chauds.",
            "enfant-f|Tu as tenu le haut pour moi.",
            "copain|Tu nouais le bas.",
            "maman|Le carreau sent le soir, tout près.",
            "papa|La porte sonnera, demain.",
            "narrateur|Chouchou les pose contre la vitre.",
            keep,
            "narrateur|Un rai jaune traverse le métal.",
            "narrateur|Le loquet redevient calme, tout seul.",
        )
    if t2 == 3 and t3 == 2:
        keep = {
            1: f"narrateur|{o['cap']} posent une ombre au plancher.",
            2: f"narrateur|{o['cap']} pose une ombre au plancher.",
            3: f"narrateur|{o['cap']} pose une ombre au plancher.",
        }[t1]
        return L(
            "narrateur|Sur le rebord, deux paires de pieds se touchent.",
            "copain|Tu as noué, d'en bas.",
            "enfant-f|Tes bras ont tenu le cadre.",
            "papa|Chacun a fait sa part, à sa hauteur.",
            "maman|Le satin du ruban sèche déjà.",
            keep,
            "copain|Ça tinte trop, Chouchou.",
            "enfant-f|C'est pour ça.",
            "narrateur|La vitre garde le rouge, tout proche.",
        )
    keep = {
        1: "narrateur|Chouchou pose les clochettes au rebord.",
        2: "narrateur|Chouchou pose le ruban au rebord.",
        3: "narrateur|Chouchou pose l'anneau au rebord.",
    }[t1]
    return L(
        "narrateur|Un peu de buée reste au carreau.",
        "enfant-f|On a tiré ensemble.",
        "copain|Sans trop monter.",
        "papa|Le rebord est resté à sa place.",
        "maman|Vos mains sentent encore le soir.",
        keep,
        "copain|Tu les as eues, enfin.",
        "enfant-f|Elles sont à nous.",
        "narrateur|Le métal tremble un peu, puis s'endort.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Le réverbère pose une barre jaune sur le plancher.",
        "narrateur|Le bois de la chambre est encore chaud.",
        "narrateur|Une soucoupe tient trois clochettes, près du lit.",
        "papa|Tu as vu la barre, Chouchou ?",
        "enfant-f|Elle avance, tout doux.",
        "maman|Le ruban rouge sent encore la lavande.",
        "narrateur|En ce moment, Chouchou touche une clochette.",
        "enfant-f|Je veux qu'elles sonnent, pour Nino.",
        "papa|Nino arrive, plus grand que toi.",
        "narrateur|Nino a déjà les cheveux sous l'abat-jour.",
        "copain|On les accroche ensemble ?",
        "maman|On prépare d'abord, alors ?",
        "papa|Merci, tu tiens la soucoupe tout droit.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près du tapis.",
        "narrateur|Les clochettes, le ruban, et l'anneau.",
        "maman|Tu prends quoi d'abord, Chouchou ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("les clochettes", "le ruban rouge", "l'anneau de bois")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Chouchou a mis {o['lab']} {o['t1q']}.",
            "maman|C'est où, maintenant ?",
        )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab(
            "au crochet de la porte", "au pied du lit", "au loquet de la fenêtre"
        )
        sons[p] = ""
        sons[f"{p}_T0002_P0000"] = ""

        for t2 in (1, 2, 3):
            sp = f"{p}_T0002_P000{t2}"
            s[sp] = t2_scene(t1, t2)
            s[f"{sp}_T0003_P0000"] = t3_question(t2)
            extras[f"{sp}_T0003_P0000"] = t3lab(*T3_LABS[t2])
            sons[sp] = ""
            for t3 in (1, 2, 3):
                s[f"{sp}_T0003_P000{t3}"] = t3_scene(t1, t2, t3)
                s[f"{sp}_T0003_P000{t3}_F0001"] = fin_scene(t1, t2, t3)

    write_tree(s, extras, sons)
    relecture(
        SID,
        TITLE,
        "Chouchou veut accrocher trois clochettes dans la chambre, le soir, "
        "pour que la porte sonne quand Nino entre. Nino est plus grand. "
        "T1 = clochettes / ruban rouge / anneau de bois (les trois partent). "
        "T2 = crochet de la porte (trop haut pour Chouchou, trop bas pour le front de Nino) "
        "/ pied du lit (trop bas, sa hanche cogne) / loquet de la fenêtre "
        "(nœud trop loin, le vent tinte sans lui). "
        "T3 = neuf résolutions (bras de Nino, tabouret à deux, poignée plus bas ; "
        "pied du lit, deux fils, s'asseoir ensemble ; "
        "loquet du bas, tenir le cadre, ruban plus long). "
        "La leçon (tailles, jouer) se vit dans les gestes, sans slogan. "
        "Fin : les clochettes sonnent pour eux.",
        "N3 ≤ 16. Léa hors troupe → Chouchou + Nino (D16). "
        "Bac/toboggan/balançoires et ballon/seau/doudou et Tom/Léa/Sami jetés. "
        "Titre slogan remplacé (objet + désir). Autre récit que DIF-032 "
        "(cabane, drap à pois) et DIF-042 (cacao, étagère). "
        "Un merci de papa lié au geste (tenir la soucoupe). "
        "Pas de « bon travail ». Audio non cuit.",
    )


if __name__ == "__main__":
    main()
