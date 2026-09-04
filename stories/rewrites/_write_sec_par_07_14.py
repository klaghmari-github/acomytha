#!/usr/bin/env python3
"""F-NAR-009 — merged.json pour ATOM-SEC.PAR.001-07 à 14."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIMITS = {"N1": 10, "N2": 15, "N3": 18}
ROLES = {"narrateur", "papa", "maman", "enfant-m", "enfant-f"}
NEED = ("espace montré", "adulte voit")
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
)
BAD_NAMES = (
    "valentine", "élisa", "elisa", "clovis", "dorian", "denis", "cécile",
    "cecile", "didier", "émilie", "emilie", "jules", "zoé", "zoe", "noé",
    "noe", "inès", "ines", "kamil", "tania", "tom ", "léa", "lea ", "lina",
    "iris", "lucas", "céline", "celine", "luca",
)


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


def make_chunk(src: dict, lines: list[str]) -> dict:
    text, script = from_script(lines)
    nc = dict(src)
    nc["text"] = text
    nc["script"] = script
    if nc.get("sons") is None:
        nc["sons"] = ""
    return nc


def check(sid: str, age: str, chunks: list[dict]) -> None:
    lim = LIMITS[age]
    joined = "\n".join(c["script"] for c in chunks)
    low = joined.lower()
    for bad in FORBIDDEN:
        if bad in low:
            raise SystemExit(f"{sid} interdit: {bad}")
    for name in BAD_NAMES:
        if name in low:
            raise SystemExit(f"{sid} prénom hors troupe: {name}")
    adults = [
        ln for ln in joined.splitlines()
        if ln.startswith("papa|") or ln.startswith("maman|")
    ]
    if not adults:
        raise SystemExit(f"{sid}: aucun papa/maman")
    aj = " ".join(a.split("|", 1)[1] for a in adults).lower()
    if "bravo" not in aj and "bon travail" not in aj:
        raise SystemExit(f"{sid}: pas de félicitation")
    if not any("?" in a for a in adults):
        raise SystemExit(f"{sid}: aucune question d'adulte")
    all_text = " ".join(c["text"] for c in chunks).lower()
    for m in NEED:
        if m not in all_text:
            raise SystemExit(f"{sid}: message manquant: {m}")
    if "là où l'adulte a dit" not in all_text and "la ou l'adulte a dit" not in all_text:
        if "là où l'adulte a dit" not in all_text:
            raise SystemExit(f"{sid}: manque safe_action là où l'adulte a dit")
    if "en ce moment" not in all_text:
        raise SystemExit(f"{sid}: manque en ce moment")
    if "l'histoire est finie" not in all_text:
        raise SystemExit(f"{sid}: manque clôture")
    first = chunks[0]["script"].splitlines()[0].split("|", 1)[1].lower()
    for bad in ("joue au salon", "est dans l'entrée", "c'est le matin"):
        if bad in first:
            raise SystemExit(f"{sid} amorce sèche: {first}")
    nwords = sum(words(c["text"]) for c in chunks)
    if nwords < 380:
        raise SystemExit(f"{sid}: trop court ({nwords} mots)")
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
                raise SystemExit(f"{sid} {c['chunk_id']} {n}>{lim}: {phrase}")
            if n == 0:
                raise SystemExit(f"{sid} phrase vide")
            if not phrase.endswith((".", "?", "!")):
                raise SystemExit(f"{sid} sans ponctuation: {phrase}")
            if phrase.count(".") + phrase.count("?") + phrase.count("!") > 1:
                raise SystemExit(f"{sid} plusieurs phrases: {phrase}")
    print(f"OK {sid} {nwords} mots")


def write_story(sid: str, fil: str, title: str, chars: str, setting: str,
                scripts: dict) -> None:
    folder = ROOT / sid
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"{sid} chunks missing={missing} extra={extra}")
    by = {}
    for c in src["chunks"]:
        by[c["chunk_id"]] = make_chunk(c, scripts[c["chunk_id"]])
    out = dict(src)
    out["fil_rouge"] = fil
    out["title"] = title
    out["characters"] = chars
    out["setting"] = setting
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(sid, out["age_band"], out["chunks"])
    path = folder / "merged.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# 07 N2 Sarah — feuille jaune / square / gâteau de sable
# ---------------------------------------------------------------------------
S07 = {
    "CHK_T0000_P0000": """
narrateur|Une feuille jaune colle au banc mouillé.
narrateur|Le square sent le sable encore humide.
narrateur|Un seau rouge est couché dans l'herbe.
narrateur|La gouttière fait plic, tout près.
narrateur|Le bois du banc est froid et lisse.
narrateur|Un moineau picore une miette grise.
narrateur|Sarah marche près de maman.
maman|Tu as vu le moineau, Sarah ?
enfant-f|Oui, maman.
enfant-f|Il picore.
narrateur|En ce moment, Sarah s'approche du bac.
narrateur|Le sable est frais sous les doigts.
maman|Tu joues ici.
maman|C'est l'espace montré.
maman|Ici, l'adulte voit.
enfant-f|Ici, maman ?
maman|Oui.
maman|Tu restes dans l'espace montré.
narrateur|Sarah va au bac à sable.
narrateur|Elle reste dans l'espace montré.
narrateur|Maman s'assoit sur le banc mouillé.
narrateur|Maman voit Sarah.
narrateur|L'adulte voit.
narrateur|Sarah verse le sable frais.
narrateur|Le seau rouge est un peu rêche.
enfant-f|Je fais un gâteau.
maman|Un gâteau de sable ?
enfant-f|Oui.
enfant-f|Il est tout mou.
narrateur|Sarah appuie avec la paume.
narrateur|Le gâteau sent le sable humide.
narrateur|Un oiseau chante au-dessus du square.
maman|Je te vois.
maman|L'adulte voit.
enfant-f|Tu me vois, maman ?
maman|Oui.
maman|Tu es dans l'espace montré.
narrateur|Les mains de Sarah restent dans le sable.
narrateur|Elle ajoute une petite feuille jaune.
narrateur|La feuille fait un chapeau tout plat.
enfant-f|Un chapeau, maman.
maman|Il est joli.
maman|Tu joues là où l'adulte a dit.
narrateur|Plus tard, Sarah prend le seau.
narrateur|Elle reste encore dans l'espace montré.
maman|Tu restes là où l'adulte a dit ?
enfant-f|Oui.
enfant-f|Ici.
maman|Bravo, Sarah.
maman|Tu as fait du bon travail.
narrateur|Maman la voit toujours.
narrateur|La feuille du banc tremble un peu.
narrateur|Le moineau s'envole vers le toit.
enfant-f|Il s'envole.
maman|Oui.
maman|Et toi, tu restes ici.
narrateur|Sarah lisse encore le gâteau.
narrateur|Le sable colle un peu aux genoux.
maman|Tu as fini ton gâteau ?
enfant-f|Presque.
narrateur|Elle pose le seau à côté.
narrateur|Elle reste dans l'espace montré.
narrateur|L'adulte voit.
    """.strip().splitlines(),
    "CHK_T0000_P0000_Q0001": """
narrateur|Sarah joue au square.
narrateur|Où joue-t-elle ?
    """.strip().splitlines(),
    "CHK_T0000_P0000_C0001": """
narrateur|Sarah est dans l'espace montré.
narrateur|Maman la voit.
narrateur|L'adulte voit.
narrateur|Le gâteau de sable est là.
maman|Tu as joué dans l'espace montré ?
enfant-f|Oui.
maman|Bravo.
maman|L'adulte voit.
narrateur|Le seau rouge brille un peu.
narrateur|La petite feuille reste sur le gâteau.
    """.strip().splitlines(),
    "CHK_T0000_P0000_END": """
narrateur|Sarah range le seau.
narrateur|Le sable tombe, tout doux.
maman|Tu as fini de ranger ?
enfant-f|Oui, maman.
maman|Bravo.
maman|Donne-moi la main.
narrateur|Maman lui tend la main.
narrateur|La feuille jaune reste sur le banc.
narrateur|Le square sent encore le sable mouillé.
    """.strip().splitlines(),
    "CHK_T0000_P0000_END_F0001": """
narrateur|Sarah tient la main de maman.
enfant-f|On a fait un gâteau.
maman|Oui.
maman|Dans l'espace montré.
maman|Bravo, Sarah.
narrateur|L'histoire est finie.
    """.strip().splitlines(),
}


# ---------------------------------------------------------------------------
# 08 N3 Nina — canards / bac / petit pont de bois
# ---------------------------------------------------------------------------
S08 = {
    "CHK_T0000_P0000": """
narrateur|Les canards font des ronds dans l'eau.
narrateur|Une miette flotte près du bord.
narrateur|Le bois de la rambarde est tiède.
narrateur|Le parc sent l'herbe coupée.
narrateur|Un caillou gris brille dans la vase.
narrateur|Papa tient le manteau de Nina.
papa|Tu as entendu les canards, Nina ?
enfant-f|Oui, papa.
enfant-f|Ils font coin-coin.
narrateur|En ce moment, Nina arrive au bac à sable.
narrateur|Le sable est frais et un peu froid.
papa|Voici l'espace montré.
papa|Tu joues ici.
papa|L'adulte voit.
enfant-f|Ici, papa ?
papa|Oui.
papa|On reste dans l'espace montré.
narrateur|Papa s'assoit sur le banc.
narrateur|Nina creuse avec la pelle.
narrateur|Elle reste dans l'espace montré.
narrateur|Papa la voit.
narrateur|L'adulte voit.
narrateur|Un seau rouge attend près du bac.
narrateur|Une pelle bleue est un peu rêche.
narrateur|Nina verse le sable, tout doux.
enfant-f|Ça fait un tas.
papa|Un beau tas.
papa|Je te vois.
narrateur|Un canard s'approche du bord.
narrateur|L'eau clapote contre la pierre.
papa|Tu restes là où l'adulte a dit ?
enfant-f|Oui.
enfant-f|Dans l'espace montré.
papa|Bravo.
narrateur|Plus tard, ils vont à l'aire de jeux.
narrateur|Le bois du petit pont est lisse.
narrateur|Il sent le soleil et la résine.
papa|Ici, c'est l'espace montré.
papa|Je reste là, sur le banc.
papa|L'adulte voit.
enfant-f|Je reste là.
narrateur|Nina marche sur le pont.
narrateur|Ses mains tiennent la rambarde tiède.
narrateur|Elle reste où papa a dit.
narrateur|Elle reste dans l'espace montré.
narrateur|Papa la voit encore.
narrateur|L'adulte voit.
enfant-f|Papa me voit.
papa|Oui.
papa|Tu joues là où l'adulte a dit.
papa|Bravo, Nina.
papa|Tu as fait du bon travail.
narrateur|Les canards font encore coin-coin.
narrateur|Nina redescend du pont, tout doucement.
narrateur|Elle revient près du banc.
papa|Tu as fini le pont ?
enfant-f|Oui, papa.
papa|Bravo.
narrateur|Ils se tiennent la main.
narrateur|Le bois du pont reste tiède.
narrateur|Nina pose la paume sur la rambarde.
enfant-f|C'est chaud.
papa|Oui.
papa|Le soleil a chauffé le bois.
narrateur|Un canard plonge, tout près.
narrateur|L'eau fait un petit cercle.
papa|Tu es restée dans l'espace montré ?
enfant-f|Oui, papa.
papa|Bravo.
narrateur|L'adulte voit.
    """.strip().splitlines(),
    "CHK_T0000_P0000_Q0001": """
narrateur|Papa montre un espace.
narrateur|Où joue Nina ?
    """.strip().splitlines(),
    "CHK_T0000_P0000_C0001": """
narrateur|Nina est restée dans l'espace montré.
narrateur|Au parc, puis à l'aire.
narrateur|L'adulte voit.
papa|Tu as joué dans l'espace montré ?
enfant-f|Oui.
enfant-f|Au bac, puis au pont.
papa|Bravo.
papa|L'adulte voit.
narrateur|Un canard secoue ses plumes.
    """.strip().splitlines(),
    "CHK_T0000_P0000_END": """
narrateur|Nina range le seau.
narrateur|Le sable tombe dans le bac.
papa|Tu as fini de ranger ?
enfant-f|Oui, papa.
papa|Bravo.
narrateur|Papa ferme le petit portail.
narrateur|Le bois claque, tout doux.
narrateur|Ils rentrent la main dans la main.
    """.strip().splitlines(),
    "CHK_T0000_P0000_END_F0001": """
narrateur|Les canards restent sur l'eau.
enfant-f|On a joué au pont.
papa|Oui.
papa|Dans l'espace montré.
papa|Bravo, Nina.
narrateur|L'histoire est finie.
    """.strip().splitlines(),
}


# ---------------------------------------------------------------------------
# 09 N1 Nino — grain de sable / bac / seau rouge
# ---------------------------------------------------------------------------
S09 = {
    "CHK_T0000_P0000": """
narrateur|Un grain de sable brille au soleil.
narrateur|Le parc sent l'herbe chaude.
narrateur|Un seau rouge attend dans le bac.
narrateur|Une abeille visite une fleur jaune.
narrateur|Le banc est chaud sous la main.
narrateur|Maman tient la main de Nino.
maman|Tu as vu le grain, Nino ?
enfant-m|Oui, maman.
enfant-m|Il brille.
narrateur|En ce moment, le bac à sable est là.
narrateur|Maman montre l'espace.
maman|C'est l'espace montré.
maman|Tu joues ici.
maman|L'adulte voit.
enfant-m|Ici ?
maman|Oui.
maman|Dans l'espace montré.
narrateur|Nino s'assoit dans le bac.
narrateur|Il sent le sable.
narrateur|Le sable est frais.
narrateur|Maman s'assoit sur le banc.
narrateur|L'adulte voit Nino.
narrateur|Maman voit.
narrateur|Nino verse le sable.
narrateur|Le seau est rouge.
narrateur|Il reste dans l'espace montré.
maman|Je te vois.
maman|L'adulte voit.
enfant-m|Tu me vois ?
maman|Oui.
maman|Tu es ici.
narrateur|Nino creuse.
narrateur|Il reste là.
narrateur|Près de maman.
narrateur|Le sable colle aux doigts.
enfant-m|C'est mou.
maman|Oui.
maman|Le sable est frais.
maman|Tu restes dans l'espace montré ?
enfant-m|Oui.
enfant-m|Ici.
maman|Bravo, Nino.
maman|Tu as fait du bon travail.
narrateur|Nino remplit encore le seau.
narrateur|Le seau rouge est lourd.
narrateur|Il verse tout doucement.
narrateur|Le tas est petit et rond.
maman|Tu joues là où l'adulte a dit.
enfant-m|Là où l'adulte a dit.
maman|Oui.
narrateur|Une abeille part vers la haie.
narrateur|Nino reste dans l'espace montré.
narrateur|L'adulte voit.
maman|Tu as fini le tas ?
enfant-m|Encore un peu.
narrateur|Nino lisse le tas.
narrateur|Il reste près du banc.
narrateur|Maman le voit.
narrateur|L'adulte voit.
narrateur|Le grain de sable brille encore.
narrateur|Nino pose la main dessus.
enfant-m|Il est chaud.
maman|Oui.
maman|Le soleil le chauffe.
narrateur|Nino recouvre le grain.
narrateur|Le tas devient un peu plus gros.
maman|Tu restes ici ?
enfant-m|Oui.
enfant-m|Dans l'espace montré.
maman|Bravo.
narrateur|Le seau rouge penche un peu.
narrateur|Nino le redresse.
narrateur|Il reste dans l'espace montré.
narrateur|L'adulte voit.
    """.strip().splitlines(),
    "CHK_T0000_P0000_Q0001": """
narrateur|Nino joue au parc.
narrateur|Où reste-t-il ?
    """.strip().splitlines(),
    "CHK_T0000_P0000_C0001": """
narrateur|Nino est dans l'espace montré.
narrateur|Maman, l'adulte, voit.
narrateur|Le sable reste dans le bac.
maman|Tu es resté dans l'espace montré ?
enfant-m|Oui.
maman|Bravo.
maman|L'adulte voit.
narrateur|Le seau rouge est encore là.
    """.strip().splitlines(),
    "CHK_T0000_P0000_END": """
narrateur|Nino range le seau.
narrateur|Le sable tombe, tout fin.
maman|Tu as fini de ranger ?
enfant-m|Oui, maman.
maman|Bravo.
narrateur|Maman lui tend la main.
narrateur|Papa arrive sur le chemin.
papa|Tu as joué ici ?
enfant-m|Oui, papa.
papa|Dans l'espace montré.
maman|L'adulte voit.
    """.strip().splitlines(),
    "CHK_T0000_P0000_END_F0001": """
narrateur|Nino tient la main de maman.
enfant-m|On a fait un tas.
maman|Oui.
maman|Dans l'espace montré.
maman|Bravo, Nino.
narrateur|L'histoire est finie.
    """.strip().splitlines(),
}


# ---------------------------------------------------------------------------
# 10 N3 Aniss — chaîne de balançoire / bac / toboggan
# ---------------------------------------------------------------------------
S10 = {
    "CHK_T0000_P0000": """
narrateur|La chaîne de la balançoire fait tic.
narrateur|Le parc sent le pin chaud.
narrateur|Une pomme de pin roule sur le chemin.
narrateur|Les aiguilles sont sèches sous les pieds.
narrateur|Un banc gris attend à l'ombre.
narrateur|Maman pose le sac sur le banc.
maman|Tu as entendu la chaîne, Aniss ?
enfant-m|Oui, maman.
enfant-m|Ça fait tic.
narrateur|En ce moment, maman montre le bac à sable.
maman|C'est l'espace montré.
maman|Tu joues ici.
maman|L'adulte voit.
enfant-m|Ici, maman ?
maman|Oui.
maman|On reste dans l'espace montré.
narrateur|Aniss s'assoit.
narrateur|Il sent le sable frais.
narrateur|Maman s'assoit sur le banc gris.
narrateur|L'adulte voit Aniss.
narrateur|Aniss verse le seau.
narrateur|Il reste dans l'espace montré.
maman|Je te vois.
maman|L'adulte voit.
enfant-m|Tu me vois ?
maman|Oui.
narrateur|Le sable coule entre les doigts.
narrateur|Il est un peu froid, tout fin.
enfant-m|Ça coule.
maman|Oui.
maman|Tu joues là où l'adulte a dit.
narrateur|Plus tard, maman montre le toboggan.
maman|Autre espace montré.
maman|Ici, l'adulte voit encore.
enfant-m|Je peux glisser ?
maman|Oui.
maman|Tu restes dans l'espace montré.
narrateur|Aniss grimpe l'échelle.
narrateur|Les barreaux sont lisses et tièdes.
narrateur|Il glisse.
narrateur|Le plastique fait un petit chuintement.
narrateur|Il revient au pied.
narrateur|Maman le voit encore.
narrateur|L'adulte voit.
enfant-m|Encore une fois ?
maman|Oui.
maman|Dans l'espace montré.
narrateur|Aniss glisse encore.
narrateur|Il reste là où maman a dit.
maman|Tu restes là où l'adulte a dit ?
enfant-m|Oui.
maman|Bravo, Aniss.
maman|Tu as fait du bon travail.
narrateur|La chaîne fait encore tic, au loin.
narrateur|Aniss range le seau près du bac.
narrateur|Il reste dans l'espace montré.
maman|Tu as fini de glisser ?
enfant-m|Oui, maman.
maman|Bravo.
narrateur|Une aiguille de pin colle à son genou.
narrateur|Aniss la retire, tout doux.
enfant-m|Ça pique un peu.
maman|Oui.
maman|Tu restes ici.
narrateur|L'adulte voit.
narrateur|Le toboggan brille encore.
narrateur|Aniss touche le plastique tiède.
enfant-m|Il est lisse.
maman|Oui.
maman|Tu as glissé dans l'espace montré.
enfant-m|Dans l'espace montré.
maman|Bravo.
    """.strip().splitlines(),
    "CHK_T0000_P0000_Q0001": """
narrateur|Aniss joue au parc.
narrateur|Où reste-t-il ?
    """.strip().splitlines(),
    "CHK_T0000_P0000_C0001": """
narrateur|Aniss est resté dans l'espace montré.
narrateur|Au bac, puis au toboggan.
narrateur|L'adulte voit.
maman|Tu es resté dans l'espace montré ?
enfant-m|Oui.
enfant-m|Au bac, puis au toboggan.
maman|Bravo.
maman|L'adulte voit.
narrateur|La pomme de pin est encore sur le chemin.
    """.strip().splitlines(),
    "CHK_T0000_P0000_END": """
narrateur|Aniss prend la main de maman.
maman|Tu as fini de ranger ?
enfant-m|Oui, maman.
maman|Bravo.
narrateur|Papa arrive près des pins.
papa|Vous avez joué ici ?
enfant-m|Oui, papa.
maman|Dans l'espace montré.
papa|L'adulte voit.
narrateur|Ils quittent le parc.
narrateur|Les aiguilles craquent sous les pas.
    """.strip().splitlines(),
    "CHK_T0000_P0000_END_F0001": """
narrateur|La chaîne de la balançoire se tait.
enfant-m|On a glissé.
maman|Oui.
maman|Dans l'espace montré.
maman|Bravo, Aniss.
narrateur|L'histoire est finie.
    """.strip().splitlines(),
}


# ---------------------------------------------------------------------------
# 11 N3 Raphaël — caillou / marelle / jeu à ressort
# ---------------------------------------------------------------------------
S11 = {
    "CHK_T0000_P0000": """
narrateur|Un caillou blanc dort dans une case.
narrateur|La marelle est dessinée à la craie.
narrateur|Le square sent le bitume tiède.
narrateur|Un manteau bleu est plié sur le banc.
narrateur|Une craie courte laisse un trait blanc.
narrateur|Papa pose le manteau.
papa|Tu as vu le caillou, Raphaël ?
enfant-m|Oui, papa.
enfant-m|Il est blanc.
narrateur|En ce moment, papa montre la marelle.
papa|C'est l'espace montré.
papa|Tu joues ici.
papa|L'adulte voit.
enfant-m|Dans les cases ?
papa|Oui.
papa|On reste dans l'espace montré.
narrateur|Raphaël saute dans les cases.
narrateur|Il sent le sol lisse.
narrateur|Papa s'assoit sur le banc.
narrateur|L'adulte voit Raphaël.
narrateur|Raphaël reste dans l'espace montré.
papa|Je te vois.
papa|L'adulte voit.
enfant-m|Tu me vois ?
papa|Oui.
narrateur|Le caillou saute d'une case à l'autre.
narrateur|Les pieds tapent, tout légers.
papa|Tu joues là où l'adulte a dit.
enfant-m|Dans l'espace montré.
papa|Oui.
narrateur|Plus tard, papa montre le jeu à ressort.
papa|Autre espace montré.
papa|Ici, l'adulte voit encore.
enfant-m|Je peux m'asseoir ?
papa|Oui.
papa|Tu restes dans l'espace montré.
narrateur|Raphaël s'assoit dessus.
narrateur|Le siège est un peu rêche.
narrateur|Ça penche, tout doux.
narrateur|Il revient au pied.
narrateur|Papa le voit encore.
narrateur|L'adulte voit.
papa|Tu restes là où l'adulte a dit ?
enfant-m|Oui.
papa|Bravo, Raphaël.
papa|Tu as fait du bon travail.
narrateur|Raphaël range son manteau sur le banc.
narrateur|Le tissu bleu est un peu chaud.
narrateur|Il reste là où papa a dit.
narrateur|Il reste dans l'espace montré.
papa|Tu as fini de sauter ?
enfant-m|Oui, papa.
papa|Bravo.
narrateur|Le caillou blanc reste dans une case.
narrateur|Raphaël le pose au milieu.
enfant-m|Il dort.
papa|Oui.
papa|Dans l'espace montré.
narrateur|Une craie blanche marque encore le sol.
narrateur|Raphaël reste près du banc.
narrateur|L'adulte voit.
narrateur|Le jeu à ressort s'arrête, tout doux.
narrateur|Raphaël pose la main sur le siège.
enfant-m|C'est rêche.
papa|Oui.
papa|Tu as sauté dans l'espace montré.
enfant-m|Dans l'espace montré.
papa|Bravo.
    """.strip().splitlines(),
    "CHK_T0000_P0000_Q0001": """
narrateur|Raphaël joue au square.
narrateur|Où reste-t-il ?
    """.strip().splitlines(),
    "CHK_T0000_P0000_C0001": """
narrateur|Raphaël est resté dans l'espace montré.
narrateur|À la marelle, puis au jeu à ressort.
narrateur|L'adulte voit.
papa|Tu es resté dans l'espace montré ?
enfant-m|Oui.
enfant-m|À la marelle, puis au ressort.
papa|Bravo.
papa|L'adulte voit.
narrateur|La craie laisse encore un trait blanc.
    """.strip().splitlines(),
    "CHK_T0000_P0000_END": """
narrateur|Raphaël prend la main de papa.
papa|Tu as fini de ranger le manteau ?
enfant-m|Oui, papa.
papa|Bravo.
narrateur|Maman arrive près du square.
maman|Vous avez joué ici ?
enfant-m|Oui, maman.
papa|Dans l'espace montré.
maman|L'adulte voit.
narrateur|Ils quittent le square.
narrateur|Le bitume reste tiède.
    """.strip().splitlines(),
    "CHK_T0000_P0000_END_F0001": """
narrateur|Le caillou blanc dort encore.
enfant-m|On a sauté.
papa|Oui.
papa|Dans l'espace montré.
papa|Bravo, Raphaël.
narrateur|L'histoire est finie.
    """.strip().splitlines(),
}


# ---------------------------------------------------------------------------
# 12 N1 Mila — cerceau rouge / jardin / herbe
# ---------------------------------------------------------------------------
S12 = {
    "CHK_T0000_P0000": """
narrateur|Un cerceau rouge chauffe dans l'herbe.
narrateur|Le jardin sent les fleurs.
narrateur|Le plastique est chaud au soleil.
narrateur|Une fourmi croise une tige.
narrateur|Le banc de bois est clair.
narrateur|Maman vient avec Mila.
maman|Tu as vu le cerceau, Mila ?
enfant-f|Oui, maman.
enfant-f|Il est rouge.
narrateur|En ce moment, maman montre les cerceaux.
maman|C'est l'espace montré.
maman|Tu joues ici.
maman|L'adulte voit.
enfant-f|Ici ?
maman|Oui.
maman|Dans l'espace montré.
narrateur|Mila saute dans un cerceau.
narrateur|Le cerceau est rouge.
narrateur|Il sent le plastique chaud.
narrateur|Maman s'assoit sur le banc.
narrateur|L'adulte voit Mila.
narrateur|Mila reste dans l'espace montré.
maman|Je te vois.
maman|L'adulte voit.
enfant-f|Tu me vois ?
maman|Oui.
narrateur|Mila saute encore.
narrateur|Ses pieds tapent l'herbe.
narrateur|L'herbe est un peu piquante.
narrateur|Elle reste là où maman a dit.
enfant-f|Encore un saut.
maman|Oui.
maman|Dans l'espace montré.
maman|Tu restes dans l'espace montré ?
enfant-f|Oui.
enfant-f|Ici.
maman|Bravo, Mila.
maman|Tu as fait du bon travail.
narrateur|Mila range un cerceau.
narrateur|Le plastique claque, tout léger.
narrateur|Elle reste près.
narrateur|L'espace montré, c'est ici.
narrateur|L'adulte voit.
maman|Tu joues là où l'adulte a dit.
enfant-f|Là où l'adulte a dit.
maman|Oui.
narrateur|Une fourmi reprend sa route.
narrateur|Mila saute dans le cerceau bleu.
narrateur|Elle reste dans l'espace montré.
maman|Tu as fini de sauter ?
enfant-f|Encore un peu.
narrateur|Mila saute une dernière fois.
narrateur|Ses pieds sentent l'herbe chaude.
narrateur|Maman la voit.
narrateur|L'adulte voit.
narrateur|Le cerceau bleu est un peu plus frais.
narrateur|Mila le pose près du rouge.
enfant-f|Rouge et bleu.
maman|Oui.
maman|Dans l'espace montré.
narrateur|Une fleur penche vers l'herbe.
narrateur|Mila la sent, tout près.
enfant-f|Ça sent bon.
maman|Oui.
maman|Tu restes ici ?
enfant-f|Oui.
maman|Bravo.
narrateur|Mila reste dans l'espace montré.
narrateur|L'adulte voit.
narrateur|Le soleil chauffe encore le cerceau rouge.
narrateur|Mila le touche du doigt.
enfant-f|Il est chaud.
maman|Oui.
    """.strip().splitlines(),
    "CHK_T0000_P0000_Q0001": """
narrateur|Mila joue au jardin.
narrateur|Où reste-t-elle ?
    """.strip().splitlines(),
    "CHK_T0000_P0000_C0001": """
narrateur|Mila est restée dans l'espace montré.
narrateur|Aux cerceaux.
narrateur|L'adulte voit.
maman|Tu es restée dans l'espace montré ?
enfant-f|Oui.
maman|Bravo.
maman|L'adulte voit.
narrateur|Le cerceau rouge reste dans l'herbe.
    """.strip().splitlines(),
    "CHK_T0000_P0000_END": """
narrateur|Mila prend la main de maman.
maman|Tu as fini de ranger ?
enfant-f|Oui, maman.
maman|Bravo.
narrateur|Elles quittent le jardin.
narrateur|L'herbe est encore chaude.
narrateur|Le cerceau rouge reste au soleil.
    """.strip().splitlines(),
    "CHK_T0000_P0000_END_F0001": """
narrateur|Mila tient la main de maman.
enfant-f|On a sauté.
maman|Oui.
maman|Dans l'espace montré.
maman|Bravo, Mila.
narrateur|L'histoire est finie.
    """.strip().splitlines(),
}


# ---------------------------------------------------------------------------
# 13 N3 Victorino — plot jaune / bac / plots sur caoutchouc
# ---------------------------------------------------------------------------
S13 = {
    "CHK_T0000_P0000": """
narrateur|Un plot jaune sent le caoutchouc chaud.
narrateur|Le parc sent l'herbe et le soleil.
narrateur|Le sol souple rebondit un peu.
narrateur|Une coccinelle grimpe sur un plot.
narrateur|Le seau bleu attend près du bac.
narrateur|Papa pose le sac contre le banc.
papa|Tu as vu la coccinelle, Victorino ?
enfant-m|Oui, papa.
enfant-m|Elle est rouge.
narrateur|En ce moment, papa montre le bac à sable.
papa|C'est l'espace montré.
papa|Tu joues ici.
papa|L'adulte voit.
enfant-m|Ici, papa ?
papa|Oui.
papa|On reste dans l'espace montré.
narrateur|Victorino s'assoit dans le sable.
narrateur|Le sable est frais.
narrateur|Il remplit un seau.
narrateur|Papa s'assoit sur le banc.
narrateur|L'adulte voit Victorino.
narrateur|Victorino reste dans l'espace montré.
papa|Je te vois.
papa|L'adulte voit.
enfant-m|Tu me vois ?
papa|Oui.
narrateur|Le seau bleu devient lourd.
narrateur|Victorino le verse, tout doucement.
enfant-m|Un château.
papa|Un petit château.
papa|Tu joues là où l'adulte a dit.
narrateur|Plus tard, papa montre les plots jaunes.
papa|C'est encore l'espace montré.
papa|Ici, l'adulte voit.
enfant-m|Je peux sauter ?
papa|Oui.
papa|Tu restes dans l'espace montré.
narrateur|Victorino saute de plot en plot.
narrateur|Ses pieds tapent le caoutchouc.
narrateur|Le sol fait poum, tout mou.
narrateur|Il reste là où papa a dit.
narrateur|Papa le voit.
narrateur|L'adulte voit.
papa|Tu restes là où l'adulte a dit ?
enfant-m|Oui.
enfant-m|Sur les plots.
papa|Bravo, Victorino.
papa|Tu as fait du bon travail.
narrateur|Victorino range le seau.
narrateur|Il reste près.
narrateur|L'espace montré, c'est ici.
narrateur|L'adulte voit.
papa|Tu as fini de sauter ?
enfant-m|Oui, papa.
papa|Bravo.
narrateur|La coccinelle a quitté le plot.
narrateur|Le caoutchouc reste chaud.
narrateur|Victorino pose la main dessus.
enfant-m|C'est mou.
papa|Oui.
papa|Le sol est souple.
narrateur|Il reste dans l'espace montré.
narrateur|L'adulte voit.
narrateur|Le château de sable tient encore.
narrateur|Victorino lisse un mur, tout fin.
enfant-m|Il est petit.
papa|Oui.
papa|Tu as joué dans l'espace montré.
enfant-m|Dans l'espace montré.
papa|Bravo.
narrateur|Un plot jaune penche un peu.
narrateur|Victorino le redresse.
narrateur|Ses pieds restent sur le caoutchouc.
    """.strip().splitlines(),
    "CHK_T0000_P0000_Q0001": """
narrateur|Victorino joue au parc.
narrateur|Où reste-t-il ?
    """.strip().splitlines(),
    "CHK_T0000_P0000_C0001": """
narrateur|Victorino est resté dans l'espace montré.
narrateur|Au bac, puis aux plots.
narrateur|L'adulte voit.
papa|Tu es resté dans l'espace montré ?
enfant-m|Oui.
enfant-m|Au bac, puis aux plots.
papa|Bravo.
papa|L'adulte voit.
narrateur|Le plot jaune brille encore.
    """.strip().splitlines(),
    "CHK_T0000_P0000_END": """
narrateur|Victorino prend la main de papa.
papa|Tu as fini de ranger le seau ?
enfant-m|Oui, papa.
papa|Bravo.
narrateur|Ils quittent le parc.
narrateur|Le caoutchouc redevient calme.
narrateur|Le seau bleu reste près du bac.
    """.strip().splitlines(),
    "CHK_T0000_P0000_END_F0001": """
narrateur|Un plot jaune garde le soleil.
enfant-m|On a sauté.
papa|Oui.
papa|Dans l'espace montré.
papa|Bravo, Victorino.
narrateur|L'histoire est finie.
    """.strip().splitlines(),
}


# ---------------------------------------------------------------------------
# 14 N3 Victorina — goutte / fontaine / toboggan bas
# ---------------------------------------------------------------------------
S14 = {
    "CHK_T0000_P0000": """
narrateur|Une goutte d'eau saute de la fontaine.
narrateur|Elle éclate sur la pierre grise.
narrateur|Le square sent l'eau fraîche.
narrateur|Une pierre lisse brille au soleil.
narrateur|Un banc vert attend à l'ombre.
narrateur|Papa pose le gilet sur le banc.
papa|Tu as vu la goutte, Victorina ?
enfant-f|Oui, papa.
enfant-f|Elle saute.
narrateur|En ce moment, papa montre la fontaine.
papa|C'est l'espace montré.
papa|Tu joues ici.
papa|L'adulte voit.
enfant-f|Près de l'eau ?
papa|Oui.
papa|On reste dans l'espace montré.
narrateur|Victorina s'approche.
narrateur|L'eau clapote.
narrateur|Elle touche une goutte.
narrateur|La goutte est froide et ronde.
narrateur|Papa s'assoit sur le banc vert.
narrateur|L'adulte voit Victorina.
narrateur|Victorina reste dans l'espace montré.
papa|Je te vois.
papa|L'adulte voit.
enfant-f|Tu me vois ?
papa|Oui.
narrateur|Une autre goutte tombe sur sa main.
enfant-f|Elle est froide.
papa|Oui.
papa|Tu joues là où l'adulte a dit.
narrateur|Plus tard, papa montre le toboggan bas.
papa|C'est encore l'espace montré.
papa|Ici, l'adulte voit.
enfant-f|Je peux glisser ?
papa|Oui.
papa|Tu restes dans l'espace montré.
narrateur|Victorina monte les marches.
narrateur|Ses mains tiennent la rampe.
narrateur|La rampe est lisse et tiède.
narrateur|Elle glisse.
narrateur|Le plastique est lisse.
narrateur|Elle reste là où papa a dit.
narrateur|Papa la voit.
narrateur|L'adulte voit.
papa|Tu restes là où l'adulte a dit ?
enfant-f|Oui.
enfant-f|Au toboggan.
papa|Bravo, Victorina.
papa|Tu as fait du bon travail.
narrateur|Victorina revient près du banc.
narrateur|L'espace montré, c'est ici.
narrateur|L'adulte voit.
papa|Tu as fini de glisser ?
enfant-f|Oui, papa.
papa|Bravo.
narrateur|La fontaine clapote encore.
narrateur|Une goutte sèche sur la pierre.
narrateur|Victorina essuie sa main au gilet.
enfant-f|C'est mouillé.
papa|Oui.
papa|L'eau est fraîche.
narrateur|Elle reste dans l'espace montré.
narrateur|L'adulte voit.
narrateur|Le toboggan bas brille un peu.
narrateur|Victorina touche la rampe encore.
enfant-f|C'est lisse.
papa|Oui.
papa|Tu as glissé dans l'espace montré.
enfant-f|Dans l'espace montré.
papa|Bravo.
narrateur|Une goutte sèche sur sa manche.
narrateur|Le square sent encore l'eau.
    """.strip().splitlines(),
    "CHK_T0000_P0000_Q0001": """
narrateur|Victorina joue au square.
narrateur|Où reste-t-elle ?
    """.strip().splitlines(),
    "CHK_T0000_P0000_C0001": """
narrateur|Victorina est restée dans l'espace montré.
narrateur|À la fontaine, puis au toboggan.
narrateur|L'adulte voit.
papa|Tu es restée dans l'espace montré ?
enfant-f|Oui.
enfant-f|À la fontaine, puis au toboggan.
papa|Bravo.
papa|L'adulte voit.
narrateur|La pierre grise brille encore.
    """.strip().splitlines(),
    "CHK_T0000_P0000_END": """
narrateur|Victorina prend la main de papa.
papa|Tu as fini près de l'eau ?
enfant-f|Oui, papa.
papa|Bravo.
narrateur|Ils quittent le square.
narrateur|La fontaine reste derrière eux.
narrateur|Le gilet bleu balance un peu.
    """.strip().splitlines(),
    "CHK_T0000_P0000_END_F0001": """
narrateur|Une dernière goutte saute.
enfant-f|On a glissé.
papa|Oui.
papa|Dans l'espace montré.
papa|Bravo, Victorina.
narrateur|L'histoire est finie.
    """.strip().splitlines(),
}


def main() -> None:
    write_story(
        "ATOM-SEC.PAR.001-07",
        "Au square, Sarah fait un gâteau de sable dans l'espace que maman a montré. Maman voit.",
        "Le gâteau de sable de Sarah",
        "Sarah, maman",
        "square, bac à sable",
        S07,
    )
    write_story(
        "ATOM-SEC.PAR.001-08",
        "Nina joue au bac à sable puis sur le petit pont, toujours dans l'espace que papa a montré.",
        "Le pont de bois de Nina",
        "Nina, papa",
        "parc puis aire de jeux",
        S08,
    )
    write_story(
        "ATOM-SEC.PAR.001-09",
        "Nino verse le sable du seau rouge dans l'espace que maman a montré. Maman voit.",
        "Le seau rouge de Nino",
        "Nino, maman, papa",
        "parc, bac à sable",
        S09,
    )
    write_story(
        "ATOM-SEC.PAR.001-10",
        "Aniss joue au bac puis au toboggan, toujours dans l'espace que maman a montré.",
        "Le toboggan d'Aniss",
        "Aniss, maman, papa",
        "parc, bac à sable puis toboggan",
        S10,
    )
    write_story(
        "ATOM-SEC.PAR.001-11",
        "Raphaël saute à la marelle puis au jeu à ressort, dans l'espace que papa a montré.",
        "La marelle de Raphaël",
        "Raphaël, papa, maman",
        "square, marelle puis jeu à ressort",
        S11,
    )
    write_story(
        "ATOM-SEC.PAR.001-12",
        "Mila saute dans les cerceaux du jardin, dans l'espace que maman a montré.",
        "Les cerceaux de Mila",
        "Mila, maman",
        "jardin public, cerceaux",
        S12,
    )
    write_story(
        "ATOM-SEC.PAR.001-13",
        "Victorino fait un château puis saute de plot en plot, dans l'espace que papa a montré.",
        "Les plots jaunes de Victorino",
        "Victorino, papa",
        "parc, bac à sable puis plots",
        S13,
    )
    write_story(
        "ATOM-SEC.PAR.001-14",
        "Victorina touche l'eau de la fontaine puis glisse, dans l'espace que papa a montré.",
        "La fontaine de Victorina",
        "Victorina, papa",
        "square, fontaine puis toboggan",
        S14,
    )


if __name__ == "__main__":
    main()
