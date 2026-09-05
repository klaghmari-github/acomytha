# ATOM-EMO.LEX.001-01 — La fraise de Chouchou

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N1 (≤10 mots/phrase), audio familial, voc 3–4 ans
- **Leçon :** EMO.LEX.001 — nommer la joie et partager (vécue : sourire qui arrive, poitrine pleine, papa accroupi, Chouchou dit « je suis content », tend un bout ; 2e ruse : fraise trop chaude, elle glisse, il refuse de foncer, un bout pour maman). JAMAIS dite dans le récit. Pas « c'est de la joie ». Pas « tu as nommé ». Pas « j'ai dit : je suis ». Pas « on peut partager ».
- **Personnages :** Chouchou, papa, maman. Dump Tom → D16 Chouchou = enfant-m (garçon, veut la fraise maintenant). Pas de copain (dump sans camarade). Troupe D16. Pas de maîtresse.
- **Lieu :** jardin, treille, terre, soleil, fraise, fil de fer, bois, feuille de vigne, jus, ombre. BAN panier / torchon / fraisier (indice dump). ≠ dump « Un petit panier attend près du gravier ».
- **Indice unique :** éclat de treille (luit à l'ouverture → tremble au sourire → luit quand la fraise glisse → tient sur le bois). BAN éclat de fraise / panier / torchon / fraisier / tour / cube.
- **Question moteur :** « Chouchou sourit. Que dit-il ? » expected dump **content**. accepted dump `content | je suis content | joie | de la joie | partager`. retry dump Tom → Chouchou. Non récitée dans les autres chunks.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

La treille du fond fait de l'ombre. Ting. Sur le bois, un éclat de treille luit. Terre chaude, feuille de vigne, fraise rouge. Chouchou veut la cueillir **maintenant**. Il attrape la feuille. Puis la fraise tiède. Sourire qui arrive. Poitrine pleine. Papa s'accroupit. Il dit je suis content. Un bout pour papa. Merci vécu. Deuxième ruse : trop chaude, la fraise glisse. Il s'arrête, lit l'éclat. Un bout pour maman. Un éclat de treille tient sur le bois.

## Arc dramatique

- Monde : jardin, treille, terre, soleil, fil, bois, feuille de vigne. BAN panier / torchon / fraisier.
- Désir : cueillir la fraise, maintenant.
- Objet : fraise rouge, tiède, trop chaude.
- Indice unique : éclat de treille, vu dès l'ouverture, payé sur le bois. Pas éclat de fraise / panier / torchon.
- Urgence douce : il attrape trop vite.
- Imprévu 1 : la feuille, pas la fraise ; puis sourire qui arrive, poitrine pleine.
- Cue : papa à la même hauteur. Un merci vécu, après le bout tendu.
- Imprévu 2 (plus rusé) : fraise trop chaude, elle glisse vers la terre.
- Résolution : il refuse de foncer, observe, écoute le jardin, retrouve l'éclat, casse un bout.
- Retour : trace de jus, fraise dans la paume, éclat sur le bois.

## Vécu

Chouchou veut la fraise **maintenant**. Impatience, puis feuille dans la main, puis fraise tiède, sourire qui arrive. Il dit je suis content, tend un bout. Papa se baisse, pose une question, ne récite pas la règle. Ils agissent : un bout sans se presser, puis un bout pour maman après la glissade. Merci vécu. Fin : l'éclat du début tient sur le bois.

## Vu et corrigé

- Titre : La fraise de Chouchou (noyau dump). Relance : Que dit-il ? expected content.
- Lieu du dump-meta (jardin). Maman et papa. Chouchou = héros enfant-m (dump + mission : garçon). BAN panier / torchon / fraisier dans le récit.
- Ouverture inventée (treille du fond, ombre, ting), pas un gabarit v2, pas panier/torchon/gravier du source, pas « Tom marche dans le jardin ».
- Indice unique : éclat de treille. BAN éclat de fraise / panier / torchon / fraisier / tour / cube. Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés. Strip « tout doucement » / « tout doux » du dump.
- Leçon non dite : on la voit quand le sourire arrive, quand il dit je suis content, quand il tend un bout. Strip dump « c'est de la joie », « tu as nommé », « Chouchou a nommé sa joie », « tu as dit : je suis content », « L'histoire est finie ».
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur : « Chouchou sourit. Que dit-il ? ». expected content. 5 chunks, kinds inchangés. expected/accepted dump conservés (labels moteur, même « de la joie »). retry Tom → Chouchou. Hors Q : expected/accepted/retry null.
- example4 054 / 086 / 018 (manière volée, gabarit non collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N1.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action un peu plus vive vers la fraise qui glisse.
- 844 mots. N1 ≤ 10. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 844 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
