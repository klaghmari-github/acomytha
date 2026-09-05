#!/usr/bin/env python3
"""TREE-DIF-022 — La marelle de Nina, pour Aniss aussi (N1, DIF.COR.001)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-022"
N1 = 10
TITLE = "La marelle de Nina, pour Aniss aussi"
FIL = (
    "Nina veut une marelle où Aniss saute aussi. "
    "Elle prépare la craie, le caillou et le linge ; les trois partent. "
    "Sur l'allée mouillée, sur la terrasse ou dans le bac, "
    "les carrés sont trop étroits pour Aniss ou trop larges pour Nina. "
    "Ils refont le jeu ensemble. Le caillou clique. Ils boivent."
)
CHARS = "Nina, Aniss, papa, maman"
SETTING = "jardin mouillé, allée, terrasse, bac à sable"


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
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"sans fin: {ph}")
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
        "pas rire",
        "sami",
        "il ne faut pas",
        "jouer ensemble",
        "zoé",
        "zoe",
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
        "lab": "la craie blanche",
        "cap": "La craie",
        "t1q": "près de la craie",
        "t1acc": "craie | la craie | près de la craie | à côté de la craie",
        "t1retry": "Le caillou est près de la craie.",
        "coda": "La craie repose près du verre.",
    },
    2: {
        "lab": "le caillou plat",
        "cap": "Le caillou",
        "t1q": "dans sa main",
        "t1acc": "main | sa main | dans sa main | dans la main",
        "t1retry": "Le caillou est dans sa main.",
        "coda": "Le caillou repose près du verre.",
    },
    3: {
        "lab": "le linge",
        "cap": "Le linge",
        "t1q": "sous le linge",
        "t1acc": "linge | le linge | sous le linge | dessous",
        "t1retry": "Le caillou est sous le linge.",
        "coda": "Le linge sèche près du verre.",
    },
}

T3_LABS = {
    1: ("attendre un peu", "le linge tendu", "trois grands carrés"),
    2: ("deux carreaux", "les joints", "autour de la table"),
    3: ("l'empreinte", "lisser le sable", "le râteau"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Nina prend la craie blanche.",
            "enfant-f|Elle sent un peu la poussière.",
            "papa|Elle écrit bien, celle-là.",
            "narrateur|Le caillou attend près du verre.",
            "enfant-f|Le caillou va avec moi.",
            "narrateur|Elle le glisse près de la craie.",
            "maman|Le linge aussi, pour le chemin.",
            "narrateur|Papa plie le linge, tout petit.",
            "narrateur|Les trois affaires restent ensemble.",
            "copain|Nina, je suis là !",
            "enfant-f|Viens, on fait la marelle.",
            "papa|La craie d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Nina prend le caillou plat.",
            "enfant-f|Il est lisse, tout chaud.",
            "maman|Il a séché au soleil.",
            "narrateur|La craie attend près du verre.",
            "papa|La craie aussi, tout près.",
            "narrateur|Elle glisse le linge par-dessus.",
            "narrateur|Les trois affaires restent ensemble.",
            "enfant-f|Aniss va tout voir.",
            "narrateur|Des pas longs sonnent dans l'herbe.",
            "copain|Me voilà, Nina.",
            "enfant-f|On saute, tous les deux ?",
            "maman|Le caillou d'abord, il est prêt.",
        )
    return L(
        "narrateur|Nina prend le linge encore frais.",
        "enfant-f|Il sent l'eau, un peu.",
        "papa|Pour sécher le chemin, oui.",
        "narrateur|Elle cache le caillou dessous.",
        "maman|La craie reste avec vous.",
        "narrateur|Papa pose la craie au bord.",
        "narrateur|Les trois affaires restent ensemble.",
        "enfant-f|Aniss, vite !",
        "narrateur|Une grande ombre arrive au seuil.",
        "copain|J'arrive, Nina.",
        "enfant-f|Je te fais une marelle.",
        "papa|Le linge d'abord, il est plié.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|La craie blanche veille près du caillou.",
            "copain|Il est tout plat !",
            "enfant-f|C'est pour sauter, Aniss.",
            "narrateur|Aniss a des chaussures plus longues.",
            "narrateur|Les siennes font un petit bruit.",
            "maman|Le jardin vous attend.",
            "papa|On reste dehors ?",
            "enfant-f|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "narrateur|Le caillou veille dans sa main.",
            "copain|Je le vois trop bien !",
            "enfant-f|Ne le lance pas encore.",
            "narrateur|Aniss penche pour voir le caillou.",
            "narrateur|Sa mèche touche presque le linge.",
            "papa|Ça sent encore l'herbe mouillée.",
            "maman|Vos mains, au-dessus du caillou ?",
            "copain|Oui, maman.",
        )
    return L(
        "narrateur|Le linge cache encore le caillou.",
        "copain|Ça sent l'eau.",
        "enfant-f|Il est là, dessous.",
        "narrateur|Le linge arrive aux genoux d'Aniss.",
        "narrateur|Pour Nina, il tombe plus bas.",
        "maman|Le jardin est tiède, devant.",
        "papa|On y va, tous les quatre ?",
        "enfant-f|Oui.",
    )


def t2_question() -> list[str]:
    return L(
        "narrateur|Le jardin sent encore l'eau.",
        "narrateur|L'allée brille, un peu trop.",
        "narrateur|La terrasse a des carreaux.",
        "narrateur|Le bac a du sable frais.",
        "papa|On commence où, pour la marelle ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|La craie frotte l'allée mouillée.",
            2: "narrateur|Le caillou tape un peu le gravier.",
            3: "narrateur|Le linge frôle l'allée, tout frais.",
        }[t1]
        return L(
            lead,
            "enfant-f|Un petit carré, pour moi.",
            "copain|Le mien, il est trop étroit.",
            "narrateur|La chaussure d'Aniss cache le trait.",
            "narrateur|Le trait pâlit dans l'eau.",
            "enfant-f|On n'arrive pas, comme ça.",
            "papa|Le chemin est encore trop mouillé.",
            "maman|Vos pieds n'ont pas la même place.",
            "copain|On fait comment, alors ?",
            "papa|Vous trouvez, tous les deux ?",
        )
    if t2 == 2:
        lead = {
            1: f"narrateur|{o['cap']} tapote un carreau chaud.",
            2: f"narrateur|{o['cap']} glisse sur un carreau.",
            3: f"narrateur|{o['cap']} frôle un carreau chaud.",
        }[t1]
        return L(
            lead,
            "enfant-f|Les carreaux sont déjà des carrés.",
            "copain|Moi, j'en prends deux d'un coup.",
            "narrateur|Le pied d'Aniss couvre deux carreaux.",
            "narrateur|Celui de Nina reste dans un seul.",
            "enfant-f|Ce n'est pas le même saut.",
            "maman|La table a de l'ombre, là.",
            "papa|Les verres attendent au bord.",
            "copain|On saute comment, alors ?",
            "maman|Vous trouvez, tous les deux ?",
        )
    lead = {
        1: f"narrateur|{o['cap']} trace un trait dans le sable.",
        2: f"narrateur|{o['cap']} s'enfonce un peu, tout doux.",
        3: f"narrateur|{o['cap']} lisse un coin de sable.",
    }[t1]
    return L(
        lead,
        "enfant-f|Une marelle dans le bac, Aniss.",
        "copain|Mes pieds font un grand trou.",
        "narrateur|L'empreinte d'Aniss ressemble à un lac.",
        "narrateur|Celle de Nina est une flaque.",
        "enfant-f|Mes carrés disparaissent dessous.",
        "papa|Le sable est encore trop meuble.",
        "maman|Le râteau repose près du bac.",
        "copain|On dessine comment, alors ?",
        "papa|Vous trouvez, tous les deux ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|L'allée garde encore trop d'eau.",
            "papa|Attendre, le linge, ou trois carrés ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Les carreaux n'ont pas la même taille.",
            "maman|Deux carreaux, les joints, ou la table ?",
        )
    return L(
        "narrateur|Le sable garde les deux empreintes.",
        "papa|L'empreinte, lisser, ou le râteau ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        wait = {
            1: "narrateur|La craie attend au bord, au sec.",
            2: "narrateur|Le caillou attend au bord, au sec.",
            3: "narrateur|Le linge attend au bord, au sec.",
        }[t1]
        return L(
            "enfant-f|On attend un peu.",
            "copain|Moi aussi, j'attends.",
            "narrateur|Le soleil lèche l'allée, grain après grain.",
            wait,
            "narrateur|Le gravier redevient clair, tout doux.",
            "enfant-f|Je fais un grand carré, maintenant.",
            "copain|Le mien rentre, cette fois.",
            "papa|Le chemin vous a laissé la place.",
            "maman|Vous avez laissé l'eau partir.",
        )
    if t2 == 1 and t3 == 2:
        use = {
            1: "narrateur|Nina trace sous le linge tendu.",
            2: "narrateur|Le caillou attend sous le linge tendu.",
            3: "narrateur|Aniss tient le linge, tout haut.",
        }[t1]
        return L(
            "copain|Je tends le linge, comme un toit.",
            "enfant-f|Un îlot sec, juste là.",
            "narrateur|Une tache sèche apparaît, toute nette.",
            use,
            "narrateur|Quatre grands carrés tiennent dessous.",
            "copain|Mes pieds rentrent, Nina.",
            "enfant-f|Les miens aussi, au milieu.",
            "papa|Vous avez séché ensemble.",
            "maman|Le linge a fait de l'ombre.",
        )
    if t2 == 1 and t3 == 3:
        hold = {
            1: "narrateur|La craie marque un, puis deux.",
            2: "narrateur|Le caillou pose un, puis deux.",
            3: "narrateur|Le linge essuie un, puis deux.",
        }[t1]
        return L(
            "enfant-f|Trois grands carrés, pas huit petits.",
            "copain|Un, deux, trois, les mêmes.",
            hold,
            "narrateur|Les traits sont larges, cette fois.",
            "narrateur|Le pied d'Aniss tient dans un carré.",
            "narrateur|Nina saute le même, tout léger.",
            "enfant-f|C'est notre marelle, Aniss.",
            "papa|Vous avez compté ensemble.",
            "maman|Trois carrés suffisent, dehors.",
        )
    if t2 == 2 and t3 == 1:
        hook = {
            1: "narrateur|La craie marque le bord des deux.",
            2: "narrateur|Le caillou saute les deux carreaux.",
            3: "narrateur|Le linge repose entre les deux.",
        }[t1]
        return L(
            "copain|Moi, je saute deux carreaux.",
            "enfant-f|Moi, j'en saute un.",
            hook,
            "narrateur|Aniss attend au bout, tout calme.",
            "narrateur|Nina le rejoint, un carreau après.",
            "copain|On arrive au même verre.",
            "enfant-f|C'est le même jeu, alors.",
            "papa|Chacun sa longueur, même arrivée.",
            "maman|Les verres sont encore frais.",
        )
    if t2 == 2 and t3 == 2:
        roll = {
            1: "narrateur|Nina pose la craie sur un joint.",
            2: "narrateur|Nina pose le caillou sur un joint.",
            3: "narrateur|Nina pose le linge sur un joint.",
        }[t1]
        return L(
            "enfant-f|On suit les joints, Aniss.",
            "copain|Les lignes minces, entre les carreaux.",
            roll,
            "narrateur|Nina marche dessus, tout facile.",
            "narrateur|Aniss met un pied devant l'autre.",
            "copain|J'arrive, tout droit.",
            "enfant-f|Moi aussi, au même bord.",
            "maman|Le joint vous a gardés ensemble.",
            "papa|Les carreaux sont restés à leur place.",
        )
    if t2 == 2 and t3 == 3:
        col = {
            1: "narrateur|La craie suit le tour de table.",
            2: "narrateur|Le caillou suit le tour de table.",
            3: "narrateur|Le linge suit le tour de table.",
        }[t1]
        return L(
            "enfant-f|On tourne autour de la table.",
            "copain|Moi dehors, toi plus près.",
            col,
            "narrateur|Le chemin d'Aniss est plus long.",
            "narrateur|Celui de Nina est plus court.",
            "enfant-f|On se retrouve aux verres.",
            "copain|J'ai fait le grand tour !",
            "papa|Vous vous êtes rejoints.",
            "maman|La table a gardé l'ombre.",
        )
    if t2 == 3 and t3 == 1:
        step = {
            1: "narrateur|La craie suit d'abord le grand pied.",
            2: "narrateur|Le caillou attend près du grand pied.",
            3: "narrateur|Le linge essuie autour du grand pied.",
        }[t1]
        return L(
            "enfant-f|Reste là, Aniss.",
            "copain|Je ne bouge plus.",
            "narrateur|Nina trace autour de sa chaussure.",
            "narrateur|Puis autour de la sienne, plus petite.",
            step,
            "enfant-f|Deux tailles, une marelle.",
            "copain|Je saute le grand, toi le petit.",
            "papa|Vos pieds ont dessiné le jeu.",
            "maman|Le bac garde les deux traces.",
        )
    if t2 == 3 and t3 == 2:
        arms = {
            1: "narrateur|La craie attend sur le bord lisse.",
            2: "narrateur|Le caillou attend sur le bord lisse.",
            3: "narrateur|Le linge a lissé tout le milieu.",
        }[t1]
        return L(
            "enfant-f|On lisse, tous les deux.",
            "copain|Moi les bords, toi le milieu.",
            "narrateur|Le sable redevient plat, tout doux.",
            arms,
            "copain|Un chemin moyen, pour nous deux.",
            "enfant-f|Ni un lac, ni une flaque.",
            "narrateur|Le caillou roule droit, cette fois.",
            "maman|Vous avez aplani ensemble.",
            "papa|Le bac vous a laissé la place.",
        )
    low = {
        1: "narrateur|La craie remplit le grand cadre.",
        2: "narrateur|Le caillou saute dans le grand cadre.",
        3: "narrateur|Le linge essuie le grand cadre.",
    }[t1]
    return L(
        "enfant-f|Papa, le râteau, s'il te plaît.",
        "papa|Je vous fais un grand cadre.",
        "narrateur|Le bois trace un carré large.",
        low,
        "copain|Je mets des traits longs, dedans.",
        "enfant-f|Moi des petits, au bord.",
        "narrateur|Les deux dessins tiennent ensemble.",
        "maman|Le râteau a juste aidé.",
        "papa|Vous avez rempli le cadre.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    coda = o["coda"]
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|L'allée est sèche, maintenant.",
            "copain|On a attendu le soleil, d'abord.",
            "enfant-f|Puis on a sauté.",
            "papa|Le grand carré a pris ton pied.",
            "maman|Buvez, l'eau est encore fraîche.",
            "narrateur|Le caillou clique, un dernier coup.",
            "copain|Il est à nous !",
            f"narrateur|{coda}",
            "narrateur|Une goutte sèche déjà sur le gravier.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Le linge retombe, tout calme.",
            "enfant-f|Ton toit a séché l'allée.",
            "copain|Tes carrés étaient assez larges.",
            "papa|Vous avez tendu ensemble.",
            "maman|Accrochez le linge, s'il est mouillé.",
            "narrateur|Nina pose le caillou au bord.",
            f"narrateur|{coda}",
            "enfant-f|Goûte l'eau, Aniss.",
            "narrateur|Une tache sèche reste au milieu.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Trois carrés brillent encore un peu.",
            "copain|Un, deux, trois, on a compté.",
            "enfant-f|Les mêmes pour toi et moi.",
            "maman|Vos chaussures ont de la poussière.",
            "papa|Soufflez, tout léger, dessus.",
            f"narrateur|{o['cap']} laisse un trait blanc.",
            "narrateur|Aniss boit, puis Nina.",
            "enfant-f|C'est notre marelle.",
            "narrateur|Le gravier se tait, tout chaud.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Ils s'assoient au bord des carreaux.",
            "enfant-f|Toi deux, moi un.",
            "copain|On est arrivés au même verre.",
            "papa|Chacun sa longueur, même jeu.",
            "maman|L'eau a attendu à sa place.",
            "enfant-f|Elle est pour Aniss, maintenant.",
            "copain|Elle est un peu froide encore.",
            f"narrateur|{coda}",
            "narrateur|Un carreau garde encore le soleil.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|Les joints sont un peu poussiéreux.",
            "copain|On les a suivis, tous les deux.",
            "enfant-f|Tes pieds allaient tout droit.",
            "maman|Le mince chemin vous a gardés.",
            "papa|Lavez-vous, tout doux, encore un peu.",
            f"narrateur|{o['cap']} garde un grain de sable.",
            "copain|Je bois, Nina.",
            "narrateur|L'eau claque, puis se tait.",
            "narrateur|Une miette de craie reste au joint.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|La table a encore un peu d'ombre.",
            "enfant-f|Tu as fait le grand tour.",
            "copain|Moi dehors, toi plus près.",
            "papa|Vous vous êtes rejoints aux verres.",
            "maman|Changez le linge, s'il est chaud.",
            f"narrateur|{coda}",
            "narrateur|Un rond d'eau marque le bois.",
            "enfant-f|Regarde-le, Aniss, il brille.",
            "narrateur|Les carreaux redeviennent calmes, tout chauds.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Le bac garde deux traces, encore.",
            "copain|Tu as dessiné mon pied.",
            "enfant-f|Puis le mien, plus petit.",
            "maman|Essuie tes chaussures, sur l'herbe.",
            "papa|Le sable est tiède, maintenant.",
            "narrateur|Aniss pose le caillou au milieu.",
            f"narrateur|{coda}",
            "narrateur|Un rai de soleil traverse le bac.",
            "narrateur|Dehors, l'allée redevient calme.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|Le sable est plat, jusqu'au bord.",
            "enfant-f|On a lissé, tous les deux.",
            "copain|Un chemin moyen, après.",
            "papa|Le bac vous a laissé le temps.",
            "maman|Le grain sèche déjà sur vos doigts.",
            f"narrateur|{o['cap']} pose un grain de sable.",
            "copain|Il roule trop bien, Nina.",
            "enfant-f|C'est pour ça.",
            "narrateur|Le verre garde l'eau, tout proche.",
        )
    return L(
        "narrateur|Un peu de sable reste au râteau.",
        "enfant-f|Papa a fait le cadre.",
        "copain|Nous, on a rempli dedans.",
        "papa|Le bois a juste aidé.",
        "maman|Vos mains sentent encore le soleil.",
        f"narrateur|{coda}",
        "narrateur|Aniss pose sa main au rebord.",
        "enfant-f|Tu as sauté, enfin.",
        "narrateur|Le bac brille un peu, puis s'endort.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Le chemin du jardin est encore mouillé.",
        "narrateur|L'arrosoir repose sur le flanc.",
        "narrateur|Une trace d'escargot brille, toute mince.",
        "narrateur|Papa ramasse deux feuilles, tout calme.",
        "narrateur|Maman pose deux verres sur la table.",
        "papa|L'eau est fraîche, Nina.",
        "maman|Aniss arrive, juste derrière la haie.",
        "narrateur|En ce moment, Nina tient une craie.",
        "narrateur|La craie blanche sent un peu la poussière.",
        "enfant-f|Je veux une marelle pour Aniss !",
        "narrateur|Les petits carrés tiennent dans sa tête.",
        "papa|Merci, tu la tiens tout doux.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Les affaires attendent près des verres.",
        "narrateur|La craie, le caillou, et le linge.",
        "maman|Tu prends quoi d'abord, Nina ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("la craie blanche", "le caillou plat", "le linge")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|Nina a glissé le caillou {o['t1q']}.",
            "maman|Il est où, le caillou ?",
        )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question()
        extras[f"{p}_T0002_P0000"] = t3lab("l'allée", "la terrasse", "le bac")

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
        TITLE,
        "Nina veut une marelle où Aniss saute aussi. T1 = craie / caillou / linge "
        "(les trois restent). T2 = allée mouillée / terrasse (carreaux) / bac à sable. "
        "T3 = neuf résolutions (attendre, linge-toit, trois carrés ; deux carreaux, joints, "
        "tour de table ; empreinte, lisser, râteau). La leçon (deux tailles de pieds) "
        "se vit : on refait le jeu, sans slogan. Fin : le caillou clique, ils boivent.",
        "N1 ≤ 10. Zoé / Tom / Léa / Sami et slogan « Plus petit ou plus grand » jetés. "
        "Un merci de papa lié au geste (tenir la craie). Audio non cuit.",
    )


if __name__ == "__main__":
    main()
