# F-NAR-008 — Récit captivant (texte d’abord)

Les histoires actuelles enchaînent des **scénarios de leçon**. L’enfant n’a pas l’impression qu’une histoire **commence** et **se termine**. On dirait un cours.

## Principe

Un **fil rouge** (aventure, envie, petit fait) **dirige** le récit. Les leçons **se greffent** dessus, elles ne le remplacent pas.

| Oui | Non |
| --- | --- |
| Un début (quelque chose commence) | Entrer direct dans la consigne |
| Un milieu (on veut, on cherche, on goûte, on attend) | Répéter la leçon à chaque phrase |
| Une fin (c’est fini, on a vécu ça) | « L’histoire est finie » seul, sans clôture |
| Leçon dans l’action | Leçon = tout le texte |

## Processus (ne pas toucher l’xlsx d’origine avant fusion)

1. Extraire : `python stories/outils/rewrite_story.py dump <story_id>`
2. **N agents en parallèle** écrivent `stories/rewrites/<story_id>/agent_<n>.json` (l’xlsx source reste intact).
3. Fusion : `python stories/outils/rewrite_story.py merge <story_id>` → `merged.json`
4. Remplacement : `python stories/outils/rewrite_story.py apply <story_id>` (l’ancien xlsx est remplacé).

Une histoire à la fois (plusieurs agents **sur la même** histoire). Texte d’abord ; audio plus tard.

## JSON agent

Mêmes `chunk_id` et `kind`. Champs : `fil_rouge`, `title`, `chunks[]` avec `text`, `script`, `sons`, `length_scale_piper`, `rate_label`.

`sons` vide = silence. Bruit **puis** calme, jamais nappe. Script `role|phrase`. N1 phrases courtes. REGLES.md inchangé.
