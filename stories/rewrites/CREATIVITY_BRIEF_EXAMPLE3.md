# Brief créativité — example1 + example2 + example3 (F-NAR-019)

Texte seulement. Pas d’audio. Pas de git. Pas de `pkill`. Décider, ne pas demander.

Lis **avant d’écrire** :
- `gestion_projet/feedback_chatgpt/examples/example1/RELECTURE.md`
- `gestion_projet/feedback_chatgpt/examples/example2/RELECTURE (1).md`
- `gestion_projet/feedback_chatgpt/examples/example2/raw.js` (profils TTS `profiles` seulement)
- **trois** fichiers `example3/acomytha_histoires_XXX.txt` (ceux assignés dans ta mission)
- la ligne de **ton** `TREE-*` dans `example2/AUDIT_EDITORIAL_VOCAL_CATALOGUE (1).md`
- `AGENT_PROMPT_F-NAR-019.md`, `AGENT_PROMPT.md`, `_lib.py`

example3 = 100 fichiers, **1500 histoires brutes**. Gabarit industriel (à ne **pas** coller). On vole l’**inventivité**, pas les refrains.

## Ce qu’il faut voler

### 1. Objet nommé, pas un accessoire
L’objet a une couleur, un poids, un petit bruit, une mission **précise** (porter / livrer / allumer / faire arriver). 60 objets du corpus — **invente le tien** pour *cette* histoire, ne recycle pas la clé de cuivre si le noyau est un seau.

Exemples de *familles* (pas à recopier) : clé de cuivre, billet bleu, lentille jaune, roue dentée en bois, enveloppe orange, chapeau à plume, trottinette rouge, lanterne de papier, bateau de feuille, couronne en carton, cerf-volant rouge, marionnette verte, grelot argenté, carton à fenêtres, coussin locomotive, sifflet en bois, galet doré, tournevis-jouet, voile rayée, gourde à étoiles, mallette-jouet, graine tachetée, feuille de musique.

### 2. Lieu qui a un nom d’aventure
Le monde n’est pas « la maison ». C’est **un coin nommé** du monde du xlsx (méta). 60+ lieux du corpus : tour de l’horloge, gare miniature, phare du jardin, bibliothèque aux escaliers rouges, musée des inventions, maison sur la dune, parade des chapeaux, cour des trottinettes, cabane des ombres, concours de bateaux, scène du préau, gâteau des nuages, piste des cerfs-volants, secret du cabanon, ferme aux tomates, jardin aromatique, passage des glycines, marché sous la verrière, plage au parasol jaune, théâtre de marionnettes, chasse aux reflets, chemin des grelots, fresque du jardin, train de coussins, verger des rubans, bibliothèque secrète, garage des boîtes, soirée des lucioles, fête sous les lampions, ville de cartons, boutique des cailloux, campement du salon, placard aux couleurs, parc aux hérissons, fournil du village.

**Règle :** rester dans le décor du xlsx (ferme reste ferme). Nommer un *coin* inventif *dedans* (le secret du cabanon, le fournil, la grille).

### 3. Mission en une phrase + urgence douce
« Porter la clé jusqu’au gardien avant que… » / « faire atteindre la ligne bleue au bateau ». Quelqu’un veut **quelque chose maintenant**. Un imprévu concret l’en empêche.

### 4. Deux imprévus, le second plus rusé
Premier : idée rapide, patatras (marche luisante, objet de travers, vent, courant).
Second : plus malin (billet qui s’envole, ombre sur la toile, pluie qui efface le tracé, autre bateau qui passe, mot coincé dans la gorge).
Le dernier indice était **déjà** dans l’ouverture (marque, ombre, couleur, petit son). La fin **paie** cette image.

### 5. Arc 7 temps — **chaque** ramification, pas seulement la racine
1. Monde ordinaire + détail sensoriel unique
2. Mission + objet
3. Première tentative ratée
4. Cue adulte (geste concret, pas une fiche)
5. Seconde ruse + idée de l’enfant
6. Dernier indice déjà vu au début
7. Retour : l’objet porte encore une trace ; un moment gardé

example1 : le 1er choix **ne retire pas** l’équipement nécessaire. 9 résolutions centrales = action + conséquence + souvenir. 27 fins cohérentes avec l’équipement. Leçons **dans** l’action.

### 6. Leçon-image (vécue, jamais dite)
Les 1500 titres collent une leçon-image (main libre, oreilles attentives, patience pétillante, place du non, cercle accueillant, casque du capitaine, distance du hérisson, voix de confiance…). **Incarne** la leçon du xlsx par un geste, ne l’annonce pas. Une nuance **différente** par chemin (27 fins = 27 souvenirs).

## Interdit de coller (gabarit example3 + `_lib.check`)

- « Aujourd’hui, je vais jusqu’au bout » (`aujourd'hui,` est FORBIDDEN)
- « J’ai une idée. Écoute-la jusqu’au bout »
- « Celui où j’ai compris comment continuer »
- « avec sa couleur, son poids et son petit bruit particulier » en refrain
- merle à trois notes / lumière couleur de miel / gouttes au bord des feuilles **par défaut**
- grand-père, maîtresse, jardinier, bibliothécaire, gardienne du parc — **sauf** s’ils sont déjà dans `characters` du xlsx. Sinon : troupe D16 + papa/maman
- tics : tout doux / encore / déjà / tout calme
- Bravo refrain, « on va apprendre », morales, 4 puces d’affilée

## Voix (example2 `raw.js` `profiles`)

Par chunk, selon la fonction : opening / choice / clue / confirm / action / obstacle / resolution / ending.
`notes` : `arc=…; intention=…; emotion=…; intensite=1|2|3; destinataire=…; sous-texte=…; tempo=…; sourire=…; respiration=…`
`slow` seulement : choix, danger doux, émotion sensible.

## Barre `check()`

N1≤10 / N2≤15 / N3≤16 mots/phrase. `en ce moment`. Papa/maman parlent + une question + **un** merci ou bravo **vécu**. 86 nœuds. 27 fins textuellement distinctes. Chemins ~550–700 mots.

## Livrable

```
python3 stories/outils/rewrite_story.py dump <ID>
# stories/rewrites/<ID>/merged.json + RELECTURE.md
# python3 -c "from stories.rewrites._lib import check; ..."  ou via le script d’écriture
# check() OK. Ne pas apply. Ne pas git. Ne pas audio.
```
