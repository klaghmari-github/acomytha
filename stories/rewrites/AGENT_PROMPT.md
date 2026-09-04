# Passe F-NAR-009 — réécriture texte (pas d’audio)

Tu réécris des histoires AcoMytha pour enfants **3–6 ans**, audio seulement.

## Interdit (entrée brutale)

- « X joue au salon. »
- « X est dans l’entrée. »
- « C’est le matin. X est… »
- « Aujourd’hui, X est avec papa. On va apprendre : … Voici le geste : … »

## Obligatoire

1. **Monde d’abord.** Lieu (maison, village, rue, parc vu de la fenêtre…), famille (papa, maman), temps (pluie, soleil, soir, odeur de soupe…), détails sensoriels. Ensuite seulement l’action présente (« en ce moment… »).
2. **Créatif.** Chaque histoire a **sa** manière de commencer. Les deux textes ci-dessous sont des **exemples de manières**, pas des modèles. **Ne pas les recopier. Ne pas se limiter à eux.** Inventer (gouttière, tapis, chaussures mouillées, rayon de lumière, doudou qui attend, fenêtre embuée, marché au loin, etc.).
3. **Détails.** Les enfants adorent ça : couleurs, bruits, textures, petite lumière, petit geste. Pas un cours.
4. **Papa et maman parlent** (répliques). Bravo / questions / discussion adaptés à la scène. Pas « papa sourit ». Pas « maman est là » à la place d’une réplique.
5. **POS-001** : dire quoi faire, jamais décrire le geste dangereux.
6. **Troupe enfant uniquement :** Amir, Aniss, Sarah, Chouchou, Mila, Nino, Nina, Raphaël, Victorino, Victorina. Un héros, au plus un autre enfant, papa et/ou maman. Remplacer Tom, Lina, Iris, Léa, etc.
7. Adultes = **papa** / **maman** (pas Lucas, Céline, Luca…).
8. N1 : ~8 mots/phrase. N2 : < 16. N3 : un peu plus, encore oral.
9. Garder les mêmes `chunk_id` et `kind`. Ne pas casser les options / `default_next` des ramifiées.
10. `script` = `role|phrase` une phrase par ligne (`narrateur`, `papa`, `maman`, `enfant-m` / `enfant-f`). `text` = les phrases du script collées avec des espaces.
11. Durée ≥ 3 min : allonger par des détails et des répliques, pas par des slogans. Plusieurs passages : certains portent la leçon, d’autres racontent.
12. **Pas d’audio. Pas de bake. Pas de git.**

### Exemples de *manières* (à ne pas coller)

Citation fondateur (prénoms d’illustration ; dans le texte : troupe D16 + papa/maman) :

> il etait une fois, dans un petit village, une petite famille heureuse, un enfant constentin, un papa luca, et une maman celine. un jour pluvieux constentin n'a paas pu sortir au paroc il est resté à la maison. en ce moment même, constentin joue au salon.

> ceci est l'histoire d'un enfant heureux qui s'appelait constentin, il vivait avec son papa lucas et sa maman celine dans une belle maison. la maison se trouvait dans un village très lointin. en ce moment dans ce village il pleut. constentin ne peut pas sortir au parc. il est au salon entrain de jouer avec des legos, ....

Ce sont **deux manières**. Inventer **autre chose** pour chaque fichier. Voir `gestion_projet/decisions/ECHANGES.md` §7.

## Fichiers

```
python stories/outils/rewrite_story.py dump <STORY_ID>
# lit stories/rewrites/<STORY_ID>/source.json
# écrit stories/rewrites/<STORY_ID>/merged.json  (tout le récit réécrit)
```

Ne pas appeler `apply` (le parent l’appliquera). `sons` : garder ou enrichir des ids, vide = silence.

Ramifiée : réécrire **tous** les passages (86), surtout la racine. Jamais « On va apprendre ». Les choix restent des lieux/objets neutres.
