#!/usr/bin/env python3
"""TREE-DIF-016 — La tarte aux fraises de Chouchou (N1, F-NAR-018)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-016"
N1 = 10


def L(*rows: str) -> list[str]:
    out: list[str] = []
    for raw in rows:
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
    out["fil_rouge"] = (
        "Chouchou veut une tarte aux fraises pour Sarah, dans la cuisine jaune. "
        "Elles prennent le bol, la cuillère et le tablier. "
        "À la table la farine cache la recette, à l'évier le manteau trempé, "
        "au bac les fraises trop hautes. Elles trouvent ensemble. Sarah goûte."
    )
    out["title"] = "La tarte aux fraises de Chouchou"
    out["characters"] = "Chouchou, Sarah, papa, maman"
    out["setting"] = "cuisine jaune, évier, bac du jardin"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "pas rire",
        "sami",
        "il ne faut pas",
    ):
        if bad in blob:
            raise SystemExit(f"{SID} slogan: {bad}")
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
        "lab": "le bol bleu",
        "cap": "Le bol bleu",
        "t1q": "dans le bol",
        "t1acc": "bol | le bol | dans le bol | au fond du bol",
        "t1retry": "La fraise est dans le bol.",
    },
    2: {
        "lab": "la cuillère",
        "cap": "La cuillère",
        "t1q": "près de la cuillère",
        "t1acc": "cuillère | la cuillère | près de la cuillère | à côté",
        "t1retry": "La fraise est près de la cuillère.",
    },
    3: {
        "lab": "le tablier",
        "cap": "Le tablier",
        "t1q": "dans la poche",
        "t1acc": "poche | la poche | dans la poche | poche du tablier",
        "t1retry": "La fraise est dans la poche.",
    },
}

T3_LABS = {
    1: ("attendre un peu", "regarder avec Sarah", "tenir le bol"),
    2: ("le crochet", "les manches", "la passoire"),
    3: ("la marche", "les bras de papa", "les fraises basses"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Chouchou tire le bol bleu vers elle.",
            "enfant-f|La fraise va dedans.",
            "maman|Glisse-la, tout doux.",
            "narrateur|Un petit toc sonne au fond.",
            "papa|La cuillère aussi, près du bol.",
            "narrateur|Maman noue le tablier, tout lâche.",
            "narrateur|Les trois affaires restent ensemble.",
            "enfant-f|Sarah va goûter ma tarte.",
            "narrateur|La porte de la cuisine s'ouvre.",
            "copine|Chouchou, je suis là.",
            "enfant-f|Viens, on fait la tarte.",
            "papa|Le bol d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Chouchou prend la cuillère en bois.",
            "enfant-f|La fraise reste juste à côté.",
            "papa|Le manche sent encore le beurre.",
            "narrateur|Le bois est un peu rêche.",
            "maman|Le bol bleu, ensuite, sur la table.",
            "narrateur|Elle glisse le tablier par-dessus.",
            "narrateur|Les trois affaires restent ensemble.",
            "enfant-f|Sarah va tout voir.",
            "narrateur|Des pas légers sonnent dans l'entrée.",
            "copine|Me voilà, Chouchou.",
            "enfant-f|On mélange, toutes les deux ?",
            "maman|La cuillère d'abord, elle est prête.",
        )
    return L(
        "narrateur|Chouchou passe la tête dans le tablier.",
        "enfant-f|Je cache la fraise ici.",
        "maman|Dans la poche, comme un secret.",
        "narrateur|Le tissu sent encore le savon.",
        "papa|Le bol et la cuillère, avec vous.",
        "narrateur|Il les pose près du beurre.",
        "narrateur|Les trois affaires restent ensemble.",
        "enfant-f|Sarah, vite !",
        "narrateur|Un manteau rouge apparaît au seuil.",
        "copine|J'arrive, Chouchou.",
        "enfant-f|Je te fais une tarte.",
        "papa|Le tablier d'abord, il est noué.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Le bol bleu porte la fraise, au fond.",
            "copine|Elle est trop rouge !",
            "enfant-f|C'est pour toi, Sarah.",
            "narrateur|Sarah a des lunettes neuves.",
            "narrateur|Elles brillent un peu, tout calmes.",
            "maman|Le beurre vous attend.",
            "papa|On reste à la cuisine ?",
            "enfant-f|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "narrateur|La cuillère veille près de la fraise.",
            "copine|Je vois le rouge !",
            "enfant-f|Ne touche pas encore.",
            "narrateur|Sarah a les cheveux tout courts.",
            "narrateur|Une pince bleue tient une mèche.",
            "papa|Ça sent déjà la vanille.",
            "maman|Vos mains, au-dessus du bois ?",
            "copine|Oui, maman.",
        )
    return L(
        "narrateur|Le tablier cache encore la fraise.",
        "copine|Ça sent le savon.",
        "enfant-f|Elle est là, dans la poche.",
        "narrateur|Le manteau rouge de Sarah tombe long.",
        "narrateur|Les manches dépassent un peu ses mains.",
        "maman|La cuisine est tiède, devant.",
        "papa|On y va, tous les quatre ?",
        "enfant-f|Oui.",
    )


def t2_question() -> list[str]:
    return L(
        "narrateur|La cuisine sent encore le beurre.",
        "narrateur|La table a un nuage de farine.",
        "narrateur|L'évier goutte, tout doux.",
        "narrateur|Le bac du jardin a des fraises.",
        "papa|On commence où, pour la tarte ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|Le bol bleu tape un peu le bois.",
            2: "narrateur|La cuillère racle un coin de farine.",
            3: "narrateur|Le tablier frotte le bord de table.",
        }[t1]
        return L(
            lead,
            "narrateur|Un nuage blanc s'élève, tout léger.",
            "enfant-f|Je ne vois plus les mots.",
            "copine|Le carnet a disparu.",
            "narrateur|La farine poudre les lunettes de Sarah.",
            "narrateur|Un peu reste dans ses cheveux courts.",
            "enfant-f|On souffle ?",
            "papa|Doucement, le nuage retombe.",
            "maman|Le carnet est encore là, dessous.",
            "copine|On le retrouve ensemble ?",
            "papa|Vous faites comment, toutes les deux ?",
        )
    if t2 == 2:
        lead = {
            1: f"narrateur|{o['cap']} penche au-dessus de l'eau.",
            2: f"narrateur|{o['cap']} tapote le bord de l'évier.",
            3: f"narrateur|{o['cap']} frôle le robinet, tout mouillé.",
        }[t1]
        return L(
            lead,
            "enfant-f|On lave les fraises, Sarah.",
            "copine|Pour qu'elles brillent vraiment.",
            "narrateur|Le manteau rouge touche l'eau froide.",
            "narrateur|Les manches deviennent lourdes, tout de suite.",
            "copine|Ça colle à mes poignets.",
            "enfant-f|Tes manches sont trop longues.",
            "maman|Le manteau peut attendre au sec.",
            "papa|L'eau reste dans l'évier.",
            "copine|On lave comment, alors ?",
            "papa|Vous trouvez, toutes les deux ?",
        )
    lead = {
        1: f"narrateur|{o['cap']} tapote l'herbe, tout léger.",
        2: f"narrateur|{o['cap']} frôle les feuilles, tout doux.",
        3: f"narrateur|{o['cap']} reste au bord, un peu sec.",
    }[t1]
    return L(
        lead,
        "enfant-f|Les fraises du bac, Sarah.",
        "copine|Celles qui sentent le soleil.",
        "narrateur|Le bac est trop haut pour leurs mains.",
        "narrateur|Chouchou se hausse, puis recule.",
        "enfant-f|Ma main n'y arrive pas.",
        "papa|Mes bras vont plus haut, là-bas.",
        "maman|Les vôtres s'arrêtent au bord.",
        "copine|On les cueille ensemble, alors ?",
        "papa|Vous faites comment, toutes les deux ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Le nuage cache encore le carnet.",
            "papa|Attendre, regarder avec Sarah, ou tenir ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Les manches restent trop mouillées.",
            "maman|Le crochet, les manches, ou la passoire ?",
        )
    return L(
        "narrateur|Les fraises du bac restent trop haut.",
        "papa|La marche, mes bras, ou les basses ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        wait = {
            1: "narrateur|Le bol bleu attend sous le nuage.",
            2: "narrateur|La cuillère attend sous le nuage.",
            3: "narrateur|Le tablier attend sous le nuage.",
        }[t1]
        return L(
            "enfant-f|On attend un peu.",
            "copine|Moi aussi, j'attends.",
            "narrateur|La farine retombe, grain après grain.",
            wait,
            "narrateur|Le carnet redevient net, tout doux.",
            "copine|Je vois les mots, maintenant.",
            "enfant-f|Mélange, Sarah.",
            "papa|Le nuage vous a laissé la place.",
            "maman|Vous avez soufflé tout doux.",
        )
    if t2 == 1 and t3 == 2:
        use = {
            1: "narrateur|Sarah penche le bol, tout près.",
            2: "narrateur|Sarah penche la cuillère, tout près.",
            3: "narrateur|Sarah penche le tablier, tout près.",
        }[t1]
        return L(
            "copine|Mes lunettes voient encore.",
            "enfant-f|Regarde le carnet, Sarah.",
            "narrateur|Sarah essuie un grain sur le verre.",
            "narrateur|Les mots reviennent, tout nets.",
            use,
            "copine|Là, on mélange trois tours.",
            "enfant-f|Je le fais avec toi.",
            "papa|Vous lisez ensemble.",
            "maman|Les lunettes ont aidé, tout calme.",
        )
    if t2 == 1 and t3 == 3:
        hold = {
            1: "narrateur|Papa tient le bol, tout stable.",
            2: "narrateur|Papa tient la cuillère, tout stable.",
            3: "narrateur|Papa tient le tablier, tout stable.",
        }[t1]
        return L(
            "enfant-f|Papa, tu tiens le bol ?",
            "papa|Je le tiens, Chouchou.",
            hold,
            "narrateur|Sarah guide la main de Chouchou.",
            "narrateur|La farine tourne, puis s'assoit.",
            "copine|Le carnet est libre, maintenant.",
            "enfant-f|On mélange, toutes les deux.",
            "maman|Vous y arrivez ensemble.",
            "narrateur|Un peu de blanc reste aux cheveux.",
        )
    if t2 == 2 and t3 == 1:
        hook = {
            1: "narrateur|Le bol bleu attend au sec, à côté.",
            2: "narrateur|La cuillère attend au sec, à côté.",
            3: "narrateur|Le tablier attend au sec, à côté.",
        }[t1]
        return L(
            "copine|Je le mets au crochet.",
            "enfant-f|Oui, tout haut.",
            "narrateur|Sarah accroche le manteau rouge.",
            "narrateur|Les manches gouttent, puis se taisent.",
            hook,
            "enfant-f|Tes bras sont libres, maintenant.",
            "copine|On lave les fraises.",
            "papa|Le manteau sèche à sa place.",
            "maman|L'eau reste dans l'évier.",
        )
    if t2 == 2 and t3 == 2:
        roll = {
            1: "narrateur|Chouchou pose le bol près du savon.",
            2: "narrateur|Chouchou pose la cuillère près du savon.",
            3: "narrateur|Chouchou relève le tablier, tout court.",
        }[t1]
        return L(
            "enfant-f|On roule tes manches, Sarah.",
            "copine|Aide-moi, Chouchou.",
            roll,
            "narrateur|Les deux filles plient le tissu.",
            "narrateur|Les poignets de Sarah apparaissent.",
            "copine|L'eau ne les touche plus.",
            "enfant-f|On lave, maintenant.",
            "maman|Vos manches sont au sec.",
            "papa|Les fraises peuvent briller.",
        )
    if t2 == 2 and t3 == 3:
        col = {
            1: "narrateur|Sarah tient le bol, Chouchou rince.",
            2: "narrateur|Sarah tient la cuillère, Chouchou rince.",
            3: "narrateur|Sarah tient le tablier, Chouchou rince.",
        }[t1]
        return L(
            "enfant-f|La passoire, Sarah.",
            "copine|Je la tiens, toi tu verses.",
            "narrateur|Maman tend la passoire ronde.",
            col,
            "narrateur|L'eau s'échappe, les fraises restent.",
            "enfant-f|Elles brillent, maintenant.",
            "copine|Mes manches n'ont presque rien.",
            "papa|Vous avez versé ensemble.",
            "maman|La passoire a fait le travail.",
        )
    if t2 == 3 and t3 == 1:
        step = {
            1: "narrateur|Le bol bleu attend au pied de la marche.",
            2: "narrateur|La cuillère attend au pied de la marche.",
            3: "narrateur|Le tablier attend au pied de la marche.",
        }[t1]
        return L(
            "enfant-f|Je monte sur la marche.",
            "copine|Je te vois, tout près.",
            "narrateur|Chouchou cueille une fraise chaude.",
            "narrateur|Sarah ouvre les deux mains.",
            "enfant-f|Elle est à toi, un moment.",
            step,
            "copine|J'en prends une autre, plus bas.",
            "papa|Vous êtes à votre hauteur.",
            "maman|Le bac reste à sa place.",
        )
    if t2 == 3 and t3 == 2:
        arms = {
            1: "narrateur|Papa pose le pot près du bol.",
            2: "narrateur|Papa pose le pot près de la cuillère.",
            3: "narrateur|Papa pose le pot près du tablier.",
        }[t1]
        return L(
            "enfant-f|Papa, un peu plus bas.",
            "papa|Je vous le descends.",
            "narrateur|Le pot de fraises arrive au menton.",
            arms,
            "copine|Je les vois trop bien !",
            "enfant-f|On cueille, toutes les deux.",
            "narrateur|Deux mains, deux fraises, même hauteur.",
            "maman|Vous les avez, enfin.",
            "papa|Mes bras ont juste aidé.",
        )
    low = {
        1: "narrateur|Elles glissent les fraises dans le bol.",
        2: "narrateur|Elles glissent les fraises près de la cuillère.",
        3: "narrateur|Elles glissent les fraises dans la poche.",
    }[t1]
    return L(
        "enfant-f|On prend celles d'en bas.",
        "copine|Celles qu'on touche, sans monter.",
        "narrateur|Des fraises basses pendent, toutes mûres.",
        low,
        "narrateur|Le soleil les a déjà chaudes.",
        "enfant-f|On en a assez, Sarah.",
        "copine|Pour la tarte, oui.",
        "papa|Vos mains allaient assez loin.",
        "maman|Le bac garde les hautes, pour plus tard.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    coda = {
        1: "narrateur|Le bol bleu sèche près de l'évier.",
        2: "narrateur|La cuillère sèche près de l'évier.",
        3: "narrateur|Le tablier sèche près de l'évier.",
    }[t1]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|La tarte sort, encore toute chaude.",
            "copine|On a attendu le nuage, d'abord.",
            "enfant-f|Puis on a mélangé.",
            "papa|Vous avez laissé la farine retomber.",
            "maman|Cette part est pour Sarah.",
            "narrateur|Sarah goûte, tout petit.",
            "copine|Elle est sucrée !",
            coda,
            "narrateur|Un grain de farine dort sur le bois.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|La tarte brille sous la fenêtre.",
            "enfant-f|Tes lunettes ont vu les mots.",
            "copine|Oui, tout près de mes yeux.",
            "papa|Vous avez lu ensemble.",
            "maman|Posez-la sur le rebord, au chaud.",
            "narrateur|Un peu de buée prend les verres.",
            coda,
            "enfant-f|Goûte, Sarah.",
            "narrateur|Le rouge de la fraise reste au coin.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Le bol a voyagé jusqu'à la table.",
            "copine|Papa le tenait, nous on tournait.",
            "enfant-f|La farine s'est assise.",
            "maman|Vos cheveux ont un peu de blanc.",
            "papa|Soufflez, tout léger, dehors.",
            f"narrateur|{o['cap']} pose une auréole de farine.",
            "narrateur|Sarah goûte la part du milieu.",
            "enfant-f|Elle est à nous.",
            "narrateur|Le beurre sent encore, tout chaud.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Elles rentrent les mains encore fraîches.",
            "enfant-f|Ton manteau sèche au crochet.",
            "copine|Les fraises ont brillé, après.",
            "papa|Le rouge a attendu à sa place.",
            "maman|La tarte est prête, sur le bois.",
            "enfant-f|Elle est pour Sarah, maintenant.",
            "copine|Elle est un peu chaude encore.",
            coda,
            "narrateur|Une goutte sèche déjà sur le carreau.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Les manches de Sarah sont restées sèches.",
            "copine|On les a roulées, toutes les deux.",
            "enfant-f|Tes poignets étaient libres.",
            "maman|L'eau n'a pas pris le tissu.",
            "papa|Lavez-vous, tout doux, encore un peu.",
            f"narrateur|{o['cap']} garde une petite goutte.",
            "copine|Je goûte, Chouchou.",
            "narrateur|La tarte craque, puis se tait.",
            "narrateur|Une miette rouge reste sur le bois.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|La passoire sèche encore près du robinet.",
            "enfant-f|Tu tenais, moi je versais.",
            "copine|Les fraises sont restées, l'eau est partie.",
            "papa|Vous avez versé ensemble.",
            "maman|Changez le tablier, s'il est mouillé.",
            coda,
            "narrateur|Une goutte rouge marque le carreau.",
            "enfant-f|Regarde-la, Sarah, elle brille.",
            "narrateur|La tarte reste au chaud, sur la table.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|La marche a un peu de terre, encore.",
            "copine|Tu l'as cueillie pour moi.",
            "enfant-f|Tu tenais tes mains ouvertes.",
            "maman|Essuie tes pieds, sur le paillasson.",
            "papa|Les fraises sont chaudes, maintenant.",
            "narrateur|Sarah pose sa part contre la vitre.",
            coda,
            "narrateur|Un rai de soleil traverse le rouge.",
            "narrateur|Dehors, le bac redevient calme.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Le pot est redescendu jusqu'à la porte.",
            "enfant-f|Papa l'a mis à notre menton.",
            "copine|On a cueilli ensemble, après.",
            "papa|Le bac vous a laissé le temps.",
            "maman|La terre sèche déjà sur vos doigts.",
            f"narrateur|{o['cap']} pose un grain de terre.",
            "copine|Elle brille trop, Chouchou.",
            "enfant-f|C'est pour ça.",
            "narrateur|La vitre garde le rouge, tout proche.",
        )
    return L(
        "narrateur|Un peu de terre reste au seuil.",
        "enfant-f|On a pris celles d'en bas.",
        "copine|Sans trop monter.",
        "papa|Le bac a gardé les hautes.",
        "maman|Vos mains sentent encore le soleil.",
        coda,
        "narrateur|Sarah pose sa part au rebord.",
        "enfant-f|Tu l'as goûtée, enfin.",
        "narrateur|Le beurre brille un peu, puis s'endort.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|La cuisine sent déjà le beurre tiède.",
        "narrateur|Un rai de soleil barre la table.",
        "narrateur|Des fraises brillent sur le rebord.",
        "narrateur|Le bois est un peu collant.",
        "papa|Sarah arrive bientôt, Chouchou.",
        "maman|Le carnet de recettes est ouvert.",
        "narrateur|En ce moment, Chouchou touche une fraise.",
        "enfant-f|Elle est pour Sarah !",
        "narrateur|Le rouge tient toute seule, au creux.",
        "enfant-f|Je veux lui faire une tarte.",
        "maman|On prépare les affaires, alors ?",
        "papa|Merci, tu la tiens tout doux.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Les affaires attendent près du beurre.",
        "narrateur|Le bol, la cuillère, et le tablier.",
        "maman|Tu prends quoi d'abord, Chouchou ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le bol bleu", "la cuillère", "le tablier")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Chouchou a glissé la fraise {o['t1q']}.",
            "maman|Elle est où, la fraise ?",
        )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question()
        extras[f"{p}_T0002_P0000"] = t3lab("la table", "l'évier", "le bac")

        for t2 in (1, 2, 3):
            sp = f"{p}_T0002_P000{t2}"
            s[sp] = t2_scene(t1, t2)
            s[f"{sp}_T0003_P0000"] = t3_question(t2)
            extras[f"{sp}_T0003_P0000"] = t3lab(*T3_LABS[t2])
            for t3 in (1, 2, 3):
                s[f"{sp}_T0003_P000{t3}"] = t3_scene(t1, t2, t3)
                s[f"{sp}_T0003_P000{t3}_F0001"] = fin_scene(t1, t2, t3)

    write_tree(s, extras, sons)
    relecture(
        SID,
        "La tarte aux fraises de Chouchou",
        "Chouchou veut une tarte aux fraises pour Sarah. T1 = bol / cuillère / tablier "
        "(les trois restent). T2 = table (farine) / évier (manteau mouillé) / bac trop haut. "
        "T3 = neuf résolutions (attendre, lunettes de Sarah, tenir le bol ; crochet, manches, "
        "passoire ; marche, bras de papa, fraises basses). La leçon (lunettes, cheveux, habit) "
        "se vit : on cuisine ensemble, sans slogan. Fin : Sarah goûte.",
        "N1 ≤ 10. Sami et cuisine/jardin/chambre/ballon jetés. "
        "Un merci de papa lié au geste (tenir la fraise). Audio non cuit.",
    )


if __name__ == "__main__":
    main()
