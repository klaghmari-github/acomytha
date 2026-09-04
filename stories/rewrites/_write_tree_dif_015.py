#!/usr/bin/env python3
"""TREE-DIF-015 — Le drap du salon et les deux peluches. DIF.COR.002, N3."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

N3 = LIMITS["N3"]
SID = "TREE-DIF-015"
TITLE = "Le drap du salon et les deux peluches"
FIL = (
    "Nino veut une tente dans le salon pour y coucher deux peluches. "
    "L'ours est tout rond, le lapin tout mince. "
    "Il prépare d'abord le drap, la pince ou la lampe ; les trois partent. "
    "Sous la table, derrière le canapé ou dans le couloir, chaque lieu a son obstacle. "
    "Les deux peluches restent ensemble."
)


def L(*rows: str) -> list[str]:
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N3:
            raise SystemExit(f"{n}>{N3}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"sans fin: {ph}")
    return list(rows)


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {"expected_answer": ans, "accepted_examples": acc, "retry_prompt": retry}


def pre(t1: int) -> str:
    return f"CHK_T0001_P000{t1}"


PREP = {
    1: dict(
        label="le drap",
        coda="Un pli du drap reste tiède, contre l'ours.",
        touch="Le drap sent le linge, un peu rêche.",
        son="tissu",
    ),
    2: dict(
        label="la pince",
        coda="La pince repose près du pied de chaise.",
        touch="Le bois de la pince est lisse, un peu froid.",
        son="",
    ),
    3: dict(
        label="la lampe",
        coda="Le rond de la lampe reste sur le tapis.",
        touch="La lampe chauffe un peu la paume.",
        son="",
    ),
}


def t1_pass(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Nino prend d'abord le drap, encore plié.",
            "narrateur|Le tissu tombe, trop large, jusqu'au tapis.",
            "enfant-m|Il sent le linge.",
            "maman|Il est un peu froid, encore.",
            "narrateur|Il le jette par-dessus les deux peluches.",
            "narrateur|L'ours fait une colline, toute ronde.",
            "narrateur|Le lapin fait une ligne, une oreille dehors.",
            "enfant-m|Un drapeau, et une colline !",
            "papa|Deux formes, une tente.",
            "narrateur|La pince attend dans le panier.",
            "maman|La lampe aussi.",
            "enfant-m|On les prend.",
        )
    if t1 == 2:
        return L(
            "narrateur|Nino saisit d'abord la pince, dans le panier.",
            "narrateur|Le bois claque une fois, tout sec.",
            "enfant-m|Elle tient fort.",
            "papa|C'est pour le coin du drap.",
            "narrateur|Il l'essaie sur un pli, près de l'ours.",
            "narrateur|Le ventre rond soulève le tissu.",
            "narrateur|L'oreille du lapin reste dehors, toute mince.",
            "enfant-m|Elle pince le drap, pas l'oreille.",
            "maman|Tu as vu les deux formes.",
            "narrateur|Le drap attend sur la chaise.",
            "papa|La lampe aussi, pour plus tard.",
            "enfant-m|Je mets la pince dans la poche.",
        )
    return L(
        "narrateur|Nino allume d'abord la lampe, un clic.",
        "narrateur|Un rond jaune tombe sur le tapis rêche.",
        "enfant-m|Ça fait un camp, déjà.",
        "maman|Tu éclaires qui, d'abord ?",
        "narrateur|Le rond passe sur le ventre de l'ours.",
        "narrateur|Puis il glisse sur l'oreille du lapin.",
        "enfant-m|Ils ne se ressemblent pas.",
        "papa|On les emmène toutes les deux.",
        "narrateur|Le drap attend, plié, sur la chaise.",
        "maman|La pince aussi, dans le panier.",
        "enfant-m|Je garde la lampe.",
        "narrateur|Le rond tremble un peu, dans sa main.",
    )


def t1_q(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Le drap couvre déjà les deux peluches.",
            "maman|Nino a pris quoi, d'abord ?",
        )
    if t1 == 2:
        return L(
            "narrateur|Le bois de la pince a claqué.",
            "papa|Nino a pris quoi, dans le panier ?",
        )
    return L(
        "narrateur|Un rond jaune est tombé sur le tapis.",
        "maman|Nino a allumé quoi ?",
    )


def t1_c(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-m|Le drap.",
            "papa|Oui.",
            "narrateur|Nino glisse la pince dans sa poche.",
            "maman|La lampe, je te la tends.",
            "enfant-m|Merci.",
            "narrateur|Il prend l'ours d'un bras, le lapin de l'autre.",
            "papa|Les deux viennent.",
            "enfant-m|On cherche l'endroit.",
        )
    if t1 == 2:
        return L(
            "enfant-m|La pince.",
            "maman|Oui.",
            "narrateur|Il ramasse le drap, tout un nuage.",
            "papa|La lampe, dans l'autre main ?",
            "enfant-m|Oui, papa.",
            "narrateur|Les deux peluches voyagent contre lui.",
            "maman|Merci d'avoir pris les deux.",
            "enfant-m|On va où, maintenant ?",
        )
    return L(
        "enfant-m|La lampe.",
        "papa|Oui.",
        "narrateur|Maman lui passe le drap, déjà plié.",
        "maman|La pince, dans la poche.",
        "enfant-m|Elle est là.",
        "narrateur|L'ours et le lapin avancent avec lui.",
        "papa|Merci, Nino.",
        "enfant-m|Il me faut un endroit.",
    )


def t2_q(t1: int) -> list[str]:
    head = {
        1: "Le drap traîne un peu, derrière Nino.",
        2: "La pince tape sa poche, à chaque pas.",
        3: "Le rond de la lampe court sur le parquet.",
    }[t1]
    return L(
        f"narrateur|{head}",
        "narrateur|Les deux peluches attendent un camp.",
        "papa|Sous la table, derrière le canapé, ou le couloir ?",
    )


def t2_pass(t1: int, t2: int) -> list[str]:
    head = {
        1: "Un coin du drap frotte encore le parquet.",
        2: "La pince claque une fois, dans la poche.",
        3: "Le rond de la lampe tremble sur le bois.",
    }[t1]
    if t2 == 1:
        extra = {
            1: "Le drap accroche un pied de chaise, puis lâche.",
            2: "Nino pince un coin, trop tôt, trop bas.",
            3: "La lampe éclaire les barreaux, tout proches.",
        }[t1]
        return L(
            f"narrateur|{head}",
            "narrateur|Ils s'accroupissent sous la table.",
            f"narrateur|{extra}",
            "narrateur|L'ombre y fait déjà une grotte.",
            "enfant-m|Vous entrez.",
            "narrateur|L'ours bute contre un pied, trop rond.",
            "narrateur|Le lapin glisse de l'autre côté, trop mince.",
            "enfant-m|L'un reste, l'autre part.",
            "maman|Ils n'ont pas la même forme.",
            "papa|Tu fais quoi, avec les deux ?",
        )
    if t2 == 2:
        extra = {
            1: "Le drap s'accroche au pied de bois, et tire.",
            2: "La pince cogne le bois, un petit toc.",
            3: "La lampe montre un passage étroit, tout sombre.",
        }[t1]
        return L(
            f"narrateur|{head}",
            "narrateur|Derrière le canapé, ça sent le tissu.",
            f"narrateur|{extra}",
            "enfant-m|C'est un secret, ici.",
            "narrateur|Nino pousse l'ours vers la fente.",
            "narrateur|Le ventre rond ne passe pas.",
            "narrateur|Le lapin, lui, disparaît déjà.",
            "enfant-m|Ce n'est pas juste.",
            "papa|Le passage est étroit, voilà tout.",
            "maman|Tu les gardes comment, ensemble ?",
        )
    extra = {
        1: "Le drap se gonfle, comme une voile trop grande.",
        2: "Nino serre la pince, pour un coin qui vole.",
        3: "La lampe dessine deux ombres, l'une ronde.",
    }[t1]
    return L(
        f"narrateur|{head}",
        "narrateur|Dans le couloir, un courant d'air passe.",
        f"narrateur|{extra}",
        "enfant-m|La tente, ici.",
        "narrateur|Le drap se lève, tout seul.",
        "narrateur|Le lapin tombe, trop léger.",
        "narrateur|L'ours reste, tout lourd, tout rond.",
        "enfant-m|Il est tombé !",
        "maman|Le vent a choisi, pas toi.",
        "papa|Tu les rassembles comment ?",
    )


def t3_q(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Sous la table, l'ours bute, le lapin glisse.",
            "papa|Tu fais quoi, Nino ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Derrière le canapé, le passage est étroit.",
            "maman|Tu fais quoi, avec eux ?",
        )
    return L(
        "narrateur|Dans le couloir, le lapin est tombé.",
        "papa|Tu fais quoi, maintenant ?",
    )


def t3_pass(t1: int, t2: int, t3: int) -> list[str]:
    col = {
        1: "Un pli du drap sent encore le linge.",
        2: "La pince brille un peu, dans sa main.",
        3: "Le rond de la lampe reste entre eux.",
    }[t1]
    if t2 == 1 and t3 == 1:
        return L(
            "enfant-m|Une porte, dans le drap.",
            "narrateur|Nino soulève un pan, tout doux.",
            "narrateur|L'ours garde l'entrée, trop rond pour passer.",
            "narrateur|Le lapin entre, et s'assoit au fond.",
            "enfant-m|Tu surveilles, toi.",
            "papa|Deux places, deux formes.",
            f"narrateur|{col}",
            "maman|Ils sont ensemble, quand même.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "enfant-m|Plus petit, le drap.",
            "narrateur|Il le plie deux fois, contre le parquet.",
            "narrateur|La grotte devient étroite, plus basse.",
            "narrateur|L'ours s'assoit, le lapin se couche.",
            "enfant-m|Vous tenez, tous les deux.",
            "maman|Ils n'ont pas besoin d'être pareils.",
            f"narrateur|{col}",
            "papa|La table les couvre, maintenant.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "enfant-m|Sur la chaise, à côté.",
            "narrateur|Nino pose le drap sur le dossier.",
            "narrateur|L'ours et le lapin montent, l'un contre l'autre.",
            "enfant-m|Un camp, plus haut.",
            "papa|La grotte reste vide, en dessous.",
            "maman|Ils se touchent, les deux.",
            f"narrateur|{col}",
            "narrateur|Un pied de table reste dans l'ombre.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "enfant-m|La pince, sur le dossier.",
            "narrateur|Il pince le drap au dos du canapé.",
            "narrateur|Ça fait clic, et le tissu tient.",
            "narrateur|L'ours s'assoit devant, trop large pour la fente.",
            "narrateur|Le lapin se glisse dans le pli.",
            "papa|Chacun a sa place.",
            f"narrateur|{col}",
            "maman|Le secret a deux gardiens.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "enfant-m|L'ours, pour tenir le drap.",
            "narrateur|Il pose l'ours rond sur un coin.",
            "narrateur|Le tissu ne bouge plus.",
            "narrateur|Le lapin se couche dans le pli, tout mince.",
            "enfant-m|Tu es le mur, toi.",
            "maman|Et lui, le toit.",
            f"narrateur|{col}",
            "papa|Deux formes, un nid.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "enfant-m|On monte dessus.",
            "narrateur|Nino grimpe sur le canapé, le drap avec.",
            "narrateur|Le tissu devient une couverture, trop grande.",
            "narrateur|L'ours et le lapin s'installent au milieu.",
            "enfant-m|Plus besoin de la fente.",
            "papa|Vous êtes tous les trois, au chaud.",
            f"narrateur|{col}",
            "maman|Le secret est devenu un lit.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "enfant-m|On ferme la porte.",
            "narrateur|Papa pousse la porte d'entrée, tout doux.",
            "narrateur|Le courant s'arrête.",
            "narrateur|Le drap retombe, comme un toit.",
            "narrateur|Nino rassied le lapin contre l'ours.",
            "maman|Plus de vent, plus de chute.",
            f"narrateur|{col}",
            "papa|Ils se tiennent, maintenant.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "enfant-m|Dos à dos.",
            "narrateur|Il assied l'ours, puis le lapin contre lui.",
            "narrateur|Le rond et le mince se tiennent.",
            "narrateur|Le drap passe par-dessus, un seul toit.",
            "enfant-m|Vous ne tombez plus.",
            "papa|L'un calme l'autre.",
            f"narrateur|{col}",
            "maman|Deux silhouettes, une tente.",
        )
    return L(
        "enfant-m|Un train, dans le drap.",
        "narrateur|Nino aligne l'ours, puis le lapin.",
        "narrateur|L'ours rond est la locomotive.",
        "narrateur|Le lapin mince est le wagon.",
        "narrateur|Le drap fait un tunnel, au-dessus.",
        "enfant-m|On roule jusqu'au tapis.",
        f"narrateur|{col}",
        "papa|Ils partent ensemble, les deux.",
    )


def t3_fin(t1: int, t2: int, t3: int) -> list[str]:
    cd = PREP[t1]["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|L'ours garde l'entrée, le ventre chaud.",
            "narrateur|Le lapin fait coucou, depuis le fond.",
            "enfant-m|Bonsoir, tous les deux.",
            "maman|Ta tente a une porte, maintenant.",
            "papa|Merci d'avoir gardé les deux.",
            f"narrateur|{cd}",
            "narrateur|La bande de soleil a quitté le parquet.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Sous la table, ça sent le bois et le linge.",
            "enfant-m|Je rentre aussi, un peu.",
            "narrateur|Ses genoux touchent l'ours, puis le lapin.",
            "papa|Il y a de la place, pour trois.",
            "maman|Bravo, Nino.",
            f"narrateur|{cd}",
            "narrateur|Le radiateur fait encore un clic, plus bas.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Sur la chaise, les deux peluches se touchent.",
            "enfant-m|Le camp est plus haut, ici.",
            "papa|La grotte attendra une autre fois.",
            "maman|Ils sont bien, l'un contre l'autre.",
            f"narrateur|{cd}",
            "narrateur|Un pied de table reste dans l'ombre, tout seul.",
            "narrateur|Le salon parle plus bas, maintenant.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|La pince tient, au dos du canapé.",
            "enfant-m|Clic, et ça reste.",
            "narrateur|L'ours regarde le salon, le lapin le pli.",
            "papa|Chacun voit un côté.",
            "maman|Merci, Nino.",
            f"narrateur|{cd}",
            "narrateur|Le tissu du canapé redevient calme.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|L'ours rond pèse encore sur le coin.",
            "narrateur|Le lapin respire, tout mince, dans le pli.",
            "enfant-m|Vous dormez ?",
            "papa|On parle tout bas, alors.",
            "maman|Le nid a tenu.",
            f"narrateur|{cd}",
            "narrateur|Une poussière tourne, puis se pose.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Sur le canapé, le drap les couvre, trop grand.",
            "enfant-m|Moi aussi, je m'assois.",
            "narrateur|Trois silhouettes, sous le même tissu.",
            "papa|Bravo.",
            "maman|Le secret est devenu doux.",
            f"narrateur|{cd}",
            "narrateur|Le dossier craque une fois, puis plus.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|La porte fermée, le couloir n'a plus d'air.",
            "enfant-m|Le toit est retombé.",
            "narrateur|Le lapin s'appuie contre le ventre rond.",
            "papa|Plus personne ne tombe.",
            "maman|Merci d'avoir fermé.",
            f"narrateur|{cd}",
            "narrateur|Le parquet du couloir redevient froid, tout calme.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Dos à dos, le rond et le mince tiennent.",
            "enfant-m|Une tente, pour deux.",
            "papa|Ils n'ont pas la même ombre.",
            "maman|Et ils jouent quand même.",
            f"narrateur|{cd}",
            "narrateur|Nino éteint presque la lampe, puis la laisse.",
            "narrateur|Le couloir n'a plus qu'un souffle, tout bas.",
        )
    return L(
        "narrateur|Le train arrive sur le tapis, tout doux.",
        "enfant-m|Terminus.",
        "narrateur|L'ours s'arrête, le lapin contre lui.",
        "papa|Vous avez voyagé ensemble.",
        "maman|Merci, Nino.",
        f"narrateur|{cd}",
        "narrateur|Le drap-tunnel s'affaisse, et le salon se tait.",
    )


def write_tree(scripts: dict[str, list[str]], extras: dict[str, dict], sons: dict[str, str]) -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        scale, rate = (1.28, "slow") if kind == "passage_question" else (1.22, "medium")
        raw_son = sons.get(cid)
        if raw_son is None:
            raw_son = c.get("sons") or ""
            if raw_son == "chien_bonjour":
                raw_son = ""
        nc = make_chunk(c, scripts[cid], raw_son, scale, rate)
        if cid in extras:
            nc.update(extras[cid])
        by[cid] = nc
    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = "Nino, papa, maman"
    out["setting"] = "salon, fin d'après-midi, à la maison"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    if re_tom(blob):
        raise SystemExit(f"{SID} prénom hors troupe: tom")
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{SID} {c['chunk_id']} fin mécanique: {last}")
    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def re_tom(blob: str) -> bool:
    import re

    return bool(re.search(r"\btom\b", blob))


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": "tissu"}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Le radiateur du salon fait un petit clic, tout chaud.",
        "narrateur|Une bande de soleil barre le parquet, toute large.",
        "narrateur|Sous la table, l'ombre fait déjà une grotte.",
        "narrateur|Deux peluches attendent sur le tapis rêche.",
        "narrateur|L'ours est tout rond, le ventre en coton.",
        "narrateur|Le lapin est tout mince, une oreille trop longue.",
        "papa|Tu les as sorties du coffre, Nino ?",
        "enfant-m|Oui.",
        "enfant-m|Je veux une tente, pour elles.",
        "maman|Une tente, dans le salon ?",
        "enfant-m|Oui, maman.",
        "narrateur|En ce moment, Nino touche le drap plié sur la chaise.",
        "narrateur|Le tissu sent le linge, encore un peu froid.",
        "enfant-m|Elles ne se ressemblent pas.",
        "papa|On les emmène toutes les deux.",
        "maman|Le drap, la pince, et la lampe.",
        "papa|Tu prépares quoi, d'abord ?",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois choses attendent près du tapis.",
        "narrateur|Le drap, la pince, et la lampe.",
        "maman|Tu commences par laquelle ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le drap", "la pince", "la lampe")

    t3_by_t2 = {
        1: t3lab("la porte", "plus petit", "la chaise"),
        2: t3lab("la pince", "le poids", "dessus"),
        3: t3lab("fermer", "dos à dos", "le train"),
    }
    q_by_t1 = {
        1: qf(
            "le drap",
            "drap | le drap | un drap | le tissu | tissu",
            "Nino a jeté le tissu sur les peluches. Il a pris quoi ?",
        ),
        2: qf(
            "la pince",
            "pince | la pince | une pince | le bois",
            "Le bois a claqué. Nino a pris quoi ?",
        ),
        3: qf(
            "la lampe",
            "lampe | la lampe | une lampe | la lumière",
            "Un rond jaune est tombé. Nino a allumé quoi ?",
        ),
    }

    for t1 in (1, 2, 3):
        p = pre(t1)
        s[p] = t1_pass(t1)
        sons[p] = PREP[t1]["son"]
        s[f"{p}_Q0001"] = t1_q(t1)
        extras[f"{p}_Q0001"] = q_by_t1[t1]
        s[f"{p}_C0001"] = t1_c(t1)
        s[f"{p}_T0002_P0000"] = t2_q(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("sous la table", "derrière le canapé", "dans le couloir")
        for t2 in (1, 2, 3):
            sp = f"{p}_T0002_P000{t2}"
            s[sp] = t2_pass(t1, t2)
            sons[sp] = {1: "", 2: "tissu", 3: ""}[t2]
            s[f"{sp}_T0003_P0000"] = t3_q(t2)
            extras[f"{sp}_T0003_P0000"] = t3_by_t2[t2]
            for t3 in (1, 2, 3):
                tp = f"{sp}_T0003_P000{t3}"
                s[tp] = t3_pass(t1, t2, t3)
                s[f"{tp}_F0001"] = t3_fin(t1, t2, t3)
                if t2 == 1:
                    sons[tp] = ""
                elif t2 == 2:
                    sons[tp] = "tissu"
                else:
                    sons[tp] = ""

    write_tree(s, extras, sons)
    relecture(
        SID,
        TITLE,
        "Nino veut une tente pour l'ours rond et le lapin mince. "
        "T1 = drap / pince / lampe, les trois partent. "
        "T2×T3 = 9 aventures : table (porte, plus petit, chaise), "
        "canapé (pince, poids, dessus), couloir (fermer, dos à dos, train). "
        "Les deux peluches restent ensemble.",
        "Gabarit Tom/slogan jeté. Désir ≠ leçon. chunk_id inchangés. "
        "check() N3. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
