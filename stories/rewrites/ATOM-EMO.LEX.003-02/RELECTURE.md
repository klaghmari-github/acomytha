# ATOM-EMO.LEX.003-02 — Amir, le canard et le miel

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N3 (≤16 mots/phrase), audio familial, voc 5–6 ans
- **Leçon :** EMO.LEX.003 — nommer la déception + autre idée (vécue : crochet vide, sourire parti, poitrine qui se bouscule, papa accroupi, Amir dit « je suis déçu », prend le canard ; 2e ruse : plus de confiture, le pot glisse, il refuse de foncer, propose le miel). JAMAIS dite en slogan. Pas « j'ai dit : je suis ». Pas « tu as nommé ». Pas « un souhait peut attendre ». Pas « lumière couleur de miel ».
- **Personnages :** Amir, papa, maman. Dump Ilyes → D16 Amir = enfant-m (veut le bateau bleu maintenant). Pas de copain (dump sans camarade). Troupe D16. Pas de maîtresse.
- **Lieu :** parc, puis cuisine (2 lieux). Coin nommé : kiosque des petits bateaux. Dump : bateau, canard, confiture, miel (objet, pas refrain sensoriel). Indice PAS bateau / miel / tasse / casserole / banc / flaque.
- **Indice unique :** éclat de kiosque (luit sur le bois peint → tremble au crochet vide → luit sur le canard au climax cuisine → tient sur le bois). BAN éclat de bateau / miel / tasse / casserole / banc / flaque / cagette.
- **Question moteur :** « Le bateau n'est plus là. Que dit Amir ? » expected dump **déçu**. accepted dump `déçu | je suis déçu | autre idée | un canard | une autre idée`. retry dump Ilyes → Amir : `Amir cherche une autre idée. Que dit-il d'abord ?`. Hors Q : null. Non récitée ailleurs.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Une cheville de bois tient le volet du kiosque. Sandale, lanière, peinture tiède. Sur le bois peint, un éclat de kiosque luit. Amir veut le bateau bleu **maintenant**. Le crochet est vide. Sourire parti. Envie et inquiétude. Papa s'accroupit. Je suis déçu. Merci vécu. Un canard en bois glisse sur l'eau. Deuxième ruse : plus de confiture, le pot glisse. Il s'arrête, lit l'éclat, propose le miel. Le couvercle résiste, puis cède. Un éclat de kiosque tient sur le bois.

## Arc dramatique

- Monde : parc, kiosque des petits bateaux, volet, cheville, sandale, herbe, puis cuisine, pain, placard.
- Désir : un bateau bleu pour l'eau, maintenant.
- Objet : bateau manquant, canard en bois, pot de confiture vide, pot de miel.
- Indice unique : éclat de kiosque, vu dès l'ouverture, payé sur le bois du canard. Pas éclat de bateau / miel / tasse / casserole / banc / flaque.
- Urgence douce : il se hausse trop vite vers le crochet.
- Imprévu 1 : bateau parti, crochet vide, sourire parti.
- Cue : papa à la même hauteur. Un merci vécu, après qu'il refuse de foncer et prend le canard.
- Imprévu 2 (plus rusé) : plus de confiture, le pot glisse, le couvercle du miel résiste.
- Résolution : il refuse de foncer, observe, écoute la cuisine, retrouve l'éclat, propose le miel.
- Retour : pain tartiné, canard près du pain, éclat sur le bois. La fin a failli (couvercle coincé, pot qui glisse).

## Vécu

Amir veut le bateau **maintenant**. Impatience, puis crochet vide, sourire parti. Il dit je suis déçu. Papa se baisse, pose une question, ne récite pas la leçon. Ils agissent : canard sur l'eau, puis cuisine, pot vide, il s'arrête. Merci vécu. Fin : l'éclat du début tient sur le bois du canard.

## Vu et corrigé

- Titre : Amir, le canard et le miel (noyau dump, miel dans le titre = objet dump OK). Relance : Que dit Amir ? expected déçu.
- Lieu du dump-meta (parc, puis cuisine). Maman et papa. Amir = héros enfant-m. Dump bateau / canard / confiture / miel gardés comme objets, pas comme indice.
- Ouverture inventée (cheville de bois, volet, sandale), pas un gabarit v2, pas gouttes/fontaine du merged, pas « Ilyes marche au parc ».
- Indice unique : éclat de kiosque ×4. BAN éclat de bateau / miel / tasse / casserole / banc / flaque / cagette. Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés. Strip « j'ai dit : je suis ». Strip « lumière couleur de miel » (miel = pot, pas refrain sensoriel).
- Leçon non dite : on la voit quand le crochet est vide, quand il dit je suis déçu, quand il prend le canard, quand il propose le miel. Pas « tu as nommé ». Une seule « je suis déçu ».
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur : « Le bateau n'est plus là. Que dit Amir ? ». expected/accepted dump. retry Ilyes → Amir. Hors Q : null. 5 chunks, kinds inchangés.
- example4 069 / 001 / 033 (manière volée, gabarit non collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N3.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action un peu plus vive vers le pot qui glisse.
- 815 mots. N3 ≤ 16. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 815 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
