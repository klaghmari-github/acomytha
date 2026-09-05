#!/usr/bin/env python3
"""TREE-DIF-001 — Le coquillage d'Aniss pour Sarah (N1, F-NAR-018)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-001"
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
        "Aniss veut montrer son coquillage à Sarah, au bord de la mer. "
        "Ils préparent le seau, le filet et le linge. "
        "Un roc trop haut, une laisse trop loin ou une mare trop profonde "
        "arrête le jeu. Ils trouvent ensemble, et Sarah tient la coquille."
    )
    out["title"] = "Le coquillage d'Aniss pour Sarah"
    out["characters"] = "Aniss, Sarah, papa, maman"
    out["setting"] = "maison près de la mer, sable mouillé"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "tailles sont différentes",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
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
        "lab": "le seau",
        "le": "le seau",
        "cap": "Le seau",
        "t1q": "dans le seau",
        "t1acc": "seau | le seau | dans le seau | au fond du seau",
        "t1retry": "Le coquillage est dans le seau.",
    },
    2: {
        "lab": "le filet",
        "le": "le filet",
        "cap": "Le filet",
        "t1q": "dans le filet",
        "t1acc": "filet | le filet | dans le filet | au fond du filet",
        "t1retry": "Le coquillage est dans le filet.",
    },
    3: {
        "lab": "le linge",
        "le": "le linge",
        "cap": "Le linge",
        "t1q": "dans le linge",
        "t1acc": "linge | le linge | dans le linge | le linge rayé",
        "t1retry": "Le coquillage est dans le linge.",
    },
}

LIEU = {
    1: {"lab": "les rochers", "ou": "vers les rochers"},
    2: {"lab": "la laisse", "ou": "vers la laisse"},
    3: {"lab": "la mare", "ou": "vers la mare"},
}

T3_LABS = {
    1: ("la main de Sarah", "les bras de papa", "un nid plus bas"),
    2: ("les petites traces", "le geste de loin", "la petite vague"),
    3: ("les chevilles", "l'eau qui recule", "tendre ensemble"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Aniss tire le seau par l'anse.",
            "enfant-m|Le coquillage ira dedans.",
            "maman|Glisse-le, tout doux.",
            "narrateur|La coquille tape un petit toc.",
            "papa|Le filet aussi, dans le sac.",
            "narrateur|Maman plie le linge rayé.",
            "narrateur|Les trois affaires partent ensemble.",
            "enfant-m|Sarah va voir ma coquille.",
            "narrateur|Un pas léger sonne sur le palier.",
            "enfant-f|Aniss, je suis là.",
            "enfant-m|Viens, on va à la mer.",
            "papa|Le seau d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Aniss ouvre le filet, tout large.",
            "enfant-m|La coquille va ici.",
            "papa|Doucement, les mailles sont fines.",
            "narrateur|Le rose brille entre les fils.",
            "maman|Le seau, ensuite, près du sac.",
            "narrateur|Elle glisse le linge par-dessus.",
            "narrateur|Les trois affaires partent ensemble.",
            "enfant-m|Sarah va tout voir.",
            "narrateur|La porte claque, tout léger.",
            "enfant-f|Me voilà, Aniss.",
            "enfant-m|On court vers l'eau ?",
            "maman|Le filet d'abord, il est prêt.",
        )
    return L(
        "narrateur|Aniss prend le linge encore tiède.",
        "enfant-m|Je cache la coquille.",
        "maman|Enroule-la, comme un secret.",
        "narrateur|Le tissu sent le soleil.",
        "papa|Le seau et le filet, avec vous.",
        "narrateur|Il les pose près des sandales.",
        "narrateur|Les trois affaires partent ensemble.",
        "enfant-m|Sarah, vite !",
        "narrateur|Des pas frais sonnent dehors.",
        "enfant-f|J'arrive, Aniss.",
        "enfant-m|Je te montre ma coquille.",
        "papa|Le linge d'abord, il est chaud.",
    )


def t1_confirm(t1: int) -> list[str]:
    o = OBJ[t1]
    if t1 == 1:
        return L(
            f"narrateur|{o['cap']} porte la coquille, tout au fond.",
            "enfant-f|Elle fait toc, encore.",
            "enfant-m|C'est pour toi, Sarah.",
            "maman|Le sable vous attend.",
            "papa|On sort par le petit chemin ?",
            "enfant-m|Oui, papa.",
        )
    if t1 == 2:
        return L(
            f"narrateur|{o['cap']} tient la coquille entre les mailles.",
            "enfant-f|Je vois le rose !",
            "enfant-m|Ne touche pas encore.",
            "papa|Le vent sent déjà le sel.",
            "maman|Vos pieds, dans les sandales ?",
            "enfant-f|Oui, maman.",
        )
    return L(
        f"narrateur|{o['cap']} rayé cache encore la coquille.",
        "enfant-f|Ça sent le chaud.",
        "enfant-m|Elle est là, au milieu.",
        "maman|La mer est calme, devant.",
        "papa|On y va, tous les quatre ?",
        "enfant-m|Oui.",
    )


def t2_question() -> list[str]:
    return L(
        "narrateur|Le sable mouillé brille encore.",
        "narrateur|Des rochers fumants attendent à gauche.",
        "narrateur|Au milieu, une ligne d'algues.",
        "narrateur|À droite, une mare ronde tremble.",
        "papa|Où montrez-vous la coquille ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|L'anse du seau tape sur le sable.",
            2: "narrateur|Le filet sent déjà le sel.",
            3: "narrateur|Le linge rayé frotte son poignet.",
        }[t1]
        return L(
            lead,
            "narrateur|Les rochers fumants sentent l'algue.",
            "enfant-m|Je la pose tout en haut.",
            "enfant-f|Je veux la voir briller.",
            "narrateur|Aniss se hausse, tout doux.",
            "narrateur|La fente est trop haute.",
            "enfant-m|Ma main n'y arrive pas.",
            "papa|Tes pieds sont plus petits.",
            "narrateur|Deux traces collent au pied du roc.",
            "narrateur|Les grandes, et les petites.",
            "enfant-f|On la montre ensemble ?",
            "maman|Vous trouvez comment, tous les deux ?",
        )
    if t2 == 2:
        lead = {
            1: f"narrateur|{o['cap']} penche, trop vite.",
            2: f"narrateur|{o['cap']} s'ouvre, un peu trop.",
            3: f"narrateur|{o['cap']} se défait, un coin.",
        }[t1]
        return L(
            lead,
            "narrateur|La coquille glisse vers les algues.",
            "enfant-m|Elle part trop loin !",
            "enfant-f|Je la vois, entre les bulles.",
            "narrateur|Une ligne d'écume barre le sable.",
            "narrateur|Des traces s'y croisent, pas pareilles.",
            "papa|Les grandes, ce sont les miennes.",
            "maman|Les petites, ce sont les vôtres.",
            "enfant-m|J'ai les jambes trop courtes.",
            "enfant-f|Moi aussi, presque.",
            "papa|Vous la reprenez comment ?",
        )
    lead = {
        1: f"narrateur|{o['cap']} tapote l'eau, tout léger.",
        2: f"narrateur|{o['cap']} frôle la mare, tout doux.",
        3: f"narrateur|{o['cap']} reste au bord, un peu sec.",
    }[t1]
    return L(
        lead,
        "enfant-m|On rince la coquille, Sarah.",
        "enfant-f|Pour qu'elle brille vraiment.",
        "narrateur|La mare ronde tremble, trop profonde.",
        "narrateur|Aniss pose un pied, puis recule.",
        "enfant-m|L'eau me monte trop vite.",
        "papa|Mes traces vont plus loin, là-bas.",
        "maman|Les vôtres s'arrêtent au bord.",
        "enfant-f|On rince ensemble, alors ?",
        "papa|Vous faites comment, tous les deux ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Le roc reste trop haut.",
            "papa|La main de Sarah, mes bras, ou un nid ?",
        )
    if t2 == 2:
        return L(
            "narrateur|La coquille a roulé trop loin.",
            "maman|Les traces, le geste de loin, ou la vague ?",
        )
    return L(
        "narrateur|L'eau de la mare est profonde.",
        "papa|Les chevilles, l'eau qui recule, ou tendre ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        use = {
            1: "narrateur|Aniss pousse le seau contre le roc.",
            2: "narrateur|Aniss tend le filet vers la fente.",
            3: "narrateur|Aniss appuie le linge contre le roc.",
        }[t1]
        return L(
            "enfant-f|Ma main passe à côté.",
            "narrateur|Sarah glisse les doigts dans la fente.",
            "enfant-m|Doucement.",
            use,
            "narrateur|La coquille avance, tout petit.",
            "enfant-f|Je la touche !",
            "papa|Vous y arrivez ensemble.",
            "narrateur|Le rose brille, à leur hauteur.",
            "enfant-m|Regarde, Sarah.",
            "enfant-f|Elle est à nous.",
        )
    if t2 == 1 and t3 == 2:
        wait = {
            1: "narrateur|Le seau attend en bas, plein de sable.",
            2: "narrateur|Le filet attend en bas, un peu salé.",
            3: "narrateur|Le linge attend en bas, un peu mouillé.",
        }[t1]
        return L(
            "enfant-m|Papa, un peu plus haut.",
            "papa|Je te tiens, Aniss.",
            "narrateur|Aniss pose la coquille sur le roc.",
            "enfant-f|Je la vois, tout près.",
            "narrateur|Sarah tend les deux mains.",
            "narrateur|La coquille glisse vers elle.",
            "enfant-m|Elle est à toi, un moment.",
            "maman|Vous la partagez.",
            wait,
        )
    if t2 == 1 and t3 == 3:
        guard = {
            1: "narrateur|Le seau garde le pied du nid.",
            2: "narrateur|Le filet ombre le pied du nid.",
            3: "narrateur|Le linge borde le pied du nid.",
        }[t1]
        return L(
            "enfant-m|On fait un nid ici.",
            "enfant-f|Avec les petits cailloux.",
            "narrateur|Ils empilent, caillou après caillou.",
            "narrateur|Le nid arrive sous leur menton.",
            "narrateur|Aniss pose la coquille au centre.",
            "enfant-f|Elle n'est plus trop haut.",
            "papa|Votre trône est à votre taille.",
            guard,
        )
    if t2 == 2 and t3 == 1:
        carry = {
            1: "narrateur|Aniss pose la coquille dans le seau.",
            2: "narrateur|Aniss rattrape la coquille au filet.",
            3: "narrateur|Aniss l'enveloppe dans le linge.",
        }[t1]
        return L(
            "enfant-m|On suit les petites traces.",
            "enfant-f|Celles du crabe, tout étroites.",
            "narrateur|Ils marchent dans leurs propres pas.",
            "narrateur|Une bulle d'écume cache le rose.",
            "enfant-f|Là !",
            carry,
            "papa|Vos pieds allaient assez loin.",
            "enfant-m|On l'a, Sarah.",
            "enfant-f|Elle est encore froide.",
        )
    if t2 == 2 and t3 == 2:
        reach = {
            1: "narrateur|Sarah tend le seau, bras tout longs.",
            2: "narrateur|Sarah tend le filet, bras tout longs.",
            3: "narrateur|Sarah tend le linge, bras tout longs.",
        }[t1]
        return L(
            "enfant-f|On reste ici.",
            "enfant-m|On attrape de loin.",
            reach,
            "narrateur|Aniss guide le bord, tout doux.",
            "narrateur|La coquille rentre, un peu sableuse.",
            "enfant-m|Je la tiens !",
            "maman|Vous n'avez pas couru trop loin.",
            "enfant-f|Elle sent les algues.",
            "papa|Soufflez dessus, tout léger.",
        )
    if t2 == 2 and t3 == 3:
        catch = {
            1: "narrateur|Le seau cueille la coquille, toc.",
            2: "narrateur|Le filet cueille la coquille, chuint.",
            3: "narrateur|Le linge cueille la coquille, tout mouillé.",
        }[t1]
        return L(
            "enfant-m|On attend la petite vague.",
            "enfant-f|Moi aussi, j'attends.",
            "narrateur|L'eau avance, puis recule.",
            "narrateur|La coquille revient, tout près.",
            catch,
            "papa|Elle est venue vers vous.",
            "enfant-f|On l'a reprise.",
            "enfant-m|Regarde, elle brille encore.",
            "maman|Vos poches sont un peu mouillées.",
        )
    if t2 == 3 and t3 == 1:
        hold = {
            1: "narrateur|Sarah garde le seau au bord.",
            2: "narrateur|Sarah garde le filet au bord.",
            3: "narrateur|Sarah garde le linge au bord.",
        }[t1]
        return L(
            "enfant-m|J'entre jusqu'aux chevilles.",
            hold,
            "narrateur|L'eau froide lui pince la peau.",
            "enfant-m|Passe-moi la coquille.",
            "enfant-f|La voilà.",
            "narrateur|Aniss la plonge, un tout petit peu.",
            "narrateur|Le rose devient net, tout de suite.",
            "enfant-f|Elle brille pour de vrai.",
            "papa|Tu es rentré juste assez.",
            "maman|Sarah tenait bien le bord.",
        )
    if t2 == 3 and t3 == 2:
        dry = {
            1: "narrateur|Ils posent le seau sur le sable sec.",
            2: "narrateur|Ils posent le filet sur le sable sec.",
            3: "narrateur|Ils posent le linge sur le sable sec.",
        }[t1]
        return L(
            "enfant-f|On attend que l'eau recule.",
            "enfant-m|Oui, un peu.",
            "narrateur|La mare se fait plus petite.",
            "narrateur|Un anneau mouillé reste au bord.",
            "enfant-m|Maintenant, on peut.",
            "narrateur|Ils trempent la coquille, tous les deux.",
            "enfant-f|Elle est propre.",
            dry,
            "papa|L'eau vous a laissé la place.",
        )
    # t2 == 3 and t3 == 3
    pull = {
        1: "narrateur|Papa tend le seau, plein d'eau.",
        2: "narrateur|Papa tend le filet, plein d'eau.",
        3: "narrateur|Papa tend le linge, tout trempé.",
    }[t1]
    return L(
        "enfant-m|On rince ici, sur le sable.",
        "enfant-f|Sans entrer trop.",
        pull,
        "narrateur|Aniss et Sarah tiennent le bord.",
        "narrateur|L'eau coule sur la coquille rose.",
        "enfant-m|Elle brille, Sarah.",
        "enfant-f|Je la vois trop bien.",
        "maman|Vous avez tiré ensemble.",
        "papa|La mare reste à sa place.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    coda = {
        1: "narrateur|Le seau sèche près des sandales.",
        2: "narrateur|Le filet sèche près des sandales.",
        3: "narrateur|Le linge sèche près des sandales.",
    }[t1]
    # 9 aventures : le souvenir change avec T2×T3 ; T1 colore la coda.
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Ils rentrent, la coquille au creux.",
            "enfant-f|Elle sent encore le roc.",
            "enfant-m|Ta main l'a fait descendre.",
            "papa|Vous l'avez montrée, enfin.",
            "maman|Posez-la sur le rebord, au sel.",
            "narrateur|Le volet garde une goutte, tout petit.",
            coda,
            "narrateur|Une mouette crie, plus loin.",
            "narrateur|Le rose dort contre le bois.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Du haut du roc, la maison était petite.",
            "enfant-m|Sarah, tu l'as vue briller.",
            "enfant-f|Oui, tout près de mes yeux.",
            "papa|Je vous ai tenus, pas trop longtemps.",
            "maman|Vos traces grandes et petites rentrent.",
            "narrateur|La coquille reste dans la paume de Sarah.",
            coda,
            "narrateur|Le sel colle encore aux cheveux.",
            "narrateur|La table sent le linge chaud.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Le nid de cailloux voyage jusqu'à la porte.",
            "enfant-f|Notre trône rentre à la maison.",
            "enfant-m|La coquille n'a plus trop haut.",
            "maman|Elle dort à votre hauteur, maintenant.",
            "papa|Les petits cailloux restent au paillasson.",
            f"narrateur|{o['cap']} pose un grain de sable.",
            "narrateur|Le volet claque, tout doux.",
            "narrateur|Une odeur d'algue reste dans l'entrée.",
            "narrateur|Le rose veille près des souliers.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Ils rentrent avec du sable aux genoux.",
            "enfant-m|Les petites traces savaient le chemin.",
            "enfant-f|Le crabe aussi, peut-être.",
            "papa|Vous avez suivi ce qui était à vous.",
            "maman|Soufflez la dernière bulle, dehors.",
            "enfant-m|Elle est pour Sarah, maintenant.",
            "enfant-f|Elle est un peu froide encore.",
            coda,
            "narrateur|L'écume sèche déjà sur le palier.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Ils n'ont pas couru jusqu'à l'eau.",
            "enfant-f|On l'a attrapée de loin.",
            "enfant-m|Tes bras étaient assez longs.",
            "maman|L'algue sent fort, sur vos mains.",
            "papa|Lavez-les, tout doux, au bac.",
            f"narrateur|{o['cap']} garde une feuille d'algue.",
            "enfant-f|Je la tiens, Aniss.",
            "narrateur|Le bac goutte, puis se tait.",
            "narrateur|La coquille sèche près de la fenêtre.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Leurs poches gouttent encore, dans l'entrée.",
            "enfant-m|La vague nous l'a rendue.",
            "enfant-f|On a attendu, tous les deux.",
            "papa|Elle est venue vers vos mains.",
            "maman|Changez le linge des poches, d'abord.",
            coda,
            "narrateur|Une goutte salée marque le carreau.",
            "enfant-m|Regarde-la, Sarah, elle brille.",
            "narrateur|Le rose reste au chaud, sur la table.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Les chevilles d'Aniss sont encore froides.",
            "enfant-f|Tu l'as rincée pour moi.",
            "enfant-m|Tu tenais le bord.",
            "maman|Essuie tes pieds, sur le paillasson.",
            "papa|La coquille est nette, maintenant.",
            "narrateur|Sarah la pose contre la vitre.",
            coda,
            "narrateur|Un rai de soleil traverse le rose.",
            "narrateur|Dehors, la mare redevient calme.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Un anneau mouillé les suit jusqu'à la porte.",
            "enfant-m|L'eau a reculé pour nous.",
            "enfant-f|On a rincé ensemble, après.",
            "papa|La mer vous a laissé le temps.",
            "maman|Le sable sèche déjà sur vos mollets.",
            f"narrateur|{o['cap']} pose une auréole au carrelage.",
            "enfant-f|Elle brille trop, Aniss.",
            "enfant-m|C'est pour ça.",
            "narrateur|La vitre garde le rose, tout proche.",
        )
    return L(
        "narrateur|Un peu d'eau de mare reste au seuil.",
        "enfant-m|On a tiré ensemble.",
        "enfant-f|Sans trop entrer.",
        "papa|La mare est restée à sa place.",
        "maman|Vos mains sentent encore le sel.",
        coda,
        "narrateur|Sarah pose la coquille au rebord.",
        "enfant-m|Tu l'as vue, enfin.",
        "narrateur|Le sel brille un peu, puis s'endort.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Le volet sent encore le sel.",
        "narrateur|Une mouette crie, tout près du toit.",
        "narrateur|La maison est petite, face à l'eau.",
        "narrateur|Des grains collent au rebord.",
        "narrateur|Papa range les sandales près de la porte.",
        "narrateur|Ça sent le linge chaud, dans la cuisine.",
        "maman|La mer est calme, ce matin.",
        "papa|Sarah arrive bientôt, Aniss.",
        "narrateur|En ce moment, Aniss ouvre la paume.",
        "enfant-m|Mon coquillage est là !",
        "narrateur|La coquille rose tient toute seule.",
        "enfant-m|Je veux le lui montrer.",
        "enfant-m|Au bord de l'eau.",
        "maman|On prépare le sac, alors ?",
        "papa|Merci, tu le tiens tout doux.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Le sac attend près des sandales.",
        "narrateur|Le seau, le filet, et le linge.",
        "maman|Tu prends quoi d'abord, Aniss ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le seau", "le filet", "le linge")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Aniss a glissé le coquillage {o['t1q']}.",
            "maman|Il est où, le coquillage ?",
        )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question()
        extras[f"{p}_T0002_P0000"] = t3lab("les rochers", "la laisse", "la mare")

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
        "Le coquillage d'Aniss pour Sarah",
        "Aniss veut montrer sa coquille à Sarah. T1 = seau / filet / linge "
        "(les trois partent). T2 = rochers trop hauts / laisse trop loin / "
        "mare trop profonde. T3 = neuf résolutions (main de Sarah, bras de papa, "
        "nid bas ; petites traces, geste de loin, vague ; chevilles, eau qui "
        "recule, tendre). La leçon (tailles, jouer ensemble) se vit dans les "
        "traces et les gestes, sans slogan. Fin : Sarah tient le rose.",
        "N1 ≤ 10. Tom/Léa/Sami et cuisine/jardin/chambre jetés. "
        "Un merci de papa lié au geste (tenir la coquille). Audio non cuit.",
    )


if __name__ == "__main__":
    main()
