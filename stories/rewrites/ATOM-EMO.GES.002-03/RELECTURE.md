# ATOM-EMO.GES.002-03 — Victorino souffle au jardin

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N2 (≤15 mots/phrase), audio familial
- **Leçon :** EMO.GES.002 — corps trop vite → souffler, pause (vécue : Victorino veut le château **maintenant**, s'effondre, poitrine trop vite, sourire parti, papa accroupi ; il souffle, pause ; 2e ruse pot trop vite). JAMAIS dite dans le récit. Pas « tu peux souffler ». Pas « tu peux faire une pause ». Pas « bravo, tu as soufflé ».
- **Personnages :** Victorino, papa, maman. Dump William/papa → D16 Victorino (héros enfant-m) + papa/maman. Troupe D16. Pas de maîtresse. Pas de copain.
- **Lieu :** jardin, château de terre, pots, terre, bord, soleil, ombre, poussière, fourmi, basilic. ≠ 002-01 tour / cubes. ≠ 002-02 comptoir / pain. ≠ PAR.001-07 rambarde / paillasson / pelle. ≠ dump arrosoir / linge / planche.
- **Indice unique :** éclat de pot (brille à l'ouverture près du bord fêlé → tremble à l'effondrement → luit au refus du second tas → tient sur la terre). BAN éclat de tour / comptoir / rambarde.
- **Question moteur :** « Le corps de Victorino va vite. Que fait-il ? » expected dump **souffler**. accepted dump `souffler | pause | une pause | s'asseoir | respirer`. retry dump (William → Victorino). expected/accepted/retry des autres chunks restent **null**. Non récitée dans les autres chunks.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Les pots tièdes font une ombre étroite. Près du bord, un éclat de pot brille. Fourmi, basilic, poussière, terre chaude. Victorino veut le château **maintenant**. Il presse trop vite. Le château s'effondre. Sourire parti. Papa s'accroupit. Il souffle, fait une pause. Merci vécu. Deuxième ruse : toit trop vite, pot qui penche, terre qui glisse. Il s'arrête, lit l'éclat. Un éclat de pot tient sur la terre.

## Arc dramatique

- Monde : jardin, pots, terre, bord fêlé, soleil, ombre, fourmi, basilic. ≠ dump arrosoir / linge / planche. ≠ rambarde / pelle / paillasson.
- Désir : le château de terre, maintenant.
- Objet : pots, terre, château, bord.
- Indice unique : éclat de pot, vu dès l'ouverture près du bord, payé sur la terre. Pas éclat de tour / comptoir / rambarde.
- Urgence douce : Victorino accélère, presse trop.
- Imprévu 1 : château trop vite, s'effondre. Poitrine trop vite, sourire parti.
- Cue : papa à la même hauteur. Un merci vécu, après le geste.
- Imprévu 2 (plus rusé) : toit trop vite, pot penche, terre glisse.
- Résolution : il s'assoit, souffle, fait une pause, observe, écoute, retrouve l'éclat, reprend sans presser.
- Retour : mur de travers, basilic, éclat sur la terre.

## Vécu

Victorino veut le château **maintenant**. Impatience, puis effondrement, sourire parti. Papa se baisse, pose une question, ne récite pas la règle. Victorino agit : souffler, pause. Merci vécu. Fin : l'éclat du début tient sur la terre.

## Vu et corrigé

- Titre : Victorino souffle au jardin (noyau + D16). Relance : Que fait-il ? expected souffler.
- Lieu du dump (jardin, château, pots) sans arrosoir / linge / planche / rambarde. Papa et maman présents. Victorino = enfant-m.
- Ouverture inventée (pots tièdes, ombre étroite), pas un gabarit v2, pas « L'arrosoir penche encore » du dump en première ligne.
- Indice unique : éclat de pot. BAN éclat de tour / comptoir / rambarde. Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés. Strip dump « tout doux » / « bravo » / « tu peux souffler ». Une phrase par ligne, ponctuation, pas de puces.
- Leçon non dite : on la voit quand Victorino souffle, s'assoit, fait une pause. Pas « tu peux souffler ». Pas « tu as fait une pause ».
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur : « Le corps de Victorino va vite. Que fait-il ? ». expected souffler. retry dump (Victorino). 5 chunks, kinds inchangés. expected/accepted/retry null hors Q.
- example4 048 / 080 / 012 (manière volée, gabarit non collé). Voix : `_write_atom_emo_ges_001_04.py`.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action plus vive vers le pot.
- 760 mots. N2 ≤ 15. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 760 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
