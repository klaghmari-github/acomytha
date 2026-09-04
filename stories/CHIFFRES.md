# Chiffres exacts du corpus

Comptage sur les xlsx (`stories/arbres/` + `stories/archive/arbres/`) et `stories/referentiel/lecons.xlsx`.  
**1449 histoires. 85 leçons. 13 thèmes.** Toutes les histoires ont au moins une question.

## Leçons

| | |
| --- | ---: |
| Leçons | **85** |
| Thèmes (domaines) | **13** |
| Sous-domaines | **44** |

Chaque histoire a un `lesson_id` parmi ces 85. Aucune leçon sans histoire. Aucune histoire hors référentiel.

| Thème | Leçons |
| --- | ---: |
| Émotions | 12 |
| Relations | 10 |
| Santé et quotidien | 9 |
| Sécurité | 9 |
| Différences du quotidien | 8 |
| Vie concrète | 7 |
| Temps et nature | 6 |
| Autonomie | 5 |
| Jeux et sport | 5 |
| Famille et confiance | 4 |
| Monde vivant | 4 |
| Vie collective | 3 |
| Langage et logique | 3 |
| **Total** | **85** |

## Histoires

Les totaux corpus (1449 / 685 / 764) sont stables. Le split live / archive bouge quand un ramifié repris passe de `archive/arbres/` à `arbres/`.

| | Corpus | Live `arbres/` | Archive |
| --- | ---: | ---: | ---: |
| **Total** | **1449** | **764** | **685** |
| Atomiques (`ATOM-*`) | 685 | 685 | 0 |
| Ramifiées (`TREE-*`) | 764 | 79 | 685 |

Familles ramifiées live : Autonomie 44, Vie collective 35 (COL entière). Le reste (DIF, EMO, FAM, JEU, LAN, REL, SAN, SEC, SOC, TMP, VIV) est encore en archive.

Une ramifiée a 86 passages (dont 16 nœuds question, 13 nœuds à 3 options, 27 fins). Une atomique a typiquement 5 passages, dont **1 question ouverte** (réponse parlée, pas 3 boutons).

## Questions

**1449 / 1449** histoires ont une question. Aucune histoire sans question.

| | Avec question | Sans question |
| --- | ---: | ---: |
| Atomiques | 685 | 0 |
| Ramifiées | 764 | 0 |

| Type | Quoi |
| --- | --- |
| Atomique | 1 `passage_question` — l’enfant **dit** la réponse |
| Ramifiée | 16 questions : `transition_question` (3 options de lieu/objet) + `passage_question` (réponse parlée) |

## Bandes d’âge (corpus)

| | N1 | N2 | N3 |
| --- | ---: | ---: | ---: |
| Corpus | 404 | 567 | 478 |
| Live | 201 | 312 | 251 |
| Archive | 203 | 255 | 227 |
