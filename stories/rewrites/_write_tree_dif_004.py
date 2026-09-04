#!/usr/bin/env python3
"""TREE-DIF-004 — La gouttière et le cube de Nino. F-NAR-018, D16, N3."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

N3 = LIMITS["N3"]
SID = "TREE-DIF-004"


def L(*rows: str) -> list[str]:
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N3:
            raise SystemExit(f"{n}>{N3}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
    return list(rows)


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
    out["fil_rouge"] = (
        "Après la pluie, Nino veut un bateau de cubes pour la gouttière. "
        "Aniss parle peu. Nino attend, tend un cube, et le bateau part."
    )
    out["title"] = "La gouttière et le cube de Nino"
    out["characters"] = "Nino, Aniss, papa, maman"
    out["setting"] = "cuisine après la pluie, puis le jardin"
    out["secondary_lessons"] = "DIF.BES.002"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
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


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {"expected_answer": ans, "accepted_examples": acc, "retry_prompt": retry}


def pre(t1: int) -> str:
    return f"CHK_T0001_P000{t1}"


COLOR = {
    1: dict(
        label="le cube rouge",
        adj="rouge",
        bateau="le bateau rouge",
        voile="le pétale",
        extra="une voile de pétale",
        eau="la flaque brique",
        touch="Le bois rouge sent encore la pluie.",
        qhint="Aniss tient le cube rouge, sans parler.",
        retry="Aniss ne dit rien. Nino fait quoi ?",
    ),
    2: dict(
        label="le cube bleu",
        adj="bleu",
        bateau="le bateau bleu",
        voile="le bouchon",
        extra="une cabine de bouchon",
        eau="l'eau profonde",
        touch="Le bleu est froid, comme une mare.",
        qhint="Aniss regarde l'eau, tout calme.",
        retry="Aniss reste silencieux. Nino fait quoi ?",
    ),
    3: dict(
        label="le cube jaune",
        adj="jaune",
        bateau="le bateau jaune",
        voile="le pissenlit",
        extra="un drapeau de pissenlit",
        eau="la flaque d'or",
        touch="Le jaune prend déjà le soleil.",
        qhint="Aniss tient le pissenlit, sans un mot.",
        retry="Aniss ne parle pas. Nino fait quoi ?",
    ),
}

PLACE = {
    1: dict(
        label="la gouttière",
        lieu="sous la gouttière",
        sol="le zinc",
        obstacle="Une feuille large barre le filet d'eau.",
        stuck="Le bateau bute, puis tremble.",
        son="eau",
    ),
    2: dict(
        label="le bac",
        lieu="dans le bac",
        sol="le sable mouillé",
        obstacle="Le sable mouillé attrape la coque.",
        stuck="Le bateau s'enfonce un peu, tout seul.",
        son="",
    ),
    3: dict(
        label="le potager",
        lieu="entre les laitues",
        sol="la terre grasse",
        obstacle="L'arrosoir laisse un courant trop vif.",
        stuck="Le bateau tourne, coincé contre une feuille.",
        son="oiseau",
    ),
}

RES = {
    1: dict(label="le pont", geste="un pont de cubes"),
    2: dict(label="la feuille", geste="une feuille-remorque"),
    3: dict(label="le quai", geste="un quai de pierre"),
}

ACC = "attendre | tendre un jouet | tendre un cube | tendre | il attend | un jouet | un cube"


def t1_script(t1: int) -> list[str]:
    c = COLOR[t1]
    if t1 == 1:
        return L(
            "narrateur|Nino prend le cube rouge, encore perlé.",
            "narrateur|Une goutte y tient, comme un hublot.",
            "enfant-m|Ça, c'est la coque.",
            "narrateur|Il glisse un pétale dans une fente.",
            "enfant-m|Et ça, la voile.",
            f"narrateur|{c['touch']}",
            "narrateur|Aniss s'approche, sans un mot.",
            "narrateur|Ses mains restent près du torchon.",
            "narrateur|Nino ouvre la bouche, puis la referme.",
            "narrateur|Il attend, le cube rouge dans la paume.",
            "enfant-m|Je te tends le cube.",
            "narrateur|C'est un jouet, pour le bateau.",
            "narrateur|Aniss le prend, tout lentement.",
            "papa|Tu as attendu, Nino.",
            "maman|Merci.",
            "enfant-m|On va à l'eau.",
        )
    if t1 == 2:
        return L(
            "narrateur|Nino choisit le cube bleu, plus lourd.",
            "narrateur|Il pose un bouchon dessus, tout droit.",
            "enfant-m|La cabine est là.",
            f"narrateur|{c['touch']}",
            "narrateur|Aniss touche le bord, du bout du doigt.",
            "narrateur|Il ne dit rien, et reste près de la nappe.",
            "narrateur|Nino a envie de raconter tout le voyage.",
            "narrateur|Il attend, les deux mains ouvertes.",
            "enfant-m|Je te tends le bleu.",
            "narrateur|Le cube est un jouet, pour eux deux.",
            "narrateur|Aniss le serre contre le bouchon.",
            "maman|Tu lui as tendu, sans le presser.",
            "papa|Merci, Nino.",
            "enfant-m|Il peut aller au fond, ce bateau.",
        )
    return L(
        "narrateur|Nino attrape le cube jaune, déjà tiède.",
        "narrateur|Un pissenlit sèche sur le rebord.",
        "enfant-m|Ce sera le drapeau.",
        "narrateur|Il le plante dans une fente, tout doux.",
        f"narrateur|{c['touch']}",
        "narrateur|Dehors, le soleil lèche déjà les flaques.",
        "enfant-m|Il faut partir, avant que ça sèche.",
        "narrateur|Aniss écoute, sans répondre.",
        "narrateur|Nino attend, le jaune tendu vers lui.",
        "enfant-m|Je te tends le jouet.",
        "narrateur|Aniss prend le cube, et le drapeau tient.",
        "papa|Tu as su attendre.",
        "maman|Le soleil, lui, n'attend pas.",
        "enfant-m|On court à l'eau.",
    )


def t2_script(t1: int, t2: int) -> list[str]:
    c = COLOR[t1]
    p = PLACE[t2]
    bateau = c["bateau"]
    adj = c["adj"]
    if t2 == 1:
        extra = {
            1: "L'eau y devient rouge, un peu brique.",
            2: "L'eau y paraît plus profonde, toute froide.",
            3: "Une tache de soleil court sur le zinc.",
        }[t1]
        return L(
            f"narrateur|Ils s'accroupissent {p['lieu']}.",
            "narrateur|Le zinc est froid, encore sonore.",
            f"narrateur|{extra}",
            f"narrateur|Nino pose {bateau} dans le filet d'eau.",
            f"narrateur|{p['obstacle']}",
            f"narrateur|{p['stuck']}",
            "enfant-m|Il est coincé.",
            "narrateur|Aniss regarde, sans un mot.",
            "narrateur|Nino attend qu'il avance la main.",
            "maman|Vous l'aidez comment ?",
        )
    if t2 == 2:
        extra = {
            1: f"Le sable colle au bois {adj}, grain par grain.",
            2: "Une flaque ronde fait un petit port, tout bleu.",
            3: "Le soleil dore le bord du bac, trop vite.",
        }[t1]
        return L(
            f"narrateur|Ils arrivent {p['lieu']}.",
            f"narrateur|{extra}",
            f"narrateur|Nino pousse {bateau} vers le milieu.",
            f"narrateur|{p['obstacle']}",
            f"narrateur|{p['stuck']}",
            "enfant-m|L'île le garde.",
            f"narrateur|{c['voile'].capitalize()} penche, puis se redresse.",
            "narrateur|Aniss pose un doigt près de l'eau, sans parler.",
            "narrateur|Nino attend, tout près.",
            "papa|Vous faites quoi, maintenant ?",
        )
    extra = {
        1: "Une laitue cache le pétale, tout un moment.",
        2: "Un bouchon cogne une tige, clic, tout mouillé.",
        3: "Entre deux choux, le pissenlit prend le vent.",
    }[t1]
    return L(
        "narrateur|Au potager, la terre sent encore chaud.",
        f"narrateur|{extra}",
        f"narrateur|Nino pose {bateau} {p['lieu']}.",
        f"narrateur|{p['obstacle']}",
        f"narrateur|{p['stuck']}",
        "enfant-m|Trop vite, le courant.",
        "narrateur|Aniss s'accroupit, les mains sur les genoux.",
        "narrateur|Nino ne le presse pas.",
        "maman|Le bateau attend, lui aussi.",
        "papa|Vous le sortez comment ?",
    )


def t3_script(t1: int, t2: int, t3: int) -> list[str]:
    c = COLOR[t1]
    p = PLACE[t2]
    bateau = c["bateau"]
    if t3 == 1:
        return L(
            "enfant-m|On fait un pont de cubes.",
            f"narrateur|Nino pose un cube gris, {p['lieu']}.",
            "narrateur|Il tend un autre cube, comme un jouet.",
            "narrateur|Aniss le prend, et le pose.",
            "narrateur|Les mains suffisent, pour ce pont.",
            f"narrateur|{bateau.capitalize()} glisse sous le pont.",
            f"narrateur|{c['voile'].capitalize()} passe, tout droit.",
            "enfant-m|Il est parti.",
            "papa|Vous l'avez laissé choisir son temps.",
            "narrateur|Nino attend encore une goutte, puis sourit.",
        )
    if t3 == 2:
        return L(
            "enfant-m|Une feuille, pour le tirer.",
            f"narrateur|Nino glisse une feuille sous {bateau}.",
            "narrateur|Il la tend vers Aniss, sans parler trop.",
            "narrateur|Aniss tient le bord, tout doux.",
            {
                1: "narrateur|La feuille coincée se soulève, tout doux.",
                2: "narrateur|Le sable lâche enfin un peu.",
                3: "narrateur|Le courant se calme, entre les laitues.",
            }[t2],
            "narrateur|La feuille pousse, et le passage s'ouvre.",
            f"narrateur|{bateau.capitalize()} avance, avec {c['extra']}.",
            "enfant-m|Doucement.",
            "maman|Tu as attendu qu'il tienne.",
            "papa|Merci, tous les deux.",
        )
    return L(
        "enfant-m|On va au quai, plus loin.",
        f"narrateur|Ils courent vers une pierre, {p['lieu']}.",
        f"narrateur|{bateau.capitalize()} reste derrière, tout petit.",
        "narrateur|Nino s'assoit, et attend.",
        "narrateur|Il tend un cube vers Aniss, pour le quai.",
        "narrateur|Aniss le pose, comme une borne.",
        f"narrateur|{c['eau'].capitalize()} amène le bateau, tout lent.",
        "enfant-m|Le voilà.",
        "papa|Vous n'avez pas forcé le courant.",
        "maman|Il est arrivé tout seul, presque.",
    )


def fin_script(t1: int, t2: int, t3: int) -> list[str]:
    c = COLOR[t1]
    p = PLACE[t2]
    bateau = c["bateau"]
    if t3 == 1:
        last = {
            1: "Une dernière goutte sonne sur le zinc, puis plus rien.",
            2: "Un grain de sable reste collé au pont, tout minuscule.",
            3: "Une laitue se redresse, et le potager redevient calme.",
        }[t2]
        return L(
            f"narrateur|{bateau.capitalize()} s'arrête près des cailloux.",
            "enfant-m|Terminus.",
            "narrateur|Aniss rend le cube, toujours sans un mot.",
            "narrateur|Nino le remercie d'un signe.",
            f"narrateur|Ils rentrent, {c['voile']} dans la paume.",
            "maman|Le torchon est prêt, près du radiateur.",
            "papa|Le bois va sécher, tout doux.",
            f"narrateur|{c['label'].capitalize()} brille encore, un peu mouillé.",
            f"narrateur|{last}",
        )
    if t3 == 2:
        last = {
            1: "La feuille reste dans la gouttière, comme un quai vide.",
            2: "Le bac garde une trace de feuille, toute mince.",
            3: "L'arrosoir ne goutte plus, entre les choux.",
        }[t2]
        return L(
            f"narrateur|Ils portent {bateau} jusqu'à la porte.",
            "enfant-m|Il a voyagé.",
            "narrateur|Aniss essuie le bord, du plat de la main.",
            "papa|Vous l'avez tiré sans le bousculer.",
            "maman|La soupe sent encore, dans la cuisine.",
            f"narrateur|{c['label'].capitalize()} sèche sur le rebord.",
            "narrateur|Nino pose le jouet, et attend.",
            "copain|Ploc.",
            f"narrateur|{last}",
        )
    last = {
        1: "Alors le zinc s'est tu, derrière la buée.",
        2: "Sous la fenêtre, le sable du bac redevient plat.",
        3: "Une odeur de terre rentre, puis la porte se referme.",
    }[t2]
    return L(
        f"narrateur|Au quai, {bateau} touche enfin la pierre.",
        "enfant-m|On t'attendait.",
        "narrateur|Aniss hoche la tête, rien de plus.",
        "maman|Ça suffit, parfois.",
        "papa|Vous avez laissé le temps.",
        f"narrateur|Ils rentrent avec {c['label']}, encore froid.",
        "narrateur|Sur le radiateur, le bois sèche, tout bas.",
        f"narrateur|Près du torchon, {c['voile']} repose.",
        f"narrateur|{last}",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": "goutte"}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Une goutte court sur le cube, toute ronde.",
        "narrateur|Elle glisse, puis s'arrête au bord.",
        "narrateur|Dehors, le zinc de la gouttière cliquette encore.",
        "narrateur|Ça sent le bois mouillé, près de la fenêtre.",
        "narrateur|La nappe à carreaux a une tache d'eau.",
        "narrateur|Papa essuie un cube avec le torchon rayé.",
        "narrateur|Maman ouvre un peu la fenêtre.",
        "maman|Tu entends les gouttes, Nino ?",
        "enfant-m|Elles font ploc, sur le zinc.",
        "papa|Le jardin est encore une rivière.",
        "narrateur|En ce moment, Nino aligne trois cubes.",
        "narrateur|Un rouge, un bleu, un jaune, encore humides.",
        "enfant-m|Je veux un bateau de cubes.",
        "enfant-m|Il partira dans la gouttière.",
        "narrateur|La porte s'ouvre, tout doux.",
        "narrateur|Aniss entre, les chaussettes un peu mouillées.",
        "narrateur|Il parle peu, et regarde les cubes.",
        "narrateur|Nino a envie de tout expliquer.",
        "narrateur|Il respire, puis attend.",
        "papa|Tu prends quelle couleur, capitaine ?",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois cubes brillent encore, sur le rebord.",
        "papa|Le rouge, le bleu, ou le jaune ?",
        "maman|C'est toi qui choisis la coque.",
    )
    extras["CHK_T0001_P0000"] = t3lab("le cube rouge", "le cube bleu", "le cube jaune")

    for t1, col in COLOR.items():
        p = pre(t1)
        s[p] = t1_script(t1)
        s[f"{p}_Q0001"] = L(
            f"narrateur|{col['qhint']}",
            "maman|Nino fait quoi ?",
        )
        extras[f"{p}_Q0001"] = qf("attendre", ACC, col["retry"])
        if t1 == 1:
            s[f"{p}_C0001"] = L(
                "narrateur|Nino reste près de lui, tout calme.",
                "narrateur|Nino ne force rien, pas même un mot.",
                "enfant-m|Le bateau t'attend aussi.",
                "narrateur|Aniss pose le cube contre le pétale.",
                "papa|Vous partez où, avec le rouge ?",
                "narrateur|Le torchon reste sur la table, un peu mouillé.",
            )
        elif t1 == 2:
            s[f"{p}_C0001"] = L(
                "narrateur|Nino n'ajoute pas de question.",
                "narrateur|Il ne force pas.",
                "enfant-m|On va chercher l'eau profonde.",
                "narrateur|Aniss garde le bleu, et suit.",
                "maman|Le bouchon tient, tout droit.",
                "papa|Par où, d'après vous ?",
            )
        else:
            s[f"{p}_C0001"] = L(
                "narrateur|Nino retient encore une phrase.",
                "narrateur|Il ne force pas la parole.",
                "enfant-m|Le soleil sèche les chemins.",
                "narrateur|Aniss serre le jaune, et hoche la tête.",
                "papa|Vite, mais sans le presser, lui.",
                "maman|Où l'eau reste-t-elle, encore ?",
            )
        s[f"{p}_T0002_P0000"] = L(
            f"narrateur|{col['bateau'].capitalize()} est prêt, tout petit.",
            "papa|La gouttière, le bac, ou le potager ?",
            "maman|Où l'eau l'appelle, d'après toi ?",
        )
        extras[f"{p}_T0002_P0000"] = t3lab("la gouttière", "le bac", "le potager")

        for t2, pl in PLACE.items():
            sp = f"{p}_T0002_P000{t2}"
            s[sp] = t2_script(t1, t2)
            sons[sp] = pl["son"]
            s[f"{sp}_T0003_P0000"] = L(
                f"narrateur|{col['bateau'].capitalize()} ne peut plus avancer.",
                "papa|Le pont, la feuille, ou le quai ?",
                "maman|Vous choisissez le geste ?",
            )
            extras[f"{sp}_T0003_P0000"] = t3lab("le pont", "la feuille", "le quai")
            sons[f"{sp}_T0003_P0000"] = pl["son"]

            for t3 in RES:
                s[f"{sp}_T0003_P000{t3}"] = t3_script(t1, t2, t3)
                s[f"{sp}_T0003_P000{t3}_F0001"] = fin_script(t1, t2, t3)
                if t3 == 2:
                    sons[f"{sp}_T0003_P000{t3}"] = pl["son"] or "eau"

    write_tree(s, extras, sons)
    relecture(
        SID,
        "La gouttière et le cube de Nino",
        "Nino veut un bateau de cubes. Aniss parle peu. "
        "T1 = cube rouge / bleu / jaune. T2 = gouttière / bac / potager. "
        "T3 = pont / feuille / quai. Fin vécue, cube qui sèche.",
        "Gabarit jeté (Jules, Raphaël-héros, slogans, goûter, animaux). "
        "Désir ≠ leçon. chunk_id inchangés. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
