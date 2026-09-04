#!/usr/bin/env python3
"""TREE-DIF-014 — Le panier de Mila et la pomme du haut (N2, DIF.COR.001)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-014"
N2 = 15


def L(*rows: str) -> list[str]:
    out: list[str] = []
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N2:
            raise SystemExit(f"{n}>{N2}: {ph}")
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
        "Sous le pommier, une pomme rouge pend trop haut. "
        "Mila la veut pour son panier, pour le goûter. "
        "Nino est plus petit, elle plus grande. "
        "Ils emportent panier, nappe et tabouret. "
        "Trois lieux, neuf façons. La pomme rentre à la maison."
    )
    out["title"] = "Le panier de Mila et la pomme du haut"
    out["characters"] = "Mila, Nino, papa, maman"
    out["setting"] = "jardin, sous le pommier"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "tailles sont différentes",
        "le corps n'est pas",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "lila",
        "sami",
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
        "lab": "le panier",
        "cap": "Le panier",
        "t1q": "dans le panier",
        "t1acc": "panier | le panier | dans le panier | au fond du panier",
        "t1retry": "La petite pomme est dans le panier.",
    },
    2: {
        "lab": "la nappe",
        "cap": "La nappe",
        "t1q": "dans la nappe",
        "t1acc": "nappe | la nappe | dans la nappe | le tissu | carreaux",
        "t1retry": "La petite pomme est dans la nappe.",
    },
    3: {
        "lab": "le tabouret",
        "cap": "Le tabouret",
        "t1q": "sur le tabouret",
        "t1acc": "tabouret | le tabouret | sur le tabouret | le bois",
        "t1retry": "La petite pomme est sur le tabouret.",
    },
}

T3_LABS = {
    1: ("le passage de Nino", "la branche levée", "la pomme qui tombe"),
    2: ("les mains de Nino", "les yeux de Mila", "l'herbe écartée"),
    3: ("le bout des doigts", "le geste d'en bas", "le banc à deux"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Mila attrape l'anse du panier.",
            "enfant-f|La petite pomme ira dedans.",
            "maman|Glisse-la, tout doux.",
            "narrateur|Une pomme déjà tombée fait toc.",
            "papa|La nappe aussi, près du sac.",
            "narrateur|Maman plie le tissu à carreaux.",
            "narrateur|Papa pose le tabouret contre le tronc.",
            "narrateur|Les trois affaires partent ensemble.",
            "enfant-f|Nino, viens sous le pommier.",
            "enfant-m|J'arrive, Mila.",
            "papa|Le panier d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Mila déplie la nappe à carreaux.",
            "enfant-f|Je cache la petite pomme.",
            "papa|Enroule-la, comme un secret.",
            "narrateur|Le tissu sent encore le jus.",
            "maman|Le panier, ensuite, près des pieds.",
            "narrateur|Elle glisse le tabouret d'une main.",
            "narrateur|Les trois affaires partent ensemble.",
            "enfant-f|Nino, on y va.",
            "enfant-m|Je suis là.",
            "maman|La nappe d'abord, elle est prête.",
        )
    return L(
        "narrateur|Mila traîne le tabouret, tout rêche.",
        "enfant-f|La petite pomme reste dessus.",
        "maman|Tiens-le droit, tout doux.",
        "narrateur|Le bois tape un petit toc.",
        "papa|Le panier et la nappe, avec vous.",
        "narrateur|Il les pose près des sandales.",
        "narrateur|Les trois affaires partent ensemble.",
        "enfant-f|Nino, vite !",
        "enfant-m|J'arrive sous l'arbre.",
        "papa|Le tabouret d'abord, il est prêt.",
    )


def t1_confirm(t1: int) -> list[str]:
    o = OBJ[t1]
    if t1 == 1:
        return L(
            f"narrateur|{o['cap']} porte la petite pomme, tout au fond.",
            "enfant-m|Elle a fait toc.",
            "enfant-f|C'est pour le goûter.",
            "maman|La grande rouge vous attend, plus haut.",
            "papa|On avance sous les feuilles ?",
            "enfant-f|Oui, papa.",
        )
    if t1 == 2:
        return L(
            f"narrateur|{o['cap']} à carreaux cache encore la petite pomme.",
            "enfant-m|Je vois un rond, sous le tissu.",
            "enfant-f|Ne touche pas encore.",
            "papa|Ça sent déjà le sucre, ici.",
            "maman|Vos pieds, dans l'herbe ?",
            "enfant-m|Oui, maman.",
        )
    return L(
        f"narrateur|{o['cap']} tient la petite pomme, tout rêche.",
        "enfant-m|Elle roule un peu.",
        "enfant-f|Je la rattrape.",
        "maman|Le pommier est calme, devant.",
        "papa|On y va, tous les quatre ?",
        "enfant-f|Oui.",
    )


def t2_question() -> list[str]:
    return L(
        "narrateur|Le pommier ouvre trois chemins.",
        "narrateur|Sous les branches, l'ombre est basse.",
        "narrateur|Dans l'herbe, ça sent le jus.",
        "narrateur|Sur le banc, la pomme rouge attend.",
        "papa|Où allez-vous, sous le pommier ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|L'anse du panier frotte une feuille.",
            2: "narrateur|La nappe accroche une brindille.",
            3: "narrateur|Le tabouret bute contre une racine.",
        }[t1]
        return L(
            lead,
            "narrateur|Les branches basses font un tunnel vert.",
            "enfant-f|J'y vais.",
            "narrateur|Mila penche la tête, trop haute.",
            "enfant-f|Ça me touche le front.",
            "enfant-m|Moi, je passe.",
            "narrateur|Nino glisse sous les feuilles, tout petit.",
            "papa|Tes épaules passent, Nino.",
            "narrateur|Une pomme rouge est coincée dans les brindilles.",
            "enfant-f|Elle est là, trop mêlée.",
            "maman|Vous la prenez comment, tous les deux ?",
        )
    if t2 == 2:
        lead = {
            1: f"narrateur|{o['cap']} penche, trop vite, dans l'herbe.",
            2: f"narrateur|{o['cap']} s'ouvre, un coin, dans l'herbe.",
            3: f"narrateur|{o['cap']} s'enfonce un peu, dans l'herbe.",
        }[t1]
        return L(
            lead,
            "narrateur|L'herbe haute sent le jus, tout fort.",
            "enfant-m|Elle me monte trop.",
            "narrateur|L'herbe arrive à la poitrine de Nino.",
            "narrateur|Mila voit par-dessus, tout clair.",
            "enfant-f|Je vois une pomme rouge.",
            "enfant-m|Moi, je vois que l'herbe.",
            "papa|Tes yeux sont plus hauts, Mila.",
            "maman|Les mains de Nino sont plus près du sol.",
            "enfant-f|On la trouve comment ?",
        )
    lead = {
        1: f"narrateur|{o['cap']} pose un toc contre le banc.",
        2: f"narrateur|{o['cap']} glisse sur le bois du banc.",
        3: f"narrateur|{o['cap']} cogne le pied du banc.",
    }[t1]
    return L(
        lead,
        "narrateur|Le banc du pommier est chaud, tout sec.",
        "enfant-f|Je monte, pour la pomme du haut.",
        "narrateur|Mila se hausse, les talons levés.",
        "narrateur|Ses doigts frôlent la peau, pas plus.",
        "enfant-m|Mes bras sont trop courts.",
        "papa|Le banc n'est pas assez haut, tout seul.",
        "maman|Nino, tu restes en bas.",
        "enfant-f|Elle brille, juste au-dessus.",
        "papa|Vous faites comment, tous les deux ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|La pomme reste coincée dans les feuilles.",
            "papa|Le passage de Nino, la branche, ou la chute ?",
        )
    if t2 == 2:
        return L(
            "narrateur|La pomme se cache dans l'herbe.",
            "maman|Les mains de Nino, les yeux de Mila, ou l'herbe ?",
        )
    return L(
        "narrateur|La pomme du haut reste trop loin.",
        "papa|Les doigts, le geste d'en bas, ou le banc à deux ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        use = {
            1: "narrateur|Nino pousse le panier sous les feuilles.",
            2: "narrateur|Nino tend la nappe sous les brindilles.",
            3: "narrateur|Nino glisse le tabouret sous le tunnel.",
        }[t1]
        return L(
            "enfant-m|Je passe, Mila.",
            "narrateur|Nino rampe, tout petit, sous le vert.",
            "enfant-f|Doucement.",
            use,
            "narrateur|Ses doigts dénouent la pomme, tout lent.",
            "enfant-m|Je la tiens !",
            "papa|Tes épaules étaient assez petites.",
            "narrateur|La pomme rouge roule à leur hauteur.",
            "enfant-f|Regarde, Nino.",
            "enfant-m|Elle est à nous.",
        )
    if t2 == 1 and t3 == 2:
        wait = {
            1: "narrateur|Le panier attend en bas, plein d'ombre.",
            2: "narrateur|La nappe attend en bas, un peu verte.",
            3: "narrateur|Le tabouret attend en bas, un peu humide.",
        }[t1]
        return L(
            "enfant-f|Je soulève la branche.",
            "papa|Je te tiens, Mila.",
            "narrateur|Mila lève le bois, plus haute que Nino.",
            "enfant-m|Je vois la pomme !",
            "narrateur|Nino tend les deux mains.",
            "narrateur|La pomme glisse vers lui.",
            "enfant-f|Elle est à toi, un moment.",
            "maman|Vous la partagez.",
            wait,
        )
    if t2 == 1 and t3 == 3:
        catch = {
            1: "narrateur|Le panier cueille la pomme, toc.",
            2: "narrateur|La nappe cueille la pomme, tout mou.",
            3: "narrateur|Le tabouret cueille la pomme, tout rêche.",
        }[t1]
        return L(
            "enfant-f|On attend un peu.",
            "enfant-m|Moi aussi, j'attends.",
            "narrateur|Un souffle passe dans les feuilles.",
            "narrateur|La pomme se décroche, toute seule.",
            catch,
            "papa|Elle est venue vers vous.",
            "enfant-m|On l'a reprise.",
            "enfant-f|Elle brille encore.",
            "maman|Vos cheveux sentent la feuille.",
        )
    if t2 == 2 and t3 == 1:
        carry = {
            1: "narrateur|Nino pose la pomme dans le panier.",
            2: "narrateur|Nino enveloppe la pomme dans la nappe.",
            3: "narrateur|Nino pose la pomme sur le tabouret.",
        }[t1]
        return L(
            "enfant-m|Je ramasse, tout près du sol.",
            "enfant-f|Je te guide, d'en haut.",
            "narrateur|Nino écarte deux brins, tout doux.",
            "narrateur|La pomme rouge est là, collée.",
            "enfant-m|Je la tiens !",
            carry,
            "papa|Tes mains étaient à la bonne hauteur.",
            "enfant-f|Passe-la, un peu.",
            "enfant-m|Elle est encore froide.",
        )
    if t2 == 2 and t3 == 2:
        reach = {
            1: "narrateur|Mila tend le panier, bras tout longs.",
            2: "narrateur|Mila tend la nappe, bras tout longs.",
            3: "narrateur|Mila pousse le tabouret, bras tout longs.",
        }[t1]
        return L(
            "enfant-f|Je reste ici, plus haut.",
            "enfant-m|Je vais où tu dis.",
            reach,
            "narrateur|Mila voit le rond rouge, par-dessus.",
            "narrateur|Nino avance vers le point d'ombre.",
            "enfant-m|Je la tiens !",
            "maman|Tes yeux ont trouvé le chemin.",
            "enfant-f|Elle sent l'herbe.",
            "papa|Soufflez dessus, tout léger.",
        )
    if t2 == 2 and t3 == 3:
        nest = {
            1: "narrateur|Le panier devient un nid, dans l'herbe.",
            2: "narrateur|La nappe devient un nid, dans l'herbe.",
            3: "narrateur|Le tabouret devient un nid, dans l'herbe.",
        }[t1]
        return L(
            "enfant-f|Papa, écarte un peu ?",
            "papa|Je fais un chemin, tout doux.",
            "narrateur|L'herbe s'ouvre, comme une porte.",
            "narrateur|La pomme rouge apparaît, collée.",
            nest,
            "enfant-m|On la prend ensemble.",
            "enfant-f|Oui.",
            "maman|Vous y arrivez, tous les deux.",
            "narrateur|Deux paires de mains tiennent le fruit.",
        )
    if t2 == 3 and t3 == 1:
        hold = {
            1: "narrateur|Nino garde le panier au pied du banc.",
            2: "narrateur|Nino garde la nappe au pied du banc.",
            3: "narrateur|Nino garde le tabouret au pied du banc.",
        }[t1]
        return L(
            "enfant-f|Je me hausse encore.",
            hold,
            "narrateur|Les doigts de Mila touchent la peau.",
            "enfant-f|Elle bouge !",
            "narrateur|La pomme penche, puis se détache.",
            "enfant-m|Je la rattrape.",
            "papa|Tes doigts allaient assez loin.",
            "maman|Nino tenait bien le bas.",
            "enfant-f|Elle est à nous.",
        )
    if t2 == 3 and t3 == 2:
        up = {
            1: "narrateur|Nino tend le panier, bras tout courts.",
            2: "narrateur|Nino tend la nappe, bras tout courts.",
            3: "narrateur|Nino pousse le tabouret, tout près.",
        }[t1]
        return L(
            "enfant-f|Reste en bas, Nino.",
            "enfant-m|Je tends, d'ici.",
            up,
            "narrateur|Mila fait basculer la pomme, tout doux.",
            "narrateur|Le fruit tombe dans les mains d'en bas.",
            "enfant-m|Je la tiens !",
            "papa|Chacun a fait sa part.",
            "enfant-f|Elle sent le soleil.",
            "maman|Vos bras n'avaient pas la même longueur.",
        )
    # t2 == 3 and t3 == 3
    two = {
        1: "narrateur|Papa pose le panier sur le banc, entre eux.",
        2: "narrateur|Papa pose la nappe sur le banc, entre eux.",
        3: "narrateur|Papa pose le tabouret sur le banc, entre eux.",
    }[t1]
    return L(
        "enfant-f|On monte à deux ?",
        "enfant-m|Oui, tout doux.",
        two,
        "narrateur|Papa tient le bois, tout ferme.",
        "narrateur|Mila et Nino tendent ensemble.",
        "enfant-f|Elle vient !",
        "enfant-m|Je la sens.",
        "maman|Vous avez tiré ensemble.",
        "papa|Le banc est resté à sa place.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    coda = {
        1: "narrateur|Le panier sèche près des sandales.",
        2: "narrateur|La nappe sèche près des sandales.",
        3: "narrateur|Le tabouret sèche près des sandales.",
    }[t1]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Ils rentrent, la pomme au creux.",
            "enfant-m|Elle sent encore la feuille.",
            "enfant-f|Tes épaules l'ont fait descendre.",
            "papa|Vous l'avez prise, enfin.",
            "maman|Posez-la sur la table, au jus.",
            "narrateur|Le tronc garde une ombre, tout petit.",
            coda,
            "narrateur|Un bourdon passe, plus loin.",
            "narrateur|Le rouge dort contre le bois.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Sous la branche, la maison paraît petite.",
            "enfant-f|Nino, tu l'as vue glisser.",
            "enfant-m|Oui, tout près de mes mains.",
            "papa|Je t'ai tenue, pas trop longtemps.",
            "maman|Vos têtes, haute et basse, rentrent.",
            "narrateur|La pomme reste dans la paume de Nino.",
            coda,
            "narrateur|Une feuille reste collée aux cheveux.",
            "narrateur|La table sent déjà le sucre.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Le souffle du pommier les suit jusqu'à la porte.",
            "enfant-m|Elle est tombée vers nous.",
            "enfant-f|On a attendu, tous les deux.",
            "maman|Elle n'était plus trop mêlée.",
            "papa|Le jus perle encore, sur la peau.",
            f"narrateur|{o['cap']} pose une feuille, tout léger.",
            "narrateur|La porte claque, tout doux.",
            "narrateur|Une odeur de pomme reste dans l'entrée.",
            "narrateur|Le rouge veille près des souliers.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Ils rentrent avec de l'herbe aux genoux.",
            "enfant-m|Mes mains savaient le chemin.",
            "enfant-f|Moi, je voyais trop haut.",
            "papa|Vous avez suivi ce qui était à vous.",
            "maman|Soufflez le dernier brin, dehors.",
            "enfant-f|Elle est pour le goûter, maintenant.",
            "enfant-m|Elle est un peu froide encore.",
            coda,
            "narrateur|L'herbe sèche déjà sur le palier.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Ils n'ont pas couru dans tout le pré.",
            "enfant-f|Je l'ai vue par-dessus.",
            "enfant-m|Tes yeux étaient assez hauts.",
            "maman|L'herbe sent fort, sur vos mains.",
            "papa|Lavez-les, tout doux, au bac.",
            f"narrateur|{o['cap']} garde un brin d'herbe.",
            "enfant-m|Je la tiens, Mila.",
            "narrateur|Le bac goutte, puis se tait.",
            "narrateur|La pomme sèche près de la fenêtre.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Leurs chaussettes portent encore de l'herbe.",
            "enfant-f|Papa a ouvert un chemin.",
            "enfant-m|On l'a prise ensemble.",
            "papa|L'herbe vous a laissé la place.",
            "maman|Changez le linge des pieds, d'abord.",
            coda,
            "narrateur|Une goutte de jus marque le carreau.",
            "enfant-f|Regarde-la, Nino, elle brille.",
            "narrateur|Le rouge reste au chaud, sur la table.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Les talons de Mila sont encore chauds.",
            "enfant-m|Tu l'as fait pencher pour moi.",
            "enfant-f|Tu tenais le bas.",
            "maman|Essuie tes pieds, sur le paillasson.",
            "papa|La pomme du haut est à vous, maintenant.",
            "narrateur|Nino la pose contre la vitre.",
            coda,
            "narrateur|Un rai de soleil traverse le rouge.",
            "narrateur|Dehors, le banc redevient calme.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Un peu de soleil les suit jusqu'à la porte.",
            "enfant-f|Tu l'as reçue, d'en bas.",
            "enfant-m|Tes doigts l'ont fait tomber.",
            "papa|Chacun a fait sa part, à sa hauteur.",
            "maman|Le bois du banc sèche déjà.",
            f"narrateur|{o['cap']} pose une auréole au carrelage.",
            "enfant-m|Elle brille trop, Mila.",
            "enfant-f|C'est pour ça.",
            "narrateur|La vitre garde le rouge, tout proche.",
        )
    return L(
        "narrateur|Un peu de poussière de banc reste au seuil.",
        "enfant-f|On a tiré ensemble.",
        "enfant-m|Sans trop monter.",
        "papa|Le banc est resté à sa place.",
        "maman|Vos mains sentent encore le sucre.",
        coda,
        "narrateur|Mila pose la pomme au rebord.",
        "enfant-m|Tu l'as eue, enfin.",
        "narrateur|Le jus brille un peu, puis s'endort.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": "oiseau"}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Une pomme sent le sucre, encore tiède.",
        "narrateur|Un bourdon dessine un fil d'or, tout bas.",
        "narrateur|L'écorce du pommier est rêche, un peu chaude.",
        "narrateur|Une feuille jaune reste collée au tronc.",
        "narrateur|Le jardin sent le jus, près de la table.",
        "papa|Tu as vu la goutte, Mila ?",
        "enfant-f|Elle est collante.",
        "maman|La nappe a pris une tache ronde.",
        "narrateur|En ce moment, Mila lève le nez.",
        "narrateur|Une pomme rouge pend trop haut.",
        "enfant-f|Je la veux, pour le panier.",
        "papa|Nino arrive, plus petit que toi.",
        "narrateur|Nino a de l'herbe jusqu'aux genoux.",
        "enfant-m|On la prend ensemble ?",
        "maman|On prépare d'abord, alors ?",
        "papa|Merci, tu regardes bien la pomme.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent sous l'arbre.",
        "narrateur|Le panier, la nappe, et le tabouret.",
        "maman|Tu prends quoi d'abord, Mila ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le panier", "la nappe", "le tabouret")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Mila a glissé la petite pomme {o['t1q']}.",
            "maman|Elle est où, la petite pomme ?",
        )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question()
        extras[f"{p}_T0002_P0000"] = t3lab("les branches basses", "l'herbe haute", "le banc")

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
        "Le panier de Mila et la pomme du haut",
        "Sous le pommier, Mila veut la pomme rouge trop haute pour son panier, "
        "pour le goûter. Nino est plus petit. T1 = panier / nappe / tabouret "
        "(les trois partent). T2 = branches basses trop basses pour Mila / "
        "herbe trop haute pour Nino / banc trop bas pour la pomme du haut. "
        "T3 = neuf résolutions (passage de Nino, branche levée, pomme qui tombe ; "
        "mains de Nino, yeux de Mila, herbe écartée ; bout des doigts, geste "
        "d'en bas, banc à deux). La leçon (tailles, jouer ensemble) se vit "
        "dans les gestes, sans slogan. Fin : la pomme rentre à la maison.",
        "N2 ≤ 15. Lila / Tom / Léa / Sami et bac/toboggan/balançoires jetés. "
        "Titre leçon collée remplacé (objet + désir). Un merci de papa lié "
        "au geste (regarder la pomme). Audio non cuit.",
    )


if __name__ == "__main__":
    main()
