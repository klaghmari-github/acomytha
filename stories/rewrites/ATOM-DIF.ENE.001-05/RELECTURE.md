# ATOM-DIF.ENE.001-05 — Le seau de la sauge

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N1 (≤10 mots/phrase), audio familial, voc 3–4 ans
- **Leçon :** DIF.ENE.001 — Aniss a de l'énergie (vécue : il saute trop, eau partout, seau passé, il veut verser tout, elle refuse de foncer). JAMAIS dite dans le récit. Pas « ce n'est pas une faute ». Pas « on peut jouer / attendre / demander ».
- **Personnages :** Mila, Aniss, papa, maman. Mila = enfant-f (veut le seau maintenant). Aniss = copain (saute, attends, souffle, veut verser tout). Troupe D16. Pas de maîtresse. Plus Tania / Ulysse.
- **Lieu :** jardin, sauge, goutte froide, terre, caisse, seau rouge, bac d'eau, linge. ≠ 001-01 flaque, ≠ 001-02 piquet, ≠ 001-03 bol, ≠ 001-04 chiffon.
- **Indice unique :** éclat de sauge (brille à l'ouverture → tremble à l'eau partout → luit quand il veut verser tout → tient sur la feuille). BAN éclat de caisse / flaque / piquet / bol / chiffon.
- **Question moteur :** « Aniss a de l'énergie. Que peut-on faire ? » expected **jouer**. accepted `jouer | attendre | un adulte | demander`. retry dump (label, pas leçon récitée). Non récitée dans les autres chunks.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Une goutte froide tient sur la sauge. Sur la feuille, un éclat de sauge brille. Mila veut le seau **maintenant**. Aniss saute trop. L'eau part partout. Sourire parti. Papa s'accroupit. Elle refuse de foncer. Ils se passent le seau. Merci vécu. Deuxième ruse : il veut verser tout, la sauge se couche. Elle s'arrête, lit l'éclat. Un éclat de sauge tient sur la feuille.

## Arc dramatique

- Monde : jardin, sauge, goutte froide, terre, caisse, seau rouge, bac, linge. ≠ 001-01 flaque, ≠ 001-02 piquet, ≠ 001-03 bol, ≠ 001-04 chiffon.
- Désir : le seau, maintenant, pour la sauge.
- Objet : seau rouge près du bac, puis l'eau trop vite.
- Indice unique : éclat de sauge, vu dès l'ouverture, payé sur la feuille. Pas éclat de caisse / flaque / piquet / bol / chiffon.
- Urgence douce : Aniss arrive, saute trop, le seau attend.
- Imprévu 1 : elle prend trop vite, il saute contre, eau partout, chaussures mouillées.
- Cue : papa à la même hauteur. Un merci vécu, après « d'accord ».
- Imprévu 2 (plus rusé) : il lève trop haut, veut verser tout, la sauge se couche.
- Résolution : elle refuse de foncer, observe, écoute le linge, retrouve l'éclat, Aniss souffle et baisse le seau.
- Retour : goutte à goutte, seau à l'envers, éclat sur la feuille. La fin a failli (la sauge s'est couchée).

## Vécu

Mila veut le seau **maintenant**. Impatience, puis eau partout, sourire parti. Aniss prend son élan, pose sa limite (attends, souffle). Papa se baisse, pose une question, ne récite pas la règle. Ils agissent : anse tenue, seau passé, verser un peu. Merci vécu. Fin : l'éclat du début tient sur la feuille.

## Vu et corrigé

- Titre : Le seau de la sauge (noyau dump). Relance : Que peut-on faire ? expected jouer.
- Lieu du dump (jardin, terre mouillée). Maman et papa. Aniss = copain. Mila = enfant-f.
- Ouverture inventée (goutte froide sur la sauge), pas « Mila est au jardin », pas le ver de terre du dump.
- Indice unique : éclat de sauge (goutte sur la feuille). BAN éclat de caisse / flaque / piquet / bol / chiffon. Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés. Strip « encore » / « tout doucement » du dump.
- Leçon non dite : on la voit quand Aniss saute, quand l'eau part, quand elle s'arrête, quand le seau passe. Pas « ce n'est pas une faute ». Pas « on peut jouer / attendre / demander » hors retry moteur.
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur inchangée : « Aniss a de l'énergie. Que peut-on faire ? ». expected jouer. retry dump. 5 chunks, kinds inchangés.
- example4 019 / 051 / 083 (manière volée, gabarit non collé). Voix : `_write_atom_dif_cor_003_04.py` / `_write_atom_dif_ene_001_02.py`, profiles N1 plus lents.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action un peu plus vive vers le seau trop haut.
- 769 mots. N1 ≤ 10. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 769 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
