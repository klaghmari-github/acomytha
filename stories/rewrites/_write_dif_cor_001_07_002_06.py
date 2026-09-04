#!/usr/bin/env python3
"""Réécriture ATOM-DIF.COR.001-07 … 002-06 — récits, pas des leçons."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIMITS = {"N1": 10, "N2": 15, "N3": 16}
ROLES = {"narrateur", "papa", "maman", "enfant-m", "enfant-f", "copain", "copine"}
FORBIDDEN = (
    "on va apprendre",
    "voici le geste",
    "papa sourit",
    "maman sourit",
    "papa est là",
    "maman est là",
    "il était une fois",
    "ceci est l'histoire",
    "aujourd'hui,",
    "tu as fait du bon travail",
    "c'était du bon travail",
    "c'est du bon travail",
    "tu as mis ce que l'adulte a dit",
    "un chuchotement serre",
    "une étape après l'autre",
)
TROUPE = {
    "amir", "aniss", "sarah", "chouchou", "mila", "nino", "nina",
    "raphaël", "raphael", "victorino", "victorina", "papa", "maman",
}
NEED = {
    "ATOM-DIF.COR.001-07": ("tailles différentes", "jouer ensemble"),
    "ATOM-DIF.COR.001-08": ("tailles différentes", "jouer ensemble"),
    "ATOM-DIF.COR.002-01": ("corps n'est pas une blague", "on joue"),
    "ATOM-DIF.COR.002-02": ("corps n'est pas une blague", "on joue"),
    "ATOM-DIF.COR.002-03": ("corps n'est pas une blague", "on joue"),
    "ATOM-DIF.COR.002-04": ("corps n'est pas une blague", "on joue"),
    "ATOM-DIF.COR.002-05": ("corps n'est pas une blague", "on joue"),
    "ATOM-DIF.COR.002-06": ("corps n'est pas une blague", "on joue"),
}


def words(s: str) -> int:
    return len(s.replace("'", " ").replace("’", " ").replace("-", " ").split())


def from_script(lines: list[str]) -> tuple[str, str]:
    phrases, out = [], []
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        role, phrase = raw.split("|", 1)
        phrase = phrase.strip()
        out.append(f"{role}|{phrase}")
        phrases.append(phrase)
    return " ".join(phrases), "\n".join(out)


def lines_of(block: str) -> list[str]:
    return [ln.strip() for ln in block.strip().splitlines() if ln.strip()]


def make_chunk(src: dict, lines: list[str], sons, scale: float, rate: str) -> dict:
    text, script = from_script(lines)
    nc = dict(src)
    nc["text"] = text
    nc["script"] = script
    nc["text_ssml"] = text
    nc["sons"] = "" if sons in (None, "") else sons
    nc["length_scale_piper"] = scale
    nc["rate_label"] = rate
    return nc


def check(sid: str, age: str, chunks: list[dict]) -> None:
    lim = LIMITS[age]
    joined = "\n".join(c["script"] for c in chunks)
    low = joined.lower()
    for bad in FORBIDDEN:
        if bad in low:
            raise SystemExit(f"{sid} interdit: {bad}")
    for ln in joined.splitlines():
        role, phrase = ln.split("|", 1)
        for tok in phrase.replace("'", " ").replace("’", " ").replace("-", " ").split():
            t = tok.lower().strip(".,!?;:«»\"")
            if t and t[0].isalpha() and t[0].isupper() is False:
                pass
        # prénoms hors troupe : mots capitalisés dans le script original
    import re
    for m in re.findall(r"(?:^|\n)(?:enfant-m|enfant-f|copain|copine|papa|maman|narrateur)\|([^.\n]+)", joined):
        pass
    # scan capitalised names in phrases
    for ln in joined.splitlines():
        phrase = ln.split("|", 1)[1]
        for w in re.findall(r"\b[A-ZÉÈÊÀÂÎÔÛŸ][\w'-]*\b", phrase):
            if w.lower() not in TROUPE and w not in {"Oui", "Non", "Oh", "Encore", "Merci", "Bravo", "Voilà", "Dedans", "Attends", "Toi", "Moi", "Nous", "Vous", "Puis", "Avec", "Pour", "Dans", "Sous", "Sur", "Une", "Un", "Le", "La", "Les", "Des", "Du", "De", "Au", "Aux", "Et", "Il", "Elle", "Ils", "Elles", "Je", "Tu", "On", "Ça", "Ce", "Cette", "Ces", "Mon", "Ma", "Mes", "Ton", "Ta", "Tes", "Son", "Sa", "Ses", "Notre", "Nos", "Votre", "Vos", "Leur", "Leurs", "Ici", "Là", "Après", "Avant", "Maintenant", "Plus", "Très", "Tout", "Toute", "Tous", "Toutes", "Deux", "Trois", "Quatre", "Cinq", "Six", "Sept", "Huit", "Neuf", "Dix", "Un", "Deux"}:
                # allow common sentence starts
                if w.lower() in TROUPE:
                    continue
    adults = [ln for ln in joined.splitlines() if ln.startswith("papa|") or ln.startswith("maman|")]
    if not adults:
        raise SystemExit(f"{sid}: aucun papa/maman")
    if not any("?" in a for a in adults):
        raise SystemExit(f"{sid}: aucune question d'adulte")
    if "en ce moment" not in low:
        raise SystemExit(f"{sid}: manque en ce moment")
    if "l'histoire est finie." not in low:
        raise SystemExit(f"{sid}: manque fin")
    all_text = " ".join(c["text"] for c in chunks).lower()
    for m in NEED[sid]:
        if m.lower() not in all_text:
            raise SystemExit(f"{sid}: message manquant: {m}")
    first = chunks[0]["script"].splitlines()[0].split("|", 1)[1]
    nwords = sum(words(c["text"]) for c in chunks)
    if nwords < 380:
        raise SystemExit(f"{sid}: trop court ({nwords} mots)")
    overflows = []
    for c in chunks:
        rebuilt, _ = from_script(c["script"].splitlines())
        if rebuilt != c["text"]:
            raise SystemExit(f"{sid} {c['chunk_id']}: text ≠ script")
        for ln in c["script"].splitlines():
            if "|" not in ln:
                raise SystemExit(f"{sid} ligne sans | : {ln}")
            role, phrase = ln.split("|", 1)
            if role not in ROLES:
                raise SystemExit(f"{sid} rôle {role}")
            n = words(phrase)
            if n > lim:
                overflows.append(f"{c['chunk_id']} {n}>{lim}: {phrase}")
            if n == 0:
                raise SystemExit(f"{sid} phrase vide")
            if not phrase.endswith((".", "?", "!")):
                raise SystemExit(f"{sid} sans ponctuation: {phrase}")
            if phrase.count(".") + phrase.count("?") + phrase.count("!") > 1:
                raise SystemExit(f"{sid} plusieurs phrases: {phrase}")
    if overflows:
        raise SystemExit(f"{sid} trop long:\n" + "\n".join(overflows))
    print(f"OK {sid} {nwords} mots  1re: {first}")


def write_story(sid: str, fil: str, title: str, chars: str, setting: str,
                scripts: dict, q: dict, scales: dict, rates: dict, sons: dict) -> None:
    folder = ROOT / sid
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"{sid} chunks missing={missing} extra={extra}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        by[cid] = make_chunk(
            c,
            lines_of(scripts[cid]),
            sons.get(cid, ""),
            scales.get(cid, 1.22),
            rates.get(cid, "medium"),
        )
    qc = by["CHK_T0000_P0000_Q0001"]
    for k, v in q.items():
        qc[k] = v
    out = dict(src)
    out["fil_rouge"] = fil
    out["title"] = title
    out["characters"] = chars
    out["setting"] = setting
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(sid, out["age_band"], out["chunks"])
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def S(n1=1.28, n2=1.22):
    return {
        "CHK_T0000_P0000": n2,
        "CHK_T0000_P0000_Q0001": n1,
        "CHK_T0000_P0000_C0001": n2,
        "CHK_T0000_P0000_END": n2,
        "CHK_T0000_P0000_END_F0001": n2,
    }


def R(q="slow", rest="medium"):
    return {
        "CHK_T0000_P0000": rest,
        "CHK_T0000_P0000_Q0001": q,
        "CHK_T0000_P0000_C0001": rest,
        "CHK_T0000_P0000_END": rest,
        "CHK_T0000_P0000_END_F0001": "slow",
    }


# ---------------------------------------------------------------------------
# 001-07 N2 — cour, figuier, boutique d'oranges
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.COR.001-07",
    "Victorina veut une boutique d'oranges dans la cour. L'enseigne est trop haute. Elle invite Aniss. Ils ont des tailles différentes. Ils ouvrent le magasin, ensemble.",
    "Les caisses d'oranges de Victorina",
    "Victorina, Aniss, maman",
    "cour après le marché",
    {
        "CHK_T0000_P0000": """
narrateur|La figue trop mûre a taché la pierre.
narrateur|Une odeur d'orange reste dans la cour.
narrateur|Les caisses du marché sont empilées.
narrateur|Le store de toile claque un peu.
narrateur|Une guêpe tourne près d'une écorce.
narrateur|L'ombre du figuier est fraîche.
narrateur|Maman pose un panier contre le mur.
maman|Tu as vu les caisses, Victorina ?
enfant-f|Oui, maman.
enfant-f|Elles sentent encore l'orange.
maman|Il en reste trois, au fond.
narrateur|En ce moment, Victorina tire une caisse.
narrateur|Le bois est rêche et chaud.
enfant-f|Je veux une boutique.
enfant-f|Une boutique d'oranges.
maman|Tu veux un magasin, ici ?
enfant-f|Oui.
enfant-f|Avec une enseigne.
narrateur|Victorina a un papier.
narrateur|Dessus, une orange un peu penchée.
narrateur|Elle veut l'accrocher tout en haut.
narrateur|La caisse du haut est trop haute.
narrateur|Ses doigts touchent seulement le bord.
enfant-f|Oh.
enfant-f|Je n'arrive pas.
narrateur|Aniss arrive dans la cour.
narrateur|Ses sandales font un bruit sec.
narrateur|Aniss est plus grand.
narrateur|Victorina est plus petite.
narrateur|Ils ont des tailles différentes.
maman|Aniss est là.
maman|Tu veux l'inviter ?
enfant-f|Aniss, tu veux la boutique ?
copain|Oui.
narrateur|Ils poussent deux caisses.
narrateur|Aniss porte la grande.
narrateur|Victorina pousse la petite.
maman|On peut jouer ensemble.
maman|Vous jouez ensemble ?
enfant-f|Oui.
copain|Oui.
narrateur|Le papier attend encore par terre.
enfant-f|L'enseigne, Aniss.
enfant-f|Elle va tout en haut.
""",
        "CHK_T0000_P0000_Q0001": """
narrateur|Victorina invite Aniss.
narrateur|Que font-ils ?
""",
        "CHK_T0000_P0000_C0001": """
narrateur|Aniss tend le bras.
narrateur|Il pose le papier sur la caisse.
narrateur|L'orange dessinée regarde la cour.
enfant-f|La boutique est ouverte !
maman|Bravo, Aniss.
maman|Tu as mis l'enseigne.
narrateur|Victorina s'assoit derrière la petite caisse.
narrateur|C'est le comptoir.
narrateur|Elle aligne les trois oranges.
narrateur|Une orange roule sous la pile.
enfant-f|Elle est partie.
copain|Je ne la vois plus.
narrateur|Victorina se glisse près du bois.
narrateur|Elle est plus petite.
narrateur|Elle attrape l'orange.
enfant-f|Te voilà.
maman|Chacun aide, à sa taille.
maman|Vous jouez ensemble.
narrateur|Maman prend une pièce imaginaire.
maman|Une orange, s'il te plaît.
enfant-f|Voilà.
narrateur|Victorina tend le fruit.
narrateur|Il est lisse et un peu froid.
maman|Merci, marchande.
copain|Et moi, le sac ?
narrateur|Aniss tient le panier.
narrateur|Victorina pose l'orange dedans.
narrateur|La guêpe s'éloigne de l'écorce.
""",
        "CHK_T0000_P0000_END": """
maman|On ferme la boutique ?
enfant-f|Encore un client.
copain|Moi.
narrateur|Aniss achète la dernière orange.
narrateur|Il fait semblant de croquer.
copain|Elle est sucrée.
enfant-f|C'est la plus belle.
maman|Vous avez des tailles différentes.
maman|Et vous avez joué ensemble.
narrateur|Victorina range le papier dans la caisse.
narrateur|Aniss empile le bois.
maman|Tu as fini de ranger le papier ?
enfant-f|Oui, maman.
narrateur|L'ombre du figuier a bougé.
narrateur|La tache de figue est encore là.
""",
        "CHK_T0000_P0000_END_F0001": """
enfant-f|On a ouvert la boutique.
copain|L'enseigne était en haut.
maman|Vous avez joué ensemble.
narrateur|La cour sent encore l'orange.
narrateur|L'histoire est finie.
""",
    },
    {
        "expected_answer": "jouer ensemble",
        "accepted_examples": "jouer ensemble | ensemble | ils jouent | on joue | jouer | la boutique",
        "retry_prompt": "Ils jouent ensemble. Que font Victorina et Aniss ?",
    },
    S(),
    R(),
    {"CHK_T0000_P0000": ""},
)

# ---------------------------------------------------------------------------
# 001-08 N1 — salon, train de coussins, lune
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.COR.001-08",
    "Sarah veut un train de coussins jusqu'à la porte. Un coussin est coincé. Victorino est plus grand. Sarah est plus petite. Ils vont voir la lune, ensemble.",
    "Le train de coussins de Sarah",
    "Sarah, Victorino, maman",
    "salon puis porte du jardin",
    {
        "CHK_T0000_P0000": """
narrateur|La vapeur de la soupe colle à la vitre.
narrateur|Une cuillère en bois attend.
narrateur|Ça sent le thym, tout chaud.
narrateur|Le canapé a trois coussins.
narrateur|Un papillon de nuit tape la lampe.
narrateur|Le tapis est un peu rêche.
maman|Tu as vu la buée, Sarah ?
enfant-f|Oui.
enfant-f|On dirait un nuage.
narrateur|En ce moment, Sarah tire un coussin.
narrateur|Le tissu est doux et lourd.
enfant-f|Je veux un train.
enfant-f|Jusqu'à la porte.
maman|Un train de coussins ?
enfant-f|Oui.
enfant-f|Pour voir la lune.
narrateur|Sarah pose un coussin.
narrateur|Le tissu fait un petit bruit.
narrateur|Puis un autre.
narrateur|Le troisième manque.
enfant-f|Il est où ?
maman|Regarde sous la table.
narrateur|Le coussin est coincé.
narrateur|Sarah tend le bras.
narrateur|Ses doigts touchent le tissu.
narrateur|Le coussin ne vient pas.
enfant-f|Oh.
narrateur|Victorino arrive du couloir.
narrateur|Ses chaussettes glissent un peu.
narrateur|Victorino est plus grand.
narrateur|Sarah est plus petite.
narrateur|Ils ont des tailles différentes.
maman|Victorino est là.
maman|Tu l'invites ?
enfant-f|Tu veux le train ?
copain|Oui.
narrateur|Ils se mettent à quatre pattes.
""",
        "CHK_T0000_P0000_Q0001": """
narrateur|Sarah invite Victorino.
narrateur|Que font-ils ?
""",
        "CHK_T0000_P0000_C0001": """
narrateur|Victorino soulève un peu la table.
narrateur|Sarah tire le coussin.
narrateur|Le coussin sort, tout chaud.
enfant-f|Je l'ai !
maman|Bravo, Sarah.
maman|On peut jouer ensemble.
maman|Vous jouez ensemble.
narrateur|Ils posent le troisième coussin.
narrateur|Le train va jusqu'à la porte.
enfant-f|Tout le monde à bord.
copain|Moi devant.
enfant-f|Moi au milieu.
narrateur|Ils s'assoient sur le tissu.
narrateur|Le tapis gratte un peu.
enfant-f|Toc, toc.
copain|Le train part.
maman|Le loquet est un peu haut.
narrateur|Victorino tourne le loquet.
narrateur|Sarah pousse le dernier coussin.
narrateur|La porte s'ouvre un peu.
narrateur|L'air du jardin entre.
enfant-f|La lune !
copain|Elle est ronde.
maman|Oui.
maman|Elle vous attendait.
""",
        "CHK_T0000_P0000_END": """
narrateur|Ils restent sur le dernier coussin.
narrateur|La lune éclaire le seuil.
narrateur|Un peu d'air touche les cheveux.
enfant-f|Elle est froide, la lune.
maman|On range le train ?
enfant-f|Encore un voyage.
copain|Un tout petit.
narrateur|Ils reculent d'un coussin.
narrateur|Puis ils avancent encore.
maman|Vous avez des tailles différentes.
maman|Et vous avez joué ensemble.
maman|Tu as fini le voyage ?
enfant-f|Oui, maman.
narrateur|Sarah pose un coussin sur le canapé.
narrateur|Victorino pose les deux autres.
maman|Merci, Victorino.
narrateur|La vapeur a quitté la vitre.
narrateur|Le thym sent encore un peu.
""",
        "CHK_T0000_P0000_END_F0001": """
enfant-f|On a vu la lune.
copain|Avec le train.
maman|Vous avez joué ensemble.
narrateur|Le thym sent encore un peu.
narrateur|L'histoire est finie.
""",
    },
    {
        "expected_answer": "jouer ensemble",
        "accepted_examples": "jouer ensemble | ensemble | ils jouent | on joue | jouer | le train",
        "retry_prompt": "Ils jouent ensemble. Que font Sarah et Victorino ?",
    },
    S(n1=1.4, n2=1.28),
    R(q="slow", rest="slow"),
    {},
)

# ---------------------------------------------------------------------------
# 002-01 N2 — cuisine dimanche, cabane de biscuits
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.COR.002-01",
    "Nino veut une cabane de biscuits au citron. Aniss arrive. Un rire commence. Papa dit : le corps n'est pas une blague. Ils bâtissent le toit, ensemble.",
    "La cabane de biscuits de Nino",
    "Nino, Aniss, papa",
    "cuisine le dimanche",
    {
        "CHK_T0000_P0000": """
narrateur|La casserole de cuivre fait tic sur le feu.
narrateur|Des zestes de citron brillent sur la planche.
narrateur|Une coquille d'œuf est encore collée.
narrateur|Ça sent le beurre tiède.
narrateur|Le carrelage est froid sous les pieds.
narrateur|Un torchon à carreaux pend.
papa|Tu as vu le citron, Nino ?
enfant-m|Oui, papa.
enfant-m|Il pique le nez.
papa|On fait des biscuits.
narrateur|En ce moment, Nino pose un biscuit plat.
narrateur|Il en pose un autre à côté.
enfant-m|Je veux une cabane.
enfant-m|Une cabane de biscuits.
papa|Avec un toit ?
enfant-m|Oui.
enfant-m|Un grand toit.
narrateur|Aniss arrive.
narrateur|Il enlève ses chaussures.
narrateur|Ses chaussettes sont jaunes.
narrateur|Papa tend deux tabliers.
narrateur|Le tablier d'Aniss tombe autrement.
narrateur|Aniss a un corps plus rond.
narrateur|Nino a un corps plus mince.
narrateur|Un petit rire commence.
papa|Le corps n'est pas une blague.
papa|On joue.
papa|On cuisine.
narrateur|Nino ferme la bouche.
narrateur|Il hoche la tête.
enfant-m|On fait la cabane.
copain|Oui.
narrateur|La pâte est froide et un peu collante.
narrateur|Elle sent le citron.
narrateur|Un peu de farine reste sur la planche.
enfant-m|Aniss, tu tiens le mur ?
copain|Je le tiens.
papa|Tout doux, les murs.
""",
        "CHK_T0000_P0000_Q0001": """
narrateur|Le corps n'est pas une blague.
narrateur|Que fait-on ?
""",
        "CHK_T0000_P0000_C0001": """
narrateur|Ils collent deux biscuits debout.
narrateur|Un peu de pâte sert de colle.
narrateur|Nino pose le grand biscuit du toit.
narrateur|Le toit glisse.
enfant-m|Il tombe.
copain|Encore.
papa|On recommence, tout doux.
narrateur|Aniss tient les murs.
narrateur|Nino pose le toit plus lentement.
narrateur|Cette fois, ça tient.
enfant-m|Une porte.
copain|Une fenêtre.
narrateur|Ils percent un petit trou.
narrateur|Le citron sent plus fort.
papa|Bravo, Nino.
papa|Tu as posé le toit.
papa|Vous jouez.
narrateur|Papa glisse un sucre sur le toit.
papa|Une cheminée.
enfant-m|Elle est petite.
copain|Elle est belle.
narrateur|Nino tapote le toit du doigt.
narrateur|Le biscuit tient.
papa|L'amitié ne dépend pas de la forme.
papa|On joue.
""",
        "CHK_T0000_P0000_END": """
papa|On goûte la porte ?
enfant-m|Oui.
narrateur|Nino casse un tout petit bout.
narrateur|Aniss casse l'autre bout.
enfant-m|C'est sucré.
copain|Et citron.
papa|Tu as fini de goûter ?
enfant-m|Oui, papa.
narrateur|Il reste les murs et le toit.
narrateur|La casserole ne fait plus tic.
papa|On essuie la planche ?
copain|Oui.
narrateur|Nino tient le torchon.
narrateur|Aniss tient l'autre bout.
narrateur|Le citron brille encore un peu.
narrateur|La cabane reste au milieu de la table.
""",
        "CHK_T0000_P0000_END_F0001": """
enfant-m|On a fait une cabane.
copain|Le toit est resté.
papa|Vous avez joué.
narrateur|La cuisine sent le citron.
narrateur|L'histoire est finie.
""",
    },
    {
        "expected_answer": "jouer",
        "accepted_examples": "jouer | on joue | pas une blague | pas blague | la cabane | on cuisine",
        "retry_prompt": "On joue. Le corps n'est pas une blague. Que fait-on ?",
    },
    S(),
    R(),
    {},
)

# ---------------------------------------------------------------------------
# 002-02 N3 — cheval de bois sous la haie, écurie d'argile
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.COR.002-02",
    "Amir cherche son cheval de bois sous la haie. Victorino l'aide. Un rire commence. Maman dit : le corps n'est pas une blague. Sur la véranda, ils font une écurie d'argile.",
    "Le cheval de bois sous la haie",
    "Amir, Victorino, maman",
    "chemin du village puis véranda",
    {
        "CHK_T0000_P0000": """
narrateur|La poussière du chemin sent encore le soleil.
narrateur|La haie de buis est chaude et serrée.
narrateur|Une abeille va d'une fleur à l'autre.
narrateur|Le portail de fer est tiède.
narrateur|Un caillou blanc brille dans l'ornière.
maman|Tu as vu le portail, Amir ?
enfant-m|Il est chaud.
maman|Oui.
maman|Le soleil l'a touché.
narrateur|En ce moment, Amir cherche dans l'herbe.
narrateur|L'herbe est sèche et un peu piquante.
enfant-m|Mon cheval de bois.
enfant-m|Il a roulé.
maman|Regarde sous la haie.
narrateur|Victorino arrive près du portail.
narrateur|Ses genoux ont déjà de la poussière.
narrateur|Victorino a un corps plus rond.
narrateur|Amir a un corps plus mince.
narrateur|Les corps ont des formes différentes.
narrateur|Un petit rire commence.
maman|Le corps n'est pas une blague.
maman|On joue.
narrateur|Amir ferme la bouche.
enfant-m|On cherche le cheval ?
copain|On cherche.
narrateur|Ils écartent une branche.
narrateur|Les feuilles sentent le vert.
narrateur|Un caillou roule.
enfant-m|Pas lui.
narrateur|Le bois du cheval apparaît.
enfant-m|Te voilà.
copain|Il a de la terre au nez.
maman|On va le laver à la maison.
""",
        "CHK_T0000_P0000_Q0001": """
narrateur|Le corps n'est pas une blague.
narrateur|Que fait-on ?
""",
        "CHK_T0000_P0000_C0001": """
narrateur|Sur la véranda, l'argile attend.
narrateur|Elle est froide et un peu grise.
narrateur|Amir lave le cheval.
narrateur|L'eau fait un filet brun.
narrateur|Le bois redevient lisse.
enfant-m|Il est propre.
maman|Il a besoin d'une écurie.
copain|On la fait.
narrateur|Ils pressent l'argile.
narrateur|Ça fait un bruit mou.
narrateur|Amir dresse un mur.
narrateur|Victorino dresse l'autre mur.
narrateur|Un mur s'affaisse.
enfant-m|Il est fatigué.
maman|On le tient ensemble.
narrateur|Victorino appuie tout doux.
narrateur|Amir pose un toit plat.
narrateur|Le cheval entre dans l'écurie.
narrateur|Sa jambe de bois touche l'argile.
copain|Il est à la maison.
maman|Bravo, Amir.
maman|Tu as trouvé le cheval.
maman|Vous jouez.
maman|L'amitié ne dépend pas de la forme.
""",
        "CHK_T0000_P0000_END": """
maman|On laisse sécher ?
enfant-m|Oui.
narrateur|L'argile devient un peu plus claire.
narrateur|Le cheval de bois attend dessous.
copain|Il dort.
enfant-m|Tout petit.
maman|Tu as fini de presser l'argile ?
enfant-m|Oui, maman.
narrateur|Ils se lavent les mains.
narrateur|L'eau est tiède.
narrateur|Dehors, le portail est encore chaud.
narrateur|Une abeille passe encore près de la haie.
maman|On le touchera demain.
enfant-m|Merci, Victorino.
copain|Merci, Amir.
""",
        "CHK_T0000_P0000_END_F0001": """
enfant-m|On a trouvé le cheval.
copain|On a fait l'écurie.
maman|Vous avez joué.
narrateur|La haie garde un peu de poussière.
narrateur|L'histoire est finie.
""",
    },
    {
        "expected_answer": "jouer",
        "accepted_examples": "jouer | on joue | pas une blague | pas blague | le cheval | l'écurie",
        "retry_prompt": "On joue. Le corps n'est pas une blague. Que fait-on ?",
    },
    S(n1=1.24, n2=1.12),
    R(q="medium", rest="medium"),
    {},
)

# ---------------------------------------------------------------------------
# 002-03 N3 — guirlande d'anniversaire
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.COR.002-03",
    "Mila veut une guirlande de papier pour l'anniversaire de papa. Nino arrive. Le corps n'est pas une blague. Un anneau se déchire. Ils allongent la guirlande, ensemble.",
    "La guirlande d'anniversaire de Mila",
    "Mila, Nino, papa",
    "salle à manger le matin",
    {
        "CHK_T0000_P0000": """
narrateur|Les volets laissent un rai de poussière d'or.
narrateur|Un tiroir de papiers est ouvert.
narrateur|Ça sent la colle, un peu sucré.
narrateur|Un fil pend du buffet.
narrateur|Une paire de ciseaux attend sur le bois.
narrateur|La chaise a un fil qui dépasse.
papa|Tu as vu le rai de soleil, Mila ?
enfant-f|Il est tout fin.
papa|Oui.
papa|Il traverse la salle.
narrateur|En ce moment, Mila coupe un rectangle.
narrateur|Les ciseaux font un petit cri.
narrateur|Le papier est rouge et un peu rêche.
enfant-f|C'est pour toi, papa.
enfant-f|Une guirlande.
papa|Jusqu'à la fenêtre ?
enfant-f|Oui.
enfant-f|Tout le chemin.
narrateur|Nino arrive avec des chaussettes silencieuses.
narrateur|Nino a un corps plus rond.
narrateur|Mila a un corps plus mince.
narrateur|Mila ne commente pas le corps.
papa|Le corps n'est pas une blague.
papa|On joue.
enfant-f|Nino, tu veux coller ?
copain|Oui.
narrateur|Ils collent le premier anneau.
narrateur|Le papier frotte entre les doigts.
narrateur|Puis le deuxième.
narrateur|La colle est froide aux doigts.
enfant-f|Elle est longue ?
papa|Pas encore assez.
""",
        "CHK_T0000_P0000_Q0001": """
narrateur|Le corps n'est pas une blague.
narrateur|Que fait-on ?
""",
        "CHK_T0000_P0000_C0001": """
narrateur|Ils ajoutent des anneaux.
narrateur|Un anneau rouge se déchire.
enfant-f|Oh.
copain|On le répare.
narrateur|Nino tient les deux bords.
narrateur|Mila met un point de colle.
narrateur|L'anneau redevient rond.
papa|Bravo, Mila.
papa|Tu as réparé.
papa|Vous jouez.
narrateur|La guirlande arrive au milieu.
narrateur|Elle pèse un peu, toute douce.
narrateur|Il manque encore un bout.
enfant-f|Encore trois.
copain|Encore trois.
narrateur|Ils collent.
narrateur|Le papier fait un petit bruit.
narrateur|Un anneau jaune s'ajoute au rouge.
enfant-f|Le jaune, c'est le soleil.
copain|Le rouge, c'est la fête.
narrateur|Papa tient un bout près du buffet.
narrateur|Mila tient l'autre bout.
narrateur|Nino pose le dernier anneau.
narrateur|La guirlande touche la fenêtre.
enfant-f|Elle est arrivée.
papa|L'amitié ne dépend pas de la forme.
papa|On joue.
""",
        "CHK_T0000_P0000_END": """
papa|On la regarde un moment ?
enfant-f|Oui.
narrateur|Le rai de soleil traverse un anneau.
narrateur|Le rouge devient plus clair.
copain|Il brille.
enfant-f|C'est ton cadeau.
papa|Merci.
papa|Tu as fini de coller ?
enfant-f|Oui, papa.
narrateur|Ils essuient la colle sur le torchon.
narrateur|Le torchon devient un peu dur.
narrateur|Le tiroir se referme.
narrateur|La salle sent encore le papier.
papa|Plus tard, le gâteau.
enfant-f|Merci, Nino.
copain|Merci, Mila.
""",
        "CHK_T0000_P0000_END_F0001": """
enfant-f|On a tendu la guirlande.
copain|Jusqu'à la fenêtre.
papa|Vous avez joué.
narrateur|Le rai de soleil reste dans le rouge.
narrateur|L'histoire est finie.
""",
    },
    {
        "expected_answer": "jouer",
        "accepted_examples": "jouer | on joue | pas une blague | pas blague | la guirlande | coller",
        "retry_prompt": "On joue. Le corps n'est pas une blague. Que fait-on ?",
    },
    S(n1=1.24, n2=1.12),
    R(q="medium", rest="medium"),
    {},
)

# ---------------------------------------------------------------------------
# 002-04 N3 — fraises, tarte
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.COR.002-04",
    "Nina veut assez de fraises pour une tarte. Victorino cueille avec elle. Un rire commence au robinet. Papa dit : le corps n'est pas une blague. Ils étendent la pâte, ensemble.",
    "Les fraises de Nina",
    "Nina, Victorino, papa",
    "jardin des fraisiers puis cuisine",
    {
        "CHK_T0000_P0000": """
narrateur|Une fraise cache une goutte sous sa feuille.
narrateur|La terre est fraîche et un peu noire.
narrateur|Un escargot avance sur une barquette.
narrateur|L'arrosoir est couché, vide.
narrateur|Ça sent le vert et le sucre.
papa|Tu as vu la goutte, Nina ?
enfant-f|Elle brille.
papa|Oui.
papa|Elle tient à la feuille.
narrateur|En ce moment, Nina soulève une feuille.
narrateur|La feuille est rêche et un peu poussiéreuse.
narrateur|Une petite bête se cache, puis part.
enfant-f|Je veux une tarte.
enfant-f|Avec beaucoup de fraises.
papa|On en cueille d'abord.
narrateur|Victorino arrive entre les rangs.
narrateur|Ses mains sont déjà un peu rouges.
narrateur|Victorino a un corps plus rond.
narrateur|Nina a un corps plus mince.
narrateur|Nina ouvre la bouche.
narrateur|Un petit rire commence.
papa|Le corps n'est pas une blague.
papa|On joue.
papa|On cueille.
narrateur|Nina ferme la bouche.
enfant-f|On cueille.
copain|On cueille.
narrateur|Ils posent les fraises dans la barquette.
narrateur|Le bois de la barquette est rêche.
narrateur|Une feuille colle au poignet de Nina.
enfant-f|Elle pique.
papa|C'est la feuille.
enfant-f|Il en faut encore.
papa|Le plant du fond en a.
""",
        "CHK_T0000_P0000_Q0001": """
narrateur|Le corps n'est pas une blague.
narrateur|Que fait-on ?
""",
        "CHK_T0000_P0000_C0001": """
narrateur|Au robinet, l'eau est froide.
narrateur|Les fraises deviennent plus brillantes.
narrateur|Une goutte mouille la chemise de Victorino.
copain|Elle est froide.
papa|On rit de l'eau.
papa|On joue.
narrateur|Dans la cuisine, la pâte attend.
narrateur|Elle est molle et un peu collante.
enfant-f|On l'étale.
copain|Moi le rouleau.
narrateur|Victorino tient un bout.
narrateur|Nina tient l'autre bout.
narrateur|La pâte devient un tapis.
narrateur|Nina pose les fraises.
narrateur|Elles font un petit cercle rouge.
narrateur|Victorino en pose aussi.
papa|Bravo, Nina.
papa|Tu as rempli la tarte.
papa|Vous jouez.
papa|L'amitié ne dépend pas de la forme.
narrateur|Papa met la tarte au chaud.
narrateur|La porte du four fait un petit clac.
enfant-f|Elle va sentir bon.
copain|Très bon.
""",
        "CHK_T0000_P0000_END": """
narrateur|Ils attendent près de la fenêtre.
narrateur|Dehors, l'escargot a avancé.
enfant-f|Il va loin.
papa|Tout doux, comme nous.
papa|Tu as fini d'attendre un moment ?
enfant-f|Oui, papa.
narrateur|La tarte sort.
narrateur|Ça sent le sucre chaud.
narrateur|Le bord est un peu doré.
narrateur|Nina souffle un peu.
narrateur|Victorino souffle aussi.
papa|On goûte le bord ?
copain|Oui.
enfant-f|C'est doux.
copain|Encore un peu.
papa|Merci d'avoir cueilli.
""",
        "CHK_T0000_P0000_END_F0001": """
enfant-f|On a fait la tarte.
copain|Avec les fraises.
papa|Vous avez joué.
narrateur|Une feuille de fraisier tremble encore.
narrateur|L'histoire est finie.
""",
    },
    {
        "expected_answer": "jouer",
        "accepted_examples": "jouer | on joue | pas une blague | pas blague | cueillir | la tarte",
        "retry_prompt": "On joue. Le corps n'est pas une blague. Que fait-on ?",
    },
    S(n1=1.24, n2=1.12),
    R(q="medium", rest="medium"),
    {},
)

# ---------------------------------------------------------------------------
# 002-05 N3 — cabane de draps
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.COR.002-05",
    "Raphaël veut une cabane avec le drap qui sent le soleil. Aniss arrive. Le corps n'est pas une blague. Le drap est trop court. Ils ajoutent un torchon et s'installent dedans.",
    "La cabane de draps de Raphaël",
    "Raphaël, Aniss, papa",
    "salon l'après-midi",
    {
        "CHK_T0000_P0000": """
narrateur|Un drap sent encore le fil et le soleil.
narrateur|Il sèche sur le dossier d'une chaise.
narrateur|Une pince à linge tient un coin.
narrateur|La pince est en bois, un peu ronde.
narrateur|Un rai de poussière traverse le salon.
narrateur|L'horloge fait un tic lent.
narrateur|Une mouche se pose sur la vitre.
narrateur|Le tapis garde un carré de soleil.
papa|Tu as senti le drap, Raphaël ?
enfant-m|Il sent dehors.
papa|Oui.
papa|Le soleil l'a séché.
narrateur|En ce moment, Raphaël tire deux chaises.
narrateur|Les pieds des chaises râpent le bois.
enfant-m|Je veux une cabane.
enfant-m|Avec le drap.
papa|Au milieu du salon ?
enfant-m|Oui.
narrateur|Aniss arrive.
narrateur|Il a encore une chaussette un peu tordue.
narrateur|Aniss a un corps plus rond.
narrateur|Raphaël a un corps plus mince.
narrateur|Raphaël ne commente pas le corps.
papa|Le corps n'est pas une blague.
papa|On joue.
enfant-m|Aniss, tu tiens la chaise ?
copain|Je la tiens.
narrateur|Ils jettent le drap par-dessus.
narrateur|Le drap tombe en biais.
narrateur|Le drap est trop court.
enfant-m|Il y a un trou.
papa|On cherche un torchon.
narrateur|Le torchon sent encore la vaisselle.
""",
        "CHK_T0000_P0000_Q0001": """
narrateur|Le corps n'est pas une blague.
narrateur|Que fait-on ?
""",
        "CHK_T0000_P0000_C0001": """
narrateur|Papa tend un torchon à carreaux.
narrateur|Raphaël le pince au bord du drap.
narrateur|Le trou se ferme.
copain|On entre ?
enfant-m|On entre.
narrateur|Ils se glissent dessous.
narrateur|La lumière devient jaune.
narrateur|Le drap sent encore le soleil.
narrateur|On entend l'horloge, plus loin.
enfant-m|On est dedans.
copain|C'est chaud.
papa|Deux biscuits, pour les capitaines.
narrateur|Papa passe les biscuits sous le bord.
narrateur|Ça croque tout doux.
narrateur|Une miette tombe sur le tapis.
papa|Bravo, Raphaël.
papa|Tu as fermé le trou.
papa|Vous jouez.
papa|L'amitié ne dépend pas de la forme.
narrateur|Une chaise glisse un peu.
enfant-m|Attends.
narrateur|Aniss la recale.
narrateur|La cabane tient.
enfant-m|Elle est solide.
""",
        "CHK_T0000_P0000_END": """
papa|On reste encore un peu ?
enfant-m|Oui.
copain|Un peu.
narrateur|L'horloge tic plus loin.
narrateur|La mouche a quitté la vitre.
papa|Tu as fini tes biscuits ?
enfant-m|Oui, papa.
narrateur|Ils sortent à reculons.
narrateur|Le salon redevient grand.
narrateur|Le rai de poussière est encore là.
narrateur|Raphaël plie le drap.
narrateur|Aniss plie le torchon.
enfant-m|Merci, Aniss.
copain|Merci, Raphaël.
papa|Le drap sent encore le soleil.
narrateur|La pince à linge reste sur la chaise.
""",
        "CHK_T0000_P0000_END_F0001": """
enfant-m|On a fait la cabane.
copain|On a mangé dedans.
papa|Vous avez joué.
narrateur|Le drap garde un peu de jaune.
narrateur|L'histoire est finie.
""",
    },
    {
        "expected_answer": "jouer",
        "accepted_examples": "jouer | on joue | pas une blague | pas blague | la cabane",
        "retry_prompt": "On joue. Le corps n'est pas une blague. Que fait-on ?",
    },
    S(n1=1.24, n2=1.12),
    R(q="medium", rest="medium"),
    {},
)

# ---------------------------------------------------------------------------
# 002-06 N2 — lanternes de pots, perron
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.COR.002-06",
    "Chouchou veut des lanternes de papier dans deux pots. Mila arrive. Un rire commence. Papa dit : le corps n'est pas une blague. Un couvercle résiste. Ils les lèvent vers le dernier soleil.",
    "Les lanternes de Chouchou",
    "Chouchou, Mila, papa",
    "perron au crépuscule",
    {
        "CHK_T0000_P0000": """
narrateur|La pierre du perron garde la chaleur du jour.
narrateur|Deux pots de confiture attendent, vides.
narrateur|Un reste de sucre brille au fond.
narrateur|Un grillon commence, tout près.
narrateur|La fenêtre de la cuisine est jaune.
narrateur|Une casserole cliquette, très loin.
narrateur|Ça sent l'herbe coupée.
narrateur|Un papillon de nuit tourne.
narrateur|Le ciel devient un peu violet.
papa|Tu as senti la pierre, Chouchou ?
enfant-m|Elle est encore chaude.
papa|Oui.
papa|Le soleil l'a gardée.
narrateur|En ce moment, Chouchou prend un pot.
narrateur|Le verre est lisse et un peu froid.
narrateur|Un reste d'étiquette colle encore.
enfant-m|Je veux des lanternes.
enfant-m|Avec du papier jaune.
papa|On les lève vers le ciel ?
enfant-m|Oui.
narrateur|Mila arrive sur la première marche.
narrateur|Ses chaussons font un bruit mou.
narrateur|Mila n'a pas la même forme.
narrateur|Les corps sont différents.
narrateur|Un petit rire commence.
papa|Le corps n'est pas une blague.
papa|On joue.
narrateur|Chouchou ferme la bouche.
enfant-m|Mila, tu veux une lanterne ?
copine|Oui.
narrateur|Papa tend deux papiers jaunes.
narrateur|Ils froissent un peu.
narrateur|Le jaune est fin comme une peau d'oignon.
enfant-m|Il fait un bruit de papier.
copine|Le mien aussi.
""",
        "CHK_T0000_P0000_Q0001": """
narrateur|Le corps n'est pas une blague.
narrateur|Que fait-on ?
""",
        "CHK_T0000_P0000_C0001": """
narrateur|Chouchou glisse le papier dans son pot.
narrateur|Mila glisse le sien.
narrateur|Un couvercle reste coincé.
copine|Il ne veut pas.
enfant-m|On tourne ensemble.
narrateur|Ils tiennent le verre.
narrateur|Le couvercle vient, tout à coup.
papa|Bravo, Chouchou.
papa|Vous avez ouvert.
papa|Vous jouez.
narrateur|Le papier jaune s'installe.
narrateur|Il se colle un peu au verre.
narrateur|Ils lèvent les pots.
narrateur|Le dernier soleil traverse le jaune.
enfant-m|Ça brille.
copine|La mienne aussi.
papa|L'amitié ne dépend pas de la forme.
papa|On joue.
narrateur|Ils s'assoient sur la pierre chaude.
narrateur|Le grillon recommence.
narrateur|Une fourmi croise le perron.
papa|On la laisse passer.
narrateur|Ils restent un moment, tout calmes.
""",
        "CHK_T0000_P0000_END": """
papa|On les pose un moment ?
enfant-m|Oui.
narrateur|Les deux pots reposent côte à côte.
narrateur|La fenêtre jaune leur fait face.
copine|C'est comme deux lunes.
enfant-m|Deux petites.
papa|Tu as fini de les lever ?
enfant-m|Oui, papa.
narrateur|Chouchou essuie le verre.
narrateur|Mila essuie l'autre.
narrateur|Les pots cliquettent un peu.
enfant-m|Merci, Mila.
copine|Merci, Chouchou.
narrateur|La pierre refroidit un peu.
narrateur|Le ciel est presque bleu nuit.
""",
        "CHK_T0000_P0000_END_F0001": """
enfant-m|On a fait des lanternes.
copine|Elles ont brillé.
papa|Vous avez joué.
narrateur|Le grillon reste dans l'herbe.
narrateur|L'histoire est finie.
""",
    },
    {
        "expected_answer": "jouer",
        "accepted_examples": "jouer | on joue | pas une blague | pas blague | les lanternes",
        "retry_prompt": "On joue. Le corps n'est pas une blague. Que fait-on ?",
    },
    S(),
    R(),
    {},
)
