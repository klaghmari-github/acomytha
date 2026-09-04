#!/usr/bin/env python3
"""Réécrit ATOM-DIF.ENE.001-01..08 — récit, pas un slogan d'énergie."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

IDS = [
    "CHK_T0000_P0000",
    "CHK_T0000_P0000_Q0001",
    "CHK_T0000_P0000_C0001",
    "CHK_T0000_P0000_END",
    "CHK_T0000_P0000_END_F0001",
]
KINDS = [
    "passage_debut",
    "passage_question",
    "passage",
    "passage",
    "passage_fin",
]


def text_of(script: str) -> str:
    phrases = []
    for line in script.strip().splitlines():
        line = line.strip()
        if not line or "|" not in line:
            raise SystemExit(f"ligne script: {line!r}")
        phrases.append(line.split("|", 1)[1])
    return " ".join(phrases)


def chunk(cid, kind, script, *, sons="", scale=1.22, rate="medium", pause=400, **extra):
    script = "\n".join(ln.strip() for ln in script.strip().splitlines() if ln.strip())
    d = {
        "chunk_id": cid,
        "kind": kind,
        "text": text_of(script),
        "script": script,
        "sons": sons,
        "length_scale_piper": scale,
        "rate_label": rate,
        "pause_after_ms": pause,
    }
    d.update(extra)
    return d


def pack(story_id, title, fil_rouge, lesson_id, age_band, kind, characters, setting, chunks, **meta):
    out = {
        "story_id": story_id,
        "title": title,
        "fil_rouge": fil_rouge,
        "lesson_id": lesson_id,
        "age_band": age_band,
        "kind": kind,
        "characters": characters,
        "setting": setting,
        "chunks": chunks,
    }
    out.update(meta)
    return out


# --- 01 N2 Sarah + Raphaël : cerceau sur les flaques ---
S01 = pack(
    "ATOM-DIF.ENE.001-01",
    "Le cerceau sur les flaques",
    "Sarah veut faire danser le cerceau jaune sur les flaques. Raphaël arrive avec beaucoup d'énergie et le cerceau tremble. Ils jouent, ils attendent, Sarah demande à maman. Le cerceau danse.",
    "DIF.ENE.001",
    "N2",
    "atomic",
    "Sarah, Raphaël, papa, maman",
    "cour d'école après la pluie",
    [
        chunk(
            IDS[0],
            KINDS[0],
            """
narrateur|Un oiseau secoue une branche près du portail.
narrateur|Trois gouttes tombent dans une flaque ronde.
narrateur|La flaque fait des ronds, tout doucement.
narrateur|L'air sent les feuilles mouillées.
narrateur|Le banc de bois est encore sombre.
narrateur|Papa noue la capuche de Sarah.
papa|Elle te tient chaud ?
enfant-f|Oui, papa.
enfant-f|Elle est un peu rêche.
narrateur|Maman frotte une feuille entre ses doigts.
maman|Ça sent le jardin, tu vois ?
enfant-f|Le jardin, oui.
narrateur|Un cerceau jaune s'appuie contre le mur.
narrateur|Il a une petite goutte sur le bord.
narrateur|Le soleil perce un tout petit nuage.
narrateur|La flaque devient un miroir.
narrateur|En ce moment, Sarah touche le cerceau.
narrateur|Le plastique est froid, un peu mouillé.
enfant-f|Je veux le faire danser.
enfant-f|Sur les flaques.
papa|On y va, tout doucement.
narrateur|Les bottes de Sarah font un bruit mou.
narrateur|Raphaël arrive dans la cour.
narrateur|Ses chaussures tapent le sol.
narrateur|Tap. Tap. Tap.
narrateur|Il saute sur place.
narrateur|Il a de l'énergie, beaucoup.
enfant-f|Il bouge tout le temps.
maman|C'est son énergie.
maman|Ce n'est pas une faute.
narrateur|Raphaël prend le cerceau jaune.
narrateur|Il le fait tourner très vite.
narrateur|Le cerceau tremble près de la flaque.
enfant-f|Moi aussi, le cerceau.
papa|À tour de rôle, alors.
narrateur|Sarah tend la main.
narrateur|Le cerceau tourne encore.
narrateur|Raphaël ne s'arrête pas.
narrateur|Sarah regarde maman.
            """,
            sons="enfants_parc",
            scale=1.22,
            rate="medium",
            pause=400,
        ),
        chunk(
            IDS[1],
            KINDS[1],
            """
narrateur|Raphaël a de l'énergie.
narrateur|Que peut-on faire ?
            """,
            sons="",
            scale=1.3,
            rate="slow",
            pause=250,
            expected_answer="jouer",
            accepted_examples="jouer | attendre | un adulte | demander",
            retry_prompt="On peut jouer, attendre, ou demander à un adulte. Que fait Sarah ?",
        ),
        chunk(
            IDS[2],
            KINDS[2],
            """
narrateur|Sarah va vers maman.
enfant-f|Maman, on fait quoi ?
maman|On joue avec le cerceau.
maman|On attend son tour.
maman|Tu peux venir me demander.
papa|Viens, Raphaël.
papa|On marche jusqu'au bac.
narrateur|Ils marchent.
narrateur|Les bottes font encore un bruit mou.
narrateur|Sarah pose les mains sur le bac.
narrateur|L'eau est froide.
narrateur|Raphaël pose les mains aussi.
narrateur|Il souffle.
narrateur|Il se calme un peu.
maman|L'énergie est encore là.
maman|Ce n'est pas une faute.
enfant-f|On attend un peu.
narrateur|Raphaël pose le cerceau.
narrateur|Il attend son tour.
papa|C'est à Sarah.
narrateur|Sarah fait tourner le cerceau.
narrateur|Le cerceau danse près des flaques.
narrateur|Il fait un rond jaune sur l'eau.
enfant-f|Maintenant c'est toi.
narrateur|Raphaël reprend le cerceau.
narrateur|Il tourne plus doucement.
narrateur|Ils jouent.
narrateur|Puis ils font une file pour les balles.
narrateur|Raphaël a encore envie d'aller vite.
enfant-f|On peut attendre.
narrateur|Raphaël souffle.
narrateur|Il reste dans la file.
maman|Chacun son tour.
narrateur|Maman donne une balle rouge.
narrateur|Raphaël la lance vers le panier.
narrateur|Sarah lance aussi.
narrateur|Le panier fait un petit toc.
            """,
            sons="enfants_parc",
            scale=1.18,
            rate="medium",
            pause=450,
        ),
        chunk(
            IDS[3],
            KINDS[3],
            """
narrateur|Le soleil touche le cerceau jaune.
maman|On range, et on rentre ?
enfant-f|Oui, maman.
narrateur|Sarah porte le cerceau.
narrateur|Raphaël porte la balle rouge.
papa|Vous vous dites au revoir ?
enfant-m|Au revoir, Sarah.
enfant-f|Au revoir, Raphaël.
narrateur|La cour redevient calme.
narrateur|La flaque ne tremble plus.
maman|Le cerceau a dansé, aujourd'hui.
papa|On le pose contre le mur ?
enfant-f|Contre le mur.
narrateur|Sarah pose le cerceau.
narrateur|Il s'appuie, tout droit.
            """,
            sons="",
            scale=1.18,
            rate="medium",
            pause=450,
        ),
        chunk(
            IDS[4],
            KINDS[4],
            """
narrateur|Le cerceau jaune sèche un peu.
narrateur|Il a encore une goutte sur le bord.
papa|Il attend demain.
enfant-f|Sur les flaques.
narrateur|L'histoire est finie.
            """,
            sons="",
            scale=1.26,
            rate="slow",
            pause=600,
        ),
    ],
)

# --- 02 N1 Victorina + Nino : ballon sous le drap ---
S02 = pack(
    "ATOM-DIF.ENE.001-02",
    "Le ballon sous le drap",
    "Victorina veut faire rebondir le ballon sur la pierre chaude. Nino a de l'énergie. Le ballon se cache sous le drap. Ils jouent, ils attendent, Victorina demande à maman. Le ballon rebondit.",
    "DIF.ENE.001",
    "N1",
    "atomic",
    "Victorina, Nino, papa, maman",
    "jardin le jour du linge",
    [
        chunk(
            IDS[0],
            KINDS[0],
            """
narrateur|Une pince à linge tombe dans l'herbe.
narrateur|Toc.
narrateur|Elle est rouge.
narrateur|Elle est chaude.
narrateur|Le drap blanc cache le soleil.
narrateur|Puis il le rend.
narrateur|Ça sent le savon.
narrateur|Papa arrose un pot.
papa|Tu entends l'eau, Victorina ?
enfant-f|Oui, papa.
narrateur|Maman chante tout bas.
maman|Le linge est presque sec.
narrateur|Une pierre attend dans l'herbe.
narrateur|Elle est ronde.
narrateur|Elle est chaude.
narrateur|En ce moment, Victorina s'assoit dessus.
narrateur|La pierre est douce.
narrateur|Elle tiédit le pantalon.
enfant-f|Je veux le ballon.
enfant-f|Sur la pierre.
maman|Il est près du bac.
narrateur|Une abeille visite une chaussette bleue.
narrateur|Elle part.
narrateur|Victorina prend le ballon.
narrateur|Il est un peu poudreux.
narrateur|Nino arrive dans le jardin.
narrateur|Il court un peu.
narrateur|Il saute.
narrateur|Il a de l'énergie.
narrateur|Beaucoup d'énergie.
enfant-f|Il saute, maman.
maman|C'est son énergie.
maman|Ce n'est pas une faute.
narrateur|Nino court vers le ballon.
narrateur|Le ballon roule.
narrateur|Il se cache sous le drap blanc.
enfant-f|Le ballon.
enfant-f|Il est dessous.
papa|On le cherche ensemble ?
narrateur|Le drap bouge un peu.
narrateur|Nino saute encore.
narrateur|Victorina regarde maman.
            """,
            sons="enfants_parc",
            scale=1.28,
            rate="slow",
            pause=400,
        ),
        chunk(
            IDS[1],
            KINDS[1],
            """
narrateur|Nino a de l'énergie.
narrateur|Que fait-on ?
            """,
            sons="",
            scale=1.4,
            rate="slow",
            pause=250,
            expected_answer="jouer",
            accepted_examples="jouer | attendre | un adulte | maman",
            retry_prompt="On peut jouer. On peut attendre. Que fait Victorina ?",
        ),
        chunk(
            IDS[2],
            KINDS[2],
            """
narrateur|Victorina va vers maman.
enfant-f|Maman, le ballon ?
maman|On joue avec le ballon.
maman|Ou on attend un peu.
maman|Tu viens me voir, si tu veux.
papa|On soulève le drap.
narrateur|Le drap sent le savon.
narrateur|Le ballon est là.
narrateur|Il est un peu tiède.
narrateur|Nino tend les mains.
narrateur|Il a encore de l'énergie.
maman|Ce n'est pas une faute.
enfant-f|On attend.
narrateur|Nino souffle.
narrateur|Il attend.
papa|C'est à Victorina.
narrateur|Victorina pose le ballon sur la pierre.
narrateur|Poumf.
narrateur|Le ballon rebondit.
narrateur|Nino le rattrape.
narrateur|Il le rend.
narrateur|Ils jouent.
narrateur|Ils se passent le ballon.
narrateur|Tout près.
narrateur|L'herbe chatouille les genoux.
papa|Le ballon est bien gonflé ?
enfant-f|Oui, papa.
maman|On reste encore un peu ?
enfant-f|Encore un peu.
narrateur|Nino saute encore un peu.
enfant-f|On peut attendre.
narrateur|Nino pose le ballon.
narrateur|Il attend son tour.
maman|Chacun son tour.
            """,
            sons="enfants_parc",
            scale=1.28,
            rate="slow",
            pause=450,
        ),
        chunk(
            IDS[3],
            KINDS[3],
            """
maman|On rentre ?
enfant-f|Oui, maman.
narrateur|Victorina porte le ballon.
narrateur|Nino ramasse la pince rouge.
papa|Vous vous dites merci ?
enfant-f|Merci, Nino.
enfant-m|Merci.
narrateur|Le linge fait encore clap clap.
maman|Le ballon a rebondi.
papa|Sur la pierre chaude.
narrateur|Victorina pose le ballon dans le panier.
narrateur|Le panier sent le bois.
            """,
            sons="",
            scale=1.28,
            rate="slow",
            pause=450,
        ),
        chunk(
            IDS[4],
            KINDS[4],
            """
narrateur|La pierre est encore chaude.
narrateur|Le ballon dort dans le panier.
papa|Il rebondira demain.
enfant-f|Sur la pierre.
narrateur|L'histoire est finie.
            """,
            sons="",
            scale=1.4,
            rate="slow",
            pause=600,
        ),
    ],
)

# --- 03 N3 Sarah + Mila : château de coussins, soupe ---
S03 = pack(
    "ATOM-DIF.ENE.001-03",
    "Le château avant la soupe",
    "Sarah veut un château de coussins avant la soupe. Mila arrive avec beaucoup d'énergie. Le mur tombe. Elles jouent, elles attendent, Sarah demande à papa. Le château tient. La soupe est prête.",
    "DIF.ENE.001",
    "N3",
    "atomic",
    "Sarah, Mila, papa, maman",
    "salon puis cuisine, soupe de carotte",
    [
        chunk(
            IDS[0],
            KINDS[0],
            """
narrateur|Un rond de vapeur s'ouvre sur la vitre.
narrateur|Dedans, le jardin est flou.
narrateur|Papa essuie un petit trou avec le doigt.
papa|Tu as senti la soupe, Sarah ?
enfant-f|Oui.
enfant-f|Ça sent la carotte.
narrateur|Maman plie une serviette chaude.
maman|On mange bientôt.
narrateur|Au salon, un coussin rayé a un carré de soleil.
narrateur|Le tissu est tiède.
narrateur|Une cuillère en bois attend près des bols.
narrateur|En ce moment, Sarah pose la joue sur le coussin.
enfant-f|Je veux un château.
enfant-f|Un château de coussins.
papa|On peut en faire un petit mur.
narrateur|Sarah pose un coussin.
narrateur|Puis un autre.
narrateur|Le mur est bas, un peu de travers.
narrateur|Mila arrive dans le salon.
narrateur|Elle court un peu.
narrateur|Elle saute.
narrateur|Elle a de l'énergie.
narrateur|Beaucoup d'énergie.
enfant-f|Elle saute partout, papa.
papa|C'est son énergie.
papa|Ce n'est pas une faute.
narrateur|Mila pose un coussin trop vite.
narrateur|Le mur bascule.
narrateur|Un coussin glisse sur le tapis.
enfant-f|Oh.
enfant-f|Le château.
maman|Il peut se reconstruire.
narrateur|Sarah tient un coussin contre elle.
narrateur|Mila saute encore.
narrateur|Sarah regarde papa.
            """,
            sons="",
            scale=1.18,
            rate="medium",
            pause=400,
        ),
        chunk(
            IDS[1],
            KINDS[1],
            """
narrateur|Mila a de l'énergie.
narrateur|Que fait-on ?
            """,
            sons="",
            scale=1.24,
            rate="medium",
            pause=250,
            expected_answer="jouer",
            accepted_examples="jouer | attendre | un adulte | papa",
            retry_prompt="On peut jouer. On peut attendre. Que fait Sarah ?",
        ),
        chunk(
            IDS[2],
            KINDS[2],
            """
narrateur|Sarah va vers papa.
enfant-f|Papa, on fait quoi ?
papa|On reconstruit le château.
papa|On joue, ou on attend un peu.
papa|Tu m'as demandé, je suis là.
maman|On se passe la cuillère en bois.
narrateur|Ils vont dans la cuisine.
narrateur|Les casseroles font tin tin.
narrateur|Mila tape un rythme sur ses genoux.
narrateur|Elle a encore de l'énergie.
papa|Ce n'est pas une faute.
enfant-f|On peut attendre.
narrateur|Mila souffle.
narrateur|Elle tend les mains.
narrateur|Sarah envoie la cuillère.
narrateur|Mila la renvoie.
narrateur|La cuillère est lisse et chaude.
narrateur|Elles jouent.
narrateur|Puis elles reviennent au salon.
narrateur|Sarah pose un coussin.
narrateur|Elle attend.
narrateur|Mila pose le suivant.
narrateur|Le mur tient.
maman|Un coussin, puis l'autre.
enfant-f|Le château.
papa|Il a une porte, là.
narrateur|Sarah glisse la main dans le trou.
narrateur|Le tissu est doux.
narrateur|La soupe chante tout bas.
narrateur|Un filet de vapeur monte.
maman|Tu as les mains sur la table, Sarah ?
enfant-f|Oui, maman.
narrateur|Mila pose la cuillère.
narrateur|Elle attend.
            """,
            sons="",
            scale=1.12,
            rate="medium",
            pause=450,
        ),
        chunk(
            IDS[3],
            KINDS[3],
            """
papa|On range ?
enfant-f|Oui, papa.
narrateur|Sarah porte un coussin.
narrateur|Mila porte la cuillère.
maman|Vous posez ça près de la table ?
enfant-f|Oui.
narrateur|Les bols attendent.
papa|La soupe est prête.
narrateur|Le château reste un peu, de travers.
maman|Il a tenu.
enfant-f|Avant la soupe.
narrateur|Sarah souffle sur sa cuillère.
narrateur|La carotte sent bon.
            """,
            sons="",
            scale=1.12,
            rate="medium",
            pause=450,
        ),
        chunk(
            IDS[4],
            KINDS[4],
            """
narrateur|Les bols sont chauds.
narrateur|Le château de coussins fait de l'ombre.
papa|Il attend après la soupe.
enfant-f|On y retourne.
narrateur|L'histoire est finie.
            """,
            sons="",
            scale=1.2,
            rate="medium",
            pause=600,
        ),
    ],
)

# --- 04 N2 Nino + Victorino : soleil jaune ---
S04 = pack(
    "ATOM-DIF.ENE.001-04",
    "Le soleil du grand pinceau",
    "Nino veut peindre un soleil jaune avec le grand pinceau bleu. Victorino arrive avec beaucoup d'énergie. Une goutte tombe. Ils jouent, ils attendent, Nino demande à maman. Le soleil est sur la feuille.",
    "DIF.ENE.001",
    "N2",
    "atomic",
    "Nino, Victorino, papa, maman",
    "atelier peinture à la maison",
    [
        chunk(
            IDS[0],
            KINDS[0],
            """
narrateur|Le tube jaune a un bouchon collant.
narrateur|Papa le tourne.
narrateur|Une petite virgule de peinture sort.
narrateur|Elle sent le papier neuf.
narrateur|Un chiffon bleu sèche près de la fenêtre.
narrateur|Le papier craque tout doucement.
papa|Tu sens la peinture, Nino ?
enfant-m|Oui.
enfant-m|Ça sent le papier.
narrateur|Maman pose de grandes feuilles.
maman|On a de la place, tous les deux.
narrateur|En ce moment, Nino regarde la feuille vide.
narrateur|Elle est un peu rugueuse.
enfant-m|Je veux le grand pinceau.
enfant-m|Pour un soleil.
maman|Il est dans le pot bleu.
narrateur|Le pot fait un petit clac.
narrateur|L'eau du pot est trouble.
narrateur|Victorino arrive en sautant.
narrateur|Il a beaucoup d'énergie.
narrateur|Il tourne.
narrateur|Il s'arrête.
narrateur|Il recommence.
enfant-m|Il saute, papa.
papa|C'est son énergie.
papa|Ce n'est pas une faute.
narrateur|Victorino prend le grand pinceau bleu.
narrateur|Il veut peindre tout de suite.
narrateur|Une goutte jaune tombe sur la table.
narrateur|Elle fait un petit point brillant.
enfant-m|À tour de rôle.
maman|Oui.
maman|On attend son tour.
narrateur|Le pinceau tremble un peu.
narrateur|Victorino ne le pose pas encore.
narrateur|Nino regarde maman.
            """,
            sons="",
            scale=1.22,
            rate="medium",
            pause=400,
        ),
        chunk(
            IDS[1],
            KINDS[1],
            """
narrateur|Victorino a de l'énergie.
narrateur|Que peut-on faire ?
            """,
            sons="",
            scale=1.3,
            rate="slow",
            pause=250,
            expected_answer="jouer",
            accepted_examples="jouer | attendre | un adulte | demander",
            retry_prompt="On peut jouer. On peut attendre. Que fait Nino ?",
        ),
        chunk(
            IDS[2],
            KINDS[2],
            """
narrateur|Nino va vers maman.
enfant-m|Maman, on fait quoi ?
maman|On peint, tous les deux.
maman|On attend le pinceau.
maman|Tu m'as appelée, Nino.
maman|Victorino, viens marcher jusqu'à l'évier.
narrateur|Victorino marche.
narrateur|Il pose les mains sous l'eau.
narrateur|L'eau est froide.
narrateur|Il souffle.
narrateur|Il se calme un peu.
papa|L'énergie est encore là.
papa|Ce n'est pas une faute.
enfant-m|On attend.
narrateur|Victorino pose le pinceau dans le pot.
narrateur|Il attend son tour.
maman|C'est à Nino.
narrateur|Nino prend le grand pinceau bleu.
narrateur|Il peint un rond.
narrateur|Le rond est jaune comme un soleil.
enfant-m|Maintenant c'est toi.
narrateur|Victorino peint une ligne.
narrateur|La ligne part du rond.
narrateur|C'est un rayon.
narrateur|Après, ils font une file pour les pots.
narrateur|Victorino a envie d'aller vite.
enfant-m|On peut attendre.
narrateur|Victorino souffle.
narrateur|Il reste dans la file.
papa|Chacun a de la peinture.
narrateur|Ils jouent.
narrateur|Puis ils rincent les pinceaux ensemble.
narrateur|L'eau devient un peu jaune.
            """,
            sons="",
            scale=1.18,
            rate="medium",
            pause=450,
        ),
        chunk(
            IDS[3],
            KINDS[3],
            """
narrateur|Nino et Victorino rangent les pinceaux.
maman|Vous posez les pots près du chiffon ?
enfant-m|Oui, maman.
papa|Le rond jaune est beau.
narrateur|Le chiffon bleu sèche encore.
maman|On a peint ensemble.
enfant-m|Un soleil.
narrateur|Nino souffle sur la feuille.
narrateur|La peinture brille un peu.
papa|On la laisse sécher ?
enfant-m|Oui, papa.
            """,
            sons="",
            scale=1.18,
            rate="medium",
            pause=450,
        ),
        chunk(
            IDS[4],
            KINDS[4],
            """
narrateur|Le soleil jaune reste sur la table.
narrateur|Le grand pinceau dort dans le pot bleu.
maman|Il a des rayons, maintenant.
enfant-m|Toute la feuille.
narrateur|L'histoire est finie.
            """,
            sons="",
            scale=1.26,
            rate="slow",
            pause=600,
        ),
    ],
)

# --- 05 N1 Mila + Aniss : seau et sauge ---
S05 = pack(
    "ATOM-DIF.ENE.001-05",
    "Le seau de la sauge",
    "Mila veut arroser la sauge avec le seau rouge. Aniss a de l'énergie. L'eau touche les chaussures. Ils jouent, ils attendent, Mila demande à papa. La sauge boit.",
    "DIF.ENE.001",
    "N1",
    "atomic",
    "Mila, Aniss, papa, maman",
    "jardin, terre mouillée",
    [
        chunk(
            IDS[0],
            KINDS[0],
            """
narrateur|Un ver de terre rose traverse le chemin.
narrateur|Il brille.
narrateur|La terre est molle.
narrateur|Elle est sombre.
narrateur|Une caisse sent le bois mouillé.
narrateur|Un seau rouge attend.
narrateur|Papa a de la terre sur une chaussure.
papa|Tu vois le ver, Mila ?
enfant-f|Oui.
enfant-f|Il brille.
narrateur|Maman tord un linge.
maman|Le bac est plein d'eau.
narrateur|En ce moment, Mila touche une feuille.
narrateur|La feuille de sauge est un peu rêche.
narrateur|Elle sent fort, un peu comme le savon.
enfant-f|Je veux le seau.
enfant-f|Pour la sauge.
maman|Il est près du bac.
narrateur|Mila marche vers le bac.
narrateur|L'eau tremble.
narrateur|Elle est claire.
narrateur|Aniss arrive en sautant.
narrateur|Il a beaucoup d'énergie.
narrateur|Il tourne.
narrateur|Il s'arrête.
narrateur|Il recommence.
enfant-f|Il saute, maman.
maman|C'est son énergie.
maman|Ce n'est pas une faute.
narrateur|Aniss prend le seau.
narrateur|L'eau bouge.
narrateur|Un peu d'eau touche les chaussures.
enfant-f|Le seau.
enfant-f|À tour de rôle.
papa|Oui.
papa|On attend.
narrateur|Aniss tient encore le seau.
narrateur|Il saute un peu.
narrateur|Mila regarde papa.
            """,
            sons="enfants_parc",
            scale=1.28,
            rate="slow",
            pause=400,
        ),
        chunk(
            IDS[1],
            KINDS[1],
            """
narrateur|Aniss a de l'énergie.
narrateur|Que peut-on faire ?
            """,
            sons="",
            scale=1.4,
            rate="slow",
            pause=250,
            expected_answer="jouer",
            accepted_examples="jouer | attendre | un adulte | demander",
            retry_prompt="On peut jouer, attendre, ou demander à un adulte. Que fait Mila ?",
        ),
        chunk(
            IDS[2],
            KINDS[2],
            """
narrateur|Mila va vers papa.
enfant-f|Papa, le seau ?
papa|On verse pour la sauge.
papa|On attend son tour.
papa|Tu peux me demander.
papa|On se passe le seau.
narrateur|Aniss tend les mains.
narrateur|Il a encore de l'énergie.
maman|Ce n'est pas une faute.
enfant-f|On peut attendre.
narrateur|Aniss souffle.
narrateur|Il attend.
narrateur|Mila verse tout doucement.
narrateur|La sauge boit.
narrateur|Ploc.
narrateur|Aniss verse après.
narrateur|Ils jouent.
narrateur|Ils se passent le seau.
narrateur|Une autre goutte tombe.
narrateur|La terre sent fort.
papa|Tu veux encore verser, Mila ?
enfant-f|Oui.
narrateur|Mila verse.
narrateur|Aniss attend.
maman|Chacun son tour.
narrateur|Un oiseau chante tout près.
papa|Tu l'as entendu ?
enfant-f|Oui, papa.
narrateur|Le ver de terre n'est plus là.
narrateur|La terre a un petit trou brillant.
enfant-f|Il est rentré.
papa|Il a de l'eau, maintenant.
            """,
            sons="enfants_parc",
            scale=1.28,
            rate="slow",
            pause=450,
        ),
        chunk(
            IDS[3],
            KINDS[3],
            """
maman|On range le seau ?
enfant-f|Oui.
narrateur|Maman tend la main.
narrateur|Mila et Aniss rangent le seau.
papa|Vous avez les mains froides ?
enfant-f|Un peu.
papa|On essuie.
narrateur|La sauge brille encore.
maman|Elle a bu.
enfant-f|Avec le seau rouge.
narrateur|Le seau sèche à l'envers.
narrateur|Une goutte tombe du bord.
narrateur|Ploc.
maman|Une dernière, pour la terre.
            """,
            sons="",
            scale=1.28,
            rate="slow",
            pause=450,
        ),
        chunk(
            IDS[4],
            KINDS[4],
            """
narrateur|La sauge est brillante.
narrateur|Le seau rouge sèche.
papa|La terre est contente.
enfant-f|Moi aussi.
narrateur|L'histoire est finie.
            """,
            sons="",
            scale=1.4,
            rate="slow",
            pause=600,
        ),
    ],
)

# --- 06 N3 Amir + Chouchou : bateau-feuille ---
S06 = pack(
    "ATOM-DIF.ENE.001-06",
    "Le bateau-feuille",
    "Amir veut faire flotter une feuille jaune dans le bac. Chouchou arrive avec beaucoup d'énergie. L'eau éclabousse. Ils jouent, ils attendent, Amir demande à papa. La feuille tourne, tout lentement.",
    "DIF.ENE.001",
    "N3",
    "atomic",
    "Amir, Chouchou, papa, maman",
    "jardin de l'école, bac sous l'arbre",
    [
        chunk(
            IDS[0],
            KINDS[0],
            """
narrateur|Une craie blanche a roulé sous le banc.
narrateur|Elle a un ventre cassé.
narrateur|Un morceau reste, tout sec.
narrateur|L'ombre du grand arbre fait des taches par terre.
narrateur|Une cloche lointaine fait ding, tout loin.
narrateur|Papa noue un lacet.
papa|Ton lacet est prêt, Amir ?
enfant-m|Oui, papa.
narrateur|Maman glisse une gourde dans le sac.
maman|L'eau est fraîche.
narrateur|En ce moment, Amir ramasse une feuille jaune.
narrateur|Elle est sèche.
narrateur|Elle a des nervures.
narrateur|Elle craque un tout petit peu.
enfant-m|Je veux un bateau.
enfant-m|Dans le bac.
papa|Le bac est sous l'arbre.
narrateur|Amir souffle sur la feuille.
narrateur|Elle tremble dans sa main.
narrateur|Les chaussures tapent le sol de la cour.
narrateur|Chouchou arrive en sautant.
narrateur|Elle a beaucoup d'énergie.
narrateur|Elle tourne.
narrateur|Elle s'arrête.
narrateur|Elle recommence.
enfant-m|Elle saute tout le temps.
maman|C'est son énergie.
maman|Ce n'est pas une faute.
narrateur|Ils font une file pour le bac.
narrateur|Chouchou a envie d'aller vite.
narrateur|L'eau éclabousse un peu.
enfant-m|Ma feuille.
narrateur|La feuille jaune tremble au bord.
narrateur|Amir regarde papa.
            """,
            sons="enfants_parc",
            scale=1.18,
            rate="medium",
            pause=400,
        ),
        chunk(
            IDS[1],
            KINDS[1],
            """
narrateur|Chouchou a de l'énergie.
narrateur|Que peut-on faire ?
            """,
            sons="",
            scale=1.24,
            rate="medium",
            pause=250,
            expected_answer="jouer",
            accepted_examples="jouer | attendre | un adulte | demander",
            retry_prompt="On peut jouer, attendre, ou demander à un adulte. Que fait Amir ?",
        ),
        chunk(
            IDS[2],
            KINDS[2],
            """
narrateur|Amir va vers papa.
enfant-m|Papa, on fait quoi ?
papa|On fait flotter le bateau.
papa|On attend dans la file.
papa|Tu es venu me demander.
papa|On marche jusqu'au bac.
narrateur|Papa marche avec Chouchou.
narrateur|L'eau est froide.
narrateur|Chouchou pose les mains un moment.
narrateur|Elle souffle.
maman|L'énergie est encore là.
maman|Ce n'est pas une faute.
enfant-m|On peut attendre.
narrateur|Chouchou reste dans la file.
narrateur|Amir pose la feuille sur l'eau.
narrateur|Elle tourne, tout lentement.
papa|On la laisse flotter ?
enfant-m|Oui.
narrateur|Chouchou regarde la feuille.
narrateur|Elle attend.
narrateur|Puis elle pousse une toute petite vague.
narrateur|La feuille avance.
narrateur|Ils jouent.
narrateur|Amir attend son tour pour verser.
narrateur|Il verse un filet.
narrateur|La feuille fait un tour.
maman|Chacun son tour.
enfant-f|Encore un tour.
papa|Encore un, tout doux.
narrateur|Une petite araignée d'eau part.
narrateur|La feuille la suit, tout lentement.
enfant-m|Elle avance.
maman|Votre bateau a un sillage.
            """,
            sons="enfants_parc",
            scale=1.12,
            rate="medium",
            pause=450,
        ),
        chunk(
            IDS[3],
            KINDS[3],
            """
maman|On reprend le sac ?
enfant-m|Oui, maman.
narrateur|Maman prend la main d'Amir.
narrateur|Chouchou ramasse le morceau de craie.
papa|Vous vous dites au revoir ?
enfant-f|Au revoir.
enfant-m|Au revoir, Chouchou.
narrateur|La feuille reste un moment sur l'eau.
papa|Ton bateau a voyagé.
enfant-m|Tout autour du bac.
maman|On la laisse là ?
enfant-m|Elle sèche sur le bord.
            """,
            sons="",
            scale=1.12,
            rate="medium",
            pause=450,
        ),
        chunk(
            IDS[4],
            KINDS[4],
            """
narrateur|La feuille jaune sèche sur le bord.
narrateur|L'ombre de l'arbre a bougé.
papa|Le bateau a fini son tour.
enfant-m|Il a flotté.
narrateur|L'histoire est finie.
            """,
            sons="",
            scale=1.2,
            rate="medium",
            pause=600,
        ),
    ],
)

# --- 07 N3 Nina + Nino : tunnel bleu ---
S07 = pack(
    "ATOM-DIF.ENE.001-07",
    "La grotte bleue",
    "Nina veut passer dans le tunnel de tissu. Nino arrive avec beaucoup d'énergie et se met devant. Ils jouent, ils attendent, Nina demande à maman. La grotte frôle les cheveux.",
    "DIF.ENE.001",
    "N3",
    "atomic",
    "Nina, Nino, papa, maman",
    "salle de jeux, tapis et tunnel",
    [
        chunk(
            IDS[0],
            KINDS[0],
            """
narrateur|Le tunnel bleu sent le linge propre.
narrateur|Une couture gratte un peu.
narrateur|Nina glisse la main dedans.
narrateur|C'est une grotte.
narrateur|La petite lampe pose un rond jaune sur le tapis.
narrateur|Des chaussettes douces attendent près des coussins.
narrateur|Papa empile deux coussins.
papa|La grotte est prête, Nina ?
enfant-f|Oui.
enfant-f|Elle est bleue.
narrateur|Maman secoue une petite clochette.
maman|Ting.
maman|Doucement.
narrateur|En ce moment, Nina rampe vers la grotte.
narrateur|Le tapis gratte un peu les genoux.
enfant-f|Je veux passer.
enfant-f|Dans le tunnel.
maman|On fait une file, alors.
narrateur|Nina pose une chaussette près de l'entrée.
narrateur|Elle est chaude, encore.
narrateur|Les chaussures tapent un peu le sol.
narrateur|Nino arrive en sautant.
narrateur|Il a beaucoup d'énergie.
narrateur|Il tourne.
narrateur|Il s'arrête.
narrateur|Il recommence.
enfant-f|Il saute, papa.
papa|C'est son énergie.
papa|Ce n'est pas une faute.
narrateur|Nino se met devant le tunnel.
narrateur|Il a envie d'aller vite.
narrateur|Nina est encore à genoux.
enfant-f|Moi aussi, le tunnel.
narrateur|Nino rebondit sur place.
narrateur|Nina regarde maman.
            """,
            sons="",
            scale=1.18,
            rate="medium",
            pause=400,
        ),
        chunk(
            IDS[1],
            KINDS[1],
            """
narrateur|Nino a de l'énergie.
narrateur|Que peut-on faire ?
            """,
            sons="",
            scale=1.24,
            rate="medium",
            pause=250,
            expected_answer="jouer",
            accepted_examples="jouer | attendre | un adulte | demander",
            retry_prompt="On peut jouer, attendre, ou demander à un adulte. Que fait Nina ?",
        ),
        chunk(
            IDS[2],
            KINDS[2],
            """
narrateur|Nina va vers maman.
enfant-f|Maman, on fait quoi ?
maman|On passe dans la grotte.
maman|On attend dans la file.
maman|Tu m'as demandé, je t'écoute.
maman|On marche jusqu'aux coussins.
narrateur|Maman marche avec eux.
narrateur|Nino s'assoit un moment.
narrateur|Nina s'assoit aussi.
narrateur|Les coussins sont mous et chauds.
papa|L'énergie est encore là.
papa|Ce n'est pas une faute.
enfant-f|On peut attendre.
narrateur|Nino souffle.
narrateur|Il reste dans la file.
maman|C'est à Nina.
narrateur|Nina passe dans la grotte.
narrateur|Le tissu frôle ses cheveux.
enfant-f|Il est doux.
narrateur|Puis Nino passe.
narrateur|Ils jouent.
narrateur|La clochette fait ting, tout bas.
narrateur|Le tapis est doux sous les mains.
papa|On reprend le tunnel après ?
enfant-f|Après, oui.
narrateur|Nino pose un coussin.
enfant-m|J'attends.
narrateur|Il attend.
narrateur|Nina touche encore le tissu bleu.
enfant-f|On y retourne ?
maman|Un dernier passage.
narrateur|Nina rampe.
narrateur|Nino attend, les mains sur le coussin.
narrateur|Puis Nino rampe aussi.
papa|La clochette, tout doux.
narrateur|Ting.
            """,
            sons="",
            scale=1.12,
            rate="medium",
            pause=450,
        ),
        chunk(
            IDS[3],
            KINDS[3],
            """
maman|On range un coussin ?
enfant-f|Oui.
narrateur|Maman prend la main de Nina.
narrateur|Nino range un coussin.
papa|La grotte bleue attend demain.
narrateur|La lampe fait encore son rond jaune.
enfant-f|J'ai passé.
maman|Le tissu a frôlé tes cheveux.
narrateur|Nina plie l'entrée du tunnel.
narrateur|La grotte devient un rectangle bleu.
            """,
            sons="",
            scale=1.12,
            rate="medium",
            pause=450,
        ),
        chunk(
            IDS[4],
            KINDS[4],
            """
narrateur|Le tunnel bleu est plié.
narrateur|Le rond jaune de la lampe reste.
papa|La grotte a été traversée.
enfant-f|Deux fois.
narrateur|L'histoire est finie.
            """,
            sons="",
            scale=1.2,
            rate="medium",
            pause=600,
        ),
    ],
)

# --- 08 N3 Aniss + Sarah : ruban rouge ---
S08 = pack(
    "ATOM-DIF.ENE.001-08",
    "Le ruban dans le rayon",
    "Aniss veut dessiner un grand rond lent avec le ruban rouge dans le rayon de soleil. Sarah arrive avec beaucoup d'énergie. Le ruban s'enroule à la chaise. Ils jouent, ils attendent, Aniss demande à maman. Le rond est lent, et il est là.",
    "DIF.ENE.001",
    "N3",
    "atomic",
    "Aniss, Sarah, papa, maman",
    "salon, radio et rayon de poussière",
    [
        chunk(
            IDS[0],
            KINDS[0],
            """
narrateur|La radio craque, puis trouve une chanson.
narrateur|Le bouton est lisse sous le doigt de papa.
papa|Tu entends la chanson, Aniss ?
enfant-m|Oui.
enfant-m|Elle est douce.
narrateur|Un ruban rouge glisse de la chaise.
narrateur|Il tombe comme une petite rivière.
narrateur|Le tapis est épais et beige.
narrateur|Maman ouvre un peu la fenêtre.
maman|L'air sent le linge sec.
narrateur|Un rayon traverse le salon.
narrateur|Il est plein de poussière brillante.
narrateur|En ce moment, Aniss prend le ruban.
narrateur|Il est long.
narrateur|Il sent un peu le bois de la chaise.
enfant-m|Je veux danser.
enfant-m|Un grand rond, lent.
maman|On danse avec le ruban, alors.
narrateur|Aniss lève le bras.
narrateur|Le ruban dessine un tout petit arc.
narrateur|Sarah arrive.
narrateur|Elle saute sur place.
narrateur|Elle a beaucoup d'énergie.
narrateur|Les pieds tapent le tapis.
enfant-m|Elle saute, papa.
papa|C'est son énergie.
papa|Ce n'est pas une faute.
narrateur|Aniss tend le ruban.
narrateur|Ils dansent.
narrateur|Sarah tourne vite.
narrateur|Le ruban s'enroule autour de la chaise.
enfant-m|Oh.
enfant-m|Le rond.
narrateur|Sarah rebondit encore.
narrateur|Aniss regarde maman.
            """,
            sons="",
            scale=1.18,
            rate="medium",
            pause=400,
        ),
        chunk(
            IDS[1],
            KINDS[1],
            """
narrateur|Sarah a de l'énergie.
narrateur|Que peut-on faire ?
            """,
            sons="",
            scale=1.24,
            rate="medium",
            pause=250,
            expected_answer="jouer",
            accepted_examples="jouer | attendre | un adulte | demander",
            retry_prompt="On peut jouer, attendre, ou demander à un adulte. Que fait Aniss ?",
        ),
        chunk(
            IDS[2],
            KINDS[2],
            """
narrateur|Aniss va vers maman.
enfant-m|Maman, on fait quoi ?
maman|On danse avec le ruban.
maman|On attend le grand tour.
maman|Tu es venu me voir.
maman|On prend les coussins.
narrateur|Ils s'assoient un moment.
narrateur|Le tapis étouffe les pas.
papa|L'énergie est encore là.
papa|Ce n'est pas une faute.
enfant-m|On peut attendre.
narrateur|Sarah souffle.
narrateur|Elle attend son tour pour le grand ruban.
maman|C'est à Aniss.
narrateur|Aniss défait le ruban de la chaise.
narrateur|Il est doux entre les doigts.
narrateur|Puis ils reprennent le ruban.
narrateur|La chanson est plus douce.
papa|Le ruban fait un grand rond ?
enfant-m|Un grand rond.
narrateur|Aniss fait un rond lent.
narrateur|Le ruban passe dans le rayon.
narrateur|Il devient tout lumineux.
narrateur|Sarah tend le ruban.
enfant-f|J'attends.
narrateur|Elle attend.
narrateur|Puis elle fait un rond, plus lent.
narrateur|Ils jouent.
narrateur|Le rayon traverse le ruban.
enfant-m|Il est tout rouge.
maman|Et tout lumineux.
papa|Encore un rond, plus calme ?
enfant-m|Plus calme.
            """,
            sons="",
            scale=1.12,
            rate="medium",
            pause=450,
        ),
        chunk(
            IDS[3],
            KINDS[3],
            """
maman|On baisse la chanson ?
enfant-m|Oui, maman.
narrateur|Maman baisse la chanson.
narrateur|Aniss range un ruban.
papa|Le ruban rouge va sur la chaise ?
enfant-m|Oui.
narrateur|Le rayon devient tout calme.
maman|Le rond était lent.
enfant-m|Et lumineux.
papa|On l'a vu, tous les deux.
narrateur|Sarah pose le bout du ruban.
narrateur|Il retombe comme une rivière.
            """,
            sons="",
            scale=1.12,
            rate="medium",
            pause=450,
        ),
        chunk(
            IDS[4],
            KINDS[4],
            """
narrateur|Le ruban rouge dort sur la chaise.
narrateur|La radio fait un tout petit souffle.
papa|Le rond est resté dans le rayon.
enfant-m|Un grand rond lent.
narrateur|L'histoire est finie.
            """,
            sons="",
            scale=1.2,
            rate="medium",
            pause=600,
        ),
    ],
)

STORIES = [S01, S02, S03, S04, S05, S06, S07, S08]


def check(story: dict) -> None:
    age = story["age_band"]
    limit = 8 if age == "N1" else 16
    names_ok = {
        "amir", "aniss", "sarah", "chouchou", "mila", "nino", "nina",
        "raphaël", "raphael", "victorino", "victorina", "papa", "maman",
    }
    forbidden_roles = {"copain", "copine"}
    for c in story["chunks"]:
        assert c["text"] == text_of(c["script"])
        for line in c["script"].splitlines():
            role, phrase = line.split("|", 1)
            if role in forbidden_roles:
                raise SystemExit(f"{story['story_id']} rôle interdit {role}")
            n = len(phrase.split())
            if n > limit + 2:
                print(f"LONG {story['story_id']} {c['chunk_id']} ({n} mots, {age}): {phrase}")
        blob = (c["text"] + " " + c["script"]).lower()
        for bad in ("hyperactif", "tdah", "autiste", "méchant", "nul", "bizarre"):
            if bad in blob:
                raise SystemExit(f"{story['story_id']} mot interdit {bad}")
    # troupe
    import re
    text = " ".join(c["text"] for c in story["chunks"])
    # crude proper names
    for m in re.findall(r"\b([A-ZÉÈÊÀÂÎÔÛ][a-zàâäéèêëïîôùûüç]+)\b", text):
        if m.lower() not in names_ok and m not in {"Oui", "Non", "Bravo", "Merci", "Oh", "Toc", "Tap", "Ting", "Ploc", "Poumf", "Ding", "Fffff"}:
            if m not in {"Chacun", "Encore", "Après", "Contre", "Avant", "Toute", "Deux", "Puis", "Maintenant", "L'histoire"}:
                pass  # only warn later
    words = sum(len(c["text"].split()) for c in story["chunks"])
    print(f"{story['story_id']} mots={words} title={story['title']!r}")


def main() -> None:
    for story in STORIES:
        check(story)
        folder = ROOT / story["story_id"]
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / "merged.json"
        path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("wrote", path)


if __name__ == "__main__":
    main()
