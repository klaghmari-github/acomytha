#!/usr/bin/env python3
"""ATOM-SOC.ARG.001-07 + ARG.002-01..07 — merged.json via _lib."""
from __future__ import annotations

from _lib import relecture, write_story


def S(block: str) -> list[str]:
    return [ln.strip() for ln in block.strip().splitlines() if ln.strip()]


EMPTY = {
    "CHK_T0000_P0000": "",
    "CHK_T0000_P0000_Q0001": "",
    "CHK_T0000_P0000_C0001": "",
    "CHK_T0000_P0000_END": "",
    "CHK_T0000_P0000_END_F0001": "",
}


# ---------------------------------------------------------------------------
# ATOM-SOC.ARG.001-07 N3 Aniss, papa — marché couvert, fromage
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SOC.ARG.001-07",
    "Aniss et papa vont au marché couvert avec l'argent du travail. Le fromage fort pique. Ils prennent le doux. Aniss le tient.",
    "Le fromage doux d'Aniss",
    "Aniss, papa",
    "marché couvert, hall de verre, stand de fromage",
    {
        "CHK_T0000_P0000": S("""
narrateur|Les vitres du hall font des carreaux d'or.
narrateur|Des pigeons marchent sur une poutre.
narrateur|Ça sent le foin et le lait.
narrateur|Une paille craque sous une caisse.
narrateur|Le toit de verre cliquette un peu.
narrateur|Papa a fini son travail.
narrateur|Sa poche de toile est lourde.
papa|J'ai travaillé, Aniss.
papa|Avec le travail, on a de l'argent.
papa|L'argent sert à acheter.
enfant-m|On achète du fromage ?
papa|Oui.
papa|Pour le pain de ce soir.
narrateur|En ce moment, ils marchent sous le verre.
narrateur|Aniss tient le bord du cabas.
narrateur|Le cabas gratte un peu sa jambe.
narrateur|Un stand aligne des meules.
narrateur|Des croûtes jaunes brillent.
enfant-m|Ça sent fort !
papa|Tu as senti le fromage ?
narrateur|Aniss se penche vers une meule.
narrateur|La croûte est rêche sous son doigt.
enfant-m|Je veux celui-là.
narrateur|Papa coupe un tout petit bout.
narrateur|Aniss goûte.
narrateur|Le goût pique sa langue.
enfant-m|Il est trop fort !
papa|Il pique, n'est-ce pas ?
narrateur|Aniss recule d'un pas.
narrateur|Ses yeux piquent un peu.
enfant-m|Je n'en veux plus.
papa|On prend le doux, alors ?
narrateur|À côté, une meule est plus claire.
narrateur|Elle sent le lait, presque rien.
enfant-m|Celle-là.
enfant-m|Elle est douce.
papa|Tu la veux pour le pain ?
enfant-m|Oui, papa.
narrateur|Papa sort l'argent de sa poche.
narrateur|Les pièces sont froides et claires.
papa|C'est l'argent du travail.
papa|Il sert à acheter.
        """),
        "CHK_T0000_P0000_Q0001": S("""
narrateur|Papa a travaillé.
narrateur|L'argent sert à quoi ?
        """),
        "CHK_T0000_P0000_C0001": S("""
narrateur|Papa pose les pièces sur le bois.
narrateur|Le bois est taché de lait.
narrateur|On lui tend le fromage doux.
narrateur|Il est enveloppé dans un papier.
narrateur|Le papier craque un peu.
enfant-m|Il est à nous ?
papa|Oui.
papa|On l'a acheté.
papa|Merci, Aniss.
papa|Tu as choisi le doux.
narrateur|Aniss prend le paquet contre lui.
narrateur|Le fromage est frais, un peu mou.
enfant-m|Il ne pique plus.
papa|Tu le portes jusqu'à la maison ?
enfant-m|Oui.
narrateur|Ils quittent le stand.
narrateur|Une goutte tombe du toit de verre.
narrateur|Elle fait un rond dans la poussière.
        """),
        "CHK_T0000_P0000_END": S("""
narrateur|Dehors, l'air est plus léger.
narrateur|Le cabas tape contre la jambe.
narrateur|Aniss garde le fromage dans ses bras.
papa|Tu as encore le paquet ?
enfant-m|Oui.
enfant-m|Il est frais.
papa|Le pain nous attend.
narrateur|La rue sent encore le foin.
narrateur|Une feuille tourne près du caniveau.
narrateur|Ils montent les marches de la maison.
narrateur|La clé fait un petit clic.
narrateur|La table de la cuisine est claire.
narrateur|Le pain est déjà là, tiède.
papa|Tu poses le fromage près du pain ?
narrateur|Aniss pose le paquet.
narrateur|Il ouvre le papier, tout doux.
        """),
        "CHK_T0000_P0000_END_F0001": S("""
narrateur|Papa coupe une tranche de pain.
narrateur|Aniss étale le fromage doux.
narrateur|Ça fond un peu, blanc et calme.
enfant-m|Il ne pique pas.
papa|Bravo.
papa|Tu as bien choisi.
narrateur|Aniss croque.
narrateur|Le pain est tiède sous les dents.
narrateur|Le fromage doux reste sur sa langue.
narrateur|Il tient encore le papier vide.
narrateur|Le fromage doux fond encore sur le pain.
        """),
    },
    EMPTY,
    {
        "expected_answer": "acheter",
        "accepted_examples": "acheter | le fromage | fromage | acheter du fromage | à acheter",
        "retry_prompt": "L'argent sert à acheter. L'argent sert à quoi ?",
    },
)
relecture(
    "ATOM-SOC.ARG.001-07",
    "Le fromage doux d'Aniss",
    "Marché couvert, argent du travail, fromage trop fort, fromage doux dans les mains, tartine.",
    "Ouverture vitres du hall. Leçon greffée : l'argent sert à acheter. Fin vécue, sans refrain.",
)


# ---------------------------------------------------------------------------
# ATOM-SOC.ARG.002-01 N2 Sarah, maman — pelote rouge
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SOC.ARG.002-01",
    "Sarah veut une petite pelote rouge à la mercerie. Elle tend la main sans demander. Maman attend la question. Sarah demande. La pelote est à elle.",
    "La pelote rouge de Sarah",
    "Sarah, maman",
    "mercerie, tiroirs de bois, vitrine de laine",
    {
        "CHK_T0000_P0000": S("""
narrateur|La mercerie sent la laine et le savon.
narrateur|Un rayon perce le verre un peu poussiéreux.
narrateur|Des boutons brillent dans un tiroir.
narrateur|Le bois du comptoir est lisse, usé.
narrateur|Une pelote bleue a perdu un fil.
narrateur|Le fil traîne comme un cheveu.
narrateur|Maman pousse la porte.
narrateur|La clochette fait un tout petit ding.
enfant-f|Ça sent la laine !
maman|Oui.
maman|On vient chercher du fil.
narrateur|Sarah touche un bouton, tout rond.
narrateur|Il est froid, un peu lisse.
narrateur|En ce moment, Sarah s'arrête devant la vitrine.
narrateur|Une petite pelote rouge attend derrière le verre.
narrateur|Elle est ronde, toute serrée.
enfant-f|Elle est rouge.
enfant-f|Je la veux.
narrateur|Sarah tend la main.
narrateur|Ses doigts touchent presque la laine.
narrateur|Maman ne bouge pas.
narrateur|Le petit sac reste fermé.
maman|Sarah.
maman|Tu me demandes ?
narrateur|La main de Sarah s'arrête.
narrateur|La pelote est encore derrière le verre.
enfant-f|Oh.
narrateur|Elle rentre les doigts.
narrateur|Maman attend, tout près.
maman|On achète si tu demandes.
maman|Tu te souviens ?
enfant-f|Je peux demander.
narrateur|La clochette s'est tue.
narrateur|Un tiroir sent encore le savon.
narrateur|La laine rouge attend encore.
        """),
        "CHK_T0000_P0000_Q0001": S("""
narrateur|Sarah veut la pelote rouge.
narrateur|Que fait-elle ?
        """),
        "CHK_T0000_P0000_C0001": S("""
enfant-f|Maman, s'il te plaît.
enfant-f|Je peux avoir la pelote ?
maman|Oui.
maman|Merci, Sarah.
maman|Tu as demandé.
narrateur|Maman ouvre le petit sac.
narrateur|Elle pose l'argent sur le bois.
narrateur|On lui tend la pelote rouge.
narrateur|Sarah la prend des deux mains.
narrateur|La laine est douce, un peu chaude.
enfant-f|Elle est à moi.
maman|Oui.
maman|Parce que tu as demandé.
narrateur|Sarah serre la pelote contre sa veste.
narrateur|Un fil rouge dépasse un peu.
maman|Tu la tiens bien ?
enfant-f|Oui, maman.
        """),
        "CHK_T0000_P0000_END": S("""
narrateur|Elles sortent.
narrateur|La clochette dingue encore une fois.
narrateur|La rue sent le pain, plus loin.
narrateur|Sarah marche avec la pelote.
narrateur|Le fil rouge tape sa manche.
maman|On rentre faire un tour de laine ?
enfant-f|Oui.
enfant-f|Pour le doudou.
maman|Tu as demandé avant d'acheter.
maman|Bravo.
narrateur|Le soleil est sur le trottoir.
narrateur|La pelote fait une ombre ronde.
narrateur|Sarah sent la laine contre sa veste.
narrateur|Elle est tiède, comme une main.
        """),
        "CHK_T0000_P0000_END_F0001": S("""
narrateur|À la maison, Sarah s'assoit.
narrateur|Elle pose la pelote sur ses genoux.
narrateur|Elle tire un peu de fil.
narrateur|Le rouge court entre ses doigts.
enfant-f|Il est doux.
maman|Oui.
maman|Tu l'as dans les mains.
narrateur|Sarah enroule le fil autour du doudou.
narrateur|Le doudou a maintenant un collier rouge.
enfant-f|Il est beau.
maman|Il est au chaud.
narrateur|La pelote rouge tourne entre ses doigts.
        """),
    },
    EMPTY,
    {
        "expected_answer": "demander",
        "accepted_examples": "demander | elle demande | elle demande à maman | à maman | s'il te plaît",
        "retry_prompt": "Elle demande à maman. Que fait Sarah ?",
    },
)
relecture(
    "ATOM-SOC.ARG.002-01",
    "La pelote rouge de Sarah",
    "Mercerie, pelote rouge, main tendue trop tôt, question, pelote dans les mains.",
    "Leçon greffée : demander avant d'acheter. Maman attend. Fin vécue.",
)


# ---------------------------------------------------------------------------
# ATOM-SOC.ARG.002-02 N2 Amir, papa — sifflet en bois au kiosque
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SOC.ARG.002-02",
    "Amir veut un sifflet en bois au kiosque. Le sifflet peint n'est plus là. Il tend la main. Papa attend. Amir demande. Le bois est à lui.",
    "Le sifflet de bois d'Amir",
    "Amir, papa",
    "kiosque de zinc sur la place, après le soleil",
    {
        "CHK_T0000_P0000": S("""
narrateur|Le zinc du kiosque claque au soleil.
narrateur|Des journaux sont pincés par une pince.
narrateur|Ça sent l'encre et le bois chaud.
narrateur|Une place de sable brille tout autour.
narrateur|Une ombre de parasol tremble un peu.
narrateur|Papa a un sac de toile à l'épaule.
enfant-m|Le kiosque est ouvert !
papa|Oui.
papa|On va voir.
narrateur|Amir marche sur le sable chaud.
narrateur|Des grains collent à sa chaussure.
narrateur|En ce moment, Amir s'arrête au bord du zinc.
narrateur|Des sifflets sont dans une boîte.
narrateur|Un sifflet rouge n'est plus là.
enfant-m|Il n'y en a plus, le rouge.
papa|Il est parti.
papa|Il reste le bois.
narrateur|Un sifflet de bois est lisse, clair.
narrateur|Un petit trou rond au bout.
enfant-m|Je le veux.
narrateur|Amir tend la main vers la boîte.
narrateur|Papa ne sort pas l'argent.
papa|Amir.
papa|Tu me demandes ?
narrateur|La main d'Amir s'arrête.
narrateur|Le sifflet reste dans la boîte.
enfant-m|Ah.
papa|On achète si tu demandes.
papa|Tu te souviens ?
enfant-m|Je peux demander.
narrateur|Le zinc est chaud sous le soleil.
narrateur|Une pince tient encore un journal.
narrateur|L'encre sent un peu fort.
        """),
        "CHK_T0000_P0000_Q0001": S("""
narrateur|Amir veut le sifflet de bois.
narrateur|Que fait-il ?
        """),
        "CHK_T0000_P0000_C0001": S("""
enfant-m|Papa, s'il te plaît.
enfant-m|Je peux avoir le sifflet ?
papa|Oui.
papa|Merci, Amir.
papa|Tu as demandé.
narrateur|Papa sort une pièce de sa poche.
narrateur|La pièce cliquette sur le zinc.
narrateur|On lui tend le sifflet de bois.
narrateur|Amir le prend.
narrateur|Le bois est chaud, tout lisse.
enfant-m|Il est à moi.
papa|Oui.
papa|Parce que tu as demandé.
papa|Tu souffles tout doux ?
narrateur|Amir souffle.
narrateur|Le sifflet fait un petit cri clair.
enfant-m|Il chante !
papa|Bravo.
narrateur|Un second souffle, plus doux.
narrateur|Le cri est plus petit.
        """),
        "CHK_T0000_P0000_END": S("""
narrateur|Ils quittent le kiosque.
narrateur|Le zinc claque encore un peu.
narrateur|Amir tient le sifflet dans la main.
narrateur|L'autre main tient papa.
papa|Tu le mets dans ta poche ?
enfant-m|Pas encore.
enfant-m|Il est tiède.
narrateur|La place sent le sable chaud.
narrateur|Un pigeon picore près d'une feuille.
papa|On rentre.
enfant-m|Avec le sifflet.
narrateur|Amir souffle encore, tout bas.
narrateur|Le cri se perd dans le sable.
        """),
        "CHK_T0000_P0000_END_F0001": S("""
narrateur|Devant la maison, Amir souffle encore.
narrateur|Le cri est petit, tout rond.
papa|Tu l'as dans les mains.
enfant-m|Oui.
narrateur|Amir glisse le bois dans sa poche.
narrateur|La poche est chaude contre sa jambe.
narrateur|Il pose la main dessus, pour garder le chant.
narrateur|Le sifflet de bois reste tiède dans sa poche.
        """),
    },
    EMPTY,
    {
        "expected_answer": "demander",
        "accepted_examples": "demander | il demande | il demande à papa | à papa | s'il te plaît",
        "retry_prompt": "Il demande à papa. Que fait Amir ?",
    },
)
relecture(
    "ATOM-SOC.ARG.002-02",
    "Le sifflet de bois d'Amir",
    "Kiosque, sifflet rouge parti, sifflet de bois, main tendue, demande, bois dans la poche.",
    "Imprévu : rouge épuisé. Leçon greffée. Fin vécue.",
)


# ---------------------------------------------------------------------------
# ATOM-SOC.ARG.002-03 N1 Mila, papa — pêche
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SOC.ARG.002-03",
    "Mila veut une pêche au stand. Elle tend la main. Papa attend. Elle demande. La pêche est à elle.",
    "La pêche de Mila",
    "Mila, papa",
    "stand de fruits, caisses en bois, soleil",
    {
        "CHK_T0000_P0000": S("""
narrateur|Les pêches brillent dans la caisse.
narrateur|Le bois est chaud.
narrateur|Ça sent le sucre.
narrateur|Une abeille tourne tout près.
narrateur|Papa tient le cabas.
narrateur|Mila marche à côté.
narrateur|Le sol est un peu poudreux.
narrateur|Une feuille colle à sa chaussure.
narrateur|Une caisse de prunes est plus loin.
narrateur|Les prunes sont sombres, toutes lisses.
narrateur|Un parasol fait une ombre ronde.
narrateur|Mila entre dans l'ombre.
papa|Tu as vu les fruits ?
enfant-f|Oui.
enfant-f|Ils brillent.
papa|Ça sent bon, tu vois ?
enfant-f|Oui, papa.
narrateur|Un grain de sable colle au bois.
narrateur|En ce moment, Mila s'arrête.
narrateur|Elle voit une pêche.
narrateur|La pêche est ronde.
narrateur|Elle est jaune et rose.
enfant-f|Je la veux.
narrateur|Mila tend la main.
narrateur|Ses doigts touchent le duvet.
narrateur|Papa ne bouge pas.
papa|Mila.
papa|Tu demandes ?
narrateur|La main s'arrête.
narrateur|La pêche reste dans la caisse.
enfant-f|Oh.
papa|On achète si tu demandes.
enfant-f|Je peux demander.
papa|Tu me dis s'il te plaît ?
enfant-f|Oui, papa.
narrateur|L'abeille s'éloigne.
narrateur|Une autre pêche roule un peu.
narrateur|Le duvet de la pêche brille.
        """),
        "CHK_T0000_P0000_Q0001": S("""
narrateur|Mila veut la pêche.
narrateur|Que fait-elle ?
        """),
        "CHK_T0000_P0000_C0001": S("""
enfant-f|Papa, s'il te plaît.
enfant-f|Je peux avoir la pêche ?
papa|Oui.
papa|Merci, Mila.
papa|Tu as demandé.
narrateur|Papa pose l'argent.
narrateur|On lui tend la pêche.
narrateur|Mila la prend.
narrateur|Elle est douce, un peu chaude.
enfant-f|Elle est à moi.
papa|Oui.
papa|Parce que tu as demandé.
papa|Tu la tiens bien ?
enfant-f|Oui, papa.
narrateur|Le cabas reste ouvert.
narrateur|Mila garde la pêche.
narrateur|Elle la tourne dans sa paume.
narrateur|Le rose est plus chaud que le jaune.
papa|Elle est mûre.
enfant-f|Elle est douce.
narrateur|Un peu de duvet reste au doigt.
        """),
        "CHK_T0000_P0000_END": S("""
narrateur|Ils quittent le stand.
narrateur|Le bois craque un peu.
narrateur|Mila marche avec la pêche.
narrateur|Le duvet chatouille sa paume.
papa|On rentre ?
enfant-f|Oui.
enfant-f|Avec la pêche.
narrateur|La rue sent encore le sucre.
narrateur|Une feuille tourne.
papa|Tu as demandé.
papa|Bravo.
narrateur|Mila serre la pêche.
narrateur|Elle la sent encore.
narrateur|Ça sent le soleil.
narrateur|Papa prend sa main libre.
enfant-f|Je tiens la pêche.
papa|Oui.
narrateur|Ils passent près d'une flaque.
        """),
        "CHK_T0000_P0000_END_F0001": S("""
narrateur|À la maison, Mila s'assoit.
narrateur|Elle croque la pêche.
narrateur|Le jus est sucré.
narrateur|Il brille sur son menton.
enfant-f|Elle est bonne.
papa|Oui.
papa|Tu l'as dans les mains.
narrateur|Mila tient le noyau.
narrateur|Il est lisse et chaud.
narrateur|Elle le pose près du cabas.
enfant-f|Il reste.
papa|Oui.
papa|Le cœur de la pêche.
narrateur|Mila essuie son menton.
narrateur|Le jus de pêche brille sur son menton.
        """),
    },
    EMPTY,
    {
        "expected_answer": "demander",
        "accepted_examples": "demander | elle demande | à papa | s'il te plaît",
        "retry_prompt": "Elle demande à papa. Que fait Mila ?",
    },
)
relecture(
    "ATOM-SOC.ARG.002-03",
    "La pêche de Mila",
    "Stand de fruits, pêche ronde, main tendue, demande, jus sur le menton.",
    "N1 phrases courtes. Leçon greffée. Fin vécue.",
)


# ---------------------------------------------------------------------------
# ATOM-SOC.ARG.002-04 N3 Nina, maman — livre d'images, deux rayons
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SOC.ARG.002-04",
    "Nina veut un livre d'images. Le premier rayon n'en a pas. Au second, elle tire un livre. Maman attend. Nina demande. Le livre est à elle.",
    "Le livre d'images de Nina",
    "Nina, maman",
    "librairie, deux rayons de bois, odeur de papier",
    {
        "CHK_T0000_P0000": S("""
narrateur|Deux allées sentent le papier neuf.
narrateur|Le bois des rayons est sombre, lisse.
narrateur|Une poussière d'or flotte dans le jour.
narrateur|Maman pousse la porte vitrée.
narrateur|Un tapis étouffe les pas.
narrateur|Une lampe basse éclaire le comptoir.
enfant-f|Ça sent le papier.
maman|Oui.
maman|On cherche un livre d'images.
narrateur|Nina glisse la main sur un dos.
narrateur|En ce moment, Nina entre dans la première allée.
narrateur|Les dos sont épais, sans images.
enfant-f|Il n'y en a pas.
maman|C'est l'autre rayon.
maman|Tu viens ?
narrateur|Elles tournent au bout.
narrateur|La seconde allée est plus basse.
narrateur|Des couvertures colorées regardent.
narrateur|Nina s'arrête.
narrateur|Un petit livre montre un bateau.
enfant-f|Celui-là.
enfant-f|Il a un bateau.
narrateur|Nina tire le livre.
narrateur|Le papier racle le bois.
narrateur|Maman ne sort pas l'argent.
maman|Nina.
maman|Tu me demandes ?
narrateur|Le livre reste à moitié sorti.
enfant-f|Oh.
narrateur|Nina rentre le livre d'un doigt.
maman|On achète si tu demandes.
maman|Tu te souviens ?
enfant-f|Je peux demander.
maman|Tu me dis s'il te plaît ?
enfant-f|Oui, maman.
narrateur|Le bateau du livre attend encore.
        """),
        "CHK_T0000_P0000_Q0001": S("""
narrateur|Nina veut le livre d'images.
narrateur|Que fait-elle ?
        """),
        "CHK_T0000_P0000_C0001": S("""
enfant-f|Maman, s'il te plaît.
enfant-f|Je peux avoir ce livre ?
maman|Oui.
maman|Merci, Nina.
maman|Tu as demandé.
narrateur|Maman ouvre le petit sac.
narrateur|Elle pose l'argent sur le comptoir.
narrateur|On glisse le livre dans un sachet.
narrateur|Nina le prend contre elle.
narrateur|Le sachet est lisse, un peu froid.
enfant-f|Il est à moi.
maman|Oui.
maman|Parce que tu as demandé.
maman|Tu le tiens bien ?
enfant-f|Oui, maman.
narrateur|Elles quittent la seconde allée.
narrateur|Le tapis étouffe encore les pas.
narrateur|Nina sent le sachet contre sa veste.
        """),
        "CHK_T0000_P0000_END": S("""
narrateur|Dehors, le jour est plus vif.
narrateur|Nina marche avec le sachet.
narrateur|Le bateau de la couverture se sent.
maman|On le regardera à la maison ?
enfant-f|Oui.
enfant-f|Le bateau.
maman|Tu as demandé avant d'acheter.
maman|Bravo.
narrateur|Une feuille tourne près du caniveau.
narrateur|Le sachet tape un peu la jambe.
narrateur|Nina serre le livre contre elle.
narrateur|Le papier sent encore la boutique.
        """),
        "CHK_T0000_P0000_END_F0001": S("""
narrateur|À la maison, Nina s'assoit.
narrateur|Elle sort le livre du sachet.
narrateur|Elle ouvre la première page.
narrateur|Le bateau a une voile rouge.
enfant-f|Il avance.
maman|Oui.
maman|Tu l'as dans les mains.
narrateur|Nina tourne la page, tout doux.
narrateur|Une vague dessinée mouille presque le papier.
enfant-f|Elle est bleue.
maman|Comme la mer.
narrateur|Le livre d'images reste ouvert sur ses genoux.
        """),
    },
    EMPTY,
    {
        "expected_answer": "demander",
        "accepted_examples": "demander | elle demande | à maman | s'il te plaît",
        "retry_prompt": "Elle demande à maman. Que fait Nina ?",
    },
)
relecture(
    "ATOM-SOC.ARG.002-04",
    "Le livre d'images de Nina",
    "Librairie, premier rayon vide, second rayon, livre tiré trop tôt, demande, bateau sur les genoux.",
    "Deux rayons vécus. Leçon greffée. Fin vécue.",
)


# ---------------------------------------------------------------------------
# ATOM-SOC.ARG.002-05 N3 Victorino, papa — cerf-volant trop grand
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SOC.ARG.002-05",
    "Victorino veut un cerf-volant. Le grand est trop grand. Il demande le petit. Papa paie. Le petit tremble dans le vent.",
    "Le petit cerf-volant de Victorino",
    "Victorino, papa",
    "stand de jouets près du parc, vent de fin de jour",
    {
        "CHK_T0000_P0000": S("""
narrateur|Une toile claque au-dessus du stand.
narrateur|Le vent tire des ficelles colorées.
narrateur|Ça sent l'herbe coupée du parc.
narrateur|Une feuille sèche tourne près d'une caisse.
narrateur|Papa a le sac de toile à l'épaule.
enfant-m|Les cerfs-volants !
papa|Oui.
papa|Ils dansent.
narrateur|Victorino lève le menton.
narrateur|Le ciel est clair, un peu pâle.
narrateur|Une ficelle claque contre un pieu.
narrateur|Le pieu est planté dans l'herbe.
narrateur|En ce moment, Victorino lève les yeux.
narrateur|Un grand cerf-volant dépasse ses bras.
narrateur|La toile est rouge, trop large.
enfant-m|Celui-là.
enfant-m|Il est grand.
narrateur|Victorino tend les deux mains.
narrateur|Le grand ne rentre pas dans le sac.
papa|Il est trop grand, tu vois ?
narrateur|Le sac de toile est trop petit.
enfant-m|Oh.
narrateur|À côté, un petit cerf-volant attend.
narrateur|Il est bleu, avec une queue.
enfant-m|Le petit.
papa|Tu me demandes ?
narrateur|Victorino rentre les mains.
narrateur|Le grand reste accroché trop haut.
papa|On achète si tu demandes.
papa|Tu te souviens ?
enfant-m|Je peux demander.
papa|Tu me dis s'il te plaît ?
enfant-m|Oui, papa.
narrateur|Le vent claque encore la toile.
        """),
        "CHK_T0000_P0000_Q0001": S("""
narrateur|Victorino veut un cerf-volant.
narrateur|Que fait-il ?
        """),
        "CHK_T0000_P0000_C0001": S("""
enfant-m|Papa, s'il te plaît.
enfant-m|Je peux avoir le petit ?
papa|Oui.
papa|Merci, Victorino.
papa|Tu as demandé.
narrateur|Papa sort l'argent de sa poche.
narrateur|Les pièces cliquettent dans le vent.
narrateur|On lui tend le petit cerf-volant.
narrateur|Victorino le prend des deux mains.
narrateur|La toile bleue tremble un peu.
enfant-m|Il est à moi.
papa|Oui.
papa|Parce que tu as demandé.
papa|Il rentre dans le sac ?
narrateur|Victorino glisse le petit dans le sac.
narrateur|La queue dépasse encore.
enfant-m|Il rentre.
papa|Bravo.
narrateur|Le vent pousse encore la grande toile.
        """),
        "CHK_T0000_P0000_END": S("""
narrateur|Ils quittent le stand.
narrateur|L'herbe du parc est plus près.
papa|On le fait voler un peu ?
enfant-m|Oui.
narrateur|Victorino sort le petit du sac.
narrateur|Le vent prend la toile bleue.
narrateur|La queue ondule.
enfant-m|Il vole !
papa|Tu le tiens bien ?
enfant-m|Oui, papa.
narrateur|La ficelle est rêche dans sa paume.
narrateur|Un brin d'herbe colle à sa chaussure.
narrateur|Victorino recule d'un pas, pour le vent.
papa|Tu le sens, le vent ?
enfant-m|Oui.
enfant-m|Il tire.
        """),
        "CHK_T0000_P0000_END_F0001": S("""
narrateur|Le petit cerf-volant monte un peu.
narrateur|Puis il redescend dans les bras.
enfant-m|Je le garde.
papa|Oui.
papa|Tu l'as dans les mains.
narrateur|Victorino serre la toile bleue.
narrateur|Elle sent encore le vent.
narrateur|La queue s'enroule autour de son poignet.
narrateur|Le petit cerf-volant tremble dans le vent.
        """),
    },
    EMPTY,
    {
        "expected_answer": "demander",
        "accepted_examples": "demander | il demande | à papa | s'il te plaît | le petit",
        "retry_prompt": "Il demande à papa. Que fait Victorino ?",
    },
)
relecture(
    "ATOM-SOC.ARG.002-05",
    "Le petit cerf-volant de Victorino",
    "Stand venteux, grand trop grand, petit bleu, demande, vol court, toile dans les mains.",
    "Imprévu taille. Leçon greffée. Fin vécue.",
)


# ---------------------------------------------------------------------------
# ATOM-SOC.ARG.002-06 N2 Chouchou, maman — crayon jaune
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SOC.ARG.002-06",
    "Chouchou veut un crayon jaune. Elle tend la main vers le pot. Maman attend. Chouchou demande. Le crayon laisse un trait.",
    "Le crayon jaune de Chouchou",
    "Chouchou, maman",
    "papeterie, pot de verre, rayons de papier",
    {
        "CHK_T0000_P0000": S("""
narrateur|Un pot de verre tient des crayons jaunes.
narrateur|Le verre fait un rond de soleil.
narrateur|Ça sent le papier et le bois.
narrateur|Des feuilles blanches attendent en pile.
narrateur|Maman pousse la porte.
narrateur|Un tapis racle sous les chaussures.
enfant-f|Les crayons !
maman|Oui.
maman|Ils sont dans le pot.
narrateur|Chouchou marche entre deux rayons.
narrateur|Le papier craque un peu sous le doigt.
narrateur|Une gomme blanche attend plus loin.
narrateur|Chouchou ne la regarde pas.
narrateur|Un crayon bleu est trop loin.
enfant-f|Je veux le jaune.
maman|Le jaune du pot ?
enfant-f|Oui.
narrateur|En ce moment, Chouchou s'approche du verre.
narrateur|Un crayon jaune dépasse les autres.
narrateur|La mine est nette, encore pointue.
enfant-f|Celui-là.
enfant-f|Il est jaune.
narrateur|Chouchou tend la main.
narrateur|Ses doigts touchent le bois.
narrateur|Maman n'ouvre pas le sac.
maman|Chouchou.
maman|Tu me demandes ?
narrateur|La main s'arrête sur le bord du pot.
enfant-f|Oh.
narrateur|Chouchou rentre les doigts.
maman|On achète si tu demandes.
maman|Tu te souviens ?
enfant-f|Je peux demander.
maman|Tu me dis s'il te plaît ?
enfant-f|Oui, maman.
narrateur|Le pot de verre reste plein.
narrateur|Le rond de soleil a bougé.
        """),
        "CHK_T0000_P0000_Q0001": S("""
narrateur|Chouchou veut le crayon jaune.
narrateur|Que fait-elle ?
        """),
        "CHK_T0000_P0000_C0001": S("""
enfant-f|Maman, s'il te plaît.
enfant-f|Je peux avoir le crayon ?
maman|Oui.
maman|Merci, Chouchou.
maman|Tu as demandé.
narrateur|Maman ouvre le petit sac.
narrateur|Elle pose l'argent sur le bois.
narrateur|On lui tend le crayon jaune.
narrateur|Chouchou le prend.
narrateur|Le bois est hexagonal, un peu froid.
enfant-f|Il est à moi.
maman|Oui.
maman|Parce que tu as demandé.
maman|Tu le tiens bien ?
enfant-f|Oui, maman.
narrateur|Le pot de verre a un crayon en moins.
narrateur|Les autres crayons se touchent.
        """),
        "CHK_T0000_P0000_END": S("""
narrateur|Elles sortent.
narrateur|La rue sent le papier, encore un peu.
narrateur|Chouchou marche avec le crayon.
narrateur|La mine pointe vers le ciel.
maman|On dessinera à la maison ?
enfant-f|Oui.
enfant-f|Un soleil.
maman|Tu as demandé avant d'acheter.
maman|Bravo.
narrateur|Le crayon tape un peu sa poche.
narrateur|Chouchou le sent, tout près du nez.
narrateur|Ça sent le bois neuf.
maman|Tu le mets dans ta poche ?
enfant-f|Pas encore.
enfant-f|Il est jaune.
        """),
        "CHK_T0000_P0000_END_F0001": S("""
narrateur|À la table, Chouchou pose une feuille.
narrateur|Elle trace un trait jaune.
narrateur|Le trait est vif, tout droit.
enfant-f|C'est le soleil.
maman|Oui.
maman|Tu l'as dans les mains.
narrateur|Chouchou tient encore le crayon.
narrateur|Elle ajoute un petit rond.
enfant-f|Il chauffe.
maman|Le soleil, oui.
narrateur|Le crayon jaune laisse un trait sur le papier.
        """),
    },
    EMPTY,
    {
        "expected_answer": "demander",
        "accepted_examples": "demander | elle demande | à maman | s'il te plaît",
        "retry_prompt": "Elle demande à maman. Que fait Chouchou ?",
    },
)
relecture(
    "ATOM-SOC.ARG.002-06",
    "Le crayon jaune de Chouchou",
    "Papeterie, pot de verre, main sur le crayon, demande, trait jaune sur la feuille.",
    "Leçon greffée. Fin vécue.",
)


# ---------------------------------------------------------------------------
# ATOM-SOC.ARG.002-07 N3 Raphaël, papa — cahier bleu, puis gomme
# ---------------------------------------------------------------------------
write_story(
    "ATOM-SOC.ARG.002-07",
    "Raphaël veut un cahier bleu. Il tend la main. Papa attend. Il demande. Puis il demande une gomme. Les deux sont à lui.",
    "Le cahier bleu de Raphaël",
    "Raphaël, papa",
    "papeterie, piles de cahiers, bac à gommes",
    {
        "CHK_T0000_P0000": S("""
narrateur|Les cahiers bleus sentent l'encre froide.
narrateur|Ils sont empilés, bien droits.
narrateur|Le sol de bois craque un peu.
narrateur|Une pile de feuilles penche un peu.
narrateur|Papa pousse la porte.
narrateur|Une clochette fait un ding bas.
enfant-m|Les cahiers !
papa|Oui.
papa|On en prend un, pour dessiner.
narrateur|Raphaël passe près d'un bac à crayons.
narrateur|Les bouts pointent comme des toits.
papa|Tu as vu le bleu ?
enfant-m|Oui.
enfant-m|Il brille.
narrateur|Un cahier rouge est trop loin.
enfant-m|Le bleu, papa.
narrateur|En ce moment, Raphaël touche un cahier.
narrateur|La couverture est lisse, d'un bleu profond.
enfant-m|Celui-là.
enfant-m|Il est bleu.
narrateur|Raphaël tire le cahier de la pile.
narrateur|La pile penche un peu.
narrateur|Papa ne sort pas l'argent.
papa|Raphaël.
papa|Tu me demandes ?
narrateur|Le cahier reste dans ses mains, encore.
enfant-m|Oh.
narrateur|Il repose le cahier sur la pile.
papa|On achète si tu demandes.
papa|Tu te souviens ?
enfant-m|Je peux demander.
papa|Tu me dis s'il te plaît ?
enfant-m|Oui, papa.
narrateur|Le bleu attend sur le bois.
        """),
        "CHK_T0000_P0000_Q0001": S("""
narrateur|Raphaël veut le cahier bleu.
narrateur|Que fait-il ?
        """),
        "CHK_T0000_P0000_C0001": S("""
enfant-m|Papa, s'il te plaît.
enfant-m|Je peux avoir ce cahier ?
papa|Oui.
papa|Merci, Raphaël.
papa|Tu as demandé.
narrateur|Papa pose l'argent sur le comptoir.
narrateur|On lui tend le cahier bleu.
narrateur|Raphaël le serre sous le bras.
narrateur|Plus loin, un bac tient des gommes.
narrateur|Une gomme blanche a roulé au bord.
enfant-m|Papa.
enfant-m|La gomme aussi, s'il te plaît ?
papa|Tu demandes encore.
papa|Oui.
papa|On prend la gomme.
narrateur|Papa ajoute une pièce.
narrateur|Raphaël prend la gomme.
narrateur|Elle est souple, un peu rêche.
enfant-m|J'ai les deux.
papa|Parce que tu as demandé.
papa|Tu tiens bien tout ?
enfant-m|Oui, papa.
narrateur|Le bac à gommes a un trou blanc.
        """),
        "CHK_T0000_P0000_END": S("""
narrateur|Ils sortent.
narrateur|La clochette dingue derrière eux.
narrateur|Raphaël a le cahier sous le bras.
narrateur|La gomme est dans l'autre main.
papa|On dessinera à la maison ?
enfant-m|Oui.
enfant-m|Et je gommerai.
papa|Tu as demandé deux fois.
papa|Bravo.
narrateur|La rue sent encore le papier.
narrateur|Le cahier tape un peu sa hanche.
narrateur|La gomme reste chaude dans sa paume.
papa|Tu as les deux.
enfant-m|Le cahier et la gomme.
        """),
        "CHK_T0000_P0000_END_F0001": S("""
narrateur|À la table, Raphaël ouvre le cahier.
narrateur|La première page est blanche, un peu rêche.
narrateur|Il pose la gomme à côté.
enfant-m|Je peux dessiner.
papa|Oui.
papa|Tu as le cahier dans les mains.
narrateur|Raphaël pose la paume sur le bleu.
narrateur|Il trace un petit bateau, tout simple.
enfant-m|La voile est bleue.
papa|Comme le cahier.
narrateur|La gomme sent encore le caoutchouc neuf.
        """),
    },
    EMPTY,
    {
        "expected_answer": "demander",
        "accepted_examples": "demander | il demande | à papa | s'il te plaît",
        "retry_prompt": "Il demande à papa. Que fait Raphaël ?",
    },
)
relecture(
    "ATOM-SOC.ARG.002-07",
    "Le cahier bleu de Raphaël",
    "Papeterie, cahier tiré trop tôt, demande, puis gomme demandée, page blanche.",
    "Deux demandes vécues. Leçon greffée. Fin vécue.",
)
