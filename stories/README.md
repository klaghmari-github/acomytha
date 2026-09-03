# Corpus d’histoires Sentier

Histoires éducatives audio pour enfants de 3 à 6 ans. Chaque fichier JSON est un arbre exécutable (un chemin unique pour les atomiques, un graphe à 3 niveaux pour les ramifiées).

## Dossiers

| Chemin | Contenu |
| --- | --- |
| `referentiel/lecons.json` | Catalogue des leçons (Source Unique v3.0 + titres CHILD_AUDIO v3.1) |
| `atomiques/` | Histoires linéaires, une leçon, sans bifurcation |
| `ramifiees/` | Arbres à 3 niveaux de choix, ≥ 3 branches à chaque niveau |
| `outils/validate.py` | Validateur déterministe (lexique, graphe, contrat pédagogique) |
| `REGLES.md` | Contraintes éditoriales non négociables |
| `schema.json` | Schéma JSON v1 |
| `rapports/` | Sorties du validateur |

## Identifiants

- Atomique : `ATOM-<LECON>-<NN>` exemple `ATOM-SAN.ALI.001-01`
- Ramifiée : `TREE-<DOMAINE>-<NNN>` exemple `TREE-SAN-001`

## Génération

Le générateur n’auto-approuve pas. Statut initial `PENDING`. Le validateur pose `APPROVED_TEXT` seulement s’il n’y a aucun finding bloquant.

```bash
python3 stories/outils/validate.py
```
