#!/usr/bin/env python3
"""TREE-COL-001 — avis2 : pomme qui s'échappe, 9 aventures, politesse vécue."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

N2 = LIMITS["N2"]
SID = "TREE-COL-001"


def L(*rows: str) -> list[str]:
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N2:
            raise SystemExit(f"{n}>{N2}: {ph}")
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
        nc = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), scale, rate)
        if cid in extras:
            nc.update(extras[cid])
        by[cid] = nc
    out = dict(src)
    out["fil_rouge"] = (
        "Raphaël veut livrer les pommes à Mila. Une pomme s'échappe. "
        "Ils la retrouvent, puis le voyage reprend."
    )
    out["title"] = "Le voyage des pommes de Raphaël"
    out["characters"] = "Raphaël, Mila, papa, maman"
    out["setting"] = "cuisine, après le marché"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def t3(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {"expected_answer": ans, "accepted_examples": acc, "retry_prompt": retry}


VEH = {
    1: dict(nom="le train", bruit="clic", mishap="Elle tombe entre deux wagons.", hide="entre les wagons"),
    2: dict(nom="le bus", bruit="stop", mishap="Elle roule sous la chaise.", hide="sous la chaise"),
    3: dict(nom="la voiture", bruit="toc", mishap="Elle se coince contre le livre.", hide="contre le livre"),
}
STOP = {
    1: dict(nom="la table", lieu="sous la nappe", detail="Des miettes collent à la nappe."),
    2: dict(nom="la fenêtre", lieu="contre la vitre", detail="Le soleil rend la vitre glissante."),
    3: dict(nom="le tabouret", lieu="sous le tabouret", detail="Une chaussette cache un coin."),
}


def pre(t1: int) -> str:
    return f"CHK_T0001_P000{t1}"


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": "goutte"}

    s["CHK_T0000_P0000"] = L(
        "narrateur|Une goutte glisse le long de la casserole.",
        "narrateur|Ça sent la pomme, toute douce.",
        "narrateur|Le torchon rayé pend près de l'évier.",
        "narrateur|Dehors, le marché parle tout bas.",
        "narrateur|Un rond de soleil se pose sur le carrelage.",
        "narrateur|Papa a mis des rondelles dans un bol jaune.",
        "narrateur|Une pomme entière reste au bord, trop ronde.",
        "enfant-m|Je veux les porter jusqu'à Mila.",
        "maman|Elle rentre du marché, tout à l'heure.",
        "papa|Tu prends un véhicule, en attendant ?",
        "narrateur|En ce moment, Raphaël touche le bol.",
        "narrateur|Le bol est un peu lourd.",
        "enfant-m|On fait le voyage des pommes.",
        "papa|Le train, le bus, ou la voiture ?",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Trois jouets attendent près du bol.",
        "narrateur|Le train, le bus, ou la voiture.",
        "maman|Qu'est-ce que tu prends, Raphaël ?",
    )
    extras["CHK_T0001_P0000"] = t3("le train", "le bus", "la voiture")

    for t1, v in VEH.items():
        p = pre(t1)
        s[p] = L(
            f"narrateur|Raphaël prend {v['nom']}.",
            f"narrateur|Les roues font {v['bruit']}, sur le carrelage.",
            "narrateur|La porte s'ouvre.",
            "narrateur|Mila entre, les joues roses.",
            "enfant-m|Bonjour, Mila.",
            "enfant-f|Bonjour, Raphaël.",
            f"enfant-m|C'est {v['nom']} des pommes.",
            "enfant-f|J'apporte le bol ?",
            "papa|Il est un peu lourd.",
            "enfant-m|S'il te plaît, aide-nous.",
            "papa|Merci, Mila.",
            "narrateur|Ils glissent le bol, tout doux.",
            "narrateur|La pomme ronde tremble au bord.",
            f"narrateur|{v['mishap']}",
            "enfant-f|Elle est partie !",
            "enfant-m|Le voyage attend.",
        )
        s[f"{p}_Q0001"] = L(
            "narrateur|La pomme ronde n'est plus dans le bol.",
            "maman|Où est-elle allée ?",
        )
        extras[f"{p}_Q0001"] = qf(
            v["hide"].split()[-1],
            f"{v['hide']} | pomme | par terre | {v['nom']}",
            "La pomme ronde n'est plus dans le bol. Où est-elle ?",
        )
        s[f"{p}_C0001"] = L(
            f"narrateur|Ils se baissent vers {v['hide']}.",
            "narrateur|La pomme brille encore, un peu loin.",
            "enfant-f|On la suit.",
            "papa|Doucement, le carrelage est froid.",
            "enfant-m|Merci, papa.",
            "narrateur|Le bol reste sur le véhicule.",
        )
        s[f"{p}_T0002_P0000"] = L(
            "narrateur|La pomme roule encore un peu.",
            "narrateur|La table, la fenêtre, ou le tabouret.",
            "papa|Elle va où, d'après toi ?",
        )
        extras[f"{p}_T0002_P0000"] = t3("la table", "la fenêtre", "le tabouret")

        for t2, st in STOP.items():
            sp = f"{p}_T0002_P000{t2}"
            s[sp] = L(
                f"narrateur|La pomme file vers {st['nom']}.",
                f"narrateur|{st['detail']}",
                f"narrateur|Elle s'arrête {st['lieu']}.",
                f"narrateur|{v['nom'].capitalize()} reste au milieu.",
                "enfant-f|On la voit à peine.",
                "enfant-m|Elle nous attend.",
                "maman|Vous la prenez comment ?",
            )
            s[f"{sp}_T0003_P0000"] = L(
                "narrateur|La pomme ne bouge plus.",
                "narrateur|On ramasse, on attend, ou on invente.",
                "papa|Vous faites quoi, tous les deux ?",
            )
            extras[f"{sp}_T0003_P0000"] = t3("on ramasse", "on attend", "on invente")

            # ramasse
            s[f"{sp}_T0003_P0001"] = L(
                "enfant-m|S'il te plaît, le torchon.",
                "maman|Le voilà.",
                "narrateur|Mila tient le torchon.",
                "narrateur|Raphaël glisse la main.",
                f"narrateur|Il touche la pomme, {st['lieu']}.",
                "enfant-f|Je te la passe.",
                "enfant-m|Merci.",
                "narrateur|La pomme est un peu froide.",
                "narrateur|Ils la posent dans le bol.",
                f"narrateur|{v['nom'].capitalize()} peut repartir.",
            )
            s[f"{sp}_T0003_P0001_F0001"] = L(
                f"narrateur|{v['nom'].capitalize()} s'arrête près des assiettes.",
                "enfant-m|Terminus.",
                "narrateur|Ils posent une rondelle chacun.",
                "narrateur|La pomme sauvée reste au milieu.",
                "enfant-f|Celle-là a voyagé plus loin.",
                "papa|Vous l'avez cherchée.",
                "maman|Le torchon sent encore la pomme.",
                f"narrateur|Un {v['bruit']} lointain, sous la table.",
                "narrateur|Il ne reste plus rien dans le bol.",
                "narrateur|La casserole fume encore, tout doux.",
            )

            # attend
            s[f"{sp}_T0003_P0002"] = L(
                "enfant-m|On attend.",
                "narrateur|La pomme tremble, puis s'arrête.",
                f"narrateur|Elle reste {st['lieu']}.",
                "enfant-f|Elle ne fuit plus.",
                "papa|Vous avez laissé le temps.",
                "narrateur|Raphaël avance deux doigts.",
                "narrateur|La pomme roule dans sa paume.",
                "enfant-m|Merci d'avoir attendu.",
                "enfant-f|On la remet.",
                f"narrateur|{v['nom'].capitalize()} reprend {v['bruit']}.",
            )
            s[f"{sp}_T0003_P0002_F0001"] = L(
                f"narrateur|{v['nom'].capitalize()} rejoint les assiettes, sans se presser.",
                "narrateur|Ils croquent, tout doux.",
                "enfant-f|Elle a attendu, elle aussi.",
                "papa|Le voyage a pris le temps qu'il faut.",
                "maman|Le marché, dehors, s'est calmé.",
                "narrateur|Une rondelle brille encore au fond.",
                f"narrateur|{st['nom'].capitalize()} garde une petite ombre mouillée.",
                "narrateur|Papa raccroche le torchon rayé.",
                "narrateur|Ça sent encore le fruit, près de l'évier.",
            )

            # invente
            s[f"{sp}_T0003_P0003"] = L(
                "enfant-f|C'est l'invitée en retard.",
                "enfant-m|Le restaurant ouvre pour elle.",
                f"narrateur|Ils posent la pomme {st['lieu']}, comme un siège.",
                "enfant-f|S'il te plaît, une rondelle.",
                "enfant-m|Voilà, madame Pomme.",
                "papa|Une table pour trois, alors.",
                "narrateur|Mila glisse une rondelle près de la ronde.",
                "narrateur|Raphaël verse un peu d'eau dans un gobelet.",
                "enfant-f|Merci d'être venue.",
                f"narrateur|{v['nom'].capitalize()} fait le vestiaire.",
            )
            s[f"{sp}_T0003_P0003_F0001"] = L(
                "narrateur|L'invitée a une goutte sur la peau.",
                "enfant-m|On l'a gardée pour la fin.",
                "enfant-f|On la partage.",
                "narrateur|Papa coupe la pomme ronde en deux.",
                "maman|Il en reste pour demain, sur le torchon.",
                f"narrateur|{v['nom'].capitalize()} dort près du bol.",
                "narrateur|Plus rien ne cache le carrelage.",
                "narrateur|Le soleil a bougé sur le carrelage.",
                "narrateur|Dehors, le marché a fermé.",
            )

    write_tree(s, extras, sons)
    relecture(
        SID,
        "Le voyage des pommes de Raphaël",
        "pomme échappée, 3 véhicules, 3 lieux, ramasse/attendre/invente, fin vécue",
        "avis2. Audio non cuit. 27 chemins non écoutés à voix haute.",
    )


if __name__ == "__main__":
    main()
