# ATOM-EMO.LEX.001-04 — Amir et le gâteau encore chaud

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N1 (≤10 mots/phrase), audio familial, voc 3–4 ans
- **Leçon :** EMO.LEX.001 — nommer la joie + partager (vécue : gâteau trop chaud, poitrine trop vite, sourire parti, papa accroupi, un sourire revient, Amir dit je suis content, deux petits bouts ; 2e ruse : le bout s'effrite, il refuse de foncer). JAMAIS dite dans le récit. Pas « c'est de la joie ». Pas « j'ai dit : je suis ». Pas « tu as nommé ».
- **Personnages :** Amir, papa, maman. Dump Amir = enfant-m (veut un bout maintenant). Pas de copain. Troupe D16. Pas de maîtresse. Flora du retry source → Amir.
- **Lieu :** cuisine, matin, gâteau, saladier, assiette, miette, carrelage, four, fenêtre, beurre, citron, table. BAN nappe / farine / casserole / tasse (indice pris ailleurs).
- **Indice unique :** éclat de saladier (luit à l'ouverture → tremble après le chaud → luit quand le bout s'effrite → tient sur le verre). BAN éclat de treille / moule / tuteur / assiette / farine / tour / comptoir / pot / rouleau / lit / étagère / torchon / tabouret / nappe / casserole / tasse / miette.
- **Question moteur :** « Amir sourit. Que dit-il ? » expected dump **content**. accepted dump `content | contente | je suis contente | joie | de la joie | partager`. retry Flora → Amir (dit-il). Hors Q : null. Non récitée dans les autres chunks.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Maman pose le saladier près du gâteau. Sur le verre, un éclat de saladier luit. Beurre, citron, carrelage tiède. Amir veut un bout **maintenant**. Le gâteau est trop chaud. Poitrine trop vite. Sourire parti. Papa s'accroupit. Un sourire revient. Il dit je suis content. Merci vécu. Deux petits bouts. Deuxième ruse : le bout s'effrite. Il s'arrête, lit l'éclat. Un éclat de saladier tient sur le verre.

## Arc dramatique

- Monde : cuisine du matin, saladier, gâteau près de la fenêtre.
- Désir : un bout du gâteau, maintenant, à partager.
- Objet : gâteau encore chaud, assiette, deux petits bouts.
- Indice unique : éclat de saladier, vu dès l'ouverture, payé sur le verre. Pas éclat d'assiette / farine / nappe.
- Urgence douce : il tend la main trop vite.
- Imprévu 1 : gâteau trop chaud, poitrine trop vite, sourire parti.
- Cue : papa à la même hauteur. Un merci vécu, après le bout offert.
- Imprévu 2 (plus rusé) : le deuxième bout s'effrite sur l'assiette.
- Résolution : il refuse de foncer, observe, écoute la cuisine, retrouve l'éclat, pose le bout pour maman.
- Retour : deux petits bouts ont suffi, éclat sur le verre.

## Vécu

Amir veut un bout **maintenant**. Impatience, puis doigts brûlés, sourire parti. Un sourire revient, tout petit. Il dit je suis content, puis on peut partager. Papa se baisse, pose une question, ne récite pas la joie. Ils agissent : un bout sans se presser, deux petits bouts. Merci vécu. Fin : l'éclat du début tient sur le verre.

## Vu et corrigé

- Titre : Amir et le gâteau encore chaud (noyau dump). Relance : Que dit-il ? expected content.
- Lieu du dump-meta (cuisine, matin). Maman et papa. Amir = héros enfant-m. Gâteau / assiette / miette du dump.
- Ouverture inventée (maman pose le saladier), pas un gabarit v2, pas « Le soleil pose des carrés chauds » du source.
- Indice unique : éclat de saladier. BAN éclat de treille / moule / tuteur / assiette / farine / tour / nappe / casserole / tasse / miette. Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés. Strip « c'est de la joie », « j'ai dit : je suis », « tu as nommé », « Bravo, Amir ».
- Leçon non dite : on la voit quand le sourire revient, quand Amir dit je suis content, quand il offre un bout. Pas « c'est de la joie ». Pas « tu as dit ta joie ».
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur : « Amir sourit. Que dit-il ? ». expected content. 5 chunks, kinds inchangés. expected/accepted dump conservés. retry Flora → Amir (dit-il). Hors Q : null.
- example4 057 / 089 / 021 (manière volée, gabarit non collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N1.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action un peu plus vive vers le bout qui s'effrite.
- 795 mots. N1 ≤ 10. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 795 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
