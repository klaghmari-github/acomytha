# ATOM-EMO.GES.001-04 — Mila dit stop au salon

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N2 (≤15 mots/phrase), audio familial
- **Leçon :** EMO.GES.001 — trop fort → stop, reculer (vécue : Mila veut jouer **maintenant**, Chouchou serre trop, poitrine, sourire parti, papa accroupi ; elle dit stop, recule ; 2e ruse derrière le tissu). JAMAIS dite dans le récit. Pas « dire stop, c'est permis ». Pas « on s'éloigne ». Pas « on va vers un adulte ».
- **Personnages :** Mila, Chouchou, papa, maman. Dump Zélie/Lila/maman → D16. Mila = enfant-f (veut jouer maintenant, trop vite, puis stop et recule). Chouchou = copine (câlin trop fort, puis mains ouvertes). Troupe D16. Pas de maîtresse.
- **Lieu :** maison, salon, table, plaid, bois, fenêtre, rayon, savon, pli, cachette. ≠ 001-03 parc / toboggan / banc / sable. ≠ dump tapis / coussin / canapé / lampe / gouttière.
- **Indice unique :** éclat de plaid (brille à l'ouverture près du pli → tremble quand Chouchou trop fort → luit au refus derrière le tissu → tient sur le bois). BAN éclat de tapis / coussin / canapé / lampe / toboggan / balançoire / rideau.
- **Question moteur :** « C'est trop pour Mila. Que dit-elle ? » expected **stop**. accepted dump `stop | s'éloigner | maman | adulte | vers maman`. retry dump (Zélie → Mila). expected/accepted/retry des autres chunks restent **null**. Non récitée dans les autres chunks.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Le plaid rouge tient un pli sur la table. Près du pli, un éclat de plaid brille. Fil de laine, savon, rayon. Mila veut jouer **maintenant**. Chouchou ouvre les bras, serre trop. Sourire parti. Papa s'accroupit. Elle dit stop, recule. Merci vécu. Deuxième ruse : pli trop vite, visage caché, bras derrière le tissu. Elle s'arrête, lit l'éclat. Un éclat de plaid tient sur le bois.

## Arc dramatique

- Monde : maison, salon, table, plaid, bois, fenêtre, rayon, savon. ≠ dump tapis / coussin / canapé / lampe. ≠ parc / toboggan / balançoire / rideau.
- Désir : jouer maintenant, faire la cachette sous le plaid.
- Objet : plaid rouge, pli, table, cachette.
- Indice unique : éclat de plaid, vu dès l'ouverture près du pli, payé sur le bois. Pas éclat de tapis.
- Urgence douce : Mila accélère, Chouchou serre.
- Imprévu 1 : Chouchou ouvre les bras trop vite, serre. Poitrine coincée, sourire parti.
- Cue : papa à la même hauteur. Un merci vécu, après le geste.
- Imprévu 2 (plus rusé) : pli trop vite, visage caché, bras derrière le tissu.
- Résolution : elle dit stop, recule, observe, écoute, retrouve l'éclat, Chouchou tend les mains sans coller.
- Retour : pli de travers, savon, éclat sur le bois.

## Vécu

Mila veut jouer **maintenant**. Impatience, puis câlin trop fort, sourire parti. Chouchou pose sa limite (souffle, puis mains ouvertes). Papa se baisse, pose une question, ne récite pas la règle. Elles agissent : stop, reculer. Merci vécu. Fin : l'éclat du début tient sur le bois.

## Vu et corrigé

- Titre : Mila dit stop au salon (noyau + D16). Relance : Que dit-elle ? expected stop.
- Lieu du dump (salon, plaid) sans tapis / coussin / canapé / lampe / gouttière. Papa présent. Chouchou = copine.
- Ouverture inventée (pli du plaid sur la table), pas un gabarit v2, pas « La gouttière chante » du dump en première ligne.
- Indice unique : éclat de plaid. BAN éclat de tapis / coussin / canapé / lampe / toboggan / balançoire / rideau. Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés. Strip « Le.. » / « encore » / « cabane de coussins » du dump. Une phrase par ligne, ponctuation, pas de puces.
- Leçon non dite : on la voit quand Mila dit stop, recule, quand Chouchou ouvre les mains. Pas « dire stop, c'est permis ». Pas « on s'éloigne » hors question.
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur : « C'est trop pour Mila. Que dit-elle ? ». expected stop. retry dump (Mila). 5 chunks, kinds inchangés. expected/accepted/retry null hors Q.
- example4 041 / 073 / 005 (manière volée, gabarit non collé). Voix : `_write_atom_dif_par_002_03.py`.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action plus vive vers le pli.
- 759 mots. N2 ≤ 15. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 759 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
