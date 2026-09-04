# Brief agent — réécriture ATOM (D38)

Produit **AcoMytha**. Audio-only, 3–6 ans. Décider, ne pas demander d’avis.

## Interdit

Liste de gestes : « Alice range le triangle. Alice range le rectangle. » Ce n’est **pas** une histoire.
« Bravo. Tu as fait du bon travail. L’histoire est finie. » — refrain **interdit**, y compris la phrase seule « L'histoire est finie. »
« Tu as mis ce que l’adulte a dit. » / recap d’objets en liste (gourde, doudou, livre / triangle, rectangle, cercle).
La même phrase-refrain d’une histoire à l’autre (« un chuchotement serre son ventre », « une étape après l’autre »).
Recopier la même amorce que l’histoire d’à côté.
Prénom hors troupe (Nora, Alice, Constantin, Lucas, Céline…). Adulte nommé autrement que papa/maman.
Décrire un geste dangereux (POS-001) : dire quoi faire, jamais la course dans la rue.

## Arc obligatoire (sinon ce n’est pas une histoire)

1. **Monde** : village / ville / montagne / mer / jardin / immeuble — lumière, odeur, saison, un détail qui n’appartient qu’à *cette* histoire.
2. **Désir** du héros (un projet concret : un bateau, un pain chaud, un ami qui attend).
3. **Petit imprévu** (pli de travers, doudou oublié, carton mouillé, flaque, objet qui roule).
4. **Résolution** par l’enfant, avec papa/maman qui parlent.
5. **Fin heureuse vécue** : image sensorielle qui referme le désir du début. Pas « L'histoire est finie. »

La leçon se **greffe** dans cet arc. Pas l’inverse.

## Obligatoire

Monde (maison, jardin, village, saison, odeur, lumière) → **désir** du héros → petit **imprévu** → **résolution** → **fin heureuse** qui répond au début.
La leçon se **greffe**. L’enfant agit. Papa/maman **parlent**.
Troupe : Amir, Aniss, Sarah, Chouchou, Mila, Nino, Nina, Raphaël, Victorino, Victorina. Un héros, au plus un autre enfant, papa/maman.
N1 : ~8 mots/phrase. N2 : < 16. ≥ 3 min d’écoute (plusieurs passages vécus).
Garder `chunk_id`, `kind`, graphe `option_*_next`.

Voix script `role|phrase` : `narrateur`, `papa`, `maman`, `enfant-m` (Amir Aniss Nino Raphaël Victorino) ou `enfant-f` (Sarah Chouchou Mila Nina Victorina).
`length_scale_piper` : narrateur 1.22, adulte 1.18, enfant 1.28.

## Commandes

```
python3 stories/outils/rewrite_story.py dump <id>
# écrire stories/rewrites/<id>/merged.json (fil_rouge, title, chunks)
python3 stories/outils/rewrite_story.py apply <id>
```

Texte seulement. Pas d’audio. Pas de `git commit`.
