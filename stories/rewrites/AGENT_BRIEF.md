# Brief agent — réécriture ATOM (D38)

Produit **AcoMytha**. Audio-only, 3–6 ans. Décider, ne pas demander d’avis.

## Interdit

**Jamais de leçon dite.** L’enfant ne doit pas entendre qu’on lui apprend quelque chose.
Interdit : « On va apprendre… », « Voici le geste », « On va ranger », « Après le jeu, on range », « C’est la règle », « Tu as suivi la règle », « Même leçon, autre moment », « Tu as repris le geste », « Il faut demander », « On doit demander. Demander, c’est… », « Il ne faut pas rire ».
La leçon est **implicite** : vécue par un imprévu. Ranger = le doudou est perdu sous le bazar ; on ne le retrouve qu’en rangeant les jouets. Pas « on va apprendre à ranger ».
Liste de gestes : « Alice range le triangle. » Ce n’est **pas** une histoire.
« Bravo. Tu as fait du bon travail. L’histoire est finie. »
« Tu as mis ce que l’adulte a dit. » / recap d’objets en liste.
La même phrase-refrain d’une histoire à l’autre.
Prénom hors troupe. Adulte autrement que papa/maman.
POS-001 : dire quoi faire dans la scène (tenir la main), jamais « on va apprendre la rue ».

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
