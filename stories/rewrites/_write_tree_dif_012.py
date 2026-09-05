#!/usr/bin/env python3
"""TREE-DIF-012 — La pomme verte et les pieds d'Amir (N1, F-NAR-018)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-012"
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
        "Sous le pommier, Amir veut la pomme verte qui tremble tout en haut. "
        "Ses pieds dansent. Il choisit un chemin : bac, toboggan ou balançoires. "
        "Puis une affaire du jardin : caisse, arrosoir ou chapeau. "
        "Papa le porte, un vent passe, ou maman incline la branche. "
        "Amir croque. Le jus sucré tient la promesse."
    )
    out["title"] = "La pomme verte et les pieds d'Amir"
    out["characters"] = "Amir, papa, maman"
    out["setting"] = "le jardin, sous le pommier"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "ce n'est pas une faute",
        "beaucoup d'énergie",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "sami",
        "nino",
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


LIEU = {
    1: {
        "lab": "le bac à sable",
        "ou": "près du bac",
        "sol": "Le sable tiède colle encore.",
        "trace": "un grain de sable",
        "bruit": "Sous les pieds, le sable chuchote.",
        "coda": "Un trou rond reste dans le bac.",
        "q_ans": "pomme",
        "q_acc": "pomme | la pomme | pomme verte | la verte | une pomme",
        "q_retry": "Amir veut la pomme verte. Il veut quoi ?",
        "q_ask": "Il saute vers quoi ?",
        "q_lead": "Amir saute sous l'ombre ronde.",
    },
    2: {
        "lab": "le toboggan",
        "ou": "près du toboggan",
        "sol": "Le métal reste chaud, un peu.",
        "trace": "une poussière de métal",
        "bruit": "Un petit toc reste dans le métal.",
        "coda": "Vide et chaud, le toboggan se tait.",
        "q_ans": "pomme",
        "q_acc": "pomme | la pomme | pomme verte | la verte | une pomme",
        "q_retry": "Du haut, Amir veut la pomme. Il veut quoi ?",
        "q_ask": "Il tend la main vers quoi ?",
        "q_lead": "Du haut, Amir tend la main.",
    },
    3: {
        "lab": "les balançoires",
        "ou": "près des balançoires",
        "sol": "Un brin d'herbe reste au mollet.",
        "trace": "un brin d'herbe",
        "bruit": "Puis la chaîne se tait, tout doux.",
        "coda": "Plus aucun cri sur la chaîne.",
        "q_ans": "pomme",
        "q_acc": "pomme | la pomme | pomme verte | la verte | une pomme",
        "q_retry": "Sous la chaîne, c'est la pomme. Il veut quoi ?",
        "q_ask": "Il veut quoi, tout en haut ?",
        "q_lead": "Amir lève le nez, sous la chaîne.",
    },
}

OUTIL = {
    1: {"lab": "la caisse", "cap": "La caisse", "le": "la caisse"},
    2: {"lab": "l'arrosoir", "cap": "L'arrosoir", "le": "l'arrosoir"},
    3: {"lab": "le chapeau", "cap": "Le chapeau", "le": "le chapeau"},
}

T3_LABS = {
    1: ("les bras de papa", "mes pieds sages", "on pousse"),
    2: ("les bras de papa", "j'attends", "maman penche"),
    3: ("papa secoue", "un petit vent", "maman incline"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Amir court vers le bac à sable.",
            "narrateur|Le sable est tiède, un peu rêche.",
            "enfant-m|L'ombre de la pomme est ici !",
            "narrateur|Il saute, et un nuage s'élève.",
            "narrateur|Un grain colle à son genou.",
            "enfant-m|Attends, je viens !",
            "narrateur|Sa main n'arrive pas.",
            "maman|Tes pieds dansent, tout forts.",
            "papa|La pomme, elle, reste sage.",
            "enfant-m|Je la veux quand même.",
            "narrateur|La feuille collée tremble encore.",
            "maman|On la cherche d'ici, alors ?",
        )
    if t1 == 2:
        return L(
            "narrateur|Amir court vers le toboggan.",
            "narrateur|Le métal est chaud, un peu lisse.",
            "enfant-m|Plus haut, je l'attrape !",
            "narrateur|Il grimpe les marches, tout vite.",
            "narrateur|Ses pieds tapent, toc toc.",
            "papa|Doucement, les marches sont chaudes.",
            "narrateur|Du haut, la pomme paraît plus près.",
            "enfant-m|Presque !",
            "narrateur|Sa main frotte l'air, rien.",
            "maman|Tes pieds veulent encore sauter.",
            "enfant-m|Je la veux, celle-là.",
            "papa|On reste un moment, ici ?",
        )
    return L(
        "narrateur|Amir court vers les balançoires.",
        "narrateur|La chaîne est froide, un peu rêche.",
        "enfant-m|Elle est juste au-dessus !",
        "narrateur|Il s'assoit, et ses pieds partent.",
        "narrateur|La chaîne chante un petit cri.",
        "maman|Tes pieds font voler le siège.",
        "papa|La pomme danse avec toi, là-haut.",
        "enfant-m|Je l'attrape en l'air !",
        "narrateur|Sa main claque le vide, tout près.",
        "narrateur|La pomme revient, trop haute.",
        "enfant-m|Encore !",
        "papa|On cherche un autre geste ?",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Oui, la pomme verte, tout en haut.",
            "enfant-m|Mes pieds n'y arrivent pas.",
            "papa|Une affaire du jardin, peut-être ?",
            "maman|La caisse, l'arrosoir, ou le chapeau.",
            "enfant-m|Pour l'atteindre.",
            "narrateur|Un grain de sable reste au genou.",
        )
    if t1 == 2:
        return L(
            "narrateur|Oui, c'est la pomme, tout en haut.",
            "enfant-m|Du haut, ma main est trop courte.",
            "maman|On prend une affaire, alors ?",
            "papa|La caisse, l'arrosoir, ou le chapeau.",
            "enfant-m|Oui, pour elle.",
            "narrateur|Le métal garde un toc, encore.",
        )
    return L(
        "narrateur|Oui, la pomme, au-dessus de la chaîne.",
        "enfant-m|Mes pieds volent, mais pas assez.",
        "papa|Une affaire du jardin, avec nous ?",
        "maman|La caisse, l'arrosoir, ou le chapeau.",
        "enfant-m|Je choisis.",
        "narrateur|La chaîne se balance, puis ralentit.",
    )


def t2_question(t1: int) -> list[str]:
    if t1 == 1:
        lead = "narrateur|Le bac n'atteint pas la pomme."
    elif t1 == 2:
        lead = "narrateur|Le toboggan n'atteint pas la pomme."
    else:
        lead = "narrateur|La balançoire n'atteint pas la pomme."
    return L(
        lead,
        "narrateur|La caisse sent encore le jus.",
        "narrateur|L'arrosoir goutte, tout près.",
        "narrateur|Le chapeau attend au clou.",
        "papa|Tu prends quoi, pour l'atteindre ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    key = (t1, t2)
    if key == (1, 1):
        return L(
            "narrateur|Amir tire la caisse sur le sable.",
            "enfant-m|Je monte, et je l'ai !",
            "narrateur|Il grimpe, et ses pieds dansent.",
            "narrateur|La caisse s'enfonce, tout mou.",
            "papa|Elle penche, avec tes pieds.",
            "enfant-m|Attends, pomme !",
            "narrateur|Sa main frôle la feuille collée.",
            "maman|Le sable mange la caisse, un peu.",
            "narrateur|La pomme reste, trop haute.",
            "enfant-m|Elle est encore loin.",
            "papa|On fait comment, avec la caisse ?",
        )
    if key == (1, 2):
        return L(
            "narrateur|Amir pose l'arrosoir sur le sable.",
            "enfant-m|Je monte dessus, tout petit.",
            "narrateur|Ses pieds tapent le métal, toc.",
            "narrateur|L'eau saute, une flaque ronde.",
            "maman|Tes pieds ont donné un coup.",
            "papa|L'arrosoir a glissé, tout seul.",
            "enfant-m|La pomme, elle, n'a pas bougé.",
            "narrateur|Une goutte brille sur le grain.",
            "narrateur|La feuille collée tremble à peine.",
            "enfant-m|Il est trop petit, l'arrosoir.",
            "papa|On le tient comment, alors ?",
        )
    if key == (1, 3):
        return L(
            "narrateur|Amir pose le chapeau sur le sable.",
            "enfant-m|Tombe dedans, pomme verte !",
            "narrateur|Il saute autour, pieds tout vifs.",
            "narrateur|Le chapeau se remplit de sable.",
            "maman|C'est un nid, mais plein de grains.",
            "papa|La pomme n'a pas vu le nid.",
            "enfant-m|Je saute plus fort !",
            "narrateur|La branche tremble, puis s'arrête.",
            "narrateur|Le chapeau reste vide, tout sablé.",
            "enfant-m|Elle n'est pas venue.",
            "maman|On l'aide, cette pomme ?",
        )
    if key == (2, 1):
        return L(
            "narrateur|Amir hisse la caisse en haut.",
            "enfant-m|Encore plus haut, maintenant !",
            "narrateur|Il pose un pied, puis l'autre.",
            "narrateur|Le métal sonne sous le bois.",
            "papa|La caisse penche, sur la marche.",
            "enfant-m|Je l'ai presque !",
            "narrateur|Ses pieds dansent, et ça vacille.",
            "maman|Tiens le bord, Amir.",
            "narrateur|Sa main manque la pomme, encore.",
            "enfant-m|Elle rit, là-haut.",
            "papa|On la reprend comment, la caisse ?",
        )
    if key == (2, 2):
        return L(
            "narrateur|Amir pose l'arrosoir en bas.",
            "enfant-m|Si elle tombe, je l'attrape !",
            "narrateur|Il glisse, pieds tout vite.",
            "narrateur|Toc, contre le bec de l'arrosoir.",
            "maman|L'eau a fait une ligne brillante.",
            "papa|Tes pieds l'ont rencontré, trop fort.",
            "enfant-m|Je voulais juste l'attendre.",
            "narrateur|La pomme n'est pas tombée.",
            "narrateur|L'arrosoir roule d'un pouce, puis s'arrête.",
            "enfant-m|Il n'est plus sous elle.",
            "papa|On le remet, tout calme ?",
        )
    if key == (2, 3):
        return L(
            "narrateur|Amir pose le chapeau en bas.",
            "enfant-m|Un nid, pour quand elle vient !",
            "narrateur|Il regarde du haut, pieds impatients.",
            "narrateur|Le chapeau attend, tout plat.",
            "maman|Tes pieds veulent déjà redescendre.",
            "papa|La pomme, elle, n'a pas bougé.",
            "enfant-m|Je saute dans le nid !",
            "narrateur|Il s'arrête au bord, un souffle.",
            "narrateur|Le chapeau reste vide, en bas.",
            "enfant-m|Elle ne veut pas tomber.",
            "maman|On l'invite, autrement ?",
        )
    if key == (3, 1):
        return L(
            "narrateur|Amir glisse la caisse sous le siège.",
            "enfant-m|Je monte, puis je m'envole !",
            "narrateur|Il se hausse, et ses pieds tapent.",
            "narrateur|La caisse recule d'un cran, dans l'herbe.",
            "papa|Elle part, avec tes pieds.",
            "enfant-m|Reviens, caisse !",
            "narrateur|La chaîne chante, et la pomme danse.",
            "maman|Le siège va, la caisse non.",
            "narrateur|Sa main manque encore la feuille.",
            "enfant-m|C'est trop loin, encore.",
            "papa|On tient la caisse, comment ?",
        )
    if key == (3, 2):
        return L(
            "narrateur|Amir pose l'arrosoir sur ses genoux.",
            "enfant-m|Je l'attrape en volant !",
            "narrateur|Il se balance, et l'eau gicle.",
            "narrateur|Une goutte mouille son genou.",
            "maman|Tes pieds donnent trop d'élan.",
            "papa|L'arrosoir n'aime pas le vent.",
            "enfant-m|La pomme, elle, se balance aussi.",
            "narrateur|Ils dansent ensemble, trop loin.",
            "narrateur|Le bec reste vide, tout creux.",
            "enfant-m|Elle n'est pas rentrée.",
            "papa|On arrête les pieds, un peu ?",
        )
    return L(
        "narrateur|Amir pose le chapeau sur l'autre siège.",
        "enfant-m|Toi tu attends, chapeau !",
        "narrateur|Il se balance vers la pomme.",
        "narrateur|Ses pieds volent, tout contents.",
        "maman|Le chapeau, lui, reste sage.",
        "papa|La pomme passe au-dessus, encore.",
        "enfant-m|Viens, viens !",
        "narrateur|Sa main claque l'air, tout près.",
        "narrateur|Le chapeau attend, vide et calme.",
        "enfant-m|Elle n'a pas voulu.",
        "maman|On l'aide à descendre ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|La caisse n'a pas suffi, toute seule.",
            "papa|Mes bras, tes pieds sages, ou on pousse ?",
        )
    if t2 == 2:
        return L(
            "narrateur|L'arrosoir n'a pas cueilli la pomme.",
            "maman|Papa te porte, tu attends, ou je penche ?",
        )
    return L(
        "narrateur|Le chapeau attend encore, tout vide.",
        "papa|Je secoue, un vent, ou maman incline ?",
    )


def _t1_color(t1: int, kind: str) -> str:
    li = LIEU[t1]
    if kind == "sol":
        return f"narrateur|{li['sol']}"
    if kind == "bruit":
        return f"narrateur|{li['bruit']}"
    if kind == "trace":
        return f"narrateur|{li['trace'].capitalize()} reste un moment."
    return f"narrateur|{li['coda']}"


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    sol = _t1_color(t1, "sol")
    if t2 == 1 and t3 == 1:
        hold = {
            1: "narrateur|Papa cale la caisse dans le sable.",
            2: "narrateur|Papa cale la caisse sur la marche.",
            3: "narrateur|Papa cale la caisse dans l'herbe.",
        }[t1]
        return L(
            "enfant-m|Papa, porte-moi un peu.",
            "papa|Je te tiens, Amir.",
            hold,
            "narrateur|Amir se hausse, pieds tout calmes.",
            "narrateur|Sa main touche la pomme verte.",
            "enfant-m|Elle est à moi !",
            "narrateur|La feuille collée vient avec.",
            "maman|Tu l'as cueillie, tout doux.",
            sol,
        )
    if t2 == 1 and t3 == 2:
        wait = {
            1: "narrateur|Le sable cesse de manger la caisse.",
            2: "narrateur|Le métal cesse de sonner.",
            3: "narrateur|L'herbe cesse de glisser.",
        }[t1]
        return L(
            "enfant-m|Mes pieds, restez sages.",
            "narrateur|Il attend, et les pieds s'arrêtent.",
            wait,
            "narrateur|La caisse ne penche plus.",
            "enfant-m|Maintenant, tout doux.",
            "narrateur|Il se hausse, un seul geste.",
            "narrateur|La pomme vient dans sa paume.",
            "papa|Tes pieds ont attendu, cette fois.",
            "maman|Elle est verte, et à toi.",
        )
    if t2 == 1 and t3 == 3:
        push = {
            1: "narrateur|Ils poussent la caisse sous l'ombre.",
            2: "narrateur|Ils poussent la caisse au pied.",
            3: "narrateur|Ils poussent la caisse sous la chaîne.",
        }[t1]
        return L(
            "enfant-m|On pousse, tous les trois !",
            push,
            "maman|J'incline la branche, un peu.",
            "narrateur|La pomme descend, tout lent.",
            "enfant-m|Dans la caisse !",
            "narrateur|Ploc, un jus mince sur le bois.",
            "papa|Vous l'avez faite venir.",
            sol,
            "narrateur|La feuille collée brille encore.",
        )
    if t2 == 2 and t3 == 1:
        lift = {
            1: "narrateur|Papa soulève Amir au-dessus du bac.",
            2: "narrateur|Papa soulève Amir près du métal.",
            3: "narrateur|Papa soulève Amir sous la chaîne.",
        }[t1]
        return L(
            "enfant-m|Papa, plus haut, s'il te plaît.",
            "papa|Je te porte, tiens l'arrosoir.",
            lift,
            "narrateur|Amir cueille, et la pomme glisse au bec.",
            "enfant-m|Elle est dedans !",
            "narrateur|Une goutte d'eau la lave, tout petit.",
            "maman|Tes pieds pendent, tout sages.",
            sol,
            "narrateur|Le bec garde un rond vert.",
        )
    if t2 == 2 and t3 == 2:
        still = {
            1: "narrateur|Le sable ne vole plus.",
            2: "narrateur|Le métal ne sonne plus.",
            3: "narrateur|La chaîne ne chante plus.",
        }[t1]
        return L(
            "enfant-m|J'attends, pieds sages.",
            "narrateur|Il pose l'arrosoir juste dessous.",
            still,
            "maman|On laisse le vent travailler.",
            "narrateur|La feuille tremble, puis s'en va.",
            "narrateur|La pomme lâche, tout doux.",
            "enfant-m|Ploc !",
            "papa|Elle est venue vers le bec.",
            sol,
        )
    if t2 == 2 and t3 == 3:
        bend = {
            1: "narrateur|Amir tient l'arrosoir, pieds dans le sable.",
            2: "narrateur|Amir tient l'arrosoir, pieds au métal.",
            3: "narrateur|Amir tient l'arrosoir, pieds dans l'herbe.",
        }[t1]
        return L(
            "maman|Je penche la branche, tout doux.",
            bend,
            "enfant-m|Je ne tape plus.",
            "narrateur|La pomme glisse le long des feuilles.",
            "narrateur|Elle rentre dans le bec, ploc.",
            "papa|Tu l'as gardé droit, l'arrosoir.",
            "enfant-m|Elle est à nous !",
            sol,
            "narrateur|Une goutte reste sur le vert.",
        )
    if t2 == 3 and t3 == 1:
        shake = {
            1: "narrateur|Le chapeau attend dans le sable.",
            2: "narrateur|Le chapeau attend au pied du métal.",
            3: "narrateur|Le chapeau attend sous la chaîne.",
        }[t1]
        return L(
            "enfant-m|Papa, secoue un peu.",
            "papa|Tout doux, pour ne pas la meurtrir.",
            shake,
            "narrateur|La branche ondule, une fois.",
            "narrateur|La pomme tombe dans la paille.",
            "enfant-m|Dans le nid !",
            "maman|Tu as bien visé le chapeau.",
            sol,
            "narrateur|La feuille collée fait un toit.",
        )
    if t2 == 3 and t3 == 2:
        wind = {
            1: "narrateur|Un grain de sable s'envole, puis rien.",
            2: "narrateur|Une poussière de métal s'envole, puis rien.",
            3: "narrateur|Un brin d'herbe s'envole, puis rien.",
        }[t1]
        return L(
            "enfant-m|On attend le petit vent.",
            "maman|Pieds sages, alors.",
            "narrateur|Amir se tait, le chapeau aussi.",
            wind,
            "narrateur|Un souffle passe dans les feuilles.",
            "narrateur|La pomme se détache, tout lent.",
            "enfant-m|Elle vient !",
            "papa|Dans le chapeau, pile.",
            "narrateur|La paille sent déjà le sucré.",
        )
    # t2 == 3 and t3 == 3
    tilt = {
        1: "narrateur|Le chapeau reste au creux du bac.",
        2: "narrateur|Le chapeau reste au pied du toboggan.",
        3: "narrateur|Le chapeau reste sous la balançoire.",
    }[t1]
    return L(
        "maman|J'incline la branche, vers le nid.",
        tilt,
        "enfant-m|Je ne saute plus.",
        "narrateur|La pomme glisse, puis se pose.",
        "papa|Dans le chapeau, tout au fond.",
        "enfant-m|Merci, maman.",
        "narrateur|La paille a un rond vert, maintenant.",
        sol,
        "narrateur|La feuille collée fait encore un toit.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = _t1_color(t1, "coda")
    bruit = _t1_color(t1, "bruit")
    outil = OUTIL[t2]["cap"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Ils s'assoient sous le pommier.",
            "enfant-m|Elle est sucrée, papa !",
            "papa|Tes bras ont cueilli, avec les miens.",
            "maman|Un morceau pour chacun.",
            "narrateur|Le jus colle un peu au menton.",
            f"narrateur|{outil} sèche déjà, à côté.",
            bruit,
            coda,
            "narrateur|Tout calme, la fourmi reprend l'écorce.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Amir croque, assis tout près.",
            "enfant-m|Mes pieds ont su attendre.",
            "maman|Et la pomme est venue.",
            "papa|Le jus, sur le pouce ?",
            "enfant-m|Oui, il brille.",
            f"narrateur|{outil} garde encore son ombre.",
            bruit,
            coda,
            "narrateur|Au soleil, la feuille collée sèche.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Ils partagent la pomme, trois bouchées.",
            "enfant-m|On a poussé, et elle est venue.",
            "papa|Le bois sent encore le jus.",
            "maman|Essuie ton menton, tout doux.",
            "narrateur|Un filet sucré reste au coin.",
            f"narrateur|{outil} a un rond mouillé, au fond.",
            bruit,
            coda,
            "narrateur|Les autres pommes restent au pommier.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|L'arrosoir sert d'assiette, un moment.",
            "enfant-m|Elle a voyagé dans le bec !",
            "papa|Je t'ai porté, tu as cueilli.",
            "maman|Le vert est froid, encore.",
            "narrateur|Amir souffle dessus, puis croque.",
            f"narrateur|{outil} sonne creux, après.",
            bruit,
            coda,
            "narrateur|Une goutte sèche sur l'herbe.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Ils croquent à l'ombre, tout lent.",
            "enfant-m|J'ai attendu, et ploc.",
            "maman|Le vent a fait le reste.",
            "papa|Le sucré, ça valait l'attente.",
            "narrateur|Le jus coule, une perle, au poignet.",
            f"narrateur|{outil} garde une auréole verte.",
            bruit,
            coda,
            "narrateur|Les feuilles ne bougent plus.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Maman coupe la pomme en trois.",
            "enfant-m|Tu as penché, et je tenais.",
            "papa|Le bec a fait un bon nid.",
            "maman|Tes pieds sont restés sages.",
            "narrateur|Chaque bouchée sent l'herbe chaude.",
            f"narrateur|{outil} repose, le bec vers le ciel.",
            bruit,
            coda,
            "narrateur|Un oiseau reprend une branche, plus haut.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Le chapeau devient une petite table.",
            "enfant-m|Papa a secoué, tout doux.",
            "papa|Elle n'a pas eu mal.",
            "maman|La paille sent le sucré, maintenant.",
            "narrateur|Amir croque, et un jus perle.",
            f"narrateur|{outil} garde un rond plus foncé.",
            bruit,
            coda,
            "narrateur|Plus tard, le clou attend le chapeau.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Ils s'allongent un peu, sous les feuilles.",
            "enfant-m|Le vent l'a mise dans le nid.",
            "maman|Tes pieds ont su se taire.",
            "papa|Une bouchée, puis une autre.",
            "narrateur|Le sucré reste longtemps, en bouche.",
            f"narrateur|{outil} a une tache ronde, au fond.",
            bruit,
            coda,
            "narrateur|Un souffle passe, puis plus rien.",
        )
    return L(
        "narrateur|Ils rentrent la pomme vers le banc.",
        "enfant-m|Maman a incliné, pile.",
        "maman|Tu as laissé le nid à sa place.",
        "papa|Le vert craque, tout frais.",
        "narrateur|Trois bouches, un même sucré.",
        f"narrateur|{outil} reprend le clou, plus tard.",
        bruit,
        coda,
        "narrateur|Enfin, la fourmi arrive en haut.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {
        "CHK_T0000_P0000": "oiseau,goutte",
        "CHK_T0001_P0001": "sable",
        "CHK_T0001_P0001_C0001": "sable",
        "CHK_T0001_P0001_T0002_P0001": "sable",
        "CHK_T0001_P0001_T0002_P0002": "eau",
        "CHK_T0001_P0002_T0002_P0002": "eau",
        "CHK_T0001_P0003_T0002_P0002": "eau",
    }

    s["CHK_T0000_P0000"] = L(
        "narrateur|Un pommier garde le fond du jardin.",
        "narrateur|Sur l'écorce rêche, une fourmi grimpe.",
        "narrateur|Tout en haut, une pomme verte attend.",
        "narrateur|Une feuille y reste collée, et tremble.",
        "narrateur|Au clou, un chapeau de paille pend.",
        "narrateur|Près du tronc, une caisse sent le jus.",
        "narrateur|L'arrosoir goutte encore sur la mousse.",
        "papa|Tu sens la pomme, Amir ?",
        "enfant-m|Elle est sucrée, papa.",
        "narrateur|En ce moment, Amir tape des pieds.",
        "narrateur|Toc, toc, sur l'herbe sèche.",
        "enfant-m|Je la veux, celle-là !",
        "maman|Elle est trop haute, dis ?",
        "enfant-m|Mes pieds vont l'attraper.",
        "papa|Merci, on te suit.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Sous les feuilles, le bac attend.",
        "narrateur|Le toboggan brille, un peu chaud.",
        "narrateur|Les balançoires bougent déjà.",
        "papa|Tu cours où, d'abord ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le bac à sable", "le toboggan", "les balançoires")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        li = LIEU[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|{li['q_lead']}",
            f"maman|{li['q_ask']}",
        )
        extras[f"{p}_Q0001"] = qf(li["q_ans"], li["q_acc"], li["q_retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question(t1)
        extras[f"{p}_T0002_P0000"] = t3lab("la caisse", "l'arrosoir", "le chapeau")

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
        "La pomme verte et les pieds d'Amir",
        "Jardin, pommier, pomme verte à feuille collée. Amir veut l'atteindre. "
        "T1 = bac / toboggan / balançoires (trois voyages). "
        "T2 = caisse / arrosoir / chapeau (trois affaires du jardin). "
        "T3 = neuf résolutions : bras de papa, pieds sages, on pousse ; "
        "bras de papa, j'attends, maman penche ; papa secoue, petit vent, "
        "maman incline. Fin : le jus sucré, la fourmi, l'objet qui se tait. "
        "Leçon vécue (DIF.ENE.001) : les pieds dansent, on attend, on demande, "
        "on cueille. Pas de slogan.",
        "N1 ≤ 10. Sami / Nino / Tom / Léa jetés. Héros Amir, papa, maman. "
        "Un merci de papa lié au désir (on te suit). Audio non cuit.",
    )


if __name__ == "__main__":
    main()
