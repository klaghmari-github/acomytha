# Brief créativité — example4 (édition finale v2)

Texte seulement. Pas d’audio. Pas de git. Pas de `pkill`.

Lis **avant d’écrire** : ce fichier + `CREATIVITY_BRIEF_EXAMPLE3.md` + `AGENT_PROMPT_F-NAR-019.md` + `_lib.py` + example1 RELECTURE + example2 `raw.js` `profiles` + **trois** fichiers `example4/acomytha_histoires_*.txt` (ceux de ta mission) + la ligne de **ton** arbre dans l’audit example2.

example4 = 100 fichiers, **1500 histoires**, mêmes objets/lieux/leçons-images qu’example3, mais **prose plus incarnée**. On vole ça. On ne colle pas le gabarit v2 non plus.

## Ce que v2 fait mieux qu’example3 (à voler)

1. **Cinq manières de commencer** (en inventer d’autres, ne pas recycler celles-ci) :
   - une idée déjà dessinée dans l’air
   - l’enfant **connaît** le lieu ; un détail paraît **nouveau**
   - d’abord un détail sensoriel, **puis** l’objet
   - une journée douce qui bascule en expédition
   - (interdit chez nous : « Aujourd’hui, je mène la mission »)
2. **Indice du début, unique** : marque fine / ombre-flèche / tache / symbole — **un seul**, nommé, déjà vu à l’ouverture, **payé** au climax. Invente le tien (pas ces quatre mots en refrain).
3. **Corps** : le sourire disparaît ; envie et inquiétude se bousculent dans la poitrine ; l’adulte s’accroupit à la même hauteur.
4. **Deuxième imprévu plus rusé** ; l’enfant **refuse de foncer** ; personne ne donne la réponse ; il observe l’objet, écoute le lieu, retrouve l’indice du début.
5. **Dénouement qui a failli ne pas arriver.** L’objet trouve une place, porte une trace. On raconte **surtout** le passage difficile.

## Toujours voler (example3)

Objet nommé + mission précise + coin d’aventure **dans** le monde du xlsx. Arc 7 temps sur **chaque** ramification. 27 fins = 27 souvenirs. 1er choix ne retire pas l’équipement.

## Interdit de coller (v2 + `_lib`)

- `aujourd'hui,` / « Aujourd’hui, je mène la mission »
- « On dirait que notre mission veut nous tester »
- « Mission accomplie » + « Avec un détour que personne n’aurait pu inventer »
- « J’ai compris ! » en refrain
- merle trois notes / lumière couleur de miel / gouttes au bord des feuilles par défaut
- grand-père, maîtresse, jardinier, bibliothécaire, gardienne — **sauf** déjà dans `characters`
- tics tout doux / encore / déjà / tout calme

Adultes = papa/maman. Troupe D16.

## Voix + check

Identique F-NAR-019 : notes + ssml + xai + piper par chunk, profils `raw.js`. N1≤10 / N2≤15 / N3≤16. `en ce moment`. Un merci vécu. 86 nœuds.

## Livrable

```
python3 stories/outils/rewrite_story.py dump <ID>
# stories/rewrites/<ID>/merged.json + RELECTURE.md + _write_tree_*.py
# check() OK. Ne pas apply. Ne pas git. Ne pas audio.
```
