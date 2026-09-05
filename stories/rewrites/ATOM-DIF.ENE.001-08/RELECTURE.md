# ATOM-DIF.ENE.001-08 — Le ruban rouge

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N3 (≤16 mots/phrase), audio familial
- **Leçon :** DIF.ENE.001 — l'énergie de Sarah (vécue : elle saute trop, le ruban s'enroule, Aniss refuse de foncer, attend, demande, passe le ruban sans se presser). JAMAIS dite dans le récit. Pas « ce n'est pas une faute ». Pas « on peut jouer / attendre / demander ».
- **Personnages :** Aniss, Sarah, papa, maman. Aniss = enfant-m (propose, trop vite, puis refuse de foncer). Sarah = enfant-f (énergie, saute, attends, silence). Troupe D16. Pas de maîtresse. Bruno / Noé du dump remplacés.
- **Lieu :** salon, radio sur la commode, chanson, ruban rouge, linge, clic du bois. ≠ 001-01 flaque / 001-02 piquet / 001-03 bol. ≠ 001-04 chiffon / 001-05 sauge / 001-06 lacet / 001-07 tapis. Pas poussière, pas chaise.
- **Indice unique :** éclat de commode (brille à l'ouverture sous la radio → tremble au pied → luit au refus → tient sur le bois). BAN éclat de ruban / radio / bouton / chaise / poussière / tapis / lacet / sauge / chiffon / bol / flaque / piquet.
- **Question moteur :** « Sarah a de l'énergie. Que peut-on faire ? » expected **jouer**. accepted `jouer | attendre | un adulte | demander`. retry dump (label). Non récitée dans les autres chunks.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Le bois de la commode fait clic, sous la radio. Sur le bois, un éclat de commode brille. Ruban rouge, chanson, linge. Aniss veut un grand rond **maintenant**, pendant la chanson. Sarah saute trop, le ruban s'enroule au pied, la radio penche. Sourire parti. Papa s'accroupit. Il refuse de foncer. Ils passent le ruban, puis tournent. Merci vécu. Deuxième ruse : clic, ruban trop vite vers la radio. Il s'arrête, lit l'éclat. Un éclat de commode tient sur le bois.

## Arc dramatique

- Monde : salon, radio sur la commode, chanson, ruban rouge, linge, clic du bois. ≠ 001-01 flaque / 001-02 piquet / 001-03 bol. Pas poussière / chaise.
- Désir : un grand rond lent, maintenant, pendant la chanson.
- Objet : ruban rouge, radio, commode.
- Indice unique : éclat de commode, vu dès l'ouverture, payé sur le bois. Pas éclat de ruban / radio / chaise / poussière.
- Urgence douce : la chanson joue, le rond doit tenir pendant.
- Imprévu 1 : Sarah saute trop, tourne trop vite, le ruban s'enroule au pied, la radio penche.
- Cue : papa à la même hauteur. Un merci vécu, après « d'accord ».
- Imprévu 2 (plus rusé) : clic, ruban trop vite, il penche vers la radio.
- Résolution : il refuse de foncer, observe, écoute le clic, retrouve l'éclat, Sarah tend les mains.
- Retour : ruban près de la radio, chanson arrêtée, éclat sur le bois.

## Vécu

Aniss veut le rond **maintenant**. Impatience, puis ruban enroulé, sourire parti. Sarah prend son élan, pose sa limite (attends, silence). Papa se baisse, pose une question, ne récite pas la règle. Ils agissent : le ruban passé, puis le rond lent. Merci vécu. Fin : l'éclat du début tient sur le bois.

## Vu et corrigé

- Titre : Le ruban rouge (noyau dump « Le ruban dans le rayon », sans poussière / chaise). Relance : Que peut-on faire ? expected jouer.
- Lieu du dump (salon, radio, musique) sans rayon de poussière ni chaise. Radio sur la commode. Maman présente. Sarah = enfant-f.
- Ouverture inventée (clic du bois sous la radio), pas un gabarit v2, pas « La radio craque, puis trouve une chanson » du dump en première ligne.
- Indice unique : éclat de commode. BAN éclat de ruban / radio / bouton / chaise / poussière / tapis / lacet / sauge / chiffon / bol / flaque / piquet. Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés. Strip « tout bas » / « encore » du dump.
- Leçon non dite : on la voit quand le ruban s'enroule, quand Aniss s'arrête, quand ils passent à tour. Pas « ce n'est pas une faute ». Pas « on peut jouer / attendre / demander » hors retry label.
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur inchangée : « Sarah a de l'énergie. Que peut-on faire ? ». expected jouer. retry dump. 5 chunks, kinds inchangés.
- example4 022 / 054 / 086 (manière volée, gabarit non collé). Voix : `_write_atom_dif_ene_001_03.py`.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action plus vive vers le ruban trop vite.
- 786 mots. N3 ≤ 16. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 786 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
