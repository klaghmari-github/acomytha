# ATOM-EMO.GES.002-04 — Sarah souffle et fait une pause

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N2 (≤15 mots/phrase), audio familial
- **Leçon :** EMO.GES.002 — corps trop vite → souffler, pause (vécue : Sarah veut coller **maintenant**, forme cassée, poitrine trop vite, sourire parti, papa accroupi ; elle souffle, fait une pause ; 2e ruse : le cœur se plie sous le rouleau). JAMAIS dite dans le récit. Pas « on peut souffler ». Pas « tu as fait une pause ». Pas « souffler, puis une pause ».
- **Personnages :** Sarah, papa, maman. Dump Paloma/papa → D16. Sarah = enfant-f (veut coller maintenant, trop vite, puis souffle et fait une pause). Troupe D16. Pas de maîtresse. Pas de copain.
- **Lieu :** cuisine, table, pâte, rouleau, bois, fenêtre, rayon, beurre, moule, formes. ≠ 002-01 tour / cubes. ≠ 002-02 comptoir / pain. ≠ 002-03 pot / jardin. ≠ dump farine.
- **Indice unique :** éclat de rouleau (brille à l'ouverture près du bois → tremble quand la forme casse → luit au refus sous le cœur plié → tient sur le bois). BAN éclat de pot / tour / comptoir / farine.
- **Question moteur :** « Le corps de Sarah va vite. Que fait-elle ? » expected dump **souffler**. accepted dump `souffler | pause | une pause | s'asseoir | respirer`. retry dump (Paloma → Sarah). expected/accepted/retry des autres chunks restent **null**. Non récitée dans les autres chunks.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Le bois du rouleau luit près de la fenêtre. Près du bois, un éclat de rouleau brille. Fil de pâte, beurre, rayon. Sarah veut coller **maintenant**. Elle appuie trop fort. Forme cassée. Sourire parti. Papa s'accroupit. Elle souffle, fait une pause. Merci vécu. Deuxième ruse : cœur trop vite, forme pliée sous le rouleau. Elle s'arrête, lit l'éclat. Un éclat de rouleau tient sur le bois.

## Arc dramatique

- Monde : cuisine, table, pâte, rouleau, bois, fenêtre, rayon, beurre. ≠ dump farine. ≠ pot / tour / comptoir.
- Désir : coller maintenant, une étoile dans la pâte.
- Objet : pâte, rouleau, moule, formes, plaque.
- Indice unique : éclat de rouleau, vu dès l'ouverture près du bois, payé sur le bois. Pas éclat de farine.
- Urgence douce : Sarah accélère, appuie trop.
- Imprévu 1 : le moule déchire la pâte. Poitrine trop vite, sourire parti.
- Cue : papa à la même hauteur. Un merci vécu, après le geste.
- Imprévu 2 (plus rusé) : cœur trop vite, forme pliée sous le rouleau.
- Résolution : elle souffle, fait une pause, observe, écoute, retrouve l'éclat, reprend sans se presser.
- Retour : forme de travers, beurre, éclat sur le bois.

## Vécu

Sarah veut coller **maintenant**. Impatience, puis forme cassée, sourire parti. Papa se baisse, pose une question, ne récite pas la règle. Elle agit : souffle, pause. Merci vécu. Fin : l'éclat du début tient sur le bois.

## Vu et corrigé

- Titre : Sarah souffle et fait une pause (noyau + D16). Relance : Que fait-elle ? expected souffler.
- Lieu du dump (cuisine, pâte, formes) sans farine / pot / tour / comptoir. Papa et maman présents.
- Ouverture inventée (bois du rouleau près de la fenêtre), pas un gabarit v2, pas « Dans la cuisine, un rayon traverse la farine » du dump en première ligne.
- Indice unique : éclat de rouleau. BAN éclat de pot / tour / comptoir / farine. Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés. Strip farine / « On peut souffler » / « Bravo » du dump. Une phrase par ligne, ponctuation, pas de puces.
- Leçon non dite : on la voit quand Sarah souffle, fait une pause. Pas « on peut souffler ». Pas « tu as fait une pause ».
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur : « Le corps de Sarah va vite. Que fait-elle ? ». expected souffler. retry dump (Sarah). 5 chunks, kinds inchangés. expected/accepted/retry null hors Q.
- example4 049 / 081 / 013 (manière volée, gabarit non collé). Voix : `_write_atom_emo_ges_001_04.py`.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action plus vive vers le cœur plié.
- 773 mots. N2 ≤ 15. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 773 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
