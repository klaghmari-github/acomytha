# ATOM-EMO.GES.001-08 — Raphaël dit stop et s'éloigne

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N1 (≤10 mots/phrase), audio familial, voc 3–4 ans
- **Leçon :** EMO.GES.001 — trop (chatouille) → dire stop, reculer (vécue : Victorino chatouille trop, ventre trop vite, Raphaël dit stop, recule, Victorino trop près du ventre, Raphaël refuse de foncer). JAMAIS dite dans le récit. Pas « il peut s'éloigner ». Pas « c'est trop » en refrain adulte. Pas « dire stop, c'est permis ».
- **Personnages :** Raphaël, Victorino, papa, maman. Dump Hippolyte/papa → D16 Raphaël = enfant-m (veut jouer maintenant). Victorino = copain (chatouille trop, souffle, recule). Troupe D16. Pas de maîtresse.
- **Lieu :** salon, plinthe, toupie rouge, sol, fenêtre, bois, cire, trait d'or. BAN tapis / canapé / coussin. ≠ 001-01 balançoire. ≠ 001-02 rideau. ≠ 001-03 toboggan. ≠ 001-04 plaid. ≠ 001-05 livre. ≠ 001-06 cadre. ≠ 001-07 marelle.
- **Indice unique :** éclat de plinthe (luit à l'ouverture → tremble aux chatouilles → luit quand Victorino se colle → tient sur le bois). BAN éclat de tapis / canapé / coussin / marelle / cadre / livre / plaid / rideau / toboggan / balançoire.
- **Question moteur :** « C'est trop pour Raphaël. Que dit-il ? » expected **stop**. accepted dump `stop | s'éloigner | papa | adulte | vers papa`. retry dump Hippolyte → Raphaël. Non récitée dans les autres chunks.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Un trait d'or file le long du bois. Toc toc. Sur le bois, un éclat de plinthe luit. Cire, toupie rouge, sol du salon. Raphaël veut jouer **maintenant**. Victorino chatouille trop. Ventre trop vite. Sourire parti. Papa s'accroupit. Raphaël dit stop, recule d'un pas. Merci vécu. Deuxième ruse : Victorino chatouille trop près du ventre. La toupie penche. Il s'arrête, lit l'éclat. Un éclat de plinthe tient sur le bois.

## Arc dramatique

- Monde : salon, plinthe, toupie, sol, fenêtre, cire, trait d'or. BAN tapis / canapé / coussin.
- Désir : faire tourner la toupie, maintenant.
- Objet : toupie rouge, puis toupie qui penche.
- Indice unique : éclat de plinthe, vu dès l'ouverture, payé sur le bois. Pas éclat de tapis / canapé / coussin.
- Urgence douce : Victorino arrive, avance les doigts trop vite.
- Imprévu 1 : chatouilles trop longues, ventre trop vite, sourire parti.
- Cue : papa à la même hauteur. Un merci vécu, après « d'accord ».
- Imprévu 2 (plus rusé) : toupie tendue, Victorino chatouille, la toupie penche.
- Résolution : il refuse de foncer, observe, écoute le bois, retrouve l'éclat, dit stop, recule.
- Retour : vzz à un pas, toupie près du sol, éclat sur le bois.

## Vécu

Raphaël veut jouer **maintenant**. Impatience, puis chatouilles trop longues, sourire parti. Victorino prend son élan, pose sa limite (je m'arrête, souffle, recule). Papa se baisse, pose une question, ne récite pas la règle. Ils agissent : un pas plus loin, lancée sans se presser, toupie rendue. Merci vécu. Fin : l'éclat du début tient sur le bois.

## Vu et corrigé

- Titre : Raphaël dit stop et s'éloigne (noyau dit stop et s'éloigne, prénom D16). Relance : Que dit-il ? expected stop.
- Lieu du dump-meta (salon). Maman et papa. Victorino = copain. Raphaël = héros. BAN tapis / canapé / coussin (dump canapé écarté).
- Ouverture inventée (trait d'or, bois, cire), pas un gabarit v2, pas canapé/coussins/orange du source, pas « Hippolyte joue au salon ».
- Indice unique : éclat de plinthe. BAN éclat de tapis / canapé / coussin / marelle / cadre / livre / plaid / rideau / toboggan / balançoire. Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés. Strip « tout bas » / « encore » du dump.
- Leçon non dite : on la voit quand Victorino chatouille, quand le ventre va trop vite, quand Raphaël dit stop, quand il recule. Pas « il peut s'éloigner ». Pas « c'est trop » en refrain adulte. Pas « dire stop, c'est permis ».
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur : « C'est trop pour Raphaël. Que dit-il ? ». expected stop. dump accepted. retry Hippolyte → Raphaël. 5 chunks, kinds inchangés.
- example4 045 / 077 / 009 (manière volée, gabarit non collé). Voix : `_write_atom_dif_par_002_07.py`, profiles N1.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action un peu plus vive vers la toupie qui penche.
- 778 mots. N1 ≤ 10. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 778 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
