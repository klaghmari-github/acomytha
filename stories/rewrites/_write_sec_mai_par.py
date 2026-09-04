#!/usr/bin/env python3
"""F-NAR-009 — merged.json pour ATOM-SEC.MAI.003-07/08 et ATOM-SEC.PAR.001-01..06."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIMITS = {"N1": 10, "N2": 15, "N3": 18}
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
)
BALCON_FORBIDDEN = (
    "sauter",
    "saute",
    "descendre",
    "descente",
    "grimper",
    "grimpe",
)
BAD_NAMES = (
    "yseult",
    "éric",
    "eric",
    "jules",
    "zoé",
    "zoe",
    "noé",
    "noe",
    "inès",
    "ines",
    "kamil",
    "tania",
    "tom ",
    "léa",
    "lea ",
    "lina",
    "iris",
    "rania",
    "kilian",
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


def make_chunk(src: dict, lines: list[str], sons) -> dict:
    text, script = from_script(lines)
    nc = dict(src)
    nc["text"] = text
    nc["script"] = script
    if sons is not None:
        nc["sons"] = sons
    return nc


def check(sid: str, age: str, chunks: list[dict], need_msgs: tuple[str, ...]) -> None:
    lim = LIMITS[age]
    joined = "\n".join(c["script"] for c in chunks)
    low = joined.lower()
    for bad in FORBIDDEN:
        if bad in low:
            raise SystemExit(f"{sid} interdit: {bad}")
    if "MAI.003" in sid:
        for bad in BALCON_FORBIDDEN:
            if bad in low:
                raise SystemExit(f"{sid} interdit balcon: {bad}")
    for name in BAD_NAMES:
        if name in low:
            raise SystemExit(f"{sid} prénom hors troupe: {name}")
    adults = [ln for ln in joined.splitlines() if ln.startswith("papa|") or ln.startswith("maman|")]
    if not adults:
        raise SystemExit(f"{sid}: aucun papa/maman")
    aj = " ".join(a.split("|", 1)[1] for a in adults).lower()
    if "bravo" not in aj and "bon travail" not in aj:
        raise SystemExit(f"{sid}: pas de félicitation")
    if not any("?" in a for a in adults):
        raise SystemExit(f"{sid}: aucune question d'adulte")
    all_text = " ".join(c["text"] for c in chunks).lower()
    for m in need_msgs:
        if m.lower() not in all_text:
            raise SystemExit(f"{sid}: message manquant: {m}")
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


def write_story(
    sid: str,
    fil: str,
    title: str,
    chars: str,
    setting: str,
    scripts: dict,
    sons: dict,
) -> None:
    folder = ROOT / sid
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"{sid} chunks missing={missing} extra={extra}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        by[cid] = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons")))
    out = dict(src)
    out["fil_rouge"] = fil
    out["title"] = title
    out["characters"] = chars
    out["setting"] = setting
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    age = out["age_band"]
    need = {
        "SEC.MAI.003": ("pieds au sol", "protection", "adulte"),
        "SEC.PAR.001": ("espace montré", "adulte voit"),
    }[out["lesson_id"]]
    check(sid, age, out["chunks"], need)
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


# ---------------------------------------------------------------------------
# ATOM-SEC.MAI.003-07 N3 Victorina, papa, balcon, géranium, toits mouillés
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SEC.MAI.003-07",
    "Après la pluie, Victorina et papa regardent les toits depuis le balcon. Pieds au sol, derrière la protection, avec papa.",
    "Les toits mouillés de Victorina",
    "Victorina, papa",
    "balcon après la pluie",
    {
        "CHK_T0000_P0000": [
            "narrateur|Une goutte glisse sur une feuille.",
            "narrateur|La feuille est d'un géranium rouge.",
            "narrateur|Les tuiles brillent encore.",
            "narrateur|La cuisine sent la soupe.",
            "narrateur|Un chat gris s'assoit sur le toit d'à côté.",
            "narrateur|Le rideau jaune bouge un peu.",
            "papa|Tu as vu le chat, Victorina ?",
            "enfant-f|Il est tout gris, papa.",
            "papa|Oui.",
            "papa|Il se tient tranquille.",
            "narrateur|Le carreau près de la porte est froid.",
            "narrateur|Victorina pose la main dessus.",
            "enfant-f|Il est froid.",
            "papa|Oui, la pluie l'a mouillé.",
            "narrateur|En ce moment, papa ouvre la porte du balcon.",
            "narrateur|L'air sent la pluie et la soupe.",
            "papa|On va regarder les toits.",
            "papa|On reste avec un adulte.",
            "papa|Papa, c'est l'adulte.",
            "narrateur|Victorina tient le manteau de papa.",
            "narrateur|Le manteau est épais et un peu humide.",
            "papa|Pieds au sol.",
            "papa|Derrière la protection.",
            "narrateur|Victorina pose les pieds au sol.",
            "narrateur|Elle sent le sol sous les chaussettes.",
            "narrateur|Les chaussettes sont grises et douces.",
            "narrateur|Elle reste derrière la protection.",
            "narrateur|La protection est lisse sous sa main.",
            "enfant-f|Elle est lisse, papa.",
            "papa|Oui.",
            "papa|On reste derrière la protection.",
            "narrateur|Victorina regarde les toits.",
            "narrateur|Les tuiles sont brunes et brillantes.",
            "narrateur|Le chat gris lèche une patte.",
            "enfant-f|Le chat, papa.",
            "papa|Je le vois.",
            "papa|Tes pieds au sol ?",
            "enfant-f|Pieds au sol.",
            "papa|Bravo.",
            "narrateur|Un pigeon passe au-dessus des tuiles.",
            "narrateur|Ses ailes font un petit bruit mou.",
            "enfant-f|Le pigeon vole.",
            "papa|Oui.",
            "papa|On le regarde d'ici.",
            "papa|Derrière la protection.",
            "papa|Avec un adulte.",
            "narrateur|Victorina serre le manteau de papa.",
            "narrateur|Le vent est doux sur ses joues.",
            "narrateur|Une autre goutte tombe du géranium.",
            "narrateur|Elle fait tic sur le carreau.",
            "papa|Tu as entendu la goutte ?",
            "enfant-f|Tic.",
            "papa|Oui.",
            "papa|Tu as fait du bon travail.",
            "narrateur|Victorina respire l'air mouillé.",
            "narrateur|Elle garde les pieds au sol.",
            "narrateur|Elle reste derrière la protection.",
            "papa|On rentre pour la soupe ?",
            "enfant-f|Oui, papa.",
            "narrateur|Ils rentrent ensemble.",
            "narrateur|Papa ferme la porte.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Victorina est sur le balcon.",
            "narrateur|Que fait-elle ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Victorina a gardé les pieds au sol.",
            "narrateur|Elle est restée derrière la protection.",
            "narrateur|Avec papa, l'adulte.",
            "papa|Tu as gardé les pieds au sol ?",
            "enfant-f|Oui.",
            "enfant-f|Derrière la protection.",
            "papa|Bravo.",
            "papa|C'est du bon travail.",
            "narrateur|Le chat est encore sur le toit.",
            "narrateur|Le géranium rouge brille un peu.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|La soupe fume dans les bols.",
            "narrateur|Elle sent la carotte.",
            "narrateur|Victorina s'assoit.",
            "narrateur|Ses chaussettes grises sont un peu froides.",
            "papa|Tu as regardé les toits avec moi ?",
            "enfant-f|Oui.",
            "enfant-f|Le chat était gris.",
            "papa|Et tes pieds ?",
            "enfant-f|Pieds au sol.",
            "papa|Derrière la protection.",
            "papa|Avec un adulte.",
            "papa|Bravo, Victorina.",
            "narrateur|Victorina souffle sur la soupe.",
            "narrateur|La vapeur chatouille son nez.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le rideau jaune ne bouge plus.",
            "narrateur|Les tuiles sèchent tout doucement.",
            "enfant-f|On a vu les toits.",
            "papa|Oui.",
            "papa|Pieds au sol, derrière la protection.",
            "papa|Bravo, Victorina.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {},
)

# ---------------------------------------------------------------------------
# ATOM-SEC.MAI.003-08 N2 Raphaël, papa, maman, serviette, pince à linge
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SEC.MAI.003-08",
    "Une pince en bois attend. Raphaël aide à étendre la serviette, puis il regarde dehors avec papa, puis avec maman. Pieds au sol, derrière la protection.",
    "La serviette bleue de Raphaël",
    "Raphaël, papa, maman",
    "balcon de l'appartement",
    {
        "CHK_T0000_P0000": [
            "narrateur|Une pince en bois dort sur le carrelage.",
            "narrateur|Elle est lisse et un peu ronde.",
            "narrateur|Une serviette bleue sent le savon.",
            "narrateur|La vitre a un peu de buée.",
            "narrateur|Un doigt de Raphaël dessine un rond.",
            "papa|Tu as vu la pince, Raphaël ?",
            "enfant-m|Elle dormait, papa.",
            "papa|On la prend ?",
            "narrateur|Raphaël ramasse la pince.",
            "narrateur|Le bois est tiède dans sa main.",
            "narrateur|En ce moment, papa ouvre le balcon.",
            "narrateur|L'air sent la pluie et le savon.",
            "papa|On étend la serviette.",
            "papa|On reste avec un adulte.",
            "papa|Papa, c'est l'adulte.",
            "papa|Pieds au sol.",
            "papa|Derrière la protection.",
            "narrateur|Raphaël pose les pieds au sol.",
            "narrateur|Il sent le sol sous les chaussettes.",
            "narrateur|Il reste derrière la protection.",
            "narrateur|La protection est solide sous sa main.",
            "enfant-m|Elle est solide, papa.",
            "papa|Oui.",
            "papa|On reste derrière.",
            "narrateur|Papa tend la serviette bleue.",
            "narrateur|Raphaël donne la pince.",
            "narrateur|La pince fait clic.",
            "papa|Bravo.",
            "papa|La serviette tient.",
            "narrateur|Raphaël tient le manteau de papa.",
            "narrateur|Il regarde les toits.",
            "narrateur|Un oiseau passe, tout petit.",
            "enfant-m|L'oiseau, papa.",
            "papa|Je le vois.",
            "papa|Tes pieds au sol ?",
            "enfant-m|Pieds au sol.",
            "papa|Avec un adulte.",
            "papa|Bravo.",
            "narrateur|Ils rentrent ensemble.",
            "narrateur|Papa ferme la porte.",
            "narrateur|Plus tard, maman ouvre aussi le balcon.",
            "narrateur|La serviette bleue bouge un peu.",
            "maman|On va voir si elle sèche.",
            "maman|Pieds au sol.",
            "maman|Derrière la protection.",
            "maman|Avec un adulte.",
            "narrateur|Raphaël pose encore les pieds au sol.",
            "narrateur|Il reste derrière la protection.",
            "narrateur|Il tient la manche de maman.",
            "enfant-m|Elle est presque sèche.",
            "maman|Oui.",
            "maman|Tu restes avec moi.",
            "maman|Bravo, Raphaël.",
            "maman|Tu as fait du bon travail.",
            "narrateur|Ils rentrent.",
            "narrateur|Maman ferme la porte.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Raphaël est sur le balcon.",
            "narrateur|Que fait-il ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Raphaël a gardé les pieds au sol.",
            "narrateur|Derrière la protection.",
            "narrateur|Avec papa, l'adulte.",
            "narrateur|Puis avec maman, l'adulte.",
            "papa|Tu as gardé les pieds au sol ?",
            "enfant-m|Oui.",
            "maman|Derrière la protection ?",
            "enfant-m|Oui, maman.",
            "papa|Bravo.",
            "maman|C'est du bon travail.",
            "narrateur|La pince en bois est rentrée.",
            "narrateur|La serviette sent encore le savon.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Raphaël s'assoit près de maman.",
            "narrateur|Ses chaussettes sont un peu froides.",
            "narrateur|La buée a disparu de la vitre.",
            "maman|La serviette sèche dehors ?",
            "enfant-m|Oui.",
            "papa|Et toi, tu es rentré avec nous.",
            "papa|Pieds au sol.",
            "maman|Derrière la protection.",
            "papa|Avec un adulte.",
            "enfant-m|Avec papa et maman.",
            "maman|Bravo, Raphaël.",
            "narrateur|Raphaël pose la pince sur la table.",
            "narrateur|Le bois fait un petit bruit doux.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|La serviette bleue sèche au vent.",
            "enfant-m|On a mis la pince.",
            "papa|Oui.",
            "maman|Pieds au sol, derrière la protection.",
            "papa|Bravo, Raphaël.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {},
)

# ---------------------------------------------------------------------------
# ATOM-SEC.PAR.001-01 N1 Nino, papa, seau jaune, bac à sable
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SEC.PAR.001-01",
    "Le seau jaune de Nino va au bac à sable. Papa montre l'espace. Nino reste où l'adulte voit.",
    "Le seau jaune de Nino",
    "Nino, papa",
    "parc, bac à sable",
    {
        "CHK_T0000_P0000": [
            "narrateur|Un seau jaune attend près des bottes.",
            "narrateur|Les bottes sont un peu mouillées.",
            "narrateur|Le pain sent bon, loin.",
            "narrateur|L'herbe sent la pluie.",
            "narrateur|Une feuille est collée sur une botte.",
            "papa|Tu as vu le seau, Nino ?",
            "enfant-m|Il est jaune, papa.",
            "papa|Oui.",
            "papa|On le prend.",
            "narrateur|Nino prend le seau.",
            "narrateur|Le plastique est lisse.",
            "narrateur|La pelle est dedans.",
            "narrateur|La pelle est rouge.",
            "papa|On met tes bottes ?",
            "narrateur|Nino enfile une botte.",
            "narrateur|Puis l'autre botte.",
            "papa|Tu as fini tes bottes ?",
            "enfant-m|Oui, papa.",
            "papa|Bravo.",
            "narrateur|Ils marchent vers le parc.",
            "narrateur|Une goutte tombe d'une feuille.",
            "narrateur|Elle fait tic sur le seau.",
            "enfant-m|Tic.",
            "papa|Oui.",
            "papa|C'est une goutte.",
            "narrateur|En ce moment, ils arrivent au parc.",
            "narrateur|Le bac à sable est là.",
            "narrateur|Le sable est frais.",
            "papa|Tu joues ici.",
            "papa|C'est l'espace montré.",
            "papa|Ici, l'adulte voit.",
            "narrateur|Nino va au bac à sable.",
            "narrateur|Il reste dans l'espace montré.",
            "narrateur|Papa s'assoit sur le banc.",
            "narrateur|Le banc est un peu humide.",
            "narrateur|Papa voit Nino.",
            "narrateur|L'adulte voit.",
            "narrateur|Nino verse le sable.",
            "narrateur|Le sable est frais et un peu froid.",
            "enfant-m|Il est froid, papa.",
            "papa|Oui.",
            "papa|Il est frais.",
            "narrateur|Nino fait un gâteau.",
            "narrateur|Il tape le seau.",
            "narrateur|Ça fait toc toc.",
            "papa|Je te vois.",
            "papa|Tu restes dans l'espace montré ?",
            "enfant-m|Oui.",
            "papa|Bravo.",
            "narrateur|Nino retourne le seau.",
            "narrateur|Le gâteau de sable est là.",
            "narrateur|Il est un peu croulé.",
            "enfant-m|Un gâteau !",
            "papa|Beau gâteau.",
            "papa|L'adulte voit.",
            "papa|Tu as fait du bon travail.",
            "narrateur|Nino reste dans l'espace.",
            "narrateur|Les mains sont dans le sable.",
            "narrateur|Le seau jaune brille un peu.",
            "papa|On fait un autre gâteau ?",
            "enfant-m|Oui.",
            "narrateur|Nino remplit encore le seau.",
            "narrateur|Il tasse avec la pelle rouge.",
            "narrateur|Il retourne encore le seau.",
            "papa|Je te vois encore.",
            "enfant-m|Je reste ici.",
            "papa|Oui.",
            "papa|Dans l'espace montré.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Nino joue au parc.",
            "narrateur|Où joue-t-il ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Nino est dans l'espace montré.",
            "narrateur|Papa le voit.",
            "narrateur|L'adulte voit.",
            "narrateur|Le gâteau de sable est là.",
            "papa|Tu as joué dans l'espace montré ?",
            "enfant-m|Oui.",
            "papa|Bravo.",
            "papa|Je te voyais.",
            "narrateur|Le seau jaune a du sable.",
            "narrateur|La pelle est à côté.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Nino range le seau.",
            "narrateur|Il range la pelle.",
            "narrateur|Papa lui tend la main.",
            "papa|Tu as fini le gâteau ?",
            "enfant-m|Oui, papa.",
            "papa|Bravo.",
            "papa|On rentre.",
            "narrateur|Nino prend la main de papa.",
            "narrateur|Le seau jaune tape doucement.",
            "narrateur|L'herbe sent encore la pluie.",
            "papa|Tu es resté où je vois.",
            "enfant-m|Dans l'espace montré.",
            "papa|Oui.",
            "papa|L'adulte voit.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le seau jaune rentre à la maison.",
            "enfant-m|J'ai fait un gâteau.",
            "papa|Oui.",
            "papa|Dans l'espace montré.",
            "papa|Bravo, Nino.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "enfants_parc",
        "CHK_T0000_P0000_Q0001": "enfants_parc",
    },
)

# ---------------------------------------------------------------------------
# ATOM-SEC.PAR.001-02 N2 Mila, papa, cerceau orange, coccinelle
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SEC.PAR.001-02",
    "Une petite bête rouge marche sur le cerceau de Mila. Papa montre l'espace près des cerceaux. Mila reste où l'adulte voit.",
    "Le cerceau orange de Mila",
    "Mila, papa",
    "jardin public, cerceaux",
    {
        "CHK_T0000_P0000": [
            "narrateur|Une petite bête rouge marche sur un cerceau.",
            "narrateur|Le cerceau est orange et un peu froid.",
            "narrateur|Le tilleul fait une ombre ronde.",
            "narrateur|Une feuille tombe, toute lente.",
            "narrateur|Le banc sent le bois chaud.",
            "narrateur|Une fourmi croise la feuille.",
            "papa|Tu as vu la petite bête, Mila ?",
            "enfant-f|Elle est rouge, papa.",
            "papa|Oui.",
            "papa|Elle a des points noirs.",
            "narrateur|Mila se penche tout doux.",
            "narrateur|La petite bête lève une patte.",
            "enfant-f|Elle marche.",
            "papa|Tout doucement, oui.",
            "narrateur|La petite bête va sous une feuille.",
            "narrateur|En ce moment, papa montre un espace.",
            "narrateur|C'est près des cerceaux colorés.",
            "papa|Tu joues ici.",
            "papa|Dans l'espace montré.",
            "papa|Ici, l'adulte voit.",
            "narrateur|Mila prend un cerceau orange.",
            "narrateur|Le plastique est un peu froid.",
            "narrateur|Elle le fait rouler.",
            "narrateur|Le cerceau fait un petit rum.",
            "narrateur|Papa s'assoit sur le banc.",
            "narrateur|Parce que Mila reste dans l'espace montré, papa la voit.",
            "narrateur|L'adulte voit.",
            "enfant-f|Il roule, papa.",
            "papa|Oui.",
            "papa|Tu restes près des cerceaux.",
            "papa|Je te vois.",
            "narrateur|Mila fait un grand cercle.",
            "narrateur|L'ombre du tilleul tourne avec elle.",
            "narrateur|Elle revient près du banc.",
            "papa|Tu es dans l'espace montré ?",
            "enfant-f|Oui.",
            "papa|Bravo.",
            "narrateur|Le vent est doux.",
            "narrateur|L'ombre du tilleul bouge un peu.",
            "papa|On recommence un tour ?",
            "enfant-f|Oui, papa.",
            "narrateur|Mila fait rouler encore le cerceau.",
            "narrateur|Le rum revient, tout rond.",
            "narrateur|Elle reste dans l'espace montré.",
            "papa|L'adulte voit.",
            "papa|Tu as fait du bon travail.",
            "enfant-f|La petite bête est partie.",
            "papa|Oui.",
            "papa|Toi, tu es restée ici.",
            "narrateur|Mila pose le cerceau.",
            "narrateur|Mila tape dans ses mains.",
            "narrateur|Papa tape aussi.",
            "narrateur|Le cerceau orange brille au soleil.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Mila joue au jardin.",
            "narrateur|Où reste-t-elle ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Mila est restée dans l'espace montré.",
            "narrateur|Parce qu'elle y est restée, papa la voyait.",
            "narrateur|L'adulte voit.",
            "papa|Tu es restée dans l'espace montré ?",
            "enfant-f|Oui, papa.",
            "papa|Bravo.",
            "papa|Je te voyais.",
            "narrateur|Le cerceau orange est posé.",
            "narrateur|L'ombre du tilleul est ronde.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Mila range le cerceau.",
            "narrateur|Le plastique n'est plus froid.",
            "narrateur|Papa lui tend la gourde.",
            "narrateur|L'eau est fraîche.",
            "papa|Tu as soif ?",
            "enfant-f|Un peu.",
            "papa|Bois.",
            "papa|Tu as joué dans l'espace montré.",
            "enfant-f|Oui.",
            "papa|L'adulte voit.",
            "papa|Bravo, Mila.",
            "narrateur|Mila boit.",
            "narrateur|Une goutte tombe sur sa main.",
            "narrateur|Le tilleul sent fort, tout près.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le cerceau orange rentre dans le sac.",
            "enfant-f|J'ai fait rouler le cerceau.",
            "papa|Oui.",
            "papa|Dans l'espace montré.",
            "papa|Bravo, Mila.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "enfants_parc",
        "CHK_T0000_P0000_C0001": "enfants_parc",
    },
)

# ---------------------------------------------------------------------------
# ATOM-SEC.PAR.001-03 N3 Aniss, maman, plots bleus puis bac à sable
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SEC.PAR.001-03",
    "Aniss pose des plots bleus dans la cour. Plus tard, au parc, il reste près du bac. Même règle : l'espace montré, l'adulte voit.",
    "Les plots bleus d'Aniss",
    "Aniss, maman",
    "cour d'école puis parc",
    {
        "CHK_T0000_P0000": [
            "narrateur|De la craie blanche poudre les plots bleus.",
            "narrateur|La poussière colle aux doigts.",
            "narrateur|Le muret de la cour est chaud.",
            "narrateur|Une cloche a sonné, tout à l'heure.",
            "narrateur|Le sac de maman sent la pomme.",
            "narrateur|Une pomme rouge brille dans le filet.",
            "maman|Tu as vu la poussière, Aniss ?",
            "enfant-m|Elle est blanche, maman.",
            "maman|Oui.",
            "maman|C'est de la craie.",
            "narrateur|Aniss souffle un peu.",
            "narrateur|Un nuage blanc s'envole.",
            "enfant-m|Ça pique le nez.",
            "maman|Un peu, oui.",
            "narrateur|En ce moment, maman montre un espace.",
            "narrateur|C'est près des plots bleus.",
            "maman|Tu joues ici, dans l'espace montré.",
            "maman|Ici, l'adulte voit.",
            "narrateur|Aniss prend un plot.",
            "narrateur|Le plastique est un peu rêche.",
            "narrateur|Il le pose.",
            "narrateur|Il fait un petit chemin bleu.",
            "narrateur|Maman s'assoit sur le muret.",
            "narrateur|Parce qu'Aniss reste dans l'espace montré, maman le voit.",
            "narrateur|L'adulte voit.",
            "enfant-m|Un chemin, maman.",
            "maman|Je le vois.",
            "maman|Tu restes dans l'espace montré ?",
            "enfant-m|Oui.",
            "maman|Bravo.",
            "narrateur|Aniss pose encore deux plots.",
            "narrateur|Le chemin bleu s'allonge un peu.",
            "narrateur|Aniss revient près d'elle.",
            "maman|Je te vois.",
            "maman|L'adulte voit.",
            "narrateur|Plus tard, ils vont au parc.",
            "narrateur|Le chemin sent l'herbe coupée.",
            "narrateur|Une abeille passe près d'une fleur.",
            "narrateur|Elle fait un petit zzz.",
            "maman|Tu as entendu ?",
            "enfant-m|Zzz.",
            "narrateur|Maman montre un autre espace.",
            "narrateur|C'est près du bac à sable.",
            "maman|Tu joues ici.",
            "maman|L'espace montré.",
            "maman|Ici, l'adulte voit.",
            "narrateur|Aniss se souvient.",
            "narrateur|Il reste près du bac.",
            "narrateur|Il verse le sable.",
            "narrateur|Le sable est frais.",
            "enfant-m|Il est frais, comme la craie.",
            "maman|Oui.",
            "maman|Tu as repris la règle.",
            "maman|Même leçon, autre lieu.",
            "narrateur|Aniss tasse un gâteau.",
            "narrateur|Il revient vers le banc.",
            "maman|Tu as fait du bon travail.",
            "enfant-m|Dans l'espace montré.",
            "maman|Oui.",
            "maman|L'adulte voit.",
            "narrateur|Aniss sourit.",
            "narrateur|Un peu de craie reste sur son pouce.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Aniss joue.",
            "narrateur|Où reste-t-il ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Aniss est resté dans l'espace montré.",
            "narrateur|À la cour, puis au parc.",
            "narrateur|L'adulte voyait.",
            "maman|Tu es resté dans l'espace montré ?",
            "enfant-m|Oui.",
            "enfant-m|Les plots, puis le bac.",
            "maman|Bravo.",
            "maman|Je te voyais.",
            "narrateur|Le plot bleu a un peu de craie.",
            "narrateur|Le seau a un peu de sable.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Aniss range le seau.",
            "narrateur|Maman lui tend la gourde.",
            "narrateur|La pomme du sac sent encore.",
            "maman|Tu as soif ?",
            "enfant-m|Oui, maman.",
            "maman|Bois.",
            "maman|Tu as repris la règle au parc.",
            "enfant-m|L'espace montré.",
            "maman|Oui.",
            "maman|L'adulte voit.",
            "maman|Bravo, Aniss.",
            "narrateur|Aniss boit.",
            "narrateur|Une goutte coule sur son menton.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Les plots bleus restent dans la cour.",
            "enfant-m|J'ai fait un chemin.",
            "maman|Oui.",
            "maman|Puis un gâteau de sable.",
            "maman|Dans l'espace montré.",
            "maman|Bravo, Aniss.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "enfants_parc",
        "CHK_T0000_P0000_C0001": "enfants_parc",
    },
)

# ---------------------------------------------------------------------------
# ATOM-SEC.PAR.001-04 N2 Nina, maman, menthe, square, bac à sable
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SEC.PAR.001-04",
    "Une feuille de menthe tremble. Nina fait un gâteau de sable au square, dans l'espace montré par maman.",
    "La menthe de Nina",
    "Nina, maman",
    "square, bac à sable",
    {
        "CHK_T0000_P0000": [
            "narrateur|Une feuille de menthe tremble dans le vent.",
            "narrateur|Elle est dans une jardinière verte.",
            "narrateur|Le banc du square est chaud.",
            "narrateur|Le vent sent l'herbe et la menthe.",
            "narrateur|Un oiseau picore une miette.",
            "narrateur|La miette est petite et sèche.",
            "maman|Tu as senti la menthe, Nina ?",
            "enfant-f|Ça pique le nez.",
            "maman|Oui.",
            "maman|C'est la menthe.",
            "narrateur|Nina touche une feuille.",
            "narrateur|Elle est fraîche et un peu collante.",
            "enfant-f|Elle est froide.",
            "maman|Un peu, oui.",
            "narrateur|En ce moment, maman montre un espace.",
            "narrateur|C'est le bac à sable.",
            "maman|Tu joues ici.",
            "maman|C'est l'espace montré.",
            "maman|Ici, l'adulte voit.",
            "narrateur|Nina va au bac.",
            "narrateur|Elle reste dans l'espace montré.",
            "narrateur|Maman s'assoit.",
            "narrateur|Le bois du banc est chaud.",
            "narrateur|Maman voit Nina.",
            "narrateur|L'adulte voit.",
            "narrateur|Parce que Nina reste là, maman la voit.",
            "narrateur|Nina verse le sable.",
            "narrateur|Le sable est frais.",
            "enfant-f|Il est frais, maman.",
            "maman|Oui.",
            "maman|Comme la menthe.",
            "narrateur|Nina fait un gâteau.",
            "narrateur|Ses mains sont occupées.",
            "maman|Je te vois.",
            "maman|Tu restes dans l'espace montré ?",
            "enfant-f|Oui.",
            "maman|Bravo.",
            "narrateur|Les pieds restent dans le bac.",
            "narrateur|Nina tasse encore le sable.",
            "narrateur|Elle retourne le seau.",
            "narrateur|Le gâteau de sable tient un peu.",
            "enfant-f|Un gâteau à la menthe.",
            "maman|Presque.",
            "maman|Tu as fait du bon travail.",
            "narrateur|Nina pose une feuille à côté.",
            "narrateur|La feuille sent fort.",
            "maman|On en met une sur le gâteau ?",
            "enfant-f|Oui.",
            "narrateur|Nina pose la feuille tout doux.",
            "narrateur|Le gâteau a une petite feuille verte.",
            "maman|Beau gâteau.",
            "narrateur|Nina sourit.",
            "narrateur|Elle reste dans l'espace montré.",
            "narrateur|L'oiseau picore encore.",
            "narrateur|La jardinière verte brille un peu.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Nina joue au square.",
            "narrateur|Où joue-t-elle ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Nina est restée dans l'espace montré.",
            "narrateur|Maman, l'adulte, la voyait.",
            "narrateur|L'adulte voit.",
            "maman|Tu as joué dans l'espace montré ?",
            "enfant-f|Oui, maman.",
            "maman|Bravo.",
            "maman|Je te voyais.",
            "narrateur|Le gâteau de sable est encore là.",
            "narrateur|La menthe tremble encore.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Nina secoue ses mains.",
            "narrateur|Le sable tombe tout doux.",
            "narrateur|Il fait un petit bruit fin.",
            "narrateur|Maman range le seau.",
            "narrateur|Le seau a du sable au fond.",
            "maman|Tu as fini le gâteau ?",
            "enfant-f|Oui.",
            "maman|On rentre.",
            "maman|Tu es restée dans l'espace montré.",
            "enfant-f|L'adulte voit.",
            "maman|Oui.",
            "maman|Bravo, Nina.",
            "narrateur|Nina sent encore la menthe sur le doigt.",
            "narrateur|Elle sent aussi un peu le sable.",
            "narrateur|Le banc reste chaud, vide.",
            "narrateur|L'oiseau s'envole, tout léger.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|La feuille de menthe tremble encore.",
            "enfant-f|J'ai fait un gâteau.",
            "maman|Oui.",
            "maman|Dans l'espace montré.",
            "maman|Bravo, Nina.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "enfants_parc",
    },
)

# ---------------------------------------------------------------------------
# ATOM-SEC.PAR.001-05 N2 Amir, papa, maman, marelle, craie dans la poche
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SEC.PAR.001-05",
    "Une craie ronde roule dans la poche d'Amir. Dans la cour, il joue à la marelle où papa voit. Maman le trouve tout de suite.",
    "La marelle d'Amir",
    "Amir, papa, maman",
    "cour d'école, marelle",
    {
        "CHK_T0000_P0000": [
            "narrateur|Une craie ronde roule dans une poche.",
            "narrateur|Elle fait un petit bruit sec.",
            "narrateur|Le portail de l'école est encore ouvert.",
            "narrateur|Le muret est tiède.",
            "narrateur|Une feuille est collée au grillage.",
            "narrateur|Le grillage sent le fer chaud.",
            "papa|Tu as entendu la craie, Amir ?",
            "enfant-m|Elle roule, papa.",
            "papa|Oui.",
            "papa|On la sort.",
            "narrateur|Amir sort la craie.",
            "narrateur|Elle est blanche et un peu cassée.",
            "enfant-m|Elle a un bout cassé.",
            "papa|On peut encore dessiner.",
            "narrateur|En ce moment, papa montre un espace.",
            "narrateur|C'est le carré de marelle.",
            "papa|Tu joues ici.",
            "papa|C'est l'espace montré.",
            "papa|Ici, l'adulte voit.",
            "narrateur|Amir prend la craie.",
            "narrateur|Il trace un trait dans une case.",
            "narrateur|Il saute dans les cases.",
            "narrateur|Parce que papa le voit, Amir reste.",
            "narrateur|Il reste dans l'espace montré.",
            "narrateur|Papa s'assoit sur le muret.",
            "narrateur|L'adulte voit.",
            "narrateur|Amir pose un caillou.",
            "narrateur|Le caillou est lisse.",
            "enfant-m|Il est lisse, papa.",
            "papa|Oui.",
            "papa|Je te vois.",
            "papa|Tu restes dans l'espace montré ?",
            "enfant-m|Oui.",
            "papa|Bravo.",
            "narrateur|Amir saute encore.",
            "narrateur|Les pieds restent dans le carré.",
            "narrateur|La craie laisse un trait blanc.",
            "narrateur|Maman arrive près du portail.",
            "narrateur|Elle voit Amir tout de suite.",
            "maman|Je te vois, Amir.",
            "maman|Tu es dans l'espace montré.",
            "enfant-m|Oui, maman.",
            "maman|Bravo.",
            "papa|Parce qu'il est dans l'espace montré, tu le trouves.",
            "maman|Oui.",
            "maman|L'adulte voit.",
            "maman|Tu as fait du bon travail.",
            "narrateur|Amir pose la craie.",
            "narrateur|Un peu de blanc reste sur ses doigts.",
            "narrateur|Le caillou lisse attend dans la case un.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Amir joue dans la cour.",
            "narrateur|Où joue-t-il ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Amir est dans l'espace montré.",
            "narrateur|Papa le voit.",
            "narrateur|Maman le voit aussi.",
            "narrateur|L'adulte voit.",
            "narrateur|La marelle est là.",
            "papa|Tu as joué dans l'espace montré ?",
            "enfant-m|Oui.",
            "maman|Bravo.",
            "maman|On t'a vu tout de suite.",
            "narrateur|La craie est un peu usée.",
            "narrateur|Le caillou lisse est encore là.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Amir range la craie.",
            "narrateur|Elle laisse un peu de blanc.",
            "narrateur|Papa lui tend la main.",
            "maman|Tu as fini la marelle ?",
            "enfant-m|Oui, maman.",
            "papa|On rentre.",
            "papa|Tu es resté où on voit.",
            "enfant-m|Dans l'espace montré.",
            "maman|L'adulte voit.",
            "papa|Bravo, Amir.",
            "narrateur|Amir prend la main de papa.",
            "narrateur|Maman ferme le sac.",
            "narrateur|Le sac sent encore le goûter.",
            "narrateur|La feuille au grillage bouge encore.",
            "narrateur|Le portail fait un petit clic.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|La craie rentre dans la poche.",
            "enfant-m|J'ai joué à la marelle.",
            "papa|Oui.",
            "maman|Dans l'espace montré.",
            "papa|Bravo, Amir.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "enfants_parc",
    },
)

# ---------------------------------------------------------------------------
# ATOM-SEC.PAR.001-06 N3 Sarah, maman, bateau de papier, parc puis square
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SEC.PAR.001-06",
    "Un bateau de papier flotte. Sarah joue au bac, puis à la marelle du square. Deux lieux, même règle : l'espace montré, l'adulte voit.",
    "Le bateau de Sarah",
    "Sarah, maman",
    "parc puis square",
    {
        "CHK_T0000_P0000": [
            "narrateur|Un petit bateau de papier flotte dans une flaque.",
            "narrateur|Le papier est blanc et un peu mouillé.",
            "narrateur|La flaque tremble quand le vent passe.",
            "narrateur|Le parc sent l'herbe mouillée.",
            "narrateur|Un banc luit, encore humide.",
            "narrateur|Une plume grise est collée au bois.",
            "maman|Tu as vu le bateau, Sarah ?",
            "enfant-f|Il flotte, maman.",
            "maman|Oui.",
            "maman|Tout doucement.",
            "narrateur|Sarah s'accroupit.",
            "narrateur|Le papier est froid sous le doigt.",
            "enfant-f|Il est mou.",
            "maman|Le papier a bu l'eau.",
            "narrateur|En ce moment, maman montre un espace.",
            "narrateur|C'est le bac à sable.",
            "maman|Tu joues ici.",
            "maman|C'est l'espace montré.",
            "maman|Ici, l'adulte voit.",
            "narrateur|Sarah verse le sable.",
            "narrateur|Il est frais.",
            "narrateur|Elle reste dans l'espace montré.",
            "narrateur|Maman s'assoit sur le banc.",
            "narrateur|L'adulte voit.",
            "narrateur|Sarah fait un gâteau.",
            "enfant-f|Un gâteau, maman.",
            "maman|Je te vois.",
            "maman|Tu restes dans l'espace montré ?",
            "enfant-f|Oui.",
            "maman|Bravo.",
            "narrateur|Sarah tasse encore le sable.",
            "narrateur|Le gâteau tient un peu.",
            "narrateur|Plus tard, elles vont au square.",
            "narrateur|Le bateau reste dans la flaque.",
            "narrateur|Le chemin sent l'herbe coupée.",
            "narrateur|Maman montre un autre espace.",
            "narrateur|C'est le tapis de marelle.",
            "maman|Tu joues ici.",
            "maman|C'est l'espace montré.",
            "maman|Ici, l'adulte voit.",
            "narrateur|Sarah se souvient.",
            "narrateur|Elle saute dans les cases.",
            "narrateur|Parce que maman la voit, Sarah reste.",
            "narrateur|Même leçon, autre lieu.",
            "narrateur|L'adulte voit.",
            "narrateur|Les pieds restent dans l'espace montré.",
            "enfant-f|Les cases, maman.",
            "maman|Je te vois.",
            "maman|Tu as repris la règle.",
            "maman|Tu as fait du bon travail.",
            "narrateur|Sarah pose un pied sur le un.",
            "narrateur|Le tapis est un peu rêche.",
            "narrateur|Le deux est un peu délavé.",
        ],
        "CHK_T0000_P0000_Q0001": [
            "narrateur|Sarah joue dehors.",
            "narrateur|Où joue-t-elle ?",
        ],
        "CHK_T0000_P0000_C0001": [
            "narrateur|Sarah est dans l'espace montré.",
            "narrateur|Maman la voit.",
            "narrateur|Au parc, puis au square.",
            "narrateur|L'adulte voit.",
            "maman|Tu as joué dans l'espace montré ?",
            "enfant-f|Oui.",
            "enfant-f|Le bac, puis la marelle.",
            "maman|Bravo.",
            "maman|Je te voyais.",
            "narrateur|Le gâteau de sable s'est un peu affaissé.",
            "narrateur|Le tapis de marelle est calme.",
        ],
        "CHK_T0000_P0000_END": [
            "narrateur|Sarah range le seau.",
            "narrateur|Un peu de sable reste sous l'ongle.",
            "narrateur|Maman lui tend la main.",
            "narrateur|Elles repassent près de la flaque.",
            "enfant-f|Le bateau est encore là.",
            "maman|Oui.",
            "maman|Il attend.",
            "maman|Toi, tu es restée dans l'espace montré.",
            "enfant-f|L'adulte voit.",
            "maman|Oui.",
            "maman|Bravo, Sarah.",
            "narrateur|Sarah prend la main de maman.",
            "narrateur|Le papier du bateau est tout mou.",
            "narrateur|La plume grise n'est plus sur le banc.",
            "narrateur|Le square sent encore l'herbe.",
        ],
        "CHK_T0000_P0000_END_F0001": [
            "narrateur|Le petit bateau tourne dans la flaque.",
            "enfant-f|J'ai joué au bac.",
            "maman|Puis à la marelle.",
            "maman|Dans l'espace montré.",
            "maman|Bravo, Sarah.",
            "narrateur|L'histoire est finie.",
        ],
    },
    {
        "CHK_T0000_P0000": "enfants_parc",
        "CHK_T0000_P0000_C0001": "enfants_parc",
    },
)
