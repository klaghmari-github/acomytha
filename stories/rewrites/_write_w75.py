#!/usr/bin/env python3
"""F-NAR-008 — ATOM-SOC.TRA.002-05..07 + ATOM-TMP.JOU.001-01..05."""
from __future__ import annotations

from _lib import relecture, write_story


def L(block: str) -> list[str]:
    return [ln.strip() for ln in block.strip().splitlines() if ln.strip()]


# ---------------------------------------------------------------------------
# ATOM-SOC.TRA.002-05  N3  Amir, papa — train, champs puis rivière
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SOC.TRA.002-05",
    "Amir veut voir la rivière depuis le train. Un sac glisse. Il reste assis. Les champs passent, puis l'eau. Ils descendent ensemble.",
    "Le train d'Amir et la rivière",
    "Amir, papa",
    "train, champs puis rivière",
    {
        "CHK_T0000_P0000": L("""
narrateur|La gare sent le pain chaud du kiosque.
narrateur|Un pigeon picore une mie près du banc.
narrateur|Le quai tremble un peu, déjà.
narrateur|Le train jaune attend, portes ouvertes.
narrateur|Ça sent le fer chaud et le pain.
papa|Tu as vu le kiosque, Amir ?
enfant-m|Il sent le pain.
papa|Oui.
papa|On en prendra un, à l'arrivée.
narrateur|Amir tient un petit sac en papier.
narrateur|Dedans, une pomme et un gâteau.
enfant-m|Je veux voir la rivière.
papa|Elle arrive après les champs.
papa|On la verra par la fenêtre.
narrateur|En ce moment, Amir monte dans le wagon.
narrateur|Le plancher vibre sous ses chaussures.
papa|Voici ta place, près de la vitre.
narrateur|Amir pose ses fesses sur le siège.
narrateur|Son dos trouve le dossier tiède.
narrateur|Ses pieds touchent le plancher qui vibre.
papa|On reste assis, avec l'adulte.
papa|Tu restes assis, d'accord ?
enfant-m|D'accord.
narrateur|Papa s'assoit tout contre lui.
narrateur|La porte se referme, sèche.
narrateur|Le wagon part sans un cri.
narrateur|Dehors, les toits du village reculent.
enfant-m|Ça va vite.
papa|Oui.
papa|Tes fesses restent sur le siège.
narrateur|Les champs arrivent, tout jaunes.
narrateur|Les épis tapent le vent, dehors.
narrateur|Une vache lève la tête, lente.
enfant-m|Une vache !
papa|Tu la vois, assis.
narrateur|Amir colle le nez à la vitre froide.
narrateur|Il reste assis.
narrateur|Le sac glisse sous le siège d'à côté.
enfant-m|Mon sac !
papa|Je le prends.
narrateur|Papa ramène le sac sans se lever fort.
narrateur|Il le pose sur les genoux d'Amir.
enfant-m|Merci.
papa|Tu es resté assis.
papa|Merci, Amir.
narrateur|Les champs s'en vont, tout doux.
narrateur|Une bande d'eau brille entre les saules.
enfant-m|La rivière !
papa|La voilà.
papa|Tu la regardes depuis ta place ?
enfant-m|Oui.
narrateur|L'eau court, plate et claire.
narrateur|Un héron reste au bord, gris.
narrateur|Le soleil tape la vitre, puis glisse.
narrateur|Amir tient la pomme sans la croquer.
narrateur|Il reste assis, le sac sur les genoux.
narrateur|Un pont de fer passe au dessus de l'eau.
narrateur|Le wagon fait un bruit creux.
enfant-m|On est dessus.
papa|Oui.
papa|Toi, tu restes assis.
"""),
        "CHK_T0000_P0000_Q0001": L("""
narrateur|Amir est dans le train.
narrateur|Que fait-il ?
"""),
        "CHK_T0000_P0000_C0001": L("""
narrateur|Amir est resté assis près de la vitre.
narrateur|Papa, l'adulte, était juste à côté.
papa|Tes fesses étaient sur le siège.
papa|Bravo.
enfant-m|J'ai vu la rivière.
papa|Oui, depuis ta place.
narrateur|Le wagon ralentit près d'un second pont.
narrateur|L'eau clignote encore sous le fer.
enfant-m|On s'arrête ?
papa|Bientôt.
papa|On se lève quand je le dis.
narrateur|Amir serre le sac.
narrateur|Ses pieds restent sur le plancher.
narrateur|La pomme roule un peu, puis s'arrête.
papa|Tu la tiens ?
enfant-m|Oui.
"""),
        "CHK_T0000_P0000_END": L("""
narrateur|Le wagon s'arrête.
narrateur|Le quai sent la poussière chaude.
papa|Maintenant on se lève.
papa|Tu me donnes la main ?
enfant-m|Oui, papa.
narrateur|Ils descendent ensemble, pas à pas.
narrateur|Le kiosque de cette gare sent encore le pain.
papa|Le pain promis.
narrateur|Amir prend un petit pain chaud.
narrateur|La mie colle un peu aux doigts.
enfant-m|Il est chaud.
papa|Comme le quai.
narrateur|Derrière les rails, l'eau brille encore.
enfant-m|La rivière est encore là.
papa|Oui.
papa|Tu l'as vue, assis.
narrateur|Un pigeon picore une mie, déjà.
"""),
        "CHK_T0000_P0000_END_F0001": L("""
narrateur|Ils marchent sur le quai, main dans la main.
narrateur|Le petit pain sent le beurre.
enfant-m|On l'a vue.
papa|Oui.
papa|Depuis ta place.
narrateur|Le train jaune repart, tout doux.
narrateur|L'eau reste entre les saules.
"""),
    },
    {"CHK_T0000_P0000": "train,quai"},
    {
        "expected_answer": "assis",
        "accepted_examples": "assis | rester assis | il reste assis | avec papa | avec l'adulte",
        "retry_prompt": "Ses fesses sont sur le siège. Que fait Amir ?",
    },
)
relecture(
    "ATOM-SOC.TRA.002-05",
    "Le train d'Amir et la rivière",
    "Amir veut la rivière par la fenêtre. Champs jaunes, puis l'eau. Un sac glisse. Il reste assis. Pain chaud sur le quai.",
    "- Désir : la rivière, pas la leçon assis.\n"
    "- Imprévu : sac sous le siège. Amir ne se lève pas.\n"
    "- Deux paysages : champs puis rivière. Troupe : Amir, papa.",
)


# ---------------------------------------------------------------------------
# ATOM-SOC.TRA.002-06  N1  Sarah, papa — voiture, doudou, tracteur
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SOC.TRA.002-06",
    "Sarah veut voir le tracteur. Elle reste assise, doudou contre elle. Le tracteur passe à la fenêtre. Ils marchent vers le champ après.",
    "Le tracteur à la fenêtre de Sarah",
    "Sarah, papa",
    "voiture, chemin de ferme",
    {
        "CHK_T0000_P0000": L("""
narrateur|Le gravier craque sous les pneus de la voiture.
narrateur|Ça sent le foin, déjà.
narrateur|Une haie d'orties borde le chemin.
narrateur|Le ciel est tout blanc, chaud.
narrateur|Des mouches tournent près du capot.
papa|Tu as senti le foin, Sarah ?
enfant-f|Ça pique le nez.
papa|Oui.
papa|On va à la ferme.
narrateur|Sarah tient son doudou gris.
narrateur|Le doudou sent le savon.
enfant-f|Je veux le tracteur.
papa|Il est dans le champ.
papa|On le verra par la fenêtre.
narrateur|En ce moment, Sarah est sur le siège.
narrateur|Papa attache la ceinture, clic.
narrateur|Le tissu est chaud sur les jambes.
narrateur|Ses pieds touchent le repose pieds.
papa|On reste assis, avec l'adulte.
papa|Tu restes assise, d'accord ?
enfant-f|D'accord.
narrateur|La voiture avance tout doux.
narrateur|Les orties reculent, vertes.
narrateur|Sarah serre le doudou.
enfant-f|Il est où ?
papa|Regarde par la vitre.
narrateur|Un bruit grave arrive, loin.
narrateur|Un gros tracteur rouge apparaît.
enfant-f|Le tracteur !
narrateur|Sarah se penche vers la vitre.
narrateur|Elle a envie de se lever.
papa|Tes fesses restent sur le siège.
narrateur|Sarah replace ses fesses.
narrateur|Le doudou reste sur ses genoux.
narrateur|Le tracteur passe tout près.
narrateur|Les grandes roues lèvent la poussière.
enfant-f|Il est grand.
papa|Tu le vois, assise.
narrateur|Sarah reste assise.
narrateur|Elle colle le nez à la vitre.
narrateur|Le tracteur s'éloigne dans le champ.
enfant-f|Au revoir.
papa|Il nous attend à la ferme.
narrateur|Le clignotant fait tic, tic.
narrateur|Sarah chante tout bas.
narrateur|Le doudou a une oreille pliée.
papa|Tu lui as plié l'oreille ?
enfant-f|Un peu.
narrateur|Un papillon tape la vitre, puis part.
narrateur|La poussière du champ reste au soleil.
"""),
        "CHK_T0000_P0000_Q0001": L("""
narrateur|Sarah est dans la voiture.
narrateur|Que fait-elle ?
"""),
        "CHK_T0000_P0000_C0001": L("""
narrateur|Sarah est restée assise.
narrateur|Le doudou était sur ses genoux.
papa|Tes fesses étaient sur le siège.
papa|Merci, Sarah.
enfant-f|J'ai vu le tracteur.
papa|Oui, depuis ta place.
narrateur|La voiture ralentit près d'une barrière.
narrateur|Le bois de la barrière est sec.
enfant-f|On arrive ?
papa|Oui.
papa|On sort quand je le dis.
narrateur|Sarah serre le doudou.
narrateur|Elle reste assise.
narrateur|Une poule traverse le chemin, lente.
enfant-f|Une poule.
papa|Tu la regardes, assise.
"""),
        "CHK_T0000_P0000_END": L("""
narrateur|La voiture s'arrête.
narrateur|Le gravier fait un dernier bruit.
papa|Maintenant on sort.
papa|Tu me donnes la main ?
enfant-f|Oui, papa.
narrateur|Papa défait la ceinture.
narrateur|Sarah descend, doudou contre elle.
narrateur|L'air sent le foin, fort.
enfant-f|Le tracteur est là.
papa|On y va ensemble.
narrateur|Ils marchent vers le champ.
narrateur|Les grandes roues sont immobiles.
papa|Tu l'as d'abord vu, assise.
enfant-f|Avec mon doudou.
narrateur|Une mouche tourne près d'une roue.
papa|Tu lui donnes l'autre oreille ?
enfant-f|Voilà.
"""),
        "CHK_T0000_P0000_END_F0001": L("""
narrateur|Sarah pose la main sur une roue.
narrateur|Le caoutchouc est chaud et poussiéreux.
enfant-f|Il est chaud.
papa|Oui.
papa|Comme le chemin.
narrateur|Le doudou a de la poussière à l'oreille.
narrateur|Le foin sent encore, tout près.
"""),
    },
    {"CHK_T0000_P0000": "voiture"},
    {
        "expected_answer": "assis",
        "accepted_examples": "assis | assise | rester assise | elle reste assise | avec papa | avec l'adulte",
        "retry_prompt": "Ses fesses sont sur le siège. Que fait Sarah ?",
    },
)
relecture(
    "ATOM-SOC.TRA.002-06",
    "Le tracteur à la fenêtre de Sarah",
    "Sarah veut le tracteur. Il passe à la vitre. Elle reste assise, doudou sur les genoux. Après, la roue chaude.",
    "- Désir : le tracteur, pas la ceinture.\n"
    "- Imprévu : envie de se lever. Elle replace ses fesses.\n"
    "- Troupe : Sarah, papa. Doudou gris.",
)


# ---------------------------------------------------------------------------
# ATOM-SOC.TRA.002-07  N1  Mila, papa — voiture, gourde qui tombe
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SOC.TRA.002-07",
    "Mila veut le gâteau rond pour mamie. La gourde tombe. Papa la pose. Mila reste assise. Ils ouvrent la boîte au village.",
    "La gourde de Mila",
    "Mila, papa",
    "voiture, route vers le village",
    {
        "CHK_T0000_P0000": L("""
narrateur|La boîte à gâteaux sent encore le beurre.
narrateur|Elle est sur le siège, à côté.
narrateur|Le parking sent l'asphalte chaud.
narrateur|Une cigale chante dans un platane.
papa|Tu as senti les gâteaux, Mila ?
enfant-f|Ça sent le beurre.
papa|Oui.
papa|On les porte à mamie.
enfant-f|Je veux le gâteau rond.
papa|Il est dans la boîte.
papa|On l'ouvrira là bas.
narrateur|En ce moment, Mila est sur le siège.
narrateur|Papa attache la ceinture, clic.
narrateur|La gourde bleue est dans le filet.
narrateur|Ses pieds touchent le tapis.
papa|On reste assis, avec l'adulte.
papa|Tu restes assise, d'accord ?
enfant-f|D'accord.
narrateur|La voiture part tout doux.
narrateur|Les platanes défilent, gris.
narrateur|Mila regarde la boîte.
enfant-f|Il est où, le rond ?
papa|Dans la boîte, tout au fond.
narrateur|Un virage penche un peu.
narrateur|La gourde tombe sur le tapis.
narrateur|Elle fait un bruit mou.
enfant-f|Ma gourde !
narrateur|Mila tend la main.
narrateur|La ceinture la retient, douce.
papa|Je la prends.
papa|Toi, tu restes assise.
narrateur|Papa pose la gourde dans le filet.
narrateur|Mila reste assise.
enfant-f|Elle est revenue.
papa|Oui.
papa|Tes fesses n'ont pas bougé.
papa|Merci, Mila.
narrateur|Les platanes font de l'ombre, puis du soleil.
narrateur|La cigale se perd, loin.
enfant-f|On arrive bientôt ?
papa|Après le pont.
narrateur|Le pont fait un petit bruit de fer.
narrateur|Mila tient la boîte d'un doigt.
papa|Doucement.
narrateur|Elle reste assise.
narrateur|Un camion passe, tout bruyant.
narrateur|La boîte tremble, puis tient.
enfant-f|Les gâteaux aussi.
papa|Oui.
papa|Toi aussi, tu tiens.
"""),
        "CHK_T0000_P0000_Q0001": L("""
narrateur|Mila est dans la voiture.
narrateur|Que fait-elle ?
"""),
        "CHK_T0000_P0000_C0001": L("""
narrateur|Mila est restée assise.
narrateur|La gourde est revenue dans le filet.
papa|Tes fesses étaient sur le siège.
papa|Bravo.
enfant-f|J'ai pas bougé.
papa|Oui.
papa|On sort quand je le dis.
narrateur|Le village arrive, petit.
narrateur|Les volets sont verts.
enfant-f|Mamie ?
papa|Tout près.
narrateur|Mila serre la boîte.
narrateur|Elle reste assise.
narrateur|La gourde ne bouge plus.
papa|Tu la vois, dans le filet ?
enfant-f|Oui.
"""),
        "CHK_T0000_P0000_END": L("""
narrateur|La voiture s'arrête.
narrateur|Le bitume sent encore le chaud.
papa|Maintenant on sort.
papa|Tu me donnes la main ?
enfant-f|Oui, papa.
narrateur|Papa défait la ceinture.
narrateur|Mila descend, la boîte contre elle.
narrateur|Papa prend la gourde bleue.
enfant-f|Elle est rentrée.
papa|Oui.
papa|Toi, tu es restée assise.
narrateur|La porte de mamie claque doucement.
narrateur|Ça sent le café, dedans.
enfant-f|Le gâteau rond.
papa|On l'ouvre ensemble.
"""),
        "CHK_T0000_P0000_END_F0001": L("""
narrateur|Mila pose la boîte sur la table.
narrateur|Le gâteau rond est encore un peu chaud.
enfant-f|Il est là.
papa|Oui.
papa|Tu l'as porté, assise.
narrateur|La gourde bleue attend près du pain.
narrateur|Le beurre sent encore, tout près.
"""),
    },
    {"CHK_T0000_P0000": "voiture"},
    {
        "expected_answer": "assis",
        "accepted_examples": "assis | assise | rester assise | elle reste assise | avec papa | avec l'adulte",
        "retry_prompt": "La gourde est tombée. Mila est restée où ?",
    },
)
relecture(
    "ATOM-SOC.TRA.002-07",
    "La gourde de Mila",
    "Mila veut le gâteau rond. La gourde tombe. Papa la pose. Elle reste assise. Le gâteau chaud sur la table.",
    "- Désir : le gâteau pour mamie.\n"
    "- Imprévu : gourde au tapis. Mila ne se lève pas.\n"
    "- Troupe : Mila, papa.",
)


# ---------------------------------------------------------------------------
# ATOM-TMP.JOU.001-01  N1  Nino, papa — cerisier, pique-nique, fourmi, lune
# ---------------------------------------------------------------------------
write_story(
    "ATOM-TMP.JOU.001-01",
    "Nino veut un pique-nique sous le cerisier. Le soleil chauffe les cerises. Une fourmi arrive sur la nappe. Le soir, la lune se pose dans les branches.",
    "Le pique-nique de Nino",
    "Nino, papa",
    "jardin, cerisier, nappe",
    {
        "CHK_T0000_P0000": L("""
narrateur|Les cerises encore vertes pendent au dessus du bac.
narrateur|L'herbe est encore mouillée, fraîche.
narrateur|Un merle picore sous le cerisier.
narrateur|Le tronc est chaud d'un côté.
papa|Tu as vu le merle, Nino ?
enfant-m|Il saute.
papa|Oui.
papa|Il cherche un ver.
enfant-m|Je veux un pique nique.
papa|Sous le cerisier ?
enfant-m|Oui.
narrateur|En ce moment, Nino tire la nappe.
narrateur|La nappe sent le tiroir.
narrateur|Il la pose dans l'herbe.
narrateur|Le soleil chauffe les cerises, au dessus.
narrateur|Des ronds d'ombre bougent sur le tissu.
papa|Le jour est chaud.
papa|Le soleil est sur l'arbre.
narrateur|Papa pose le pain.
narrateur|Nino pose deux pommes.
enfant-m|Et le fromage.
narrateur|Une fourmi arrive sur la nappe.
narrateur|Elle est toute petite, noire.
enfant-m|Oh.
enfant-m|Une fourmi.
papa|Elle veut la mie ?
enfant-m|C'est notre pain.
narrateur|Nino souffle tout doux.
narrateur|La fourmi ne part pas.
papa|On avance le pain un peu ?
enfant-m|Oui.
narrateur|Nino pousse le pain.
narrateur|La fourmi reste sur le coin.
narrateur|Ils mangent de l'autre côté.
papa|Merci, Nino.
papa|Tu as laissé la fourmi.
narrateur|Le pain a des miettes.
narrateur|Une cerise tombe près du bac.
enfant-m|Elle est dure.
papa|Pas encore mûre.
narrateur|L'ombre du cerisier s'allonge.
narrateur|L'air refroidit les bras.
papa|Le jour s'en va.
enfant-m|Le merle est parti.
narrateur|Le ciel devient bleu foncé.
narrateur|Une lune ronde se pose dans les branches.
enfant-m|Elle est dans l'arbre.
papa|La nuit est là.
papa|La lune est sur le cerisier.
papa|On range la nappe ?
enfant-m|Oui.
"""),
        "CHK_T0000_P0000_Q0001": L("""
narrateur|La lune est dans les branches.
narrateur|Quel moment est-ce ?
"""),
        "CHK_T0000_P0000_C0001": L("""
narrateur|Nino a mangé sous le cerisier.
narrateur|Le soleil était sur les cerises.
narrateur|Maintenant la lune est dans l'arbre.
papa|Le jour, c'était le soleil.
papa|La nuit, c'est la lune.
enfant-m|Elle est ronde.
papa|Oui.
papa|On rentre se coucher ?
enfant-m|Encore un peu.
narrateur|La fourmi a quitté le coin.
narrateur|La nappe a une tache de mie.
papa|Tu plies ton côté ?
enfant-m|Oui, papa.
"""),
        "CHK_T0000_P0000_END": L("""
narrateur|Nino plie la nappe, tout croche.
narrateur|Papa prend le pain.
narrateur|Ils rentrent, l'herbe froide aux chevilles.
papa|Le pyjama, maintenant.
narrateur|Le pyjama est doux, un peu rêche aux poignets.
enfant-m|La lune est encore là ?
papa|À la fenêtre.
narrateur|Nino monte sur le lit.
narrateur|Le cerisier est noir, dehors.
narrateur|La lune tient encore une branche.
papa|La nuit, on fait dodo.
papa|Tu fermes les yeux ?
enfant-m|Presque.
narrateur|Papa baisse la lumière.
narrateur|Nino respire le savon du drap.
"""),
        "CHK_T0000_P0000_END_F0001": L("""
narrateur|Une cerise bouge encore, dehors.
narrateur|La lune la touche, toute pâle.
enfant-m|Notre nappe est pliée.
papa|Oui.
papa|Le pique nique est fini.
narrateur|Nino ferme les yeux.
narrateur|Le merle se tait, déjà.
"""),
    },
    {"CHK_T0000_P0000": "oiseaux,jardin"},
    {
        "expected_answer": "nuit",
        "accepted_examples": "nuit | la nuit | le soir | dodo | c'est la nuit",
        "retry_prompt": "La lune est dans l'arbre. C'est le jour, ou la nuit ?",
    },
)
relecture(
    "ATOM-TMP.JOU.001-01",
    "Le pique-nique de Nino",
    "Nino veut un pique-nique. Soleil sur les cerises. Fourmi sur la nappe. Le soir, lune dans les mêmes branches.",
    "- Désir : le pique-nique, pas la leçon jour/nuit.\n"
    "- Imprévu : fourmi. Nino pousse le pain.\n"
    "- Soleil vécu (chaleur, ombre), lune vécue (branches, fenêtre).",
)


# ---------------------------------------------------------------------------
# ATOM-TMP.JOU.001-02  N3  Nina, maman — mer, coquillage, lune dans la vitre
# ---------------------------------------------------------------------------
write_story(
    "ATOM-TMP.JOU.001-02",
    "Nina veut un coquillage. Le soleil chauffe le sable. Une vague remplit la coquille. Le soir, la lune est dans la vitre, le coquillage sur la table.",
    "Le coquillage de Nina",
    "Nina, maman",
    "mer le jour, voiture puis chambre la nuit",
    {
        "CHK_T0000_P0000": L("""
narrateur|Le sel colle déjà aux genoux de Nina.
narrateur|Le sable est tiède et rêche.
narrateur|Une vague vient, puis recule.
narrateur|Ça sent l'iode et le chaud.
maman|Tu as senti l'eau, Nina ?
enfant-f|Elle est froide aux pieds.
maman|Oui.
maman|Plus loin, elle brille.
enfant-f|Je veux un coquillage.
maman|On en cherche un, près de l'écume.
narrateur|En ce moment, Nina marche au bord.
narrateur|Le soleil tape ses épaules, fort.
narrateur|Son ombre est toute courte, devant elle.
maman|Le jour est long, ici.
maman|Le soleil est sur la mer.
narrateur|Nina ramasse une coquille beige.
narrateur|Elle est pleine de sable mouillé.
enfant-f|Il y a du sable.
maman|On la rince ?
enfant-f|Oui.
narrateur|Une vague plus vive arrive.
narrateur|L'eau prend la coquille, un instant.
enfant-f|Oh.
narrateur|Nina la reprend, ruisselante.
narrateur|Elle la plonge dans une flaque claire.
narrateur|Le sable part, le rose apparaît.
enfant-f|Elle est rose dedans.
maman|Merci, Nina.
maman|Tu l'as rincée.
narrateur|Ils restent encore un peu.
narrateur|Les épaules de Nina piquent, chaudes.
narrateur|Un bateau passe, tout petit.
enfant-f|Il va loin.
maman|Comme nous, tout à l'heure.
narrateur|Plus tard, le sable refroidit.
narrateur|Le ciel se teinte de mauve.
maman|On rentre.
narrateur|Dans la voiture, la coquille tient dans un gant.
narrateur|La mer recule derrière les dunes.
narrateur|La vitre s'assombrit.
narrateur|Une lune ronde glisse sur le verre.
enfant-f|Elle nous suit.
maman|La nuit est là.
maman|La lune est dans la vitre.
"""),
        "CHK_T0000_P0000_Q0001": L("""
narrateur|Nina est rentrée.
narrateur|La nuit, que voit-elle à la vitre ?
"""),
        "CHK_T0000_P0000_C0001": L("""
narrateur|Nina a marché au soleil, le sable chaud.
narrateur|Maintenant la lune est sur la vitre.
maman|Le jour, c'était le soleil sur la mer.
maman|La nuit, c'est la lune.
enfant-f|Elle est ronde, comme le coquillage.
maman|Un peu, oui.
narrateur|La coquille pose une tache d'eau sur le gant.
enfant-f|Elle est encore mouillée.
maman|On la met près de la fenêtre ?
enfant-f|Oui.
narrateur|La maison sent le sel, encore.
maman|Le pyjama, maintenant.
"""),
        "CHK_T0000_P0000_END": L("""
narrateur|Nina enfile le pyjama, un peu rêche de sel.
narrateur|Elle pose le coquillage sur la table.
narrateur|La lune le touche, pâle.
maman|La nuit, on se couche.
maman|Tu fermes les yeux ?
enfant-f|Je regarde encore.
narrateur|Dehors, la mer n'est plus qu'un souffle.
narrateur|Dedans, le verre de la fenêtre est froid.
enfant-f|Elle est toujours là.
maman|Oui.
maman|La lune reste.
narrateur|Maman baisse la lumière.
narrateur|Nina respire l'iode sur sa peau.
"""),
        "CHK_T0000_P0000_END_F0001": L("""
narrateur|Le coquillage sèche tout doux.
narrateur|Le rose dedans devient mat.
enfant-f|Il a gardé la mer.
maman|Un peu, oui.
narrateur|La lune reste collée à la vitre.
narrateur|Nina ferme les yeux, le sel aux genoux.
"""),
    },
    {"CHK_T0000_P0000": "vagues"},
    {
        "expected_answer": "lune",
        "accepted_examples": "lune | la lune | la lune dans la vitre | la lune à la fenêtre",
        "retry_prompt": "Le jour, le soleil. La nuit, à la vitre, que voit-on ?",
    },
)
relecture(
    "ATOM-TMP.JOU.001-02",
    "Le coquillage de Nina",
    "Nina veut un coquillage. Soleil sur les épaules, vague, sable. Le soir, lune dans la vitre, coquille sur la table.",
    "- Désir : le coquillage.\n"
    "- Imprévu : vague puis sable. Elle rince.\n"
    "- Jour mer / nuit vitre. Troupe : Nina, maman.",
)


# ---------------------------------------------------------------------------
# ATOM-TMP.JOU.001-03  N2  Aniss, maman — tomates, soleil puis lune
# ---------------------------------------------------------------------------
write_story(
    "ATOM-TMP.JOU.001-03",
    "Aniss veut une tomate rouge pour la salade. Le soleil chauffe le fruit. L'arrosoir verse de travers. Le soir, la lune pose un rond blanc sur le même pied.",
    "Les tomates d'Aniss",
    "Aniss, maman",
    "jardin, pied de tomate",
    {
        "CHK_T0000_P0000": L("""
narrateur|Les feuilles de tomate sentent le vert, fort.
narrateur|La terre du rang est sèche, déjà.
narrateur|Une abeille tourne autour d'une fleur jaune.
narrateur|Le tuteur en bois est chaud.
maman|Tu as senti les feuilles, Aniss ?
enfant-m|Ça sent fort.
maman|Oui.
maman|C'est le pied de tomate.
enfant-m|Je veux une tomate rouge.
maman|Pour la salade, ce soir ?
enfant-m|Oui.
narrateur|En ce moment, Aniss touche un fruit.
narrateur|Le soleil le rend lisse et chaud.
narrateur|Un autre fruit est encore vert, dur.
maman|Le jour chauffe les rouges.
maman|Le soleil est sur les tomates.
narrateur|Aniss lève l'arrosoir.
narrateur|L'eau part de travers, trop vite.
narrateur|La terre fait une flaque, puis boit.
enfant-m|Oh.
enfant-m|Ça a trop coulé.
maman|On verse plus lentement ?
enfant-m|Oui.
narrateur|Aniss penche l'arrosoir tout doux.
narrateur|L'eau file au pied, sans flaque.
maman|Merci, Aniss.
maman|Tu as rattrapé l'eau.
narrateur|Il cherche la plus rouge.
narrateur|Celle-là est trop haute, un peu.
maman|Je te la tends.
narrateur|La tomate se détache, tiède.
enfant-m|Elle est chaude.
maman|Le soleil l'a tenue.
narrateur|Ils la posent dans le panier.
narrateur|Le panier sent l'osier sec.
narrateur|Plus tard, l'air refroidit les feuilles.
narrateur|Le ciel passe au bleu foncé.
narrateur|Une lune ronde s'accroche au tuteur.
enfant-m|Elle est sur le pied.
maman|La nuit est là.
maman|La lune est sur les tomates.
"""),
        "CHK_T0000_P0000_Q0001": L("""
narrateur|La lune est sur le pied.
narrateur|Quel moment est-ce ?
"""),
        "CHK_T0000_P0000_C0001": L("""
narrateur|Aniss a cueilli au soleil, le fruit chaud.
narrateur|Maintenant la lune pose un rond sur les feuilles.
maman|Le jour, c'était le soleil.
maman|La nuit, c'est la lune.
enfant-m|Le même pied.
maman|Oui.
maman|On rentre avec le panier ?
enfant-m|La salade.
narrateur|Les tomates vertes restent dehors.
narrateur|Elles sont plus pâles, sous la lune.
maman|Elles attendront demain.
"""),
        "CHK_T0000_P0000_END": L("""
narrateur|La cuisine sent la tomate coupée.
narrateur|Le fruit est encore tiède au couteau.
enfant-m|Elle est sucrée.
maman|Le soleil l'avait gardée.
maman|La nuit, on se couche.
maman|Tu mets le pyjama ?
enfant-m|Oui.
narrateur|Aniss enfile le pyjama, les doigts un peu verts.
narrateur|À la fenêtre, le pied est déjà sombre.
enfant-m|La lune est encore là ?
maman|Sur les feuilles, oui.
narrateur|Maman baisse la lumière.
narrateur|Aniss respire le vert des tomates.
"""),
        "CHK_T0000_P0000_END_F0001": L("""
narrateur|Aniss pose le noyau dans le compost.
narrateur|À la fenêtre, le pied est noir.
narrateur|La lune tient encore une feuille.
enfant-m|Elle est toujours là.
maman|Oui.
maman|Sur le même pied.
narrateur|Aniss ferme les yeux, le vert aux doigts.
"""),
    },
    {"CHK_T0000_P0000": "jardin"},
    {
        "expected_answer": "nuit",
        "accepted_examples": "nuit | la nuit | le soir | dodo | c'est la nuit",
        "retry_prompt": "La lune est sur les tomates. C'est le jour, ou la nuit ?",
    },
)
relecture(
    "ATOM-TMP.JOU.001-03",
    "Les tomates d'Aniss",
    "Aniss veut une tomate rouge. Soleil sur le fruit. Arrosoir de travers. Le soir, lune sur le même pied.",
    "- Désir : la tomate pour la salade.\n"
    "- Imprévu : eau trop vite. Il verse plus lentement.\n"
    "- Même pied, jour puis nuit. Troupe : Aniss, maman.",
)


# ---------------------------------------------------------------------------
# ATOM-TMP.JOU.001-04  N3  Raphaël, maman, papa — montagne, chaussettes
# ---------------------------------------------------------------------------
write_story(
    "ATOM-TMP.JOU.001-04",
    "Raphaël veut le goûter sur la crête. Un ruisseau mouille ses chaussettes. Elles sèchent au soleil. Le soir, la lune tient la crête, les chaussettes sont sèches.",
    "Les chaussettes de Raphaël",
    "Raphaël, maman, papa",
    "montagne, crête, chalet",
    {
        "CHK_T0000_P0000": L("""
narrateur|L'air de la crête pique les oreilles.
narrateur|L'herbe est rase, un peu grise.
narrateur|Une pierre tient encore le froid de la nuit.
narrateur|Ça sent le thym et la laine.
papa|Tu as senti le vent, Raphaël ?
enfant-m|Il pique.
maman|Oui.
maman|Plus haut, il pique davantage.
enfant-m|Je veux le goûter, là haut.
papa|Sur la crête ?
enfant-m|Oui.
narrateur|En ce moment, Raphaël saute le ruisseau.
narrateur|L'eau est étroite, mais vive.
narrateur|Une chaussette prend une goutte, puis l'autre.
enfant-m|Elles sont mouillées.
maman|On les ôte ?
papa|On les met au soleil.
narrateur|Le soleil tient déjà la crête, nette.
narrateur|La pierre devient tiède, puis chaude.
narrateur|Maman étend les chaussettes sur la pierre.
narrateur|Elles font deux virgules sombres, qui s'éclaircissent.
enfant-m|Elles sèchent ?
papa|Le jour les sèche.
papa|Le soleil est sur la crête.
narrateur|Raphaël marche pieds nus, l'herbe pique.
narrateur|Papa ouvre le sac du goûter.
narrateur|Le pain sent encore la maison.
enfant-m|Le fromage.
maman|Le voilà.
narrateur|Ils mangent face à la ligne claire.
narrateur|Un nuage passe, l'ombre court sur la pierre.
enfant-m|Mes chaussettes.
papa|Elles sont encore un peu froides.
maman|Encore un peu de jour.
narrateur|Plus tard, le vent tourne, plus doux.
narrateur|Le ciel se creuse, bleu foncé.
narrateur|Une lune ronde s'accroche à la crête.
enfant-m|Elle est sur la pierre.
maman|La nuit est là.
papa|La lune est sur la crête.
maman|On rentre au chalet ?
enfant-m|Les chaussettes.
narrateur|Elles sont sèches, un peu raides.
papa|Merci, soleil.
maman|Merci, Raphaël.
maman|Tu as attendu.
"""),
        "CHK_T0000_P0000_Q0001": L("""
narrateur|La lune est sur la crête.
narrateur|Quel moment est-ce ?
"""),
        "CHK_T0000_P0000_C0001": L("""
narrateur|Raphaël a mangé au soleil, les chaussettes sur la pierre.
narrateur|Maintenant la lune tient la même ligne.
papa|Le jour, c'était le soleil.
maman|La nuit, c'est la lune.
enfant-m|Mes chaussettes sont sèches.
papa|Oui.
papa|On se couche au chalet ?
enfant-m|Encore la lune.
maman|On la verra à la fenêtre.
narrateur|Le thym sent encore, dans la laine.
"""),
        "CHK_T0000_P0000_END": L("""
narrateur|Le chalet sent le bois chaud.
narrateur|Raphaël enfile les chaussettes, sèches et rêche.
enfant-m|Elles chatouillent.
maman|Le soleil les a tenues.
papa|La nuit, on fait dodo.
papa|Tu fermes les yeux ?
enfant-m|Je regarde la crête.
narrateur|À la fenêtre, la lune est encore nette.
narrateur|La pierre du goûter n'est plus qu'une ombre.
maman|Elle est toujours là.
papa|Oui.
narrateur|Papa baisse la lampe.
narrateur|Raphaël respire le thym sur ses chaussettes.
"""),
        "CHK_T0000_P0000_END_F0001": L("""
narrateur|Les deux chaussettes font deux virgules claires.
narrateur|La lune tient encore la crête.
enfant-m|Elles sont sèches.
maman|Oui.
papa|Le jour les a séchées.
narrateur|Raphaël ferme les yeux, le vent aux oreilles.
"""),
    },
    {"CHK_T0000_P0000": "vent"},
    {
        "expected_answer": "nuit",
        "accepted_examples": "nuit | la nuit | le soir | dodo | c'est la nuit",
        "retry_prompt": "La lune est sur la crête. C'est le jour, ou la nuit ?",
    },
)
relecture(
    "ATOM-TMP.JOU.001-04",
    "Les chaussettes de Raphaël",
    "Raphaël veut le goûter sur la crête. Chaussettes mouillées, séchage au soleil. Le soir, lune sur la même ligne.",
    "- Désir : le goûter en haut.\n"
    "- Imprévu : ruisseau, chaussettes. Ils attendent qu'elles sèchent.\n"
    "- Papa et maman parlent. Troupe : Raphaël, papa, maman.",
)


# ---------------------------------------------------------------------------
# ATOM-TMP.JOU.001-05  N1  Chouchou, papa — balcon, toits, chat, lune
# ---------------------------------------------------------------------------
write_story(
    "ATOM-TMP.JOU.001-05",
    "Chouchou veut le chat du mur. Le soleil cligne sur les toits. Un pigeon fait fuir le chat. Le soir, la lune est sur le zinc, le chat revient.",
    "Le chat du mur de Chouchou",
    "Chouchou, papa",
    "balcon en ville",
    {
        "CHK_T0000_P0000": L("""
narrateur|Les toits de zinc clignent sous le soleil.
narrateur|Le balcon sent le linge chaud.
narrateur|Une gouttière tient une feuille sèche.
narrateur|Le mur d'en face est déjà brûlant.
papa|Tu as vu le zinc, Chouchou ?
enfant-f|Il brille.
papa|Oui.
papa|Les toits sont chauds.
enfant-f|Je veux le chat.
papa|Il vient sur le mur.
narrateur|En ce moment, Chouchou s'accoude.
narrateur|Le fer du balcon est chaud.
narrateur|Le soleil tape les toits, fort.
papa|Le jour est clair.
papa|Le soleil est sur les toits.
narrateur|Un chat gris arrive sur le mur.
narrateur|Il se frotte, lent.
enfant-f|Il est là.
papa|Tout doux.
narrateur|Un pigeon se pose, brusque.
narrateur|Le chat saute, disparu.
enfant-f|Oh.
enfant-f|Il est parti.
papa|Il reviendra.
papa|On attend ?
enfant-f|Oui.
narrateur|Chouchou reste accoudée.
narrateur|Une lessive claque, à côté.
narrateur|Une radio chante, loin.
narrateur|Un camion passe en bas, sourd.
enfant-f|Il tarde.
papa|Le jour est encore long.
narrateur|Une goutte tombe de la gouttière.
narrateur|Elle sèche sur le zinc, vite.
narrateur|L'ombre du mur s'allonge.
narrateur|Le zinc perd son clignement.
narrateur|Le ciel devient bleu foncé.
narrateur|Une lune ronde s'assoit sur un toit.
enfant-f|Elle est sur le zinc.
papa|La nuit est là.
papa|La lune est sur les toits.
narrateur|Le chat revient, plus silencieux.
enfant-f|Le voilà.
papa|Merci d'avoir attendu.
papa|Tu as été patiente.
"""),
        "CHK_T0000_P0000_Q0001": L("""
narrateur|La lune est sur le toit.
narrateur|Quel moment est-ce ?
"""),
        "CHK_T0000_P0000_C0001": L("""
narrateur|Chouchou a vu le zinc tout brillant.
narrateur|Maintenant la lune est sur le même toit.
papa|Le jour, c'était le soleil.
papa|La nuit, c'est la lune.
enfant-f|Le chat est revenu.
papa|Oui.
papa|On rentre se coucher ?
enfant-f|Encore le chat.
narrateur|Le chat se lèche une patte.
narrateur|La gouttière tient encore sa feuille.
papa|Tu lui dis au revoir ?
enfant-f|À demain.
narrateur|Le linge ne claque plus.
narrateur|L'air du balcon est plus frais.
"""),
        "CHK_T0000_P0000_END": L("""
narrateur|Chouchou quitte le fer du balcon.
narrateur|Le fer est plus froid, maintenant.
papa|Le pyjama, maintenant.
narrateur|Le pyjama sent le linge du balcon.
enfant-f|La lune est encore là ?
papa|À la fenêtre.
narrateur|Chouchou monte sur le lit.
narrateur|Le zinc est gris, dehors.
narrateur|La lune tient encore un coin de toit.
papa|La nuit, on fait dodo.
papa|Tu fermes les yeux ?
enfant-f|Presque.
narrateur|Papa baisse la lumière.
narrateur|Chouchou respire le linge chaud.
"""),
        "CHK_T0000_P0000_END_F0001": L("""
narrateur|Le chat reste une tache sur le mur.
narrateur|La lune reste une tache sur le zinc.
enfant-f|Il est revenu.
papa|Oui.
papa|Toi aussi, tu as attendu.
narrateur|Chouchou ferme les yeux.
narrateur|La gouttière ne bouge plus.
"""),
    },
    {"CHK_T0000_P0000": "ville"},
    {
        "expected_answer": "nuit",
        "accepted_examples": "nuit | la nuit | le soir | dodo | c'est la nuit",
        "retry_prompt": "La lune est sur le toit. C'est le jour, ou la nuit ?",
    },
)
relecture(
    "ATOM-TMP.JOU.001-05",
    "Le chat du mur de Chouchou",
    "Chouchou veut le chat. Soleil sur le zinc. Un pigeon le fait fuir. Le soir, lune sur le toit, le chat revient.",
    "- Désir : le chat, pas la leçon.\n"
    "- Imprévu : pigeon. Elle attend.\n"
    "- Toits le jour, toits la nuit. Troupe : Chouchou, papa.",
)
