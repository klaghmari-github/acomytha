# ATOM-EMO.LEX.003-05 — Raphaël et la porte fermée

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N3 (≤16 mots/phrase), audio familial, voc 5–6 ans
- **Leçon :** EMO.LEX.003 — nommer la déception + autre idée (vécue : porte fermée, sourire parti, poitrine qui se bouscule, papa accroupi, Raphaël dit « je suis déçu », propose de lire à la maison ; 2e ruse : plus de fraises, la pomme glisse, il refuse de foncer, choisit une pomme). JAMAIS dite en slogan. Pas « j'ai dit : je suis ». Pas « tu as nommé ». Pas « un souhait peut attendre ». Pas de bibliothécaire qui parle.
- **Personnages :** Raphaël, papa, maman. Dump Ugo → D16 Raphaël = enfant-m (veut entrer maintenant). Maman ajoutée. Pas de copain (dump sans camarade). Troupe D16. Pas de maîtresse. Pas de bibliothécaire.
- **Lieu :** rue de la bibliothèque puis maison (2 lieux). Coin nommé : store de la façade. Dump : porte, fraises, pomme, livre (objet, pas indice). Indice PAS vitre / volet / sonnette / clé / livre.
- **Indice unique :** éclat de store (luit sur les lamelles → tremble à la porte fermée → luit sur le store au climax maison → tient sur le tissu). BAN éclat de vitre / volet / sonnette / clé / livre / cagette / kiosque / pelle / ficelle.
- **Question moteur :** « La bibliothèque est fermée. Que dit Raphaël ? » expected dump **déçu**. accepted dump `déçu | je suis déçu | autre idée | une pomme | une autre idée`. retry dump Ugo → Raphaël : `Raphaël cherche une autre idée. Que dit-il d'abord ?`. Hors Q : null. Non récitée ailleurs.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

La barre de fer est froide. Sac, manteau, lamelles. Sur les lamelles, un éclat de store luit. Raphaël veut entrer **maintenant**. La porte est fermée. Sourire parti. Envie et inquiétude. Papa s'accroupit. Je suis déçu. Merci vécu. Ils lisent à la maison. Deuxième ruse : plus de fraises, la pomme glisse. Il s'arrête, lit l'éclat, choisit une pomme. La peau résiste, puis cède. Un éclat de store tient sur le tissu.

## Arc dramatique

- Monde : rue de la bibliothèque, store de la façade, barre de fer, sac, puis maison, table, corbeille, livre.
- Désir : entrer à la bibliothèque, maintenant.
- Objet : porte fermée, livre de trains, corbeille vide, pomme.
- Indice unique : éclat de store, vu dès l'ouverture, payé sur le store de la maison. Pas éclat de vitre / volet / sonnette / clé / livre.
- Urgence douce : il pousse la porte trop vite.
- Imprévu 1 : porte fermée, sourire parti.
- Cue : papa à la même hauteur. Un merci vécu, après qu'il refuse de foncer et propose de lire à la maison.
- Imprévu 2 (plus rusé) : plus de fraises, la pomme glisse, la peau résiste.
- Résolution : il refuse de foncer, observe, écoute la maison, retrouve l'éclat, choisit une pomme.
- Retour : livre ouvert, pomme coupée, éclat sur le tissu. La fin a failli (pomme qui glisse, peau coincée).

## Vécu

Raphaël veut entrer **maintenant**. Impatience, puis porte fermée, sourire parti. Il dit je suis déçu. Papa se baisse, pose une question, ne récite pas la leçon. Ils agissent : lire à la maison, puis corbeille vide, il s'arrête. Merci vécu. Fin : l'éclat du début tient sur le tissu du store.

## Vu et corrigé

- Titre : Raphaël et la porte fermée (noyau dump). Relance : Que dit Raphaël ? expected déçu.
- Lieu du dump-meta (rue de la bibliothèque puis maison). Maman et papa. Raphaël = héros enfant-m. Dump porte / fraises / pomme / livre gardés comme objets, pas comme indice.
- Ouverture inventée (barre de fer, store baissé, sac), pas un gabarit v2, pas flaque/vitre/poignée du merged, pas « Ugo veut aller à la bibliothèque ».
- Indice unique : éclat de store ×4. BAN éclat de vitre / volet / sonnette / clé / livre / cagette / kiosque / pelle / ficelle. Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés. Strip « j'ai dit : je suis ». Strip merle/miel. Strip bibliothécaire qui parle.
- Leçon non dite : on la voit quand la porte est fermée, quand il dit je suis déçu, quand il propose le livre, quand il choisit la pomme. Pas « tu as nommé ». Une seule « je suis déçu ».
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur : « La bibliothèque est fermée. Que dit Raphaël ? ». expected/accepted dump. retry Ugo → Raphaël. Hors Q : null. 5 chunks, kinds inchangés.
- example4 072 / 004 / 036 (manière volée, gabarit non collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N3.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action un peu plus vive vers la pomme qui glisse.
- 804 mots. N3 ≤ 16. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 804 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
