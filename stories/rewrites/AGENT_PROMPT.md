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

- Conte : il était une fois, un petit village, une famille heureuse… un jour de pluie… en ce moment, l’enfant joue au salon.
- Présentation : ceci est l’histoire d’un enfant heureux… une belle maison dans un village lointain… en ce moment il pleut… il est au salon avec des cubes.

Inventer **autre chose** pour chaque fichier.

## Fichiers

```
python stories/outils/rewrite_story.py dump <STORY_ID>
# lit stories/rewrites/<STORY_ID>/source.json
# écrit stories/rewrites/<STORY_ID>/merged.json  (tout le récit réécrit)
```

Ne pas appeler `apply` (le parent l’appliquera). `sons` : garder ou enrichir des ids, vide = silence.

Ramifiée : réécrire **tous** les passages (86), surtout la racine. Jamais « On va apprendre ». Les choix restent des lieux/objets neutres.
