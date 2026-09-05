#!/usr/bin/env python3
"""TREE-DIF-021 — Le fort d'Amir près de la fenêtre (N1, DIF.BES.002)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-DIF-021"
N1 = 10
TITLE = "Le fort d'Amir près de la fenêtre"
FIL = (
    "Amir veut un fort de coussins pour Nina, près de la grande fenêtre. "
    "Il prend d'abord le coussin, la couverture ou la lampe ; les trois restent. "
    "À la fenêtre Nina regarde la pluie, sous la table elle a déjà une cave, "
    "dans le couloir elle met ses chaussures. Il propose, et il accepte oui, "
    "plus tard, ou une autre idée."
)


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
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = "Amir, Nina, papa, maman"
    out["setting"] = "salon, grande fenêtre, table, couloir"
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
        "inviter sans forcer",
        "accepter plusieurs réponses",
        "\btom\b",
    ):
        if bad.startswith("\\"):
            continue
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
        "lab": "le coussin rouge",
        "cap": "Le coussin rouge",
        "t1q": "sur le tapis",
        "t1acc": "tapis | le tapis | sur le tapis | par terre",
        "t1retry": "Le coussin est sur le tapis.",
        "coda": "Le coussin rouge reste tiède, au milieu.",
    },
    2: {
        "lab": "la couverture bleue",
        "cap": "La couverture bleue",
        "t1q": "autour du coussin",
        "t1acc": "coussin | le coussin | autour | autour du coussin",
        "t1retry": "La couverture est autour du coussin.",
        "coda": "La couverture bleue garde un pli, tout doux.",
    },
    3: {
        "lab": "la petite lampe",
        "cap": "La petite lampe",
        "t1q": "près du fort",
        "t1acc": "fort | le fort | près du fort | à côté",
        "t1retry": "La lampe éclaire le fort.",
        "coda": "La petite lampe fait encore un rond jaune.",
    },
}

T3_LABS = {
    1: ("attendre un peu", "parler tout bas", "s'asseoir à côté"),
    2: ("glisser le coussin", "mélanger les forts", "rester à côté"),
    3: ("un tout petit jeu", "l'accompagner", "proposer plus tard"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Amir tire d'abord le coussin rouge.",
            "enfant-m|Il est tout mou.",
            "maman|Pose-le sur le tapis, tout doux.",
            "narrateur|Un petit toc sonne contre le sol.",
            "papa|La couverture aussi, près de toi.",
            "narrateur|Maman glisse la lampe, tout près.",
            "narrateur|Les trois affaires restent ensemble.",
            "enfant-m|Nina va rentrer dans le fort.",
            "papa|Tu l'invites, quand elle arrive ?",
            "enfant-m|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "narrateur|Amir prend d'abord la couverture bleue.",
            "enfant-m|Elle sent le savon.",
            "papa|Enroule-la autour du coussin.",
            "narrateur|Le tissu tombe, un peu froid.",
            "maman|Le coussin rouge, ensuite, dessous.",
            "narrateur|Il pose la lampe à côté.",
            "narrateur|Les trois affaires restent ensemble.",
            "enfant-m|Nina va tout voir.",
            "maman|Tu lui proposes le fort ?",
            "enfant-m|Oui, maman.",
        )
    return L(
        "narrateur|Amir allume d'abord la petite lampe.",
        "enfant-m|Ça fait un camp, déjà.",
        "maman|Le rond jaune éclaire le tapis.",
        "narrateur|Un clic sec, puis le silence.",
        "papa|Le coussin et la couverture, avec toi.",
        "narrateur|Il les pose près du fort.",
        "narrateur|Les trois affaires restent ensemble.",
        "enfant-m|Nina va aimer la lumière.",
        "papa|Tu lui proposes, tout calme ?",
        "enfant-m|Oui.",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Le coussin rouge attend sur le tapis.",
            "narrateur|Des pas légers sonnent dans l'entrée.",
            "copine|Amir, je suis là.",
            "enfant-m|Viens voir le fort.",
            "narrateur|Nina a les joues encore froides.",
            "maman|Elle enlève son manteau, tout doux.",
            "papa|Vous restez dans le salon ?",
            "enfant-m|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "narrateur|La couverture veille autour du coussin.",
            "narrateur|La porte s'ouvre, tout léger.",
            "copine|Me voilà, Amir.",
            "enfant-m|Regarde, c'est tout bleu.",
            "narrateur|Nina touche le tissu, un instant.",
            "papa|Ça sent encore le savon.",
            "maman|Vous restez près du tapis ?",
            "copine|Je ne sais pas encore.",
        )
    return L(
        "narrateur|La petite lampe tient le fort allumé.",
        "narrateur|Un manteau mouillé apparaît au seuil.",
        "copine|J'arrive, Amir.",
        "enfant-m|Regarde le rond jaune.",
        "narrateur|Nina cligne un peu, tout calme.",
        "maman|Le salon est tiède, devant.",
        "papa|On vous laisse le temps ?",
        "enfant-m|Oui.",
    )


def t2_question() -> list[str]:
    return L(
        "narrateur|Nina est dans la maison, quelque part.",
        "narrateur|La fenêtre a encore des gouttes.",
        "narrateur|Sous la table, ça fait cave.",
        "narrateur|Le couloir sent les chaussures.",
        "papa|On l'invite où, Amir ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1:
        lead = {
            1: "narrateur|Le coussin rouge voyage vers la fenêtre.",
            2: "narrateur|La couverture bleue glisse vers la fenêtre.",
            3: "narrateur|La petite lampe avance vers la fenêtre.",
        }[t1]
        return L(
            lead,
            "narrateur|Nina a le nez contre le verre.",
            "enfant-m|Nina, le fort est prêt.",
            "narrateur|Elle ne se tourne pas encore.",
            "copine|La pluie fait des chemins.",
            "enfant-m|Tu viens ?",
            "copine|J'écoute les gouttes, un moment.",
            "maman|Elle regarde encore, tout absorbée.",
            "papa|Tu proposes comment, Amir ?",
        )
    if t2 == 2:
        lead = {
            1: f"narrateur|{o['cap']} penche vers les chaises.",
            2: f"narrateur|{o['cap']} frôle le pied de table.",
            3: f"narrateur|{o['cap']} éclaire un peu dessous.",
        }[t1]
        return L(
            lead,
            "narrateur|Nina est déjà sous la table.",
            "copine|C'est ma cave, à moi.",
            "enfant-m|Mon fort est au salon.",
            "narrateur|Deux jeux, trop loin l'un de l'autre.",
            "enfant-m|Tu viens dans le mien ?",
            "copine|Le mien est déjà commencé.",
            "maman|Elle a son idée, déjà.",
            "papa|Tu fais comment, Amir ?",
        )
    lead = {
        1: f"narrateur|{o['cap']} voyage jusqu'au couloir.",
        2: f"narrateur|{o['cap']} traîne un peu, au seuil.",
        3: f"narrateur|{o['cap']} éclaire les chaussures, tout bas.",
    }[t1]
    return L(
        lead,
        "narrateur|Nina enfile déjà une chaussure.",
        "copine|Maman m'attend, tout à l'heure.",
        "enfant-m|Le fort est prêt, Nina.",
        "narrateur|L'autre chaussure attend, encore ouverte.",
        "enfant-m|Tu restes un peu ?",
        "copine|Je ne sais pas.",
        "maman|Le manteau est près de la porte.",
        "papa|Tu proposes quoi, Amir ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Nina reste collée à la fenêtre.",
            "papa|Attendre, parler tout bas, ou s'asseoir ?",
        )
    if t2 == 2:
        return L(
            "narrateur|La cave de Nina est déjà commencée.",
            "maman|Glisser, mélanger, ou rester à côté ?",
        )
    return L(
        "narrateur|Une chaussure est déjà enfilée.",
        "papa|Un petit jeu, accompagner, ou plus tard ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    if t2 == 1 and t3 == 1:
        wait = {
            1: "narrateur|Le coussin rouge attend derrière elle.",
            2: "narrateur|La couverture bleue attend derrière elle.",
            3: "narrateur|La petite lampe attend derrière elle.",
        }[t1]
        return L(
            "enfant-m|J'attends un peu.",
            "copine|Merci, Amir.",
            "narrateur|Une goutte glisse, puis une autre.",
            wait,
            "narrateur|Nina se tourne, enfin, tout calme.",
            "copine|Je viens, maintenant.",
            "enfant-m|Le fort est encore chaud.",
            "papa|Tu as laissé son regard finir.",
            "maman|Elle a dit oui, à son heure.",
        )
    if t2 == 1 and t3 == 2:
        near = {
            1: "narrateur|Il pose le coussin, tout proche.",
            2: "narrateur|Il pose la couverture, tout proche.",
            3: "narrateur|Il pose la lampe, tout proche.",
        }[t1]
        return L(
            "enfant-m|Nina, je te propose le fort.",
            "narrateur|Sa voix reste tout bas, près du verre.",
            near,
            "copine|J'ai entendu, Amir.",
            "enfant-m|Tu peux dire non.",
            "copine|Oui, je viens.",
            "narrateur|Elle quitte la fenêtre, tout doux.",
            "papa|Tu as proposé, sans tirer.",
            "maman|Elle a choisi d'elle-même.",
        )
    if t2 == 1 and t3 == 3:
        sit = {
            1: "narrateur|Amir s'assoit sur le coussin rouge.",
            2: "narrateur|Amir s'assoit sous la couverture bleue.",
            3: "narrateur|Amir s'assoit dans le rond jaune.",
        }[t1]
        return L(
            "enfant-m|Je m'assois à côté.",
            sit,
            "narrateur|Il ne tire pas sa manche.",
            "copine|Tu regardes la pluie, toi aussi ?",
            "enfant-m|Oui, avec toi.",
            "narrateur|Deux nez, maintenant, contre le verre.",
            "copine|Après, on va dans le fort.",
            "papa|Tu es resté près d'elle.",
            "maman|Elle a proposé la suite.",
        )
    if t2 == 2 and t3 == 1:
        slide = {
            1: "narrateur|Le coussin rouge glisse sous la table.",
            2: "narrateur|La couverture bleue glisse sous la table.",
            3: "narrateur|La petite lampe glisse sous la table.",
        }[t1]
        return L(
            "enfant-m|Je te propose mon coussin.",
            "copine|Dans ma cave ?",
            "enfant-m|Si tu veux.",
            slide,
            "narrateur|Nina recule un peu, puis accepte.",
            "copine|Il est mou, merci.",
            "enfant-m|On est deux, maintenant.",
            "papa|Tu as glissé, sans pousser.",
            "maman|Sa cave a gardé sa place.",
        )
    if t2 == 2 and t3 == 2:
        mix = {
            1: "narrateur|Le coussin rouge fait un mur commun.",
            2: "narrateur|La couverture bleue recouvre les deux coins.",
            3: "narrateur|La petite lampe éclaire les deux coins.",
        }[t1]
        return L(
            "enfant-m|On mélange les deux forts ?",
            "copine|Le mien reste, le tien aussi.",
            "enfant-m|D'accord.",
            mix,
            "narrateur|Une chaise bouge, tout doux.",
            "copine|C'est plus grand, maintenant.",
            "enfant-m|C'est le nôtre.",
            "papa|Vous avez dit oui, tous les deux.",
            "maman|Deux idées, une seule cave.",
        )
    if t2 == 2 and t3 == 3:
        side = {
            1: "narrateur|Le coussin rouge reste juste à côté.",
            2: "narrateur|La couverture bleue reste juste à côté.",
            3: "narrateur|La petite lampe reste juste à côté.",
        }[t1]
        return L(
            "copine|Pas dans ma cave, Amir.",
            "enfant-m|D'accord.",
            "enfant-m|Je reste à côté, alors.",
            side,
            "narrateur|Il joue tout près, sans entrer.",
            "copine|Tu peux parler, d'ici.",
            "enfant-m|Mon fort t'écoute.",
            "papa|Tu as accepté son non.",
            "maman|Vous êtes encore ensemble.",
        )
    if t2 == 3 and t3 == 1:
        game = {
            1: "narrateur|Le coussin rouge devient un siège, une minute.",
            2: "narrateur|La couverture bleue devient une cape, une minute.",
            3: "narrateur|La petite lampe devient un phare, une minute.",
        }[t1]
        return L(
            "enfant-m|Un tout petit jeu, Nina ?",
            "copine|Très petit, alors.",
            "enfant-m|D'accord.",
            game,
            "narrateur|Ils comptent jusqu'à trois, tout bas.",
            "copine|C'est fini, déjà.",
            "enfant-m|Merci d'être restée.",
            "papa|Tu as proposé court, juste assez.",
            "maman|La chaussure attendait, sans se fâcher.",
        )
    if t2 == 3 and t3 == 2:
        walk = {
            1: "narrateur|Le coussin rouge reste au seuil, un instant.",
            2: "narrateur|La couverture bleue reste au seuil, un instant.",
            3: "narrateur|La petite lampe reste au seuil, un instant.",
        }[t1]
        return L(
            "copine|Je m'en vais, Amir.",
            "enfant-m|Je t'accompagne, alors.",
            walk,
            "narrateur|Il marche à côté d'elle, tout calme.",
            "papa|La porte s'ouvre, un peu d'air.",
            "enfant-m|À bientôt, Nina.",
            "copine|À bientôt, le fort.",
            "maman|Tu as accepté qu'elle parte.",
            "narrateur|Ils se font un petit signe.",
        )
    later = {
        1: "narrateur|Le coussin rouge garde sa place, au salon.",
        2: "narrateur|La couverture bleue garde sa place, au salon.",
        3: "narrateur|La petite lampe garde sa place, au salon.",
    }[t1]
    return L(
        "enfant-m|On joue plus tard, alors ?",
        "copine|Oui, plus tard.",
        "enfant-m|D'accord.",
        later,
        "narrateur|Nina noue l'autre chaussure.",
        "copine|Garde le fort allumé.",
        "enfant-m|Il t'attend.",
        "papa|Tu as proposé une autre heure.",
        "maman|Elle a dit oui, pour plus tard.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    coda = f"narrateur|{o['coda']}"
    if t2 == 1 and t3 == 1:
        return L(
            "narrateur|Ils rentrent dans le fort, enfin.",
            "copine|La pluie a fini son chemin.",
            "enfant-m|Toi aussi.",
            "papa|Vous avez attendu le bon moment.",
            "maman|Le cacao est encore un peu chaud.",
            coda,
            "narrateur|Nina souffle sur sa tasse.",
            "enfant-m|C'est notre fort, maintenant.",
            "narrateur|Une goutte sèche déjà sur le verre.",
        )
    if t2 == 1 and t3 == 2:
        return L(
            "narrateur|Le fort sent encore le savon.",
            "enfant-m|Tu as dit oui, tout bas.",
            "copine|J'avais entendu, près du verre.",
            "papa|Tu as proposé, sans tirer.",
            "maman|Buvez un peu, tout doux.",
            coda,
            "narrateur|Nina pose sa joue sur le tissu.",
            "enfant-m|Reste autant que tu veux.",
            "narrateur|Le cacao laisse un rond sur le bois.",
        )
    if t2 == 1 and t3 == 3:
        return L(
            "narrateur|Après la pluie, ils glissent dans le fort.",
            "copine|On a regardé ensemble, d'abord.",
            "enfant-m|Puis tu as dit : on y va.",
            "maman|Deux nez, puis deux coussins.",
            "papa|Le salon redevient calme.",
            coda,
            "narrateur|Nina rit, tout petit.",
            "enfant-m|Le fort t'a attendue.",
            "narrateur|Dehors, le verre redevient net.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "narrateur|Sous la table, ça sent le bois.",
            "copine|Ton coussin est dans ma cave.",
            "enfant-m|Tu as dit oui.",
            "papa|Vous tenez tous les deux, là-dessous.",
            "maman|Le cacao descend jusqu'à vous.",
            coda,
            "narrateur|Nina tape deux fois, tout doux.",
            "enfant-m|C'est le signal.",
            "narrateur|Une miette dort près du pied de chaise.",
        )
    if t2 == 2 and t3 == 2:
        return L(
            "narrateur|La grande cave a deux coins, maintenant.",
            "enfant-m|Le tien, et le mien.",
            "copine|C'est le nôtre, Amir.",
            "papa|Vous avez mélangé sans tout casser.",
            "maman|Le cacao, au milieu, pour deux.",
            coda,
            "narrateur|Nina souffle, puis Amir souffle.",
            "enfant-m|On reste encore un peu.",
            "narrateur|Une chaise garde encore leur secret.",
        )
    if t2 == 2 and t3 == 3:
        return L(
            "narrateur|Deux jeux restent côte à côte.",
            "copine|Tu n'es pas entré, Amir.",
            "enfant-m|Tu avais dit non.",
            "papa|Le non a eu sa place.",
            "maman|Vous vous parlez encore, d'ici.",
            coda,
            "narrateur|Nina tend une main, sous la nappe.",
            "enfant-m|Je la prends, d'à côté.",
            "narrateur|Le bois craque, puis se tait.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "narrateur|Le petit jeu est déjà fini.",
            "copine|J'ai eu le temps, juste assez.",
            "enfant-m|Merci d'être restée.",
            "papa|Vous avez compté jusqu'à trois.",
            "maman|L'autre chaussure se ferme, maintenant.",
            coda,
            "narrateur|Nina fait un signe vers le salon.",
            "enfant-m|Le fort t'a vue, une minute.",
            "narrateur|Le paillasson garde une petite boue.",
        )
    if t2 == 3 and t3 == 2:
        return L(
            "narrateur|La porte se referme, tout doux.",
            "enfant-m|Je l'ai accompagnée.",
            "papa|Tu as marché à son pas.",
            "maman|Le manteau a pris le vent.",
            coda,
            "narrateur|Amir revient vers le salon.",
            "enfant-m|Le fort attendra.",
            "papa|Il a eu son au revoir.",
            "narrateur|Une goutte sèche encore sur le carreau.",
        )
    return L(
        "narrateur|Nina est partie, le fort reste allumé.",
        "enfant-m|Plus tard, elle a dit.",
        "enfant-m|Garde-le pour moi.",
        "papa|Tu as proposé une autre heure.",
        "maman|Le cacao attend, tout doux.",
        coda,
        "narrateur|Amir souffle sur le rond jaune.",
        "enfant-m|Il t'attend, Nina.",
        "narrateur|Le tapis garde encore sa chaleur.",
    )


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {"CHK_T0000_P0000": ""}

    s["CHK_T0000_P0000"] = L(
        "narrateur|La grande fenêtre a des gouttes.",
        "narrateur|Elles glissent, lentes, sur le verre.",
        "narrateur|Le tapis du salon est tiède.",
        "narrateur|Ça sent le cacao, tout proche.",
        "papa|Nina arrive bientôt, Amir.",
        "maman|Les coussins sont encore en tas.",
        "narrateur|En ce moment, Amir tire un coussin.",
        "enfant-m|Je veux un fort, pour Nina.",
        "narrateur|Le tissu tombe, tout mou.",
        "enfant-m|Elle va rentrer dedans.",
        "maman|On prépare le fort, alors ?",
        "papa|Merci, tu le tiens tout doux.",
    )
    s["CHK_T0001_P0000"] = L(
        "narrateur|Les affaires attendent près du tapis.",
        "narrateur|Le coussin, la couverture, et la lampe.",
        "maman|Tu prends quoi d'abord, Amir ?",
    )
    extras["CHK_T0001_P0000"] = t3lab("le coussin rouge", "la couverture bleue", "la petite lampe")

    for t1 in (1, 2, 3):
        p = f"CHK_T0001_P000{t1}"
        o = OBJ[t1]
        s[p] = t1_passage(t1)
        if t1 == 1:
            s[f"{p}_Q0001"] = L(
                "narrateur|Amir a posé le coussin rouge.",
                "maman|Il est où, maintenant ?",
            )
        elif t1 == 2:
            s[f"{p}_Q0001"] = L(
                "narrateur|Amir a enroulé la couverture bleue.",
                "maman|Elle est où, maintenant ?",
            )
        else:
            s[f"{p}_Q0001"] = L(
                "narrateur|La petite lampe éclaire encore.",
                "maman|Elle éclaire quoi, Amir ?",
            )
        extras[f"{p}_Q0001"] = qf(o["t1q"].split()[-1], o["t1acc"], o["t1retry"])
        s[f"{p}_C0001"] = t1_confirm(t1)
        s[f"{p}_T0002_P0000"] = t2_question()
        extras[f"{p}_T0002_P0000"] = t3lab("la fenêtre", "sous la table", "le couloir")

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
        "Amir veut un fort de coussins pour Nina. T1 = coussin rouge / couverture bleue / "
        "petite lampe (les trois restent). T2 = fenêtre (pluie) / sous la table (cave de Nina) / "
        "couloir (chaussures). T3 = neuf résolutions : attendre, proposer tout bas, s'asseoir ; "
        "glisser, mélanger, rester à côté (accepter le non) ; petit jeu, accompagner, plus tard. "
        "La leçon se vit : il propose, il accepte oui, non, ou une autre idée. Fin : cacao, fort, goutte.",
        "N1 ≤ 10. Tom et le slogan « Inviter sans forcer » jetés. "
        "Un merci de papa lié au geste (tenir le coussin). Audio non cuit.",
    )


if __name__ == "__main__":
    main()
