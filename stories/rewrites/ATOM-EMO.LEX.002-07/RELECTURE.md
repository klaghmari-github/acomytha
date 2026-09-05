# ATOM-EMO.LEX.002-07 — Mila et le doudou rose

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N1 (≤10 mots/phrase), audio familial, voc 3–4 ans
- **Leçon :** EMO.LEX.002 — nommer la tristesse + demander un câlin (vécue : doudou perdu, sourire parti, poitrine serrée, yeux chauds, Mila dit je suis triste, pleure, demande un câlin, maman ouvre les bras ; 2e ruse : doudou vu puis disparu, oreille coincée dans le panier, elle refuse de foncer, papa trouve). JAMAIS dite dans le récit. Pas « pleurer est permis ». Pas « le câlin aide ». Pas « c'est de la tristesse ». Pas « j'ai dit : je suis ».
- **Personnages :** Mila, papa, maman. Dump Céline → D16 Mila = enfant-f (veut le doudou maintenant). Pas de copain (dump sans camarade). Troupe D16. Pas de maîtresse. Distinct 002-01 (Aniss, doudou bleu).
- **Lieu :** chambre, soir, housse, lit, doudou, panier, oreiller, radiateur, fenêtre, veilleuse, verre. Dump doudou / panier / lit gardés. BAN couverture / plaid / coussin / lampe / tapis (indice pris ailleurs).
- **Indice unique :** éclat de housse (luit à l'ouverture → tremble aux larmes → luit quand l'oreille est coincée → tient sur le tissu). BAN éclat de doudou / couverture / panier / lit / plaid / coussin / lampe / tapis. Pas fauteuil / paillasson / coffre / haie / capuche / treille / moule.
- **Question moteur :** « Mila a les yeux chauds. Que dit-elle ? » expected dump **triste**. accepted dump `triste | je suis triste | câlin | un câlin`. retry dump Céline → Mila (dit-elle). Non récitée dans les autres chunks. Hors Q : expected / accepted / retry nuls.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Un tic léger traverse la chambre. Linge, veilleuse, rond rose, fenêtre embuée. Sur la housse, un éclat de housse luit. Mila veut le doudou **maintenant**. Le doudou n'est pas là. Sourire parti. Poitrine serrée. Yeux chauds. Papa s'accroupit. Je suis triste. Un câlin. Merci vécu. Deuxième ruse : bout rose vu, puis disparu, oreille coincée dans le panier. Elle s'arrête, lit l'éclat. Papa trouve. Un éclat de housse tient sur le tissu.

## Arc dramatique

- Monde : chambre, soir, housse, lit, panier, veilleuse.
- Désir : retrouver le doudou rose, maintenant.
- Objet : doudou rose, puis oreille coincée dans le panier.
- Indice unique : éclat de housse, vu dès l'ouverture, payé sur le tissu. Pas éclat de doudou / couverture / panier / lit.
- Urgence douce : elle fouille trop vite, trop bas.
- Imprévu 1 : doudou absent, sourire parti, poitrine serrée, larmes.
- Cue : papa à la même hauteur. Un merci vécu, après le câlin.
- Imprévu 2 (plus rusé) : doudou vu dans le panier, puis disparu, oreille coincée sous le linge.
- Résolution : elle refuse de foncer, observe, écoute la chambre, retrouve l'éclat. Papa tire tout petit à petit.
- Retour : oreille froissée, doudou contre le lit, éclat sur le tissu. Dénouement qui a failli : l'oreille partait plus loin.

## Vécu

Mila veut le doudou **maintenant**. Impatience, puis lit vide, sourire parti. Elle dit je suis triste, pleure, demande un câlin. Maman ouvre les bras. Papa se baisse, pose une question, ne récite pas la règle. Ils agissent : chercher sans se presser, tenir le bord, papa trouve dans le panier. Merci vécu. Fin : l'éclat du début tient sur le tissu.

## Vu et corrigé

- Titre : Mila et le doudou rose (noyau dump). Relance : Que dit-elle ? expected triste.
- Lieu du dump-meta (chambre, soir). Maman et papa. Mila = héros enfant-f. Dump doudou / panier / lit.
- Ouverture inventée (tic du radiateur, soir), pas un gabarit v2, pas « Céline cherche son doudou », pas « L'histoire est finie », pas « La veilleuse dessine des lunes » en tête.
- Indice unique : éclat de housse. BAN éclat de doudou / couverture / panier / lit / plaid / coussin / lampe / tapis. Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme/toute calme et `aujourd'hui` retirés. Strip « pleurer est permis » et « j'ai dit : je suis » du dump.
- Leçon non dite : on la voit quand les yeux sont chauds, quand Mila dit je suis triste, quand elle pleure, quand elle demande un câlin. Pas « pleurer est permis ». Pas « le câlin aide ». Pas « j'ai dit : je suis ».
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur : « Mila a les yeux chauds. Que dit-elle ? ». expected triste. 5 chunks, kinds inchangés. expected/accepted dump conservés. retry Céline → Mila (dit-elle). Hors Q : null.
- example4 067 / 099 / 031 (manière volée, gabarit non collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N1.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action un peu plus vive vers l'oreille coincée.
- 819 mots. N1 ≤ 10. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 819 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
