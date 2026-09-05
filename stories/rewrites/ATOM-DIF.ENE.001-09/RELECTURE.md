# ATOM-DIF.ENE.001-09 — Le ballon jaune de la cour

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N1 (≤10 mots/phrase), audio familial, voc 3–4 ans
- **Leçon :** DIF.ENE.001 — Aniss a de l'énergie (vécue : il court trop, ballon contre le bois, ballon sous le portail, Raphaël refuse de foncer, ils se passent le ballon). JAMAIS dite dans le récit. Pas « ce n'est pas une faute ». Pas « on peut jouer / on peut attendre ».
- **Personnages :** Raphaël, Aniss, papa, maman. Dump Amélie/Loïc → D16 Raphaël = enfant-m (veut le ballon maintenant). Aniss = copain (court, saute, attends, souffle). Troupe D16. Pas de maîtresse.
- **Lieu :** cour, portail de bois, gond, lattes, poussière chaude, mouche, caisse, ballon jaune. ≠ 001-01 cour/flaques. ≠ 001-02 jardin/linge. ≠ COR.003-07 portail de fer.
- **Indice unique :** éclat de gond (luit à l'ouverture → tremble au ballon → luit sous le portail → tient sur le bois). BAN éclat de portail / feuille / cour / pierre / commode / lacet / tapis / sauge.
- **Question moteur :** « Aniss a de l'énergie. Que fait Raphaël ? » expected **jouer**. accepted `jouer | attendre | maman | un adulte | papa | demander`. retry dump adapté. Non récitée dans les autres chunks.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Le bois du portail sent le soleil. Toc toc. Sur le gond, un éclat de gond luit. Mouche, poussière chaude. Raphaël veut le ballon **maintenant**. Aniss court trop. Le ballon tape le bois. Sourire parti. Papa s'accroupit. Il refuse de foncer. Ils tiennent le bord. Merci vécu. Deuxième ruse : le ballon sous le portail. Il s'arrête, lit l'éclat. Un éclat de gond tient sur le bois.

## Arc dramatique

- Monde : cour, portail de bois, gond, lattes, poussière, mouche. ≠ 001-01 flaques. ≠ 001-02 linge. ≠ 003-07 fer.
- Désir : le ballon jaune, maintenant.
- Objet : ballon jaune, puis ballon sous le portail.
- Indice unique : éclat de gond, vu dès l'ouverture, payé sur le bois. Pas éclat de portail / feuille / cour / pierre.
- Urgence douce : Aniss arrive, court trop, le ballon attend.
- Imprévu 1 : poussée trop vite, Aniss dessus, ballon contre le bois.
- Cue : papa à la même hauteur. Un merci vécu, après « d'accord ».
- Imprévu 2 (plus rusé) : caisse, Aniss court, le portail avale le ballon.
- Résolution : il refuse de foncer, observe, écoute le gond, retrouve l'éclat, Aniss tend les mains.
- Retour : poumf tout près, ballon près du mur, éclat sur le bois.

## Vécu

Raphaël veut le ballon **maintenant**. Impatience, puis ballon contre le bois, sourire parti. Aniss prend son élan, pose sa limite (attends, souffle). Papa se baisse, pose une question, ne récite pas la règle. Ils agissent : bord tenu, poussée sans se presser, ballon rendu. Merci vécu. Fin : l'éclat du début tient sur le bois.

## Vu et corrigé

- Titre : Le ballon jaune de la cour (noyau dump). Relance : Que fait Raphaël ? expected jouer.
- Lieu du dump-meta (cour, portail). Maman et papa. Aniss = copain. Raphaël = héros.
- Ouverture inventée (bois du portail, soleil, gond), pas un gabarit v2, pas cuisine/raisins du source, pas « Amélie est dans la cour ».
- Indice unique : éclat de gond (portail de bois). BAN éclat de portail (003-07) / feuille / cour / pierre / commode / lacet / tapis / sauge. Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés. Strip « encore » du dump.
- Leçon non dite : on la voit quand Aniss court, quand le ballon tape le bois, quand il s'arrête, quand le ballon revient. Pas « ce n'est pas une faute ». Pas « on peut jouer / on peut attendre » hors retry moteur.
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur : « Aniss a de l'énergie. Que fait Raphaël ? ». expected jouer. 5 chunks, kinds inchangés.
- example4 023 / 055 / 087 (manière volée, gabarit non collé). Voix : `_write_atom_dif_ene_001_02.py`, profiles N1.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action un peu plus vive vers le ballon sous le portail.
- 761 mots. N1 ≤ 10. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 761 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
