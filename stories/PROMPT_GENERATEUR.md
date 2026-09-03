# Brief générateur d’histoires Sentier

Lis `stories/REGLES.md`, `stories/schema.json`, `stories/referentiel/lecons.json` et l’exemple `stories/atomiques/SAN/ATOM-SAN.ALI.001-01.json`.

Tu écris des fichiers JSON **valides**, un fichier par histoire, sans demander d’avis.

## Chemins

- Atomique : `stories/atomiques/<DOMAINE>/ATOM-<LECON>-<NN>.json`
- Ramifiée : `stories/ramifiees/<DOMAINE>/TREE-<DOMAINE>-<NNN>.json`

NN commence à `01`. Si le fichier existe, incrémente (`02`, `03`…).

## JSON atomique

Copie la structure de l’exemple. Un seul chemin. Nœuds : `audio` → `question_lesson` → `feedback` → `ending`. Optionnel : un `audio` d’accroche supplémentaire. **Pas** de `choice_story`.

- `family_model`: `"father_mother_children"`
- `language`: `"fr"`
- `validation.status`: `"PENDING"`
- Texte oral, phrases courtes. N1 : < 12 mots par phrase. N2/N3 : < 16.
- Inclure tous les `required_messages` de la leçon dans le texte du chemin.
- `safe_actions` montrées, pas seulement dites.
- Question : réponse 1–3 mots, `expected_intents` = ceux de la fiche, `wrong_feedback` = conduite sûre seulement.
- Nommer papa et/ou maman. Personnages originaux (Lina, Tom, Nora, Sami, Léa, Hugo, Inès, Jules, Maya, Noé, Adam, Sara, Lila, Kenzo, Zoé, Iris, Nino, Ava…). Pas de franchise.
- Cadre concret : maison, cuisine, parc, école, marché, trajet avec adulte, jardin, ferme.

## JSON ramifié

`kind`: `"ramifiee"`. `root_id` pointe vers le premier nœud.

Trois niveaux de `choice_story`, **exactement 3 options** chacune (N2/N3). N1 ramifié : 3 options quand même car la consigne utilisateur l’exige ; rester en phrases N1.

Schéma d’ids :

```
root (audio)
c1 (choice_story) → a / b / c
  a (audio + question_lesson + feedback)
  c2a (choice_story) → a1 / a2 / a3
    a1 (audio) → c3a1 (choice) → a1x / a1y / a1z (audio+ending chacun)
    ...
```

Au total : 1 + 3 + 9 = 13 scènes narratives de niveau, et **27 endings**.

Chaque option de choix est **narrative et neutre** (lieu, objet, camarade, moment), jamais « le bon geste vs le geste dangereux ».

Chaque chemin jusqu’à la feuille :

1. porte la leçon principale (`required_messages`)
2. peut porter une leçon secondaire compatible du même domaine ou d’un domaine listé compatible
3. a une question_lesson quelque part sur le chemin (au niveau 1 ou 2)
4. fin naturelle distincte

`default_next` sur chaque question et chaque choix (silence → première option / feedback sûr).

## Interdits (rappel)

Pas de religion, politique, guerre, arme, crime, deux papas/mamans, diagnostic, humiliation, menace affective, franchise, consigne visuelle, description d’un geste dangereux.

Framing `positive_only_critical` : pieds/mains/place du corps + adulte nommé. Jamais « ne cours pas sur la route », jamais « ne mets pas ça dans la prise ». Dire : « les pieds restent sur le trottoir », « on appelle papa ou maman pour la lumière ».

## Couverture

Écris **uniquement** les leçons/domaines assignés dans ta tâche. Histoire unique, pas de copier-coller entre fichiers. Varie lieux, prénoms, objets.

Après écriture, ne lance pas le validateur global (le parent s’en charge). Relis chaque JSON (virgules, ids `next` existants, `ending` sans `next`).
