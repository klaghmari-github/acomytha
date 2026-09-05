#!/usr/bin/env python3
"""TREE-DIF-010 — chapeau de paille, Raphaël saute. DIF.ENE.001 implicite."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-010"
N3 = LIMITS["N3"]


def vet(lines: list[str]) -> list[str]:
    out = []
    for raw in lines:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N3:
            raise SystemExit(f"{n}>{N3}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        out.append(f"{role}|{ph}")
    return out


def t3(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {
        "expected_answer": ans,
        "accepted_examples": acc,
        "retry_prompt": retry,
    }


def write_tree(
    scripts: dict[str, list[str]],
    sons: dict[str, str],
    extras: dict[str, dict],
) -> None:
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
        nc = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), scale, rate)
        if cid in extras:
            nc.update(extras[cid])
        by[cid] = nc
    out = dict(src)
    out["fil_rouge"] = (
        "Le chapeau de paille sèche sur la rampe. Raphaël veut sauter dehors, "
        "le chapeau sur la tête. Le vent soulève l'aile. Il le tient, il attend "
        "un calme, ou il le donne à papa. Puis il saute. Le chapeau revient."
    )
    out["title"] = "Le chapeau de paille et Raphaël qui saute"
    out["characters"] = "Raphaël, papa, maman"
    out["setting"] = "maison de bois au bord de la mer"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for bad in (
        "cette énergie n'est pas une faute",
        "on peut jouer ou attendre",
        "on peut demander à un adulte",
        "lina",
        "sarah",
    ):
        if bad in blob:
            raise SystemExit(f"{SID} slogan/prénom: {bad}")
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


COUL = {
    1: dict(
        lab="le chapeau jaune",
        coul="jaune",
        objet="le chapeau jaune",
        aile="l'aile jaune",
        lum="une lumière dorée",
        odeur="la paille chaude",
        sol="le sable d'or",
        vent="le vent du soleil",
    ),
    2: dict(
        lab="le ruban rouge",
        coul="rouge",
        objet="le ruban rouge",
        aile="le ruban",
        lum="une ombre rose",
        odeur="le tissu chaud",
        sol="le sable rose",
        vent="le vent de la serviette",
    ),
    3: dict(
        lab="la dune verte",
        coul="verte",
        objet="la dune verte",
        aile="l'aile d'ombre",
        lum="une ombre d'herbe",
        odeur="l'oyat salé",
        sol="le sable gris-vert",
        vent="le vent de la dune",
    ),
}

LIEU = {
    1: dict(lab="le chemin", ou="sur le chemin", de="du chemin"),
    2: dict(lab="le bac", ou="dans le bac", de="du bac"),
    3: dict(lab="la rampe", ou="sur la rampe", de="de la rampe"),
}


def t1_pass(i: int) -> list[str]:
    if i == 1:
        return vet(
            [
                "narrateur|Raphaël prend le chapeau jaune, tout croustillant.",
                "enfant-m|Il sent le soleil.",
                "maman|La paille pique un peu le front.",
                "narrateur|Il le pose de travers, puis le remet droit.",
                "narrateur|Un grain de sable tombe de l'aile.",
                "papa|Tu veux sauter, avec ?",
                "enfant-m|Oui.",
                "enfant-m|Tout le chemin !",
                "narrateur|Il plie les genoux, trop vite.",
                "narrateur|Le vent soulève l'aile jaune, tout léger.",
                "enfant-m|Il veut partir !",
                "papa|Tu l'as senti, le vent ?",
                "narrateur|Le chapeau retombe, un peu de travers.",
                "maman|Le jaune brille encore, sur tes cheveux.",
            ]
        )
    if i == 2:
        return vet(
            [
                "narrateur|Raphaël tire le ruban rouge, tout mince.",
                "enfant-m|Il claque.",
                "papa|Il est cousu au chapeau, tu vois.",
                "narrateur|Le ruban bat sa joue, puis s'envole un peu.",
                "narrateur|Une ombre rose glisse sur le bois.",
                "maman|La serviette rayée claque, elle aussi.",
                "enfant-m|Je veux sauter, pour qu'il vole.",
                "papa|Comme un drapeau ?",
                "enfant-m|Oui, un drapeau !",
                "narrateur|Il s'élance, trop content.",
                "narrateur|Le ruban tire le chapeau vers le vent.",
                "enfant-m|Il m'échappe !",
                "maman|Le rouge est encore dans ta main.",
                "narrateur|Le fil chaud reste collé à ses doigts.",
            ]
        )
    return vet(
        [
            "narrateur|Raphaël tourne vers la dune verte.",
            "narrateur|Les oyats bougent, tout minces, et sentent le sel.",
            "enfant-m|L'herbe est haute.",
            "papa|Le vent vient de là-bas.",
            "narrateur|Le chapeau passe dans l'ombre de l'herbe.",
            "maman|L'aile a pris un peu de vert.",
            "enfant-m|Je saute jusqu'à la dune !",
            "narrateur|Il plie les genoux, face aux oyats.",
            "narrateur|Un souffle vert soulève la paille.",
            "enfant-m|Il grimpe !",
            "papa|La dune a son vent, tout fort.",
            "narrateur|Le chapeau retombe, une herbe sur le bord.",
            "maman|L'ombre verte est encore sur toi.",
            "enfant-m|Je le garde.",
        ]
    )


def t1_q(i: int) -> list[str]:
    if i == 1:
        return vet(
            [
                "narrateur|Le soleil a teinté la paille.",
                "papa|De quelle couleur est le chapeau ?",
            ]
        )
    if i == 2:
        return vet(
            [
                "narrateur|Un fil claque encore au vent.",
                "maman|De quelle couleur est le ruban ?",
            ]
        )
    return vet(
        [
            "narrateur|L'herbe a touché le bord.",
            "papa|De quelle couleur est la dune ?",
        ]
    )


def t1_c(i: int) -> list[str]:
    if i == 1:
        return vet(
            [
                "enfant-m|Jaune.",
                "papa|Oui.",
                "narrateur|La paille garde un rond de soleil.",
                "maman|Il tient encore, un peu de travers.",
                "enfant-m|Je veux sauter.",
                "papa|On choisit où, alors.",
                "narrateur|Le chapeau jaune attend le prochain saut.",
            ]
        )
    if i == 2:
        return vet(
            [
                "enfant-m|Rouge.",
                "maman|Oui.",
                "narrateur|Le ruban se calme, collé à la joue.",
                "papa|Il a failli partir avec le vent.",
                "enfant-m|Je saute encore.",
                "maman|On choisit l'endroit.",
                "narrateur|Le fil rouge tremble, tout mince.",
            ]
        )
    return vet(
        [
            "enfant-m|Verte.",
            "papa|Oui.",
            "narrateur|Une herbe reste sur l'aile, tout légère.",
            "maman|La dune t'a prêté son ombre.",
            "enfant-m|Je veux sauter là-bas.",
            "papa|On choisit le lieu, d'abord.",
            "narrateur|Le chapeau garde un peu de vert.",
        ]
    )


def t2_q(i: int) -> list[str]:
    c = COUL[i]
    return vet(
        [
            f"narrateur|{c['objet'].capitalize()} est sur sa tête, encore.",
            "narrateur|Le chemin de sable, le bac chaud, ou la rampe.",
            "papa|Où tu sautes, Raphaël ?",
        ]
    )


def t2_pass(i: int, j: int) -> list[str]:
    key = (i, j)
    if key == (1, 1):
        return vet(
            [
                "narrateur|Raphaël prend le chemin de sable, chapeau jaune.",
                "narrateur|Le sable est tiède, et ses pieds font toc.",
                "enfant-m|Je saute loin !",
                "narrateur|Il saute, trop grand, et l'aile bat.",
                "narrateur|Un nuage d'or s'envole autour des chevilles.",
                "papa|Le chapeau a bougé, tu as vu ?",
                "enfant-m|Il a dansé.",
                "maman|La mer est encore loin, tout calme.",
                "narrateur|Il plie encore les genoux, déjà.",
                "papa|On le garde, pendant le saut ?",
                "enfant-m|Oui.",
                "narrateur|L'aile jaune tremble au-dessus du chemin.",
            ]
        )
    if key == (1, 2):
        return vet(
            [
                "narrateur|Raphaël arrive au bac, le chapeau trop grand.",
                "narrateur|Le sable du bac est chaud, un peu rêche.",
                "enfant-m|Je saute dedans !",
                "narrateur|Il saute, et l'aile jaune se remplit de grains.",
                "maman|On dirait un seau, ton chapeau.",
                "enfant-m|Il est lourd, maintenant.",
                "papa|Vide-le tout doux, en marchant.",
                "narrateur|Il penche l'aile, et l'or retombe.",
                "narrateur|Un grain reste coincé dans la paille.",
                "enfant-m|Encore un saut ?",
                "maman|Le bac t'attend, le chapeau aussi.",
                "narrateur|Le jaune brille au fond du bac, tout petit.",
            ]
        )
    if key == (1, 3):
        return vet(
            [
                "narrateur|Raphaël revient vers la rampe de bois.",
                "narrateur|C'est là que le chapeau séchait, tout à l'heure.",
                "enfant-m|Je saute les marches !",
                "narrateur|Il saute la première, trop vite.",
                "narrateur|La paille racle le bois, et un fil jaune reste.",
                "papa|La rampe est étroite, pour les deux pieds.",
                "maman|Le sel a laissé un rond, sur la marche.",
                "enfant-m|Le chapeau a gratté.",
                "narrateur|Il pose une main sur la rampe, l'autre sur l'aile.",
                "papa|Tu montes, ou tu sautes encore ?",
                "enfant-m|Je saute, mais je le tiens.",
                "narrateur|Le bois sent le sel, et un peu le soleil.",
            ]
        )
    if key == (2, 1):
        return vet(
            [
                "narrateur|Le ruban rouge bat sur le chemin, comme un drapeau.",
                "narrateur|Raphaël court, puis saute, et le fil claque.",
                "enfant-m|Il vole !",
                "maman|Il t'a giflé la joue, tout doux.",
                "narrateur|Une ombre rose court à côté de ses pieds.",
                "papa|Le chemin est long, le ruban est court.",
                "enfant-m|Je saute plus fort.",
                "narrateur|Le saut tire le chapeau vers l'avant.",
                "narrateur|Le ruban s'enroule un peu autour du poignet.",
                "maman|Il s'est accroché à toi.",
                "papa|Tu le libères, ou tu le gardes ainsi ?",
                "narrateur|Le fil chaud reste collé, tout mince.",
            ]
        )
    if key == (2, 2):
        return vet(
            [
                "narrateur|Raphaël penche le ruban au-dessus du bac.",
                "narrateur|Le sable rose de l'ombre colle déjà.",
                "enfant-m|Je le garde hors du sable.",
                "papa|On saute, le ruban en l'air.",
                "narrateur|Il saute au bord, et le ruban plonge.",
                "maman|Une virgule rouge dans le bac.",
                "enfant-m|Je le sors !",
                "narrateur|Il tire, trop fort, et le chapeau penche.",
                "narrateur|Du sable tombe de l'aile, tout fin.",
                "papa|Tout doux, le fil est mince.",
                "enfant-m|Je recommence le saut.",
                "narrateur|Le ruban garde un grain, tout rouge de poussière.",
            ]
        )
    if key == (2, 3):
        return vet(
            [
                "narrateur|Sur la rampe, le ruban s'accroche à un clou.",
                "narrateur|Raphaël saute, et le fil tire en arrière.",
                "enfant-m|Il est coincé !",
                "maman|Le bois a pris le rouge.",
                "papa|On le détache, sans tirer trop.",
                "narrateur|Il s'arrête sur la marche, le chapeau de travers.",
                "narrateur|Le ruban vibre, tendu entre le clou et lui.",
                "enfant-m|Je saute pour le libérer ?",
                "papa|Ou tu attends, et on le glisse.",
                "maman|Le clou est lisse, un peu de sel dessus.",
                "narrateur|Une ombre rose reste sur le bois.",
                "enfant-m|Je veux le ruban, et je veux sauter.",
            ]
        )
    if key == (3, 1):
        return vet(
            [
                "narrateur|Le chemin monte un peu, vers les oyats.",
                "narrateur|Raphaël saute, et l'ombre verte le suit.",
                "enfant-m|La dune m'appelle !",
                "papa|Le vent vient d'en haut, tout salé.",
                "narrateur|L'aile d'ombre se soulève à chaque saut.",
                "maman|Une herbe a voyagé jusqu'ici.",
                "enfant-m|Je saute plus près.",
                "narrateur|Le sable gris-vert gicle, puis retombe.",
                "narrateur|Le chapeau penche vers la dune, déjà.",
                "papa|Tu vas jusqu'aux oyats, ou tu restes ici ?",
                "enfant-m|Encore un saut, d'abord.",
                "narrateur|Le vent de la dune chante dans la paille.",
            ]
        )
    if key == (3, 2):
        return vet(
            [
                "narrateur|Le bac est au pied de la dune, un peu d'herbe dedans.",
                "narrateur|Raphaël saute au bord, chapeau d'ombre.",
                "enfant-m|Il y a de l'herbe, dans le sable !",
                "maman|Un oyat a perdu un brin.",
                "narrateur|Le brin s'accroche à l'aile, tout vert.",
                "papa|Tu le laisses, ou tu le sors ?",
                "enfant-m|Je saute, après je vois.",
                "narrateur|Il saute, et le brin danse sur le bord.",
                "narrateur|Le sable du bac sent l'herbe, un peu humide.",
                "maman|La dune est juste derrière, tu l'entends.",
                "enfant-m|Elle souffle fort.",
                "narrateur|Le chapeau garde le brin, comme un secret.",
            ]
        )
    return vet(
        [
            "narrateur|La rampe regarde la dune, tout droit.",
            "narrateur|Raphaël saute sur le bois, face aux oyats.",
            "enfant-m|Le vent me pousse !",
            "papa|Il vient de l'herbe, pas de la mer.",
            "narrateur|L'aile d'ombre claque contre la rampe.",
            "maman|Le bois a une ombre d'herbe, tout étroite.",
            "enfant-m|Je saute plus haut.",
            "narrateur|Le saut le rapproche du vent, trop près.",
            "narrateur|Le chapeau bascule, une graine d'oyat dessus.",
            "papa|Tu le rattrapes, ou tu t'arrêtes ?",
            "enfant-m|Les deux.",
            "narrateur|La rampe vibre encore, sous ses pieds nus.",
        ]
    )


def t3_q(i: int, j: int) -> list[str]:
    c = COUL[i]
    l = LIEU[j]
    return vet(
        [
            f"narrateur|{c['objet'].capitalize()} bouge encore {l['ou']}.",
            "maman|Tu le tiens, tu attends, ou tu le donnes ?",
            "papa|Le vent écoute, lui aussi.",
        ]
    )


def t3_pass(i: int, j: int, k: int) -> list[str]:
    c = COUL[i]
    l = LIEU[j]
    if k == 1:
        suite = {
            1: [
                "narrateur|Il pose les deux mains sur l'aile, puis saute.",
                f"narrateur|{c['aile'].capitalize()} reste, {l['ou']}.",
                "enfant-m|Il n'est pas parti.",
                "papa|Tu l'as gardé, pendant le saut.",
                f"narrateur|{c['lum'].capitalize()} tremble, puis se calme.",
            ],
            2: [
                "narrateur|Il plaque le chapeau, et saute au bord du bac.",
                f"narrateur|{c['aile'].capitalize()} ne se remplit plus.",
                "enfant-m|Mes mains l'ont tenu.",
                "maman|Le sable est resté en bas.",
                f"narrateur|{c['sol'].capitalize()} ne vole plus.",
            ],
            3: [
                "narrateur|Une main sur la rampe, une main sur l'aile.",
                "narrateur|Il saute la marche, tout court.",
                "enfant-m|Le bois et le chapeau, ensemble.",
                "papa|Tu as tenu les deux.",
                f"narrateur|{c['odeur'].capitalize()} reste sur le bois.",
            ],
        }[j]
        return vet(
            [
                "enfant-m|Je le tiens.",
                "narrateur|Raphaël serre la paille, tout contre le crâne.",
            ]
            + suite
        )
    if k == 2:
        suite = {
            1: [
                "narrateur|Il s'accroupit sur le sable, chapeau sur les genoux.",
                f"narrateur|{c['vent'].capitalize()} passe, puis s'en va.",
                "enfant-m|Maintenant ?",
                "papa|Maintenant, un saut.",
                f"narrateur|Il saute {l['ou']}, tout simple.",
            ],
            2: [
                "narrateur|Il s'assoit au bord du bac, l'aile à plat.",
                "narrateur|Un grain roule, puis plus rien.",
                "enfant-m|Le bac s'est tu.",
                "maman|Tu peux sauter, tout petit.",
                "narrateur|Il remet l'aile, puis saute un tout petit saut.",
            ],
            3: [
                "narrateur|Il pose le chapeau sur la marche, et compte.",
                "enfant-m|Un, deux.",
                "papa|Le bois ne claque plus.",
                "narrateur|Il reprend l'aile, puis saute une marche.",
                f"maman|{c['vent'].capitalize()} a fini sa course.",
            ],
        }[j]
        return vet(
            [
                "enfant-m|J'attends.",
                f"narrateur|Raphaël s'arrête {l['ou']}, le souffle encore haut.",
            ]
            + suite
        )
    suite = {
        1: [
            "narrateur|Papa prend le chapeau, et Raphaël saute libre.",
            "enfant-m|Plus haut !",
            "papa|Je le garde, va.",
            f"narrateur|{c['lum'].capitalize()} reste dans les mains de papa.",
            "maman|Le chemin est à tes pieds, maintenant.",
        ],
        2: [
            "narrateur|Maman prend le chapeau, hors du bac.",
            "enfant-m|Je saute sans lui !",
            "maman|Je le tiens au chaud.",
            "narrateur|Il saute dans le sable, les cheveux au vent.",
            "papa|Le bac est à toi, le chapeau à nous.",
        ],
        3: [
            "narrateur|Papa pose le chapeau sur la rampe, tout droit.",
            "enfant-m|Je saute les marches !",
            "papa|Il t'attend ici.",
            "narrateur|Raphaël saute, les mains libres, tout léger.",
            f"maman|{c['objet'].capitalize()} ne bouge plus, sur le bois.",
        ],
    }[j]
    return vet(
        [
            "enfant-m|Je le donne.",
            f"narrateur|Raphaël tend {c['objet']}, encore chaud.",
        ]
        + suite
    )


FIN_IMG = {
    (1, 1, 1): "L'aile jaune ne bouge plus, sur le chemin.",
    (1, 1, 2): "Le chapeau attendait, plat, puis il a sauté.",
    (1, 1, 3): "Papa rend le jaune, après le grand saut.",
    (1, 2, 1): "Un grain d'or reste dans la paille.",
    (1, 2, 2): "Le bac garde un rond d'ombre jaune.",
    (1, 2, 3): "Le chapeau sèche dans les mains de maman.",
    (1, 3, 1): "La rampe a un fil de paille, tout mince.",
    (1, 3, 2): "Le bois attendait, le chapeau sur les genoux.",
    (1, 3, 3): "Le chapeau est revenu sur la rampe, droit.",
    (2, 1, 1): "Le ruban rouge ne claque plus.",
    (2, 1, 2): "Le ruban s'est calmé, collé à la joue.",
    (2, 1, 3): "Papa tient encore le fil, tout calme.",
    (2, 2, 1): "Un fil rouge reste dans le sable du bac.",
    (2, 2, 2): "Le bac a une virgule rouge, tout fine.",
    (2, 2, 3): "Maman démêle le ruban, hors du bac.",
    (2, 3, 1): "Le ruban a quitté le clou de la rampe.",
    (2, 3, 2): "Le bois garde une ombre rose.",
    (2, 3, 3): "Le ruban revient, lisse, dans sa main.",
    (3, 1, 1): "Une herbe verte reste sur l'aile.",
    (3, 1, 2): "Le chapeau a attendu dans l'ombre des oyats.",
    (3, 1, 3): "Papa rend le chapeau, face à la dune.",
    (3, 2, 1): "Un brin d'oyat croise encore le bac.",
    (3, 2, 2): "Le sable vert-gris s'est calmé.",
    (3, 2, 3): "Maman souffle une graine hors de la paille.",
    (3, 3, 1): "La rampe a une ombre d'herbe, tout étroite.",
    (3, 3, 2): "Le bois sent encore la dune.",
    (3, 3, 3): "Le chapeau est rentré, vert d'ombre, puis sec.",
}

FIN_DROP = {
    1: "Une goutte de sel a séché sur le bois.",
    2: "La serviette rayée ne claque plus.",
    3: "Les oyats parlent plus bas, maintenant.",
}


def t3_fin(i: int, j: int, k: int) -> list[str]:
    c = COUL[i]
    l = LIEU[j]
    img = FIN_IMG[(i, j, k)]
    drop = FIN_DROP[i]
    if k == 1:
        return vet(
            [
                f"narrateur|{img}",
                "enfant-m|J'ai sauté, avec.",
                "papa|Bravo, Raphaël.",
                f"maman|{c['objet'].capitalize()} est encore à toi.",
                f"narrateur|Ils restent un peu {l['ou']}, sans courir.",
                "papa|Merci d'avoir tenu l'aile.",
                f"narrateur|{drop}",
                "narrateur|Une mouette crie, plus loin, tout bas.",
                f"narrateur|{c['odeur'].capitalize()} reste dans ses cheveux.",
            ]
        )
    if k == 2:
        return vet(
            [
                f"narrateur|{img}",
                "enfant-m|J'ai attendu le vent.",
                "maman|Puis tu as sauté, tout simple.",
                "papa|Merci d'avoir pris le temps.",
                f"narrateur|{c['objet'].capitalize()} est calme, maintenant.",
                f"narrateur|{drop}",
                "narrateur|Le sel pique encore un peu le nez.",
                f"narrateur|{l['lab'].capitalize()} ne bouge plus, ou presque.",
            ]
        )
    return vet(
        [
            f"narrateur|{img}",
            "enfant-m|Vous l'avez gardé, pour moi.",
            "papa|Et toi, tu as sauté.",
            "maman|Bravo, Raphaël.",
            "maman|Le chapeau te revient.",
            "narrateur|Il le remet, un peu de travers, puis droit.",
            f"narrateur|{drop}",
            "narrateur|La maison sent encore le linge chaud.",
            f"narrateur|{c['lum'].capitalize()} s'en va, tout doux.",
        ]
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = vet(
        [
            "narrateur|Le bois de la rampe sent encore le sel.",
            "narrateur|Une goutte glisse, lente, et fait ploc sur le bord.",
            "narrateur|Loin, une mouette crie, tout bas.",
            "narrateur|La maison sent le linge chaud, un peu rêche.",
            "papa|Le chapeau de paille sèche, Raphaël.",
            "enfant-m|Il est à moi.",
            "maman|Le vent le touche déjà, tu vois.",
            "narrateur|Papa déplie une serviette rayée, sable aux bords.",
            "narrateur|Les chaussures restent mouillées, près de la porte.",
            "enfant-m|Je veux sauter, avec le chapeau.",
            "papa|Tu le gardes, même si ça saute ?",
            "enfant-m|Oui.",
            "narrateur|En ce moment, Raphaël tend la main vers la paille.",
            "maman|Jaune, rouge, ou vert ?",
            "narrateur|Le jaune dort au soleil, tout croustillant.",
            "narrateur|Un ruban rouge pend, tout mince.",
            "narrateur|Vers la dune, l'ombre est verte.",
        ]
    )
    sons["CHK_T0000_P0000"] = "oiseau,vague"

    s["CHK_T0001_P0000"] = vet(
        [
            "narrateur|Trois couleurs attendent le saut.",
            "narrateur|Le jaune du chapeau, le rouge du ruban, le vert de la dune.",
            "papa|Lequel colore ton saut, Raphaël ?",
        ]
    )
    extras["CHK_T0001_P0000"] = t3(
        "le chapeau jaune", "le ruban rouge", "la dune verte"
    )

    q_extra = {
        1: qf(
            "jaune",
            "jaune | chapeau jaune | paille | doré | dorée | soleil",
            "Le soleil a teinté la paille. De quelle couleur est le chapeau ?",
        ),
        2: qf(
            "rouge",
            "rouge | ruban | ruban rouge | fil | rose",
            "Un fil claque au vent. De quelle couleur est le ruban ?",
        ),
        3: qf(
            "verte",
            "verte | vert | dune | dune verte | herbe | oyats | oyat",
            "L'herbe a touché le bord. De quelle couleur est la dune ?",
        ),
    }

    t1_sons = {1: "vent", 2: "vent", 3: "vent"}
    t2_sons = {1: "sable", 2: "sable", 3: "bois"}

    for i, coul in COUL.items():
        p = f"CHK_T0001_P000{i}"
        s[p] = t1_pass(i)
        sons[p] = t1_sons[i]
        s[f"{p}_Q0001"] = t1_q(i)
        extras[f"{p}_Q0001"] = q_extra[i]
        s[f"{p}_C0001"] = t1_c(i)
        s[f"{p}_T0002_P0000"] = t2_q(i)
        extras[f"{p}_T0002_P0000"] = t3("le chemin", "le bac", "la rampe")
        for j, lieu in LIEU.items():
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = t2_pass(i, j)
            sons[p2] = t2_sons[j]
            s[f"{p2}_T0003_P0000"] = t3_q(i, j)
            extras[f"{p2}_T0003_P0000"] = t3("je le tiens", "j'attends", "je le donne")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = t3_pass(i, j, k)
                s[f"{p3}_F0001"] = t3_fin(i, j, k)

    write_tree(s, sons, extras)
    relecture(
        SID,
        "Le chapeau de paille et Raphaël qui saute",
        "Raphaël veut sauter dehors avec le chapeau de paille. "
        "T1 colore le voyage (chapeau jaune / ruban rouge / dune verte). "
        "T2 change le lieu du saut (chemin / bac / rampe). "
        "T3 change la fin (il tient, il attend le vent, ou il donne le chapeau). "
        "Le vent soulève l'aile ; l'élan se voit, la leçon énergie n'est pas dite.",
        "Gabarit Sarah/Lina/cubes/dînette jeté. Slogans DIF.ENE retirés. "
        "Questions factuelles (couleur). Fins vécues, sans « l'histoire est finie ». "
        "Audio non cuit. 27 chemins non écoutés à voix haute.",
    )


if __name__ == "__main__":
    main()
