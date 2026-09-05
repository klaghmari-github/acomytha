# ATOM-EMO.LEX.002-01 — Aniss et le doudou bleu

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N1 (≤10 mots/phrase), audio familial, voc 3–4 ans
- **Leçon :** EMO.LEX.002 — nommer la tristesse + demander un câlin (vécue : doudou perdu, sourire parti, poitrine serrée, yeux chauds, Aniss dit je suis triste, pleure, demande un câlin, maman ouvre les bras ; 2e ruse : doudou vu puis disparu, oreille coincée, il refuse de foncer, papa trouve). JAMAIS dite dans le récit. Pas « pleurer est permis ». Pas « le câlin aide ». Pas « c'est de la tristesse ». Pas « j'ai dit : je suis ».
- **Personnages :** Aniss, papa, maman. Dump Nora → D16 Aniss = enfant-m (veut le doudou maintenant). Pas de copain (dump sans camarade). Troupe D16. Pas de maîtresse.
- **Lieu :** chambre, soir, lampe, tapis, lit, doudou, couverture, oreiller, table. Dump doudou / lampe / tapis / lit gardés. ≠ plaid / coussin.
- **Indice unique :** éclat de couverture (luit à l'ouverture → tremble aux larmes → luit quand l'oreille est coincée → tient sur le tissu). BAN éclat de doudou / lampe / tapis / lit / plaid / coussin. Pas treille / moule / tuteur / saladier / gomme / berge / brouette / torchon / tabouret.
- **Question moteur :** « Aniss a les yeux chauds. Que dit-il ? » expected dump **triste**. accepted dump `triste | je suis triste | câlin | un câlin | pleurer`. retry dump Nora → Aniss (dit-il). Non récitée dans les autres chunks. Hors Q : expected / accepted / retry nuls.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Une chaussette glisse du bord du lit. Savon, lampe, rond jaune sur le tapis. Sur la couverture, un éclat de couverture luit. Aniss veut le doudou **maintenant**. Le doudou n'est pas là. Sourire parti. Poitrine serrée. Yeux chauds. Papa s'accroupit. Je suis triste. Un câlin. Merci vécu. Deuxième ruse : bout bleu vu, puis disparu, oreille coincée. Il s'arrête, lit l'éclat. Papa trouve. Un éclat de couverture tient sur le tissu.

## Arc dramatique

- Monde : chambre, soir, lampe, tapis, lit, couverture.
- Désir : retrouver le doudou bleu, maintenant.
- Objet : doudou bleu, puis oreille coincée.
- Indice unique : éclat de couverture, vu dès l'ouverture, payé sur le tissu. Pas éclat de doudou / lampe / tapis / lit.
- Urgence douce : il fouille trop vite, trop haut.
- Imprévu 1 : doudou absent, sourire parti, poitrine serrée, larmes.
- Cue : papa à la même hauteur. Un merci vécu, après le câlin.
- Imprévu 2 (plus rusé) : doudou vu sous la table, puis disparu, oreille coincée sous le bord.
- Résolution : il refuse de foncer, observe, écoute la chambre, retrouve l'éclat. Papa tire tout petit à petit.
- Retour : oreille froissée, doudou contre le lit, éclat sur le tissu. Dénouement qui a failli : l'oreille partait plus loin.

## Vécu

Aniss veut le doudou **maintenant**. Impatience, puis lit vide, sourire parti. Il dit je suis triste, pleure, demande un câlin. Maman ouvre les bras. Papa se baisse, pose une question, ne récite pas la règle. Ils agissent : chercher sans se presser, tenir le bord, papa trouve. Merci vécu. Fin : l'éclat du début tient sur le tissu.

## Vu et corrigé

- Titre : Aniss et le doudou bleu (noyau dump). Relance : Que dit-il ? expected triste.
- Lieu du dump-meta (chambre, soir). Maman et papa. Aniss = héros enfant-m. Dump doudou / lampe / tapis / lit.
- Ouverture inventée (chaussette qui glisse, soir), pas un gabarit v2, pas « Nora cherche son doudou », pas « L'histoire est finie ».
- Indice unique : éclat de couverture. BAN éclat de doudou / lampe / tapis / lit / plaid / coussin. Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme/toute calme et `aujourd'hui` retirés. Strip « toute calme » du dump.
- Leçon non dite : on la voit quand les yeux sont chauds, quand Aniss dit je suis triste, quand il pleure, quand il demande un câlin. Pas « pleurer est permis ». Pas « le câlin aide ». Pas « j'ai dit : je suis ».
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur : « Aniss a les yeux chauds. Que dit-il ? ». expected triste. 5 chunks, kinds inchangés. expected/accepted dump conservés. retry Nora → Aniss (dit-il). Hors Q : null.
- example4 061 / 093 / 025 (manière volée, gabarit non collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N1.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action un peu plus vive vers l'oreille coincée.
- 821 mots. N1 ≤ 10. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 821 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
