#!/usr/bin/env python3
"""F-NAR-008 — merged.json ATOM-DIF.ENE.001-09 + ATOM-DIF.PAR.001-01..07."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIMITS = {"N1": 10, "N2": 15, "N3": 15}
ROLES = {"narrateur", "papa", "maman", "enfant-m", "enfant-f"}
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
    "c'est du bon travail",
)
BAD_NAMES = (
    "rania", "kilian", "béatrice", "beatrice", "bruno", "brice",
    "inès", "ines", "maya", "jules", "théo", "theo", "océane",
    "oceane", "malo", "tom ", "léa", "lea ", "lina", "iris",
    "aïcha", "aicha", "clément", "clement", "léonie", "leonie",
    "clarisse", "éléonore", "eleonore", "dominique", "zoé", "zoe",
    "adam", "ariane", "benoît", "benoit", "kenzo", "valentine",
    "faustine", "marceau", "aline", "denis", "gwenaëlle", "hervé",
    "amélie", "loïc", "ruben",
)
TROUPE = {
    "amir", "aniss", "sarah", "chouchou", "mila", "nino", "nina",
    "raphaël", "raphael", "victorino", "victorina",
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


def piper_for(age: str, kind: str, lines: list[str]) -> tuple[float, str]:
    role0 = lines[0].split("|", 1)[0]
    if kind == "passage_question":
        return (1.28 if age == "N1" else 1.22), "slow"
    if kind == "passage_fin" or role0.startswith("enfant"):
        return 1.28, ("slow" if age == "N1" else "medium")
    return (1.28 if age == "N1" else 1.22), ("slow" if age == "N1" else "medium")


def make_chunk(src: dict, lines: list[str], sons, age: str) -> dict:
    text, script = from_script(lines)
    nc = dict(src)
    nc["text"] = text
    nc["script"] = script
    nc["text_ssml"] = text
    nc["sons"] = sons if sons is not None else (src.get("sons") or "")
    if nc["sons"] is None:
        nc["sons"] = ""
    scale, rate = piper_for(age, src.get("kind") or "", lines)
    nc["length_scale_piper"] = scale
    nc["rate_label"] = rate
    return nc


def stems_ok(need: tuple[str, ...], text: str) -> None:
    low = text.lower()
    for m in need:
        tokens = [t.strip() for t in re.split(r"[|/]", m) if t.strip()]
        ok = False
        for t in tokens:
            ws = [
                w
                for w in re.findall(r"[a-zàâäéèêëïîôùûüçœ-]{3,}", t.lower())
                if w not in ("une", "des", "les", "est", "avec", "pour", "dans")
            ]
            if ws and all(w in low for w in ws[:2]):
                ok = True
                break
            if t.lower() in low:
                ok = True
                break
        if not ok:
            raise SystemExit(f"message manquant: {m}")


def check(sid: str, age: str, chunks: list[dict], need: tuple[str, ...]) -> None:
    lim = LIMITS[age]
    joined = "\n".join(c["script"] for c in chunks)
    low = joined.lower()
    for bad in FORBIDDEN:
        if bad in low:
            raise SystemExit(f"{sid} interdit: {bad}")
    for name in BAD_NAMES:
        if re.search(r"(^|[^a-zàâäéèêëïîôùûüçœ])" + re.escape(name) + r"([^a-zàâäéèêëïîôùûüçœ]|$)", low):
            raise SystemExit(f"{sid} prénom hors troupe: {name}")
    adults = [ln for ln in joined.splitlines() if ln.startswith("papa|") or ln.startswith("maman|")]
    if not adults:
        raise SystemExit(f"{sid}: aucun papa/maman")
    aj = " ".join(a.split("|", 1)[1] for a in adults).lower()
    if "bravo" not in aj and "merci" not in aj:
        raise SystemExit(f"{sid}: pas de félicitation")
    if aj.count("bravo") > 2:
        raise SystemExit(f"{sid}: bravo en refrain")
    if not any("?" in a for a in adults):
        raise SystemExit(f"{sid}: aucune question d'adulte")
    if "en ce moment" not in low:
        raise SystemExit(f"{sid}: manque en ce moment")
    if "l'histoire est finie." not in low:
        raise SystemExit(f"{sid}: manque fin")
    all_text = " ".join(c["text"] for c in chunks).lower()
    stems_ok(need, all_text)
    first = chunks[0]["script"].splitlines()[0].split("|", 1)[1].lower()
    for bad in ("joue au salon", "est dans l'entrée", "c'est le matin"):
        if bad in first:
            raise SystemExit(f"{sid} ouverture brutale: {first}")
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
    print(f"OK {sid} {nwords} mots  1re: {chunks[0]['script'].splitlines()[0].split('|',1)[1]}")


def write_story(
    sid: str,
    fil: str,
    title: str,
    chars: str,
    setting: str,
    scripts: dict,
    sons: dict,
    need: tuple[str, ...],
    q: dict | None = None,
    qid: str = "CHK_T0000_P0000_Q0001",
) -> None:
    folder = ROOT / sid
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"{sid} chunks missing={missing} extra={extra}")
    age = src.get("age_band") or "N2"
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        by[cid] = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), age)
    if q:
        for k, v in q.items():
            by[qid][k] = v
    out = dict(src)
    out["fil_rouge"] = fil
    out["title"] = title
    out["characters"] = chars
    out["setting"] = setting
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(sid, age, out["chunks"], need)
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


ENE = ("énergie", "pas une faute", "jouer", "attendre")
PAR = ("attendre", "tendre un jouet", "force", "parole")


# ---------------------------------------------------------------------------
# ENE.001-09 N1 — Victorina, Amir — escargot de raisins
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.ENE.001-09",
    "Victorina veut un escargot de raisins sur le gâteau. Amir a de l'énergie. Les raisins roulent. Ils posent un raisin chacun. Le gâteau part au four.",
    "L'escargot de raisins",
    "Victorina, Amir, papa, maman",
    "cuisine, bol de raisins, four",
    {
        "CHK_T0000_P0000": [
            "narrateur|La farine a fait un nuage blanc.",
            "narrateur|Le bol de raisins sent le soleil.",
            "narrateur|Un grain colle au bord du bol.",
            "narrateur|La cuillère en bois est encore farinée.",
            "papa|Tu as vu le nuage, Victorina ?",
            "enfant-f|Il est blanc, papa.",
            "maman|Ça sent déjà le gâteau.",
            "enfant-f|Je veux un escargot.",
            "enfant-f|Un escargot de raisins.",
            "maman|Sur le gâteau rond ?",
            "enfant-f|Oui.",
            "enfant-f|Tout en rond.",
            "narrateur|Papa tapote la pâte.",
            "narrateur|Toc, toc, sur le bois.",
            "narrateur|La pâte est molle et tiède.",
            "narrateur|Elle sent un peu le lait.",
            "narrateur|Maman beurre le moule.",
            "narrateur|Le beurre brille un peu.",
            "narrateur|Le moule est rond et froid.",
            "narrateur|En ce moment, Victorina prend un raisin.",
            "narrateur|Il est lisse et un peu collant.",
            "enfant-f|Le premier, au milieu.",
            "papa|Comme une tête d'escargot.",
            "narrateur|Elle pose le raisin.",
            "narrateur|Le gâteau est encore pâle.",
            "narrateur|Amir arrive dans la cuisine.",
            "narrateur|Il saute sur place.",
            "narrateur|Ses chaussettes tapent le carrelage.",
            "narrateur|Ça fait tap, tap, tap.",
            "narrateur|Le bol tremble.",
            "narrateur|Des raisins roulent sur la table.",
            "enfant-f|Ils partent, papa !",
            "papa|Amir a de l'énergie.",
            "maman|Beaucoup d'énergie.",
            "maman|Ce n'est pas une faute.",
            "narrateur|Victorina attrape un raisin.",
            "narrateur|Amir saute encore.",
            "narrateur|Le bol glisse un peu.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Amir a de l'énergie.",
            "narrateur|Que peut faire Victorina ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Victorina va vers maman.",
            "enfant-f|Maman, Amir saute.",
            "enfant-f|Les raisins roulent.",
            "maman|On peut jouer.",
            "maman|On peut attendre.",
            "papa|On peut demander à un adulte.",
            "enfant-f|On pose un raisin chacun ?",
            "maman|Oui.",
            "maman|À tour de rôle.",
            "narrateur|Maman pose un petit bol.",
            "narrateur|Victorina y met des raisins.",
            "narrateur|Amir s'arrête.",
            "narrateur|Il souffle.",
            "narrateur|Il attend son tour.",
            "papa|Tu as demandé.",
            "papa|Bravo, Victorina.",
            "narrateur|Elle pose un raisin.",
            "narrateur|Puis Amir pose un raisin.",
            "narrateur|Le rond grandit.",
            "enfant-m|Encore un.",
            "enfant-f|Encore un.",
            "narrateur|L'escargot apparaît.",
            "narrateur|Une tête, puis la coquille.",
            "narrateur|Amir attend encore.",
            "narrateur|Puis il pose le dernier raisin.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Papa glisse le moule au four.",
            "narrateur|La porte du four fait clic.",
            "narrateur|Ça sent le beurre chaud.",
            "maman|On attend devant la vitre ?",
            "enfant-f|Oui.",
            "enfant-f|L'escargot cuit.",
            "narrateur|Amir s'assoit.",
            "narrateur|Ses pieds ne tapent plus.",
            "narrateur|Victorina pose le bol vide.",
            "papa|Tu as fini de poser le bol ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le nuage de farine est retombé.",
            "narrateur|Le carrelage est calme.",
            "narrateur|La cuillère en bois sèche.",
            "maman|On sent le gâteau, maintenant.",
            "enfant-m|Il est tout chaud.",
            "papa|Oui.",
            "papa|L'escargot aussi.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-f|L'escargot est sur le gâteau.",
            "maman|Tout en rond.",
            "papa|Il sent bon, maintenant.",
            "narrateur|Le bol est vide.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {"CHK_T0000_P0000": "", "CHK_T0000_P0000_Q0001": "", "CHK_T0000_P0000_C0001": "", "CHK_T0000_P0000_END": "", "CHK_T0000_P0000_END_F0001": ""},
    ENE,
    q={
        "expected_answer": "jouer",
        "accepted_examples": "jouer | attendre | maman | un adulte | papa | demander",
        "retry_prompt": "On peut jouer. On peut attendre. Que fait Victorina ?",
    },
)


# ---------------------------------------------------------------------------
# PAR.001-01 N2 — Sarah, Victorina — route de coussins, camion rouge
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.PAR.001-01",
    "Sarah veut que le camion rouge arrive au garage en bois. Victorina parle peu. Sarah lui tend le camion. Elles font une route de coussins. Le camion entre au garage.",
    "Le garage au bout des coussins",
    "Sarah, Victorina, papa, maman",
    "cuisine puis salon, tartine et tapis",
    {
        "CHK_T0000_P0000": [
            "narrateur|Le couvercle du pot de confiture résiste.",
            "narrateur|Un peu de fraise a collé au bord.",
            "narrateur|Des miettes dorées sont sur la table.",
            "narrateur|La tartine sent encore le pain chaud.",
            "papa|Tu as vu la colle de fraise, Sarah ?",
            "enfant-f|Elle est rouge, papa.",
            "maman|On tourne tout doux.",
            "narrateur|Le couvercle part.",
            "narrateur|Ça fait un petit toc.",
            "narrateur|Sarah lèche un doigt.",
            "enfant-f|C'est sucré.",
            "maman|Un peu, pas trop.",
            "narrateur|Le camion rouge attend près du tapis.",
            "narrateur|Ses roues sont un peu poussiéreuses.",
            "narrateur|Le garage en bois est au bout du salon.",
            "narrateur|La porte du garage est ouverte.",
            "narrateur|En ce moment, Sarah pose un coussin.",
            "narrateur|Puis un autre coussin.",
            "enfant-f|Je fais une route.",
            "enfant-f|Jusqu'au garage.",
            "papa|Pour le camion rouge ?",
            "enfant-f|Oui.",
            "enfant-f|Il doit arriver.",
            "narrateur|La porte s'ouvre.",
            "narrateur|Victorina arrive avec son sac.",
            "narrateur|Le sac frotte le parquet.",
            "narrateur|Victorina parle peu.",
            "narrateur|Elle regarde le sol.",
            "narrateur|Sarah a envie de tout raconter.",
            "narrateur|La tartine.",
            "narrateur|La fraise.",
            "narrateur|La route.",
            "narrateur|Les mots montent très vite.",
            "maman|On peut attendre.",
            "papa|Tu peux tendre un jouet.",
            "narrateur|Sarah tient le camion rouge.",
            "narrateur|Les roues sont encore froides.",
            "narrateur|Victorina ne dit rien.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Victorina parle peu.",
            "narrateur|Que fait Sarah ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Sarah respire.",
            "narrateur|Elle tend le camion.",
            "enfant-f|Pour toi.",
            "narrateur|Elle attend.",
            "narrateur|On n'entend plus que l'horloge.",
            "narrateur|Victorina prend le camion.",
            "narrateur|Elle ne dit rien.",
            "maman|On ne force pas la parole.",
            "papa|Regarder, c'est déjà jouer.",
            "narrateur|Sarah pose encore un coussin.",
            "narrateur|Victorina pousse le camion.",
            "narrateur|Les roues font un petit bruit.",
            "narrateur|La route grandit.",
            "narrateur|Le garage se rapproche.",
            "enfant-f|Encore un coussin.",
            "narrateur|Victorina le pose.",
            "narrateur|Puis elle dit tout bas.",
            "enfant-f|Vroom.",
            "enfant-f|Vroom.",
            "papa|Tu as su attendre.",
            "papa|Bravo, Sarah.",
            "narrateur|Le camion entre dans le garage.",
            "narrateur|Toc.",
            "maman|Il est arrivé.",
            "narrateur|Sarah passe la main sur le toit.",
            "narrateur|Le plastique est tiède.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Maman apporte deux tartines.",
            "narrateur|La confiture brille encore.",
            "maman|Vous voulez un goûter ?",
            "narrateur|Victorina secoue la tête.",
            "enfant-f|D'accord.",
            "papa|D'accord.",
            "narrateur|Sarah croque un coin.",
            "narrateur|Victorina reste près du garage.",
            "narrateur|Elle tient encore le camion.",
            "narrateur|Sarah attend.",
            "narrateur|Puis Victorina s'assoit.",
            "narrateur|Elle croque un morceau de pomme.",
            "maman|Tu as fini ta route, Sarah ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Le camion est au garage.",
            "papa|Les miettes sont encore là.",
            "narrateur|Le couvercle repose sur le pot.",
            "narrateur|La fraise sent encore un peu.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-f|Le camion est arrivé.",
            "maman|Au bout des coussins.",
            "papa|La tartine est finie, aussi.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {k: "" for k in (
        "CHK_T0000_P0000",
        "CHK_T0000_P0000_Q0001",
        "CHK_T0000_P0000_C0001",
        "CHK_T0000_P0000_END",
        "CHK_T0000_P0000_END_F0001",
    )},
    PAR,
    q={
        "expected_answer": "attendre",
        "accepted_examples": "attendre | tendre un jouet | un jouet | le camion | elle attend",
        "retry_prompt": "Elle tend un jouet. Elle attend. Que fait Sarah ?",
    },
)


# ---------------------------------------------------------------------------
# PAR.001-02 N2 — Nino, Mila — puits dans le sable
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.PAR.001-02",
    "Nino veut un puits dans le sable pour le seau rouge. Mila parle peu. Il lui tend le seau. Ils creusent. L'eau de la gourde tombe dans le puits.",
    "Le puits du seau rouge",
    "Nino, Mila, papa, maman",
    "parc, bac à sable, couverture à carreaux",
    {
        "CHK_T0000_P0000": [
            "narrateur|Une cigale chante tout près du bac.",
            "narrateur|Le sable sent encore le soleil.",
            "narrateur|Un oiseau gris picore près du banc.",
            "narrateur|Papa pose le sac de goûter.",
            "narrateur|Le sac fait un bruit de papier.",
            "narrateur|Maman déplie une couverture à carreaux.",
            "narrateur|Les carreaux sont bleus et blancs.",
            "papa|Tu as entendu la cigale, Nino ?",
            "enfant-m|Elle chante fort.",
            "maman|Le sable est encore chaud.",
            "enfant-m|Je veux un puits.",
            "enfant-m|Pour le seau rouge.",
            "papa|Un puits dans le bac ?",
            "enfant-m|Oui.",
            "enfant-m|Bien creux.",
            "narrateur|En ce moment, Nino s'assoit près du bac.",
            "narrateur|Le seau rouge est tiède.",
            "narrateur|Une pelle jaune est à côté.",
            "narrateur|Le manche est un peu rêche.",
            "narrateur|Mila est déjà là.",
            "narrateur|Elle parle peu.",
            "narrateur|Elle regarde ses mains.",
            "narrateur|Le sable y brille un peu.",
        ],
        "CHK_T0000_P0000_X": [
            "narrateur|Nino a envie de tout expliquer.",
            "narrateur|Le puits.",
            "narrateur|L'eau.",
            "narrateur|Le seau.",
            "narrateur|Les mots restent un moment.",
            "maman|On peut attendre.",
            "papa|Tu peux tendre un jouet.",
            "narrateur|Nino tient le seau rouge.",
            "narrateur|Le plastique est tiède.",
            "narrateur|Mila ne dit rien.",
            "narrateur|Un grain de sable roule sur le bord.",
            "narrateur|La cigale chante encore.",
            "narrateur|Nino reste assis.",
        ],
        "CHK_T0000_P0000_X_Q0001": [
            "narrateur|Mila parle peu.",
            "narrateur|Que fait Nino ?",
        ],
        "CHK_T0000_P0000_X_C0001": [
            "narrateur|Nino tend le seau.",
            "enfant-m|Pour le puits.",
            "narrateur|Il attend.",
            "narrateur|Mila touche le seau.",
            "narrateur|Elle ne dit rien.",
            "maman|On ne force pas la parole.",
            "papa|Le seau peut suffire.",
            "narrateur|Mila prend le seau.",
            "narrateur|Elle le remplit.",
            "narrateur|Le sable fait un bruit doux.",
            "narrateur|Nino creuse avec la pelle jaune.",
            "narrateur|Un trou rond s'ouvre.",
            "narrateur|Mila verse le seau.",
            "narrateur|Le puits grandit.",
            "enfant-m|Encore un peu.",
            "narrateur|Mila verse encore.",
            "narrateur|Puis elle dit tout bas.",
            "enfant-f|Puits.",
            "enfant-m|Puits.",
            "papa|Tu as su attendre.",
            "papa|Bravo, Nino.",
            "narrateur|Maman ouvre la gourde.",
            "narrateur|Un filet d'eau tombe dans le trou.",
            "narrateur|Le fond devient sombre.",
            "enfant-f|Eau.",
            "enfant-m|Eau.",
        ],
        "CHK_T0000_P0000_X_END": [
            "narrateur|Le puits brille un peu.",
            "narrateur|Le bord est encore chaud.",
            "narrateur|La cigale chante encore.",
            "maman|Une compote ?",
            "narrateur|Mila secoue la tête.",
            "enfant-m|D'accord.",
            "papa|D'accord.",
            "maman|Tu as fini le puits, Nino ?",
            "enfant-m|Oui, maman.",
            "enfant-m|Il a de l'eau.",
            "narrateur|Papa plie un coin de couverture.",
            "narrateur|Nino pose le seau à l'ombre.",
            "narrateur|Mila reste près du trou.",
            "narrateur|Elle regarde l'eau.",
            "narrateur|Un grain colle encore à son genou.",
            "papa|L'oiseau s'est envolé.",
            "narrateur|Le bac reste chaud.",
            "narrateur|La couverture à carreaux est un peu sablée.",
            "enfant-m|Le sable colle.",
        ],
        "CHK_T0000_P0000_X_END_F0001": [
            "enfant-m|On a fait un puits.",
            "maman|Avec le seau rouge.",
            "papa|L'eau est au fond.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "enfants_parc",
        "CHK_T0000_P0000_X": "enfants_parc",
        "CHK_T0000_P0000_X_Q0001": "",
        "CHK_T0000_P0000_X_C0001": "enfants_parc",
        "CHK_T0000_P0000_X_END": "",
        "CHK_T0000_P0000_X_END_F0001": "",
    },
    PAR,
    q={
        "expected_answer": "attendre",
        "accepted_examples": "attendre | tendre | le seau | un jouet | il attend",
        "retry_prompt": "Il tend un jouet. Il attend. Que fait Nino ?",
    },
    qid="CHK_T0000_P0000_X_Q0001",
)


# ---------------------------------------------------------------------------
# PAR.001-03 N3 — Mila, Aniss — voiture verte, puis chemin de sable
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.PAR.001-03",
    "Mila veut que la voiture verte arrive à la maison de cubes. Aniss parle peu. Elle lui tend la voiture. Plus tard au parc, elle lui tend un seau. Ils font un chemin de sable.",
    "La maison au bout du tapis",
    "Mila, Aniss, papa, maman",
    "entrée mouillée, classe, puis parc",
    {
        "CHK_T0000_P0000": [
            "narrateur|Une goutte tombe du manteau rouge.",
            "narrateur|Elle fait un rond sombre sur le carrelage.",
            "narrateur|Le manteau sent encore la pluie.",
            "narrateur|Les casiers sont un peu froids.",
            "narrateur|Un cartable frotte le bois.",
            "narrateur|Papa noue les lacets de Mila.",
            "narrateur|Les lacets font un bruit de tissu.",
            "maman|Tu as ton goûter dans la poche.",
            "papa|Les lacets sont bien faits ?",
            "enfant-f|Oui, papa.",
            "narrateur|Un cube jaune attend sur le tapis.",
            "narrateur|Puis un cube bleu.",
            "narrateur|Le tapis sent un peu la laine.",
            "narrateur|En ce moment, Mila pose les cubes.",
            "narrateur|Le cube jaune est lisse.",
            "enfant-f|Je fais une maison.",
            "enfant-f|Pour la voiture verte.",
            "maman|Une maison au bout du tapis ?",
            "enfant-f|Oui.",
            "enfant-f|Elle doit arriver.",
            "narrateur|Aniss arrive.",
            "narrateur|Aniss parle peu.",
            "narrateur|Il regarde le tapis.",
            "narrateur|Mila a envie de poser beaucoup de questions.",
            "narrateur|Elle referme un peu la bouche.",
            "maman|On peut attendre.",
            "papa|Tu peux tendre un jouet.",
            "narrateur|La voiture verte est dans sa main.",
            "narrateur|Les roues sont lisses.",
            "narrateur|Aniss ne dit rien.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Aniss parle peu.",
            "narrateur|Que fait Mila ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Mila tend la voiture.",
            "enfant-f|Pour la maison.",
            "narrateur|Elle attend.",
            "narrateur|Un oiseau chante derrière la vitre.",
            "narrateur|Aniss prend la voiture.",
            "narrateur|Il la fait rouler.",
            "narrateur|Les roues font un petit rrr.",
            "maman|On ne force pas la parole.",
            "papa|La voiture peut parler pour vous.",
            "narrateur|Ils posent encore des cubes.",
            "narrateur|Un toit.",
            "narrateur|Un mur.",
            "narrateur|Une porte.",
            "narrateur|La maison a une porte.",
            "narrateur|La voiture entre.",
            "narrateur|Les roues s'arrêtent.",
            "enfant-f|Elle est arrivée.",
            "narrateur|Aniss dit tout bas.",
            "enfant-m|Maison.",
            "enfant-f|Maison.",
            "papa|Tu as su attendre.",
            "papa|Bravo, Mila.",
            "narrateur|Plus tard, au parc, le sable est frais.",
            "narrateur|Papa s'assoit sur le banc.",
            "narrateur|Le bois du banc est un peu froid.",
            "narrateur|Aniss est là aussi.",
            "narrateur|Il parle encore peu.",
            "narrateur|Mila se souvient.",
            "narrateur|Elle tend le seau bleu.",
            "narrateur|Le seau est un peu rêche.",
            "narrateur|Aniss le pousse.",
            "narrateur|Un chemin de sable s'allonge.",
            "narrateur|Il va jusqu'au bac.",
            "enfant-m|Chemin.",
            "enfant-f|Chemin.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Maman aide Aniss à mettre son manteau.",
            "narrateur|Le manteau sent encore la pluie.",
            "narrateur|Aniss fait un petit signe.",
            "papa|À demain ?",
            "enfant-f|À demain.",
            "maman|Le chemin reste dans le bac.",
            "enfant-f|Et la maison, à l'école.",
            "papa|Deux arrivées, aujourd'hui.",
            "narrateur|Le banc du parc reste vide.",
            "narrateur|Une goutte sèche sur le carrelage, plus tard.",
            "narrateur|Le manteau rouge ne goutte plus.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-f|La voiture est à la maison.",
            "maman|Le seau a fait un chemin.",
            "papa|Deux jeux, peu de mots.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "enfants_parc",
        "CHK_T0000_P0000_END": "",
        "CHK_T0000_P0000_END_F0001": "",
    },
    PAR,
    q={
        "expected_answer": "attendre",
        "accepted_examples": "attendre | tendre un jouet | un jouet | la voiture | elle attend",
        "retry_prompt": "Elle tend un jouet. Elle attend. Que fait Mila ?",
    },
)


# ---------------------------------------------------------------------------
# PAR.001-04 N3 — Amir, Victorina — bateau en papier, puis port de sable
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.PAR.001-04",
    "Amir veut faire flotter son bateau en papier dans le bac d'eau. Victorina parle peu. Il lui tend le bateau. Plus tard au parc, ils font un port de sable. Le bateau a un quai.",
    "Le bateau sur le rebord",
    "Amir, Victorina, papa, maman",
    "classe au bac d'eau, puis parc",
    {
        "CHK_T0000_P0000": [
            "narrateur|Un bateau en papier sèche sur le rebord.",
            "narrateur|Une goutte a marqué la proue.",
            "narrateur|Le papier sent encore la colle.",
            "narrateur|Le pliage est un peu raide.",
            "narrateur|Une fenêtre est entrouverte.",
            "narrateur|L'air sent la craie.",
            "narrateur|Papa range le cartable d'Amir.",
            "narrateur|Maman glisse une pomme dans la poche.",
            "narrateur|La pomme est lisse et froide.",
            "papa|Tu as vu la goutte, Amir ?",
            "enfant-m|Elle a fait une tache.",
            "maman|Je te dis au revoir ici.",
            "maman|Papa t'attend au parc, plus tard.",
            "narrateur|En ce moment, Amir prend le bateau.",
            "narrateur|Le bac d'eau brille près de la fenêtre.",
            "narrateur|L'eau est claire et froide.",
            "enfant-m|Je veux qu'il flotte.",
            "enfant-m|Jusqu'à l'autre bord.",
            "papa|Tout droit, alors.",
            "narrateur|Victorina est déjà là.",
            "narrateur|Victorina parle peu.",
            "narrateur|Elle regarde ses chaussures.",
            "narrateur|Les lacets sont verts.",
            "narrateur|Amir a envie de poser beaucoup de questions.",
            "narrateur|Il respire.",
            "maman|On peut attendre.",
            "papa|Tu peux tendre un jouet.",
            "narrateur|Le bateau est léger dans sa main.",
            "narrateur|Victorina ne dit rien.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Victorina parle peu.",
            "narrateur|Que fait Amir ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Amir tend le bateau.",
            "enfant-m|Pour toi.",
            "narrateur|Il attend.",
            "narrateur|Une feuille tape encore la vitre.",
            "narrateur|Victorina prend le bateau.",
            "narrateur|Elle le pose sur l'eau.",
            "narrateur|Le papier avance tout doux.",
            "maman|On ne force pas la parole.",
            "papa|Le bateau n'a pas besoin de mots.",
            "narrateur|Amir souffle un peu.",
            "narrateur|Une petite vague va jusqu'au bord.",
            "narrateur|Le bateau touche l'autre bord.",
            "narrateur|Le papier est un peu mouillé.",
            "enfant-m|Il est arrivé.",
            "narrateur|Victorina dit tout bas.",
            "enfant-f|Bateau.",
            "enfant-m|Bateau.",
            "papa|Tu as su attendre.",
            "papa|Bravo, Amir.",
            "narrateur|Plus tard, au parc, papa est au banc.",
            "narrateur|Maman arrive avec le goûter.",
            "narrateur|Le sac sent la pomme.",
            "narrateur|Victorina est là aussi.",
            "narrateur|Amir tend un seau.",
            "narrateur|Le seau est tiède.",
            "narrateur|Victorina le remplit de sable.",
            "narrateur|Ils font un port, tout bas.",
            "narrateur|Le sable est frais sous les doigts.",
            "narrateur|Un quai.",
            "narrateur|Une crique.",
            "narrateur|Un trou d'eau.",
            "enfant-f|Port.",
            "enfant-m|Port.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Maman aide Victorina à mettre son manteau.",
            "narrateur|Les boutons sont ronds et lisses.",
            "narrateur|Victorina fait un petit signe.",
            "papa|À demain ?",
            "enfant-m|À demain.",
            "maman|Le bateau sèche encore sur le rebord.",
            "enfant-m|Et le port reste au parc.",
            "papa|Deux eaux, aujourd'hui.",
            "narrateur|La pomme reste dans la poche.",
            "narrateur|Le bateau sèche encore un peu.",
            "enfant-m|La tache est partie.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-m|Le bateau a touché l'autre bord.",
            "maman|Le port a un quai.",
            "papa|Peu de mots, deux voyages.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "",
        "CHK_T0000_P0000_Q0001": "",
        "CHK_T0000_P0000_C0001": "enfants_parc",
        "CHK_T0000_P0000_END": "",
        "CHK_T0000_P0000_END_F0001": "",
    },
    PAR,
    q={
        "expected_answer": "attendre",
        "accepted_examples": "attendre | tendre un jouet | un jouet | le bateau | il attend",
        "retry_prompt": "Il tend un jouet. Il attend. Que fait Amir ?",
    },
)


# ---------------------------------------------------------------------------
# PAR.001-05 N2 — Nina, Raphaël — haricot sous le châssis
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.PAR.001-05",
    "Nina veut planter un haricot sous le châssis embué. Raphaël parle peu. Elle lui tend la petite pelle. Ils font un trou. Le haricot disparaît sous la terre tiède.",
    "Le haricot sous la buée",
    "Nina, Raphaël, papa, maman",
    "jardin, châssis, thym",
    {
        "CHK_T0000_P0000": [
            "narrateur|La vitre du châssis est toute embuée.",
            "narrateur|Un doigt y a dessiné un petit rond.",
            "narrateur|Ça sent le thym et la terre chaude.",
            "narrateur|Une abeille passe près du romarin.",
            "narrateur|Les pots sont encore humides.",
            "narrateur|Papa arrose les pots.",
            "narrateur|L'eau fait un bruit fin.",
            "narrateur|Maman pose un chapeau de paille.",
            "narrateur|Le chapeau sent le soleil.",
            "papa|Tu as vu le rond, Nina ?",
            "enfant-f|Il est sur la buée.",
            "maman|Le thym sent fort, hein ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Je veux planter un haricot.",
            "enfant-f|Sous le châssis.",
            "papa|Un haricot à lui, tout seul ?",
            "enfant-f|Oui.",
            "enfant-f|Dans un petit trou.",
            "narrateur|En ce moment, Nina s'agenouille.",
            "narrateur|La petite pelle est lisse.",
            "narrateur|Le haricot est dans sa poche.",
            "narrateur|Il fait un petit bruit.",
            "narrateur|Raphaël est déjà là.",
            "narrateur|Il parle peu.",
            "narrateur|Il regarde une coccinelle sur le rebord.",
            "narrateur|La coccinelle est rouge et ronde.",
            "narrateur|Nina a envie de tout expliquer.",
            "maman|On peut attendre.",
            "papa|Tu peux tendre un jouet.",
            "narrateur|Nina tient la petite pelle.",
            "narrateur|Raphaël ne dit rien.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Raphaël parle peu.",
            "narrateur|Que fait Nina ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Nina tend la petite pelle.",
            "enfant-f|Pour le trou.",
            "narrateur|Elle attend.",
            "narrateur|Un grain de terre colle à son genou.",
            "narrateur|Raphaël touche la pelle.",
            "narrateur|Il ne dit rien.",
            "maman|On ne force pas la parole.",
            "papa|La terre n'a pas besoin de mots.",
            "narrateur|Raphaël prend la pelle.",
            "narrateur|Il creuse près du thym.",
            "narrateur|Nina pose le haricot.",
            "narrateur|Il est lisse et un peu froid.",
            "narrateur|Raphaël recouvre.",
            "narrateur|La terre est tiède.",
            "narrateur|Elle sent le jardin.",
            "narrateur|Un peu l'eau.",
            "narrateur|Un peu le thym.",
            "enfant-f|Il est caché.",
            "narrateur|Puis Raphaël dit tout bas.",
            "enfant-m|Haricot.",
            "enfant-f|Haricot.",
            "papa|Tu as su attendre.",
            "papa|Bravo, Nina.",
            "narrateur|Papa verse un peu d'eau.",
            "narrateur|La terre devient sombre.",
            "narrateur|Une petite flaque brille, puis s'en va.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Maman essuie un peu la buée.",
            "narrateur|Le rond a disparu.",
            "narrateur|On voit le haricot caché, presque.",
            "maman|Un peu d'eau, pour toi ?",
            "narrateur|Raphaël secoue la tête.",
            "enfant-f|D'accord.",
            "papa|D'accord.",
            "maman|Tu as fini le trou, Nina ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Le haricot est dessous.",
            "narrateur|Papa ferme le robinet.",
            "narrateur|L'eau s'arrête.",
            "narrateur|Nina donne la main.",
            "narrateur|Le chapeau de paille reste sur le banc.",
            "papa|La coccinelle s'en va.",
            "narrateur|Le thym sent encore.",
            "narrateur|L'abeille s'éloigne.",
            "enfant-f|Le thym reste.",
            "papa|Oui.",
            "papa|Il sent encore.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-f|Le haricot est sous la terre.",
            "maman|Sous le châssis.",
            "papa|Il a de l'eau, maintenant.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {k: "" for k in (
        "CHK_T0000_P0000",
        "CHK_T0000_P0000_Q0001",
        "CHK_T0000_P0000_C0001",
        "CHK_T0000_P0000_END",
        "CHK_T0000_P0000_END_F0001",
    )},
    PAR,
    q={
        "expected_answer": "attendre",
        "accepted_examples": "attendre | tendre | la pelle | un jouet | elle attend",
        "retry_prompt": "Elle tend un jouet. Elle attend. Que fait Nina ?",
    },
)


# ---------------------------------------------------------------------------
# PAR.001-06 N2 — Victorino, Sarah — gare de bois sous la pluie
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.PAR.001-06",
    "Victorino veut que la locomotive rouge arrive à la gare de bois. Il pleut. Sarah parle peu. Il lui tend un wagon. Ils posent les rails. La locomotive entre en gare.",
    "La gare sous la pluie",
    "Victorino, Sarah, papa, maman",
    "chambre, jour de pluie, tapis beige",
    {
        "CHK_T0000_P0000": [
            "narrateur|Les chaussettes épaisses sentent le radiateur.",
            "narrateur|Les gouttes tapent, tapent, tapent.",
            "narrateur|Le carreau est tout mouillé.",
            "narrateur|Une goutte glisse, puis s'arrête.",
            "narrateur|Le zinc fait un petit bruit.",
            "narrateur|Un ours en tissu attend sur l'oreiller.",
            "narrateur|Papa apporte encore une paire.",
            "narrateur|Maman ouvre la caisse des rails.",
            "narrateur|Le bois du tiroir glisse.",
            "narrateur|Les rails sentent le bois neuf.",
            "papa|Tu as senti les chaussettes, Victorino ?",
            "enfant-m|Elles sont chaudes.",
            "maman|On reste au sec, là.",
            "enfant-m|Je veux une gare.",
            "enfant-m|Pour la locomotive rouge.",
            "papa|Une gare sur le tapis ?",
            "enfant-m|Oui.",
            "enfant-m|Avec un quai.",
            "narrateur|En ce moment, Victorino est sur le tapis.",
            "narrateur|Le tapis est doux et beige.",
            "narrateur|La locomotive rouge attend près de lui.",
            "narrateur|Ses roues sont froides.",
            "narrateur|La porte s'ouvre.",
            "narrateur|Sarah arrive avec son sac.",
            "narrateur|Le sac est mouillé sur le bord.",
            "narrateur|Une goutte tombe sur le tapis.",
            "narrateur|Sarah parle peu.",
            "narrateur|Elle regarde le sol.",
            "narrateur|Victorino a envie de poser beaucoup de questions.",
            "narrateur|Il respire.",
            "maman|On peut attendre.",
            "papa|Tu peux tendre un jouet.",
            "narrateur|Un wagon bleu est dans sa main.",
            "narrateur|Sarah ne dit rien.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Sarah parle peu.",
            "narrateur|Que fait Victorino ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Victorino tend le wagon.",
            "enfant-m|Pour la gare.",
            "narrateur|Il attend.",
            "narrateur|On entend encore la pluie.",
            "narrateur|Sarah prend le wagon.",
            "narrateur|Elle le pose sur un rail.",
            "narrateur|Clic.",
            "maman|On ne force pas la parole.",
            "papa|Le train peut rouler sans mots.",
            "narrateur|Victorino pose un autre rail.",
            "narrateur|Le bois fait clic.",
            "narrateur|Sarah pose le quai.",
            "narrateur|Un petit rectangle de bois.",
            "narrateur|La locomotive rouge avance.",
            "narrateur|Elle entre en gare.",
            "narrateur|Les roues s'arrêtent au quai.",
            "enfant-m|Elle est arrivée.",
            "narrateur|Puis Sarah dit tout bas.",
            "enfant-f|Train.",
            "enfant-m|Train.",
            "papa|Tu as su attendre.",
            "papa|Bravo, Victorino.",
            "narrateur|L'ours regarde depuis l'oreiller.",
            "narrateur|Un œil en bouton brille.",
            "narrateur|La locomotive reste au quai.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Maman apporte deux bols.",
            "narrateur|La soupe sent la carotte.",
            "maman|Un peu de soupe ?",
            "narrateur|Sarah secoue la tête.",
            "enfant-m|D'accord.",
            "papa|D'accord.",
            "maman|Tu as fini la gare, Victorino ?",
            "enfant-m|Oui, maman.",
            "enfant-m|La locomotive est au quai.",
            "narrateur|Maman aide Sarah à mettre son manteau.",
            "narrateur|Le manteau est encore un peu humide.",
            "narrateur|Sarah fait un petit signe.",
            "papa|À demain ?",
            "enfant-m|À demain.",
            "narrateur|Les chaussettes sèchent encore.",
            "narrateur|L'ours attend sur l'oreiller.",
            "narrateur|La pluie chante encore un peu.",
            "enfant-m|Le zinc aussi.",
            "papa|Oui.",
            "papa|Il chante encore.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-m|Le train est en gare.",
            "maman|Même sous la pluie.",
            "papa|Le quai est prêt.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {k: "" for k in (
        "CHK_T0000_P0000",
        "CHK_T0000_P0000_Q0001",
        "CHK_T0000_P0000_C0001",
        "CHK_T0000_P0000_END",
        "CHK_T0000_P0000_END_F0001",
    )},
    PAR,
    q={
        "expected_answer": "attendre",
        "accepted_examples": "attendre | tendre un jouet | un jouet | le wagon | il attend",
        "retry_prompt": "Il tend un jouet. Il attend. Que fait Victorino ?",
    },
)


# ---------------------------------------------------------------------------
# PAR.001-07 N2 — Chouchou (f), Mila — colline pour l'escargot
# ---------------------------------------------------------------------------
write_story(
    "ATOM-DIF.PAR.001-07",
    "Chouchou veut une colline de terre pour l'escargot de la rambarde. Mila parle peu. Chouchou lui tend la pelle jaune. Elles font la colline. L'escargot avance tout seul.",
    "La colline de l'escargot",
    "Chouchou, Mila, papa, maman",
    "jardin, soir, rambarde",
    {
        "CHK_T0000_P0000": [
            "narrateur|Un escargot avance sur la rambarde.",
            "narrateur|Sa maison brille un peu.",
            "narrateur|L'herbe sent le soir qui arrive.",
            "narrateur|Les chaussures de jardin sont près du mur.",
            "narrateur|Elles sont encore un peu mouillées.",
            "narrateur|Papa cale un arrosoir contre le mur.",
            "narrateur|Maman étend une petite nappe sur le banc.",
            "narrateur|La nappe a des pois blancs.",
            "narrateur|Un coin de nappe vole un peu.",
            "papa|Tu as vu l'escargot, Chouchou ?",
            "enfant-f|Il avance tout seul.",
            "maman|L'herbe sent bon, ce soir.",
            "enfant-f|Je veux une colline.",
            "enfant-f|Pour sa maison.",
            "papa|Une colline de terre ?",
            "enfant-f|Oui.",
            "enfant-f|Tout près des pots.",
            "narrateur|En ce moment, Chouchou tient la pelle jaune.",
            "narrateur|Le manche est lisse.",
            "narrateur|Un seau vert attend près des pots.",
            "narrateur|La terre est un peu grise.",
            "narrateur|Mila est près du bac.",
            "narrateur|Elle parle peu.",
            "narrateur|Elle regarde la terre des pots.",
            "narrateur|Un caillou gris brille un peu.",
            "narrateur|Chouchou a envie de jouer tout de suite.",
            "maman|On peut attendre.",
            "papa|Tu peux tendre un jouet.",
            "narrateur|La pelle jaune est dans sa main.",
            "narrateur|Mila ne dit rien.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Mila parle peu.",
            "narrateur|Que fait Chouchou ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Chouchou tend la pelle.",
            "enfant-f|Pour la colline.",
            "narrateur|Elle attend.",
            "narrateur|Une feuille sèche craque sous son pied.",
            "narrateur|Mila touche la pelle.",
            "narrateur|Elle ne dit rien.",
            "maman|On ne force pas la parole.",
            "papa|L'escargot n'a pas besoin de mots.",
            "narrateur|Mila prend la pelle.",
            "narrateur|Elle pousse un peu de terre.",
            "narrateur|Chouchou pose le seau vert.",
            "narrateur|Mila verse.",
            "narrateur|Un petit tas grandit.",
            "narrateur|La terre est fraîche sous les doigts.",
            "narrateur|Elle sent le soir.",
            "enfant-f|La colline.",
            "narrateur|Puis Mila dit tout bas.",
            "enfant-f|Terre.",
            "enfant-f|Terre.",
            "papa|Tu as su attendre.",
            "papa|Bravo, Chouchou.",
            "narrateur|L'escargot arrive au bout de la rambarde.",
            "narrateur|Il glisse vers la colline.",
            "narrateur|Ses cornes sortent tout doux.",
            "narrateur|La terre est un peu humide.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Maman ouvre la gourde.",
            "narrateur|L'eau sent le plastique tiède.",
            "maman|Un peu d'eau ?",
            "narrateur|Mila secoue la tête.",
            "enfant-f|D'accord.",
            "papa|D'accord.",
            "maman|Tu as fini la colline, Chouchou ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Il grimpe dessus.",
            "narrateur|Maman range la nappe à pois.",
            "narrateur|Les pois sont un peu sablés.",
            "narrateur|Papa reprend l'arrosoir.",
            "narrateur|Chouchou donne la main.",
            "papa|Les chaussures sèchent encore.",
            "narrateur|L'escargot reste sur la colline.",
            "narrateur|Sa maison brille encore un peu.",
            "enfant-f|Il avance tout seul.",
            "maman|Oui.",
            "maman|Tout seul.",
            "narrateur|L'herbe est plus fraîche.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "enfant-f|L'escargot a sa colline.",
            "maman|Près des pots.",
            "papa|Sa maison brille encore.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {k: "" for k in (
        "CHK_T0000_P0000",
        "CHK_T0000_P0000_Q0001",
        "CHK_T0000_P0000_C0001",
        "CHK_T0000_P0000_END",
        "CHK_T0000_P0000_END_F0001",
    )},
    PAR,
    q={
        "expected_answer": "attendre",
        "accepted_examples": "attendre | tendre | la pelle | un jouet | elle attend",
        "retry_prompt": "Elle tend un jouet. Elle attend. Que fait Chouchou ?",
    },
)
