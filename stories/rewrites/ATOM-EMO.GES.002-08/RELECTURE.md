# ATOM-EMO.GES.002-08 — Le pont de Nina

Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.

- **Public :** N3 (≤16 mots/phrase), audio familial, voc 4–6 ans
- **Leçon :** EMO.GES.002 — pont qui tombe, corps trop vite → souffler, faire une pause (vécue : Nina veut un pont maintenant, cubes tombent, poitrine trop vite, sourire parti, papa accroupi, elle souffle, s'assoit, pause ; 2e ruse cuisine : casserole glisse, bruit fort, le corps repart, elle refuse de foncer). JAMAIS dite dans le récit. Pas « on peut souffler ». Pas « tu peux souffler ». Pas « tu as fait une pause ».
- **Personnages :** Nina, papa, maman. Dump Nina/papa/maman, troupe D16. Nina = enfant-f (veut le pont maintenant). Pas d'autre adulte. (002-05 a aussi Nina : chambre/lit ; ici salon puis cuisine, pont.) Zéro Ferdinand.
- **Lieu :** salon puis cuisine, tabouret, cubes, voiture, soupe, pain, bois, casserole, sol. BAN tapis / canapé / coussin / torchon / farine comme indice. 2e temps cuisine conservé.
- **Indice unique :** éclat de tabouret (luit à l'ouverture → tremble à la chute → luit quand la casserole glisse → tient sur le bois). BAN éclat de casserole / tapis / cube / chaise / torchon.
- **Question moteur :** « Le pont tombe. Que fait Nina ? » expected dump **souffler**. accepted dump `souffler | il souffle | pause | une pause | s'asseoir`. retry dump `Il souffle. Il s'assoit. Que fait-il ?` (pas de nom hors D16 à remapper). Non récitée dans les autres chunks.
- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

La petite voiture tape le tabouret. Sur le bois, un éclat de tabouret luit. Soupe, pain, cubes. Nina veut un pont **maintenant**. Le pont tombe. Poitrine trop vite. Sourire parti. Papa s'accroupit. Elle souffle, pause. Merci vécu. Deuxième ruse : casserole qui glisse, bruit fort. Elle s'arrête, lit l'éclat. Un éclat de tabouret tient sur le bois.

## Arc dramatique

- Monde : salon puis cuisine, tabouret, cubes, voiture, soupe, pain, bois, casserole. BAN tapis / canapé / torchon.
- Désir : un pont pour la voiture, maintenant.
- Objet : cubes, voiture, puis casserole qui glisse.
- Indice unique : éclat de tabouret, vu dès l'ouverture, payé sur le bois. Pas éclat de casserole / tapis / cube.
- Urgence douce : elle pose trop vite, trop haut.
- Imprévu 1 : le pont tombe, poitrine trop vite, sourire parti.
- Cue : papa à la même hauteur. Un merci vécu, après la pause.
- Imprévu 2 (plus rusé) : cuisine, casserole qui glisse, bruit fort, le corps repart trop vite.
- Résolution : elle refuse de foncer, observe, écoute la cuisine, retrouve l'éclat, souffle, attend.
- Retour : soupe, petit pont qui a failli rester en tas, éclat sur le bois.

## Vécu

Nina veut un pont **maintenant**. Impatience, puis cubes par terre, sourire parti. Elle souffle, s'assoit, les mains sur les genoux. Papa se baisse, pose une question, ne récite pas la règle. Ils agissent : un cube sans se presser, pont de deux. Merci vécu. Cuisine : la casserole glisse, elle refuse de foncer. Fin : l'éclat du début tient sur le bois. Le pont a failli rester en tas.

## Vu et corrigé

- Titre : Le pont de Nina (noyau dump). Relance dump : Que fait Nina ? expected souffler.
- Lieu du dump (salon puis cuisine). Maman et papa. Nina = héros enfant-f. BAN tapis / canapé comme indice.
- Ouverture inventée (voiture tape le tabouret), pas un gabarit v2, pas « Sur le toit, la pluie » du source, pas les cinq ouvertures du brief.
- Indice unique : éclat de tabouret. BAN éclat de casserole / tapis / cube / chaise / torchon. Pas tache/flèche/marque/symbole.
- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés. Strip « tout doucement » / « Bravo, Nina » slogan / « L'histoire est finie » du dump.
- Leçon non dite : on la voit quand le pont tombe, quand la poitrine va trop vite, quand Nina souffle, quand elle s'assoit, quand elle refuse de foncer. Pas « on peut souffler ». Pas « tu as fait une pause ».
- Un « en ce moment ». Un merci vécu. Adulte + question.
- Question moteur : « Le pont tombe. Que fait Nina ? ». expected souffler. 5 chunks, kinds inchangés. expected/accepted/retry dump conservés.
- example4 053 / 085 / 017 (manière volée, gabarit non collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N3 raw.js.
- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). `slow` = question et fin. Action un peu plus vive vers la casserole qui glisse.
- 794 mots. N3 ≤ 16. `check()` OK. Pas apply.

## Contrôles

- 5 chunks, graphe inchangé
- 794 mots
- `text` = `script` collé

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
