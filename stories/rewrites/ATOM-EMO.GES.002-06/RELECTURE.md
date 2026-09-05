# ATOM-EMO.GES.002-06 — Mila souffle et fait une pause

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N3 (≤16 mots/phrase), audio familial
- **Leçon :** EMO.GES.002 — corps trop vite → souffler, pause (vécue : Mila veut la tour **maintenant**, cubes glissent, épaules serrées, sourire parti, maman accroupie ; elle souffle, reste ; 2e ruse derrière l'étagère). JAMAIS dite dans le récit. Pas « on peut souffler ». Pas « on peut faire une pause ». Pas « tu as soufflé ».
- **Personnages :** Mila, papa, maman. Dump Flore/Sarah/maman → D16. Mila = enfant-f (veut la tour maintenant, trop vite, puis souffle et reste). Troupe D16. Pas de copine. Pas de maîtresse.
- **Lieu :** maison, chambre, étagère, bois, fenêtre, rayon, cire, panier, cubes, tour. ≠ 002-05 rideau / doudou / oreiller / tapis. ≠ dump lampe / chaussettes / radiateur / puzzle.
- **Indice unique :** éclat d'étagère (brille à l'ouverture près du bord → tremble quand la tour tombe → luit au refus derrière l'étagère → tient sur le bois). BAN éclat de tour / lit / pot / rouleau / comptoir / cube.
- **Question moteur :** « La tour de Mila tombe. Que fait-elle ? » expected dump **souffler**. accepted dump `souffler | une pause | s'asseoir | pause`. retry dump (Flore → Mila). expected/accepted/retry des autres chunks restent **null**. Non récitée dans les autres chunks.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Le bois de l'étagère sent la cire. Près du bord, un éclat d'étagère brille. Fil de poussière, rayon, panier. Mila veut la tour **maintenant**. Cubes trop vite, trop haut. La tour tombe. Sourire parti. Maman s'accroupit. Elle souffle, reste. Merci vécu. Deuxième ruse : cube derrière l'étagère, trop vite, tour qui tremble. Elle s'arrête, lit l'éclat. Un éclat d'étagère tient sur le bois.

## Arc dramatique

- Monde : maison, chambre, étagère, bois, fenêtre, rayon, cire. ≠ dump lampe / tapis / chaussettes / radiateur. ≠ 002-05 rideau / doudou / oreiller.
- Désir : la tour, maintenant, avec les cubes du panier.
- Objet : cubes, tour, étagère, panier.
- Indice unique : éclat d'étagère, vu dès l'ouverture près du bord, payé sur le bois. Pas éclat de cube / tour / lit.
- Urgence douce : Mila accélère, pose trop haut.
- Imprévu 1 : les cubes glissent, la tour tombe. Poitrine coincée, sourire parti, épaules serrées.
- Cue : maman à la même hauteur. Un merci vécu, après le geste.
- Imprévu 2 (plus rusé) : cube trop vite, derrière l'étagère, tour qui tremble.
- Résolution : elle s'assoit, souffle, reste, observe, écoute, retrouve l'éclat, pose sans se presser.
- Retour : tour de travers, cire, éclat sur le bois.

## Vécu

Mila veut la tour **maintenant**. Impatience, puis chute, sourire parti. Maman se baisse, pose une question, ne récite pas la règle. Mila agit : s'asseoir, souffler, rester. Merci vécu. Fin : l'éclat du début tient sur le bois.

## Vu et corrigé

- Titre : Mila souffle et fait une pause (noyau + D16). Relance : Que fait-elle ? expected souffler.
- Lieu du dump (chambre, tour de cubes) sans tapis / lampe / chaussettes / radiateur / puzzle. Papa et maman présents.
- Ouverture inventée (cire du bois de l'étagère), pas un gabarit v2, pas « Le soir, la lampe ronde » du dump en première ligne.
- Indice unique : éclat d'étagère. BAN éclat de tour / lit / pot / rouleau / comptoir / cube. Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés. Strip dump « On peut souffler » / « Bravo » / puzzle. Une phrase par ligne, ponctuation, pas de puces.
- Leçon non dite : on la voit quand Mila s'assoit, souffle, reste. Pas « on peut souffler ». Pas « tu as fait une pause ».
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur : « La tour de Mila tombe. Que fait-elle ? ». expected dump souffler. retry dump (Mila). 5 chunks, kinds inchangés. expected/accepted/retry null hors Q.
- example4 051 / 083 / 015 (manière volée, gabarit non collé). Voix : `_write_atom_emo_ges_001_04.py`.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action plus vive vers l'étagère.
- 732 mots. N3 ≤ 16. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 732 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
