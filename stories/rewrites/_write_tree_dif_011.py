#!/usr/bin/env python3
"""TREE-DIF-011 — parasol jaune, Amir propose, Nina répond. DIF.BES.002 implicite."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-011"
N2 = LIMITS["N2"]

EXTRA_FORBID = (
    "nora",
    "plusieurs réponses",
    "on propose",
    "on accepte",
    "c'est du bon travail",
    "tu as fait du bon travail",
    "regarder, c'est une réponse",
    "un non est possible",
)


def vet(lines: list[str]) -> list[str]:
    out = []
    for raw in lines:
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
        raise SystemExit(f"{SID} missing={missing[:8]} extra={sorted(extra_ids)[:8]}")
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
        "Le parasol jaune fait un rond d'ombre sur la plage. Amir veut s'y asseoir "
        "et jouer avec Nina. Il l'invite près du sable, des galets, ou de l'ombre. "
        "Le seau, le filet ou le livre change le jeu. Nina regarde, dit plus tard, "
        "ou non. Amir dit d'accord. Le parasol garde son rond frais."
    )
    out["title"] = "Le parasol jaune et la réponse d'Amir"
    out["characters"] = "Amir, Nina, papa, maman"
    out["setting"] = "plage, sous un parasol jaune"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for bad in EXTRA_FORBID:
        if bad in blob:
            raise SystemExit(f"{SID} interdit extra: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    check(SID, out["age_band"], out["chunks"])
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


LIEU = {
    1: dict(
        lab="le sable",
        son="sable",
        q_ans="sable",
        q_acc="sable | le sable | chaud | château | colline | genoux",
        q_retry="Amir s'agenouille. Où sont ses genoux ?",
    ),
    2: dict(
        lab="les galets",
        son="galet",
        q_ans="galets",
        q_acc="galets | galet | les galets | gris | file | pierres | pierre",
        q_retry="Amir pose des pierres lisses. Que pose-t-il ?",
    ),
    3: dict(
        lab="l'ombre",
        son="toile",
        q_ans="jaune",
        q_acc="jaune | parasol | parasol jaune | ombre | le jaune",
        q_retry="Le parasol fait l'ombre. De quelle couleur est-il ?",
    ),
}

OBJ = {
    1: dict(lab="le seau", son="seau"),
    2: dict(lab="le filet", son="filet"),
    3: dict(lab="le livre", son="page"),
}


def t1_pass(i: int) -> list[str]:
    if i == 1:
        return vet(
            [
                "narrateur|Amir s'agenouille sur le sable chaud.",
                "narrateur|Le grain colle aux genoux, tout fin.",
                "narrateur|Il pousse une colline, pour un château.",
                "narrateur|La tour penche, trop sèche.",
                "enfant-m|Elle tombe.",
                "papa|Le sable a soif.",
                "narrateur|Nina s'arrête, un peu plus loin.",
                "enfant-m|Tu viens, Nina ?",
                "enfant-m|On fait un château ?",
                "narrateur|Nina garde les mains sur ses genoux.",
                "maman|Elle t'a entendu.",
                "narrateur|Amir creuse un creux, tout près.",
                "enfant-m|Ta place est là.",
                "narrateur|Un grain brille encore, tout chaud.",
            ]
        )
    if i == 2:
        return vet(
            [
                "narrateur|Amir s'accroupit près des galets.",
                "narrateur|Ils sont lisses, un peu froids.",
                "narrateur|Un gris porte une ligne blanche.",
                "enfant-m|Un chemin, jusqu'au parasol.",
                "maman|Les galets glissent, tout doux.",
                "narrateur|Nina touche l'eau, plus bas.",
                "enfant-m|Tu poses un galet, Nina ?",
                "narrateur|Nina recule d'un pas, vers l'écume.",
                "papa|Elle t'écoute, depuis l'eau.",
                "narrateur|Amir aligne deux galets, tout droits.",
                "enfant-m|Je te garde une pierre.",
                "narrateur|La ligne blanche reste au soleil.",
            ]
        )
    return vet(
        [
            "narrateur|Amir rejoint le rond sous le parasol.",
            "narrateur|La toile jaune vibre, un peu sèche.",
            "narrateur|L'ombre saute quand le vent passe.",
            "enfant-m|Elle part !",
            "papa|Le pied du parasol bouge.",
            "narrateur|Nina reste au bord du rond frais.",
            "enfant-m|Tu t'assois, Nina ?",
            "enfant-m|Il y a de la place.",
            "narrateur|Nina plisse les yeux, vers la toile.",
            "maman|Le rond est là, pour vous deux.",
            "narrateur|Amir appuie le pied, des deux mains.",
            "enfant-m|Je tiens l'ombre.",
            "narrateur|Un coin de toile claque, puis se tait.",
        ]
    )


def t1_q(i: int) -> list[str]:
    if i == 1:
        return vet(
            [
                "narrateur|Amir a poussé une colline.",
                "papa|Où sont ses genoux ?",
            ]
        )
    if i == 2:
        return vet(
            [
                "narrateur|Amir aligne des pierres lisses.",
                "maman|Que pose-t-il ?",
            ]
        )
    return vet(
        [
            "narrateur|Le parasol fait un rond d'ombre.",
            "papa|De quelle couleur est le parasol ?",
        ]
    )


def t1_c(i: int) -> list[str]:
    if i == 1:
        return vet(
            [
                "enfant-m|Sur le sable.",
                "papa|Oui.",
                "narrateur|La colline attend encore un peu d'eau.",
                "maman|Merci, Amir.",
                "enfant-m|Je continue.",
                "narrateur|Un grain reste collé au genou.",
            ]
        )
    if i == 2:
        return vet(
            [
                "enfant-m|Des galets.",
                "maman|Oui.",
                "narrateur|Deux pierres tiennent déjà, tout calmes.",
                "papa|Merci.",
                "enfant-m|Le chemin va au parasol.",
                "narrateur|La ligne blanche brille encore.",
            ]
        )
    return vet(
        [
            "enfant-m|Jaune.",
            "papa|Oui.",
            "narrateur|Le rond d'ombre se tient, un moment.",
            "maman|Merci, Amir.",
            "enfant-m|Nina a une place.",
            "narrateur|La toile jaune ne claque plus.",
        ]
    )


def t2_pass(i: int, j: int) -> list[str]:
    scenes = {
        (1, 1): [
            "narrateur|Amir prend le seau rouge.",
            "narrateur|Le plastique brûle un peu les doigts.",
            "narrateur|Du sable sec tombe, tout fin.",
            "enfant-m|Il a soif, le château.",
            "papa|Va chercher l'eau de la flaque.",
            "narrateur|Amir plonge le seau, tout doux.",
            "narrateur|L'eau tiède tape, contre le bord.",
            "enfant-m|Tu portes le seau, Nina ?",
            "narrateur|Nina avance le menton, sans bouger.",
            "maman|Elle a vu l'eau.",
            "narrateur|Un rond mouillé reste dans le sable.",
        ],
        (1, 2): [
            "narrateur|Amir traîne le filet sur le sable mouillé.",
            "narrateur|Les mailles sentent le sel, un peu rêche.",
            "narrateur|Le vent gonfle le filet, puis le lâche.",
            "enfant-m|Du sable mouillé, pour la tour.",
            "maman|Les mailles en prennent beaucoup.",
            "narrateur|Une motte lourde reste au fond.",
            "enfant-m|Tu tiens le manche, Nina ?",
            "narrateur|Nina suit le filet des yeux.",
            "papa|Le sel brille sur les mailles.",
            "narrateur|Le filet laisse une ligne, tout longue.",
        ],
        (1, 3): [
            "narrateur|Amir ouvre le livre, près de la colline.",
            "narrateur|Un coin de page est encore mouillé.",
            "narrateur|Un crabe rouge est dessiné, tout large.",
            "enfant-m|Un château crabe !",
            "papa|Comme sur la page.",
            "narrateur|Du sable glisse dans le pli.",
            "enfant-m|Tu regardes le crabe, Nina ?",
            "narrateur|Nina penche la tête, tout près du dessin.",
            "maman|Le crabe a deux pinces, sur le papier.",
            "narrateur|La page claque, puis se calme.",
        ],
        (2, 1): [
            "narrateur|Amir glisse des galets dans le seau.",
            "narrateur|Ils sonnent, tout secs, contre le plastique.",
            "narrateur|Le seau penche, déjà lourd.",
            "enfant-m|Trop lourd, tout seul.",
            "papa|Le chemin peut se faire pierre par pierre.",
            "narrateur|Amir pose un galet, vers le parasol.",
            "enfant-m|Tu en poses un, Nina ?",
            "narrateur|Nina reste près de l'écume, les pieds mouillés.",
            "maman|Le seau attend, à mi-chemin.",
            "narrateur|Un galet gris tinte encore, tout bas.",
        ],
        (2, 2): [
            "narrateur|Amir plonge le filet dans l'écume.",
            "narrateur|Une vague courte mouille les mailles.",
            "narrateur|Un galet lisse reste pris, tout rond.",
            "enfant-m|Je l'ai !",
            "maman|Il brille encore, tout mouillé.",
            "narrateur|Amir le pose en ligne, vers l'ombre.",
            "enfant-m|Tu en prends un, Nina ?",
            "narrateur|Nina recule quand la vague revient.",
            "papa|Le filet goutte sur le sable.",
            "narrateur|Une goutte de sel perle au bout.",
        ],
        (2, 3): [
            "narrateur|Amir pose le livre au départ du chemin.",
            "narrateur|Un galet plat tient la page ouverte.",
            "narrateur|Des galets de couleurs sont dessinés.",
            "enfant-m|Le gris, comme le mien.",
            "papa|La page montre une ligne, aussi.",
            "narrateur|Le vent veut emporter le livre.",
            "enfant-m|Tu choisis un galet, Nina ?",
            "narrateur|Nina regarde le dessin, sans se baisser.",
            "maman|Le galet plat fait un poids.",
            "narrateur|La page tient, contre le vent.",
        ],
        (3, 1): [
            "narrateur|Amir pose le seau sur le pied du parasol.",
            "narrateur|Le plastique est frais, à l'ombre.",
            "narrateur|Le rond jaune arrête de sauter.",
            "enfant-m|Il tient !",
            "papa|Le seau pèse, tout juste.",
            "narrateur|Un peu de sable entre sous le pied.",
            "enfant-m|Tu t'assois, Nina ?",
            "narrateur|Nina reste au soleil, tout au bord.",
            "maman|L'ombre a de la place, encore.",
            "narrateur|Le seau garde le pied, sans bouger.",
        ],
        (3, 2): [
            "narrateur|Amir accroche le filet à une tige.",
            "narrateur|Les mailles font un second toit, tout léger.",
            "narrateur|Une ombre rayée tombe sur le sable.",
            "enfant-m|Plus d'ombre !",
            "maman|Le filet sèche déjà, tout salé.",
            "narrateur|Une goutte glisse le long d'une maille.",
            "enfant-m|Tu viens sous le filet, Nina ?",
            "narrateur|Nina lève la main, vers les mailles.",
            "papa|La goutte va tomber, tout lent.",
            "narrateur|Le filet fait un bruit de toile, très fin.",
        ],
        (3, 3): [
            "narrateur|Amir s'assoit avec le livre, dans le rond.",
            "narrateur|La page sent encore le sel, un peu.",
            "narrateur|Le crabe rouge attend, sous le jaune.",
            "enfant-m|On lit ici, Nina ?",
            "papa|Le vent tourne les pages, tout seul.",
            "narrateur|Amir pose un doigt, pour tenir.",
            "narrateur|Nina s'arrête à la limite de l'ombre.",
            "maman|Le crabe reste sur le papier.",
            "enfant-m|Ta place est au frais.",
            "narrateur|Un coin de page tremble, puis tient.",
        ],
    }
    return vet(scenes[(i, j)])


def t2_trans(i: int) -> list[str]:
    if i == 1:
        return vet(
            [
                "narrateur|La colline attend un geste, encore.",
                "maman|Le seau, le filet, ou le livre ?",
                "papa|Qu'est-ce qui aide le château ?",
            ]
        )
    if i == 2:
        return vet(
            [
                "narrateur|Le chemin de galets n'est pas fini.",
                "papa|Le seau, le filet, ou le livre ?",
                "maman|Qu'est-ce qui porte les pierres ?",
            ]
        )
    return vet(
        [
            "narrateur|Le rond jaune veut tenir, encore.",
            "maman|Le seau, le filet, ou le livre ?",
            "papa|Qu'est-ce qui garde l'ombre ?",
        ]
    )


def t3_trans(j: int) -> list[str]:
    if j == 1:
        return vet(
            [
                "narrateur|Nina est près du seau, tout calme.",
                "papa|Elle regarde, plus tard, ou un non ?",
                "maman|On l'écoute.",
            ]
        )
    if j == 2:
        return vet(
            [
                "narrateur|Nina suit le filet des yeux.",
                "maman|Elle regarde, plus tard, ou un non ?",
                "papa|Sa réponse arrive.",
            ]
        )
    return vet(
        [
            "narrateur|Nina est près du livre ouvert.",
            "papa|Elle regarde, plus tard, ou un non ?",
            "maman|On reste tout près.",
        ]
    )


def t3_pass(i: int, j: int, k: int) -> list[str]:
    # k=1 regarder, k=2 plus tard, k=3 non
    suite = {
        (1, 1, 1): [
            "enfant-f|Je regarde.",
            "enfant-m|D'accord.",
            "narrateur|Amir verse l'eau, tout doux, sur la tour.",
            "narrateur|Nina suit le filet d'eau des yeux.",
            "papa|La tour boit, sans se casser.",
            "narrateur|Le seau reste à sa place, tout près.",
        ],
        (1, 1, 2): [
            "enfant-f|Plus tard.",
            "enfant-m|D'accord.",
            "narrateur|Amir pose le seau à l'ombre du château.",
            "enfant-m|Je te le garde.",
            "narrateur|Nina recule vers la flaque, un pas.",
            "maman|L'eau attend, dans le plastique.",
            "narrateur|Un filet d'eau brille encore au bord.",
        ],
        (1, 1, 3): [
            "enfant-f|Non.",
            "enfant-m|D'accord.",
            "narrateur|Amir verse tout seul, une petite gorgée.",
            "narrateur|La tour tient, plus basse, plus ferme.",
            "papa|Elle a assez bu.",
            "narrateur|Nina reste près de l'eau, les pieds mouillés.",
            "narrateur|Le seau vide sent encore le sel.",
        ],
        (1, 2, 1): [
            "enfant-f|Je regarde.",
            "enfant-m|D'accord.",
            "narrateur|Amir dépose la motte, contre la colline.",
            "narrateur|Nina suit le geste, sans toucher le manche.",
            "maman|Le sable mouillé colle, tout lourd.",
            "narrateur|Le filet s'affaisse, vide, sur le chaud.",
        ],
        (1, 2, 2): [
            "enfant-f|Plus tard.",
            "enfant-m|D'accord.",
            "narrateur|Amir laisse le filet ouvert, à côté.",
            "enfant-m|Ta motte est là.",
            "narrateur|Nina s'éloigne vers une coquille.",
            "papa|Le sel sèche déjà sur les mailles.",
            "narrateur|Une maille garde un grain, tout pris.",
        ],
        (1, 2, 3): [
            "enfant-f|Non.",
            "enfant-m|D'accord.",
            "narrateur|Amir tasse la motte, tout seul, du poing.",
            "narrateur|Une petite tour se tient, encore ronde.",
            "maman|Elle a pris le sable mouillé.",
            "narrateur|Nina est déjà près de l'écume.",
            "narrateur|Le filet repose, tout salé.",
        ],
        (1, 3, 1): [
            "enfant-f|Je regarde.",
            "enfant-m|D'accord.",
            "narrateur|Amir pince le sable, comme les pinces.",
            "narrateur|Nina suit le crabe du livre, du regard.",
            "papa|Deux petites pinces, dans le grain.",
            "narrateur|La page reste ouverte, entre eux.",
        ],
        (1, 3, 2): [
            "enfant-f|Plus tard.",
            "enfant-m|D'accord.",
            "narrateur|Amir laisse le livre ouvert, sur le sable.",
            "enfant-m|Le crabe t'attend.",
            "narrateur|Nina part vers la flaque, tout lent.",
            "maman|Le dessin ne bouge plus.",
            "narrateur|Un grain reste dans le pli de la page.",
        ],
        (1, 3, 3): [
            "enfant-f|Non.",
            "enfant-m|D'accord.",
            "narrateur|Amir fait une pince, tout seul, dans le grain.",
            "narrateur|Le château crabe est petit, tout rouge de sable.",
            "papa|Il ressemble, un peu.",
            "narrateur|Nina s'éloigne, les mains dans le dos.",
            "narrateur|La page claque une dernière fois.",
        ],
        (2, 1, 1): [
            "enfant-f|Je regarde.",
            "enfant-m|D'accord.",
            "narrateur|Amir pose un galet, puis un autre.",
            "narrateur|Nina compte des yeux, sans les prendre.",
            "papa|Le chemin avance, pierre par pierre.",
            "narrateur|Le seau s'allège, tout doux.",
        ],
        (2, 1, 2): [
            "enfant-f|Plus tard.",
            "enfant-m|D'accord.",
            "narrateur|Amir laisse un galet hors du seau.",
            "enfant-m|Celui-là, pour toi.",
            "narrateur|Nina s'essuie un pied, dans l'écume.",
            "maman|La pierre lisse attend, au soleil.",
            "narrateur|Le seau tient encore trois galets.",
        ],
        (2, 1, 3): [
            "enfant-f|Non.",
            "enfant-m|D'accord.",
            "narrateur|Amir finit une petite file, tout seul.",
            "narrateur|Elle s'arrête avant le parasol, assez.",
            "papa|Le chemin est court, et il tient.",
            "narrateur|Nina reste dans l'eau, jusqu'aux chevilles.",
            "narrateur|Le seau vide penche, sur le sable.",
        ],
        (2, 2, 1): [
            "enfant-f|Je regarde.",
            "enfant-m|D'accord.",
            "narrateur|Amir tire le galet hors des mailles.",
            "narrateur|Nina suit la goutte qui tombe.",
            "maman|Il brille encore, tout mouillé.",
            "narrateur|Le filet s'égoutte, vers le chemin.",
        ],
        (2, 2, 2): [
            "enfant-f|Plus tard.",
            "enfant-m|D'accord.",
            "narrateur|Amir laisse le galet dans le filet.",
            "enfant-m|Je te le garde mouillé.",
            "narrateur|Nina recule d'une vague, puis s'arrête.",
            "papa|Les mailles tiennent la pierre.",
            "narrateur|Une goutte de sel perle encore.",
        ],
        (2, 2, 3): [
            "enfant-f|Non.",
            "enfant-m|D'accord.",
            "narrateur|Amir pose le galet du filet, tout seul.",
            "narrateur|La ligne va jusqu'à l'ombre, presque.",
            "maman|L'écume n'a plus ce galet.",
            "narrateur|Nina joue avec une vague, plus loin.",
            "narrateur|Le filet sèche, tout plat.",
        ],
        (2, 3, 1): [
            "enfant-f|Je regarde.",
            "enfant-m|D'accord.",
            "narrateur|Amir montre le gris du livre, du doigt.",
            "narrateur|Nina compare, des yeux, avec la pierre.",
            "papa|C'est le même gris.",
            "narrateur|Le galet plat tient encore la page.",
        ],
        (2, 3, 2): [
            "enfant-f|Plus tard.",
            "enfant-m|D'accord.",
            "narrateur|Amir laisse le livre ouvert, sous le galet.",
            "enfant-m|Le gris t'attend.",
            "narrateur|Nina s'éloigne le long de l'eau.",
            "maman|Le vent n'emporte plus la page.",
            "narrateur|Le dessin reste au soleil, tout calme.",
        ],
        (2, 3, 3): [
            "enfant-f|Non.",
            "enfant-m|D'accord.",
            "narrateur|Amir choisit le gris, tout seul, dans le sable.",
            "narrateur|Il le pose en tête du chemin.",
            "papa|Le livre a assez montré.",
            "narrateur|Nina a déjà tourné le dos, vers la mer.",
            "narrateur|La page se referme, presque.",
        ],
        (3, 1, 1): [
            "enfant-f|Je regarde.",
            "enfant-m|D'accord.",
            "narrateur|Amir s'assoit dans le rond, près du seau.",
            "narrateur|Nina reste au bord, les yeux sur la toile.",
            "papa|Le pied ne bouge plus.",
            "narrateur|L'ombre couvre les genoux d'Amir.",
        ],
        (3, 1, 2): [
            "enfant-f|Plus tard.",
            "enfant-m|D'accord.",
            "narrateur|Amir laisse un coin d'ombre, tout vide.",
            "enfant-m|Ta place est fraîche.",
            "narrateur|Nina recule au soleil, un moment.",
            "maman|Le seau tient encore le pied.",
            "narrateur|Un bout de serviette attend, à l'ombre.",
        ],
        (3, 1, 3): [
            "enfant-f|Non.",
            "enfant-m|D'accord.",
            "narrateur|Amir s'assoit tout seul, sous le jaune.",
            "narrateur|Le seau reste lourd, sur le pied.",
            "papa|Le rond lui suffit, ce matin.",
            "narrateur|Nina marche au soleil, tout près.",
            "narrateur|La toile ne claque plus.",
        ],
        (3, 2, 1): [
            "enfant-f|Je regarde.",
            "enfant-m|D'accord.",
            "narrateur|Amir s'allonge sous les mailles rayées.",
            "narrateur|Nina suit la goutte, jusqu'au sable.",
            "maman|Elle tombe, tout lent.",
            "narrateur|Le filet fait une ombre étroite, tout nette.",
        ],
        (3, 2, 2): [
            "enfant-f|Plus tard.",
            "enfant-m|D'accord.",
            "narrateur|Amir laisse le filet tendu, pour elle.",
            "enfant-m|Le second toit t'attend.",
            "narrateur|Nina s'éloigne vers la flaque, un instant.",
            "papa|Les mailles sèchent, tout salées.",
            "narrateur|Une ombre rayée reste sur le sable.",
        ],
        (3, 2, 3): [
            "enfant-f|Non.",
            "enfant-m|D'accord.",
            "narrateur|Amir reste sous le filet, tout seul.",
            "narrateur|La goutte a déjà séché, en rond.",
            "maman|Les mailles suffisent, pour lui.",
            "narrateur|Nina court un peu, hors de l'ombre.",
            "narrateur|Le filet ne bouge plus, ou presque.",
        ],
        (3, 3, 1): [
            "enfant-f|Je regarde.",
            "enfant-m|D'accord.",
            "narrateur|Amir lit le crabe, tout bas, pour les deux.",
            "narrateur|Nina écoute depuis le bord de l'ombre.",
            "papa|La page ne s'envole plus.",
            "narrateur|Le doigt d'Amir tient encore le coin.",
        ],
        (3, 3, 2): [
            "enfant-f|Plus tard.",
            "enfant-m|D'accord.",
            "narrateur|Amir laisse le livre ouvert, sur les genoux.",
            "enfant-m|Le crabe t'attend.",
            "narrateur|Nina part vers l'eau, puis se retourne.",
            "maman|Le vent n'a plus la page.",
            "narrateur|Un coin d'ombre reste libre, à côté.",
        ],
        (3, 3, 3): [
            "enfant-f|Non.",
            "enfant-m|D'accord.",
            "narrateur|Amir referme presque le livre, tout doux.",
            "narrateur|Il garde le crabe pour lui, un moment.",
            "papa|La page se tait.",
            "narrateur|Nina est déjà hors du rond, au soleil.",
            "narrateur|Le parasol jaune ne tremble plus.",
        ],
    }
    return vet(suite[(i, j, k)])


FIN = {
    (1, 1, 1): [
        "narrateur|La tour a bu, et elle tient.",
        "narrateur|Nina est encore là, les yeux ouverts.",
        "enfant-m|Tu as vu l'eau.",
        "enfant-f|Oui.",
        "maman|Le château a une petite ombre, maintenant.",
        "papa|Merci, Amir.",
        "narrateur|Ils se reculent sous le parasol jaune.",
        "narrateur|Le seau sèche, tout rouge, à leurs pieds.",
        "narrateur|La mer chuchote encore, tout bas.",
    ],
    (1, 1, 2): [
        "narrateur|Nina revient, les joues un peu salées.",
        "enfant-f|Maintenant ?",
        "enfant-m|Oui.",
        "enfant-m|Le seau est encore là.",
        "narrateur|Elle verse une gorgée, tout maladroite.",
        "papa|Vous avez pris le temps.",
        "maman|Merci, tous les deux.",
        "narrateur|Ils s'assoient dans le rond jaune.",
        "narrateur|L'eau du château ne coule plus.",
    ],
    (1, 1, 3): [
        "narrateur|La petite tour reste ferme, toute seule.",
        "enfant-m|Elle a bu.",
        "papa|Oui.",
        "narrateur|Nina fait des ronds, plus loin, dans l'eau.",
        "maman|Le château t'attend sous le parasol.",
        "enfant-m|J'y vais.",
        "narrateur|Amir s'assoit dans le rond frais.",
        "narrateur|Le seau vide penche, puis se tient.",
        "narrateur|Une coquille brille dans la flaque.",
    ],
    (1, 2, 1): [
        "narrateur|La motte a rejoint la colline.",
        "narrateur|Nina n'a pas touché, et elle a tout vu.",
        "enfant-m|C'est mouillé, maintenant.",
        "enfant-f|Oui.",
        "papa|Le filet a travaillé.",
        "maman|Merci, Amir.",
        "narrateur|Ils gagnent l'ombre du parasol, tout lents.",
        "narrateur|Les mailles sèchent, étendues au soleil.",
        "narrateur|Le grain ne vole plus.",
    ],
    (1, 2, 2): [
        "narrateur|Nina revient avec la coquille.",
        "enfant-f|Je tiens le manche ?",
        "enfant-m|Oui.",
        "narrateur|Le filet glisse un peu, puis elle le tient.",
        "papa|Vous avez attendu le bon moment.",
        "maman|Merci.",
        "narrateur|Une dernière motte rejoint la tour.",
        "narrateur|Ils s'abritent sous le jaune, après.",
        "narrateur|Le sel sèche sur leurs mains.",
    ],
    (1, 2, 3): [
        "narrateur|La petite tour ronde reste chaude.",
        "enfant-m|Je l'ai tassée.",
        "maman|Oui.",
        "narrateur|Nina court dans l'écume, plus loin.",
        "papa|Le filet peut sécher, maintenant.",
        "narrateur|Amir le pose au pied du parasol.",
        "narrateur|Il s'assoit dans le rond, tout calme.",
        "narrateur|Les mailles ne bougent plus.",
    ],
    (1, 3, 1): [
        "narrateur|Deux pinces de sable tiennent, tout droites.",
        "narrateur|Nina a suivi le dessin, jusqu'au bout.",
        "enfant-m|Comme le crabe.",
        "enfant-f|Oui.",
        "papa|Le livre a aidé.",
        "maman|Merci, Amir.",
        "narrateur|Ils ferment la page, sous le parasol.",
        "narrateur|Le château crabe garde son ombre courte.",
        "narrateur|Un coin de page n'est plus mouillé.",
    ],
    (1, 3, 2): [
        "narrateur|Nina revient, les pieds sablés.",
        "enfant-f|Le crabe ?",
        "enfant-m|Il est encore sur la page.",
        "narrateur|Elle s'agenouille, enfin, près du livre.",
        "papa|Vous avez lu le dessin, plus tard.",
        "maman|Merci.",
        "narrateur|Une pince s'ajoute, tout douce.",
        "narrateur|Puis ils gagnent le rond jaune.",
        "narrateur|Le pli du livre n'a plus de sable.",
    ],
    (1, 3, 3): [
        "narrateur|Le petit crabe de sable reste seul.",
        "enfant-m|Il me ressemble un peu.",
        "papa|Un peu.",
        "narrateur|Nina a déjà rejoint l'eau, tout loin.",
        "maman|Le livre peut se fermer, maintenant.",
        "narrateur|Amir le pose à l'ombre, sur la serviette.",
        "narrateur|Il s'allonge dans le rond frais.",
        "narrateur|La page ne claque plus.",
    ],
    (2, 1, 1): [
        "narrateur|La file de galets touche presque l'ombre.",
        "narrateur|Nina a tout compté, sans rien poser.",
        "enfant-m|On peut marcher dessus.",
        "enfant-f|J'ai vu.",
        "papa|Pierre par pierre.",
        "maman|Merci, Amir.",
        "narrateur|Ils suivent la file, jusqu'au parasol.",
        "narrateur|Le seau vide reste au départ, tout rouge.",
        "narrateur|Les galets tiennent, encore froids.",
    ],
    (2, 1, 2): [
        "narrateur|Nina revient, un pied encore mouillé.",
        "enfant-f|Le mien ?",
        "enfant-m|Il t'attend.",
        "narrateur|Elle pose le galet, tout maladroit, en ligne.",
        "papa|Vous avez fini le chemin.",
        "maman|Merci, tous les deux.",
        "narrateur|La file arrive sous le parasol jaune.",
        "narrateur|Ils s'assoient, les galets à leurs pieds.",
        "narrateur|Le seau ne sonne plus.",
    ],
    (2, 1, 3): [
        "narrateur|La petite file s'arrête, assez longue.",
        "enfant-m|Elle va vers l'ombre.",
        "papa|Oui.",
        "narrateur|Nina éclabousse, plus loin, tout légère.",
        "maman|Les galets te mènent au parasol.",
        "narrateur|Amir marche dessus, un pas, puis deux.",
        "narrateur|Il s'assoit dans le rond, tout seul.",
        "narrateur|Le seau reste penché, au soleil.",
    ],
    (2, 2, 1): [
        "narrateur|Le galet du filet brille encore, tout salé.",
        "narrateur|Nina a vu la goutte, jusqu'au bout.",
        "enfant-m|Il vient de la mer.",
        "enfant-f|Oui.",
        "papa|Les mailles l'ont bien tenu.",
        "maman|Merci, Amir.",
        "narrateur|La ligne rejoint le pied du parasol.",
        "narrateur|Ils s'assoient, le filet égoutté entre eux.",
        "narrateur|Une dernière goutte sèche sur le sable.",
    ],
    (2, 2, 2): [
        "narrateur|Nina revient quand la vague s'en va.",
        "enfant-f|Il est encore mouillé ?",
        "enfant-m|Oui.",
        "narrateur|Elle tire le galet des mailles, tout doux.",
        "papa|Vous l'avez gardé pour plus tard.",
        "maman|Merci.",
        "narrateur|Elle le pose, et la ligne touche l'ombre.",
        "narrateur|Ils s'abritent sous le jaune, après.",
        "narrateur|Le filet s'affaisse, vide.",
    ],
    (2, 2, 3): [
        "narrateur|Le galet de l'écume est en place.",
        "enfant-m|Presque jusqu'à l'ombre.",
        "maman|C'est assez.",
        "narrateur|Nina saute une vague, plus loin.",
        "papa|Le filet peut sécher au pied.",
        "narrateur|Amir le tend sous le parasol.",
        "narrateur|Il s'assoit dans le rond, les genoux frais.",
        "narrateur|Les mailles ne gouttent plus.",
    ],
    (2, 3, 1): [
        "narrateur|Le gris du livre et le vrai se touchent.",
        "narrateur|Nina a comparé, jusqu'au bout des yeux.",
        "enfant-m|Le même.",
        "enfant-f|Oui.",
        "papa|La page a montré le chemin.",
        "maman|Merci, Amir.",
        "narrateur|Ils ferment le livre sous le parasol.",
        "narrateur|Le galet plat rejoint la file, tout simple.",
        "narrateur|Le vent n'a plus rien à tourner.",
    ],
    (2, 3, 2): [
        "narrateur|Nina revient le long de l'eau.",
        "enfant-f|Le gris ?",
        "enfant-m|Il est sur la page, encore.",
        "narrateur|Elle choisit enfin une pierre, tout près.",
        "papa|Vous l'avez choisie plus tard.",
        "maman|Merci.",
        "narrateur|La file arrive à l'ombre, complète.",
        "narrateur|Ils s'assoient, le livre fermé entre eux.",
        "narrateur|Le galet plat ne sert plus de poids.",
    ],
    (2, 3, 3): [
        "narrateur|Le gris d'Amir ouvre le chemin, tout seul.",
        "enfant-m|Le livre a montré, c'est tout.",
        "papa|Oui.",
        "narrateur|Nina a le dos à la mer, déjà loin.",
        "maman|Tu peux fermer la page.",
        "narrateur|Amir la pose à l'ombre, sur la serviette.",
        "narrateur|Il s'assoit dans le rond jaune.",
        "narrateur|Le vent passe, sans emporter le papier.",
    ],
    (3, 1, 1): [
        "narrateur|Le seau tient encore le pied, tout lourd.",
        "narrateur|Nina a regardé la toile, sans s'asseoir.",
        "enfant-m|L'ombre est à nous.",
        "enfant-f|Je l'ai vue.",
        "papa|Elle ne saute plus.",
        "maman|Merci, Amir.",
        "narrateur|Le rond jaune couvre leurs deux ombres.",
        "narrateur|Même Nina, au bord, a les orteils au frais.",
        "narrateur|La chaise de papa ne craque plus.",
    ],
    (3, 1, 2): [
        "narrateur|Nina revient, le front un peu chaud.",
        "enfant-f|Ma place ?",
        "enfant-m|Elle est encore fraîche.",
        "narrateur|Elle s'assoit, enfin, contre le seau.",
        "papa|Vous avez gardé le rond.",
        "maman|Merci, tous les deux.",
        "narrateur|Le parasol jaune ne penche plus.",
        "narrateur|Leurs genoux se touchent, à l'ombre.",
        "narrateur|Un peu de sable reste sous le pied.",
    ],
    (3, 1, 3): [
        "narrateur|Le seau reste lourd, et le rond tient.",
        "enfant-m|Pour moi, c'est assez.",
        "papa|Oui.",
        "narrateur|Nina marche au soleil, tout près, sans entrer.",
        "maman|L'ombre t'appartient, ce matin.",
        "narrateur|Amir s'allonge, les yeux sous la toile.",
        "narrateur|Un carré jaune danse sur sa joue.",
        "narrateur|Le plastique du seau reste froid.",
    ],
    (3, 2, 1): [
        "narrateur|L'ombre rayée a recouvert le sable.",
        "narrateur|Nina a vu la goutte, jusqu'au rond sec.",
        "enfant-m|Deux toits.",
        "enfant-f|Oui.",
        "papa|Le filet a aidé la toile.",
        "maman|Merci, Amir.",
        "narrateur|Ils restent sous les mailles, un moment.",
        "narrateur|Le sel a séché, tout blanc, sur le fil.",
        "narrateur|La mer parle plus bas, maintenant.",
    ],
    (3, 2, 2): [
        "narrateur|Nina revient vers les mailles.",
        "enfant-f|Le second toit ?",
        "enfant-m|Il t'attend.",
        "narrateur|Elle passe la tête sous le filet, tout doux.",
        "papa|Vous l'avez tendu pour plus tard.",
        "maman|Merci.",
        "narrateur|Deux ombres rayées se mêlent, au frais.",
        "narrateur|Le parasol jaune tient le premier toit.",
        "narrateur|Une maille ne goutte plus.",
    ],
    (3, 2, 3): [
        "narrateur|Le filet garde son ombre étroite, pour Amir.",
        "enfant-m|Ça suffit.",
        "maman|Oui.",
        "narrateur|Nina court hors des mailles, tout légère.",
        "papa|Tu as un toit, à toi.",
        "narrateur|Amir s'allonge, les rayures sur les bras.",
        "narrateur|Le rond jaune et le filet se tiennent.",
        "narrateur|Plus aucune goutte ne tombe.",
    ],
    (3, 3, 1): [
        "narrateur|Le crabe du livre a fini sa page.",
        "narrateur|Nina a écouté, depuis le bord.",
        "enfant-m|Tu as entendu.",
        "enfant-f|Oui.",
        "papa|La page n'est plus partie.",
        "maman|Merci, Amir.",
        "narrateur|Ils laissent le livre ouvert, à l'ombre.",
        "narrateur|Le parasol jaune couvre encore le papier.",
        "narrateur|Un coin de page ne tremble plus.",
    ],
    (3, 3, 2): [
        "narrateur|Nina revient, une goutte d'eau aux cheveux.",
        "enfant-f|Le crabe ?",
        "enfant-m|Il est encore là.",
        "narrateur|Elle s'assoit, enfin, contre le livre.",
        "papa|Vous l'avez lu plus tard.",
        "maman|Merci.",
        "narrateur|Amir recommence la page, tout bas.",
        "narrateur|Le rond jaune les tient tous les deux.",
        "narrateur|Le vent passe au-dessus, sans tourner.",
    ],
    (3, 3, 3): [
        "narrateur|Le livre reste presque fermé, sur les genoux.",
        "enfant-m|Le crabe est à moi, un moment.",
        "papa|Oui.",
        "narrateur|Nina est hors du rond, déjà sèche.",
        "maman|L'ombre te va, toute seule.",
        "narrateur|Amir pose la page contre sa chemise.",
        "narrateur|Le parasol jaune ne tremble plus.",
        "narrateur|La mer reprend son chuchotement, tout bas.",
    ],
}


def t3_fin(i: int, j: int, k: int) -> list[str]:
    return vet(FIN[(i, j, k)])


def main() -> None:
    s: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}

    s["CHK_T0000_P0000"] = vet(
        [
            "narrateur|Le parasol jaune tremble au vent, tout léger.",
            "narrateur|Un rond d'ombre dort sur le sable.",
            "narrateur|Une coquille de crabe attend dans une flaque.",
            "narrateur|L'eau de la flaque est tiède.",
            "narrateur|La mer chuchote, tout bas.",
            "narrateur|Papa déplie une chaise, près de la toile.",
            "papa|La toile craque un peu.",
            "maman|J'étale la serviette à carreaux.",
            "papa|Tu entends la mer, Amir ?",
            "enfant-m|Oui.",
            "enfant-m|Elle chuchote.",
            "maman|La flaque sent le sel.",
            "narrateur|Nina marche au bord de l'eau.",
            "narrateur|Ses pieds laissent des ronds, tout clairs.",
            "narrateur|En ce moment, Amir veut ce rond d'ombre.",
            "enfant-m|Je veux m'asseoir dessous.",
            "enfant-m|Avec Nina.",
            "papa|Tu l'invites ?",
            "enfant-m|Oui, papa.",
            "maman|Elle est près de l'eau.",
            "narrateur|Le parasol penche, puis se tient.",
            "narrateur|La coquille reste dans l'eau tiède.",
        ]
    )
    sons["CHK_T0000_P0000"] = "vague,oiseau"

    s["CHK_T0001_P0000"] = vet(
        [
            "narrateur|Trois coins de plage attendent, sous le soleil.",
            "papa|Le sable, les galets, ou l'ombre ?",
            "maman|Où commences-tu, Amir ?",
        ]
    )
    extras["CHK_T0001_P0000"] = t3lab("le sable", "les galets", "l'ombre")
    sons["CHK_T0001_P0000"] = ""

    q_extra = {
        1: qf(
            LIEU[1]["q_ans"],
            LIEU[1]["q_acc"],
            LIEU[1]["q_retry"],
        ),
        2: qf(
            LIEU[2]["q_ans"],
            LIEU[2]["q_acc"],
            LIEU[2]["q_retry"],
        ),
        3: qf(
            LIEU[3]["q_ans"],
            LIEU[3]["q_acc"],
            LIEU[3]["q_retry"],
        ),
    }

    for i, lieu in LIEU.items():
        p = f"CHK_T0001_P000{i}"
        s[p] = t1_pass(i)
        sons[p] = lieu["son"]
        s[f"{p}_Q0001"] = t1_q(i)
        extras[f"{p}_Q0001"] = q_extra[i]
        s[f"{p}_C0001"] = t1_c(i)
        s[f"{p}_T0002_P0000"] = t2_trans(i)
        extras[f"{p}_T0002_P0000"] = t3lab("le seau", "le filet", "le livre")
        for j, obj in OBJ.items():
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = t2_pass(i, j)
            sons[p2] = obj["son"]
            s[f"{p2}_T0003_P0000"] = t3_trans(j)
            extras[f"{p2}_T0003_P0000"] = t3lab("regarder", "plus tard", "un non")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = t3_pass(i, j, k)
                s[f"{p3}_F0001"] = t3_fin(i, j, k)

    write_tree(s, sons, extras)
    relecture(
        SID,
        "Le parasol jaune et la réponse d'Amir",
        "parasol jaune, rond d'ombre, château / chemin de galets / ombre tenue, "
        "seau filet livre, Nina regarde / plus tard / non, Amir dit d'accord",
        "Nora hors troupe. Héros Amir, Nina copine, papa/maman. "
        "Gabarit slogan (on propose / on accepte plusieurs réponses) jeté. "
        "Q concrets (sable, galets, jaune). T1 change le voyage. "
        "Leçon BES.002 vécue, pas dite. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
