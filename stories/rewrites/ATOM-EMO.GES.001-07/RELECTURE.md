# ATOM-EMO.GES.001-07 — Nino dit stop et s'éloigne

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N1 (≤10 mots/phrase), audio familial, voc 3–4 ans
- **Leçon :** EMO.GES.001 — trop fort → stop, reculer (vécue : Aniss serre trop, poitrine coincée, Nino dit stop, recule d'un pas ; 2e ruse : le caillou glisse, Aniss serre pour aider, Nino dit stop, recule). JAMAIS dite. Pas « dire stop, c'est permis ». Pas « on s'éloigne ».
- **Personnages :** Nino, Aniss, papa, maman. Dump Florian/Chouchou/papa → D16 Nino = enfant-m (veut jouer maintenant). Aniss = copain (serre trop, Viens, Loin). Troupe D16. Pas de maîtresse.
- **Lieu :** cour de récréation, marelle, craie, cases, poussière, soleil, caillou. ≠ 001-01 balançoire. ≠ 001-03 toboggan. ≠ 001-04 plaid. ≠ 001-05 livre. ≠ 001-06 cadre. BAN cour/grille/banc dans le texte.
- **Indice unique :** éclat de marelle (luit à l'ouverture → tremble au câlin trop fort → luit quand le caillou glisse → tient sur la case). BAN éclat de cour / grille / banc / cadre / livre / plaid / toboggan / balançoire.
- **Question moteur :** « C'est trop pour Nino. Que dit-il ? » expected / accepted / retry **null** (consigne). Non récitée dans les autres chunks.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Un trait rose s'étire sur le sol chaud. Sur une case, un éclat de marelle luit. Craie, caillou, cases. Nino veut jouer **maintenant**. Aniss ouvre les bras, serre trop. Sourire parti. Papa s'accroupit. Stop, recule. Merci vécu. Deuxième ruse : le caillou glisse. Aniss serre pour aider. Nino dit stop, recule, lit l'éclat. Un éclat de marelle tient sur la case.

## Arc dramatique

- Monde : cour de récréation, marelle, craie, cases, poussière, soleil, caillou. ≠ 001-01 balançoire. ≠ 001-03 toboggan. ≠ 001-04 plaid.
- Désir : jouer à la marelle, maintenant.
- Objet : caillou plat, puis craie rose.
- Indice unique : éclat de marelle, vu dès l'ouverture, payé sur la case. Pas éclat de cour / grille / banc / cadre / livre / plaid / toboggan / balançoire.
- Urgence douce : le caillou est lancé, Aniss veut y aller aussi, tout de suite.
- Imprévu 1 : Aniss serre trop, poitrine coincée, sourire parti.
- Cue : papa à la même hauteur. Un merci vécu, après « un peu loin ».
- Imprévu 2 (plus rusé) : craie rose, le caillou glisse, Aniss attrape les épaules pour aider.
- Résolution : Nino dit stop, recule d'un pas, observe, écoute le vent, retrouve l'éclat, Aniss dit « il glisse ».
- Retour : trait rose, caillou sur une case, éclat qui tient.

## Vécu

Nino veut jouer **maintenant**. Impatience, puis bras trop forts, sourire parti. Aniss est chaleureux, trop près (Viens, Loin, souffle). Papa se baisse, pose une question, ne récite pas la règle. Ils agissent : stop, un pas, cases sautées avec de l'air. Merci vécu. Fin : l'éclat du début tient sur la case.

## Vu et corrigé

- Titre : Nino dit stop et s'éloigne (noyau « dit stop et s'éloigne », prénom D16). Relance : Que dit-il ? expected null.
- Lieu : cour de récréation (marelle). Maman et papa. Aniss = copain. Nino = héros. Dump Florian/Chouchou du json remappé : Florian→Nino, Chouchou→Aniss.
- Ouverture inventée (trait rose sur le sol chaud), pas un gabarit v2, pas « Les pierres de la cour sont froides » du dump.
- Indice unique : éclat de marelle (récré). BAN éclat de cour / grille / banc (BAN) / cadre (001-06) / livre (001-05) / plaid (001-04) / toboggan (001-03) / balançoire (001-01). Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés. Strip « encore » / « tout doucement » du dump.
- Leçon non dite : on la voit quand Aniss serre, quand Nino dit stop, quand il recule, quand le caillou glisse. Pas « dire stop, c'est permis ». Pas « on s'éloigne ».
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur : « C'est trop pour Nino. Que dit-il ? ». expected/accepted/retry null. 5 chunks, kinds inchangés.
- example4 044 / 076 / 008 (manière volée, gabarit non collé). Voix : `_write_atom_dif_par_002_05.py`, profiles N1 lents.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action un peu plus vive vers le caillou qui glisse.
- 794 mots. N1 ≤ 10. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 794 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
