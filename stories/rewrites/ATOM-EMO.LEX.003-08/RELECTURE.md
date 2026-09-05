# ATOM-EMO.LEX.003-08 — Le citron de Victorina

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N2 (≤15 mots/phrase), audio familial, voc 4–5 ans
- **Leçon :** EMO.LEX.003 — nommer la déception + chercher une autre idée (vécue : Victorina veut les fraises **maintenant**, fraises pour plus tard, sourire parti, trou dans la poitrine, papa accroupi ; « Je suis déçue » ; elle sent le basilic ; 2e ruse : basilic qui glisse, citron trop acide, elle refuse de foncer, choisit un citron plus rond). JAMAIS dite dans le récit. Pas « on peut chercher une autre idée ». Pas « c'est de la déception ». Pas « j'ai dit : je suis ».
- **Personnages :** Victorina, papa, maman. Dump maman seulement → **ajoute papa**. Victorina = enfant-f (veut les fraises maintenant). Pas de copain. Troupe D16. Pas de maîtresse.
- **Lieu :** marché, barquette, basilic, citron, fraises, panier, table, herbes, linge, plastique, verre. Fraises / basilic / citron / marché = dump. ≠ cagette / kiosque / étal / cageot. ≠ gâteau / poire (003-01).
- **Indice unique :** éclat de barquette (luit à l'ouverture → tremble à la déception → luit quand le basilic glisse et le citron pique → tient sur le plastique). BAN éclat de citron / fraise / cagette / kiosque / étal / caisse / cageot / store / napperon / rail / pelle / ficelle.
- **Question moteur :** « Victorina n'a pas les fraises. Que dit-elle ? » expected dump **déçue**. accepted dump `déçue | je suis déçue | autre idée | le citron | le basilic`. retry dump conservé. Non récitée dans les autres chunks. Hors Q : expected/accepted/retry restent **null**.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Une tige de basilic accroche la manche. Passage des herbes, verre d'eau, barquette. Sur le plastique, un éclat de barquette luit. Victorina veut les fraises **maintenant**. Les fraises, c'est pour plus tard. Sourire parti. Trou dans la poitrine. Papa s'accroupit. Je suis déçue. Merci vécu. Elle sent le basilic. Deuxième ruse : basilic qui glisse, citron trop acide. Elle refuse de foncer. Citron plus rond, petite trace. Le citron roule, presque dehors, puis tient. Un éclat de barquette tient sur le plastique.

## Arc dramatique

- Monde : marché, passage des herbes, barquette, verre, linge, panier. ≠ cagette / kiosque / étal / cageot.
- Désir : les fraises, maintenant.
- Objet : fraises pour plus tard, puis basilic senti, puis citron choisi.
- Indice unique : éclat de barquette, vu dès l'ouverture, payé sur le plastique. Pas éclat de citron / fraise / cagette / kiosque / étal / cageot / store / napperon / rail / pelle / ficelle.
- Urgence douce : elle avance trop vite vers la barquette.
- Imprévu 1 : fraises pour plus tard, sourire parti, trou dans la poitrine.
- Cue : papa à la même hauteur. Un merci vécu, après l'arrêt.
- Imprévu 2 (plus rusé) : basilic qui glisse, citron trop acide.
- Résolution : elle refuse de foncer, observe, écoute le marché, retrouve l'éclat, choisit un citron plus rond.
- Retour : citron contre le panier, petite trace, il a failli sortir. Éclat sur le plastique. Dénouement qui a failli.

## Vécu

Victorina veut les fraises **maintenant**. Impatience, puis fraises pour plus tard, sourire parti, trou dans la poitrine. Elle dit je suis déçue. Elle s'arrête, sent le basilic, choisit un citron. Papa se baisse, pose une question, ne récite pas la règle. Merci vécu. Fin : l'éclat du début tient sur le plastique.

## Vu et corrigé

- Titre : Le citron de Victorina (noyau dump). Relance : Victorina n'a pas les fraises. Que dit-elle ? expected déçue.
- Lieu du dump-meta (marché). Maman et papa (papa ajouté). Victorina = héros enfant-f. Fraises / basilic / citron conservés. Distinct de 003-01 (pas de gâteau, pas de poire, pas de cagette).
- Ouverture inventée (tige de basilic à la manche), pas un gabarit v2, pas « La balance du marché fait tic », pas « L'histoire est finie ».
- Indice unique : éclat de barquette ×4. BAN éclat de citron / fraise / cagette / kiosque / étal / cageot / store / napperon / rail / pelle / ficelle. Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme/toute calme et `aujourd'hui` retirés. Strip « j'ai dit : je suis », « on peut chercher une autre idée », « c'est de la déception », « tu as nommé ».
- Leçon non dite : on la voit quand les fraises restent, quand Victorina dit je suis déçue, quand elle sent le basilic, quand elle choisit un citron. Pas « on peut chercher une autre idée ». Pas « c'est de la déception ». Pas « j'ai dit : je suis ».
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur : « Victorina n'a pas les fraises. Que dit-elle ? ». expected déçue. 5 chunks, kinds inchangés. expected/accepted/retry dump conservés. Hors Q : null.
- example4 075 / 007 / 039 (manière volée, gabarit non collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N2.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action un peu plus vive vers le basilic qui glisse.
- 850 mots. N2 ≤ 15. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 850 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
